[🇺🇸 English](README.md) | [🇺🇦 Українська](README.uk.md)

---

# 🛠️ System Tools & CI/CD Scripts (`scripts/`)

This directory contains standalone utility scripts, orchestration tools, and machine learning pipelines that support the main application. These scripts are crucial for development, auditing, and maintenance operations.

## 🌟 Key Tools

### 🎛️ 1. Developer Dashboard (`system/dev_dashboard.py`)
A centralized Streamlit-based control panel for developers. Instead of running scripts via CLI, the Dev Dashboard provides an interactive GUI to execute audits, check database health, and run ML benchmarks with rich visual outputs.
*(Launch via `START_DASHBOARD.py` in the project root).*

### 🤖 2. Machine Learning Pipelines (`ml/`)
- **`benchmark_models.py`**: Executes an automated competition between predictive models (e.g., ARIMA vs LSTM) on historical data, generating comparative accuracy graphs and R² metrics.
- **`audit_data.py`**: A deep-dive dataset analyzer that checks for anomalies, missing values, and feature correlations before model training.
- **`real_data_evaluation.py`**: Validates pre-trained models against continuous live/simulated telemetry data.

### 🛡️ 3. Architecture Auditing (`system/`)
- **`diagnose.py`**: Runs a deep code audit searching for security vulnerabilities (e.g., SQL injections), memory leaks, and architectural anti-patterns, generating an interactive HTML health report.
- **`check_db_stats.py`**: Monitors PostgreSQL database health, identifying large tables and tracking query performance.

### 📄 4. Documentation Stewardship
- **`audit_passports.py`**: Validates the integrity of all architectural Markdown documents (ProperDocs).
- **`rebuild_master_index.py`**: Automatically updates navigation links across the documentation system.

---

## ⚙️ How to use
It is highly recommended to run these scripts via the Developer Dashboard:
```bash
python START_DASHBOARD.py
```
