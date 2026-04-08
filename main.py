import logging
import os

# --- OPENBLAS & NUMPY MEMORY SPIKE PREVENTION ---
# Забороняємо математичним бібліотекам створювати зайві потоки,
# які дублюють пам'ять і вбивають Render (OpenBLAS Memory allocation failed).
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import sys
import warnings

# --- OS-LEVEL HARD RAM LIMIT (RENDER SURVIVAL) ---
try:
    import resource
    # Встановлюємо жорсткий ліміт на 480 MB (Render limit: 512MB)
    # Якщо Python спробує взяти більше, він отримає MemoryError (без крашу сервера 503)
    HARD_LIMIT_MB = 480
    limit_bytes = HARD_LIMIT_MB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, limit_bytes))
except ImportError:
    # Modul resource доступний лише на Unix/Linux, на Windows він просто проігнорується
    pass

# Блокуємо шум від сторонніх бібліотек
import logging
logging.getLogger("streamlit").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

import threading

# Ініціалізація синглтон-логера для системи моніторингу
log = logging.getLogger("ENERGY_MONITOR")
INITIALIZATION_LOCK = threading.Lock()

if not getattr(log, "initialized", False):
    with INITIALIZATION_LOCK:
        # Перевірка всередині блокування (Double-checked locking pattern)
        if not getattr(log, "initialized", False):
            log.propagate = False
            log.setLevel(logging.INFO)
            # Очищуємо старі обробники, якщо вони є (напр. від минулих запусків у тому самому процесі)
            log.handlers = []

            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s] ⚡ %(levelname)-5s | %(message)s", datefmt="%H:%M:%S"
                )
            )
            log.addHandler(handler)

            log.info("=" * 60)
            log.info("🚀 ENERGY MONITOR ULTIMATE: SYSTEM STARTUP")
            log.info("=" * 60)
            log.info("📦 Load modules...")

            log.initialized = True

logger = log


# Налаштування стартового середовища
def system_startup():
    """
    Виконує початкове налаштування середовища (System Bootstrapping).

    Ця функція забезпечує "чистий" запуск додатку:
    1. Очищення терміналу: Видаляє старі логи попередніх запусків (підтримує Windows/Linux).
    2. Візуалізація: Виводить вітальний банер з використанням ANSI-кольорів для індикації успішного старту.
    3. Фільтрація шумів: Приглушує технічні попередження (warnings) бібліотек (зокрема Streamlit),
       які не впливають на роботу, але засмічують консоль.
    """
    # 1. ОЧИЩЕННЯ ЕКРАНУ (Закоментовано, щоб не прати банер)
    # os.system('cls' if os.name == 'nt' else 'clear')
    pass

    # 3. ГЛУШИМО, ЩО МОЖЕМО
    warnings.filterwarnings("ignore")
    # Додатковий глушник для streamlit (можеш дописати, якщо хочеш)


# Database & Queries


from app.config import DataKeys
from core.analytics.filter import filter_dataframe
from core.database.loader import get_verified_data
from ui.components.styles import setup_streamlit_page
from ui.segments.dashboard import render_dashboard_ui
from ui.segments.sidebar import render_sidebar
from ui.segments.splash import show_boot_sequence
import streamlit as st


def select_data_source(data, data_source):
    """
    Адаптує набір даних відповідно до обраного джерела (Live/Kaggle).
    """
    res_data = data.copy()
    if data_source == "Еталонні дані (Kaggle)":
        res_data["load"] = res_data["real_load"]
    return res_data


# Головний оркестратор додатка (Application Entry Point)
def main():
    # Налаштування параметрів сторінки
    setup_streamlit_page()

    # --- BOOT SEQUENCE (ACTIVE SPLASH SCREEN) ---
    if "booted" not in st.session_state:
        # Pass real work into the splash screen
        boot_data = show_boot_sequence()
        st.session_state["boot_data"] = boot_data
        st.session_state["booted"] = True
        st.rerun()

    # Oтримуємо дані (вони вже завантажені заставкою або кешовані)
    data = get_verified_data()

    # Регулювання фільтрів бічної панелі (Input Layer)
    selected_region, date_range, data_source, selected_substation = render_sidebar(data)

    # Винесення логіки вибору джерела даних користувача (Data Source Switching)
    data = select_data_source(data, data_source)

    # Застосування бізнес-логіки фільтрації (Filtering Layer)
    filtered_data = {
        key: filter_dataframe(df, selected_region, date_range, key, selected_substation)
        for key, df in data.items()
    }

    # Визначення рівнів агрегації
    group_by_col = (
        "substation_name" if selected_region != DataKeys.ALL_REGIONS else "region_name"
    )

    # Рендеринг головного екрану (Presentation Layer)
    render_dashboard_ui(
        data,
        filtered_data,
        group_by_col,
        data_source,
        selected_region,
        date_range,
        selected_substation,
    )


# --- ТОЧКА ВХОДУ (ENTRY POINT) ---
if __name__ == "__main__":
    # Захист від випадкового запуску (Guard Clause).
    #
    # Код нижче (system_startup та main) спрацює, тільки якщо ми
    # запускаємо саме ЦЕЙ файл. Якщо ми імпортуємо його в інший скрипт
    # (наприклад, для тестів), то main() автоматично НЕ запуститься.
    system_startup()  # Очищення консолі та вивід банера
    main()  # Запуск логіки додатка
