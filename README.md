# ⚡ Energy Monitor Ultimate (Digital Twin Platform)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM-orange)

Інтелектуальна аналітична система класу **Digital Twin (Цифровий Двійник)** для моніторингу, діагностики та прогнозування навантаження на енергосистеми в режимі реального часу.

---

## 📸 Огляд функціоналу

### 1. 🏥 Оперативний моніторинг (Live Telemetry)
Автономне опитування віртуальних датчиків кожні 5 секунд. Система відображає:
* Здоров'я мережі (AI Health Score).
* Частоту системи ($f$).
* Напругу ($U$) та струми навантаження ($I$).

### 2. 🔮 ШІ-Прогнозування (LSTM)
Прогнозування споживання на 24 години наперед за допомогою трьох архітектур нейромереж:
* **V1 (Базова)** — Тільки історія МВт.
* **V2 (Мультимодальна)** — Враховує температуру та технічний стан.
* **V3 (Advanced)** — Враховує часові ознаки (Hour/Dayofweek).

### 3. 📊 Аналіз втрат та Кластеризація (KMeans)
* Сегментація підстанцій на рівні ризику (🔴 Високе, 🟡 Штатне, 🟢 Низьке навантаження).
* Розрахунок фізичних втрат потужності для ліній змінного струму (**AC**) та постійного струму високої напруги (**HVDC**).

---

## 🏛️ Архітектура рішення

Проєкт побудовано за принципами **SOLID** та **Layered Architecture** (Багатошарова архітектура):

```text
📦 Test/Py
 ┣ 📂 app                     # Додаткові системні файли
 ┃ ┗ 📜 config.py             # Системний config (відключає логи, порти тощо)
 ┃
 ┣ 📂 core                    # БІЗНЕС-ЛОГІКА (Domain Layer)
 ┃ ┣ 📂 database              # SQL, сесії, connection pool
 ┃ ┣ 📂 analytics             # Математичні розрахунки для відображення
 ┃ ┃ ┣ 📜 aggregator.py       # Всі `.resample()`, `.sum()` винесені сюди
 ┃ ┃ ┣ 📜 clustering.py       # Логіка KMeans та аналітики
 ┃ ┃ ┗ 📜 physics.py          # Розрахунок втрат AC/DC
 ┃ ┗ 📂 data_loaders          # KaggleLoader, Репозиторії даних
 ┃
 ┣ 📂 ui                      # ПРЕДСТАВЛЕННЯ (Presentation Layer)
 ┃ ┣ 📂 components            # Дрібні атомні компоненти (Atomics)
 ┃ ┃ ┣ 📜 cards.py            # render_gauge, make_health_bar
 ┃ ┃ ┣ 📜 charts.py           # px.line, px.bar wrappers
 ┃ ┃ ┗ 📜 styles.py           # CSS утиліти
 ┃ ┣ 📂 segments              # Панелі (Sidebar, Header, Navigation)
 ┃ ┗ 📂 views                 # Модулі відображення (Колишні tabs/)
 ┃
 ┣ 📂 ml                      # Моделі машинного навчання (LSTM, Predictors)
 ┗ 📜 main.py                 # Router (Ініціалізація та виклик views)
```

---

## 🚀 Як запустити проект

Для запуску вам знадобиться встановлений **Python 3.9+**.

1. **Клонуйте репозиторій:**
   ```bash
   git clone https://github.com/Lutvunenko-Dmutro/my-telegram-bot.git
   cd my-telegram-bot
   ```

2.  **Встановіть залежності:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Запустіть фоновий генератор датчиків:**
    ```bash
    python -m src.services.data_generator
    ```

4.  **Запустіть панель моніторингу:**
    ```bash
    python -m streamlit run main.py
    ```

---

## 🛠 Технологічний стек

  * **Backend**: Python 3.9+
  * **Frontend Panel**: Streamlit, Plotly (Dynamic charts)
  * **Database Layer**: Memory Sync DB / SQLite
  * **Machine Learning**: TensorFlow (Keras LSTM), Scikit-Learn (KMeans)
  * **Data Processing**: Pandas, NumPy

---

### 👨‍💻 Автор
**Литвиненко Дмитро**  
Дипломний проєкт розробки інтелектуальних систем моніторингу енергомереж.
