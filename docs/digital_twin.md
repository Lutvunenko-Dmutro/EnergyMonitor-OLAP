# 🏭 Digital Twin

## Концепція

Digital Twin — це **фізична симуляція** підстанцій у реальному часі. На відміну від ML (статистичний підхід), Digital Twin використовує детерміновані фізичні формули для моделювання:

- Теплового стану трансформаторного масла
- Генерації водню (H₂) при деградації ізоляції
- Health Score обладнання

---

## Архітектура процесу

```
UI: Sidebar "▶️ Запустити"
          │
          ▼
   subprocess.Popen()          ← не блокує UI
          │
          ▼
   sensors_db.py               ← фоновий процес
   run_cosmetic_collector()
          │
          ├──► logs/sensors.lock       (singleton PID)
          │
          └────────────────────────────────────────┐
    кожні ~5 сек:                                  │
          │                                        │
          ▼                                        │
   src/core/physics.py                             │ TIMEOUT
   calculate_substation_load()                     │ = 900s
   calculate_transformer_health()                  │ (15 хв)
          │                                        │
          ▼                                        │
   logs/live_state.json ◄───────────────────────── ┘
          │
          ▼
   live_kpi.py
   @st.fragment(run_every=5)   ← читає JSON, оновлює UI
```

---

## Фізичні моделі

### Модель навантаження підстанції

```python
# src/core/physics.py — calculate_substation_load()
base_load = capacity_mw * base_factor   # 60-80% від потужності

# Температурний множник (вплив пори року)
if temperature > 30:
    temp_multiplier = 1.15   # Літо: кондиціонери
elif temperature < 0:
    temp_multiplier = 1.20   # Зима: опалення
else:
    temp_multiplier = 1.0

# Добовий профіль (час доби)
hour_factor = LOAD_PROFILES[substation_type][current_hour]

actual_load = base_load * temp_multiplier * hour_factor * (1 + noise)
```

### Теплова модель трансформатора

```python
# calculate_transformer_health()
# Температура масла залежить від навантаження нелінійно:
oil_temp = ambient_temp + (load_pct / 100) ** 1.6 * delta_temp_max

# Генерація H₂ — індикатор деградації ізоляції (Arrhenius):
h2_rate = base_rate * exp(activation_energy * (oil_temp - 85) / 10)

# Health Score спадає з часом:
health = max(0, health - degradation_rate * delta_time)
```

### Модель втрат у мережі (core/analytics/physics.py)

| Тип лінії | Формула втрат | Коефіцієнт |
|-----------|--------------|------------|
| **AC** | $P_{loss} = P \cdot 0.035 \cdot (load\%)^2$ | Квадратична (I²R) |
| **HVDC** | $P_{loss} = P \cdot 0.015 \cdot load\%$ | Лінійна |

HVDC > 3000 МВт — класифікується автоматично.

---

## Файли стану

### `logs/live_state.json`

```json
{
    "timestamp": "2026-04-11T08:05:23",
    "substations": [
        {
            "name": "Київська ТЕЦ-5",
            "actual_load_mw": 312.4,
            "health_score": 94.2,
            "temperature_c": 68.1,
            "h2_ppm": 23.7,
            "load_pct": 78.1
        }
    ],
    "total_mw": 2847.3,
    "avg_health": 91.8
}
```

### `logs/sensors.lock`

```
12847
```
Містить PID процесу. Sidebar перевіряє наявність файлу, щоб визначити статус симуляції.

---

## Конфігурація

```python
# src/services/sensors_db.py
TIMEOUT_SECONDS = 900    # 15 хвилин (для демо диплому)

# Для продакшн-режиму:
TIMEOUT_SECONDS = 3600   # 1 година
# або
TIMEOUT_SECONDS = 0      # Нескінченно (вручну зупиняти)
```

---

## Тестування фізики

Фізичні формули верифікуються автоматично в `tests/test_physics.py`:

```python
class TestPhysics:
    def test_solar_generation_at_night(self):
        """Сонячна генерація вночі = 0."""
        gen = calculate_generation(source="solar", hour=2)
        assert gen == 0.0

    def test_nuclear_stable_at_98_percent(self):
        """Атомна генерація стабільна ≈ 98%."""
        gen = calculate_generation(source="nuclear", hour=12)
        assert 0.95 <= gen / max_capacity <= 1.0

    def test_industrial_load_drops_on_weekend(self):
        """Промислове навантаження у вихідні знижується."""
        weekday_load = calculate_substation_load(type="industrial", weekday=True)
        weekend_load = calculate_substation_load(type="industrial", weekday=False)
        assert weekend_load < weekday_load * 0.8
```

**Принцип:** якщо Digital Twin генерує нереалістичну телеметрію → LSTM навчиться на неправильних патернах → *Garbage In, Garbage Out*. Тести гарантують фізичну достовірність.

---

## Запуск і зупинка

```bash
# Запустити вручну (для тестування)
python -m src.services.sensors_db

# Перевірити стан
Get-Content logs/live_state.json   # Windows

# Примусово зупинити
Remove-Item logs/sensors.lock      # Windows
rm logs/sensors.lock               # Linux
```
