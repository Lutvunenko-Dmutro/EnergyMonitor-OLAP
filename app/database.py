import os
import pandas as pd
import streamlit as st
import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# --- 1. CONFIGURATION ---
@st.cache_resource
def get_engine():
    """
    Створює та кешує пул з'єднань з базою даних.
    Використовує pool_pre_ping=True для автоматичного відновлення розірваних з'єднань.
    """
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "password")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "postgres")
    
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(url, pool_pre_ping=True)

# --- 2. CORE OPERATIONS ---

def run_query(query_text: str, params: dict = None) -> pd.DataFrame:
    """Виконує SELECT запит і повертає DataFrame."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            return pd.read_sql(text(query_text), conn, params=params)
    except Exception as e:
        st.error(f"Помилка SQL: {e}")
        return pd.DataFrame()

def execute_update(query_text: str, params: dict = None) -> bool:
    """Виконує INSERT/UPDATE/DELETE з автоматичним комітом."""
    try:
        engine = get_engine()
        with engine.begin() as conn: # Автоматичний COMMIT
            conn.execute(text(query_text), params or {})
        return True
    except Exception as e:
        st.error(f"Помилка запису: {e}")
        return False

# --- 3. BUSINESS LOGIC (ALERTS) ---

def create_custom_alert(sub_name: str, alert_type: str, description: str) -> tuple[bool, str]:
    """
    Створює нову аварію.
    Повертає кортеж: (Успіх [True/False], Повідомлення).
    """
    engine = get_engine()
    
    try:
        with engine.begin() as conn:
            # 1. Знаходимо ID підстанції за назвою
            res = conn.execute(
                text("SELECT substation_id FROM Substations WHERE substation_name = :name"), 
                {"name": sub_name}
            ).fetchone()
            
            if not res:
                return False, f"Підстанцію '{sub_name}' не знайдено!"

            sub_id = res[0]

            # 2. Вставляємо запис про аварію
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
            conn.execute(text(sql), params)
            
        return True, "Інцидент успішно створено!"

    except Exception as e:
        return False, f"Помилка бази даних: {e}"

def update_alert_status(alert_id, new_status: str):
    """Оновлює статус існуючої аварії."""
    sql = "UPDATE Alerts SET status = :status WHERE alert_id = :id"
    execute_update(sql, {"status": new_status, "id": int(alert_id)})

def delete_alert(alert_id: int):
    """Видаляє конкретний запис за ID."""
    sql = "DELETE FROM Alerts WHERE alert_id = :id"
    execute_update(sql, {"id": int(alert_id)})

def cleanup_old_alerts(keep_last: int = 10) -> bool:
    """
    Розумна очистка: видаляє всі старі записи, залишаючи N останніх.
    Використовує безпечний підхід через SELECT -> DELETE NOT IN.
    """
    engine = get_engine()
    try:
        # Крок 1: Знаходимо ID, які треба залишити
        with engine.connect() as conn:
            res = conn.execute(
                text("SELECT alert_id FROM Alerts ORDER BY alert_id DESC LIMIT :lim"), 
                {"lim": keep_last}
            ).fetchall()
            
            keep_ids = [row[0] for row in res]

        if not keep_ids:
            return True # Таблиця вже пуста або майже пуста

        # Крок 2: Видаляємо все зайве
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM Alerts WHERE alert_id NOT IN :ids"), 
                {"ids": tuple(keep_ids)}
            )
            
        return True
        
    except Exception as e:
        st.error(f"Помилка очищення: {e}")
        return False
