<p align="right">
  <a href="README.md"><img src="https://flagcdn.com/24x18/us.png" alt="English"> English</a> |
  <a href="README.uk.md"><img src="https://flagcdn.com/24x18/ua.png" alt="Українська"> Українська</a>
</p>

---

# 🧠 Core System Architecture (`src/`)

This directory contains the primary source code for the EnergyMonitor-OLAP platform. The system is built using a highly modular, decoupled architecture (Clean Architecture) to ensure scalability, ease of maintenance, and robust performance under heavy data loads.

## 🏗️ Directory Structure

### 1. `app/` (Application Layer)
Contains global application configurations, lifecycle management, and shared data types (`Enums`, `Types`).

### 2. `core/` (Core Analytics & Engines)
The mathematical and logical heart of the system.
- **`analytics/`**: High-performance data aggregation, filtering, and K-Means clustering algorithms.
- **`database/`**: Data Access Layer (DAL) handling connections and queries to PostgreSQL via SQLAlchemy.
- **`diagnostics/`**: Real-time security auditing and code health monitoring.
- **`physics.py`**: A dedicated Digital Twin physics engine that calculates power grid losses, resistance changes, and weather impacts.

### 3. `ml/` (Machine Learning Pipeline)
Dedicated subsystem for time-series forecasting and predictive analytics.
- Implements both Statistical models (ARIMA) and Deep Learning models (LSTM).
- Contains automated training pipelines, metrics engines, and model serialization (`ONNX`/`H5`).
- Includes the `models/` directory where production-ready weights and scalers are stored.

### 4. `services/` (Business Logic & Simulation)
Background services and business logic execution.
- **Data Mining**: Advanced trend analysis and anomaly detection.
- **Data Generator**: A telemetry simulator that mimics real-world power grid behavior for stress-testing.
- **Migrations**: Database seeding and schema migration services.

### 5. `ui/` (User Interface)
The frontend layer built on Streamlit, organized for maximum reusability.
- **`components/`**: Reusable UI widgets (cards, interactive Plotly charts).
- **`segments/`**: Larger structural blocks (Sidebars, Dashboards, Live KPI grids).
- **`views/`**: Full-page layouts (Map View, Finance, Generation, Advanced Analytics).

### 6. `utils/` (System Utilities)
- High-performance caching managers (`cache_manager.py`).
- Universal error handlers and system validators.
- Unified logging configuration (`logging_config.py`).

## 🚀 Technologies Used
- **Language**: Python 3.10+ (Strict typing enforced)
- **Machine Learning**: TensorFlow / Keras, Scikit-Learn, Statsmodels
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Streamlit
- **Database**: PostgreSQL, SQLAlchemy, Psycopg2
