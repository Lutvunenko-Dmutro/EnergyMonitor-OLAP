import gc
import logging
import time
from typing import Dict, Generator, Optional, Tuple, Any

import pandas as pd
import streamlit as st

from src.core import database as db
from src.core import queries as q
from src.services.data.db_services import get_latest_measurements
from src.utils.error_handlers import robust_database_handler, ErrorContext
from src.utils.validators import validate_step_key, ValidationError

logger = logging.getLogger(__name__)

# Глобальний фільтр для уникнення дублювання логів
LOGGED_BOOT_MESSAGES = set()

# Error counters for monitoring
BOOT_ERRORS = {}


# --- ACTIVE LOADING EXTENSIONS ---

@robust_database_handler(default_value={})
def fetch_granular_data(step_key: str) -> Dict[str, pd.DataFrame]:
    """
    Завантажує конкретний підмножина даних для поетапного завантаження.
    З специфічною обробкою помилок для кожного step.
    
    Args:
        step_key: Валідований ключ етапу
        
    Returns:
        Dict з даними або порожній dict при помилці
        
    Raises:
        ValidationError: If step_key not in whitelist
    """
    # ✅ ВАЛІДАЦІЯ INPUT
    try:
        validate_step_key(step_key)
    except ValidationError as e:
        logger.error(f"Invalid step_key: {e}")
        return {}
    
    # Специфічна обробка для кожного step
    try:
        with ErrorContext(f"Fetch step: {step_key}"):
            if step_key == "sql_load":
                return {"load": db.run_query(q.QUERY_LOAD_WEATHER)}
            elif step_key == "sql_gen":
                return {"gen": db.run_query(q.QUERY_GENERATION)}
            elif step_key == "sql_fin":
                return {"fin": db.run_query(q.QUERY_FINANCE)}
            elif step_key == "sql_alerts":
                return {"alerts": db.run_query(q.QUERY_ALERTS)}
            elif step_key == "sql_lines":
                return {"lines": db.run_query(q.QUERY_LINES)}
            elif step_key == "telemetry":
                return {"telemetry": get_latest_measurements()}
            else:
                return {}
    
    except (st.runtime.scriptrunner.StopException, st.errors.StreamlitAPIException):
        raise # Прокидаємо системні сигнали Streamlit далі
    
    except ConnectionError as e:
        logger.warning(f"Connection error on {step_key}: {e}")
        BOOT_ERRORS[step_key] = "connection_failed"
        return {}
    
    except TimeoutError as e:
        logger.warning(f"Timeout on {step_key}: {e}")
        BOOT_ERRORS[step_key] = "timeout"
        return {}
    
    except KeyError as e:
        logger.error(f"Data structure error on {step_key}: {e}")
        BOOT_ERRORS[step_key] = "missing_column"
        return {}
    
    except Exception as e:
        from streamlit.runtime.scriptrunner.exceptions import RerunException
        if isinstance(e, RerunException): raise e
        logger.exception(f"Unexpected error on {step_key}: {e}")
        BOOT_ERRORS[step_key] = type(e).__name__
        return {}


@st.cache_data(show_spinner=False, ttl=300)  # 5 хвилин — Kaggle дані завантажуються lazy при першому відкритті вкладки
def load_kaggle_lazy() -> pd.DataFrame:
    """
    Lazy-завантаження Kaggle CSV з кешем 5 хвилин.
    Викликається тільки коли юзер переходить на вкладку 'Еталонні дані'.
    """
    from src.core.kaggle_loader import load_kaggle_data
    try:
        df = load_kaggle_data()
        gc.collect()
        return df
    except Exception as e:
        logger.warning(f"⚠️ Kaggle дані недоступні: {e}")
        return pd.DataFrame()


def get_active_boot_data_generator():
    """
    Generator: yields (message, progress_pct, data_chunk).
    
    [ОПТИМІЗОВАНО v2]: Kaggle ВИДАЛЕНО з boot sequence.
    Завантажується ~100 MB менше при старті.
    Kaggle дані — lazy через load_kaggle_lazy().
    """
    steps = [
        ("> Initializing Kernel & Handshake protocol...",         10,  None),
        ("> 🔌 [CHANNEL 0] Connecting to Neon Cloud Cluster...",  20,  "sql_load"),
        ("> 🧬 Synchronizing Neural Historical Data...",          35,  "sql_gen"),
        ("> ⚡ Calibrating Asset Capacity Buffers...",             50,  "sql_fin"),
        ("> 🛡️ Pulling Strategic Alert Matrices (SAM)...",        62,  "sql_alerts"),
        ("> ⚖️ Validating Grid Topology & Line Vectors...",       74,  "sql_lines"),
        ("> 🌌 Establishing Real-time Telemetry Stream...",        87,  "telemetry"),
        ("> 🎯 ENERGY CORE ONLINE. WELCOME, OPERATOR.",           100, None),
    ]

    final_data = {}

    for msg, p, key in steps:
        try:
            if key:
                chunk = fetch_granular_data(key)
                if isinstance(chunk, dict):
                    final_data.update(chunk)
                gc.collect()
        except (st.runtime.scriptrunner.StopException, st.errors.StreamlitAPIException):
            raise
        except (ConnectionError, TimeoutError) as e:
            # Network/connection errors - skip and continue
            logger.error(f"⚠️ Connection error on step '{msg}': {e}")
        except KeyError as e:
            # Data structure error - log and continue
            logger.error(f"⚠️ Data key missing on step '{msg}': {e}")
        except MemoryError as e:
            # Out of memory - critical, let it fail
            logger.critical(f"🔴 Memory error on step '{msg}': {e}")
            raise
        except Exception as e:
            # Unexpected errors - log with traceback
            logger.exception(f"⚠️ Unexpected error on step '{msg}': {e}")

        clean_msg = msg.replace(">", "").strip()
        if clean_msg not in LOGGED_BOOT_MESSAGES:
            logger.info(clean_msg)
            LOGGED_BOOT_MESSAGES.add(clean_msg)

        yield msg, p, final_data


@st.cache_data(show_spinner=False, max_entries=1, ttl=1800)  # [ОПТ]
def fetch_database_data():
    """
    Повне завантаження даних (резервний варіант).
    max_entries=1 — зберігає тільки 1 версію кешу (було 5).
    """
    generator = get_active_boot_data_generator()
    last_data = {}
    for _, _, chunk in generator:
        last_data = chunk

    gc.collect()
    return last_data


def get_verified_data() -> dict:
    """
    Головна точка входу для отримання даних з валідацією та відновленням.
    
    [ОПТИМІЗОВАНО v2]: session_state зберігає дані тільки при бутстрапі.
    Після першого завантаження — дані читаються з @st.cache_data (спільний кеш).
    """
    from src.services.data.db_seeder import generate_professional_data

    # [ОПТІМІЗАЦІЯ v2.3]: Повертаємо Kaggle-override ТІЛЬКИ якщо обрано цей режим
    is_kaggle = st.session_state.get("active_source") == "Еталонні дані (Kaggle)"
    if is_kaggle and "active_data" in st.session_state and st.session_state["active_data"]:
        return st.session_state["active_data"]

    # В усіх інших випадках (Live) — читаємо свіжі дані з кешу/БД
    data = fetch_database_data()
    
    # Якщо кеш порожній, але є дані в сесії (boot_data), використовуємо їх як fallback.
    if not data and "boot_data" in st.session_state:
        data = st.session_state["boot_data"]

    is_empty = (data is None or not data or data.get("load") is None or data["load"].empty)

    if is_empty:
        st.warning("⚠️ База даних порожня або недоступна!")
        if st.button("🚀 Згенерувати тестові дані", type="primary"):
            with st.spinner("⏳ Генерація..."):
                generate_professional_data()
                st.cache_data.clear()
                st.rerun()
        st.stop()

    return data
