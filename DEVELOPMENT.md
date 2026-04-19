# 👨‍💻 ПОСІБНИК РОЗРОБНИКА — Energy Monitor ULTIMATE

> Цей гайд призначений для розробників, які прагнуть зрозуміти архітектуру проекту та розширити його функціональні можливості.

---

## 📋 Зміст

1. [Швидкий старт](#-швидкий-старт)
2. [Структура проєкту](#️-структура-проєкту)
3. [Тестування](#-тестування)
4. [Стандарти кодування](#-стандарти-кодування)
5. [Digital Twin та Симуляція](#-digital-twin--симуляція)
6. [ML Pipeline (ШІ-конвеєр)](#-ml-pipeline)
7. [Docker](#-docker)
8. [Робочий процес Git](#-git-воркфлоу)
9. [Налагодження (Дебагінг)](#-дебагінг)
10. [FAQ (Часті запитання)](#-faq)

---

## 🚀 Швидкий старт

### 1. Налаштування середовища

```bash
# 1. Клонувати репозиторій
git clone https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP.git
cd EnergyMonitor-OLAP

# 2. Створити та активувати віртуальне середовище (venv)
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS

# 3. Встановити необхідні залежності
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Налаштувати змінні оточення
cp .env.example .env
# Відредагувати .env — вставити дані доступу (credentials) до БД від Neon Cloud
```

### 2. Локальний запуск

```bash
# Запустити дашборд Streamlit
python -m streamlit run main.py
# Проєкт буде доступний за адресою: http://localhost:8501
```

### 3. Запуск тестів

```bash
# Виконати всі тести
pytest tests/ -v
# Очікуваний результат: 74 passed, 5 skipped, 0 failed

# Запуск із перевіркою покриття коду
pytest tests/ --cov=src --cov=core --cov=ml --cov-report=html
# Результат можна переглянути у файлі: htmlcov/index.html

# Запуск конкретного файлу або тесту
pytest tests/test_physics.py -v
pytest tests/test_core_analytics.py::TestFilterDataframe::test_filter_dataframe_empty_input -v
```

---

## 🏗️ Структура проєкту

```text
EnergyMonitor-OLAP/
│
├── main.py                        # Точка входу (оркестратор Streamlit)
│
├── app/                           # Глобальні конфігурації
│   └── config.py                  # Константи, перерахування (DataKeys enum)
│
├── core/                          # Аналітичне ядро (бізнес-логіка)
│   ├── analytics/
│   │   ├── physics.py             # Фізика мереж (втрати AC/HVDC, теплова деградація)
│   │   ├── aggregator.py          # OLAP агрегація даних
│   │   ├── clustering.py          # K-Means кластеризація підстанцій
│   │   └── filter.py              # Фільтрація DataFrame за регіоном/датою
│   └── database/
│       └── loader.py              # Верифікований завантажувач (get_verified_data)
│
├── ml/                            # AI Pipeline (Машинне навчання)
│   ├── predict_v2.py              # LSTM контролер + Domain Adaptation
│   ├── vectorizer.py              # Sliding Window + Feature Engineering (9 ознак)
│   ├── metrics_engine.py          # RMSE/MAE/MAPE/R² + Статистичний аудит
│   ├── backtest.py                # Бектест на історичних даних
│   ├── baseline_arima.py          # Seasonal Naive Fallback (Режим Zero-Fail)
│   ├── model_loader.py            # Завантажувач моделей ONNX/H5
│   └── train_lstm.py              # Скрипт навчання LSTM
│
├── src/                           # Серверні сервіси
│   ├── core/
│   │   ├── database.py            # Підключення до PostgreSQL (Neon Cloud)
│   │   ├── config.py              # Налаштування БД, профілі навантаження
│   │   └── physics.py             # Обчислювальна фізика (серверний шар)
│   └── services/
│       ├── sensors_db.py          # Digital Twin симуляція датчиків
│       ├── data_generator.py      # ETL генератор навантаження мережі
│       ├── db_seeder.py           # Початкове заповнення БД тестовими даними
│       ├── advanced_mining.py     # Аналіз трендів та патернів споживання
│       └── sensors.py            # Об'єктна модель сенсорів
│
├── ui/                            # Інтерфейс користувача (Streamlit)
│   ├── components/
│   │   ├── styles.py              # Глобальні CSS-стилі
│   │   └── cards.py               # UI-компоненти (картки метрик, бейджі)
│   ├── segments/
│   │   ├── dashboard.py           # Головний оркестратор сторінок (фрагменти)
│   │   ├── sidebar.py             # Бічна панель: фільтри та управління
│   │   ├── live_kpi.py            # Живий блок KPI (@st.fragment)
│   │   └── splash.py              # Екран завантаження (boot sequence)
│   ├── views/
│   │   ├── kpi.py                 # Телеметрія в реальному часі
│   │   ├── forecast.py            # LSTM прогноз на 24 години
│   │   ├── alerts.py              # Журнал аварій (data_editor)
│   │   ├── historical_audit.py    # OLAP архів та аналітика трендів
│   │   ├── generation.py          # Баланс генерації (діаграми)
│   │   └── map.py                 # ГІС карта вузлів мережі
│   └── common.py                  # Спільні UI-хелпери
│
├── utils/                         # Допоміжні утиліти
│   ├── cache_manager.py           # TTL-кеш (автоочищення кожні 24 год)
│   ├── error_handlers.py          # Декоратори обробки помилок
│   ├── memory_helper.py           # Auto-GC watchdog (ліміт 380 MB)
│   ├── logging_config.py          # Конфігурація логів (Rich + File)
│   └── validators.py              # Валідатори SQL (захист від ін'єкцій)
│
├── tests/                         # Автоматичне тестування (79 тестів)
│   ├── conftest.py                # Фікстури Pytest (сесії БД, тестові DF)
│   ├── test_physics.py            # Валідація фізики Digital Twin
│   ├── test_ml_model.py           # Тести ML Pipeline
│   ├── test_core_analytics.py     # Тести OLAP аналітики
│   ├── test_security.py           # Тести безпеки (SQLi, XSS, валідація)
│   ├── test_utils.py              # Тести утиліт
│   ├── test_pipeline.py           # Інтеграційні тести системи
│   └── test_database.py           # Тести взаємодії з БД
│
├── models/                        # Збережені ваги моделей
│   ├── substation_model_v3_final.keras
│   └── scaler_v3_final.pkl
│
├── logs/                          # Системні логи (автогенерація)
│   ├── energy-monitor.log
│   ├── sensors.lock               # Файл блокування для Digital Twin
│   ├── live_state.json            # Поточний стан симуляції датчиків
│   └── heartbeat.txt              # Сигнал активності (heartbeat)
│
└── cache/                         # TTL кеш (JSON автоочищення)
    └── *.graphml                  # Файли карт (захищено від очищення)
```

---

## 🧪 Тестування

### Написання нових тестів

```python
# tests/test_core_analytics.py
import pytest
import pandas as pd
from src.core.analytics.filter import filter_dataframe

class TestFilterDataframe:
    """Набір тестів для функції filter_dataframe."""

    def test_filter_by_region(self, sample_dataframe):
        """Фільтрація за регіоном повертає лише відповідні рядки."""
        result = filter_dataframe(
            sample_dataframe,
            region="Київ",
            dates=None,
            dataset_name="load"
        )
        assert all(result['region_name'] == 'Київ')
        assert len(result) > 0

    def test_filter_empty_input_returns_empty(self):
        """Порожній DataFrame на вході повертає порожній результат."""
        result = filter_dataframe(pd.DataFrame(), region="Київ", dates=None, dataset_name="load")
        assert result.empty
```

### Використання фікстур (conftest.py)

```python
@pytest.fixture
def sample_dataframe():
    """DataFrame з реалістичними тестовими даними для аналітики."""
    return pd.DataFrame({
        "region_name": ["Київ", "Харків"],
        "actual_load_mw": [150.0, 200.0],
        "timestamp": pd.date_range("2024-01-01", periods=2, freq="h")
    })

@pytest.fixture
def db_session(db_engine):
    """Ізольована сесія БД з автоматичним відкатом після кожного тесту."""
    # ... логіка фікстури ...
    pass
```

### Аналіз покриття коду

```bash
# Створити детальний HTML-звіт про покриття
pytest tests/ --cov=src --cov=core --cov=ml --cov-report=html

# Вивести звіт безпосередньо у термінал
pytest tests/ --cov=src --cov=core --cov=ml --cov-report=term-missing
```

---

## 📝 Стандарти кодування

### Підказки типів (Type Hints)

```python
# ❌ Погано — типи не вказані, важко налагоджувати
def filter_data(df, region, dates):
    return df

# ✅ Добре — чітка типізація покращує стабільність
from typing import Optional, Tuple
from datetime import date
import pandas as pd

def filter_data(
    df: pd.DataFrame,
    region: str,
    dates: Optional[Tuple[date, date]] = None
) -> pd.DataFrame:
    """Фільтрує DataFrame за регіоном та діапазоном дат."""
    return df
```

### Документування коду (Google-style Docstrings)

```python
def calculate_line_losses(df_lines: pd.DataFrame) -> pd.DataFrame:
    """Розраховує втрати потужності для AC та HVDC ліній електропередач.

    Використовує квадратичну модель для AC (I²R) та спрощену лінійну модель для HVDC.

    Args:
        df_lines: DataFrame з даними actual_load_mw, load_pct, max_load_mw.

    Returns:
        DataFrame з розрахованими колонками 'losses_mw' та 'line_type'.

    Raises:
        ValueError: Якщо вхідні дані не містять необхідних колонок.

    Example:
        >>> df = pd.DataFrame({"actual_load_mw": [100], "load_pct": [80], "max_load_mw": [200]})
        >>> result = calculate_line_losses(df)
        >>> "losses_mw" in result.columns
        True
    """
    # ... реалізація ...
    pass
```

### Обробка помилок (Error Handling)

```python
# ✅ Використовуй специфічні винятки замість загальних блоків
try:
    result = fetch_data_from_db()
except ConnectionError as e:
    logger.warning(f"Збій підключення до БД, використовуємо кеш: {e}")
    result = get_cached_data()
except ValueError as e:
    logger.error(f"Помилка валідації даних: {e}")
    raise
except Exception as e:
    logger.exception(f"Непередбачувана помилка при читанні даних: {e}")
    raise

# ✅ Використовуй готові декоратори стабільності
from src.utils.error_handlers import robust_ml_handler, robust_database_handler

@robust_ml_handler
def predict(window: np.ndarray) -> np.ndarray:
    """Передбачення за допомогою LSTM з автоматичним fallback-захистом."""
    pass

@robust_database_handler(default_value=pd.DataFrame())
def get_substations() -> pd.DataFrame:
    """Безпечне отримання переліку підстанцій."""
    pass
```

### Логування (Logging)

```python
import logging
logger = logging.getLogger(__name__)  # Завжди використовуйте __name__

# ✅ Використовуйте відповідні рівні: DEBUG < INFO < WARNING < ERROR < CRITICAL
logger.debug("Налагоджувальна інформація для розробки")
logger.info("✅ Операція виконана успішно")
logger.warning("⚠️ Виявлено відхилення, але система продовжує роботу")
logger.error("❌ Помилка при виконанні конкретної дії")
logger.exception("🔥 Критичний збій програми (додає traceback у лог)")
```

---

## 🤖 Digital Twin та Симуляція

### Схема роботи симуляції

```text
Кнопка в Sidebar "▶️ Запустити"
         │
         ▼
  subprocess.Popen()  ← Запускається фоновий процес
         │
         ▼
  sensors_db.py → run_cosmetic_collector()
         │
         ├── logs/sensors.lock   ← Захист від подвійного запуску
         ├── logs/heartbeat.txt  ← Мітка часу "система жива"
         └── logs/live_state.json ← Поточний стан (MW, Health%, H2...)
         │
         ▼ (оновлення кожні 5 секунд)
  live_kpi.py (@st.fragment run_every=5)
         │
         ▼
  Читає live_state.json → Миттєво оновлює показники в UI
```

### Ручне управління симуляцією

```bash
# Запустити колектор датчиків напряму в терміналі
python -m src.services.sensors_db

# Перевірити поточний стан у форматі JSON
Get-Content logs/live_state.json  # Windows
cat logs/live_state.json          # Linux

# Примусова зупинка — просто видаліть lock-файл
Remove-Item logs/sensors.lock     # Windows
rm logs/sensors.lock              # Linux
```

---

## 🧠 ML Payload (AI Конвеєр)

### Додавання нової версії моделі (наприклад, v4)

1.  У `vectorizer.py` додайте нові ознаки до списку `v4_features`.
2.  У `train_lstm.py` налаштуйте нову архітектуру моделі.
3.  Запустіть навчання: `python src/ml/train_lstm.py --version v3`.
4.  Зареєструйте шлях до нової моделі у `MODEL_REGISTRY` у файлі `model_loader.py`.

### Тестування якості моделі (Backtest)

Запустіть бектест через інтерфейс (вкладка «AI Аналітика») або вручну через Python:
```python
from src.ml.backtest import run_backtest
run_backtest(version='v4', substation='Одеська-Південна')
```

---

## 🐳 Контейнеризація (Docker)

```bash
# Побудова Docker-образу
docker build -t energy-monitor:dev .

# Запуск контейнера з підключенням файлу змінних оточення
docker run -p 10000:10000 --env-file .env energy-monitor:dev

# Перегляд логів контейнера в реальному часі
docker logs -f <container_id>
```

---

## 🔄 Робочий процес Git (Workflows)

1.  Завжди оновлюйте локальний `main`: `git pull origin main`.
2.  Створюйте окрему гілку для нових фіч: `git checkout -b feat/my-new-feature`.
3.  Перед комітом обов'язково проганяйте тести: `pytest tests/ -v`.
4.  Використовуйте **Conventional Commits**:
    - `feat:` нова функція.
    - `fix:` виправлення багу.
    - `docs:` зміни в документації.
    - `refactor:` зміни коду без зміни логіки.

---

## 🐛 Налагодження (Дебагінг)

### Активація DEBUG-режиму
У файлі `.env` встановіть `STREAMLIT_LOGGER_LEVEL=debug` або налаштуйте логер безпосередньо в коді:
```python
import logging
logging.getLogger("src.core.database").setLevel(logging.DEBUG)
```

### Автодіагностика системи
Запустіть вбудований інструмент діагностики:
```bash
python diagnose.py
```
Він перевірить 20+ критичних параметрів (з'єднання з БД, шляхи до моделей, версії пакетів) і створить детальний HTML-звіт.

---

## ❓ FAQ (Часті запитання)

**Q: Чому папка `models/` порожня в репозиторії?**
A: Ваги нейромереж мають великий обсяг і не зберігаються в Git. Їх потрібно згенерувати локально (`src/ml/train_lstm.py`) або отримати з хмарного сховища.

**Q: Як додати новий тест у систему?**
A: Створіть файл `test_*.py` в папці `tests/`. Всі функції, що починаються з `test_`, будуть автоматично знайдені Pytest.

**Q: Чому є дві папки `core/`?**
A: `core/` (в корені) — це аналітичні функції для інтерфейсу. `src/core/` — це низькорівнева логіка (БД, фізика). Консолідація планується у Фазі 8 плану розвитку.

---

## 📚 Корисні ресурси

| Ресурс | Посилання |
| :--- | :--- |
| Документація Streamlit | [docs.streamlit.io](https://docs.streamlit.io) |
| Посібник Pytest | [docs.pytest.org](https://docs.pytest.org) |
| Neon PostgreSQL | [neon.tech/docs](https://neon.tech/docs) |
| Google Python Style | [гугл-стайл](https://google.github.io/styleguide/pyguide.html) |

---

**Успішної розробки! 🚀✨**
