[🇺🇸 English](README.md) | [🇺🇦 Українська](README.uk.md)

---

# 🧪 Testing Suite (`tests/`)

Quality assurance is paramount. This directory houses a comprehensive suite of automated tests built using the `pytest` framework. These tests ensure the reliability, accuracy, and security of the EnergyMonitor-OLAP platform.

## 🎯 Test Categories

### 1. `test_database.py` (Integration Tests)
Validates the Data Access Layer. Ensures robust connections to PostgreSQL, verifies CRUD operations, and tests transaction rollbacks under failure conditions.

### 2. `test_core_analytics.py` (Unit Tests)
Tests the mathematical correctness of data aggregation, filtering mechanisms, and the K-Means clustering engine used for anomaly detection.

### 3. `test_ml_model.py` (ML Pipeline Validation)
Does not train models (to save time), but verifies that pre-trained weights (`.h5` / `.onnx`) load correctly, scalers function as expected, and the model inference outputs valid tensor shapes.

### 4. `test_physics.py` (Domain Logic Tests)
Strict unit tests for the Digital Twin physics engine. Validates the thermodynamic formulas, power loss calculations, and resistance-temperature dependencies.

### 5. `test_security.py` (Security Audits)
Tests the system's resilience against common vulnerabilities, ensuring all SQL queries are parameterized (preventing SQL Injection) and inputs are properly sanitized.

---

## 🚀 How to Run

To execute the entire test suite, ensure your virtual environment is activated and run:

```bash
pytest tests/ -v
```

For testing specific components:
```bash
pytest tests/test_physics.py -v
```
