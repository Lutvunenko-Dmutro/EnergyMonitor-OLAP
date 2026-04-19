<p align="center">Додаток А</p>
<p align="center">лістинги програмного коду</p>

Нижче наведено фрагменти вихідного коду ключових модулів інтелектуальної системи EnergyMonitor-OLAP.

А.1. Модуль фізичного моделювання та цифрового двійника (physics.py)
Цей модуль відповідає за розрахунок енергетичних характеристик у реальному часі та симуляцію стану обладнання підстанції.

```python
def calculate_line_losses(df_lines: pd.DataFrame) -> pd.DataFrame:
    """
    Розраховує втрати потужності в мережі для AC та HVDC ліній.
    Математична модель: 
    - AC: Losses ~ I^2 * R (квадратична залежність від навантаження)
    - HVDC: Losses ~ I * R (більш лінійна, менші втрати на дистанції)
    """
    if df_lines.empty:
        return df_lines
    df = df_lines.copy()
    
    if "line_type" not in df.columns:
        df["line_type"] = "AC"

    is_hvdc = df["line_type"] == "HVDC"
    
    # Базис втрат: 1.5% для DC, 3.5% для AC при піку
    loss_dc = (df["actual_load_mw"] * 0.015) * (df["load_pct"] / 100)
    loss_ac = (df["actual_load_mw"] * 0.035) * (df["load_pct"] / 100) ** 2
    
    df["losses_mw"] = np.where(is_hvdc, loss_dc, loss_ac)
    return df
```

А.2. Модуль інтелектуального прогнозування (predict_v2.py)
Реалізація логіки інференсу нейронної мережі LSTM із попередньою векторизацією даних.

```python
def generate_lstm_forecast():
    """Фрагмент реалізації інтелектуального передбачення з ковзним вікном."""
    for i in range(24):
        # 1. Прогноз на 1 крок вперед
        pred_scaled = model.predict(current_window, verbose=0)[0][0]
        
        # 2. Денормалізація та Доменна Адаптація
        pred_val = float(pred_scaled * (max_val - min_val) + min_val)
        pred_val = adaptive_scaling_v3(pred_val, context_mean, scaler)
        
        predictions.append(pred_val)
        
        # 3. Формування нового вектора ознак для T+1
        next_dt = start_dt + timedelta(hours=i+1)
        next_hr_sin = np.sin(2 * np.pi * next_dt.hour / 24)
        next_hr_cos = np.cos(2 * np.pi * next_dt.hour / 24)
        next_day_sin = np.sin(2 * np.pi * next_dt.dayofweek / 7)
        next_day_cos = np.cos(2 * np.pi * next_dt.dayofweek / 7)
        
        # 4. Зсув вікна (Rolling Window)
        current_window = np.roll(current_window, -1, axis=1)
        current_window[0, -1] = [pred_scaled, next_temp_scaled, next_cloud_scaled,
                                 next_hr_sin, next_hr_cos, next_day_sin, next_day_cos,
                                 next_is_weekend_scaled, next_demand_scaled]
    return predictions
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
