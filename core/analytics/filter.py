from app.config import DataKeys


def filter_dataframe(df, region, dates, dataset_name, substation="Усі підстанції"):
    """
    Фільтрує вхідний DataFrame на основі обраних критеріїв.

    :param df: Вхідний DataFrame.
    :param region: Обраний регіон для аналізу.
    :param dates: Кортеж дат (start_date, end_date).
    :param dataset_name: Ідентифікатор типу даних.
    :param substation: Назва підстанції або перелік.
    :return: Відфільтрований DataFrame.
    """
    if df.empty:
        return df

    df_filtered = df.copy()

    # 1. Логіка регіону
    if (
        region != DataKeys.ALL_REGIONS
        and region != "США (PJM Interconnection)"
        and "region_name" in df_filtered.columns
    ):
        df_filtered = df_filtered[df_filtered["region_name"] == region]

    # 2. Логіка підстанції
    if "substation_name" in df_filtered.columns:
        if isinstance(substation, list) and substation:
            if "Усі підстанції" not in substation:
                df_filtered = df_filtered[
                    df_filtered["substation_name"].isin(substation)
                ]
        elif isinstance(substation, str) and substation != "Усі підстанції":
            df_filtered = df_filtered[df_filtered["substation_name"] == substation]

    # 3. Логіка дати (Виняток для alerts)
    if dataset_name != "alerts":
        if (
            "timestamp" in df_filtered.columns
            and isinstance(dates, tuple)
            and len(dates) == 2
        ):
            start_date, end_date = dates
            mask = (df_filtered["timestamp"].dt.date >= start_date) & (
                df_filtered["timestamp"].dt.date <= end_date
            )
            df_filtered = df_filtered.loc[mask]

    return df_filtered
