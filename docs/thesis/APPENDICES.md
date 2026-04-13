# ДОДАТКИ

### ДОДАТОК А. Фрагменти програмного коду інтелектуального ядра

```python
def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(128, input_shape=input_shape, return_sequences=True),
        Dropout(0.2),
        LSTM(64, return_sequences=False),
        Dropout(0.1),
        Dense(32, activation='relu'),
        Dense(2)
    ])
    model.compile(optimizer='adam', loss='huber')
    return model
```

### ДОДАТОК Б. Протокол автоматизованого тестування

| Група тестів | Кількість | Результат | Опис |
| :--- | :---: | :---: | :--- |
| Security (SQLi, XSS) | 26 | Passed | Перевірка захищеності від ін'єкцій |
| Database Layer | 4 | Passed | Коректність OLAP-запитів |
| ML Pipeline | 3 | Passed | Цілісність вхідних тензорів |
| Physics Engine | 5 | Passed | Верифікація фізичних законів |
| Core Analytics | 11 | Passed | Розрахунок KPI та здоров'я |
| Utilities | 19 | Passed | Обробка кешу та конфігурацій |

### ДОДАТОК В. Специфікація середовища розгортання (Dockerfile)

```dockerfile
FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### ДОДАТОК Г. Ілюстративні матеріали програмного комплексу

Нижче наведено повну серію контрольних знімків екрана, що демонструють функціональні можливості системи EnergyMonitor-OLAP.

#### 1. Системні компоненти та завантаження
![Рисунок Г.1. Екран ініціалізації системи](../../docs/images/boot_1.png)
![Рисунок Г.2. Процес завантаження та автентифікації](../../docs/images/boot_loader.png)

#### 2. Моніторинг та ГІС-аналітика
![Рисунок Г.3. Глобальна карта енергосистеми](../../docs/images/map.png)
![Рисунок Г.4. Панель моніторингу споживання за регіонами](../../docs/images/consumption.png)
![Рисунок Г.5. Розподіл генерації за джерелами енергії](../../docs/images/generation.png)

#### 3. Інтелектуальний аналіз та прогнозування
![Рисунок Г.6. Інтерфейс ШІ-прогнозування (LSTM v3)](../../docs/images/ai_forecast.png)
![Рисунок Г.7. Порівняльний аудит моделей прогнозування](../../docs/images/audit_comparison.png)
![Рисунок Г.8. Кластеризація споживачів методом K-Means](../../docs/images/clustering.png)

#### 4. Цифровий двійник та фізичний стан
![Рисунок Г.9. Моніторинг здоров'я трансформаторів](../../docs/images/health_monitoring.png)
![Рисунок Г.10. Аналіз впливу погодних умов](../../docs/images/weather_impact.png)
![Рисунок Г.11. Динаміка добових циклів навантаження](../../docs/images/day_cycle_raw.png)

#### 5. Верифікація на еталонних даних (Kaggle PJM)
![Рисунок Г.12. Робота системи на великих даних PJM](../../docs/images/kaggle_consumption.png)
![Рисунок Г.13. Глобальний прогноз для мережі Kaggle](../../docs/images/kaggle_global_forecast.png)

---
[⬅️ Назад до Списку джерел](BIBLIOGRAPHY.md) | [На головну сторінку системи](../../README.md)
