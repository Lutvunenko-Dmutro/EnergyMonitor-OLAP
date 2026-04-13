# 🚀 ІНСТРУКЦІЯ З РОЗГОРТАННЯ — Energy Monitor ULTIMATE

> **Наживо:** [energymonitor-olap.onrender.com](https://energymonitor-olap.onrender.com/)  
> Версія: 3.1 STABLE · Python 3.13 · Docker · Render.com

---

## 📋 Зміст

1. [Локальний запуск](#-локальний-запуск)
2. [Розгортання на Render.com](#-розгортання-на-rendercom)
3. [CI/CD Конвеєр](#-cicd-конвеєр)
4. [Контейнеризація (Docker)](#-docker)
5. [Чеклист перед релізом](#-release-checklist)
6. [Усунення несправностей (Troubleshooting)](#-troubleshooting)
7. [Моніторинг](#-моніторинг)
8. [Безпека](#-безпека)

---

## 💻 Локальний запуск

### Швидкий старт

```bash
# 1. Клонувати репозиторій
git clone https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP.git
cd EnergyMonitor-OLAP

# 2. Створити та активувати віртуальне середовище
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 3. Встановити залежності
pip install -r requirements.txt

# 4. Налаштувати змінні оточення
cp .env.example .env
# Відредагувати .env — вставити дані доступу до вашої БД

# 5. Запустити автоматичні тести
pytest tests/ -v

# 6. Запустити дашборд
python -m streamlit run main.py
```

Дашборд буде доступний за адресою: `http://localhost:8501`

### Змінні оточення (.env)

```env
# База даних (Neon Cloud PostgreSQL)
DB_NAME=neondb
DB_USER=<ваш_користувач_neon>
DB_PASSWORD=<ваш_пароль_neon>
DB_HOST=<ваш_кластер>.c-2.eu-central-1.aws.neon.tech
DB_PORT=5432
DB_SSL=require

# Налаштування Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=info
```

> [!CAUTION]
> Ніколи не додавайте файл `.env` у репозиторій Git. Він уже доданий до `.gitignore` для вашої безпеки.

---

## 🌐 Розгортання на Render.com

### Попередні вимоги

- Акаунт GitHub, підключений до [Render.com](https://render.com)
- База даних у Neon Cloud (URL підключення готовий)
- Файл `requirements.txt` містить усі необхідні бібліотеки

### Крок 1: Підготувати репозиторій

```bash
# Переконатися, що всі зміни закомічені
git status

# Обов'язково запустити тести перед деплоєм
pytest tests/ -v  # Результат має бути: 74 passed, 0 failed

# Відправити зміни в гілку main
git push origin main
```

### Крок 2: Створення сервісу на Render

1. Зайдіть у панель управління [Render](https://dashboard.render.com).
2. Натисніть **"New +"** → **"Web Service"**.
3. Підключіть ваш GitHub репозиторій.
4. Виберіть гілку `main`.

### Крок 3: Налаштування характеристик

| Параметр | Значення |
| :--- | :--- |
| **Name** | `energy-monitor` |
| **Environment** | `Docker` |
| **Region** | `Frankfurt (EU Central)` |
| **Branch** | `main` |
| **Plan** | Free (або Starter для більшої RAM) |

### Крок 4: Встановлення змінних середовища

У вкладці **"Environment"** додайте такі змінні (копіюючи значення з вашого `.env`):

```env
DB_NAME=neondb
DB_USER=<ваш_користувач_neon>
DB_PASSWORD=<ваш_пароль_neon>
DB_HOST=<ваш_хост_neon>
DB_PORT=5432
DB_SSL=require
STREAMLIT_SERVER_PORT=10000
STREAMLIT_LOGGER_LEVEL=info
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
OMP_NUM_THREADS=1
```

> [!WARNING]
> Змінна `OPENBLAS_NUM_THREADS=1` є критично важливою. Без неї Render може зупинити сервіс через різкий сплеск використання пам'яті бібліотекою NumPy.

### Крок 5: Запуск деплою

1. Натисніть **"Create Web Service"**.
2. Перший білд триває 5-10 хвилин (збірка Docker-образу).
3. Після успішного завершення додаток буде доступний за посиланням: `https://energy-monitor.onrender.com`

---

## ⚙️ CI/CD Конвеєр

Автоматизація налаштована через **GitHub Actions** (`.github/workflows/ci-cd.yml`).

### Процес автоматизації

При кожному `git push origin main` відбувається наступне:
1. **Linting**: Перевірка стилю коду (flake8 + pylint).
2. **Type Check**: Перевірка типізації (mypy).
3. **Tests**: Запуск 74 тестів (pytest).
4. **Security**: Сканування на вразливості та витік секретів.
5. **Docker Build**: Збірка контейнера та його відправка на Docker Hub.
6. **Deploy**: Автоматичне оновлення сервісу на Render.com.

---

## 🐳 Контейнеризація (Docker)

### Локальна збірка та запуск

```bash
# Зібрати образ
docker build -t energy-monitor:latest .

# Запустити (підставивши ваш файл .env)
docker run -p 10000:10000 --env-file .env energy-monitor:latest
```

Проєкт буде доступний за адресою: `http://localhost:10000`

---

## 📋 Release Checklist (Чеклист релізу)

Перед кожним деплоєм у "Production":

- [x] Всі 74 тести проходять успішно (`74 passed, 0 failed`).
- [x] Виконано перевірку лінтером (flake8).
- [x] Відсутні захардкоджені секрети або паролі.
- [x] Оновлені змінні оточення в панелі Render.
- [x] Файл `requirements.txt` актуальний.
- [x] `PROJECT_STATUS.md` відображає актуальні метрики.

---

## 🚨 Усунення несправностей (Troubleshooting)

### ❌ Додаток не запускається на Render

**Симптом:** Статус "Deploy failed" або помилка в логах при старті.

**Рішення:**
- Перевірте `requirements.txt`: чи не забули ви додати нову бібліотеку?
- Перевірте змінні оточення (Environment Variables) на Render.
- Переконайтеся, що `OPENBLAS_NUM_THREADS=1` встановлено.

### ❌ Помилка підключення до бази даних

**Рішення:**
- Переконайтеся, що IP-адреси Render дозволені у налаштуваннях Neon Cloud (або встановлено дозволити підключення з усіх IP).
- Перевірте правильність написання `DB_HOST` та пароля.

### ❌ Проблеми з пам'яттю (Out of Memory)

**Рішення:**
- Система вже має вбудований `memory_helper.py`, який очищає RAM при досягненні 380 МБ.
- Встановіть `OMP_NUM_THREADS=1` для обмеження багатопоточності обчислень.

---

## 📊 Моніторинг

### Перевірка стану (Health Check)
Render автоматично перевіряє доступність за посиланням:
`https://energymonitor-olap.onrender.com/_stcore/health`

### Перегляд логів
У панелі Render перейдете до вкладки **"Logs"**. Нас цікавить "Live Tail" для відстеження роботи системи в реальному часі.

---

## 🔒 Безпека

Система Energy Monitor ULTIMATE використовує багаторівневий захист:
- **SSL/TLS**: Усі з'єднання з БД зашифровані (`sslmode=require`).
- **SQL Injection Protection**: Використання параметризованих запитів ORM SQLAlchemy.
- **Secret Isolation**: Паролі ніколи не потрапляють у код — тільки через змінні середовища.
- **Security Scans**: Регулярне сканування Bandit та pip-audit у CI/CD процесі.

---

**Успішного розгортання! 🚀✨**
