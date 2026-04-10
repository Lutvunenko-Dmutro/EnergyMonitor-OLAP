# ═══════════════════════════════════════════════════════════════
# Shared Utilities & Helpers
# ═══════════════════════════════════════════════════════════════
"""
Утиліти, що повторювалися 15+ разів у коді.
Це DRY-pattern для скорочення дублювання.
"""

from typing import Union, List, Optional, Any, Tuple
from datetime import date
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

try:
    from app.types import SubstationSelection
except ImportError:
    SubstationSelection = Union[str, List[str]]

# Builtin "all" keywords
BUILTIN_ALL_NAMES = frozenset([
    "Усі підстанції", "Всі об'єкти", "Всі", "All", "Усі",
    "ALL_REGIONS", "Усі регіони", "USA (PJM)", "США (PJM Interconnection)"
])


def is_all_keyword(value: str) -> bool:
    """Check if value matches any 'all' keyword."""
    return str(value).strip() in BUILTIN_ALL_NAMES


def normalize_substation_selection(substation: SubstationSelection) -> Optional[str]:
    """
    Нормалізує вибір підстанції (одна або список) в одну рядок.

    Цей паттерн повторювався 15+ разів у различних lugar коду.
    Тепер робимо в одній функції для DRY-принципу.

    Args:
        substation: Назва підстанції (str) або список ({str})

    Returns:
        Одна назва підстанції як рядок або None

    Examples:
        >>> normalize_substation_selection("Київ ТЕС")
        'Київ ТЕС'
        >>> normalize_substation_selection(["Київ ТЕС", "Харків ТЕС"])
        'Київ ТЕС'
        >>> normalize_substation_selection([])
        'Усі підстанції'
        >>> normalize_substation_selection(None)
        None
    """
    if substation is None:
        return None
    
    if isinstance(substation, list):
        return substation[0] if substation else "Усі підстанції"
    
    return str(substation)


def is_valid_date_range(start_date: Optional[date], end_date: Optional[date], max_days: int = 365 * 5) -> bool:
    """
    Перевіряє, чи дата-діапазон валідний.

    Args:
        start_date: Початкова дата
        end_date: Кінцева дата
        max_days: Максимальна довжина діапазону (5 років за замовчуванням)

    Returns:
        True якщо start_date <= end_date, інакше False
    """
    if start_date is None or end_date is None:
        return False
    
    if start_date > end_date:
        return False
    
    # Check if range is too large
    if (end_date - start_date).days > max_days:
        logger.warning(f"Very large date range: {(end_date - start_date).days} days")
    
    return True


def get_safe_column_list(df: pd.DataFrame, expected_columns: Optional[List[str]] = None) -> List[str]:
    """
    Повертирає список колонок, які існують у DataFrame.
    Проігнорує колонки, що не існують (безопасно).

    Args:
        df: DataFrame для перевірки
        expected_columns: Список очікуваних колонок (опціонально)

    Returns:
        Список ТІЛЬКИ існуючих колонок
    """
    if not isinstance(df, pd.DataFrame):
        return []
    
    if expected_columns is None:
        return list(df.columns)
    
    return [col for col in expected_columns if col in df.columns]


def filter_by_column(
    df: pd.DataFrame,
    column: str,
    value: Optional[Union[str, List[str]]] = None,
    keep_all_keyword: bool = True
) -> pd.DataFrame:
    """
    Filter DataFrame by column value(s).
    Eliminates duplicated filtering logic (~7 instances in codebase).

    Args:
        df: Input DataFrame
        column: Column name
        value: Single value or list of values
        keep_all_keyword: If True, "All" keywords bypass filter

    Returns:
        Filtered DataFrame
    """
    if value is None or column not in df.columns:
        return df
    
    # Handle "all" keywords
    if isinstance(value, str) and keep_all_keyword and is_all_keyword(value):
        return df
    
    # Single value filter
    if isinstance(value, str):
        return df[df[column] == value]
    
    # Multiple values filter
    if isinstance(value, list):
        values_to_filter = [v for v in value if not is_all_keyword(str(v))]
        if not values_to_filter:
            return df
        return df[df[column].isin(values_to_filter)]
    
    return df


def filter_by_date(
    df: pd.DataFrame,
    date_column: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> pd.DataFrame:
    """
    Filter DataFrame by date range.
    Eliminates duplicated date filtering (~5 instances).

    Args:
        df: Input DataFrame
        date_column: Column with dates
        start_date: Start date (inclusive)
        end_date: End date (inclusive)

    Returns:
        Filtered DataFrame
    """
    if start_date is None and end_date is None:
        return df
    
    if date_column not in df.columns:
        return df
    
    df_copy = df.copy()
    
    # Ensure datetime type
    if not pd.api.types.is_datetime64_any_dtype(df_copy[date_column]):
        try:
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        except Exception as e:
            logger.error(f"Could not convert to datetime: {e}")
            return df
    
    # Extract dates for comparison
    dates = df_copy[date_column].dt.date if hasattr(df_copy[date_column], 'dt') else df_copy[date_column]
    
    # Apply filters
    if start_date is not None and end_date is not None:
        mask = (dates >= start_date) & (dates <= end_date)
    elif start_date is not None:
        mask = dates >= start_date
    else:
        mask = dates <= end_date
    
    return df_copy[mask]


def safe_divide(numerator: Union[int, float], denominator: Union[int, float], default: float = 0.0) -> float:
    """Safe division with default on zero division."""
    try:
        if denominator == 0:
            return default
        return float(numerator) / float(denominator)
    except (TypeError, ValueError):
        return default


def clip_value(value: Union[int, float], min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Clip value to range."""
    try:
        return float(np.clip(value, min_val, max_val))
    except (TypeError, ValueError):
        return min_val


def batch_list(items: List[Any], batch_size: int = 100) -> List[List[Any]]:
    """Split list into batches."""
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]


def deduplicate_list(items: List[Any], preserve_order: bool = True) -> List[Any]:
    """Remove duplicates from list."""
    if preserve_order:
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    else:
        return list(set(items))
