# 🎨 Мапа Інтерфейсу (UI & Dashboards)

Цей розділ описує, як система візуалізує дані для користувача через Streamlit.

## 📂 Головний Дашборд (`src/ui/segments/`)

### 📄 [dashboard.py](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/src/ui/segments/dashboard.py)
**Навіщо:** Центр керування всіма вкладками сайту.
- **Як працює:** Використовує **Streamlit Fragments** (`@st.fragment`) для незалежного оновлення частин сторінки.
- **Чому так:** Це дозволяє оновлювати «Живу карту» та «Аварійні сповіщення» кожні кілька секунд без перезавантаження всього сайту.

---

## 📂 Сторінки та Вкладки (`src/ui/views/`)

### 📄 [forecast.py](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/src/ui/views/forecast.py)
**Навіщо:** Сторінка ШІ-прогнозування.
- **Роль:** Поєднує дані з БД та виклики нейромережі з `src/ml/predict_v2.py`.

### 📄 [map.py](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/src/ui/views/map.py)
**Навіщо:** Візуалізація енергомережі на карті України.
- **Роль:** Малює підстанції та лінії передач, змінюючи їх колір залежно від навантаження.

---

## 📂 Графіки та Стилі (`src/ui/components/`)

**Навіщо:** Забезпечує єдиний візуальний стиль (Glassmorphism) та інтерактивні графіки Plotly/Altair.
- **[styles.py](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/src/ui/components/styles.py)**: Додає кастомний CSS для темної теми та ефектів наведення.
