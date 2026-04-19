# ⚡ Energy Monitor ULTIMATE

**Інтелектуальна система OLAP-моніторингу та ШІ-прогнозування навантаження енергетичних мереж**

---

## Про проект

Energy Monitor ULTIMATE — це production-ready SaaS-дашборд для моніторингу та прогнозування навантаження електроенергетичних мереж. Система поєднує:

- 🧠 **LSTM нейронні мережі** (v1/v2/v3) для часового прогнозування
- 🏭 **Digital Twin** — фізична симуляція трансформаторів у реальному часі
- 📊 **OLAP-аналітика** — багатовимірні зрізи споживання по регіонах і підстанціях
- ☁️ **Cloud-native** — PostgreSQL (Neon), Docker, Render.com, GitHub Actions CI/CD

**Live Demo:** [energymonitor-olap.onrender.com](https://energymonitor-olap.onrender.com/)

---

## Структура документації

| Розділ | Зміст |
|--------|-------|
| **[Архітектура](architecture.md)** | Шари системи, модульна структура, діаграми |
| **[ML Pipeline](ml/index.md)** | LSTM, векторизація, бектест, метрики |
| **[API Reference](api/index.md)** | Автодокументація модулів |
| **[Digital Twin](digital_twin.md)** | Фізична симуляція, сенсори, lifecycle |
| **[Database](database.md)** | Схема БД, SQL запити, OLAP |
| **[Testing](testing.md)** | 79 тестів, coverage, стратегія |
| **[Security](security.md)** | SQL injection, секрети, Bandit |
| **[Diploma Plan](DIPLOMA_PLAN.md)** | Структура дипломної роботи |

---

## Швидкий старт

```bash
git clone https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP.git
cd EnergyMonitor-OLAP
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # Заповнити DB credentials
pytest tests/ -v       # 74 passed ✅
python -m streamlit run main.py
```

---

## Технологічний стек

| Компонент | Технологія |
|-----------|------------|
| **Runtime** | Python 3.11+ |
| **AI/ML** | TensorFlow/Keras LSTM + ONNX Runtime |
| **Database** | PostgreSQL 15 (Neon Cloud) |
| **Frontend** | Streamlit 1.37+ |
| **Hosting** | Render.com (Docker) |
| **CI/CD** | GitHub Actions |
| **Cache** | File-based TTL (24h, `utils/cache_manager.py`) |

---

## Метрики проекту

```
🧪 Тести:         74 passed, 0 failed, 5 skipped
⏱️ Час тестів:   13.71s
🔒 Security:      Clean (Bandit + detect-secrets)
💾 Cache:         TTL 24h (auto-cleanup)
🚀 Deploy:        Auto via GitHub Actions → Render.com
```