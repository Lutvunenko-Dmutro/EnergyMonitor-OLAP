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

import numpy as np

load_dotenv()

log = setup_logger(__name__)


# Колонки з малою кількістю унікальних значень — конвертуємо у Category
_KNOWN_CATEGORICAL_COLS = {
    "region_name", "substation_name", "alert_type", "status",
    "conditions", "generator_type", "day_type", "source_type",
}

def memory_diet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Агресивна оптимізація пам'яті DataFrame (5 рівнів):
    1. float64 → float32  (економія ~50% числових даних)
    2. int64 → int32       (економія ~50% цілочисельних)
    3. object → Category   (економія ~80% для рядкових повторюваних значень)
    4. datetime64[ns] → datetime64[s]  (нам мікросекунди не потрібні)
    5. bool залишається bool (вже оптимально)
    """
    if df.empty:
        return df

    for col in df.columns:
        col_type = df[col].dtype

        if col_type == np.float64:
            df[col] = df[col].astype(np.float32)

        elif col_type == np.int64:
            col_min, col_max = df[col].min(), df[col].max()
            if col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                df[col] = df[col].astype(np.int16)
            elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                df[col] = df[col].astype(np.int32)

        elif col_type == object:
            # ⚠️ Category ТІЛЬКИ для відомих статичних колонок з whitelist!
            # НЕ використовуємо unique_ratio — це ламає код, що присвоює нові значення.
            if col in _KNOWN_CATEGORICAL_COLS:
                df[col] = df[col].astype("category")

        elif hasattr(col_type, 'tz') or str(col_type).startswith("datetime64"):
            # Знижуємо точність з ns до s (економить 4x пам'яті для часових рядів)
            try:
                df[col] = df[col].astype("datetime64[s]")
            except Exception:
                pass  # Не критично якщо не вдалося

    return df


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

    ssl_mode = os.getenv("DB_SSL")
    if not ssl_mode:
        ssl_mode = "prefer" if host in ["localhost", "127.0.0.1", "::1"] else "require"
        
    # Маскуємо технічну адресу для "охайного" виводу в консоль
    display_name = "Neon Cloud Cluster" if "neon.tech" in host.lower() else host
    log.info(f"🔌 База даних -> Підключення до {display_name} (DB: {dbname})")
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

    retries = 5
    for i in range(retries):
        try:
            engine = get_engine()
            with engine.connect() as conn:
                chunks = []
                for chunk in pd.read_sql(text(query_text), conn, params=params, chunksize=5000):
                    chunks.append(memory_diet(chunk))

                if not chunks:
                    return pd.DataFrame()

                df = pd.concat(chunks, ignore_index=True)
                del chunks          # Явне звільнення chunks з пам'яті
                import gc; gc.collect()

                if not df.empty:
                    df.to_parquet(cache_path, index=False)
                return df
                
        except Exception as e:
            err_msg = str(e).lower()
            err_type = type(e).__name__
            
            # Обробка розширеного списку мережевих помилок
            recoverable_patterns = [
                "503", "502", "504", "service unavailable", 
                "connection", "timeout", "reset by peer", "broken pipe"
            ]
            is_recoverable = any(x in err_msg for x in recoverable_patterns)
            
            if is_recoverable and i < retries - 1:
                wait_time = (i * 6) + 4 # Продвинуті паузи: 4, 10, 16, 22...
                log.warning(f"🔌 [{err_type}] БД Neon прокидається... Спроба {i+1}/{retries}. Чекаємо {wait_time}с.")
                import time
                time.sleep(wait_time)
                continue
                
            log.error(f"❌ КРИТИЧНА ПОМИЛКА БАЗИ [{err_type}]: {e}")
            
            log.warning(f"⚠️ Активуємо Офлайн-режим (локальний кеш).")
            if os.path.exists(cache_path):
                return pd.read_parquet(cache_path)
            
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
