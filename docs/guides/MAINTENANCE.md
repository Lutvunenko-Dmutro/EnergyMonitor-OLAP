# 🛠️ Технічне обслуговування (Maintenance Guide)

Цей документ призначений для адміністраторів системи та DevOps-інженерів. Він описує механізми стабільності та регламентні роботи.

---

## 💾 Управління кешем (TTL Cache)

Система використовує файловий кеш для прискорення запитів та зменшення навантаження на БД Neon.

*   **Директорія**: `cache/`
*   **Логіка**: `utils/cache_manager.py` автоматично видаляє файли, старші за 24 години.
*   **Захист**: Файли з розширенням `.graphml` (карти мережі) захищені від автоматичного видалення.

**Ручне очищення:**
```bash
python -c "from src.utils.cache_manager import clean_cache; clean_cache(ttl_hours=0)"
```

---

## 🧠 Управління пам'яттю (Memory Watchdog)

Через обмеження Render Free (512MB RAM), у системі працює активний Garbage Collector.

*   **Логіка**: `utils/memory_helper.py`
*   **Поріг спрацювання**: 380MB (налаштовується у `main.py`).
*   **Моніторинг**: Логи за посиланням `Memory usage: XXX MB | Threshold: 380 MB`.

**Як змінити поріг:**
У файлі `main.py`:
```python
auto_gc(threshold_mb=400) # Збільшити до 400MB
```

---

## 🔌 З'єднання з базою даних

Проект використовує `SQLAlchemy` з кастомним обробником `robust_database_handler`.

*   **Retries**: Система робить до 3 спроб підключення при помилках мережі.
*   **SSL**: Режим `require` обов'язковий для Neon Cloud.
*   **Connection Pool**: Налаштований на 10 з'єднань (`pool_size=10`) для запобігання переповненню лімітів безкоштовного тарифу.

---

## 📝 Логування (Logging)

Логи зберігаються у директорії `logs/`.

*   **Головний лог**: `logs/energy-monitor.log`
*   **Рівень логування**: Налаштовується через `STREAMLIT_LOGGER_LEVEL` (по замовчуванню `info`).
*   **Формат**: Rich-форматування для консолі + plain-text для файлу.

**Перегляд помилок у реальному часі (Windows):**
```powershell
Get-Content logs/energy-monitor.log -Wait -Tail 20 | Select-String "ERROR"
```

---

## 🔑 Змінні середовища (env)

| Змінна | Призначення | Рекомендація |
| :--- | :--- | :--- |
| `DB_NAME` | Ім'я БД | `neondb` |
| `OPENBLAS_NUM_THREADS` | Ліміт потоків NumPy | `1` (Критично для Render!) |
| `STREAMLIT_SERVER_PORT` | Порт | `10000` (для Render) |
| `AUTO_CLEAN_CACHE` | Авто-очищення | `True` |

---

## 🚨 План дій при збої

1.  **Application Error (500)**: Перевірити `logs/energy-monitor.log` на наявність `MemoryError`. Якщо так — збільшити Instance Type на Render.
2.  **DB Connection Timeout**: Перевірити статус Neon.tech. Перевірити ліміт `max_connections` (50 для Free плану).
3.  **Simulation won't start**: Видалити вручну файл `logs/sensors.lock`.
