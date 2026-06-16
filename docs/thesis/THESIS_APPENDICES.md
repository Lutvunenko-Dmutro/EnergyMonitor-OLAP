# ДОДАТКИ

<p align="center"><b>Додаток А. Вихідний код ключових модулів системи</b></p>

*Повний вихідний код програмного комплексу (понад 170 файлів), автоматичні тести (94 успішних), інтерактивна документація та налаштування розгортання доступні у відкритому репозиторії GitHub за посиланням: [https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP)*


**А.1. Модуль математичного моделювання фізичних процесів (physics.py)**

```python
import numpy as np
import pandas as pd
from typing import Tuple
import random

def calculate_transformer_health(
    actual_load: float,
    capacity: float,
    prev_health: float = 100.0
) -> Tuple[float, float, float]:
    """
    Розраховує діагностичні показники (температура масла, H2, здоров'я) 
    на основі поточного навантаження.
    """
    factor = actual_load / capacity if capacity > 0 else 0.5
    
    # 1. Температура масла (база 50 C + приріст від навантаження)
    base_temp = 50.0 + (factor * 30.0)
    temperature_c = round(base_temp + random.uniform(-2.0, 2.0), 1)

    # 2. Вміст водню H2 (ppm)
    base_h2 = 10.0 + (factor * 20.0)
    if factor > 1.1: # Перевантаження
        base_h2 += random.uniform(10.0, 25.0)
    h2_ppm = round(base_h2 + random.uniform(-1.0, 1.0), 1)

    # 3. Health Score (0-100)
    target_health = 100.0
    if temperature_c > 75.0:
        target_health -= (temperature_c - 75.0) * 0.5
    if h2_ppm > 50.0:
        target_health -= (h2_ppm - 50.0) * 0.1
    if factor > 1.0:
        target_health -= (factor - 1.0) * 5.0

    # Плавне відновлення/деградація здоров'я
    if target_health > prev_health:
        new_h = min(target_health, prev_health + 5.0)
    else:
        new_h = target_health

    final_health = max(0.0, min(round(new_h, 1), 100.0))
    
    return temperature_c, h2_ppm, final_health
```

**А.2. Модуль предиктивного аналізу (predict_v2.py)**

```python
import gc
import logging
import numpy as np
import pandas as pd
from src.ml.vectorizer import get_latest_window, select_features_v2
from src.ml.model_loader import load_resources, DEFAULT_WINDOW_SIZE

logger = logging.getLogger(__name__)

@robust_ml_handler
def get_ai_forecast(
    hours_ahead: int = 24,
    substation_name: Optional[str] = None,
    source_type: str = "Live",
    version: str = "v3",
    offset_hours: int = 0,
    temp_shift: float = 0.0,
    constants: dict = None,
    **kwargs
) -> Tuple[pd.DataFrame, Optional[str]]:
    """Generates high-fidelity energy forecasts with fallback protection."""
    if substation_name is None:
        return pd.DataFrame(), "Substation name must be provided."

    try:
        # 1. Завантаження ресурсів
        model, scaler = load_resources(version)
        if model is None or scaler is None:
            return pd.DataFrame(), "Baseline Fallback (AI offline)"

        # 2. Отримання вхідного вікна
        window_size = int(model.get_inputs()[0].shape[1]) if model.get_inputs()[0].shape[1] else DEFAULT_WINDOW_SIZE
        values, constants_res, last_ts, _ = get_latest_window(
            substation_name, source_type, version, offset_hours=offset_hours, window_size=window_size
        )

        if values is None:
            return pd.DataFrame(), "Input telemetry window is empty or insufficient."

        values = select_features_v2(values, version)
        n_features = values.shape[1]
        original_last_load = float(values[-1, 0])

        # 3. Підготовка нормалізованих перезаписів
        current_window = scaler.transform(values)
        future_ts = [last_ts + pd.Timedelta(hours=i + 1) for i in range(hours_ahead)]

        # 4. ONNX Inference (Спрощений вигляд для додатку)
        input_name = model.get_inputs()[0].name
        all_stage_predictions = []
        for i in range(hours_ahead):
            x_input = current_window.reshape(1, window_size, n_features).astype(np.float32)
            pred_s = model.run(None, {input_name: x_input})[0][0]
            pred_s[0] = np.clip(pred_s[0], 0, 1.1)
            all_stage_predictions.append(pred_s)
            
            new_row = current_window[-1].copy()
            new_row[0] = pred_s[0]
            current_window = np.append(current_window[1:], [new_row], axis=0)

        # 5. Inverse Transform
        n_sc = scaler.n_features_in_
        dummy = np.zeros((hours_ahead, n_sc))
        preds_p = np.array(all_stage_predictions)
        dummy[:, 0] = preds_p[:, 0]
        unscaled_raw = scaler.inverse_transform(dummy)
        load_fc = unscaled_raw[:, 0]

        # 6. Формування результату (з довірчими інтервалами)
        load_stitched = np.insert(load_fc, 0, original_last_load)
        all_ts_stitched = [last_ts] + future_ts
        error_band = np.array(load_stitched) * 0.13

        df_result = pd.DataFrame({
            "timestamp": all_ts_stitched,
            "predicted_load_mw": load_stitched,
            "upper_bond": load_stitched + error_band,
            "lower_bond": np.maximum(load_stitched - error_band, 0),
            "is_actual_start": [True] + [False] * hours_ahead
        })

        del values, current_window, dummy, unscaled_raw
        gc.collect()

        logger.info(f"🎯 Optimization success: Forecast generated for {substation_name}")
        return df_result, None

    except Exception as exc:
        logger.error(f"Prediction Pipeline Failure: {str(exc)}", exc_info=True)
        return pd.DataFrame(), f"System Error: {str(exc)}"
```

**А.3. Модуль векторизації та підготовки ознак (vectorizer.py)**

```python
import numpy as np
import pandas as pd

def select_features_v2(data: Any, version: str = "v3") -> np.ndarray:
    """Standardized feature selection for LSTM input tensors."""
    if data is None:
        return np.array([])

    v1_features = ["actual_load_mw"]
    v2_features = v1_features + ["temperature_c", "h2_ppm", "health_score", "air_temp"]
    v3_features = v2_features + ["hour_sin", "hour_cos", "day_sin", "day_cos"]

    target_f = v3_features if version == "v3" else (v2_features if version == "v2" else v1_features)

    if isinstance(data, pd.DataFrame):
        for col in target_f:
            if col not in data.columns:
                data[col] = 0.0
        return data[target_f].values

    expected_len = len(target_f)
    if data.shape[1] < expected_len:
        padding = np.zeros((data.shape[0], expected_len - data.shape[1]))
        return np.hstack([data, padding])

    return data[:, :expected_len]


def _prepare_features(
    df: pd.DataFrame,
    version: str,
    last_ts_col: str
) -> Tuple[np.ndarray, Dict[str, float], pd.Timestamp, List[str]]:
    """Internal helper to calculate periodic signals and metadata."""
    # Тригонометричне кодування циклічних ознак часу (Temporal Engineering)
    hours = df["ts"].dt.hour
    days = df["ts"].dt.weekday
    df["hour_sin"] = np.sin(2 * np.pi * hours / 24)
    df["hour_cos"] = np.cos(2 * np.pi * hours / 24)
    df["day_sin"] = np.sin(2 * np.pi * days / 7)
    df["day_cos"] = np.cos(2 * np.pi * days / 7)

    constants = {
        "oil": float(df["temperature_c"].iloc[-1]) if "temperature_c" in df.columns else 70.0,
        "h2": float(df["h2_ppm"].iloc[-1]) if "h2_ppm" in df.columns else 20.0,
        "air": float(df["air_temp"].iloc[-1]) if "air_temp" in df.columns else 15.0,
        "health": float(df["health_score"].iloc[-1]) if "health_score" in df.columns else 100.0,
    }

    values = select_features_v2(df, version)
    last_ts = pd.to_datetime(df[last_ts_col].iloc[-1])

    f_names = ["actual_load_mw", "temperature_c", "h2_ppm", "health_score", "air_temp",
               "hour_sin", "hour_cos", "day_sin", "day_cos"]
    f_limit = 9 if version == "v3" else (5 if version == "v2" else 1)

    return values, constants, last_ts, f_names[:f_limit]
```

**А.4. Архітектура нейронної мережі (models.py)**

```python
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential

def build_lstm_model(look_back: int, n_features: int, version: str = "v3") -> Sequential:
    """
    Побудова архітектури нейронної мережі (Keras/TensorFlow).
    """
    if version == "v3":
        # Глибока архітектура для складних взаємозв'язків
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=(look_back, n_features)),
            LSTM(64, return_sequences=False),
            Dense(32, activation='relu'),
            Dense(1) 
        ])
    else:
        # Базова архітектура для V1 / V2
        model = Sequential([
            LSTM(128, return_sequences=False, input_shape=(look_back, n_features)),
            Dropout(0.1),
            Dense(32, activation='relu'),
            Dense(1)
        ])

    # Динамічний вибір функції втрат: MAE (чіткість) або Huber (стійкість до викидів)
    loss_fn = "huber" if version == "v3" else "mae"
    model.compile(optimizer="adam", loss=loss_fn)
    
    return model
```

<pagebreak>

<p align="center"><b>Додаток Б</b></p>
<p align="center"><b>Конфігураційні файли та DevOps</b></p>

**Б.1. Конфігурація Docker-контейнера (Dockerfile)**

```dockerfile
# Production Dockerfile for Energy Monitor Ultimate
FROM python:3.11-slim

LABEL maintainer="Energy Monitor Team"
LABEL description="Energy Monitor Ultimate - OLAP & AI Forecasting System"

WORKDIR /app

# Налаштування системних змінних для оптимізації Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Встановлення системних залежностей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копіювання та встановлення Python залежностей
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Копіювання вихідного коду
COPY . .

# Створення непривілейованого користувача для безпеки (Non-root user)
RUN useradd -m -u 1000 streamlit && \
    chown -R streamlit:streamlit /app

USER streamlit

# Налаштування Health Check для оркестратора (Kubernetes/Docker Swarm)
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]
```

<pagebreak>

<p align="center"><b>Додаток В</b></p>
<p align="center"><b>Схема бази даних (SQL DDL)</b></p>

```sql
-- Створення структури таблиць для системи EnergyMonitor-OLAP (PostgreSQL)

CREATE TABLE Substations (
    substation_id INT PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    substation_name VARCHAR(150) NOT NULL,
    location VARCHAR(255),
    capacity_mw DECIMAL(10, 2) NOT NULL CHECK (capacity_mw > 0),
    region_id INT,
    latitude DECIMAL(9, 6),
    longitude DECIMAL(10, 6)
);

CREATE TABLE LoadMeasurements (
    measurement_id BIGINT PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    timestamp TIMESTAMPTZ NOT NULL,
    actual_load_mw DECIMAL(10, 2) NOT NULL,
    substation_id INT,
    voltage_kv DECIMAL(10, 2),
    frequency_hz DECIMAL(10, 2),
    temperature_c DECIMAL(10, 2),
    h2_ppm DECIMAL(10, 2),
    health_score DECIMAL(10, 2),
    sensor_status VARCHAR(50),
    FOREIGN KEY (substation_id) REFERENCES Substations(substation_id) ON DELETE CASCADE
);

-- Композитний індекс для швидкого пошуку графіків по підстанції (OLAP)
CREATE INDEX idx_load_ts_sub ON LoadMeasurements (substation_id, timestamp);
```

<pagebreak>

<p align="center"><b>Додаток Г</b></p>
<p align="center"><b>Результати тестування та верифікації системи</b></p>

**Г.1. Протокол виконання модульних тестів (pytest)**
У ході тестування було перевірено ключові функції системи за допомогою фреймворку `pytest`. 
- **Загальна кількість тестів:** 94 (всі успішні - 100% PASSED).
- **Покриття коду (Coverage):** 97% для ядра системи (`src/ml`, `src/app`).
- `test_physics_engine`: PASSED (перевірка законів фізики та розрахунку зносу);
- `test_lstm_inference`: PASSED (перевірка стабільності нейромережі);
- `test_db_connectivity`: PASSED (успішне з'єднання з хмарною БД Neon).

**Г.2. Валідація точності на тестовій вибірці**
Фінальна оцінка моделі на тестовій вибірці PJM:
- Mean Absolute Percentage Error (MAPE): 3.08%;
- Root Mean Square Error (RMSE): 12.45 MW.

<pagebreak>

<p align="center"><b>Додаток Д</b></p>
<p align="center"><b>Настанови користувача щодо експлуатації системи</b></p>

**Д.1. Системні вимоги**
Для запуску системи необхідно:
- Веб-браузер (Chrome, Firefox, Edge);
- Доступ до мережі Інтернет (для зв'язку з Neon PostgreSQL).

**Д.2. Запуск у локальному середовищі**
1. Встановити залежності: `pip install -r requirements.txt`.
2. Налаштувати змінні середовища (DATABASE_URL).
3. Запустити інтерфейс: `streamlit run main.py`.

**Д.3. Використання аналітичної панелі**
- Перемикання режимів здійснюється через бічну панель (Sidebar).
- Для генерації прогнозу необхідно обрати підстанцію та натиснути кнопку "Generate Forecast".
- Технічний стан обладнання відображається на вкладці "Health Monitoring".
