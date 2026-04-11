import logging
import os
import sys
import warnings

# --- OPENBLAS & NUMPY MEMORY SPIKE PREVENTION ---
# Забороняємо математичним бібліотекам створювати зайві потоки,
# які дублюють пам'ять і вбивають Render (OpenBLAS Memory allocation failed).
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

# Блокуємо шум від сторонніх бібліотек
logging.getLogger("streamlit").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

# ✨ Використовуємо централізовану конфігурацію логування
from utils.logging_config import setup_logging

log = setup_logging(log_level=os.getenv("STREAMLIT_LOGGER_LEVEL", "INFO"))
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

    # 4. TTL CACHE CLEANUP: Видаляємо JSON-файли кешу старіші за 24 години
    try:
        from utils.cache_manager import startup_cache_cleanup
        startup_cache_cleanup(ttl_hours=24)
    except Exception:
        pass  # Ніколи не ламаємо запуск через помилку в очищенні


# Database & Queries


from app.config import DataKeys
from core.analytics.filter import filter_dataframe
from core.database.loader import get_verified_data
from ui.components.styles import setup_streamlit_page
from ui.segments.dashboard import render_dashboard_ui
from ui.segments.sidebar import render_sidebar
from ui.segments.splash import show_boot_sequence
from utils.memory_helper import auto_gc
import streamlit as st



# Головний оркестратор додатка (Application Entry Point)
def main():
    # --- MEMORY WATCHDOG (AUTO-GC) ---
    # Якщо RAM > 380 MB, автоматично очищаємо кеш + gc.collect()
    auto_gc(threshold_mb=380)

    # Налаштування параметрів сторінки
    setup_streamlit_page()

    # --- BOOT SEQUENCE (ACTIVE SPLASH SCREEN) ---
    if "booted" not in st.session_state:
        boot_data = show_boot_sequence()
        st.session_state["boot_data"] = boot_data
        st.session_state["booted"] = True
        # [ОПТИМІЗОВАНО]: Замість st.rerun(), продовжуємо з даними
        # Це дозволяє уникнути додаткового перезавантаження та фрагмент-помилок
        data = boot_data
    else:
        # Отримуємо дані (вже завантажені заставкою або кешовані)
        data = get_verified_data()

    # Регулювання фільтрів бічної панелі
    selected_region, date_range, data_source, selected_substation = render_sidebar(data)
    st.session_state["active_source"] = data_source

    # Data source switching (Kaggle — lazy)
    if data_source == "Еталонні дані (Kaggle)":
        from core.database.loader import load_kaggle_lazy
        kaggle_df = load_kaggle_lazy()
        if not kaggle_df.empty:
            data = data.copy()
            data["real_load"] = kaggle_df
            data["load"] = kaggle_df
            # [STABILITY]: Оновлюємо активні дані, щоб фрагменти бачили Kaggle
            st.session_state["active_data"] = data
    else:
        # [STABILITY]: Повертаємо оригінальні дані для симуляції
        st.session_state["active_data"] = data

    # Визначення рівнів агрегації
    group_by_col = (
        "substation_name" if selected_region != DataKeys.ALL_REGIONS else "region_name"
    )

    # [ОПТИМІЗОВАНО v2]: filtered_data НЕ формується заздалегідь для всіх ключів.
    # Кожна вкладка сама фільтрує тільки потрібний DF у момент рендеру.
    render_dashboard_ui(
        data,
        group_by_col,
        data_source,
        selected_region,
        date_range,
        selected_substation,
        filter_fn=filter_dataframe,
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
