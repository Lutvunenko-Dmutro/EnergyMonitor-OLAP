from typing import Optional, Union, List, Tuple
from datetime import date
import pandas as pd
import logging

from app.config import DataKeys
from utils.validators import (
    validate_region_name,
    validate_substation_name,
    validate_date_range,
    ValidationError
)

logger = logging.getLogger(__name__)


def filter_dataframe(
    df: pd.DataFrame,
    region: str,
    dates: Optional[Tuple[date, date]],
    dataset_name: str,
    substation: Union[str, List[str]] = "Усі підстанції"
) -> pd.DataFrame:
    """
    Фільтрує вхідний DataFrame на основі обраних критеріїв (з валідацією вводу).

    Args:
        df: Вхідний DataFrame.
        region: Обраний регіон для аналізу (valided vs whitelist).
        dates: Кортеж дат (start_date, end_date).
        dataset_name: Ідентифікатор типу даних.
        substation: Назва підстанції або перелік (valueded vs whitelist).

    Returns:
        Відфільтрований DataFrame.

    Raises:
        TypeError: Якщо df не є DataFrame.
        ValidationError: Якщо input містить підозрілі паттерни.
    """
    # ✅ ВАЛІДАЦІЯ ВХОДЖЕННЯ
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pd.DataFrame, got {type(df)}")
    
    try:
        validate_region_name(region)
        validate_substation_name(substation)
        if isinstance(dates, tuple) and len(dates) == 2:
            validate_date_range(dates[0], dates[1])
    except ValidationError as e:
        logger.error(f"Input validation failed: {e}")
        raise
    
    if df.empty:
        logger.debug("Empty DataFrame provided, returning as-is")
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
