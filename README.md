<p align="right">
  <a href="README.md"><img src="https://flagcdn.com/24x18/us.png" alt="English"> English</a> |
  <a href="README.uk.md"><img src="https://flagcdn.com/24x18/ua.png" alt="Українська"> Українська</a>
</p>

---

# ⚡ Energy Monitor Ultimate (v3.1 STABLE)

<p align="left">
  <a href="https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/actions"><img src="https://img.shields.io/badge/Build-passing-brightgreen?style=for-the-badge&logo=github-actions" alt="Build Status"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="#-testing-and-quality-assurance-qa"><img src="https://img.shields.io/badge/Tests-94%20Passed-success?style=for-the-badge&logo=pytest" alt="Tests"></a>
  <a href="#-mathematical-forecasting-model"><img src="https://img.shields.io/badge/Accuracy-MAPE%203.08%25-orange?style=for-the-badge&logo=target" alt="Accuracy"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"></a>
</p>

**An intelligent analytics and predictive modeling system for power grid loads, based on the Digital Twin concept and LSTM recurrent neural networks.**

🚀 **Live Production (MaaS/SaaS):** [energymonitor-olap.onrender.com](https://energymonitor-olap.onrender.com/)  
📖 **Live Documentation (ProperDocs):** [lutvunenko-dmutro.github.io/EnergyMonitor-OLAP](https://lutvunenko-dmutro.github.io/EnergyMonitor-OLAP/)

### 📂 System Documentation

*   📊 [**PROJECT_STATUS.md**](docs/PROJECT_STATUS.md) — Current system state (94 tests / 0 skipped / 0 failed).
*   🏗️ [**ARCHITECTURE.md**](docs/system/architecture.md) — Architectural schema and layer descriptions.
*   📚 [**ProperDocs Defense Edition**](https://lutvunenko-dmutro.github.io/EnergyMonitor-OLAP/) — Official documentation website (includes Glossary, API Reference, and 3D-Atlas).
*   🗺️ [**ATLAS MASTER INDEX (Live)**](https://lutvunenko-dmutro.github.io/EnergyMonitor-OLAP/system/map/ATLAS_MASTER_INDEX/) — Full interactive registry of all 170+ system passports.
*   📜 [**PROJECT_HISTORY.md**](docs/PROJECT_HISTORY.md) — Complete development timeline (from lab prototype to analytics complex).

---

## 📌 Quick Navigation

* 💻 [**Deployment Guide**](#-deployment-guide) — How to run locally.
* 🧮 [**Mathematical Model**](#-mathematical-forecasting-model) — Formalization of LSTM and feature engineering.
* 💻 [**Tech Stack**](#️-tech-stack) — Tools and architectural justification.
* 🖼️ [**Interface Gallery**](#️-interface-gallery-energy-core) — Interactive overview of system screens.
* 📊 [**Schemas & Diagrams**](#-visual-models-and-diagrams-mermaid) — UML and system architecture.
* 🧪 [**Testing & QA**](#-testing-and-quality-assurance-qa) — Validation of physics and resilience.

---

## 👤 Author

**Lutvunenko Dmutro**  
*Software Developer, Machine Learning Engineer*

---

## 🛠️ Key Features & Automation

To ensure high reliability and rapid development, the following tools were implemented:

*   🚀 **Modular Converter System** — scalable architecture for MD -> DOCX conversion (built-in report generator).
*   🧠 **Smart City Predictive Core** — hybrid modeling combining stochastic forecasting (LSTM networks) with deterministic grid physics models (power loss calculation, thermal degradation).
*   📘 **ProperDocs Defense System** — automated static documentation site generation via MkDocs with auto-build API support (`mkdocstrings`) and interactive Mermaid graphs.
*   🗺️ **Atlas Auto-Mapper** — dynamic source code scanning to maintain a registry of 170+ module "passports".

---

## 🧮 Mathematical Forecasting Model

The mathematical apparatus of the analytical core is based on discrete dynamical systems theory and Deep Learning for multivariate time series.

### 🧬 1. Feature Engineering and Normalization

**Cyclical encoding of periodicity:**  
To eliminate continuity breaks (e.g., $23:59 \rightarrow 00:00$) and preserve seasonality, time features $h \in [0, 23]$ (hour) and $d \in [0, 6]$ (day of week) are mapped to a trigonometric circle:

$$
\text{hour}_{sin}(t) = \sin\left(\frac{2\pi \cdot h(t)}{24}\right), \quad \text{hour}_{cos}(t) = \cos\left(\frac{2\pi \cdot h(t)}{24}\right)
$$

$$
\text{day}_{sin}(t) = \sin\left(\frac{2\pi \cdot d(t)}{7}\right), \quad \text{day}_{cos}(t) = \cos\left(\frac{2\pi \cdot d(t)}{7}\right)
$$

**Feature Normalization ($MinMaxScaler$):**  
Scaling the input space to the $[0, 1]$ range to balance different physical quantities (MW, % health, $\text{ppm}$):

$$
x'_{i,j} = \frac{x_{i,j} - x_{j}^{min}}{x_{j}^{max} - x_{j}^{min}}
$$

### 📦 2. Sliding Window Transformation

For RNN training, the input vector $x_t \in \mathbb{R}^N$ ($N=9$ for v3.1) is transformed into a 3D-tensor $\mathbf{X}_t$ with memory depth $W = 48$ (timesteps):

$$
\mathbf{X}_t = \begin{pmatrix} 
x_{t-W+1} \\ 
x_{t-W+2} \\ 
\vdots \\ 
x_t 
\end{pmatrix} \in \mathbb{R}^{W \times N}
$$

Feature vector:

$$
x_t = [\text{load}, \text{temp}, \text{h2}, \text{health}, \text{air}, \text{h}_{sin}, \text{h}_{cos}, \text{d}_{sin}, \text{d}_{cos}]^T
$$

### 🧠 3. Internal LSTM Cell Architecture

The predictive module is built on LSTM (Long Short-Term Memory) layers. The internal cell dynamics are defined by:

**1. Forget Gate:** Clears outdated information.
$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$

**2. Input Gate & Candidate State:** Forms new incoming information.
$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$
$$\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$$

**3. Cell State UPDATE:** Updates long-term memory.
$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

**4. Output Gate & Hidden State:** Calculates the output signal.
$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$
$$h_t = o_t \odot \tanh(C_t)$$

### 📉 4. Loss Function and Optimization

Minimizes **Huber Loss** ($\delta=1.0$) — an adaptive function acting as MSE for small errors and MAE for large ones (robust to telemetry outliers):

$$
\mathcal{L}_{\delta}(y, \hat{y}) = \begin{cases} \frac{1}{2}(y - \hat{y})^2, & |y - \hat{y}| \leq \delta \\ \delta \cdot |y - \hat{y}| - \frac{1}{2}\delta^2, & |y - \hat{y}| > \delta \end{cases} \rightarrow \min
$$

Weights are updated using the **Adam** algorithm via Backpropagation Through Time (**BPTT**). Forecasting accuracy: achieved a stable **MAPE of 1.5% – 3.1%** on benchmark data.

---

## 👥 User Personas

The analytical system is designed for two key user groups:
*   **👷 Grid Dispatcher:** Uses the dynamic map and alerts service for instant reaction to node overload risks.
*   **📊 Analyst (Energy Engineer):** Uses OLAP slices and predictive charts for power balance planning.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend & Core** | `Python 3.11+`, `SQLAlchemy`, `Psycopg2` |
| **Database (Data)** | `PostgreSQL 15` (Aggregation: `DATE_TRUNC`) |
| **Artificial Intelligence** | `TensorFlow/Keras` (LSTM), `scikit-learn`, `ONNX` |
| **Frontend UI** | `Streamlit 1.37+` (Modular interface) |
| **Visualization** | `Plotly Express`, `Graphviz` |

*Justification*: PostgreSQL (Neon Cloud) is used for fast time-series aggregation. SQLAlchemy ORM implements the Data Access Layer (DAL) pattern for security and flexibility.

---

## 🖼️ Interface Gallery (Energy Core)

<details>
  <summary>🔍 <b>Expand full screenshot gallery (13+ images)</b></summary>
  <br>

  ### 🛰️ 1. System Initialization (Splash Screen)
  Connection node selection screen: local node or Neon cloud cluster.
  ![Initialization](docs/images/boot_1.png)

  ### 📟 2. Energy Core Bootloader
  Authentication process, data integrity verification, and connection to the OLAP layer.
  ![Bootloader](docs/images/boot_loader.png)

  ### 🗺️ 3. GIS Grid Monitoring
  Geographical node visualization and current status (Load Heatmap).
  ![Grid Map](docs/images/map.png)

  ### 📊 4. Consumption Dynamics
  Detailed load analysis by regions and time frames.
  ![Consumption](docs/images/consumption.png)

  ### ⚡ 5. Generation Structure
  Energy balance by source (Nuclear, Hydro, Thermal, Solar, Wind).
  ![Generation](docs/images/generation.png)

  ### ⚠️ 6. Alert Management Center
  Intelligent system for registering and managing critical incidents.
  ![Alerts Log](docs/images/alerts.png)

  ### 💰 7. Financial Analytics
  Generation cost analysis, price heatmaps, and loss characteristics.
  ![Finance](docs/images/finance.png)

  ### 🧠 8. AI Analytics & Clustering
  Substation segmentation by risk level using K-Means.
  ![Clustering](docs/images/clustering.png)

  ### 📈 9. Predictive Modeling (LSTM v3.1)
  Operational 24-hour load forecasting with accuracy auditing.
  ![AI Forecast](docs/images/ai_forecast.png)
  ![Global Grid](docs/images/multi_forecast.png)

  ### 🔬 10. Detailed Audit and Model Verification
  Comprehensive model accuracy testing: streaming analytics (7d backtest), LSTM architecture comparison (v1, v2, v3), and statistical error distribution analysis.
  ![Backtest](docs/images/streaming_analytics.png)
  ![Comparison](docs/images/audit_comparison.png)
  ![Error Distribution](docs/images/error_distribution.png)
  ![Metrics](docs/images/metrics_table.png)

  ### 🌡️ 11. Digital Twin and Physical Monitoring
  Deep asset analysis: thermodynamic balance (weather impact), transformer "health" monitoring via gas concentrations (H2), and cyclic analysis.
  ![Balance](docs/images/weather_impact.png)
  ![Health](docs/images/health_monitoring.png)

  ### 📈 12. Benchmark Testing (Kaggle PJM Interconnection)
  System verification on open US power grid Big Data (PJM). Demonstration of the OLAP core and AI forecasts with gigawatt-scale loads.
  ![Kaggle Forecast](docs/images/kaggle_global_forecast.png)

</details>

---

## 📊 Visual Models and Diagrams (Mermaid)

### 🗺️ 1. UML Components Schema
4-Layer architecture with local and cloud environment separation:

```mermaid
graph TD
    classDef edge fill:#121212,stroke:#ff3366,stroke-width:2px,color:#fff;
    classDef db fill:#0e1726,stroke:#00a4df,stroke-width:2px,color:#fff;
    classDef ml fill:#0b1320,stroke:#ffb703,stroke-width:2px,color:#fff;
    classDef ui fill:#1c1e22,stroke:#00ff88,stroke-width:1px,color:#fff;

    subgraph Local ["💻 LOCAL (Digital Twin)"]
        DG["data_generator.py\n(Simulator)"]:::edge
    end

    subgraph Render ["☁️ CLOUD RENDER (SaaS)"]
        DB[(PostgreSQL\nOLAP Database)]:::db
        subgraph Pipeline ["🧠 AI Pipeline"]
            Vect["vectorizer.py"]:::ml
            Pred["predict_v2.py"]:::ml
        end
        UI["main.py\n(Streamlit Dashboard)"]:::ui
    end

    DG ==>|"PUSH"| DB
    DB <-->|"Query"| Vect
    Vect --> Pred
    Pred --> UI
    DB <--> UI
```

---

## 🧪 Testing and Quality Assurance (QA)

### Test Targets:
* **Digital Twin Fidelity:** Verification of physical laws in `test_physics.py` (e.g., solar power generation at night equals zero).
* **ML Reliability:** Testing LSTM pipeline input/output and data normalization stability.
* **Security Validation:** SQL-injection protection, correct password masking in logs, and date range validation.

**Running Tests:**
```bash
python -m pytest tests/ -v
```
*Current result: 94 passed, 0 skipped — 1.41s ✅*

---

## 📈 Economic Justification (OPEX Savings)

Implementing the system for a hypothetical city of **500,000 population** provides a high economic impact via **Predictive Maintenance (PdM)**.
* **Projected maintenance cost reduction:** **$20\%$** (industry PdM standard).
* **Savings via Health Score:** Prevention of cascading failures.
* **Net annual savings:** $\approx \mathbf{5,500,000}$ **UAH/year**.

---

## 🛡️ Security and Resilience

*   **SQL Injection Protection:** Implemented via SQLAlchemy ORM parameterization and input whitelist validators.
*   **Zero-Failure Fallback:** If AI computations fail, the system automatically falls back to a statistical baseline (ARIMA).
*   **Auto-GC Watchdog:** Automatic memory management for stable operation on cloud hosting.

---

## 💻 Deployment Guide

### 1. Quick Start (Local)
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run main dashboard
streamlit run main.py
```

### 2. Run Developer Dashboard (Control Center)
The project includes a special developer dashboard uniting all scripts (ML training, DB analysis, documentation generation):
```bash
python START_DASHBOARD.py
```

### 3. AI Model Training
Models are pre-trained, but if you wish to retrain them from scratch on your own data:
```bash
python src/ml/train_lstm.py --version v3
```

### 4. Run Local Documentation
```bash
# Generate and run local MkDocs server
properdocs serve
# Open in browser: http://127.0.0.1:8000
```

---

**Happy monitoring! 🚀✨**
