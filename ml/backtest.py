import gc
import logging
from typing import Tuple, Optional, Dict, List, Any

import numpy as np
import pandas as pd

from src.core.database import run_query
from ml.predict_v2 import load_resources, DEFAULT_WINDOW_SIZE
from ml.vectorizer import select_features_v2, get_latest_window
from utils.error_handlers import robust_ml_handler

from ml.metrics_engine import perform_statistical_audit, finalize_backtest_metrics, _get_scaling_factor, TEST_SIZE_HOURS

logger = logging.getLogger(__name__)

@robust_ml_handler
def evaluate_last_24h(substation_name: str, version: str, source_type: str = "Live") -> Optional[Dict[str, float]]:
    """Runs a 1-Step-Ahead vectorized evaluation strictly on the LAST 24 Hours."""
    try:
        model, scaler = load_resources(version)
        if not model or not scaler:
            return None
            
        try:
            ws = int(model.get_inputs()[0].shape[1]) if model.get_inputs()[0].shape[1] else DEFAULT_WINDOW_SIZE
        except Exception:
            ws = DEFAULT_WINDOW_SIZE
            
        from ml.vectorizer import get_latest_window, select_features_v2
        
        sv, _, _, _ = get_latest_window(
            substation_name, source_type, version, 
            offset_hours=0, window_size=24 + ws
        )
        if sv is None or len(sv) < 24 + ws:
            return None
            
        values = select_features_v2(sv, version)
        
        scale_factor = _get_scaling_factor(values, scaler, version, substation_name, source_type=source_type)
        if scale_factor != 1.0:
            values[:, 0] *= scale_factor
                
        X_batch = np.array([scaler.transform(values[i : i + ws]) for i in range(24)]).astype(np.float32)
        preds_scaled = model.run(None, {model.get_inputs()[0].name: X_batch})[0][:, 0]
        
        n_sc = scaler.n_features_in_
        dummy = np.zeros((24, n_sc))
        dummy[:, 0] = preds_scaled
        unscaled = scaler.inverse_transform(dummy)
        p = unscaled[:, 0] / scale_factor
        
        a = (values[-24:, 0] / scale_factor)
        
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        rmse = np.sqrt(mean_squared_error(a, p))
        mae = mean_absolute_error(a, p)
        r2 = r2_score(a, p)
        sigma = float(np.std(a - p))
        
        import gc; gc.collect()
        
        return {
            "rmse": rmse, "mae": mae, "r2": r2,
            "accuracy": max(0, min(100, r2 * 100)) if r2 > 0.0 else 0.0,
            "confidence": max(0, min(100, r2 * 100)) if r2 > 0.0 else 0.0,
            "sigma": sigma
        }
    except Exception as e:
        logger.error(f"1-Step-Ahead Eval Failed: {e}", exc_info=True)
        return None

@robust_ml_handler
def run_backtest_step(version: str, shared_values: np.ndarray, current_idx: int, batch_size: int = 24) -> List[float]:
    """Executes a segment of predictions for an interactive backtest session."""
    model, scaler = load_resources(version)
    if not model or not scaler:
        return []
    
    values = select_features_v2(shared_values, version)
    
    sf = _get_scaling_factor(values, scaler, version, substation_name=None)
    if sf != 1.0:
        values = values.copy()
        values[:, 0] *= sf

    try:
        window_size = int(model.get_inputs()[0].shape[1]) if model.get_inputs()[0].shape[1] else DEFAULT_WINDOW_SIZE
    except Exception:
        window_size = DEFAULT_WINDOW_SIZE
        
    preds_scaled = []
    end_idx = min(current_idx + batch_size, TEST_SIZE_HOURS)
    
    try:
        for i in range(current_idx, end_idx):
            x_window = values[i : i + window_size]
            if len(x_window) < window_size:
                break
                
            scaled_window = scaler.transform(x_window)
            x_input = scaled_window.reshape(1, window_size, -1).astype(np.float32)
            p = model.run(None, {model.get_inputs()[0].name: x_input})[0][0]
            preds_scaled.append(float(p[0]))
            
    except Exception as e:
        logger.error(f"Error in backtest batch at index {current_idx}: {e}")
        return []
    finally:
        import gc
        gc.collect()
        
    return preds_scaled

@robust_ml_handler
def get_fast_backtest(substation_name: str, version: str, source_type: str = "Live", offset_hours: int = 0) -> Optional[Tuple]:
    """Batch-vectorized backtest for instant Multi-Dashboard metrics."""
    try:
        model, scaler = load_resources(version)
        if not model or not scaler:
            return None
        
        try:
            ws = int(model.get_inputs()[0].shape[1]) if model.get_inputs()[0].shape[1] else DEFAULT_WINDOW_SIZE
        except Exception:
            ws = DEFAULT_WINDOW_SIZE
            
        sv, _, slts, _ = get_latest_window(
            substation_name, source_type, version, 
            offset_hours=offset_hours, window_size=TEST_SIZE_HOURS + ws
        )
        if sv is None:
            return None
        
        values = select_features_v2(sv, version)
        sf = _get_scaling_factor(values, scaler, version, substation_name, source_type=source_type)
        if sf != 1.0:
            values[:, 0] *= sf
            
        X_batch = np.array([scaler.transform(values[i : i + ws]) for i in range(TEST_SIZE_HOURS)]).astype(np.float32)
        all_preds_scaled = model.run(None, {model.get_inputs()[0].name: X_batch})[0][:, 0]
        
        results = finalize_backtest_metrics(version, all_preds_scaled, sv, slts, substation_name, source_type, sf=sf)
        
        gc.collect()
        
        return results
    except Exception as e:
        logger.error(f"Critical Failure in Fast Backtest for {substation_name}: {e}", exc_info=True)
        return None

@robust_ml_handler
def get_backtest_metrics(version: str, shared_values: np.ndarray, shared_last_ts: pd.Timestamp, 
                          substation_name: str = "Усі підстанції", source_type: str = "Live") -> Optional[Tuple]:
    """High-level wrapper for backtest execution (Compatibility layer)."""
    if isinstance(substation_name, list):
        substation_name = substation_name[0] if substation_name else "Усі підстанції"
        
    logger.info(f"🔄 Starting Backtest Audit for {substation_name} [{version}]")
    return get_fast_backtest(substation_name, version, source_type)
