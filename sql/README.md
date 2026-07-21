<p align="right">
  <a href="README.md"><img src="https://flagcdn.com/24x18/us.png" alt="English"> English</a> |
  <a href="README.uk.md"><img src="https://flagcdn.com/24x18/ua.png" alt="Українська"> Українська</a>
</p>

---

# 🗄️ Database Schemas & Migrations (`sql/`)

This directory contains the foundational SQL scripts required to initialize the PostgreSQL database for the EnergyMonitor-OLAP system. 

## 📜 Script Execution Order

### 1. `01_create_schema.sql` (Data Definition Language)
Defines the core relational structure of the system.
- **Substations (`substations`)**: Core grid nodes.
- **Telemetry (`substation_data`)**: High-frequency time-series data storage (Voltage, Current, Power, Weather conditions).
- **Alerts & Logs**: System health monitoring tables.
- Implements hyper-optimized indexing for fast OLAP (Online Analytical Processing) queries on time-series data.

### 2. `02_insert_static_data.sql` (Data Manipulation Language)
Populates the database with essential initial configurations.
- Seeds the system with the primary substations (e.g., "ПС Київська-Центральна").
- Establishes baseline geographical and physical parameters required by the `physics.py` simulation engine.

---

## ⚙️ Automated Migration
You do not need to run these scripts manually. The application includes a self-healing initialization routine. When the system starts, `src/services/data/migrate_db.py` will automatically execute these scripts if it detects a fresh database instance.
