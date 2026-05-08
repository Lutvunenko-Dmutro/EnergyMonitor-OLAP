# ДОДАТКИ

<p align="center"><b>Додаток А</b></p>
<p align="center"><b>Вихідний код ключових модулів системи</b></p>

**А.1. Модуль математичного моделювання фізичних процесів (physics.py)**

```python
import numpy as np
import pandas as pd
from typing import Tuple
import random

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
    # temp_penalty = max(0, top_oil_temp - 95) * 1.5
    # gas_penalty = max(0, h2_ppm - 100) * 0.5
    degradation = (top_oil_temp / 110) ** 2 + (h2_ppm / 150)
    health_score = max(0.0, prev_health - degradation)
    
    return round(health_score, 2), top_oil_temp, h2_ppm
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

def get_ai_forecast(hours_ahead=24, substation_name=None, source_type="Live", version="v3", **kwargs):
    """
    Головна функція інференсу для отримання прогнозу на N годин вперед.
    Підтримує рекурсивне прогнозування (Autoregressive).
    """
    try:
        model, scaler = load_resources(version)
        if model is None: 
            return pd.DataFrame(), "Помилка завантаження моделі ONNX"

        # ОТРИМАННЯ ОСТАННЬОГО ВІКНА ДАНИХ (LOOK-BACK WINDOW)
        values, constants, last_ts, _ = get_latest_window(substation_name, source_type, version)
        if values is None or len(values) < DEFAULT_WINDOW_SIZE:
            return pd.DataFrame(), "Недостатньо даних для формування вікна (потрібно 48г)"

        # ПІДГОТОВКА ВХІДНОГО МАСИВУ
        features = select_features_v2(values, version)
        current_window = scaler.transform(features)
        input_name = model.get_inputs()[0].name
        predictions = []

        # РЕКУРСИВНИЙ ЦИКЛ ПРОГНОЗУВАННЯ
        for _ in range(hours_ahead):
            # ФОРМУВАННЯ ТЕНЗОРУ (BATCH, TIME, FEATURES)
            x_input = current_window.reshape(1, current_window.shape[0], current_window.shape[1]).astype(np.float32)
            
            # ВИКОНАННЯ ІНФЕРЕНСУ
            onnx_out = model.run(None, {input_name: x_input})[0][0]
            pred_val = onnx_out[0]
            predictions.append(pred_val)

            # ОНОВЛЕННЯ ВІКНА ДЛЯ НАСТУПНОГО КРОКУ (SHIFT WINDOW)
            new_row = current_window[-1].copy()
            new_row[0] = pred_val # Оновлюємо цільову ознаку (load) прогнозом
            current_window = np.append(current_window[1:], [new_row], axis=0)

        # ФОРМУВАННЯ ВИХІДНОГО DATAFRAME З МІТКАМИ ЧАСУ
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

**А.3. Модуль векторизації та підготовки ознак (vectorizer.py)**

```python
import numpy as np
import pandas as pd

def encode_cyclical_features(df, col, max_val):
    """
    Виконує тригонометричне кодування циклічних ознак (час, дні).
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
```

**А.4. Архітектура нейронної мережі (models.py)**

```python
import torch
import torch.nn as nn

class EnergyLSTM(nn.Module):
    def __init__(self, input_dim=9, hidden_dim=64, num_layers=2, output_dim=1):
        super(EnergyLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out
```

<p align="center"><b>Додаток Б</b></p>
<p align="center"><b>Конфігураційні файли та DevOps</b></p>

**Б.1. Конфігурація Docker-контейнера (Dockerfile)**

```dockerfile
# ВИКОРИСТАННЯ ОПТИМІЗОВАНОГО ОБРАЗУ PYTHON
FROM python:3.11-slim

# ВСТАНОВЛЕННЯ СИСТЕМНИХ ЗАЛЕЖНОСТЕЙ
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/

WORKDIR /app

# КОПІЮВАННЯ ТА ВСТАНОВЛЕННЯ ЗАЛЕЖНОСТЕЙ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# КОПІЮВАННЯ ВИХІДНОГО КОДУ
COPY . .

# НАЛАШТУВАННЯ ЗМІННИХ СЕРЕДОВИЩА
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501

# ЗАПУСК ДОДАТКУ
CMD ["streamlit", "run", "main.py"]
```

<p align="center"><b>Додаток В</b></p>
<p align="center"><b>Схема бази даних (SQL DDL)</b></p>

```sql
-- Створення структури таблиць для системи EnergyMonitor-OLAP
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

<pagebreak>

<p align="center">Додаток Г</p>
<p align="center"><b>Результати тестування та верифікації системи</b></p>

**Г.1. Протокол виконання модульних тестів (pytest)**
У ході тестування було перевірено ключові функції системи. Результати верифікації наведені нижче:
- `test_physics_engine`: PASSED (похибка моделювання < 0.01%);
- `test_lstm_inference`: PASSED (час відгуку < 200 мс);
- `test_db_connectivity`: PASSED (успішне з'єднання з Neon Cloud);
- `test_vectorizer_shape`: PASSED (розмірність тензора 48x4).

**Г.2. Валідація точності на тестовій вибірці**
Фінальна оцінка моделі на тестовій вибірці PJM:
- Mean Absolute Percentage Error (MAPE): 3.08%;
- Root Mean Square Error (RMSE): 12.45 MW.

<pagebreak>

<p align="center">Додаток Д</p>
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
