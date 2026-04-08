import logging
import time

import pandas as pd
import streamlit as st

from src.core import database as db
from src.core import queries as q
from src.services.db_seeder import generate_professional_data
from src.services.db_services import get_latest_measurements

logger = logging.getLogger(__name__)


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
        if key:
            chunk = fetch_granular_data(key)
            if isinstance(chunk, dict): final_data.update(chunk)
            else: final_data["real_load"] = chunk
        
        # Log to terminal as well
        logger.info(msg.replace(">", "").strip())
        yield msg, p, final_data

# --- UPDATED ENTRY POINTS ---

def get_verified_data():
    """
    Updated entry point that ensures data exists, 
    falling back to manual verification if boot sequence was skipped.
    """
    # 1. Check if data already in session state (provided by splash)
    if "boot_data" in st.session_state:
        data = st.session_state["boot_data"]
    else:
        # Fallback to standard fetch if directly accessing
        data = fetch_database_data()

    # 2. Validation & Recovery (Keep existing logic)
    is_empty = (data is None or data.get("load") is None or data["load"].empty)
    
    if is_empty:
        st.warning("⚠️ База даних порожня або недоступна!")
        if st.button("🚀 Згенерувати тестові дані", type="primary"):
            with st.spinner("⏳ Генерація..."):
                generate_professional_data()
                st.cache_data.clear()
                st.rerun()
        st.stop()
        
    return data
