# 🚀 DEPLOYMENT GUIDE — Energy Monitor ULTIMATE

> **Live:** [energymonitor-olap.onrender.com](https://energymonitor-olap.onrender.com/)  
> Версія: 3.0 GOLD · Python 3.13 · Docker · Render.com

---

## 📋 Зміст

1. [Локальний запуск](#-локальний-запуск)
2. [Деплой на Render.com](#-деплой-на-rendercom)
3. [CI/CD Pipeline](#-cicd-pipeline)
4. [Docker](#-docker)
5. [Release Checklist](#-release-checklist)
6. [Troubleshooting](#-troubleshooting)
7. [Моніторинг](#-моніторинг)
8. [Безпека](#-безпека)

---

## 💻 Локальний запуск

### Швидкий старт

```bash
# 1. Клонувати репозиторій
git clone https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP.git
cd EnergyMonitor-OLAP

# 2. Створити та активувати venv
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 3. Встановити залежності
pip install -r requirements.txt

# 4. Налаштувати середовище
cp .env.example .env
# Відредагувати .env своїми DB credentials

# 5. Запустити тести
pytest tests/ -v

# 6. Запустити дашборд
python -m streamlit run main.py
```

Дашборд буде доступний на `http://localhost:8501`

### Змінні середовища (.env)

```env
# База даних (Neon Cloud PostgreSQL)
DB_NAME=neondb
DB_USER=<your_neon_user>
DB_PASSWORD=<your_neon_password>
DB_HOST=<your_cluster>.c-2.eu-central-1.aws.neon.tech
DB_PORT=5432
DB_SSL=require

# Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=info
```

> [!CAUTION]
> Ніколи не комітьте `.env` у репозиторій. Він вже в `.gitignore`.

---

## 🌐 Деплой на Render.com

### Попередні вимоги

- GitHub акаунт підключений до Render
- Neon Cloud DatabaseURL готовий
- `requirements.txt` актуальний

### Крок 1: Підготувати репозиторій

```bash
# Переконатися, що всі зміни закомічені
git status

# Запустити тести перед деплоєм
pytest tests/ -v  # Має бути 74 passed, 0 failed

# Відправити в main
git push origin main
```

### Крок 2: Підключити до Render

1. Зайти на [render.com](https://render.com)
2. Натиснути **"New +"** → **"Web Service"**
3. Підключити GitHub репозиторій
4. Вибрати гілку `main`

### Крок 3: Налаштувати сервіс

| Параметр | Значення |
|----------|----------|
| **Name** | `energy-monitor` |
| **Environment** | `Docker` |
| **Region** | `Frankfurt (EU Central)` |
| **Branch** | `main` |
| **Plan** | Free або Starter |

### Крок 4: Встановити змінні середовища

У вкладці **"Environment"** додати:

```
DB_NAME=neondb
DB_USER=<your_neon_user>
DB_PASSWORD=<your_neon_password>
DB_HOST=<your_cluster>.c-2.eu-central-1.aws.neon.tech
DB_PORT=5432
DB_SSL=require
STREAMLIT_SERVER_PORT=10000
STREAMLIT_LOGGER_LEVEL=info
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
OMP_NUM_THREADS=1
```

> [!WARNING]
> `OPENBLAS_NUM_THREADS=1` обов'язковий — без нього Render падає через Memory Spike від NumPy.

### Крок 5: Деплой

1. Натиснути **"Create Web Service"**
2. Очікувати 5-10 хвилин (перший білд)
3. Слідкувати за логами білду
4. Додаток доступний: `https://energy-monitor.onrender.com`

### Пост-деплой чеклист

```
✅ Додаток доступний за URL
✅ База даних підключена (перевірити в логах)
✅ Логи без помилок
✅ Health check відповідає: GET /_stcore/health
✅ UI завантажується і відображає дані
✅ Немає hardcoded секретів у логах
```

---

## ⚙️ CI/CD Pipeline

Налаштований через **GitHub Actions** (`.github/workflows/ci-cd.yml`).

### Автоматичний флоу

```
git push origin main
       │
       ▼
  🧹 Lint (flake8 + pylint)
       │
       ▼
  🔍 Type Check (mypy)
       │
       ▼
  🧪 Tests (pytest — 74 тести)
       │
       ▼
  🛡️ Security (bandit + detect-secrets)
       │
       ▼
  🐳 Docker Build & Push
       │
       ▼
  🚀 Deploy → Render.com
```

### Ручний деплой (без CI/CD)

```bash
# Option 1: Автоматично через git push
git push origin main
# Render auto-deploys!

# Option 2: Вручну через Render Dashboard
# Dashboard → Select service → "Deploy" button
```

### GitHub Secrets (необхідні для CI/CD)

| Secret | Де взяти |
|--------|----------|
| `DOCKER_USERNAME` | Docker Hub профіль |
| `DOCKER_PASSWORD` | Docker Hub access token |
| `RENDER_DEPLOY_HOOK` | Render → Settings → Deploy Hook |

---

## 🐳 Docker

### Локальний запуск в Docker

```bash
# Зібрати образ
docker build -t energy-monitor:latest .

# Запустити (з .env файлом)
docker run -p 10000:10000 --env-file .env energy-monitor:latest

# Дашборд доступний на http://localhost:10000
```

### Push на Docker Hub

```bash
# Логін
docker login

# Зібрати та тегнути
docker build -t yourusername/energy-monitor:latest .
docker tag yourusername/energy-monitor:latest yourusername/energy-monitor:v3.0

# Відправити
docker push yourusername/energy-monitor:latest
docker push yourusername/energy-monitor:v3.0
```

### Деплой з Docker Hub на Render

1. Create new Web Service
2. Select **"Deploy existing image from registry"**
3. Image URL: `docker.io/yourusername/energy-monitor:latest`
4. Додати environment variables (Крок 4 вище)

---

## 📋 Release Checklist

Перед деплоєм в production:

```bash
# 1. Запустити всі тести
pytest tests/ -v
# Очікуваний результат: 74 passed, 0 failed

# 2. Перевірити лінтінг
flake8 src/ core/ ml/ ui/ --max-line-length=127

# 3. Перевірити типізацію
mypy src/ core/ ml/ --ignore-missing-imports

# 4. Перевірити форматування
black --check src/ core/ ml/ ui/ --line-length=120

# 5. Security scan
pip-audit
bandit -r src/ core/ ml/ -f text
```

**Перед кожним релізом:**

- [ ] Всі тести проходять (`74 passed, 0 failed`)
- [ ] Лінтінг без критичних помилок
- [ ] Немає hardcoded секретів
- [ ] `.env` значення оновлені в Render UI
- [ ] `requirements.txt` актуальний
- [ ] Зроблено бекап БД (для важливих змін схеми)
- [ ] `PROJECT_STATUS.md` оновлено

---

## 🚨 Troubleshooting

### ❌ Додаток не стартує на Render

**Симптом:** Логи показують помилку при запуску.

```bash
# Перевірити локально
python -m streamlit run main.py

# Перевірити логи
Get-Content logs/energy-monitor.log -Tail 50  # Windows
```

**Часті причини:**

| Помилка | Рішення |
|---------|---------|
| `ModuleNotFoundError` | Додати пакет у `requirements.txt` |
| `Connection refused` | Перевірити DB env variables у Render |
| `Memory Spike / OOM` | Переконатись, що `OPENBLAS_NUM_THREADS=1` встановлено |
| `TypeError: 'str' cannot be interpreted as integer` | Перевірити `use_container_width` у Streamlit компонентах |
| `ImportError: cannot import name X` | Перевірити синтаксис файлу на `IndentationError` |

### ❌ Проблема з базою даних

```python
# Швидкий тест підключення
import psycopg2, os
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    sslmode="require"
)
print("✅ Connected!")
conn.close()
```

### ❌ Memory issues (Render Free tier: 512 MB)

```bash
# У .env або Render Environment:
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
OMP_NUM_THREADS=1

# У коді вже є Auto-GC watchdog:
# auto_gc(threshold_mb=380) у main.py
```

### ❌ Кеш переповнений

```bash
# Запустити TTL-очищення вручну (видалить JSON старші 0 год)
python -c "from utils.cache_manager import clean_cache; print(clean_cache(ttl_hours=0))"

# Або при наступному запуску очищення відбудеться автоматично (TTL=24h)
```

---

## 📊 Моніторинг

### Health Check

```bash
# Автоматичний (Render перевіряє автоматично)
GET https://energymonitor-olap.onrender.com/_stcore/health

# Ручна перевірка
curl -I https://energymonitor-olap.onrender.com/_stcore/health
```

### Метрики Render Dashboard

Render Dashboard → Select service → **Metrics**:
- CPU usage
- Memory usage (FREE: 512MB limit)
- Network I/O
- Restart events

### Логи

```bash
# Локально (Windows)
Get-Content logs/energy-monitor.log -Tail 100 -Wait

# Render Dashboard
Settings → Logs → Live tail
```

### Автодіагностика

```bash
# Запустити вбудований аудит
python diagnose.py
# Очікуваний результат: 100/100 ✅
```

---

## 🔒 Безпека

### ✅ Що зроблено

| Захист | Реалізація |
|--------|------------|
| SQL Injection | Параметризовані запити + `utils/validators.py` |
| Секрети | `.env` + GitHub Secrets + Render Environment UI |
| Секрети в коді | `detect-secrets` у CI pipeline |
| Вразливий код | Bandit SAST у CI pipeline |
| Credentials у логах | Redacted logger у `utils/logging_config.py` |
| SSL/TLS | `DB_SSL=require` для Neon |

### ✅ DO

```
✅ Зберігай секрети ТІЛЬКИ в Render Environment UI
✅ Використовуй .env.example як шаблон (без реальних значень)
✅ Регулярно оновлюй залежності (pip-audit)
✅ Встановлюй STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false у prod
✅ Слідкуй за логами на підозрілу активність
```

### ❌ DON'T

```
❌ Не комітьте .env файл (він є в .gitignore)
❌ Не хардкодьте паролі в коді
❌ Не публікуйте DB URL у логах або README
❌ Не деплойте без проходження тестів
```

---

## 📈 Масштабування

### Vertical Scaling (більше ресурсів)

1. Render Dashboard → Select app
2. Settings → Instance Type
3. Вибрати: **Starter** (512MB+) / **Standard** (2GB)

### Horizontal Scaling (майбутнє — Phase 7)

- Redis cache для historical даних
- SQL-індекси на `LoadMeasurements.timestamp`
- Async підтримка (після Phase 7 з ROADMAP)

---

## 📞 Корисні посилання

| Ресурс | URL |
|--------|-----|
| Live Demo | [energymonitor-olap.onrender.com](https://energymonitor-olap.onrender.com/) |
| GitHub | [github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP) |
| Neon Docs | [neon.tech/docs](https://neon.tech/docs) |
| Render Docs | [render.com/docs](https://render.com/docs) |
| Streamlit Docs | [docs.streamlit.io](https://docs.streamlit.io) |
| Docker Docs | [docs.docker.com](https://docs.docker.com) |

---

> [!TIP]
> Відчуваєш проблему? Запусти `python diagnose.py` — він перевірить 20+ параметрів і підкаже, де саме збій.

**Happy deploying! 🚀✨**
