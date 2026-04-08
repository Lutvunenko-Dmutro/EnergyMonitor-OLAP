import logging
import time

import pandas as pd
import streamlit as st

from src.core import database as db
from src.core import queries as q
from src.services.db_seeder import generate_professional_data
from src.services.db_services import get_latest_measurements

logger = logging.getLogger(__name__)


@st.cache_data(ttl=600)
def fetch_database_data():
    """
    Виконує SQL-запити до всіх таблиць та повертає словник з DataFrame.

    Використовує кешування Streamlit (TTL = 600 секунд / 10 хвилин),
    щоб не навантажувати базу даних при кожному кліку користувача.

    Returns:
        dict: Словник, де ключі — це назви датасетів ('load', 'gen', 'alerts'...),
              а значення — відповідні Pandas DataFrames.
    """
    try:
        from src.core.kaggle_loader import load_kaggle_data

        real_load_df = load_kaggle_data()
    except Exception:
        real_load_df = pd.DataFrame()

    return {
        "load": db.run_query(q.QUERY_LOAD_WEATHER),
        "gen": db.run_query(q.QUERY_GENERATION),
        "alerts": db.run_query(q.QUERY_ALERTS),
        "lines": db.run_query(q.QUERY_LINES),
        "fin": db.run_query(q.QUERY_FINANCE),
        "telemetry": get_latest_measurements(),
        "real_load": real_load_df,
    }


def get_verified_data():
    """
    Керує процесом отримання та валідації даних (Data Orchestrator).

    Ця функція виконує повний цикл захисту (Guard Clauses):
    1. Спроба завантаження: Тягне дані з кешу або БД.
    2. Валідація: Перевіряє структуру та наявність даних.
    3. Відновлення (Recovery): Якщо база пуста, пропонує інтерфейс
       для запуску генератора (data_generator.py).

    Returns:
        dict: Перевірений словник з DataFrame, якщо дані існують.
        Нічого (st.stop), якщо дані відсутні.
    """

    # 1. Завантаження
    with st.spinner("⏳ Завантаження даних з бази..."):
        data = fetch_database_data()

    # 2. Перевірка на помилки (Error Handling)
    is_empty = False
    if data is None:
        is_empty = True
    elif "load" not in data:
        st.error("❌ Помилка структури даних: Ключ 'load' не знайдено.")
        is_empty = True
    elif data["load"].empty:
        is_empty = True

    # 3. Обробка пустой бази (UI Action)
    if is_empty:
        st.warning("⚠️ База даних порожня або недоступна!")

        col1, _ = st.columns([1, 2])
        with col1:
            if st.button("🚀 Згенерувати тестові дані", type="primary"):
                with st.spinner("⏳ Генерація даних (ETL Process)..."):
                    try:
                        generate_professional_data()

                        st.success("✅ Дані згенеровано!")
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        logger.error(f"Помилка генератора: {e}", exc_info=True)

        st.stop()

    assert data is not None, "Data cannot be None here"
    return data
