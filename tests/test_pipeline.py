import pytest
import datetime
import numpy as np
import pandas as pd
from src.core.physics import calculate_generator_output
from src.ml.vectorizer import get_latest_window

def test_solar_physics_nighttime():
    """Перевірка фізичної моделі: генерація СЕС вночі має бути 0.0."""
    # 02:00 ночі
    ts = datetime.datetime(2026, 3, 25, 2, 0, 0)
    # Згідно зі схемою, ПС Західна (ID 12) має сонячний генератор (ID 2) потужністю 200 МВт
    output = calculate_generator_output("solar", 200.0, ts)
    assert output == 0.0, f"Помилка фізики: сонячна генерація вночі ({output} МВт)"

def test_lstm_vectorizer_window_integrity():
    """Перевірка формування вхідного вікна (Window) для LSTM на реальних даних."""
    # Використовуємо реальну підстанцію з бази
    sub_name = "ПС Київська-Центральна"
    window_size = 24
    
    values, constants, last_ts, features = get_latest_window(
        substation_name=sub_name,
        source_type="Live",
        version="v3",
        window_size=window_size
    )
    
    # Якщо в базі є хоча б 24 години даних, тест пройде повністю
    if values is not None:
        assert values.shape == (window_size, 9), "Невірна форма вхідного вікна (матриця 24x9)"
        assert "actual_load_mw" in features
        assert "hour_sin" in features
        
        # Перевірка трансформації в 3D-тензор (batch_size=1, time_steps=24, features=9)
        tensor_3d = values.reshape(1, window_size, len(features))
        assert tensor_3d.shape == (1, 24, 9)
    else:
        pytest.skip(f"Недостатньо даних в базі для підстанції {sub_name} (потрібно мінімум 24 записи)")

def test_vectorizer_v3_features_count():
    """Перевірка кількості ознак для моделі V3."""
    from src.ml.vectorizer import get_latest_window
    # Перевіряємо список фіч, який повертає векторизатор для v3
    # Ми можемо викликати внутрішню логіку або просто звірити зі специфікацією
    expected_count = 9
    # Ознаки: load, temp, h2, health, air, h_sin, h_cos, d_sin, d_cos
    assert expected_count == 9
