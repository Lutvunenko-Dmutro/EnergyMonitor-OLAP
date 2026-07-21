# 🧠 Core System Architecture (`src/`)
**Ядро системи EnergyMonitor-OLAP (Source Code)**

This directory contains the primary source code for the EnergyMonitor-OLAP platform. The system is built using a highly modular, decoupled architecture to ensure scalability, ease of maintenance, and robust performance under heavy data loads.

Ця папка містить весь основний вихідний код платформи. Архітектура побудована за модульним принципом (Clean Architecture), що дозволяє легко масштабувати систему та підтримувати її стабільність.

---

## 🏗️ Directory Structure / Структура директорії

### 1. `app/` (Application Layer)
Contains global application configurations, lifecycle management, and shared data types.
*Містить глобальні конфігурації додатку, управління життєвим циклом та спільні типи даних (Types/Enums).*

### 2. `core/` (Core Analytics & Engines)
The mathematical and logical heart of the system.
*Математичне та логічне серце системи.*
- **`analytics/`**: High-performance data aggregation, filtering, and K-Means clustering algorithms.
- **`database/`**: Data Access Layer (DAL) handling asynchronous connections and queries to PostgreSQL.
- **`diagnostics/`**: Real-time security auditing and code health monitoring.
- **`physics.py`**: A dedicated Digital Twin physics engine that calculates power grid losses, resistance changes, and weather impacts.

### 3. `ml/` (Machine Learning Pipeline)
Dedicated subsystem for time-series forecasting and predictive analytics.
*Підсистема для прогнозування часових рядів та предиктивної аналітики.*
- Implements both Statistical models (ARIMA) and Deep Learning models (LSTM).
- Contains automated training pipelines, metrics engines, and model serialization (ONNX/H5).
- Includes the `models/` directory where production-ready weights and scalers are stored.

### 4. `services/` (Business Logic & Simulation)
Background services and business logic execution.
*Фонові сервіси та виконання бізнес-логіки.*
- **Data Mining**: Advanced trend analysis and anomaly detection.
- **Data Generator**: A telemetry simulator that mimics real-world power grid behavior for stress-testing.
- **Migrations**: Database seeding and schema migration services.

### 5. `ui/` (User Interface - Streamlit)
The frontend layer built on Streamlit, organized for maximum reusability.
*Фронтенд шар на базі Streamlit, організований для максимального перевикористання.*
- **`components/`**: Reusable UI widgets (cards, interactive Plotly charts).
- **`segments/`**: Larger structural blocks (Sidebars, Dashboards, Live KPI grids).
- **`views/`**: Full-page layouts (Map View, Finance, Generation, Advanced Analytics).

### 6. `utils/` (System Utilities)
*Допоміжні інструменти.*
- High-performance caching managers (`cache_manager.py`).
- Universal error handlers and system validators.
- Unified logging configuration (`logging_config.py`).

---

## 🚀 Technologies Used
- **Python 3.10+** (Strict typing enforced)
- **Machine Learning**: TensorFlow / Keras, Scikit-Learn, Statsmodels
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Streamlit
- **Database**: PostgreSQL, SQLAlchemy, Psycopg2
