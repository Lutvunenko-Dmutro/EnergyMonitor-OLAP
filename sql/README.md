# 🗄️ Database Schemas & Migrations (`sql/`)
**База Даних (Схеми та міграції)**

This directory contains the foundational SQL scripts required to initialize the PostgreSQL database for the EnergyMonitor-OLAP system. 

Містить SQL скрипти для ініціалізації та початкового налаштування структури бази даних PostgreSQL.

---

## 📜 Script Execution Order / Порядок виконання

### 1. `01_create_schema.sql` (Data Definition Language)
Defines the core relational structure of the system.
*Створює структуру таблиць, індекси та зв'язки.*
- **Substations (`substations`)**: Core grid nodes.
- **Telemetry (`substation_data`)**: High-frequency time-series data storage (Voltage, Current, Power, Weather conditions).
- **Alerts & Logs**: System health monitoring tables.
- Implements hyper-optimized indexing for fast OLAP (Online Analytical Processing) queries on time-series data.

### 2. `02_insert_static_data.sql` (Data Manipulation Language)
Populates the database with essential initial configurations.
*Заповнює довідники та початкові статичні дані.*
- Seeds the system with the primary Ukrainian substations (e.g., "ПС Київська-Центральна").
- Establishes baseline geographical and physical parameters required by the `physics.py` simulation engine.

---

## ⚙️ Automated Migration
You do not need to run these scripts manually. The application includes a self-healing initialization routine. When the system starts, `src/services/data/migrate_db.py` will automatically execute these scripts if it detects a fresh database instance.

*Вам не потрібно запускати ці скрипти вручну. Сервіс міграцій автоматично застосує їх під час першого запуску системи, якщо база даних порожня.*
