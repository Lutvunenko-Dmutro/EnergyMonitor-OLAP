"""
Robust error handling utilities with logging and recovery strategies.
Handles specific exceptions with proper context and recovery options.
"""

import functools
import logging
import streamlit as st
from typing import Callable, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def robust_ml_handler(func: Callable) -> Callable:
    """
    Декоратор для захисного програмування в ML-потоках.
    Відловлює СПЕЦИФІЧНІ помилки (не generic Exception).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Optional[Any]:
        try:
            return func(*args, **kwargs)
        except (FileNotFoundError, IOError) as e:
            logger.error(f"File error: {e}")
            st.error(f"📁 Модель не знайдена: {e}")
            return None
        except ValueError as e:
            logger.error(f"Shape error: {e}")
            st.warning(f"📐 Shape Mismatch: {e}")
            return None
        except Exception as e:
            logger.exception(f"Error in {func.__name__}: {e}")
            st.error(f"🔥 Помилка: {e}")
            return None
    return wrapper


def robust_database_handler(func: Callable = None, default_value: Any = None) -> Callable:
    """
    Декоратор для операцій з БД з підтримкою default_value.
    
    Usage:
        @robust_database_handler
        def my_func(): pass
        
        @robust_database_handler(default_value={})
        def my_func(): pass
    """
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs) -> Optional[Any]:
            try:
                return f(*args, **kwargs)
            except ConnectionError as e:
                logger.warning(f"DB connection failed: {e}")
                return default_value
            except TimeoutError as e:
                logger.warning(f"DB timeout: {e}")
                return default_value
            except KeyError as e:
                logger.error(f"Data structure error: {e}")
                return default_value
            except Exception as e:
                logger.exception(f"Database error: {e}")
                return default_value
        return wrapper
    
    # Support both @robust_database_handler and @robust_database_handler(default_value=...)
    if func is not None:
        return decorator(func)
    else:
        return decorator


def robust_io_handler(func: Callable) -> Callable:
    """Декоратор для операцій I/O."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Optional[Any]:
        try:
            return func(*args, **kwargs)
        except (IOError, OSError, FileNotFoundError) as e:
            logger.error(f"IO error: {e}")
            return None
    return wrapper


class ErrorContext:
    """Context manager для логування операцій."""
    def __init__(self, operation: str):
        self.operation = operation
        self.start = __import__("datetime").datetime.now()
    
    def __enter__(self):
        logger.info(f"▶️ {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = (__import__("datetime").datetime.now() - self.start).total_seconds()
        if exc_type:
            logger.error(f"❌ {self.operation} failed: {exc_type.__name__}")
            return False
        logger.info(f"✅ {self.operation} ({elapsed:.2f}s)")
        return True


def safe_getattr(obj: Any, attr: str, default: Any = None) -> Any:
    """Safe attribute access."""
    try:
        return getattr(obj, attr, default)
    except:
        return default


def safe_dict_access(d: dict, path: str, default: Any = None) -> Any:
    """Safe nested dict access with dot notation."""
    try:
        keys = path.split('.')
        current = d
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return default
