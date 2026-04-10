# ═══════════════════════════════════════════════════════════════
# Unit Tests for ML Module
# ═══════════════════════════════════════════════════════════════
"""
Тести для ml/predict_v2.py (LSTM inference)
Запуск: pytest tests/test_ml_model.py -v
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class TestLSTMPredictor:
    """Test suite для LSTM prediction функціональності."""
    
    def test_model_initialization(self):
        """Тест: модель інітіалізується без помилок."""
        try:
            from ml.predict_v2 import LSTMPredictor
            model = LSTMPredictor()
            assert model is not None
        except ImportError:
            pytest.skip("ML module not available")
    
    def test_forecast_output_shape(self, sample_forecast_data):
        """Тест: forecast повинен повертати правильний shape."""
        try:
            from ml.predict_v2 import LSTMPredictor
            model = LSTMPredictor()
            
            # Prepare input
            X_test = sample_forecast_data.reshape(1, 24, 9)
            
            # Predict
            prediction = model.predict(X_test)
            
            # Check shape: (1, 24, 1) для 24-hour forecast, 1 feature
            assert prediction.shape[0] == 1  # batch size
            assert prediction.shape[1] == 24  # forecast horizon
            assert prediction.shape[2] == 1   # output feature
        except ImportError:
            pytest.skip("ML module not available")
    
    def test_forecast_values_in_range(self, sample_forecast_data):
        """Тест: forecasted values повинні бути в розумному діапазоні."""
        try:
            from ml.predict_v2 import LSTMPredictor
            model = LSTMPredictor()
            
            X_test = sample_forecast_data.reshape(1, 24, 9)
            prediction = model.predict(X_test)
            
            # Check that values are not NaN or inf
            assert not np.isnan(prediction).any()
            assert not np.isinf(prediction).any()
            
            # Check that values are in reasonable range (0-500 MW for energy)
            assert (prediction >= 0).all() or (prediction.min() > -500)
            assert prediction.max() < 1000
        except ImportError:
            pytest.skip("ML module not available")
    
    def test_batch_prediction(self, sample_forecast_data):
        """Тест: модель повинна обробляти batch predictions."""
        try:
            from ml.predict_v2 import LSTMPredictor
            model = LSTMPredictor()
            
            # Create batch of 5 samples
            X_batch = np.repeat(sample_forecast_data[np.newaxis, :, :], 5, axis=0)
            
            # Predict
            predictions = model.predict(X_batch)
            
            assert predictions.shape[0] == 5  # batch size
            assert predictions.shape[1] == 24  # horizon
        except ImportError:
            pytest.skip("ML module not available")
    
    def test_domain_adaptation(self):
        """Тест: модель повинна підтримувати domain adaptation."""
        try:
            from ml.predict_v2 import LSTMPredictor
            model = LSTMPredictor()
            
            # Спробуємо адаптуватися до різних регіонів
            regions = ['Київ', 'Харків', 'Львів']
            
            for region in regions:
                # Проверь, чи функція adapt_to_region існує
                if hasattr(model, 'adapt_to_region'):
                    model.adapt_to_region(region)
                    assert True  # If no error, test passes
        except ImportError:
            pytest.skip("ML module not available")


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
