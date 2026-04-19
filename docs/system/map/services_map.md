# 🏭 Мапа Сервісів (Services & Simulation)

Цей розділ описує систему симуляції реального часу та фонові служби.

## 📂 Симуляція Цифрового Двійника (`src/services/simulation/`)

### 📄 [data_generator.py](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/src/services/simulation/data_generator.py)
**Навіщо:** Головний двигун «цифрового двійника».
- **Як працює:** У нескінченному циклі імітує роботу підстанцій, розраховуючи навантаження на основі фізики (`calculate_substation_load`).
- **Чому так:** Дозволяє системі мати «живі» дані для демонстрації, навіть якщо реальні датчики відключені.

### 📄 [sensors.py](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/src/services/simulation/sensors.py)
**Навіщо:** Імітація датчиків стану обладнання.
- **Роль:** Генерує показники температури обмоток трансформаторів та вмісту водню (H2 ppm) в маслі.

---

## 📂 Аналітика та Майнінг (`src/services/analysis/`)

### 📄 [trends_and_patterns.py](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/src/services/analysis/trends_and_patterns.py)
**Навіщо:** Глибокий аналіз історичних даних.
- **Роль:** Шукає аномалії та закономірності в споживанні, які не помітні на звичайних графіках.
