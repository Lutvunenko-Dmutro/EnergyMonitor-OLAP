# 🗺️ Атлас Проєкту: Інтерактивна Карта

Ця сторінка є вашим навігатором по архітектурі **Energy Monitor ULTIMATE**. Кожен вузол на схемі нижче є клікабельним — він переведе вас до детального технічного розбору конкретного файлу або модуля.

---

## 🏗️ Архітектурна Схема (Інтерактивна)

```mermaid
graph TD
    %% Стилізація вузлів
    classDef ui fill:#e1bee7,stroke:#7b1fa2,stroke-width:2px,color:#000
    classDef ml fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#000
    classDef core fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#000
    classDef services fill:#f1f8e9,stroke:#689f38,stroke-width:2px,color:#000
    classDef infra fill:#f5f5f5,stroke:#616161,stroke-width:2px,color:#000

    subgraph ENTRY ["🏁 Точка входу"]
        MAIN["main.py<br/>(Оркестратор)"]:::ui
    end

    subgraph UI_LAYER ["🎨 Інтерфейс (Streamlit)"]
        DASHBOARD["dashboard.py<br/>(UI Logic)"]:::ui
        VIEWS["views/<br/>(Pages)"]:::ui
        COMPONENTS["components/<br/>(Design)"]:::ui
    end

    subgraph ML_LAYER ["🧠 AI Pipeline (LSTM)"]
        PREDICT["predict_v2.py<br/>(AI Controller)"]:::ml
        VECTOR["vectorizer.py<br/>(Data Prep)"]:::ml
        MODELS["models/<br/>(Weights)"]:::ml
    end

    subgraph CORE_LAYER ["⚙️ Аналітичне Ядро"]
        PHYSICS["physics.py<br/>(Grid Physics)"]:::core
        DB_LOAD["loader.py<br/>(Data Service)"]:::core
        ANALYTICS["analytics/<br/>(OLAP)"]:::core
    end

    subgraph SERVICES_LAYER ["🏭 Digital Twin / Services"]
        SENSORS["sensors_db.py<br/>(Live Sim)"]:::services
        GEN["data_generator.py<br/>(ETL)"]:::services
    end

    %% Зв'язки
    MAIN --> DASHBOARD
    DASHBOARD --> VIEWS
    VIEWS --> PREDICT
    PREDICT --> VECTOR
    VECTOR --> CORE_LAYER
    CORE_LAYER --> DB_LOAD
    SENSORS --> CORE_LAYER

    %% Клікабельні посилання (Anchors)
    click MAIN "map/ui_map.md#main-py" "Переглянути опис main.py"
    click DASHBOARD "map/ui_map.md#dashboard-py" "Переглянути опис dashboard.py"
    click PHYSICS "map/core_map.md#physics-py" "Переглянути опис physics.py"
    click PREDICT "map/ml_map.md#predict-v2-py" "Переглянути опис predict_v2.py"
    click SENSORS "map/services_map.md#sensors-db-py" "Переглянути опис sensors_db.py"
    click DB_LOAD "map/core_map.md#loader-py" "Переглянути опис loader.py"
```

---

## 🔍 Як користуватися Атласом?

1.  **Натисніть на вузол:** Вас буде перенаправлено до секції з технічним описом.
2.  **Шари системи:**
    *   🟣 **UI (Фіолетовий):** Все, що бачить користувач у браузері.
    *   🟡 **ML (Золотий):** Інтелект системи — прогнози та метрики.
    *   🔵 **CORE (Синій):** Розрахунки, фізика енергосистем та робота з БД.
    *   🟢 **SERVICES (Зелений):** Фонова симуляція (Digital Twin).

---

## 🗄️ Швидка навігація по розділах

| Шар | Детальний опис | Ключові технології |
| :--- | :--- | :--- |
| **🎨 User Interface** | [Перейти до UI Map](map/ui_map.md) | Streamlit, Plotly, Folium |
| **🧠 Machine Learning** | [Перейти до ML Map](map/ml_map.md) | TensorFlow, ONNX, Scikit-learn |
| **⚙️ Core Analytics** | [Перейти до Core Map](map/core_map.md) | NumPy, Pandas, SQLAlchemy |
| **🏭 System Services** | [Перейти до Services Map](map/services_map.md) | Digital Twin, Real-time Sim |
