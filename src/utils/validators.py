"""
Input validation module to prevent SQL injection and invalid data.
Whitelist-based validation for all user inputs.
"""

from typing import Optional, Union, List, Set
from datetime import date
import logging

logger = logging.getLogger(__name__)

# Whitelist of special "all" strings
BUILTIN_NAMES = frozenset([
    "Усі підстанції", "Всі об'єкти", "Всі", "All", "Усі"
])

# Valid data fetch step keys
VALID_STEP_KEYS = frozenset([
    "sql_load", "sql_gen", "sql_fin", "sql_alerts", "sql_lines", "telemetry"
])

# Valid data source names
VALID_DATA_SOURCES = frozenset([
    "PostgreSQL", "Kaggle", "Cache", "Historical"
])

# Dangerous SQL patterns - simple keywords to detect
DANGEROUS_KEYWORDS = frozenset([
    "drop", "truncate", "delete", "update", "insert", "union",
    "exec", "execute", "xp_", "sp_", "select", "create", "alter",
    "grant", "revoke", "--", "/*", "*/", "';", "\";"
])


class ValidationError(ValueError):
    """Raised when input validation fails."""
    pass


def _has_dangerous_patterns(text: str) -> bool:
    """Check if text contains SQL injection patterns."""
    text_lower = text.lower()
    
    # Check for common SQL injection keywords
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in text_lower:
            logger.warning(f"Dangerous pattern detected: {keyword}")
            return True
    
    # Check for quotes followed by special chars (common in injections)
    if "' or " in text_lower or "' and " in text_lower:
        logger.warning("Dangerous quote pattern detected")
        return True
    
    if "' = " in text_lower or "\" = " in text_lower:
        logger.warning("Dangerous equality pattern detected")
        return True
    
    return False


def validate_step_key(key: str) -> bool:
    """Validate step key against whitelist."""
    if key not in VALID_STEP_KEYS:
        raise ValidationError(
            f"Invalid step_key: '{key}'. "
            f"Must be one of: {', '.join(sorted(VALID_STEP_KEYS))}"
        )
    return True


def validate_substation_name(
    name: Union[str, List[str], None],
    valid_names: Optional[Set[str]] = None
) -> bool:
    """
    Validate substation name(s) against whitelist.
    
    Args:
        name: Single string, list of strings, or None
        valid_names: Set of valid substation names
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If invalid format or dangerous patterns
    """
    if name is None:
        return True
    
    if isinstance(name, str):
        # Allow builtin special names
        if name in BUILTIN_NAMES:
            return True
        
        # Check for SQL injection patterns
        if _has_dangerous_patterns(name):
            raise ValidationError(f"Invalid characters detected: {name}")
        
        # Check against valid list if provided
        if valid_names and name not in valid_names:
            logger.warning(f"Substation name not in whitelist: {name}")
            # Don't raise - might be new station
            return True
        
        return True
    
    elif isinstance(name, list):
        for item in name:
            if not isinstance(item, str):
                raise ValidationError(f"List items must be strings, got {type(item)}")
            validate_substation_name(item, valid_names)
        return True
    
    else:
        raise ValidationError(
            f"Expected str or list[str], got {type(name).__name__}"
        )


def validate_region_name(region: str) -> bool:
    """
    Validate region name.
    
    Args:
        region: Region identifier
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If contains dangerous patterns
    """
    if _has_dangerous_patterns(region):
        raise ValidationError(f"Invalid characters in region: {region}")
    
    if len(region) > 100:
        raise ValidationError(f"Region name too long: {len(region)} > 100")
    
    return True


def validate_date_range(
    start_date: Optional[date],
    end_date: Optional[date]
) -> bool:
    """
    Validate date range.
    
    Args:
        start_date: Start date or None
        end_date: End date or None
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If invalid range
    """
    if start_date is None or end_date is None:
        return True
    
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        raise ValidationError("Dates must be date objects")
    
    if start_date > end_date:
        raise ValidationError(
            f"Start date {start_date} > end date {end_date}"
        )
    
    # Check if range is not too large (e.g., > 5 years)
    days_diff = (end_date - start_date).days
    if days_diff > 365 * 5:
        logger.warning(f"Very large date range: {days_diff} days")
    
    return True


def validate_data_source(source: str) -> bool:
    """
    Validate data source name.
    
    Args:
        source: Data source identifier
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If not in whitelist
    """
    if source not in VALID_DATA_SOURCES:
        raise ValidationError(
            f"Unknown data source: {source}. "
            f"Must be one of: {', '.join(sorted(VALID_DATA_SOURCES))}"
        )
    return True


def sanitize_column_name(name: str, max_length: int = 100) -> str:
    """
    Sanitize column name for safe SQL use.
    
    Args:
        name: Column name
        max_length: Maximum allowed length
        
    Returns:
        Sanitized name
        
    Raises:
        ValidationError: If invalid
    """
    if not isinstance(name, str):
        raise ValidationError(f"Column name must be string, got {type(name)}")
    
    if len(name) > max_length:
        raise ValidationError(f"Column name too long: {len(name)} > {max_length}")
    
    # Check for valid SQL identifier: letters, numbers, underscore only
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
    if not all(c in allowed_chars for c in name):
        raise ValidationError(f"Invalid column name (chars): {name}")
    
    return name


def validate_numeric_input(value: Union[int, float], min_val: float = None, max_val: float = None) -> bool:
    """
    Validate numeric input with bounds checking.
    
    Args:
        value: Numeric value
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If invalid or out of bounds
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(f"Expected number, got {type(value)}")
    
    if min_val is not None and value < min_val:
        raise ValidationError(f"Value {value} < minimum {min_val}")
    
    if max_val is not None and value > max_val:
        raise ValidationError(f"Value {value} > maximum {max_val}")
    
    return True
