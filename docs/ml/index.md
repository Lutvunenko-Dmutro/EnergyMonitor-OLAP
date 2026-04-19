# 🧠 ML Pipeline

## Огляд

AI-підсистема побудована на трирівневій архітектурі:

```
Дані з БД → Векторизація → LSTM Inference → Domain Adaptation → Прогноз
                                     ↓ (якщо недоступний)
                              Seasonal Naive Fallback
```

---

## Версії моделей

| Версія | Ознак | Вікно | Таргети | Статус |
|--------|-------|-------|---------|--------|
| **v1** | 1 (`load_mw`) | 24h | 1 | Архів |
| **v2** | 5 (+ погода) | 24h | 1 | Архів |
| **v3** | 9 (+ time harmonics) | 48h | 1 | ✅ **Production** |
| **Zero-Fail** | — | — | 1 | Fallback |

---

## Вектор ознак v3

$$x_t = [\underbrace{load}_{МВт}, \underbrace{temp\_oil}_{°C}, \underbrace{h2\_ppm}_{ppm}, \underbrace{health}{\%}, \underbrace{air\_temp}_{°C}, \underbrace{h_{sin}}_{}, \underbrace{h_{cos}}_{}, \underbrace{d_{sin}}_{}, \underbrace{d_{cos}}_{}]^T \in \mathbb{R}^9$$

### Часові гармоніки (циклічне кодування)

```python
# vectorizer.py
df["hour_sin"] = np.sin(2 * np.pi * hours / 24)
df["hour_cos"] = np.cos(2 * np.pi * hours / 24)
df["day_sin"]  = np.sin(2 * np.pi * days / 7)
df["day_cos"]  = np.cos(2 * np.pi * days / 7)
```

Усуває розриви неперервності (23:59 → 00:00) через проекцію на тригонометричне коло.

---

## vectorizer.py

Головна функція — `get_latest_window()`:

```python
def get_latest_window(
    substation_name: Optional[str],
    source_type: str = "Live",    # "Live" (DB) або "CSV" (Kaggle)
    version: str = "v3",
    offset_hours: int = 0,         # Для rolling backtest
    window_size: int = 48          # DEFAULT_WINDOW_SIZE
) -> Tuple[np.ndarray, Dict, pd.Timestamp, List[str]]:
    """
    Повертає:
      - values: матриця (48, 9) нормалізованих ознак
      - constants: {'oil', 'h2', 'air', 'health'} останнього спостереження
      - last_ts: timestamp останньої точки
      - feature_names: назви ознак
    """
```

**Джерела даних:**

| `source_type` | Звідки | Коли використовувати |
|---------------|--------|---------------------|
| `"Live"` | PostgreSQL (Neon) | Production, реальний моніторинг |
| `"CSV"` | Kaggle CSV файл | Backtest, офлайн-тестування |

---

## predict_v2.py

### Domain Adaptation

Автоматично масштабує прогноз під конкретну підстанцію:

```python
def _compute_scale_factor(values, substation_name, source_type, scaler):
    """
    Порівнює глобальний максимум (з усіх підстанцій, навчена модель)
    з локальним максимумом (конкретна підстанція).

    Якщо global_max >> local_max: scale_down (не перепрогнозувати)
    Якщо local_max >> global_max: scale_up (збільшити для великих об'єктів)
    """
    scale_factor = clip(global_max / local_max, 1.0, 100.0)
```

### Ітеративний прогноз (Recursive Forecasting)

```python
# predict_v2.py — спрощена логіка
for step in range(hours_ahead):          # 24 кроки вперед
    prediction = model.predict(window)   # LSTM.predict → load_t+1 (здоров'я рахує physics.py)
    window = roll(window, prediction)    # Зсув вікна: викидаємо t-48, додаємо t+1
```

### 📈 Smart Stitching (Exponential Decay)

При переході від останнього відомого факту $y_{t}$ до першого кроку прогнозу $\hat{y}_{t+1}$ часто виникає розрив (step-jump) через похибку моделі. Для візуальної та логічної цілісності використовується експоненціальне згладжування помилки:

**Помилка початкового кроку**:
$$\delta = y_t - \hat{y}_t$$

**Корекція для k-го кроку прогнозу**:
$$\hat{y}_{t+k}^{corr} = \hat{y}_{t+k} + \delta \cdot \lambda^k$$

Де $\lambda$ — коефіцієнт затухання ($\approx 0.85$). Це забезпечує плавний старт прогнозної кривої без втрати точності моделі на довгій дистанції.

---

## metrics_engine.py

### Метрики точності

| Метрика | Формула | Значення |
|---------|---------|----------|
| **RMSE** | $\sqrt{\frac{1}{n}\sum(y_i - \hat{y}_i)^2}$ | МВт (менше — краще) |
| **MAE** | $\frac{1}{n}\sum\|y_i - \hat{y}_i\|$ | МВт (менше — краще) |
| **MAPE** | $\frac{1}{n}\sum\frac{\|y_i - \hat{y}_i\|}{y_i} \times 100$ | % (менше — краще) |
| **R²** | $1 - \frac{SS_{res}}{SS_{tot}}$ | 0..1 (більше — краще) |

### Statistical Audit (Shapiro-Wilk)

```python
def perform_statistical_audit(errors: np.ndarray) -> Dict[str, Any]:
    """
    Перевіряє нормальність розподілу залишків прогнозу.

    Returns:
        mu, sigma, p_value, is_normal (p > 0.05),
        skew (асиметрія), kurt (ексцес)
    """
    _, p_val = stats.shapiro(errors)
    return {"is_normal": p_val > 0.05, ...}
```

Методологічна цінність: якщо `is_normal=True` — модель не систематично помиляється.

---

## backtest.py

Валідація на 7 днях (168 годин) реальних даних:

```python
TEST_SIZE_HOURS = 168  # 7 днів

# Запуск через UI: "Аналітика" → "Бектест"
# Або вручну:
from src.ml.backtest import run_backtest
run_backtest(version="v3", substation="Київська ТЕЦ-5")
```

Бектест включає:
1. Rolling window prediction (offset_hours)
2. Merge з реальними даними з БД
3. Robust 3-sigma outlier filtering (MAD)
4. Обчислення RMSE/MAE/MAPE/R²

---

## baseline_arima.py — Zero-Fail Fallback

```python
# Якщо LSTM модель недоступна (файл не знайдено, OOM, тощо) —
# система автоматично переходить на Seasonal Naive:
# forecast[h] = actual[h - period]  (period = 24 або 168 год.)
```

Це гарантує **24/7 uptime** дашборду навіть без AI-моделі.

---

## Навчання нової моделі

```bash
# Версія v3 (рекомендована)
python ml/train_lstm.py --version v3

# Результат: models/substation_model_v3.h5 + substation_scaler_v3.pkl
```

Функція втрат — **Huber Loss** (стійка до викидів у телеметрії):
$$\mathcal{L}_{\delta}(y, \hat{y}) = \begin{cases} \frac{1}{2}(y - \hat{y})^2, & |y - \hat{y}| \leq \delta \\ \delta \cdot |y - \hat{y}| - \frac{1}{2}\delta^2, & |y - \hat{y}| > \delta \end{cases}$$

Оптимізатор: **Adam** з Backpropagation Through Time (BPTT).
