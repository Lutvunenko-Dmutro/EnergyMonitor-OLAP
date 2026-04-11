# 🧪 Тестування

## Загальний стан

```
Platform:  Windows / Python 3.13
Framework: pytest 7.4.3
Result:    74 passed, 5 skipped, 0 failed — 13.71s ✅
```

---

## Покриття по модулях

| Файл тесту | Кількість | Що тестується |
|------------|-----------|---------------|
| `test_core_analytics.py` | 11 | OLAP фільтрація, агрегація |
| `test_database.py` | 4 | DB підключення, запити |
| `test_ml_model.py` | 8 (5 skip) | ML pipeline, форми тензорів |
| `test_physics.py` | 5 | Фізична симуляція (Digital Twin) |
| `test_pipeline.py` | 3 | Інтеграційні тести |
| `test_security.py` | 26 | SQL injection, XSS, validation |
| `test_utils.py` | 19 | Утиліти, cache, error handlers |

---

## test_security.py (26 тестів)

Найбільший файл — покриває OWASP Top-10 для дашборду.

```python
class TestSQLInjectionProtection:
    """Перевіряє захист від SQL Injection у всіх точках входу."""

    MALICIOUS_INPUTS = [
        "'; DROP TABLE LoadMeasurements; --",
        "1 OR 1=1",
        "' UNION SELECT * FROM pg_tables --",
        "admin'--",
        "1; DELETE FROM Substations",
    ]

    def test_region_filter_rejects_sql_injection(self):
        for payload in self.MALICIOUS_INPUTS:
            with pytest.raises((ValueError, Exception)):
                validate_region_input(payload)

class TestXSSProtection:
    """Перевіряє захист від Cross-Site Scripting."""

    XSS_PAYLOADS = [
        "<script>alert('xss')</script>",
        "javascript:alert(1)",
        "<img src=x onerror=alert(1)>",
    ]
```

---

## test_physics.py (5 тестів)

Верифікує **фізичну достовірність** Digital Twin.

```python
class TestPhysicsEngine:

    def test_solar_generation_zero_at_night(self):
        """Сонячна генерація о 2:00 = 0."""
        result = calculate_generation(source="solar", hour=2, month=6)
        assert result == 0.0, "Solar cannot generate at night"

    def test_nuclear_generation_stable(self):
        """Атомна базова, незалежна від часу доби."""
        results = [calculate_generation("nuclear", h) for h in range(24)]
        variation = max(results) - min(results)
        assert variation < 0.05 * max(results)

    def test_industrial_load_lower_on_weekend(self):
        """Промислове навантаження знижується у вихідні."""
        weekday = calculate_substation_load("industrial", weekday=True, hour=14)
        weekend = calculate_substation_load("industrial", weekday=False, hour=14)
        assert weekend < weekday * 0.85

    def test_transformer_health_decreases_over_time(self):
        """Health Score знижується при тривалому навантаженні."""
        initial = calculate_transformer_health(load_pct=90, hours=0)
        after_100h = calculate_transformer_health(load_pct=90, hours=100)
        assert after_100h < initial

    def test_hvdc_lower_losses_than_ac(self):
        """HVDC має менші втрати ніж AC при однаковому навантаженні."""
        ac_loss = calculate_losses(type="AC", load_mw=1000, load_pct=80)
        hvdc_loss = calculate_losses(type="HVDC", load_mw=1000, load_pct=80)
        assert hvdc_loss < ac_loss
```

---

## Запуск тестів

```bash
# Всі тести
pytest tests/ -v

# Конкретний файл
pytest tests/test_security.py -v

# Конкретний тест
pytest tests/test_physics.py::TestPhysicsEngine::test_solar_generation_zero_at_night -v

# З покриттям (HTML звіт)
pytest tests/ --cov=src --cov=core --cov=ml --cov-report=html
open htmlcov/index.html

# Тільки швидкі тести (без DB)
pytest tests/ -v -m "not db"

# Паралельно (якщо встановлено pytest-xdist)
pytest tests/ -n auto
```

---

## Написання нових тестів

### Шаблон

```python
# tests/test_my_module.py
import pytest
import pandas as pd
from my_module import my_function


class TestMyFunction:
    """Test suite для my_function."""

    def test_basic_case(self):
        """Базовий сценарій — нормальні вхідні дані."""
        result = my_function(valid_input)
        assert result == expected_output

    def test_empty_input(self):
        """Пустий вхід не викидає виняток."""
        result = my_function(pd.DataFrame())
        assert result.empty

    def test_invalid_type_raises(self):
        """Неправильний тип → ValueError."""
        with pytest.raises(ValueError, match="Expected DataFrame"):
            my_function("not a dataframe")

    @pytest.mark.parametrize("input,expected", [
        (0, 0.0),
        (100, 1.0),
        (50, 0.5),
    ])
    def test_normalized_values(self, input, expected):
        """Параметризований тест нормалізації."""
        assert normalize(input) == pytest.approx(expected, abs=0.01)
```

### Fixtures (conftest.py)

```python
@pytest.fixture
def sample_dataframe():
    """Реалістичний DataFrame із телеметрією."""
    return pd.DataFrame({
        "region_name": ["Київ", "Харків", "Одеса"],
        "actual_load_mw": [150.5, 200.3, 120.1],
        "health_score": [94.2, 88.7, 97.1],
        "timestamp": pd.date_range("2024-01-01", periods=3, freq="h")
    })

@pytest.fixture
def mock_db_empty(monkeypatch):
    """Підміняє DB на порожній результат."""
    monkeypatch.setattr("src.core.database.run_query", lambda *a, **k: pd.DataFrame())
```

---

## CI/CD інтеграція

Тести запускаються автоматично у GitHub Actions при кожному push в `main`:

```yaml
# .github/workflows/ci-cd.yml (скорочено)
- name: Run unit tests
  env:
    DB_NAME: neondb
    DB_HOST: localhost
    PYTHONPATH: .
  run: |
    pytest tests/ -v --cov=src --cov=core --cov=ml \
           --cov-report=xml --junitxml=junit/test-results.xml
```

Результати завантажуються до Codecov для відстеження покриття з часом.
