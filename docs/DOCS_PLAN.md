# 📊 План документації (DOCS_PLAN)

Цей документ є навігаційною картою всієї документації проекту **Energy Monitor ULTIMATE**. Він пов'язує програмні модулі з розділами технічного опису та дипломної роботи.

---

## 🗺️ Карта документації

| Документ | Цільова аудиторія | Пов'язані модулі коду | Розділ диплому |
| :--- | :--- | :--- | :--- |
| **[README.md](index.md)** | Всі користувачі | Весь проект | Вступ, 4.1 |
| **[ARCHITECTURE.md](system/architecture.md)** | Архітектори, RE | `core/`, `app/`, `ui/segments/` | 2.1, 2.2, 5.2 |
| **[ML Pipeline](ml/index.md)** | Data Scientists | `ml/`, `ml/vectorizer.py` | 1.4, Розділ 3 |
| **[Digital Twin](system/digital_twin.md)** | Інженери, DevOps | `src/services/sensors_db.py`, `src/core/physics.py` | 2.3, 4.2 |
| **[Database](system/database.md)** | DBA, Backend | `src/core/database.py`, `utils/validators.py` | 2.4, 4.4 |
| **[Security Audit](guides/SECURITY.md)** | Security Auditor | `tests/test_security.py` | 4.4 |
| **[Testing](guides/TESTING_GUIDE.md)** | QA, розробники | `tests/`, `test_security.py`, `diagnose.py` | 5.1 |
| **[User Manual](guides/USER_MANUAL.md)** | Кінцеві користувачі | `ui/views/`, `ui/segments/dashboard.py` | 5.2 |
| **[Maintenance](guides/MAINTENANCE.md)** | DevOps, Admin | `utils/cache_manager.py`, `utils/memory_helper.py` | 4.4 |
| **[Glossary & FAQ](GLOSSARY.md)** | Всі (особливо комісія) | Всі модулі | Вступ, 7.3 |
| **[Development](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/DEVELOPMENT.md)** | Розробники | Весь проект | — |

---

## 🏗️ Деталізація за рівнями

### Рівень 1: Огляд проекту (High-Level)
*   **README.md**: Швидкий старт, опис стеку та результатів.
*   **PROJECT_STATUS.md**: Актуальний стан розробки та проходження тестів.

### Рівень 2: Технічний дизайн (Technical Design)
*   **architecture.md**: Опис 4-шарової архітектури, потоки даних, діаграми Mermaid.
*   **database.md**: Схема БД (ER-діаграма), OLAP-запити, індекси.
*   **ml/index.md**: Опис ознак v3, LSTM архітектури, метрик RMSE/MAE та статистичного аудиту.

### Рівень 3: Експлуатація та підтримка (Operational)
*   **DEPLOYMENT.md**: Інструкція з деплою на Render.com з урахуванням специфіки (thread limits).
*   **USER_MANUAL.md**: Гід по інтерфейсу, інтерпретація графіків та управління симуляцією.
*   **docs/guides/MAINTENANCE.md**: Робота з логами, очищення кешу, моніторинг ресурсів.

### Рівень 4: Валідація та безпека (Quality Assurance)
*   **testing.md**: Покриття 79 тестами, методологія тестування фізики та безпеки.
*   **Security Details**: Опис захисту від SQLi, XSS та управління секретами.

---

## 🎓 Зв'язок із Дипломною роботою

| Розділ Диплому | Першоджерело в документації | Ключові дані для копіювання |
| :--- | :--- | :--- |
| **Розділ 1** | `docs/ml/index.md` | Аналіз існуючих методів прогнозування |
| **Розділ 2** | `docs/system/architecture.md`, `docs/system/database.md` | Діаграми класів, ER-діаграма, опис шарів |
| **Розділ 3** | `docs/ml/index.md` | Графіки навчання LSTM, опис 9 ознак (вектор ознак) |
| **Розділ 4** | `docs/system/digital_twin.md`, `docs/guides/MAINTENANCE.md` | Алгоритм Digital Twin, опис стеку технологій |
| **Розділ 5** | `docs/guides/TESTING_GUIDE.md`, `docs/guides/USER_MANUAL.md` | Результати 79 тестів, скріншоти інтерфейсу |

---

## 📈 План росту документації (Roadmap)

1.  **Phase 4.1 (Поточна)**: Завершення User Manual та Maintenance Guide.
2.  **Phase 5 (Типізація)**: Оновлення докстрінгів для 100% покриття `mypy`.
3.  **Phase 6 (Scientific)**: Додавання академічних описів математичних моделей у `docs/system/architecture.md`.
