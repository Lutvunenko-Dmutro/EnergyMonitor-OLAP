import gc
import logging
import time

import pandas as pd
import streamlit as st

from src.core import database as db
from src.core import queries as q
from src.services.db_seeder import generate_professional_data
from src.services.db_services import get_latest_measurements

logger = logging.getLogger(__name__)

# Глобальний фільтр для уникнення дублювання логів у терміналі при перезапусках Streamlit
# Працює на рівні процесу Python, що надійніше за session_state для стартових логів.
LOGGED_BOOT_MESSAGES = set()


# --- ACTIVE LOADING EXTENSIONS ---

def fetch_granular_data(step_key):
    """
    Fetches a specific data subset to allow progressive reporting.
    """
    if step_key == "kaggle":
        from src.core.kaggle_loader import load_kaggle_data
        try: return load_kaggle_data()
        except: return pd.DataFrame()
    
    # Granular SQL Fetches
    if step_key == "sql_load": return {"load": db.run_query(q.QUERY_LOAD_WEATHER)}
    if step_key == "sql_gen":  return {"gen": db.run_query(q.QUERY_GENERATION)}
    if step_key == "sql_fin":  return {"fin": db.run_query(q.QUERY_FINANCE)}
    if step_key == "sql_alerts": return {"alerts": db.run_query(q.QUERY_ALERTS)}
    if step_key == "sql_lines": return {"lines": db.run_query(q.QUERY_LINES)}
    if step_key == "telemetry": return {"telemetry": get_latest_measurements()}
    
    return {}

def get_active_boot_data_generator():
    """
    A generator that yields (message, progress_pct, data_chunk)
    to be consumed by the splash screen.
    """
    steps = [
        ("> Initializing Kernel & Handshake protocol...", 10, None),
        ("> Connecting to Neon DB (PostgreSQL v15)...", 15, "sql_load"),
        ("> Synchronizing Historical Load Data (1000+ rows)...", 25, "sql_gen"),
        ("> Fetching Generation Metrics & Asset Capacity...", 35, "sql_fin"),
        ("> Pulling Strategic Financial OLAP Cube...", 45, "sql_alerts"),
        ("> Checking System Alerts & Anomaly Buffers...", 55, "sql_lines"),
        ("> Mapping Electrical Infrastructure Topology...", 65, None),
        ("> Fetching Kaggle Benchmark Data (AEP/COMED)...", 75, "kaggle"),
        ("> Establishing Real-time Telemetry Stream...", 85, "telemetry"),
        ("> Calibrating Physics-Informed Digital Twin...", 95, None),
        ("> UI ORCHESTRATOR READY.", 100, None)
    ]
    
    final_data = {}
    
    for msg, p, key in steps:
        try:
            if key:
                chunk = fetch_granular_data(key)
                if isinstance(chunk, dict): final_data.update(chunk)
                else: final_data["real_load"] = chunk
                # Примусове очищення пам'яті після кожного кроку завантаження
                gc.collect()
        except Exception as e:
            logger.error(f"⚠️ Помилка на кроці '{msg}': {e}")
            # Продовжуємо навіть при помилці окремого кроку
        
        # Log to terminal ONLY ONCE per unique message to avoid clutter
        clean_msg = msg.replace(">", "").strip()
        if clean_msg not in LOGGED_BOOT_MESSAGES:
            logger.info(clean_msg)
            LOGGED_BOOT_MESSAGES.add(clean_msg)
            
        yield msg, p, final_data

# --- UPDATED ENTRY POINTS ---

@st.cache_data(max_entries=5, ttl=3600)
def fetch_database_data():
    """
    Повне завантаження даних (резервний варіант).
    Використовує memory_diet та gc для економії RAM.
    """
    generator = get_active_boot_data_generator()
    last_data = {}
    for _, _, chunk in generator:
        last_data = chunk
    
    gc.collect()
    return last_data

def get_verified_data():
    """
    Головна точка входу для отримання даних з валідацією та відновленням.
    """
    # 1. Перевіряємо сесію (дані від заставки)
    if "boot_data" in st.session_state:
        data = st.session_state["boot_data"]
    else:
        # Резервне завантаження, якщо заставка була пропущена
        data = fetch_database_data()

    # 2. Перевірка на порожнечу та відновлення
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
