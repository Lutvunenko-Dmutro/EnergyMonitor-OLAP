import logging
import json
import time
from pathlib import Path

import streamlit as st
import pandas as pd

from ui.views import kpi as tab_kpi

logger = logging.getLogger("ENERGY_MONITOR")
LIVE_STATE_FILE = Path("logs/live_state.json")

# Захист від застарілих версій бібліотеки в хмарних середовищах
def safe_fragment(run_every=None):
    """Декоратор-запобіжник для st.fragment з підтримкою таймера"""
    def decorator(func):
        if hasattr(st, "fragment"):
            return st.fragment(run_every=run_every)(func)
        return func
    return decorator

@safe_fragment(run_every=5)
def live_telemetry_wrapper(active=False):
    """
    Автономний фрагмент для живого оновлення показників (KPI).
    Пріоритетно зчитує дані з живого JSON-стейту симуляції.
    Оновлюється автоматично кожні 5 секунд.
    """
    if not active:
        return
        
    region_filter = st.session_state.get("selected_region", None)
    active_source = st.session_state.get("active_source", "Локальна БД (Симуляція)")

    if active_source == "Еталонні дані (Kaggle)":
        st.info("📊 **Режим історичного аналізу активний**")
        st.caption("Жива телеметрія сенсорів вимкнена для еталонного датасету.")
        return

    try:
        # ПЕРЕВІРКА ЖИВОГО СТАНУ (Сocmetic Monitoring)
        if LIVE_STATE_FILE.exists():
            # Перевірка на свіжість файлу (не старіше 15 секунд)
            mtime = LIVE_STATE_FILE.stat().st_mtime
            if (time.time() - mtime) < 15:
                with open(LIVE_STATE_FILE, "r", encoding="utf-8") as f:
                    state = json.load(f)
                
                # Перетворюємо JSON у формат DataFrame, який очікує tab_kpi.render
                # (Він очікує колонки: substation_name, actual_load_mw, health_score, temperature_c, h2_ppm)
                df_telemetry = pd.DataFrame(state["substations"])
                df_telemetry.rename(columns={
                    "name": "substation_name",
                    "load": "actual_load_mw",
                    "health": "health_score",
                    "temp": "temperature_c",
                    "h2": "h2_ppm",
                    "voltage": "voltage_kv"
                }, inplace=True)
                
                # Гарантована наявність всіх колонок (Safety Layer)
                for col in ["voltage_kv", "temperature_c", "h2_ppm", "health_score"]:
                    if col not in df_telemetry.columns:
                        df_telemetry[col] = 0.0
                
                # Додаємо глобальну частоту до кожної підстанції для рендерингу KPI
                df_telemetry["frequency_hz"] = state["frequency_hz"]
                
                # Додаємо глобальні метрики в session_state для інших віджетів
                st.session_state["live_total_mw"] = state["total_load_mw"]
                st.session_state["live_freq"] = state["frequency_hz"]
                st.session_state["live_avg_health"] = state["avg_health_score"]
                
                # Рендеримо KPI
                tab_kpi.render(df_telemetry, region_filter=region_filter)
                return

        # FALLBACK: Зчитування з БД (якщо трансляція офлайн)
        from src.services.db_services import get_latest_measurements
        telemetry_data = get_latest_measurements()

        if telemetry_data is None or telemetry_data.empty:
            st.warning("🔌 СИСТЕМА МОНІТОРИНГУ В ОЧІКУВАННІ ДАНИХ")
            st.info("Запустіть датчики в боковій панелі (Sidebar) для старту симуляції.")
        else:
            tab_kpi.render(telemetry_data, region_filter=region_filter)

    except Exception as e:
        logger.error(f"Помилка зчитування живої телеметрії: {e}")
        st.error("Помилка зв'язку з датчиками.")
