import numpy as np
import pandas as pd

from src.core.database import run_query

WINDOW_SIZE = 24


def get_latest_window(
    substation_name: str | None, source_type: str = "Live", version="v3"
):
    """
    Формує вектор вхідних даних (Window) за останні 24 години для прогнозування.

    :param substation_name: Назва підстанції.
    :param source_type: Джерело даних ('Live' / 'CSV').
    :param version: Версія архітектури моделі ('v1', 'v2', 'v3').
    :return: Кортеж (np.ndarray, dict, pd.Timestamp, list).
    """
    if source_type == "CSV":
        from src.core.kaggle_loader import load_kaggle_data

        df_all = load_kaggle_data()
        if substation_name:
            df_all = df_all[df_all["substation_name"] == substation_name]

        df = df_all.sort_values("timestamp", ascending=False).head(WINDOW_SIZE)
        if df.empty:
            return None, None, None, None
        df = df.iloc[::-1].reset_index(drop=True)
        df["oil_temp"] = 70.0
        df["h2_ppm"] = 20.0
        df["health"] = 100.0
        df["air_temp"] = 15.0

        df["ts"] = pd.to_datetime(df["timestamp"])
        df["hour"] = df["ts"].dt.hour
        df["day"] = df["ts"].dt.weekday
        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
        df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
        df["day_sin"] = np.sin(2 * np.pi * df["day"] / 7)
        df["day_cos"] = np.cos(2 * np.pi * df["day"] / 7)

        if version == "v1":
            cols = ["actual_load_mw"]
        elif version == "v2":
            cols = ["actual_load_mw", "oil_temp", "h2_ppm", "health", "air_temp"]
        else:
            cols = [
                "actual_load_mw",
                "oil_temp",
                "h2_ppm",
                "health",
                "air_temp",
                "hour_sin",
                "hour_cos",
                "day_sin",
                "day_cos",
            ]

        values = df[cols].values
        constants = {"oil": 70.0, "h2": 20.0, "air": 15.0}
        return values, constants, pd.to_datetime(df["timestamp"].iloc[-1]), cols

    # Live режим
    if substation_name:
        sql = """
        SELECT
            AVG(lm.actual_load_mw) AS actual_load_mw,
            AVG(lm.temperature_c) AS temperature_c,
            AVG(lm.h2_ppm) AS h2_ppm,
            AVG(lm.health_score) AS health_score,
            AVG(COALESCE(wr.temperature, 15.0)) AS air_temp,
            DATE_TRUNC('hour', lm.timestamp) AS ts
        FROM LoadMeasurements lm
        JOIN Substations s ON lm.substation_id = s.substation_id
        JOIN Regions r     ON s.region_id = r.region_id
        LEFT JOIN WeatherReports wr 
               ON DATE_TRUNC('hour', wr.timestamp) = DATE_TRUNC('hour', lm.timestamp)
               AND wr.region_id = r.region_id
        WHERE s.substation_name = :sub
        GROUP BY DATE_TRUNC('hour', lm.timestamp)
        ORDER BY ts DESC LIMIT :limit
        """
        df = run_query(sql, {"sub": substation_name, "limit": WINDOW_SIZE})
    else:
        sql = """
            SELECT 
                SUM(avg_load) AS actual_load_mw,
                AVG(avg_temp) AS temperature_c,
                AVG(avg_h2) AS h2_ppm,
                AVG(avg_health) AS health_score,
                AVG(avg_air) AS air_temp,
                ts
            FROM (
                SELECT 
                    DATE_TRUNC('hour', lm.timestamp) AS ts,
                    lm.substation_id,
                    AVG(lm.actual_load_mw)           AS avg_load,
                    AVG(lm.temperature_c)            AS avg_temp,
                    AVG(lm.h2_ppm)                   AS avg_h2,
                    AVG(lm.health_score)             AS avg_health,
                    AVG(COALESCE(wr.temperature, 15.0)) AS avg_air
                FROM LoadMeasurements lm
                LEFT JOIN WeatherReports wr 
                       ON DATE_TRUNC('hour', wr.timestamp) = DATE_TRUNC('hour', lm.timestamp)
                GROUP BY DATE_TRUNC('hour', lm.timestamp), lm.substation_id
            ) s
            GROUP BY ts
            ORDER BY ts DESC LIMIT :limit
        """
        df = run_query(sql, {"limit": WINDOW_SIZE})

    if df.empty or len(df) < WINDOW_SIZE:
        return None, None, None, None

    df = df.iloc[::-1].reset_index(drop=True)
    df = df.ffill().bfill()

    df["ts"] = pd.to_datetime(df["ts"])
    df["hour"] = df["ts"].dt.hour
    df["day"] = df["ts"].dt.weekday

    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
    df["day_sin"] = np.sin(2 * np.pi * df["day"] / 7)
    df["day_cos"] = np.cos(2 * np.pi * df["day"] / 7)

    try:
        if substation_name:
            cap_res = run_query(
                "SELECT capacity_mw FROM Substations WHERE substation_name = :sub",
                {"sub": substation_name},
            )
            capacity_mw = (
                float(cap_res["capacity_mw"].iloc[0]) if not cap_res.empty else 1000.0
            )
        else:
            cap_res = run_query(
                "SELECT SUM(capacity_mw) as capacity_mw FROM Substations WHERE substation_name != 'AEP Region'"
            )
            capacity_mw = (
                float(cap_res["capacity_mw"].iloc[0]) if not cap_res.empty else 10000.0
            )
    except Exception:
        capacity_mw = 1000.0

    constants = {
        "oil": float(df["temperature_c"].iloc[-1]),
        "h2": float(df["h2_ppm"].iloc[-1]),
        "air": float(df["air_temp"].iloc[-1]),
        "capacity": capacity_mw,
    }

    if version == "v1":
        features = ["actual_load_mw"]
    elif version == "v2":
        features = [
            "actual_load_mw",
            "temperature_c",
            "h2_ppm",
            "health_score",
            "air_temp",
        ]
    else:
        features = [
            "actual_load_mw",
            "temperature_c",
            "h2_ppm",
            "health_score",
            "air_temp",
            "hour_sin",
            "hour_cos",
            "day_sin",
            "day_cos",
        ]

    values = df[features].values
    last_ts = pd.to_datetime(df["ts"].iloc[-1])

    return values, constants, last_ts, features


def get_local_scalers(version: str, values: np.ndarray):
    """
    Ініціалізує та навчає локальні скалери для ізоляції даних відповідно до версії.
    """
    from sklearn.preprocessing import MinMaxScaler

    local_scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_window = local_scaler.fit_transform(values)

    target_scaler = None
    if version in ["v2", "v3"]:
        target_scaler = MinMaxScaler(feature_range=(0, 1))
        target_scaler.fit(values[:, 0].reshape(-1, 1))

    return local_scaler, target_scaler, scaled_window


def inverse_scale_predictions(
    predictions: np.ndarray,
    version: str,
    local_scaler,
    target_scaler,
    scaler,
    hours_ahead: int,
):
    """
    Розмасштабовує передбачення назад у фізичні одиниці (МВт, % Health).
    """
    if version == "v1":
        predictions_array = predictions[:, 0].reshape(-1, 1)
        unscaled_fc = local_scaler.inverse_transform(predictions_array)
        load_fc = unscaled_fc[:, 0]
        health_fc = np.full(hours_ahead, 100.0)
    elif version == "v3":
        predictions_array = predictions[:, 0].reshape(-1, 1)
        load_fc = target_scaler.inverse_transform(predictions_array)[:, 0]
        placeholder = np.zeros((hours_ahead, 9))
        placeholder[:, 0] = predictions[:, 0]
        if predictions.shape[1] > 1:
            placeholder[:, 3] = predictions[:, 1]
        unscaled_fc = local_scaler.inverse_transform(placeholder)
        health_fc = unscaled_fc[:, 3]
    elif version == "v2":
        predictions_array = predictions[:, 0].reshape(-1, 1)
        load_fc = target_scaler.inverse_transform(predictions_array)[:, 0]
        placeholder = np.zeros((hours_ahead, 5))
        placeholder[:, 0] = predictions[:, 0]
        if predictions.shape[1] > 1:
            placeholder[:, 3] = predictions[:, 1]
        unscaled_fc = local_scaler.inverse_transform(placeholder)
        health_fc = unscaled_fc[:, 3]
    else:
        num_features = scaler.n_features_in_ if hasattr(scaler, "n_features_in_") else 1
        placeholder = np.zeros((hours_ahead, num_features))
        placeholder[:, 0] = predictions[:, 0]
        if predictions.shape[1] > 1:
            placeholder[:, 3] = predictions[:, 1]
        unscaled_fc = scaler.inverse_transform(placeholder)
        load_fc = unscaled_fc[:, 0]
        health_fc = (
            unscaled_fc[:, 3]
            if predictions.shape[1] > 1
            else np.full(hours_ahead, 100.0)
        )

    return load_fc, health_fc
