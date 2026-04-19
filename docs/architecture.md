# 🏗️ Архітектура системи

## Огляд (4 шари)

```mermaid
%%{init: {'theme': 'dark'}}%%
graph TB
    subgraph UI["🌐 Presentation Layer"]
        A1["📊 KPI Dashboard\nlive_kpi.py"]
        A2["📈 ML Forecast\nforecast.py"]
        A3["🗺️ Geo Map\nmap.py"]
        A4["⚠️ Alerts\nalerts.py"]
        A5["📜 Archive\nhistorical_audit.py"]
    end

    subgraph CORE["🧠 Intelligence Layer"]
        B1["LSTM v3\npredict_v2.py"]
        B2["Fallback\nbaseline_arima.py"]
        B3["Physics\nphysics.py"]
        B4["Vectorizer\nvectorizer.py"]
    end

    subgraph DATA["💾 Data Layer"]
        C1[("PostgreSQL\nNeon Cloud")]
        C2["Cache TTL 24h\ncache_manager.py"]
        C3["Digital Twin\nsensors_db.py"]
    end

    subgraph DEVOPS["⚙️ DevOps"]
        D1["GitHub Actions\nCI/CD"]
        D2["Docker"]
        D3["Render.com"]
    end

    UI --> CORE --> DATA
    C3 --> C1
    DEVOPS --> UI

    style UI fill:#0d1117,stroke:#58a6ff
    style CORE fill:#0d1117,stroke:#ffb703
    style DATA fill:#0d1117,stroke:#00ff88
    style DEVOPS fill:#0d1117,stroke:#ff6b6b
```

---

## Presentation Layer (UI)

Реалізований на **Streamlit** як набір незалежних view-модулів.

| Модуль | Файл | Призначення |
|--------|------|-------------|
| KPI Dashboard | `ui/segments/live_kpi.py` | Live телеметрія (auto-refresh 5s) |
| ML Forecast | `ui/views/forecast.py` | LSTM прогноз на 24 год. |
| Geo Map | `ui/views/map.py` | Geomap підстанцій |
| Alerts | `ui/views/alerts.py` | Управління аваріями |
| Archive | `ui/views/historical_audit.py` | OLAP архів |
| Sidebar | `ui/segments/sidebar.py` | Фільтри + керування Digital Twin |

---

## Intelligence Layer (ML)

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    DB[("DB: last 48h")] --> VEC["vectorizer.py\nSliding Window"]
    VEC --> FEAT["Feature Engineering\n9 features + sin/cos time"]
    FEAT --> LSTM["LSTM v3\npredict_v2.py"]
    LSTM --> ADAPT["Domain Adaptation\n(substation scaling)"]
    ADAPT --> OUT["df_forecast\n24 годин"]

    LSTM -- "Якщо unavailable" --> FALL["Seasonal Naive\nbaseline_arima.py"]
    FALL --> OUT
```

**Версії моделей:**

| Версія | Ознак | Таргети | Особливість |
|--------|-------|---------|-------------|
| v1 | 1 | 1 | Базова (load_mw) |
| v2 | 5 | 2 | + Погода + Health |
| v3 | 9 | 2 | + Часові гармоніки sin/cos |
| Zero-Fail | — | 2 | Seasonal Naive Fallback |

---

## Data Layer

### PostgreSQL (Neon Cloud)

```sql
-- Ключові таблиці
Regions           -- Регіони (Київ, Харків...)
Substations       -- Підстанції (підкатегорія регіону)
LoadMeasurements  -- Телеметрія (MW, Health, H2, температура)
Predictions       -- Збережені прогнози LSTM
Alerts            -- Аварійні події
WeatherReports    -- Погода по регіонах
```

### Cache Manager

```python
# utils/cache_manager.py
# TTL = 24 годин
# Захищає: *.graphml (карти міст)
# Очищає: *.json (застарілі запити)
startup_cache_cleanup(ttl_hours=24)  # викликається з main.py
```

---

## 🧬 Потоки даних (Data Flows)

### Послідовність прогнозування (Forecasting Sequence)

Наступна діаграма демонструє шлях даних від запиту користувача до візуалізації ШІ-прогнозу.

```mermaid
%%{init: {'theme': 'dark'}}%%
sequenceDiagram
    participant U as 👤 Користувач
    participant UI as 🖥️ UI (Streamlit)
    participant V as 🧪 Vectorizer
    participant DB as 💾 PostgreSQL
    participant ML as 🧠 LSTM Model
    participant S as 📉 Scaler (Domain Adaptation)

    U->>UI: Вибір підстанції
    UI->>DB: Запит вікна 48 год.
    DB-->>UI: df_history (raw)
    UI->>V: get_latest_window(df)
    V->>V: FE: sin/cos, normalization
    V-->>UI: model_input_tensor
    UI->>ML: model.predict(input)
    ML-->>UI: raw_forecast (0..1)
    UI->>S: inverse_transform() + scale_factor
    S-->>UI: final_forecast (MW)
    UI->>U: Відображення графіка
```

---

## ⚙️ DevOps Layer

### Детальний CI/CD Pipeline

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart TD
    Build[Build Phase] --> Test[Test Phase]
    Test --> Security[Security Phase]
    Security --> Deploy[Deploy Phase]

    subgraph Build
        B1["Docker build\n(Multi-stage)"]
    end

    subgraph Test
        T1["pytest\n(79 tests)"]
        T2["mypy\n(Type check)"]
    end

    subgraph Security
        S1["bandit\n(SAST)"]
        S2["detect-secrets"]
    end

    subgraph Deploy
        D1["Push to Registry\n(Docker Hub)"]
        D2["Render.com\nWebHook"]
    end
```

### Ключові конфіги

| Файл | Призначення |
|------|-------------|
| `Dockerfile` | Multi-stage Docker build |
| `.github/workflows/ci-cd.yml` | GitHub Actions pipeline |
| `mkdocs.yml` | MkDocs документація |
| `.env.example` | Шаблон змінних середовища |

---

---

## 📐 Математичний додаток (Academic Appendix)

### 1. Кластеризація підстанцій (K-Means)

Для сегментації об'єктів (вкладка AI Аналітика) використовується алгоритм K-Means. Математична мета полягає у мінімізації сумарного квадратичного відхилення точок кластерів від їх центроїдів:

$$J = \sum_{j=1}^{k} \sum_{x \in C_j} \|x - \mu_j\|^2$$

Де:
- $k$ — кількість кластерів (визначається методом ліктя).
- $C_j$ — множина точок $j$-го кластера.
- $\mu_j$ — центроїд (середнє значення) кластера $C_j$.

**Вектор ознак для кластеризації:**
- $\bar{L}$: Середнє навантаження за період.
- $\sigma_L$: Стандартне відхилення (показник волатильності).
- $H$: Середній показник Health Score.

Це дозволяє автоматично виділяти «вузлові», «промислові» та «критичні» підстанції без втручання оператора.
