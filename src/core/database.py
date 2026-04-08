import os
import hashlib
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

    ssl_mode = os.getenv("DB_SSL", "require")
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}?sslmode={ssl_mode}"
    return create_engine(url, pool_pre_ping=True)


# --- 2. psycopg2 CORE (For Data Generator) ---
@contextmanager
def get_db_cursor():
    """Контекстний менеджер для безпечної роботи з базою даних через psycopg2 з ретраями."""
    conn = None
    retries = 3
    for i in range(retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            yield conn, conn.cursor()
            conn.commit()
            break
        except Exception as e:
            if i < retries - 1:
                log.warning(f"🔄 Спроба підключення до БД {i+1}/{retries} (база прокидається)...")
                import time
                time.sleep(3)
                continue
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
    """
    Виконує SELECT запит з ретраями для холодного старту Neon DB.
    """
    query_id = hashlib.md5(f"{query_text}_{params}".encode()).hexdigest()
    cache_path = os.path.join("data", "fallback", f"query_{query_id}.parquet")
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    retries = 3
    for i in range(retries):
        try:
            engine = get_engine()
            with engine.connect() as conn:
                df = pd.read_sql(text(query_text), conn, params=params)
                
                if not df.empty:
                    df.to_parquet(cache_path, index=False)
                return df
                
        except Exception as e:
            err_msg = str(e).lower()
            if ("503" in err_msg or "connection" in err_msg) and i < retries - 1:
                import time
                log.warning(f"🔌 БД Neon прокидається... Спроба {i+1}/{retries}")
                time.sleep(4) # Даємо Neon час підняти інстанс
                continue
                
            log.warning(f"⚠️ БД Neon недоступна. Офлайн-режим: {e}")
            if os.path.exists(cache_path):
                return pd.read_parquet(cache_path)
            
            log.error(f"❌ Критична помилка SQL: {e}")
            return pd.DataFrame()


def execute_update(query_text: str, params: Optional[dict] = None) -> bool:
    """Виконує INSERT/UPDATE/DELETE з ретраями."""
    retries = 2
    for i in range(retries):
        try:
            engine = get_engine()
            with engine.begin() as conn:
                conn.execute(text(query_text), params or {})
            return True
        except Exception as e:
            if i < retries - 1:
                import time
                time.sleep(2)
                continue
            log.error(f"Помилка запису: {e}")
            return False
