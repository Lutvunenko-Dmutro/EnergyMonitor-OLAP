import gc
import logging
from typing import Tuple, Optional

import numpy as np
import pandas as pd

from ml.vectorizer import get_latest_window, select_features_v2
from utils.error_handlers import robust_ml_handler

from ml.model_loader import load_resources, _get_substation_peak_automated, DEFAULT_WINDOW_SIZE

logger = logging.getLogger(__name__)


# ─── INTERNAL HELPERS ─────────────────────────────────────────────────────────

def _compute_scale_factor(
    values: np.ndarray,
    substation_name: Optional[str],
    source_type: str,
    scaler
) -> Tuple[float, float]:
    """Обчислює коефіцієнт масштабування для адаптації до підстанції."""
    scale_factor = 1.0
    loc_max = 1.0
    skip_names = {"Усі підстанції", "Всі об'єкти", "Всі", "All", "Усі"}
    glb_max = float(getattr(scaler, "data_max_", [5269])[0])

    if substation_name and substation_name not in skip_names:
        if source_type == "CSV":
            loc_max = float(np.max(values[:, 0]))
        else:
            loc_max = _get_substation_peak_automated(substation_name)

        if loc_max > 1.0:
            if glb_max > loc_max * 1.5:
                scale_factor = np.clip(glb_max / loc_max, 1.0, 100.0)
            elif loc_max > glb_max:
                scale_factor = glb_max / loc_max

            if scale_factor != 1.0:
                values[:, 0] *= scale_factor
                logger.info(f"⚖️ Applied Domain Adaptation Scale (x{scale_factor:.4f}) for {substation_name}")

    return scale_factor, loc_max


def _build_norm_overrides(
    n_features: int,
    current_window: np.ndarray,
    scaler,
    temp_shift: float,
    constants: Optional[dict]
) -> Tuple[Optional[float], Optional[float]]:
    """Підготовка нормалізованих перезаписів для температури та здоров'я."""
    norm_health = None
    target_norm_temp = None

    if n_features > 4:
        t_range = scaler.data_max_[4] - scaler.data_min_[4]
        norm_temp_shift = temp_shift / t_range if t_range > 0 else 0.0
        target_norm_temp = np.clip(current_window[-1, 4] + norm_temp_shift, 0.0, 1.0)

        if constants and "health" in constants:
            h_val = float(constants["health"])
            h_min, h_max = scaler.data_min_[3], scaler.data_max_[3]
            h_range = h_max - h_min
            norm_health = (h_val - h_min) / h_range if h_range > 0 else 0.8

    return target_norm_temp, norm_health


def _run_onnx_inference(
    model,
    current_window: np.ndarray,
    window_size: int,
    n_features: int,
    hours_ahead: int,
    future_ts: list,
    target_norm_temp: Optional[float],
    norm_health: Optional[float]
) -> list:
    """Запускає ONNX-модель у рекурентному режимі на hours_ahead кроків."""
    # Передобчислення тригонометрії для майбутніх часових міток
    sin_h = cos_h = sin_d = cos_d = None
    if n_features >= 9:
        h_idx = np.array([ts.hour for ts in future_ts])
        d_idx = np.array([ts.weekday() for ts in future_ts])
        sin_h, cos_h = np.sin(2 * np.pi * h_idx / 24), np.cos(2 * np.pi * h_idx / 24)
        sin_d, cos_d = np.sin(2 * np.pi * d_idx / 7), np.cos(2 * np.pi * d_idx / 7)

    input_name = model.get_inputs()[0].name
    all_stage_predictions = []

    for i in range(hours_ahead):
        x_input = current_window.reshape(1, window_size, n_features).astype(np.float32)
        ort_outs = model.run(None, {input_name: x_input})
        pred_s = ort_outs[0][0]
        pred_s[0] = np.clip(pred_s[0], 0, 1.1)
        all_stage_predictions.append(pred_s)

        new_row = current_window[-1].copy()
        new_row[0] = pred_s[0]
        if n_features > 4 and target_norm_temp is not None:
            new_row[4] = target_norm_temp
            if norm_health is not None:
                new_row[3] = norm_health
        if n_features >= 9 and sin_h is not None:
            new_row[5:9] = [sin_h[i], cos_h[i], sin_d[i], cos_d[i]]

        current_window = np.append(current_window[1:], [new_row], axis=0)

    return all_stage_predictions


def _apply_bias_correction_and_blend(
    load_fc: np.ndarray,
    original_last_load: float,
    values: np.ndarray,
    scale_factor: float,
    hours_ahead: int,
    substation_name: Optional[str]
) -> np.ndarray:
    """Безшовне зшивання (Bias Correction) та сезонне змішування."""
    # --- SEAMLESS STITCHING (Zero-Lag Bias Correction) ---
    initial_bias = original_last_load - load_fc[0]
    decay_steps = min(8, hours_ahead)
    decay_curve = np.ones(hours_ahead)
    for step in range(decay_steps):
        decay_curve[step] = 1.0 - (step / decay_steps)
    if hours_ahead > decay_steps:
        decay_curve[decay_steps:] = 0
    load_fc = load_fc + (initial_bias * decay_curve)

    # --- SEASONS BLENDING (Continuity) ---
    raw_vals = values[:, 0] / scale_factor
    if len(raw_vals) >= hours_ahead:
        template = raw_vals[-hours_ahead:].copy()
        template_ratio = original_last_load / template[0] if (len(template) > 0 and template[0] > 0) else 1.0
        template_ratio = np.clip(template_ratio, 0.8, 1.25)
        seasonal_fc = np.clip(template * template_ratio, 0, None)

        # --- AI SANITY CHECKER ---
        loc_max = _get_substation_peak_automated(substation_name) if substation_name else 0
        safe_limit = (loc_max * 1.5) if loc_max > 1.0 else (original_last_load * 3.0)
        if np.any(load_fc > safe_limit):
            logger.warning(f"🛡️ Sanity Checker triggered for {substation_name}. Falling back to Seasonal Naive.")
            ALPHA = 0.05
        else:
            ALPHA = 0.20
        load_fc = ALPHA * load_fc + (1 - ALPHA) * seasonal_fc

    return np.clip(load_fc, 0, None)


# ─── MAIN FORECAST FUNCTION ───────────────────────────────────────────────────

def _run_baseline_fallback(hours_ahead, values, last_ts):
    """Генерація базового прогнозу при відсутності ШІ-моделей (Seasonal Naive)."""
    logger.warning("🛡️ AI Fallback: Generating Seasonal Naive baseline.")
    template = values[-min(len(values), hours_ahead):, 0]
    future_ts = [last_ts + pd.Timedelta(hours=i + 1) for i in range(hours_ahead)]
    load_fc = np.resize(template, hours_ahead) * np.random.uniform(0.99, 1.01, size=hours_ahead)
    
    all_ts = [last_ts] + future_ts
    load_stitched = np.insert(load_fc, 0, values[-1, 0])
    err_band = load_stitched * 0.20
    
    return pd.DataFrame({
        "timestamp": all_ts,
        "predicted_load_mw": load_stitched,
        "predicted_health_score": np.full(len(all_ts), 100.0),
        "upper_bond": load_stitched + err_band,
        "lower_bond": np.maximum(load_stitched - err_band, 0),
        "is_actual_start": [True] + [False] * hours_ahead
    })

@robust_ml_handler
def get_ai_forecast(
    hours_ahead: int = 24,
    substation_name: Optional[str] = None,
    source_type: str = "Live",
    version: str = "v3",
    offset_hours: int = 0,
    temp_shift: float = 0.0,
    constants: dict = None,
    **kwargs
) -> Tuple[pd.DataFrame, Optional[str]]:
    """Generates high-fidelity energy forecasts with fallback protection."""
    if substation_name is None:
        return pd.DataFrame(), "Substation name must be provided."

    # Initial data reach
    try:
        from ml.model_loader import DEFAULT_WINDOW_SIZE
        values, constants_res, last_ts, _ = get_latest_window(
            substation_name, source_type, version, offset_hours=offset_hours, window_size=DEFAULT_WINDOW_SIZE
        )
        if values is None:
            return pd.DataFrame(), "Telemetry unavailable."
    except Exception as e:
        return pd.DataFrame(), f"Data error: {e}"

    try:
        # 1. Завантаження ресурсів
        model, scaler = load_resources(version)
        if model is None or scaler is None:
            return _run_baseline_fallback(hours_ahead, values, last_ts), "Baseline Fallback (AI offline)"

        try:
            window_size = int(model.get_inputs()[0].shape[1]) if model.get_inputs()[0].shape[1] else DEFAULT_WINDOW_SIZE
        except Exception:
            window_size = DEFAULT_WINDOW_SIZE

        # 2. Отримання вхідного вікна
        values, constants_res, last_ts, _ = get_latest_window(
            substation_name, source_type, version, offset_hours=offset_hours, window_size=window_size
        )
        if hasattr(constants_res, "copy"):
            merged_consts = constants_res.copy() if constants_res else {}
            if constants:
                merged_consts.update(constants)
            constants = merged_consts

        if values is None:
            return pd.DataFrame(), "Input telemetry window is empty or insufficient."

        values = select_features_v2(values, version)
        n_features = values.shape[1]
        original_last_load = float(values[-1, 0])

        # 3. Масштабування під підстанцію
        scale_factor, _ = _compute_scale_factor(values, substation_name, source_type, scaler)

        # 4. Підготовка нормалізованих перезаписів
        current_window = scaler.transform(values)
        target_norm_temp, norm_health = _build_norm_overrides(n_features, current_window, scaler, temp_shift, constants)
        future_ts = [last_ts + pd.Timedelta(hours=i + 1) for i in range(hours_ahead)]

        # 5. ONNX Inference
        all_stage_predictions = _run_onnx_inference(
            model, current_window, window_size, n_features,
            hours_ahead, future_ts, target_norm_temp, norm_health
        )

        # 6. Inverse Transform
        n_sc = scaler.n_features_in_
        dummy = np.zeros((hours_ahead, n_sc))
        preds_p = np.array(all_stage_predictions)
        dummy[:, 0] = preds_p[:, 0]
        if preds_p.shape[1] > 1 and n_sc > 3:
            dummy[:, 3] = preds_p[:, 1]

        unscaled_raw = scaler.inverse_transform(dummy)
        load_fc = unscaled_raw[:, 0] / scale_factor
        health_fc = unscaled_raw[:, 3] if n_sc > 3 else np.full(hours_ahead, 100.0)

        # 7. Bias Correction + Seasonal Blend
        load_fc = _apply_bias_correction_and_blend(load_fc, original_last_load, values, scale_factor, hours_ahead, substation_name)

        # 8. Формування результату
        load_stitched = np.insert(load_fc, 0, original_last_load)
        health_stitched = np.insert(health_fc, 0, constants.get("health", 100.0) if constants else 100.0)
        all_ts_stitched = [last_ts] + future_ts
        error_band = np.array(load_stitched) * 0.13

        df_result = pd.DataFrame({
            "timestamp": all_ts_stitched,
            "predicted_load_mw": load_stitched,
            "predicted_health_score": health_stitched,
            "upper_bond": load_stitched + error_band,
            "lower_bond": np.maximum(load_stitched - error_band, 0),
            "is_actual_start": [True] + [False] * hours_ahead
        })

        del values, current_window, dummy, unscaled_raw
        gc.collect()

        logger.info(f"🎯 Optimization success: Forecast generated for {substation_name}")
        return df_result, None

    except Exception as exc:
        logger.error(f"Prediction Pipeline Failure: {str(exc)}", exc_info=True)
        return pd.DataFrame(), f"System Error: {str(exc)}"
