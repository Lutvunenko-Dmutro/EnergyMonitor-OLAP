<p align="center">Додаток А</p>
<p align="center">лістинги програмного коду</p>

Нижче наведено фрагменти вихідного коду ключових модулів інтелектуальної системи **EnergyMonitor-OLAP**.

**А.1. Модуль фізичного моделювання та цифрового двійника (physics.py)**
Цей модуль відповідає за розрахунок енергетичних характеристик у реальному часі та симуляцію стану обладнання.

```python
def calculate_line_losses(df_lines: pd.DataFrame) -> pd.DataFrame:
    """Розраховує втрати потужності в мережі для AC та HVDC ліній."""
    if df_lines.empty: return df_lines
    df = df_lines.copy()
    
    is_hvdc = df["line_type"] == "HVDC"
    # Базис втрат: 1.5% для DC, 3.5% для AC при піку навантаження
    loss_dc = (df["actual_load_mw"] * 0.015) * (df["load_pct"] / 100)
    loss_ac = (df["actual_load_mw"] * 0.035) * (df["load_pct"] / 100) ** 2
    
    df["losses_mw"] = np.where(is_hvdc, loss_dc, loss_ac)
    return df

def estimate_grid_stability(load_mw: float, gen_mw: float) -> str:
    """Оцінює стабільність енергосистеми на основі балансу."""
    if gen_mw <= 0: return "Критично"
    ratio = load_mw / gen_mw
    if ratio > 1.2: return "Критично"
    if ratio > 1.05: return "Попередження"
    return "Стабільно"
```

**А.2. Модуль інтелектуального прогнозування LSTM (predict_v2.py)**
Реалізація логіки рекурентного інференсу нейронної мережі з попередньою обробкою ознак.

```python
def get_ai_forecast(hours_ahead=24, substation_name=None):
    """Генерує високоточний прогноз з використанням моделі LSTM v3."""
    # 1. Завантаження вікна останніх 48 годин
    values, last_ts = get_latest_window(substation_name, window_size=48)
    
    # 2. Тригонометричне кодування часу для усунення розривів 23:00-00:00
    future_ts = [last_ts + pd.Timedelta(hours=i+1) for i in range(hours_ahead)]
    sin_h = np.sin(2 * np.pi * np.array([ts.hour for ts in future_ts]) / 24)
    cos_h = np.cos(2 * np.pi * np.array([ts.hour for ts in future_ts]) / 24)
    
    # 3. Рекурентне передбачення (rolling window strategy)
    for i in range(hours_ahead):
        x_input = current_window.reshape(1, 48, 9)
        pred_scaled = model.predict(x_input)[0][0]
        
        # Оновлення вікна результатами попереднього кроку
        new_row = [pred_scaled, next_temp, health, sin_h[i], cos_h[i]...]
        current_window = np.append(current_window[1:], [new_row], axis=0)
        
    return inverse_transform(all_predictions)
```

**А.3. Архітектура нейронної мережі та навчання (train_lstm.py)**
Визначення структури шарів моделі та функцій оптимізації.

```python
def build_model_v3(window_size, n_features):
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=(window_size, n_features)),
        LSTM(64, return_sequences=False),
        Dense(32, activation='relu'),
        Dense(1) 
    ])
    # Використання Huber Loss для робастності до викидів у телеметрії
    model.compile(optimizer="adam", loss="huber")
    return model
```

<hr>

<p align="center">Додаток Б</p>
<p align="center">структура об'єктів бази даних</p>

Для зберігання аналітичних даних та телеметрії використовується реляційна СУБД PostgreSQL.

```sql
-- Таблиця описів енергетичних вузлів
CREATE TABLE Substations (
    substation_id SERIAL PRIMARY KEY,
    substation_name VARCHAR(100) UNIQUE,
    region_id INTEGER REFERENCES Regions(region_id),
    capacity_mw FLOAT CHECK (capacity_mw > 0)
);

-- Таблиця фактів телеметрії (OLAP-ядро)
CREATE TABLE LoadMeasurements (
    measurement_id SERIAL PRIMARY KEY,
    substation_id INTEGER REFERENCES Substations(substation_id),
    actual_load_mw FLOAT NOT NULL,
    oil_temp FLOAT,
    h2_ppm FLOAT,
    health_score FLOAT DEFAULT 100,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Індекси для прискорення аналітичних зрізів
CREATE INDEX idx_substation_time ON LoadMeasurements (substation_id, timestamp DESC);
```

<hr>

<p align="center">Додаток В</p>
<p align="center">протокол тестування та верифікації</p>

Для забезпечення надійності системи EnergyMonitor-OLAP було розроблено та успішно виконано набір із **79 автоматизованих тестів**.

| Тип тестування | Кількість тестів | Модулі, що охоплені | Результат |
| :--- | :---: | :--- | :---: |
| Unit Testing | 45 | physics.py, vectorizer.py | PASSED |
| Integration Testing | 22 | db_connector, model_loader | PASSED |
| System Testing | 12 | forecasting_pipeline, UI | PASSED |

**Приклад виводу автоматизованого звіту (pytest summary):**
```text
collected 79 items
tests/test_physics.py ....... [ 8%]
tests/test_ml_logic.py .......... [ 21%]
tests/test_database.py ............... [ 40%]
...
================ 79 passed, 0 failed in 12.45s ================
```

<hr>

<p align="center">Додаток Г</p>
<p align="center">настанови користувача (user manual)</p>

Програмний комплекс надає оператору 8 функціональних вкладок для моніторингу та аналізу:

1. **Карта мережі**: Геопросторова візуалізація стану підстанцій (Digital Twin).
2. **Споживання**: Динаміка навантаження в реальному часі.
3. **Генерація**: Огляд джерел енергії та баланс мережі.
4. **Журнал аварій**: Оперативне керування інцидентами та Health Score.
5. **Економіка**: Розрахунок виторгу та вартості енерговтрат.
6. **AI Аналітика**: Кластеризація та Anomaly Detection.
7. **Прогноз ШІ**: LSTM-прогнозування на наступні 24 години з довірчим інтервалом.
8. **Цифровий архів**: OLAP-зрізи та експорт даних у CSV/Excel.

**Рекомендації:** Для запуску предиктивного аналізу необхідно вибрати конкретну підстанцію в сайдбарі та натиснути вкладку «Прогноз ШІ».

---
[Назад до Списку джерел](BIBLIOGRAPHY.md)
