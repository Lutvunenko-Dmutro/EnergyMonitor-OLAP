import datetime
from datetime import timedelta
import subprocess
import sys

import streamlit as st

from app.config import DataKeys
from src.core import database as db
from src.services.db_seeder import generate_professional_data


def render_sidebar(data):
    """
    Відображає панель керування (Sidebar) та повертає обрані фільтри.

    Ця функція аналізує завантажені дані і динамічно формує елементи керування:
    1. Dropdown для вибору регіону.
    2. DatePicker для вибору діапазону дат.
    3. Multiselect для вибору підстанцій.

    Args:
        data (dict): Словник з DataFrames, отриманий з get_verified_data().

    Returns:
        tuple: (selected_region, date_range, data_source, selected_substation)
    """
    if st.sidebar.button("🔄 Оновити дані", type="primary"):
        st.cache_data.clear()
        st.rerun()

    st.sidebar.header("🎛️ Фільтрація")

    # --- 0. Джерело Даних ---
    data_source = st.sidebar.radio(
        "📂 Джерело даних:",
        ["Локальна БД (Симуляція)", "Еталонні дані (Kaggle)"],
        index=0,
    )

    # Визначаємо, з яким датасетом працюємо зараз
    active_load_df = (
        data["load"] if data_source == "Локальна БД (Симуляція)" else data["real_load"]
    )

    if data_source == "Еталонні дані (Kaggle)":
        selected_region = st.sidebar.selectbox(
            "📍 Регіон:",
            options=["США (PJM Interconnection)"],
            index=0,
            disabled=True,
            help="Регіон зафіксовано для Kaggle датасету.",
        )
        sub_names = (
            sorted(active_load_df["substation_name"].unique().tolist())
            if not active_load_df.empty
            else []
        )
    else:
        # --- 1. Регіон ---
        regions_list = [DataKeys.ALL_REGIONS]
        if not active_load_df.empty and "region_name" in active_load_df.columns:
            regions_list += sorted(active_load_df["region_name"].unique().tolist())

        selected_region = st.sidebar.selectbox(
            "📍 Регіон:",
            options=regions_list,
            index=0,
            help="Оберіть область для аналізу.",
        )

        # --- 2. Підстанція (Каскадна фільтрація) ---
        if selected_region != DataKeys.ALL_REGIONS:
            sql = """
                SELECT s.substation_name 
                FROM Substations s
                JOIN Regions r ON s.region_id = r.region_id
                WHERE r.region_name = :r
                ORDER BY s.substation_name
            """
            substations_df = db.run_query(sql, {"r": selected_region})
        else:
            substations_df = db.run_query(
                "SELECT substation_name FROM Substations ORDER BY substation_name"
            )

        sub_names = (
            substations_df["substation_name"].tolist()
            if not substations_df.empty
            else []
        )

    selected_substation = st.sidebar.multiselect(
        "🔍 Підстанція:",
        options=sub_names,
        default=[],
        placeholder="🟢 Всі об'єкти регіону",
        key=f"sub_select_{selected_region}",
        help="Оберіть конкретні об'єкти. Якщо порожньо — аналізуються всі доступні.",
    )

    if not selected_substation:
        selected_substation = ["Усі підстанції"]

    # --- 3. Дата ---
    if not active_load_df.empty and "timestamp" in active_load_df.columns:
        min_date = active_load_df["timestamp"].min().date()
        max_date = active_load_df["timestamp"].max().date()
    else:
        min_date = datetime.date.today() - timedelta(days=7)
        max_date = datetime.date.today()

    default_start = max(min_date, max_date - timedelta(days=30))

    date_range = st.sidebar.date_input(
        "📅 Період:",
        value=(default_start, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Фільтрація графіків за часом.",
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("📡 Керування телеметрією")
    
    if "sensor_proc" not in st.session_state:
        st.session_state.sensor_proc = None

    if st.session_state.sensor_proc is None or st.session_state.sensor_proc.poll() is not None:
        if st.sidebar.button("▶️ Запустити Live Датчики", type="primary", use_container_width=True):
            proc = subprocess.Popen([sys.executable, "-m", "src.services.sensors_db"])
            st.session_state.sensor_proc = proc
            st.rerun()
    else:
        st.sidebar.success("✅ Датчики генерують дані (Фон)")
        if st.sidebar.button("🛑 Зупинити Датчики", type="secondary", use_container_width=True):
            st.session_state.sensor_proc.terminate()
            st.session_state.sensor_proc.wait()
            st.session_state.sensor_proc = None
            st.rerun()

    with st.sidebar.expander("⚙️ Системні Дії (Data Generator)"):
        st.caption("Ця дія повністю видалить поточну телеметрію та засіє 'ідеальний' початковий набір даних для тестування ML.")
        if st.button("♻️ Перегенерувати Базу Даних", type="primary", use_container_width=True):
            with st.spinner("⏳ Генерація (ETL)... триває 1-2 хвилини"):
                try:
                    generate_professional_data()
                    st.success("✅ Базу відновлено!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Помилка: {e}")

    return selected_region, date_range, data_source, selected_substation
