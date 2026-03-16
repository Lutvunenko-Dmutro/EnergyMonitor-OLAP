import logging
import os
import sys
import warnings

# Відключення надлишкового логування сторонніх бібліотек (TensorFlow, Streamlit)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("streamlit").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

# Ініціалізація синглтон-логера для системи моніторингу
log = logging.getLogger("ENERGY_MONITOR")

if not getattr(log, "initialized", False):
    log.propagate = False
    log.setLevel(logging.INFO)
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
    warnings.filterwarnings(
        "ignore", category=UserWarning, message=".*use_container_width.*"
    )


# Database & Queries


from app.config import DataKeys
from core.analytics.filter import filter_dataframe
from core.database.loader import get_verified_data
from ui.components.styles import setup_streamlit_page
from ui.segments.dashboard import render_dashboard_ui
from ui.segments.sidebar import render_sidebar


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
    """
    Головна функція-оркестратор додатка (Application Entry Point).

    Вона реалізує класичний пайплайн обробки даних (Data Pipeline):
    1. Setup: Налаштування параметрів сторінки.
    2. Data Ingestion: Отримання "сирих" даних з бази (get_verified_data).
    3. User Input: Отримання параметрів фільтрації від користувача (render_sidebar).
    4. Data Processing: Застосування фільтрів до всіх наборів даних (filter_dataframe).
    5. UI Rendering: Відображення фінального інтерфейсу (render_dashboard_ui).
    """
    # Налаштування параметрів сторінки
    setup_streamlit_page()

    # Отримання джерел даних (Data Access Layer)
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
