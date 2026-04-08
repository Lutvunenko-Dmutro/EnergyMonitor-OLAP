import gc
import logging
from typing import Tuple, Optional

import numpy as np
import pandas as pd

from ml.vectorizer import get_latest_window, select_features_v2
from utils.error_handlers import robust_ml_handler

from ml.model_loader import load_resources, _get_substation_peak_automated, DEFAULT_WINDOW_SIZE

logger = logging.getLogger(__name__)

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
    """Generates high-fidelity energy forecasts with architectural rigor."""
    if substation_name is None:
        return pd.DataFrame(), "Substation name must be provided."

    try:
        model, scaler = load_resources(version)
        if model is None or scaler is None:
            return pd.DataFrame(), "Model resources unavailable."

        try:
            window_size = int(model.get_inputs()[0].shape[1]) if model.get_inputs()[0].shape[1] else DEFAULT_WINDOW_SIZE
        except Exception:
            window_size = DEFAULT_WINDOW_SIZE
            
        values, constants_res, last_ts, _ = get_latest_window(
            substation_name, source_type, version, offset_hours=offset_hours, window_size=window_size
        )
        # Use merged defaults (prefer passed constants)
        if hasattr(constants_res, "copy"):
            merged_consts = constants_res.copy() if constants_res else {}
            if constants: merged_consts.update(constants)
            constants = merged_consts
        
        if values is None:
            return pd.DataFrame(), "Input telemetry window is empty or insufficient."

        values = select_features_v2(values, version)
        n_features = values.shape[1]
        
        scale_factor = 1.0
        original_last_load = float(values[-1, 0])
        glb_max = float(getattr(scaler, "data_max_", [5269])[0])

        if substation_name and substation_name not in ["Усі підстанції", "Всі об'єкти", "Всі", "All", "Усі"]:
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

        current_window = scaler.transform(values)
        
        future_ts = [last_ts + pd.Timedelta(hours=i+1) for i in range(hours_ahead)]
        if n_features >= 9:
            h_idx = np.array([ts.hour for ts in future_ts])
            d_idx = np.array([ts.weekday() for ts in future_ts])
            sin_h, cos_h = np.sin(2 * np.pi * h_idx / 24), np.cos(2 * np.pi * h_idx / 24)
            sin_d, cos_d = np.sin(2 * np.pi * d_idx / 7), np.cos(2 * np.pi * d_idx / 7)

        all_stage_predictions = []
        
        norm_temp_shift = 0.0
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
        
        input_name = model.get_inputs()[0].name
        for i in range(hours_ahead):
            x_input = current_window.reshape(1, window_size, n_features).astype(np.float32)
            # ONNX Inference: model.run([output_names], {input_name: input_data})
            ort_outs = model.run(None, {input_name: x_input})
            pred_s = ort_outs[0][0]  # First output, first batch element
            pred_s[0] = np.clip(pred_s[0], 0, 1.1)
            all_stage_predictions.append(pred_s)

            new_row = current_window[-1].copy()
            new_row[0] = pred_s[0]
            
            if n_features > 4 and target_norm_temp is not None:
                new_row[4] = target_norm_temp 
                if norm_health is not None:
                    new_row[3] = norm_health 
            
            if n_features >= 9:
                new_row[5:9] = [sin_h[i], cos_h[i], sin_d[i], cos_d[i]]
            
            current_window = np.append(current_window[1:], [new_row], axis=0)

        n_sc = scaler.n_features_in_
        dummy = np.zeros((hours_ahead, n_sc))
        preds_p = np.array(all_stage_predictions)
        dummy[:, 0] = preds_p[:, 0]
        if preds_p.shape[1] > 1 and n_sc > 3:
            dummy[:, 3] = preds_p[:, 1]

        unscaled_raw = scaler.inverse_transform(dummy)
        load_fc = unscaled_raw[:, 0] / scale_factor
        health_fc = unscaled_raw[:, 3] if n_sc > 3 else np.full(hours_ahead, 100.0)

        # --- SEAMLESS STITCHING LOGIC (Zero-Lag Bias Correction) ---
        first_pred_val = load_fc[0]
        initial_bias = original_last_load - first_pred_val
        
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
            
            # --- AI SANITY CHECKER (Safety Guard) ---
            # Визначаємо фізичну межу для підстанції
            safe_limit = (loc_max * 1.5) if 'loc_max' in locals() and loc_max > 1.0 else (original_last_load * 3.0)
            
            # Якщо ШІ "галюцинує" (прогноз > 1.5x від потужності ПС)
            if np.any(load_fc > safe_limit):
                logger.warning(f"🛡️ Sanity Checker triggered for {substation_name}. AI hallucination detected (> {safe_limit:.1f} MW). Falling back to Seasonal Naive.")
                # Агресивне вирівнювання: 95% сезонності, 5% ШІ
                ALPHA = 0.05 
            else:
                # Стандартне безшовне зшивання (20% ШІ / 80% сезонності)
                ALPHA = 0.20
            
            load_fc = ALPHA * load_fc + (1 - ALPHA) * seasonal_fc
            
        load_fc = np.clip(load_fc, 0, None)
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
        
        logger.info(f"🎯 Optimization success: Forecast generated for {substation_name}")
        return df_result, None

    except Exception as exc:
        logger.error(f"Prediction Pipeline Failure: {str(exc)}", exc_info=True)
        return pd.DataFrame(), f"System Error: {str(exc)}"
