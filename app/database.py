import os
import pandas as pd
import streamlit as st
import datetime
import random
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
@st.cache_resource
def get_engine():
    """Створює та кешує з'єднання з БД (Singleton pattern)."""
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "password")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "postgres")
    
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(url, pool_pre_ping=True)

# --- READ OPERATIONS ---
@st.cache_data(ttl=600)
def run_query(query_text: str, params: dict = None) -> pd.DataFrame:
    """Виконує SELECT запит і повертає DataFrame."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text(query_text), conn, params=params)
        return df
    except Exception as e:
        st.error(f"Помилка бази даних: {e}")
        return pd.DataFrame()

# --- WRITE OPERATIONS ---
def execute_update(query_text: str, params: dict = None) -> bool:
    """Виконує INSERT/UPDATE/DELETE."""
    try:
        engine = get_engine()
        with engine.begin() as conn: 
            conn.execute(text(query_text), params or {})
        return True
    except Exception as e:
        st.error(f"Помилка запису в БД: {e}")
        return False

# --- ACTIONS ---
def create_custom_alert(sub_name: str, alert_type: str, description: str):
    """Створення інциденту."""
    engine = get_engine()
    with engine.connect() as conn:
        res = conn.execute(
            text("SELECT substation_id FROM Substations WHERE substation_name = :name"), 
            {"name": sub_name}
        ).fetchone()
        
        if not res:
            st.error(f"Підстанцію '{sub_name}' не знайдено!")
            return

        sub_id = res[0]

    sql = """
        INSERT INTO Alerts (timestamp, alert_type, description, substation_id, status)
        VALUES (:ts, :type, :desc, :sub_id, 'NEW')
    """
    params = {
        "ts": datetime.datetime.now(),
        "type": alert_type,
        "desc": description,
        "sub_id": sub_id
    }
    execute_update(sql, params)

def update_alert_status(alert_id, new_status: str):
    """Оновлення статусу аварії."""
    sql = "UPDATE Alerts SET status = :status WHERE alert_id = :id"
    execute_update(sql, {"status": new_status, "id": int(alert_id)})
