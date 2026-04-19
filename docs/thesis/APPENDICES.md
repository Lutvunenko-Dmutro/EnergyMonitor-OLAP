<p align="center">Додаток А</p>
<p align="center">лістинги програмного коду</p>

Нижче наведено фрагменти вихідного коду ключових модулів інтелектуальної системи EnergyMonitor-OLAP.

А.1. Модуль фізичного моделювання та цифрового двійника (physics.py)
Цей модуль відповідає за розрахунок енергетичних характеристик у реальному часі та симуляцію стану обладнання підстанції.

```python
import numpy as np

def calculate_physics_telemetry(actual_load, capacity_mw):
    """
    Розрахунок фізичних параметрів на основі навантаження
    та стану обладнання підстанції.
    """
    # 1. Розрахунок термічної деградації (наближена модель)
    temp_factor = actual_load / capacity_mw
    oil_temp = 40 + (temp_factor * 50) + np.random.normal(0, 2)
    
    # 2. Розрахунок втрат у лінії електропередачі (ЛЕП)
    # Формула втрат P = I^2 * R
    resistance = 0.05  # Опір (Ом)
    line_losses = (actual_load ** 2) * resistance * 0.001
    
    # 3. Інтегральний показник здоров'я (Health Score)
    health_score = 100 - (temp_factor * 15) - (oil_temp / 10)
    
    return {
        "oil_temp": round(oil_temp, 2),
        "line_losses": round(line_losses, 4),
        "health_score": round(max(0, health_score), 2)
    }
```

А.2. Модуль інтелектуального прогнозування (predict_v2.py)
Реалізація логіки інференсу нейронної мережі LSTM із попередньою векторизацією даних.

```python
import tensorflow as tf
import numpy as np

def generate_lstm_forecast(model, input_window):
    """
    Генерація прогнозу на 24 години на основі look-back вікна.
    input_window shape: (1, 48, 9)
    """
    # Виконання інференсу (Single step ahead)
    prediction = model.predict(input_window, verbose=0)
    
    # Денормалізація (приклад зворотного MinMaxScaler)
    # actual_val = prediction * (max_val - min_val) + min_val
    
    return prediction

def encode_time_cyclic(hour, day_of_week):
    """
    Тригонометричне кодування часу (Sin/Cos Encoding)
    """
    hr_sin = np.sin(2 * np.pi * hour / 24)
    hr_cos = np.cos(2 * np.pi * hour / 24)
    
    day_sin = np.sin(2 * np.pi * day_of_week / 7)
    day_cos = np.cos(2 * np.pi * day_of_week / 7)
    
    return hr_sin, hr_cos, day_sin, day_cos
```

А.3. Опис структури об'єктів бази даних (schema.sql)
Схема таблиць для зберігання телеметрії та результатів аналітики.

```sql
-- Таблиця фактів навантаження
CREATE TABLE LoadMeasurements (
    measurement_id SERIAL PRIMARY KEY,
    substation_id INTEGER REFERENCES Substations(substation_id),
    actual_load_mw FLOAT NOT NULL,
    oil_temp FLOAT,
    line_losses FLOAT,
    health_score FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблиця регіонів та метеоумов
CREATE TABLE WeatherReports (
    report_id SERIAL PRIMARY KEY,
    region_id INTEGER REFERENCES Regions(region_id),
    temperature FLOAT,
    humidity FLOAT,
    timestamp TIMESTAMP
);

-- OLAP індекс для швидкого пошуку за часом
CREATE INDEX idx_load_time ON LoadMeasurements (timestamp DESC);
```

---
[Назад до Списку джерел](BIBLIOGRAPHY.md)
