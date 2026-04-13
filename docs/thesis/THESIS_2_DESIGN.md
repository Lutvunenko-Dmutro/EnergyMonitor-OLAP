# РОЗДІЛ 2. ПРОЄКТУВАННЯ АРХІТЕКТУРИ СИСТЕМИ ENERGYMONITOR-OLAP

### 2.1. Опис архітектури платформи

Проєктування архітектури інтелектуальної системи EnergyMonitor-OLAP базується на принципах модульності, масштабованості та розділення відповідальності (Separation of Concerns). Для забезпечення стабільної роботи у хмарному середовищі та високої швидкості аналітичних обчислень було обрано **багатошарову архітектуру (Layered Architecture)**, що складається з чотирьох основних рівнів.

#### Логічна структура шарів (Layered Model)
Нижче наведено ієрархічну схему взаємодії основних компонентів системи (Рисунок 2.1):

```mermaid
graph TB
    subgraph UI["Рівень представлення (Streamlit)"]
        direction LR
        A1["KPI Панель"]
        A2["ML Прогноз"]
        A3["ГІС Карта"]
    end

    subgraph CORE["Інтелектуальний шар"]
        direction LR
        B1["LSTM v3\npredict_v2.py"]
        B3["Фізичний двигун\nphysics.py"]
        B4["Векторизатор\n(Sliding Window)"]
    end

    subgraph DATA["Шар даних (OLAP)"]
        direction LR
        C1[("PostgreSQL\nNeon Cloud")]
        C3["Цифровий двійник\nСимуляція сенсорів"]
    end

    subgraph DEVOPS["DevOps Шар"]
        direction LR
        D1["GitHub Actions\nCI/CD"]
        D2["Docker\nКонтейнер"]
    end

    UI -->|"Запит даних"| CORE
    CORE -->|"SQL SELECT"| DATA
    C3 -->|"SQL INSERT телеметрія"| C1
    B1 -->|"Результати ШІ"| UI
```
*Рисунок 2.1. Багатошарова архітектура інтелектуальної системи EnergyMonitor-OLAP*

#### Компонентна схема та середовища розгортання
Система спроєктована для роботи у гібридному середовищі, де генерація даних може відбуватися локально, а аналітика та прогнозування — у хмарному кластері (Рисунок 2.2):

```mermaid
graph TD
    subgraph Local ["💻 LOCAL ENVIRONMENT"]
        DG["data_generator.py\n(Симулятор)"]
    end

    subgraph Cloud ["☁️ CLOUD INFRASTRUCTURE (Render)"]
        DB[(PostgreSQL\nOLAP Database)]
        Vect["vectorizer.py"]
        Pred["predict_v2.py"]
        UI["main.py\n(Dashboard)"]
    end

    DG ==>|"Telemetry Push"| DB
    DB <-->|"Data Exchange"| Vect
    Vect --> Pred
    Pred --> UI
```
*Рисунок 2.2. UML-діаграма компонентів та розподілу середовищ*

#### Діаграма послідовності обробки прогнозу
Для глибшого розуміння динаміки системи розглянемо процес обробки запиту користувача на отримання прогнозу споживання (Рисунок 2.3):

```mermaid
sequenceDiagram
    participant User as Користувач
    participant UI as Streamlit UI
    participant Core as ML Controller
    participant Vect as Vectorizer
    participant DB as PostgreSQL
    participant Model as LSTM v3

    User->>UI: Натискання кнопки "Отримати прогноз"
    UI->>Core: Запит на інференс (sub_name)
    Core->>Vect: Підготовка вікна даних (look-back)
    Vect->>DB: SQL SELECT (останні 24 години)
    DB-->>Vect: Набір телеметрії
    Vect->>Vect: Нормалізація та sin/cos кодування
    Vect-->>Core: Вхідний тензор (24, 9)
    Core->>Model: Виконання прогнозу
    Model-->>Core: Результати (t+1 ... t+24)
    Core-->>UI: Денормалізований масив даних
    UI->>User: Візуалізація графіка Plotly
```
*Рисунок 2.3. Sequence Diagram процесу інтелектуального прогнозування*

### 2.2. Реалізація аналітичної бази даних

Центральним сховищем системи є реляційна база даних PostgreSQL 15. Вибір реляційної моделі зумовлений необхідністю суворої типізації даних телеметрії та складною структурою взаємозв’язків між об’єктами енергосистеми.

#### Схема даних (ER-діаграма)
Структура бази даних спроєктована за принципом «зірка» (Star Schema). Центром схеми є таблиці фактів (вимірювання), які пов’язані з таблицями вимірів (довідники об’єктів).

```mermaid
erDiagram
    REGIONS ||--o{ SUBSTATIONS : "містить"
    SUBSTATIONS ||--o{ LOADMEASUREMENTS : "генерує навантаження"
    SUBSTATIONS ||--o{ ALERTS : "генерує аварії"
    SUBSTATIONS ||--o{ GENERATORS : "має джерела"
    GENERATORS ||--o{ GENERATIONMEASUREMENTS : "виробляє енергію"
    REGIONS ||--o{ WEATHERREPORTS : "має погоду"

    REGIONS {
        int region_id PK
        string region_name
    }
    SUBSTATIONS {
        int substation_id PK
        string substation_name
        float capacity_mw
    }
    LOADMEASUREMENTS {
        int measurement_id PK
        float actual_load_mw
        float health_score
        timestamp timestamp
    }
```

#### SQL-запити та OLAP-обробка
Для забезпечення швидкодії інтерфейсу система використовує складні SQL-запити з поєднанням даних (JOIN) на рівні серверу БД. Прикладом є запит для кореляції навантаження та погодних умов:

```sql
SELECT 
    lm.timestamp,
    r.region_name,
    lm.actual_load_mw,
    s.substation_name,
    wr.temperature
FROM LoadMeasurements lm
JOIN Substations s ON lm.substation_id = s.substation_id
JOIN Regions r ON s.region_id = r.region_id
LEFT JOIN WeatherReports wr ON 
    lm.timestamp = wr.timestamp 
    AND r.region_id = wr.region_id
WHERE lm.timestamp >= NOW() - INTERVAL '30 days'
ORDER BY lm.timestamp ASC;
```

### 2.3. Проєктування модуля інтелектуального прогнозування

Архітектура модуля прогнозування побудована як замкнений ETL-конвеєр (Extraction, Transformation, Loading), що інтегрує фізичне моделювання та методи глибокого навчання.

#### Механізм «Цифрового двійника»
Для генерації потоку даних реалізовано модуль спеціальної симуляції, що виконує роль цифрового аналога енергомережі. Система використовує фонові процеси та механізми контролю станів (lock-файли) для забезпечення цілісності даних.

#### Конвеєр підготовки даних
Взаємодія симулятора з прогнозуючим ядром відбувається через наступні етапи:
1.  **Extraction**: Вилучення історичного вікна даних з бази.
2.  **Transformation**: Застосування методу ковзного вікна для формування вхідних тензорів.
3.  **Inference**: Обробка даних LSTM-моделлю та видача результату.

---
[⬅️ Назад до Розділу 1](THESIS_1_THEORY.md) | [Далі: Розділ 3 ➡️](THESIS_3_ML_CORE.md)
