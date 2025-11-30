import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import streamlit as st
import datetime
import random # Потрібен для генерації ID симуляції

# Завантажуємо змінні оточення
load_dotenv()

def get_db_url():
    """Формує URL підключення до PostgreSQL."""
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "password")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "postgres")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

@st.cache_data(ttl=300)
def run_query(query_text: str) -> pd.DataFrame:
    """
    Виконує SQL-запит (SELECT) і повертає DataFrame.
    Кешує результат на 5 хвилин.
    """
    try:
        engine = create_engine(get_db_url())
        with engine.connect() as conn:
            df = pd.read_sql(text(query_text), conn)
        return df
    except Exception as e:
        st.error(f"Помилка бази даних: {e}")
        return pd.DataFrame()

def execute_update(query_text: str, params: dict = None) -> bool:
    """
    Виконує запити INSERT/UPDATE/DELETE без повернення даних.
    """
    try:
        engine = create_engine(get_db_url())
        with engine.begin() as conn:
            conn.execute(text(query_text), params or {})
        return True
    except Exception as e:
        st.error(f"Помилка запису в БД: {e}")
        return False

# --- ФУНКЦІЇ КЕРУВАННЯ ---

def simulate_new_alert():
    """Створює випадкову аварію."""
    engine = create_engine(get_db_url())
    with engine.connect() as conn:
        res = conn.execute(text("SELECT substation_id FROM Substations ORDER BY RANDOM() LIMIT 1")).fetchone()
        if not res: return
        sub_id = res[0]

    sql = """
        INSERT INTO Alerts (timestamp, alert_type, description, substation_id, status)
        VALUES (:ts, :type, :desc, :sub_id, 'NEW')
    """
    params = {
        "ts": datetime.datetime.now(),
        "type": "Симуляція збою",
        "desc": f"Автоматична генерація (Test #{random.randint(1000,9999)})",
        "sub_id": sub_id
    }
    execute_update(sql, params)

def create_custom_alert(sub_name: str, alert_type: str, description: str):
    """Створення конкретного інциденту."""
    engine = create_engine(get_db_url())
    with engine.connect() as conn:
        query = text("SELECT substation_id FROM Substations WHERE substation_name = :name")
        res = conn.execute(query, {"name": sub_name}).fetchone()
        
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
    """Оновлює статус аварії (безпечно для типів NumPy)."""
    sql = "UPDATE Alerts SET status = :status WHERE alert_id = :id"
    execute_update(sql, {"status": new_status, "id": int(alert_id)})