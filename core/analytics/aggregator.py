import pandas as pd

from src.core.database import run_query


def aggregate_consumption(
    df: pd.DataFrame, group_by_col: str, num_cols: list
) -> pd.DataFrame:
    """
    Дискретизує та агрегує дані за годинами.
    """
    if df.empty:
        return df

    df_c = df.copy()
    df_c["timestamp"] = pd.to_datetime(df_c["timestamp"])

    return (
        df_c.set_index("timestamp")
        .groupby(group_by_col)[num_cols]
        .resample("1h")
        .mean()
        .reset_index()
        .sort_values([group_by_col, "timestamp"])
        .dropna(subset=["actual_load_mw"])
    )


def add_relative_load(df: pd.DataFrame, group_by_col: str) -> pd.DataFrame:
    """
    Здійснює нормалізацію навантаження до відносних показників (%).
    """
    if df.empty:
        return df

    df_res = df.copy()
    df_res["relative_load"] = df_res.groupby(group_by_col)["actual_load_mw"].transform(
        lambda x: (x / x.max() * 100) if x.max() > 0 else x.fillna(0)
    )
    return df_res


def get_history_live(substation_name: str | None) -> pd.DataFrame:
    """
    Завантажує історичні дані споживання з реляційної БД за останні 72 години.
    """
    try:
        if substation_name:
            sql = """
                SELECT m.timestamp, m.actual_load_mw, m.temperature_c, m.health_score
                FROM LoadMeasurements m
                JOIN Substations s ON m.substation_id = s.substation_id
                WHERE s.substation_name = :sub
                  AND m.timestamp >= (SELECT MAX(timestamp) FROM LoadMeasurements) - INTERVAL '72 hours'
                ORDER BY m.timestamp ASC
            """
            return run_query(sql, {"sub": substation_name})
        else:
            sql = """
                SELECT timestamp, SUM(actual_load_mw) AS actual_load_mw, 
                AVG(temperature_c) AS temperature_c, AVG(health_score) AS health_score
                FROM LoadMeasurements
                WHERE timestamp >= (SELECT MAX(timestamp) FROM LoadMeasurements) - INTERVAL '72 hours'
                GROUP BY timestamp
                ORDER BY timestamp ASC
            """
            return run_query(sql)
    except Exception as exc:
        return pd.DataFrame({"error": [str(exc)]})


def get_history_csv(substation_name: str | None = None) -> pd.DataFrame:
    """
    Зчитує історичні покази за останні 48 годин з еталонного датасету (Kaggle).
    """
    try:
        from src.core.kaggle_loader import load_kaggle_data

        df = load_kaggle_data()

        if substation_name:
            df = df[df["substation_name"] == substation_name]

        if not df.empty:
            max_ts = df["timestamp"].max()
            df = df[df["timestamp"] >= max_ts - pd.Timedelta(hours=48)]

        return df.sort_values("timestamp")
    except Exception as exc:
        return pd.DataFrame({"error": [str(exc)]})
