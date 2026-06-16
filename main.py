# ATLAS_PASSPORT: docs/system/map/system_orchestrator.md
"""
🚀 ATLAS COMMAND & CONTROL CENTER (Strategic Orchestrator).
Модуль: main.py | Версія: 5.0.0 "Defense Edition"
Призначення: Високорівнева оркестрація життєвого циклу системи, управління потоками даних та забезпечення операційної стійкості HUD-інтерфейсу.

Ключові технології:
- 🛡️ Watchdog Sentinel: Активний моніторинг ресурсів та превентивне очищення RAM для запобігання витокам.
- ⚡ Cloud-Safe Engine: Оптимізація паралелізму математичних бібліотек для стабільності у хмарних середовищах.
- 🧬 Hybrid Data Strategy: Динамічне перемикання між Live-телеметрією та Lazy-архівами Kaggle.
- 🩺 Project Diagnostics: Автоматична верифікація цілісності середовища при кожному запуску.
"""

import logging
import os
import sys
import warnings
import streamlit as st

# --- КОНФІГУРАЦІЯ ОБЧИСЛЮВАЛЬНОГО СЕРЕДОВИЩА ---
# Примусове обмеження паралелізму математичних бібліотек до одного потоку.
# Це критично для запобігання помилкам алокації пам'яті (Memory Spike) в обмежених контейнерах.
os.environ.update({
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1"
})

# Фільтрація технічних попереджень сторонніх бібліотек для чистоти логів
logging.getLogger("streamlit").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

# Імпорт сервісних модулівAtlas
from src.utils.logging_config import setup_logging
from src.app.config import DataKeys
from src.core.analytics.filter import filter_dataframe
from src.core.database.loader import get_verified_data
from src.ui.components.styles import init_page_config, apply_custom_css
from src.ui.segments.dashboard import render_dashboard_ui
from src.ui.segments.sidebar import render_sidebar
from src.ui.segments.splash import show_boot_sequence
from src.utils.memory_helper import auto_gc

# Ініціалізація централізованого логера (тільки один раз завдяки кешуванню)
@st.cache_resource
def init_logger():
    return setup_logging(log_level=os.getenv("STREAMLIT_LOGGER_LEVEL", "INFO"))

log = init_logger()

def system_startup():
    """
    Виконує процедуру початкового розгортання середовища (Bootstrapping).
    
    Технічні етапи:
    1. Верифікація кешу: Перевірка та очищення застарілих тимчасових файлів (TTL 24h).
    2. Фільтрація виводу: Придушення некритичних попереджень від Streamlit-ядра.
    3. Діагностика: (Опціонально) Вивід системного банера в консоль для візуалізації статусу.
    """
    try:
        from src.utils.cache_manager import startup_cache_cleanup
        startup_cache_cleanup(ttl_hours=24)
    except Exception as e:
        log.warning(f"Cache cleanup bypass: {e}")

def main():
    """
    Головний цикл управління додатком (Main Event Loop).
    
    Послідовність виконання:
    1. Налаштування метаданих сторінки (Page Config).
    2. Перевірка лімітів пам'яті (Watchdog Trigger).
    3. Обробка стану сесії та ініціалізація заставки (Splash Screen).
    4. Координація джерел даних та логіка агрегації.
    5. Рендеринг основного аналітичного дашборда.
    """
    # 1. Ініціалізація конфігурації сторінки (має бути першим викликом Streamlit)
    init_page_config()
    
    # 2. Моніторинг ресурсів: автоматичне очищення RAM при досягненні порогу 380 MB
    auto_gc(threshold_mb=380)

    # 3. Застосування кастомної HUD-стилізації (CSS-ін'єкції)
    apply_custom_css()

    # 4. Керування логікою завантаження (Boot Sequence)
    # Використовує Session State для уникнення повторних анімацій при кожній взаємодії.
    if "booted" not in st.session_state:
        boot_data = show_boot_sequence()
        st.session_state.update({
            "boot_data": boot_data,
            "booted": True
        })
        data = boot_data
    else:
        # Отримання верифікованих даних з кешу сесії або БД
        data = get_verified_data()

    # 5. Оркестрація джерел даних (Hybrid Data Strategy)
    # Реалізує механізм Lazy Loading для великих архівів Kaggle.
    active_source = st.session_state.get("active_source", "Локальна БД (Симуляція)")
    
    if active_source == "Еталонні дані (Kaggle)":
        from src.core.database.loader import load_kaggle_lazy
        kaggle_df = load_kaggle_lazy()
        if not kaggle_df.empty:
            data = data.copy()
            data["load"] = kaggle_df
            st.session_state["active_data"] = data
    else:
        st.session_state["active_data"] = data

    # 6. Обробка фільтрів та отримання параметрів від користувача
    selected_region, date_range, data_source, selected_substation = render_sidebar(data)

    # 7. Динамічне визначення рівнів агрегації
    # Логіка: якщо обрано конкретний регіон — фокус на підстанціях, інакше — на регіонах.
    group_by_col = (
        "substation_name" if selected_region != DataKeys.ALL_REGIONS else "region_name"
    )

    # 8. Виклик основного UI-модуля для побудови аналітичного простору
    # [ОПТИМІЗАЦІЯ]: Фільтрація даних відбувається безпосередньо у вкладках дашборда.
    render_dashboard_ui(
        data,
        group_by_col,
        data_source,
        selected_region,
        date_range,
        selected_substation,
        filter_fn=filter_dataframe,
    )

# --- ТОЧКА ВХОДУ ---
if __name__ == "__main__":
    # Guard Clause для безпечного імпорту модуля.
    # system_startup() готує середовище, main() запускає прикладний рівень.
    system_startup()
    main()
