import os
from contextlib import contextmanager
from typing import Optional

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from src.core.config import DB_CONFIG
from src.core.logger import setup_logger

load_dotenv()

log = setup_logger(__name__)

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

    ssl_mode = os.getenv("DB_SSL", "prefer")
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}?sslmode={ssl_mode}"
    return create_engine(url, pool_pre_ping=True)


# --- 2. psycopg2 CORE (For Data Generator) ---
@contextmanager
def get_db_cursor():
    """Контекстний менеджер для безпечної роботи з базою даних через psycopg2."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn, conn.cursor()
        conn.commit()
    except Exception as e:
        log.error(f"Database operation failed: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def execute_sql_file(cursor, filename):
    """Читає та виконує SQL з файлу."""
    if not os.path.exists(filename):
        log.error(f"❌ Файл {filename} не знайдено! Пропускаємо.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        sql_script = f.read()

    cursor.execute(sql_script)
    log.info(f"📜 Виконано скрипт: {filename}")


# --- 3. SQLALCHEMY CORE (For Streamlit App) ---
def run_query(query_text: str, params: Optional[dict] = None) -> pd.DataFrame:
    """Виконує SELECT запит і повертає DataFrame."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            return pd.read_sql(text(query_text), conn, params=params)
    except Exception as e:
        log.error(f"Помилка SQL: {e}", exc_info=True)
        return pd.DataFrame()


def execute_update(query_text: str, params: Optional[dict] = None) -> bool:
    """Виконує INSERT/UPDATE/DELETE з автоматичним комітом."""
    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text(query_text), params or {})
        return True
    except Exception as e:
        log.error(f"Помилка запису: {e}", exc_info=True)
        return False
