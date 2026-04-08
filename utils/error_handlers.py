import functools
import logging
import streamlit as st
import os

logger = logging.getLogger(__name__)

def robust_ml_handler(func):
    """
    Декоратор для захисного програмування в ML-потоках.
    Відловлює критичні помилки I/O та Shape Mismatch, запобігаючи крашу UI.
    Повертає None у разі помилки.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (FileNotFoundError, IOError) as e:
            msg = "📁 Не знайдено файл моделі або скейлера. Перевірте папку models/"
            logger.error(f"{msg} Detail: {e}")
            st.error(msg)
            return None
        except ValueError as e:
            msg = "📐 Помилка розмірності даних (Shape Mismatch). Матриці не збігаються."
            logger.error(f"{msg} Detail: {e}")
            st.warning(msg)
            return None
        except Exception as e:
            msg = f"🔥 Критична помилка ML-ядра: {str(e)}"
            logger.error(msg, exc_info=True)
            st.error(msg)
            return None
    return wrapper
