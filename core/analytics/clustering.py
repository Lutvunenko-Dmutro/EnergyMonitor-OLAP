import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def cluster_substations(df: pd.DataFrame, n_clusters: int = 3):
    """
    Аналізує навантаження на підстанції та сегментує їх за рівнем ризику.

    :param df: DataFrame з колонками actual_load_mw, substation_name.
    :param n_clusters: Кількість кластерів (дефолт = 3).
    :return: DataFrame з додатковою колонкою 'Status' i 'cluster_id'.
    """
    if df.empty:
        return df

    df_cluster = df[df["substation_name"] != "AEP Region"].copy()

    agg_dict = {
        "avg_load": ("actual_load_mw", "mean"),
        "max_load": ("actual_load_mw", "max"),
    }
    if "temperature" in df_cluster.columns:
        agg_dict["avg_temp"] = ("temperature", "mean")
    elif "temperature_c" in df_cluster.columns:
        agg_dict["avg_temp"] = ("temperature_c", "mean")

    df_grouped = (
        df_cluster.groupby("substation_name").agg(**agg_dict).reset_index().fillna(0)
    )
    if "avg_temp" not in df_grouped.columns:
        df_grouped["avg_temp"] = 20.0  # Фіксований замінник

    if df_grouped.empty:
        return df_grouped

    features = df_grouped[["avg_load", "max_load", "avg_temp"]]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    n_clusters = min(n_clusters, len(df_grouped))
    names = ["🟢 Низьке навантаження", "🟡 Штатний режим", "🔴 Високе навантаження"]

    if n_clusters > 1:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
        df_grouped["cluster_id"] = kmeans.fit_predict(scaled_features)
        cluster_ranking = (
            df_grouped.groupby("cluster_id")["avg_load"].mean().sort_values().index
        )
        labels_map = {idx: names[i] for i, idx in enumerate(cluster_ranking)}
        df_grouped["Status"] = df_grouped["cluster_id"].map(labels_map)
    else:
        df_grouped["Status"] = "🟡 Штатний режим"

    return df_grouped
