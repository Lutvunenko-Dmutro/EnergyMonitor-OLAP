import logging
from typing import Tuple, Optional, Dict, List, Any

import numpy as np
import pandas as pd
from src.core.database import run_query

# --- CONSTANTS ---
DEFAULT_WINDOW_SIZE = 48  # Unified 48h horizon for all V3+ models
logger = logging.getLogger(__name__)


def select_features_v2(data: Any, version: str = "v3") -> np.ndarray:
    """Standardized feature selection for LSTM input tensors.

    Args:
        data: Input data as pd.DataFrame or np.ndarray.
        version: Model version ('v1', 'v2', 'v3').

    Returns:
        NumPy array containing only relevant features in the correct order.
    """
    if data is None:
        return np.array([])

    v1_features = ["actual_load_mw"]
    v2_features = v1_features + ["temperature_c", "h2_ppm", "health_score", "air_temp"]
    v3_features = v2_features + ["hour_sin", "hour_cos", "day_sin", "day_cos"]

    target_f = v3_features if version == "v3" else (v2_features if version == "v2" else v1_features)

    if isinstance(data, pd.DataFrame):
        for col in target_f:
            if col not in data.columns:
                data[col] = 0.0
        return data[target_f].values

    expected_len = len(target_f)
    if data.shape[1] < expected_len:
        padding = np.zeros((data.shape[0], expected_len - data.shape[1]))
        return np.hstack([data, padding])

    return data[:, :expected_len]


def _prepare_features(
    df: pd.DataFrame,
    version: str,
    last_ts_col: str
) -> Tuple[np.ndarray, Dict[str, float], pd.Timestamp, List[str]]:
    """Internal helper to calculate periodic signals and metadata.

    Args:
        df: Processed DataFrame.
        version: Architecture version.
        last_ts_col: Name of the timestamp column.

    Returns:
        Same tuple format as get_latest_window.
    """
    hours = df["ts"].dt.hour
    days = df["ts"].dt.weekday
    df["hour_sin"] = np.sin(2 * np.pi * hours / 24)
    df["hour_cos"] = np.cos(2 * np.pi * hours / 24)
    df["day_sin"] = np.sin(2 * np.pi * days / 7)
    df["day_cos"] = np.cos(2 * np.pi * days / 7)

    constants = {
        "oil": float(df["temperature_c"].iloc[-1]) if "temperature_c" in df.columns else 70.0,
        "h2": float(df["h2_ppm"].iloc[-1]) if "h2_ppm" in df.columns else 20.0,
        "air": float(df["air_temp"].iloc[-1]) if "air_temp" in df.columns else 15.0,
        "health": float(df["health_score"].iloc[-1]) if "health_score" in df.columns else 100.0,
    }

    values = select_features_v2(df, version)
    last_ts = pd.to_datetime(df[last_ts_col].iloc[-1])

    f_names = ["actual_load_mw", "temperature_c", "h2_ppm", "health_score", "air_temp",
               "hour_sin", "hour_cos", "day_sin", "day_cos"]
    f_limit = 9 if version == "v3" else (5 if version == "v2" else 1)

    return values, constants, last_ts, f_names[:f_limit]


def _fetch_window_csv(
    substation_name: Optional[str],
    version: str,
    offset_hours: int,
    window_size: int
) -> Tuple[Optional[np.ndarray], Optional[Dict], Optional[pd.Timestamp], Optional[List[str]]]:
    """Завантажує вікно даних із Kaggle CSV-джерела."""
    from src.core.kaggle_loader import load_kaggle_data
    df_all = load_kaggle_data()

    if substation_name:
        if isinstance(substation_name, list):
            df_all = df_all[df_all["substation_name"].isin(substation_name)]
        else:
            df_all = df_all[df_all["substation_name"] == substation_name]

    if "actual_load_mw" in df_all.columns:
        df_all = df_all.groupby("timestamp")["actual_load_mw"].sum().reset_index()
    elif "load" in df_all.columns:
        df_all = df_all.groupby("timestamp")["load"].sum().reset_index()
        df_all.rename(columns={"load": "actual_load_mw"}, inplace=True)
    else:
        load_col = [c for c in df_all.columns if "load" in c.lower() or "mw" in c.lower()]
        if load_col:
            df_all = df_all.groupby("timestamp")[load_col[0]].sum().reset_index()
            df_all.rename(columns={load_col[0]: "actual_load_mw"}, inplace=True)

    df_all["temperature_c"] = 25.0
    df_all["h2_ppm"] = 20.0
    df_all["health_score"] = 100.0
    df_all["air_temp"] = 15.0

    df = df_all.sort_values("timestamp", ascending=False).iloc[offset_hours: offset_hours + window_size]
    if len(df) < window_size:
        return None, None, None, None

    df = df.iloc[::-1].reset_index(drop=True)
    df["ts"] = pd.to_datetime(df["timestamp"])
    df.interpolate(method='linear', limit_direction='both', inplace=True)
    df.ffill().bfill(inplace=True)

    return _prepare_features(df, version, last_ts_col="timestamp")


def _build_live_sql(substation_name, is_all: bool, window_size: int, offset_hours: int):
    """Будує SQL-запит та параметри для Live-джерела даних."""
    all_indicators = {"Усі підстанції", "Всі об'єкти", "Всі", "All", "Усі"}
    params = {"limit": window_size, "offset": offset_hours}

    if not is_all:
        if isinstance(substation_name, str):
            sub_filter = "s.substation_name = :sub"
            params["sub"] = substation_name
        else:
            sub_filter = "s.substation_name = ANY(:sub)"
            params["sub"] = list(substation_name)

        sql = f"""
        SELECT
            SUM(lm.actual_load_mw) AS actual_load_mw,
            AVG(lm.temperature_c) AS temperature_c,
            AVG(lm.h2_ppm) AS h2_ppm,
            AVG(lm.health_score) AS health_score,
            AVG(COALESCE(wr.temperature, 15.0)) AS air_temp,
            DATE_TRUNC('hour', lm.timestamp) AS timestamp
        FROM LoadMeasurements lm
        JOIN Substations s ON lm.substation_id = s.substation_id
        JOIN Regions r ON s.region_id = r.region_id
        LEFT JOIN WeatherReports wr
               ON DATE_TRUNC('hour', wr.timestamp) = DATE_TRUNC('hour', lm.timestamp)
               AND wr.region_id = r.region_id
        WHERE {sub_filter}
        GROUP BY 6 ORDER BY timestamp DESC LIMIT :limit OFFSET :offset
        """
    else:
        sql = """
        SELECT SUM(avg_load) AS actual_load_mw, AVG(avg_temp) AS temperature_c,
               AVG(avg_h2) AS h2_ppm, AVG(avg_health) AS health_score,
               AVG(avg_air) AS air_temp, ts
        FROM (
            SELECT DATE_TRUNC('hour', lm.timestamp) AS ts, lm.substation_id,
                   AVG(lm.actual_load_mw) AS avg_load, AVG(lm.temperature_c) AS avg_temp,
                   AVG(lm.h2_ppm) AS avg_h2, AVG(lm.health_score) AS avg_health,
                   AVG(COALESCE(wr.temperature, 15.0)) AS avg_air
            FROM LoadMeasurements lm
            LEFT JOIN WeatherReports wr
                ON DATE_TRUNC('hour', wr.timestamp) = DATE_TRUNC('hour', lm.timestamp)
            GROUP BY 1, 2
        ) sub_agg GROUP BY ts ORDER BY ts DESC LIMIT :limit OFFSET :offset
        """

    return sql, params


def get_latest_window(
    substation_name: Optional[str],
    source_type: str = "Live",
    version: str = "v3",
    offset_hours: int = 0,
    window_size: int = DEFAULT_WINDOW_SIZE
) -> Tuple[Optional[np.ndarray], Optional[Dict[str, float]], Optional[pd.Timestamp], Optional[List[str]]]:
    """Fetches and prepares the most recent data window for forecasting.

    Args:
        substation_name: Substation identifier (None for global).
        source_type: 'Live' (DB) or 'CSV' (Kaggle).
        version: Model version for feature selection.
        offset_hours: Rolling offset for backtesting.
        window_size: Number of hours to look back.

    Returns:
        Tuple: (Input array, Last observed constants, Last timestamp, Feature names).
    """
    all_indicators = {"Усі підстанції", "Всі об'єкти", "Всі", "All", "Усі"}
    is_all = (
        not substation_name
        or (isinstance(substation_name, list) and any(x in all_indicators for x in substation_name))
        or substation_name in all_indicators
    )
    if is_all:
        substation_name = None

    # Branch A: CSV (Kaggle/Backtest)
    if source_type == "CSV":
        return _fetch_window_csv(substation_name, version, offset_hours, window_size)

    # Branch B: Live DB
    sql, params = _build_live_sql(substation_name, is_all, window_size, offset_hours)

    df = run_query(sql, params)
    if df.empty or len(df) < window_size:
        return None, None, None, None

    df = df.iloc[::-1].reset_index(drop=True)
    if "ts" in df.columns:
        df.rename(columns={"ts": "timestamp"}, inplace=True)
    df["ts"] = pd.to_datetime(df["timestamp"] if "timestamp" in df.columns else df["ts"])

    if df.isna().any().any():
        df.interpolate(method='linear', limit_direction='both', inplace=True)
        df.ffill().bfill(inplace=True)

    return _prepare_features(df, version, last_ts_col="ts")
