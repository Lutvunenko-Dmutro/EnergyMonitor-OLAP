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
    # Defensive check for list-type input from UI multiselect
    all_objs = ["Усі підстанції", "Всі", "All", "Усі"]
    is_global = not substation_name or (isinstance(substation_name, list) and any(x in all_objs for x in substation_name)) or substation_name in all_objs

    try:
        if is_global:
            # Case 1: Global Aggregation (All Substations)
            sql = """
                SELECT timestamp, SUM(actual_load_mw) AS actual_load_mw, 
                AVG(temperature_c) AS temperature_c, AVG(health_score) AS health_score
                FROM LoadMeasurements
                WHERE timestamp >= (SELECT MAX(timestamp) FROM LoadMeasurements) - INTERVAL '72 hours'
                GROUP BY timestamp
                ORDER BY timestamp ASC
            """
            return run_query(sql)
        else:
            # Case 2: Specific Substation or Group of Substations
            sub_filter = substation_name if isinstance(substation_name, list) else [substation_name]
            sql = """
                SELECT m.timestamp, SUM(m.actual_load_mw) AS actual_load_mw, 
                       AVG(m.temperature_c) AS temperature_c, AVG(m.health_score) AS health_score
                FROM LoadMeasurements m
                JOIN Substations s ON m.substation_id = s.substation_id
                WHERE s.substation_name = ANY(:sub)
                  AND m.timestamp >= (SELECT MAX(timestamp) FROM LoadMeasurements) - INTERVAL '72 hours'
                GROUP BY m.timestamp
                ORDER BY m.timestamp ASC
            """
            return run_query(sql, {"sub": sub_filter})
    except Exception as exc:
        return pd.DataFrame({"error": [str(exc)]})


def get_history_csv(substation_name: str | None = None) -> pd.DataFrame:
    """
    Зчитує історичні покази за останні 48 годин з еталонного датасету (Kaggle).
    """
    try:
        from src.core.kaggle_loader import load_kaggle_data
        df = load_kaggle_data()

        all_objs = ["Усі підстанції", "Всі", "All", "Усі"]
        if substation_name and substation_name not in all_objs:
            df = df[df["substation_name"] == substation_name]
        else:
            # Aggregate across all stations
            df = df.groupby("timestamp")["actual_load_mw"].sum().reset_index()

        if not df.empty:
            max_ts = df["timestamp"].max()
            df = df[df["timestamp"] >= max_ts - pd.Timedelta(hours=48)]

        return df.sort_values("timestamp")
    except Exception as exc:
        return pd.DataFrame({"error": [str(exc)], "actual_load_mw": [0], "timestamp": [pd.Timestamp.now()]})
