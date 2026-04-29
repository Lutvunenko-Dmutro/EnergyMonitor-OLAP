# ДОДАТКИ

## Додаток А. Вихідний код ключових модулів системи

### А.1. Модуль математичного моделювання фізичних процесів (physics.py)

```python
import datetime
import random
from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd
from src.core.config import LOAD_PROFILES

def calculate_line_losses(df_lines: pd.DataFrame) -> pd.DataFrame:
    """
    Розраховує втрати потужності в мережі для AC та HVDC ліній.
    Враховує квадратичну залежність втрат від навантаження для AC.
    """
    if df_lines.empty: return df_lines
    df = df_lines.copy()
    
    if "line_type" not in df.columns and "max_load_mw" in df.columns:
        df["line_type"] = df["max_load_mw"].apply(lambda x: "HVDC" if x >= 3000 else "AC")
    
    is_hvdc = df["line_type"] == "HVDC"
    
    # Модель втрат: 1.5% для постійного струму, до 3.5% для змінного при номіналі
    loss_dc = (df["actual_load_mw"] * 0.015) * (df["load_pct"] / 100)
    loss_ac = (df["actual_load_mw"] * 0.035) * (df["load_pct"] / 100) ** 2
    
    df["losses_mw"] = np.where(is_hvdc, loss_dc, loss_ac)
    df["efficiency_pct"] = 100 * (1 - df["losses_mw"] / df["actual_load_mw"])
    return df

def calculate_weather(ts: datetime.datetime, current_temps: Dict[int, float]) -> Dict[int, Tuple[float, str]]:
    """
    Імітує добовий цикл температури з випадковими флуктуаціями.
    Використовує синусоїдальну апроксимацію добового ходу.
    """
    weather_map = {}
    time_val = ts.hour + ts.minute / 60.0
    
    for region_id, base_temp in current_temps.items():
        # Добова амплітуда 5-7 градусів, пік о 14:00
        amplitude = 6.0
        peak_hour = 14.0
        daily_cycle = amplitude * np.sin((time_val - peak_hour + 6) * np.pi / 12)
        
        # Додавання випадкового шуму (броунівський рух температури)
        noise = np.random.normal(0, 0.15)
        final_temp = float(base_temp + daily_cycle + noise)
        
        condition = "Ясно" if final_temp > 15 else "Хмарно"
        if random.random() > 0.9: condition = "Дощ"
        
        weather_map[region_id] = (round(final_temp, 2), condition)
    return weather_map

def calculate_substation_load(capacity: float, profile_type: str, ts: datetime.datetime, 
                              temp: float, is_weekend: bool, prev_f: float = 0.5) -> Tuple[float, Optional[str]]:
    """
    Розраховує поточне навантаження підстанції з урахуванням профілю, 
    температури та дня тижня.
    """
    hour = ts.hour
    hourly_profile = LOAD_PROFILES.get(profile_type, LOAD_PROFILES["RESIDENTIAL"]).get(hour, 0.5)
    
    # Корекція на вихідний день (-20% навантаження)
    day_mult = 0.85 if is_weekend else 1.0
    
    # Вплив температури (кондиціювання або опалення)
    # Базова комфортна температура 21 градус
    temp_diff = abs(temp - 21.0)
    temp_mult = 1.0 + (temp_diff * 0.02) # +2% навантаження на кожний градус відхилення
    
    final_f = hourly_profile * day_mult * temp_mult + np.random.normal(0, 0.02)
    
    # Ефект інерційності споживання (Smoothing)
    smoothed_f = (final_f * 0.7) + (prev_f * 0.3)
    
    actual_load = round(float(capacity * max(0.05, smoothed_f)), 2)
    return actual_load, None

def calculate_transformer_health(actual_load: float, capacity: float, prev_health: float = 100.0) -> Tuple[float, float, float]:
    """
    Моделює фізичний стан трансформатора (Digital Twin).
    Враховує перегрів та розчинені гази (DGA).
    """
    load_factor = actual_load / capacity if capacity > 0 else 0.5
    
    # Температура верхніх шарів масла (Top-oil temperature)
    ambient_base = 20.0
    temp_rise = 45.0 * (load_factor ** 1.6) # Спрощена формула IEEE
    top_oil_temp = round(ambient_base + temp_rise + random.uniform(-2, 2), 1)
    
    # Генерація водню (H2) як індикатора деградації
    h2_increment = 0.1 * (load_factor ** 2) if top_oil_temp > 80 else 0.01
    h2_ppm = round(15.0 + h2_increment + random.uniform(0, 0.5), 1)
    
    # Розрахунок інтегрального Health Score
    temp_penalty = max(0, top_oil_temp - 95) * 1.5
    gas_penalty = max(0, h2_ppm - 100) * 0.5
    load_penalty = max(0, load_factor - 1.1) * 20.0
    
    health = 100.0 - temp_penalty - gas_penalty - load_penalty
    return top_oil_temp, h2_ppm, max(0.0, min(round(health, 2), 100.0))
```

### А.2. Модуль предиктивного аналізу (predict_v2.py)

```python
import gc
import logging
import numpy as np
import pandas as pd
from src.ml.vectorizer import get_latest_window, select_features_v2
from src.ml.model_loader import load_resources, DEFAULT_WINDOW_SIZE

logger = logging.getLogger(__name__)

def get_ai_forecast(hours_ahead=24, substation_name=None, source_type="Live", version="v3", **kwargs):
    """
    Головна функція інференсу для отримання прогнозу на N годин вперед.
    Підтримує рекурсивне прогнозування (Autoregressive).
    """
    try:
        model, scaler = load_resources(version)
        if model is None: 
            return pd.DataFrame(), "Помилка завантаження моделі ONNX"
        
        # Отримання останнього вікна даних (Look-back window)
        values, constants, last_ts, _ = get_latest_window(substation_name, source_type, version)
        if values is None or len(values) < DEFAULT_WINDOW_SIZE:
            return pd.DataFrame(), "Недостатньо даних для формування вікна (потрібно 48г)"
        
        # Підготовка вхідного масиву
        features = select_features_v2(values, version)
        current_window = scaler.transform(features)
        
        input_name = model.get_inputs()[0].name
        predictions = []
        
        # Рекурсивний цикл прогнозування
        for _ in range(hours_ahead):
            # Формування тензору (Batch, Time, Features)
            x_input = current_window.reshape(1, current_window.shape[0], current_window.shape[1]).astype(np.float32)
            
            # Виконання інференсу
            onnx_out = model.run(None, {input_name: x_input})[0][0]
            pred_val = onnx_out[0]
            predictions.append(pred_val)
            
            # Оновлення вікна для наступного кроку (Shift window)
            new_row = current_window[-1].copy()
            new_row[0] = pred_val # Оновлюємо цільову ознаку (load) прогнозом
            
            current_window = np.append(current_window[1:], [new_row], axis=0)
        
        # Формування вихідного DataFrame з мітками часу
        future_ts = [last_ts + pd.Timedelta(hours=i+1) for i in range(hours_ahead)]
        df_res = pd.DataFrame({
            "timestamp": future_ts,
            "predicted_load_mw": np.array(predictions)
        })
        
        return df_res, None
        
    except Exception as e:
        logger.error(f"Inference error: {e}")
        return pd.DataFrame(), str(e)
    finally:
        gc.collect()
```

### А.3. Модуль векторизації та підготовки ознак (vectorizer.py)

```python
import numpy as np
import pandas as pd
from src.core.database import run_query

def encode_cyclical_features(df, col, max_val):
    """
    Виконує тригонометричне кодування циклічних ознак (час, дні).
    Дозволяє уникнути розриву між 23:59 та 00:00.
    """
    df[col + '_sin'] = np.sin(2 * np.pi * df[col]/max_val)
    df[col + '_cos'] = np.cos(2 * np.pi * df[col]/max_val)
    return df

def select_features_v3(data: pd.DataFrame) -> np.ndarray:
    """
    Відбирає фінальний набір ознак для моделі v3.
    """
    required = [
        "actual_load_mw", "temp_c", "h2_ppm", "health_score",
        "hour_sin", "hour_cos", "day_sin", "day_cos", "is_weekend"
    ]
    return data[required].values

def prepare_training_data(raw_df):
    """
    Повний цикл Preprocessing для навчання.
    """
    df = raw_df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    df = encode_cyclical_features(df, 'hour', 24)
    df = encode_cyclical_features(df, 'day_of_week', 7)
    
    return select_features_v3(df)
```

## Додаток Б. Конфігураційні файли та DevOps

### Б.1. Конфігурація Docker-контейнера (Dockerfile)

```dockerfile
# Використання оптимізованого образу Python
FROM python:3.11-slim

# Встановлення системних залежностей для математичних бібліотек
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копіювання та встановлення залежностей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання вихідного коду
COPY . .

# Налаштування змінних середовища
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501

# Запуск додатку
CMD ["streamlit", "run", "main.py"]
```

## Додаток В. Схема бази даних (SQL DDL)

```sql
-- Створення структури таблиць для системи EnergyMonitor-OLAP
CREATE TABLE Regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL
);

CREATE TABLE Substations (
    substation_id SERIAL PRIMARY KEY,
    region_id INT REFERENCES Regions(region_id),
    substation_name VARCHAR(100) NOT NULL,
    capacity_mw FLOAT NOT NULL,
    profile_type VARCHAR(50) DEFAULT 'RESIDENTIAL'
);

CREATE TABLE LoadMeasurements (
    measurement_id BIGSERIAL PRIMARY KEY,
    substation_id INT REFERENCES Substations(substation_id),
    timestamp TIMESTAMP NOT NULL,
    actual_load_mw FLOAT NOT NULL,
    temp_c FLOAT,
    h2_ppm FLOAT,
    health_score FLOAT,
    
    CONSTRAINT unique_measurement UNIQUE (substation_id, timestamp)
);

-- Створення індексів для прискорення OLAP-запитів
CREATE INDEX idx_load_timestamp ON LoadMeasurements(timestamp DESC);
CREATE INDEX idx_substation_id ON LoadMeasurements(substation_id);
```

## Додаток Г. Настанови користувача (Інструкція)

### Г.1. Вимоги до середовища
Для запуску системи необхідно мати встановлений **Docker** та **Docker Compose**. Весь інструментарій (Python, TensorFlow, PostgreSQL клієнти) автоматично налаштується всередині контейнера.

### Г.2. Запуск системи
1. Склонуйте репозиторій з кодом.
2. Створіть файл `.env` та вкажіть у ньому посилання на базу даних Neon: `DATABASE_URL=postgres://user:pass@host/db`.
3. Запустіть термінал у папці проєкту та виконайте команду:
   ```bash
   docker-compose up --build
   ```
4. Відкрийте браузер за адресою `http://localhost:8501`.

### Г.3. Робота з інтерфейсом
* **Панель моніторингу**: Оберіть підстанцію у бічному меню для перегляду поточних KPI.
* **Генерація прогнозу**: Перейдіть на вкладку "AI Forecast" та натисніть кнопку "Generate 24h Prediction".
* **Діагностика**: У розділі "Health Score" доступна детальна інформація про технічний стан трансформаторів.

## Додаток Д. Результати тестування (Протокол)

### Д.1. Результати модульного тестування (Unit Tests)
Тестування проводилося за допомогою фреймворку `pytest`.

| Модуль | Кількість тестів | Статус | Час виконання |
| :--- | :---: | :---: | :---: |
| `physics.py` (Math formulas) | 12 | PASSED | 0.45s |
| `vectorizer.py` (Data prep) | 8 | PASSED | 1.20s |
| `model_loader.py` (Resources) | 4 | PASSED | 2.10s |

### Д.2. Результати валідації ШІ-моделі (ML Validation)
Валідація проводилася на відкладеній вибірці (20% даних PJM Dayton).

| Метрика | Значення | Цільовий показник | Статус |
| :--- | :---: | :---: | :---: |
| **MAPE** | 3.08% | < 4.0% | УСПІШНО |
| **RMSE** | 42.15 MW | < 60.0 MW | УСПІШНО |
| **R² Score** | 0.92 | > 0.85 | УСПІШНО |
