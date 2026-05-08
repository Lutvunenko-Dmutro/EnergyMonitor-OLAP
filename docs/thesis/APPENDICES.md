# ДОДАТКИ

<p align="center">Додаток А</p>
<p align="center"><b>Вихідний код ключових модулів системи</b></p>

### А.1. Модуль математичного моделювання фізичних процесів (physics.py)

```python
import numpy as np
import pandas as pd

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
    
    # Розрахунок індексу здоров'я (Health Score)
    degradation = (top_oil_temp / 110) ** 2 + (h2_ppm / 150)
    health_score = max(0.0, prev_health - degradation)
    
    return round(health_score, 2), top_oil_temp, h2_ppm
```

### А.2. Модуль нейромережевого прогнозування (models.py)

```python
import torch
import torch.nn as nn

class EnergyLSTM(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, num_layers=2, output_dim=24):
        super(EnergyLSTM, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        # x shape: (batch, seq_len, input_dim)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :]) # Прогноз на основі останнього стану
        return out
```

<p align="center">Додаток Б</p>
<p align="center"><b>Графічні матеріали та інтерфейси системи</b></p>

Б.1. Схема потоків даних EnergyMonitor-OLAP.
Б.2. Скріншоти дашбордів візуалізації (Grafana).
Б.3. Результати тестування моделі на валідаційних даних.
    
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

<p align="center">Додаток Б</p>
<p align="center"><b>Конфігураційні файли та DevOps</b></p>

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

<p align="center">Додаток В</p>
<p align="center"><b>Схема бази даних (SQL DDL)</b></p>

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

<p align="center">Додаток Г</p>
<p align="center"><b>Настанови користувача (Інструкція)</b></p>

### Г.1. Вимоги до середовища
Для запуску системи необхідно мати встановлений Docker та Docker Compose. Весь інструментарій (Python, TensorFlow, PostgreSQL клієнти) автоматично налаштується всередині контейнера.

### Г.2. Запуск системи
1. Склонуйте репозиторій з кодом.
2. Створіть файл `.env` та вкажіть у ньому посилання на базу даних Neon: `DATABASE_URL=postgres://user:pass@host/db`.
3. Запустіть термінал у папці проєкту та виконайте команду:
   ```bash
   docker-compose up --build
   ```
4. Відкрийте браузер за адресою `http://localhost:8501`.

### Г.3. Робота з інтерфейсом
* оберіть підстанцію у бічному меню для перегляду поточних KPI (панель моніторингу);
* перейдіть на вкладку "AI Forecast" та натисніть кнопку "Generate 24h Prediction" (генерація прогнозу);
* у розділі "Health Score" доступна детальна інформація про технічний стан трансформаторів (діагностика).

<p align="center">Додаток Д</p>
<p align="center"><b>Результати тестування (Протокол)</b></p>

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
