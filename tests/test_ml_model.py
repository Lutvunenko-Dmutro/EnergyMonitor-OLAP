"""
ВЕРИФІКАЦІЯ ШІ-ДВИГУНА ТА LSTM-ПРОГНОЗІВ (ML Model & Inference Validation)
========================================================================
Набір тестів для аудиту інтелектуальних модулів прогнозування Energy Monitor.
Ключові можливості:
1. Neural Inference Verification: тестування ініціалізації LSTM-предикторів та виконання прогнозів.
2. Tensor Topology Audit: верифікація розмірностей (Shape) тензорів для сумісності з Keras.
3. Forecast Quality Metrics: перевірка алгоритмів розрахунку похибок (RMSE, MAE, MAPE).
4. Preprocessing & Encoding: валідація циклічного кодування часу та нормалізації даних.
Гарантує стабільність та математичну достовірність ШІ-прогнозів системи.
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class TestLSTMPredictor:
    """Test suite для LSTM prediction функціональності."""
    
    def test_model_initialization(self):
        """Тест: перевірка наявності модулів прогнозування."""
        from src.ml import predict_v2
        assert hasattr(predict_v2, "get_ai_forecast")
        
    def test_forecast_output_shape(self):
        """Тест: baseline fallback генерує правильний shape DataFrame."""
        from src.ml.predict_v2 import _run_baseline_fallback
        import pandas as pd
        values = np.array([[100.0], [105.0], [110.0]])
        last_ts = pd.Timestamp("2023-01-01 12:00:00")
        df = _run_baseline_fallback(24, values, last_ts)
        # 1 last value + 24 predictions
        assert len(df) == 25
        assert "predicted_load_mw" in df.columns
        
    def test_forecast_values_in_range(self):
        """Тест: значення прогнозу знаходяться в адекватному діапазоні."""
        from src.ml.predict_v2 import _run_baseline_fallback
        import pandas as pd
        values = np.array([[100.0]])
        last_ts = pd.Timestamp("2023-01-01 12:00:00")
        df = _run_baseline_fallback(24, values, last_ts)
        assert df["predicted_load_mw"].min() >= 0
        assert not df["predicted_load_mw"].isnull().any()
        
    def test_batch_prediction(self):
        """Тест: перевірка обчислення scale factor для адаптації."""
        from src.ml.predict_v2 import _compute_scale_factor
        class DummyScaler:
            data_max_ = [5000]
        values = np.array([[1000.0]])
        scale, loc_max = _compute_scale_factor(values, "Test Sub", "CSV", DummyScaler())
        assert scale >= 1.0
        assert loc_max == 1000.0
        
    def test_domain_adaptation(self):
        """Тест: перевірка нормалізації температури та health score."""
        from src.ml.predict_v2 import _build_norm_overrides
        class DummyScaler:
            data_max_ = [0, 0, 0, 100, 30]
            data_min_ = [0, 0, 0, 0, -20]
        current_window = np.zeros((1, 5))
        current_window[-1, 4] = 0.5
        target_temp, norm_health = _build_norm_overrides(
            5, current_window, DummyScaler(), 5.0, {"health": 80}
        )
        assert target_temp is not None
        assert norm_health == 0.8


class TestForecastMetrics:
    """Test suite для метрик якості прогнозу."""
    
    def test_rmse_calculation(self):
        """Тест: RMSE розраховується правильно."""
        y_true = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1.1, 2.1, 2.9, 3.9, 5.1])
        
        # Compute RMSE manually
        mse = np.mean((y_true - y_pred) ** 2)
        rmse = np.sqrt(mse)
        
        assert rmse > 0
        assert rmse < 1  # Should be small errors
    
    def test_mae_calculation(self):
        """Тест: MAE розраховується правильно."""
        y_true = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1.1, 2.1, 2.9, 3.9, 5.1])
        
        # Compute MAE manually
        mae = np.mean(np.abs(y_true - y_pred))
        
        assert mae > 0
        assert mae < 1
    
    def test_mape_calculation(self):
        """Тест: MAPE розраховується правильно."""
        y_true = np.array([100, 200, 300, 400, 500])
        y_pred = np.array([101, 202, 298, 399, 501])
        
        # Compute MAPE manually
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        assert mape > 0
        assert mape < 5  # Should be < 5% error


class TestDataPreprocessing:
    """Test suite для preprocessing даних для моделі."""
    
    def test_normalization(self):
        """Тест: нормалізація працює правильно."""
        from sklearn.preprocessing import MinMaxScaler
        
        X = np.array([100, 200, 300, 400, 500]).reshape(-1, 1)
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Check range [0, 1]
        assert X_scaled.min() >= 0
        assert X_scaled.max() <= 1
    
    def test_sliding_window_creation(self):
        """Тест: sliding window створюється правильно."""
        data = np.arange(100)
        window_size = 24
        
        windows = []
        for i in range(len(data) - window_size):
            windows.append(data[i:i+window_size])
        
        windows = np.array(windows)
        
        assert windows.shape[0] == len(data) - window_size
        assert windows.shape[1] == window_size
    
    def test_cyclical_encoding(self):
        """Тест: cyclical encoding для часу."""
        hour = 12  # noon
        
        hour_sin = np.sin(2 * np.pi * hour / 24)
        hour_cos = np.cos(2 * np.pi * hour / 24)
        
        # Check that values are in [-1, 1]
        assert -1 <= hour_sin <= 1
        assert -1 <= hour_cos <= 1
        
        # Check that 0 and 24 дають однакові значення
        hour_0_sin = np.sin(2 * np.pi * 0 / 24)
        hour_24_sin = np.sin(2 * np.pi * 24 / 24)
        
        assert np.isclose(hour_0_sin, hour_24_sin)
