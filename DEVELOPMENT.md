# 👨‍💻 DEVELOPMENT GUIDE — Energy Monitor ULTIMATE

> Цей гайд для розробників, які хочуть зрозуміти проект і розширити його функціонал.

---

## 📋 Зміст

1. [Швидкий старт](#-швидкий-старт)
2. [Структура проекту](#️-структура-проекту)
3. [Тестування](#-тестування)
4. [Кодові стандарти](#-кодові-стандарти)
5. [Digital Twin & Симуляція](#-digital-twin--симуляція)
6. [ML Pipeline](#-ml-pipeline)
7. [Docker](#-docker)
8. [Git-воркфлоу](#-git-воркфлоу)
9. [Дебагінг](#-дебагінг)
10. [FAQ](#-faq)

---

## 🚀 Швидкий старт

### 1. Налаштування середовища

```bash
# 1. Клонувати репозиторій
git clone https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP.git
cd EnergyMonitor-OLAP

# 2. Створити та активувати venv
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS

# 3. Встановити залежності
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Налаштувати середовище
cp .env.example .env
# Відредагувати .env — вставити DB credentials від Neon Cloud
```

### 2. Запустити локально

```bash
# Запустити дашборд
python -m streamlit run main.py
# Відкриється: http://localhost:8501
```

### 3. Запустити тести

```bash
# Всі тести
pytest tests/ -v
# Очікуваний результат: 74 passed, 5 skipped, 0 failed

# З покриттям коду
pytest tests/ --cov=src --cov=core --cov=ml --cov-report=html
# Відкрити: htmlcov/index.html

# Конкретний файл або тест
pytest tests/test_physics.py -v
pytest tests/test_core_analytics.py::TestFilterDataframe::test_filter_dataframe_empty_input -v
```

---

## 🏗️ Структура проекту

```
EnergyMonitor-OLAP/
│
├── main.py                        # Точка входу (Streamlit orchestrator)
│
├── app/                           # Глобальні конфігурації
│   └── config.py                  # Constants, DataKeys enum
│
├── core/                          # Аналітичне ядро (бізнес-логіка)
│   ├── analytics/
│   │   ├── physics.py             # Фізика мереж (AC/HVDC втрати, теплова деградація)
│   │   ├── aggregator.py          # OLAP агрегація
│   │   ├── clustering.py          # K-Means кластеризація підстанцій
│   │   └── filter.py              # Фільтрація DataFrame за регіоном/датою
│   └── database/
│       └── loader.py              # Верифікований завантажувач (get_verified_data)
│
├── ml/                            # AI Pipeline
│   ├── predict_v2.py              # LSTM контролер + Domain Adaptation
│   ├── vectorizer.py              # Sliding Window + Feature Engineering (9 ознак)
│   ├── metrics_engine.py          # RMSE/MAE/MAPE/R² + Shapiro-Wilk audit
│   ├── backtest.py                # Бектест на historical даних
│   ├── baseline_arima.py          # Seasonal Naive Fallback (Zero-Fail)
│   ├── model_loader.py            # ONNX/H5 завантажувач моделей
│   └── train_lstm.py              # Навчання LSTM (запускати окремо)
│
├── src/                           # Серверні сервіси
│   ├── core/
│   │   ├── database.py            # PostgreSQL підключення (Neon Cloud)
│   │   ├── config.py              # DB_CONFIG, LOAD_PROFILES
│   │   └── physics.py             # Фізика (серверний варіант)
│   └── services/
│       ├── sensors_db.py          # Digital Twin симуляція датчиків (run_cosmetic_collector)
│       ├── data_generator.py      # ETL генератор навантаження
│       ├── db_seeder.py           # Первинне заповнення БД тестовими даними
│       ├── advanced_mining.py     # Аналіз трендів і патернів
│       └── sensors.py            # Об'єктна модель сенсора
│
├── ui/                            # Інтерфейс (Streamlit)
│   ├── components/
│   │   ├── styles.py              # CSS + st.set_page_config (точка входу стилів)
│   │   └── cards.py               # Типові UI-компоненти (метрики, бейджі)
│   ├── segments/
│   │   ├── dashboard.py           # Головний оркестратор сторінок (fragments)
│   │   ├── sidebar.py             # Сайдбар: фільтри + керування симуляцією
│   │   ├── live_kpi.py            # Живий KPI блок (@st.fragment run_every=5s)
│   │   └── splash.py              # Заставка завантаження (boot sequence)
│   ├── views/
│   │   ├── kpi.py                 # Телеметрія в реальному часі
│   │   ├── forecast.py            # LSTM прогноз на 24 год.
│   │   ├── alerts.py              # Управління аваріями (data_editor)
│   │   ├── historical_audit.py    # OLAP архів + аналітика
│   │   ├── generation.py          # Генерація і ресурси (кругові діаграми)
│   │   └── map.py                 # Гео-карта вузлів
│   └── common.py                  # Спільні хелпери UI
│
├── utils/                         # Утиліти
│   ├── cache_manager.py           # TTL-кеш (auto-cleanup, 24h)
│   ├── error_handlers.py          # Декоратори (robust_ml_handler, robust_db_handler)
│   ├── memory_helper.py           # Auto-GC watchdog (threshold_mb=380)
│   ├── logging_config.py          # Централізований логер (Rich + File)
│   └── validators.py              # SQL whitelist-валідатори (SQL injection protection)
│
├── tests/                         # Автоматичні тести (74 штуки)
│   ├── conftest.py                # Pytest fixtures (db_session, sample_dataframe...)
│   ├── test_physics.py            # Фізична валідація Digital Twin
│   ├── test_ml_model.py           # ML Pipeline тести
│   ├── test_core_analytics.py     # OLAP аналітика
│   ├── test_security.py           # Security (26 тестів: SQL inject, XSS, validation)
│   ├── test_utils.py              # Утиліти (19 тестів)
│   ├── test_pipeline.py           # Інтеграційні тести
│   └── test_database.py           # DB тести
│
├── models/                        # Навчені моделі (не комітити у git!)
│   ├── substation_model_v3.h5
│   └── substation_scaler_v3.pkl
│
├── logs/                          # Логи (автогенерація)
│   ├── energy-monitor.log
│   ├── sensors.lock               # Singleton lock для Digital Twin
│   ├── live_state.json            # Поточний стан симуляції
│   └── heartbeat.txt              # Heartbeat від sensors_db.py
│
└── cache/                         # TTL кеш (auto-cleans JSON > 24h)
    └── *.graphml                  # Карти (захищено від видалення)
```

---

## 🧪 Тестування

### Написання тестів

```python
# tests/test_core_analytics.py
import pytest
import pandas as pd
from src.core.analytics.filter import filter_dataframe

class TestFilterDataframe:
    """Test suite for filter_dataframe function."""

    def test_filter_by_region(self, sample_dataframe):
        """Filtering by region returns only matching rows."""
        result = filter_dataframe(
            sample_dataframe,
            region="Київ",
            dates=None,
            dataset_name="load"
        )
        assert all(result['region_name'] == 'Київ')
        assert len(result) > 0

    def test_filter_empty_input_returns_empty(self):
        """Empty DataFrame input returns empty DataFrame."""
        result = filter_dataframe(pd.DataFrame(), region="Київ", dates=None, dataset_name="load")
        assert result.empty
```

### Фікстури (conftest.py)

```python
@pytest.fixture
def sample_dataframe():
    """DataFrame з реалістичними тестовими даними."""
    return pd.DataFrame({
        "region_name": ["Київ", "Харків"],
        "actual_load_mw": [150.0, 200.0],
        "timestamp": pd.date_range("2024-01-01", periods=2, freq="h")
    })

@pytest.fixture
def db_session(db_engine):
    """Ізольована DB-сесія з авто-rollback після тесту."""
    ...
```

### Покриття коду

```bash
# Генерувати HTML-звіт
pytest tests/ --cov=src --cov=core --cov=ml --cov-report=html
# Відкрити: htmlcov/index.html

# Текстовий звіт у термінал
pytest tests/ --cov=src --cov=core --cov=ml --cov-report=term-missing
```

---

## 📝 Кодові стандарти

### Type Hints

```python
# ❌ Погано — без типів
def filter_data(df, region, dates):
    return df

# ✅ Добре — з типами
from typing import Optional, Tuple
from datetime import date
import pandas as pd

def filter_data(
    df: pd.DataFrame,
    region: str,
    dates: Optional[Tuple[date, date]] = None
) -> pd.DataFrame:
    """Filter dataframe by region and date range."""
    return df
```

### Google-style Docstrings

```python
def calculate_line_losses(df_lines: pd.DataFrame) -> pd.DataFrame:
    """Розраховує втрати потужності для AC та HVDC ліній.

    Використовує квадратичну модель для AC (I²R) і лінійну для HVDC.

    Args:
        df_lines: DataFrame з колонками actual_load_mw, load_pct, max_load_mw.

    Returns:
        DataFrame з додатковими колонками 'losses_mw' та 'line_type'.

    Raises:
        ValueError: Якщо відсутні обов'язкові колонки.

    Example:
        >>> df = pd.DataFrame({"actual_load_mw": [100], "load_pct": [80], "max_load_mw": [200]})
        >>> result = calculate_line_losses(df)
        >>> "losses_mw" in result.columns
        True
    """
    ...
```

### Error Handling

```python
# ✅ Специфічні винятки замість bare except
try:
    result = fetch_data_from_db()
except ConnectionError as e:
    logger.warning(f"DB connection failed, using cache: {e}")
    result = get_cached_data()
except ValueError as e:
    logger.error(f"Data validation error: {e}")
    raise
except Exception as e:
    logger.exception(f"Unexpected error in fetch_data: {e}")
    raise

# ✅ Використовуй готові декоратори проекту
from src.utils.error_handlers import robust_ml_handler, robust_database_handler

@robust_ml_handler
def predict(window: np.ndarray) -> np.ndarray:
    ...

@robust_database_handler(default_value=pd.DataFrame())
def get_substations() -> pd.DataFrame:
    ...
```

### Логування

```python
import logging
logger = logging.getLogger(__name__)  # Завжди __name__, не рядок

# ✅ Рівні: DEBUG < INFO < WARNING < ERROR < CRITICAL
logger.debug("Детальна інформація для розробки")
logger.info("✅ Завдання виконано успішно")
logger.warning("⚠️ Щось підозріле, але не критичне")
logger.error("❌ Помилка, яку можна пережити")
logger.exception("🔥 Критична помилка (логує traceback)")
```

---

## 🤖 Digital Twin & Симуляція

### Архітектура симуляції

```
Sidebar button "▶️ Запустити"
         │
         ▼
  subprocess.Popen()  ← Фоновий процес (без вікна)
         │
         ▼
  sensors_db.py → run_cosmetic_collector()
         │
         ├── logs/sensors.lock   ← Singleton guard
         ├── logs/heartbeat.txt  ← Timestamp "я живий"
         └── logs/live_state.json ← Поточний стан (MW, Health, H2...)
         │
         ▼ (кожні 5 секунд)
  live_kpi.py (@st.fragment run_every=5)
         │
         ▼
  Читає live_state.json → Відображає в UI
```

### Запуск симуляції вручну

```bash
# Запустити фоновий колектор напряму
python -m src.services.sensors_db

# Перевірити стан
Get-Content logs/live_state.json  # Windows
cat logs/live_state.json          # Linux

# Зупинити — видалити lock-файл
Remove-Item logs/sensors.lock     # Windows
rm logs/sensors.lock              # Linux
```

### Таймаут симуляції

```python
# src/services/sensors_db.py
TIMEOUT_SECONDS = 900  # 15 хвилин — для захисту диплому
# Змінити для production: 3600 (1 год) або 0 (нескінченно)
```

---

## 🧠 ML Pipeline

### Додати нову версію моделі

```python
# 1. У vectorizer.py — додати нові ознаки до v4_features
v4_features = v3_features + ["new_feature"]

# 2. У train_lstm.py — вибрати нову архітектуру
model = build_lstm_model(input_shape=(window_size, len(v4_features)))

# 3. Натренувати
python ml/train_lstm.py --version v4

# 4. Зареєструвати у model_loader.py
MODEL_REGISTRY = {
    "v3": {...},
    "v4": {"path": "models/substation_model_v4.h5", ...}
}
```

### Бектест нової моделі

```bash
# Запустити через UI: вкладка "Аналітика" → "Бектест"
# Або вручну:
python -c "
from src.ml.backtest import run_backtest
run_backtest(version='v4', substation='Київська ТЕЦ-5')
"
```

---

## 🐳 Docker

```bash
# Зібрати образ
docker build -t energy-monitor:dev .

# Запустити з .env файлом
docker run -p 10000:10000 --env-file .env energy-monitor:dev

# Логи контейнера
docker logs -f <container_id>

# Зайти в контейнер
docker exec -it <container_id> /bin/bash
```

---

## 🔄 Git-воркфлоу

```bash
# 1. Оновити main
git pull origin main

# 2. Створити feature гілку
git checkout -b feat/my-feature

# 3. Перевірити перед комітом
pytest tests/ -v          # 74 passed!
flake8 src/ core/ ml/ ui/
mypy src/ core/ ml/ --ignore-missing-imports

# 4. Коміт (Conventional Commits)
git commit -m "feat: add transformer temperature alert"
git commit -m "fix: correct HVDC loss calculation"
git commit -m "docs: update ARCHITECTURE.md"
git commit -m "refactor: extract DB helpers to utils"

# 5. Push і PR
git push origin feat/my-feature
# Створити Pull Request → CI/CD прогонить 74 тести автоматично
```

### Conventional Commits

| Prefix | Коли використовувати |
|--------|---------------------|
| `feat:` | Нова функція |
| `fix:` | Виправлення помилки |
| `docs:` | Документація |
| `refactor:` | Рефакторинг без зміни поведінки |
| `test:` | Тести |
| `chore:` | Залежності, CI, конфіги |

---

## 🐛 Дебагінг

### Активувати DEBUG-режим

```python
# У .env або Render Environment:
STREAMLIT_LOGGER_LEVEL=debug

# Або тимчасово в коді:
import logging
logging.getLogger("src.core.database").setLevel(logging.DEBUG)
```

### Перегляд логів (Windows)

```powershell
# Слідкувати за логами в реальному часі
Get-Content logs/energy-monitor.log -Wait -Tail 50

# Тільки помилки
Select-String "ERROR" logs/energy-monitor.log

# Стан Digital Twin
Get-Content logs/live_state.json
```

### Корисні однострічники

```bash
# Перевірити DB підключення
python -c "from src.core.database import run_query; print(run_query('SELECT 1'))"

# Запустити TTL-очищення кешу вручну
python -c "from src.utils.cache_manager import clean_cache, get_cache_stats; print(get_cache_stats()); clean_cache(ttl_hours=0)"

# Запустити автодіагностику
python diagnose.py

# Перевірити memory watchdog
python -c "from src.utils.memory_helper import auto_gc; auto_gc(threshold_mb=0)"
```

---

## ❓ FAQ

**Q: Де зберігаються навчені моделі?**  
A: `models/` — папка не трекається Git (`.gitignore`). Необхідно або натренувати локально (`ml/train_lstm.py`), або скопіювати з Render.

**Q: Як додати новий тест?**  
A: Створити `test_*.py` у `tests/`, успадкувати від `Test*` класу, іменувати методи `test_*`. Запустити `pytest tests/ -v` — CI підхопить автоматично.

**Q: Як запустити симуляцію без UI?**  
A: `python -m src.services.sensors_db` — запустить фоновий колектор напряму на 15 хвилин.

**Q: Що робить `diagnose.py`?**  
A: Перевіряє 20+ параметрів: наявність файлів, імпорти, DB підключення, якість коду. Видає звіт у HTML.

**Q: Чому є два `core/`?**  
A: `core/` (root) — аналітика для UI. `src/core/` — серверна логіка (DB, physics). Консолідація заплановано після захисту (ROADMAP Phase 5).

**Q: Як оновити залежності безпечно?**  
A: `pip list --outdated` → `pip-audit` (security) → оновити `requirements.txt` → `pytest tests/ -v` → якщо 74 passed — `git push`.

---

## 📚 Корисні ресурси

| Ресурс | URL |
|--------|-----|
| Streamlit Docs | [docs.streamlit.io](https://docs.streamlit.io) |
| Pytest | [docs.pytest.org](https://docs.pytest.org) |
| Neon PostgreSQL | [neon.tech/docs](https://neon.tech/docs) |
| Google Python Style | [google.github.io/styleguide/pyguide.html](https://google.github.io/styleguide/pyguide.html) |
| ARCHITECTURE.md | [./ARCHITECTURE.md](ARCHITECTURE.md) |
| DEPLOYMENT.md | [./DEPLOYMENT.md](DEPLOYMENT.md) |

---

**Happy coding! 🚀✨**
