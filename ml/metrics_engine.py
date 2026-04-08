import gc
import numpy as np
import pandas as pd
import scipy.stats as stats
from typing import Dict, Any, Optional, Tuple
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf

from src.core.database import run_query
from utils.error_handlers import robust_ml_handler
from ml.predict_v2 import load_resources

def perform_statistical_audit(errors: np.ndarray) -> Dict[str, Any]:
    """Performs a comprehensive mathematical audit of forecast residuals."""
    if len(errors) < 3:
        return {}
    
    mu, sigma = np.mean(errors), np.std(errors)
    
    # Shapiro-Wilk Normality Test (Scientific Standard)
    try:
        _, p_val = stats.shapiro(errors)
    except Exception:
        p_val = 0.0
        
    return {
        "mu": float(mu),
        "sigma": float(sigma),
        "p_value": float(p_val),
        "is_normal": p_val > 0.05,
        "skew": float(stats.skew(errors)),
        "kurt": float(stats.kurtosis(errors))
    }

def _get_scaling_factor(vals: np.ndarray, scaler: Any, version: str, 
                        substation_name: str = None, source_type: str = "Live") -> float:
    """Automated scaling factor based on substation historical peaks."""
    if not substation_name or substation_name in ["Усі підстанції", "Всі об'єкти", "Всі", "All", "Усі"]:
        return 1.0
        
    try:
        glb_max = float(getattr(scaler, "data_max_", [5269.0])[0])
        
        if source_type == "CSV":
            loc_max = float(np.max(vals[:, 0]))
        else:
            from ml.predict_v2 import _get_substation_peak_automated
            loc_max = _get_substation_peak_automated(substation_name)
            
        if loc_max > 1.0:
            if glb_max > loc_max * 1.5:
                return float(np.clip(glb_max / loc_max, 1.0, 100.0))
            elif loc_max > glb_max:
                return float(glb_max / loc_max)
    except Exception:
        pass
    return 1.0

def _get_ground_truth(sub: str, min_ts: pd.Timestamp, max_ts: pd.Timestamp, source_type: str = "Live") -> pd.DataFrame:
    """Fetches actual load data from the database or CSV loader."""
    if source_type == "CSV":
        from src.core.kaggle_loader import load_kaggle_data
        df_all = load_kaggle_data()
        
        if sub and sub not in ["Усі підстанції", "Всі об'єкти", "Всі", "All", "Усі"]:
            if isinstance(sub, list):
                df_all = df_all[df_all["substation_name"].isin(sub)]
            else:
                df_all = df_all[df_all["substation_name"] == sub]
        
        if not df_all.empty:
            df_all["timestamp"] = df_all["timestamp"].dt.floor("h")
            df_all = df_all.groupby("timestamp")["actual_load_mw"].sum().reset_index()
            
            mask = (df_all["timestamp"] >= min_ts) & (df_all["timestamp"] <= max_ts)
            df_all = df_all[mask].sort_values("timestamp")
            return df_all.rename(columns={"timestamp": "ts"})
        return pd.DataFrame(columns=["ts", "actual_load_mw"])

    if sub and sub not in ["Усі підстанції", "Всі об'єкти", "Всі", "All", "Усі"]:
        sql = """SELECT AVG(actual_load_mw) as actual_load_mw, DATE_TRUNC('hour', timestamp) as ts 
                 FROM LoadMeasurements lm JOIN Substations s ON lm.substation_id = s.substation_id 
                 WHERE s.substation_name = :sub AND lm.timestamp BETWEEN :min AND :max GROUP BY 2 ORDER BY ts ASC"""
        return run_query(sql, {"sub": sub, "min": min_ts, "max": max_ts})
    else:
        sql = """SELECT SUM(actual_load_mw) as actual_load_mw, DATE_TRUNC('hour', timestamp) as ts 
                 FROM LoadMeasurements WHERE timestamp BETWEEN :min AND :max GROUP BY 2 ORDER BY ts ASC"""
        return run_query(sql, {"min": min_ts, "max": max_ts})

def _get_outlier_mask(actual: np.ndarray, preds: np.ndarray) -> np.ndarray:
    """Calculates robust 3-sigma mask to filter sensor noise."""
    valid_mask = ~np.isnan(actual) & ~np.isnan(preds)
    if not np.any(valid_mask):
        return np.array([], dtype=bool)
        
    err = np.abs(actual - preds)
    clean_err = err[valid_mask]
    
    if len(clean_err) == 0:
        return valid_mask
        
    mad = np.median(np.abs(clean_err - np.median(clean_err)))
    threshold = 3.5 * 1.4826 * mad if mad > 0 else 500
    
    return valid_mask & (err <= np.clip(threshold, 100, 5000))

TEST_SIZE_HOURS = 168

@robust_ml_handler
def finalize_backtest_metrics(version: str, all_preds_scaled: np.ndarray, shared_values: np.ndarray, 
                             shared_last_ts: pd.Timestamp, substation_name: str, source_type: str,
                             sf: float = 1.0) -> Optional[Tuple]:
    """Calculates final metrics and merges with database ground truth."""
    _, scaler = load_resources(version)
    
    preds_norm = np.asarray(all_preds_scaled).flatten()[:TEST_SIZE_HOURS]
    dummy = np.zeros((TEST_SIZE_HOURS, scaler.n_features_in_))
    dummy[:, 0] = preds_norm
    predicted = (scaler.inverse_transform(dummy)[:, 0]) / sf
    
    forecast_ts = [shared_last_ts - pd.Timedelta(hours=TEST_SIZE_HOURS - 1 - i) for i in range(TEST_SIZE_HOURS)]
    df_fc = pd.DataFrame({"timestamp": pd.to_datetime(forecast_ts), "predicted_load_mw": predicted})
    df_fc["timestamp"] = df_fc["timestamp"].dt.floor("h") 
    
    df_act = _get_ground_truth(substation_name, df_fc["timestamp"].min(), df_fc["timestamp"].max(), source_type)
    if df_act is None or df_act.empty:
        return None
    
    if "ts" in df_act.columns:
        df_act["ts"] = pd.to_datetime(df_act["ts"]).dt.floor("h")
    
    merged = pd.merge(df_fc, df_act, left_on="timestamp", right_on="ts", how="inner")
    
    actual, preds = merged["actual_load_mw"].values, merged["predicted_load_mw"].values
    mask = _get_outlier_mask(actual, preds)
    
    a_m, p_m = actual[mask], preds[mask]
    if len(a_m) == 0:
        return 0, 0, 0, 0, "No data overlap", merged

    rmse = float(np.sqrt(mean_squared_error(a_m, p_m)))
    mae = float(mean_absolute_error(a_m, p_m))
    mape = float(np.mean(np.abs((a_m - p_m) / a_m)) * 100)
    r2 = float(r2_score(a_m, p_m))
    
    tf.keras.backend.clear_session()
    gc.collect()

    return rmse, mae, mape, r2, None, merged
