import os
import sys
import time
import signal
import datetime
import subprocess
from datetime import timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

from src.app.config import DataKeys
from src.core import database as db
from src.ui.components.styles import apply_custom_css
from src.services.data.db_seeder import generate_professional_data
from src.core.database.loader import load_kaggle_lazy


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
    # --- APPLY STYLES (Global persistent injection) ---
    apply_custom_css()

    # --- HEARTBEAT SIGNAL ---
    heartbeat_path = Path("logs/heartbeat.txt")
    heartbeat_path.parent.mkdir(exist_ok=True)
    heartbeat_path.touch() # Оновлюємо час модифікації файлу

    if st.sidebar.button("🔄 Оновити дані", type="primary"):
        st.cache_data.clear()
        st.rerun()

    st.sidebar.header("🎛️ Фільтрація")

    # --- 0. Джерело Даних ---
    data_source_options = ["Локальна БД (Симуляція)", "Еталонні дані (Kaggle)"]
    
    # Визначаємо початковий індекс з session_state, якщо він там є
    current_source = st.session_state.get("active_source", data_source_options[0])
    try:
        start_index = data_source_options.index(current_source)
    except ValueError:
        start_index = 0

    data_source = st.sidebar.radio(
        "📂 Джерело даних:",
        data_source_options,
        index=start_index,
        key="active_source"
    )

    # Визначаємо, з яким датасетом працюємо зараз для відображення фільтрів
    if data_source == "Еталонні дані (Kaggle)":
        # Ліниво підтягуємо Kaggle дані для отримання правильних дат
        active_load_df = load_kaggle_lazy()
    else:
        active_load_df = data.get("load", pd.DataFrame())

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

    # [ОПТІМІЗАЦІЯ v2.1]: Динамічний ключ для календаря, щоб він скидався при зміні джерела даних
    date_key = f"date_filter_{data_source.split(' ')[0]}"
    
    date_range = st.sidebar.date_input(
        "📅 Період:",
        value=(default_start, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Фільтрація графіків за часом.",
        key=date_key
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("📡 Керування телеметрією")
    st.sidebar.warning("🚧 МОДУЛЬ В РОЗРОБЦІ (Симуляція)")
    
    lock_file = Path("logs/sensors.lock")
    is_running = lock_file.exists()

    if not is_running:
        if st.sidebar.button("▶️ Запустити Симуляцію Датчиків", type="primary", use_container_width=True):
            # [NUCLEAR OPTIMIZATION]: Локальні імпорти для уникнення UnboundLocalError
            import os
            import sys
            import subprocess
            
            # Запускаємо процес (Windows-safe з прихованим вікном)
            cwd = os.getcwd()
            env = os.environ.copy()
            env["PYTHONPATH"] = cwd
            
            subprocess.Popen(
                [sys.executable, "-m", "src.services.sensors_db"],
                cwd=cwd,
                env=env,
                # Додаємо прапори, щоб на Windows не вискакувало зайве вікно консолі
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            st.rerun()
    else:
        st.sidebar.success("✅ Симуляція активна (15 хв)")
        if st.sidebar.button("🛑 Зупинити Датчики", type="secondary", use_container_width=True):
            if lock_file.exists():
                try:
                    import os
                    import signal
                    with open(lock_file, "r") as f:
                        pid = int(f.read())
                    os.kill(pid, signal.SIGTERM)
                except (ProcessLookupError, ValueError, OSError):
                    pass
                if lock_file.exists(): lock_file.unlink()
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
                    from streamlit.runtime.scriptrunner.exceptions import StopException, RerunException
                    if isinstance(e, (StopException, RerunException)): raise e
                    st.error(f"Помилка: {e}")

    from src.utils.memory_helper import get_resource_status
    status, usage, color, top_objs = get_resource_status()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Render Health")
    st.sidebar.write(f"RAM Usage: :{color}[**{usage:.1f} MB**]")
    st.sidebar.caption(f"Status: {status} (Limit: 512MB)")

    if top_objs:
        with st.sidebar.expander("🔍 Top Objects"):
            for name, size in top_objs:
                st.caption(f"{name}: {size:.1f} MB")

    return selected_region, date_range, data_source, selected_substation
