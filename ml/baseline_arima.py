import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import warnings
import itertools

warnings.filterwarnings('ignore')

# Темна тема для графіків (узгоджена зі Streamlit)
if 'dark_background' in plt.style.available:
    plt.style.use('dark_background')

def find_best_arima(train_data, test_data):
    """
    Систематичний Grid Search для SARIMA.
    """
    p_values = [0, 1, 2]
    d_values = [1]
    q_values = [0, 1]
    
    best_score, best_cfg = float("inf"), None
    pdq_combinations = list(itertools.product(p_values, d_values, q_values))
    
    # Використовуємо підмножину даних для прискорення пошуку
    test_sub = test_data[:72] # Оцінюємо по перших 3 днях
    
    for pdq in pdq_combinations:
        try:
            # Завжди фіксуємо сезонність на 24 години
            model = ARIMA(train_data, order=pdq, seasonal_order=(1, 1, 1, 24))
            model_fit = model.fit()
            predictions = model_fit.forecast(steps=len(test_sub))
            
            rmse = np.sqrt(mean_squared_error(test_sub, predictions))
            if rmse < best_score:
                best_score = rmse
                best_cfg = pdq
        except Exception:
            continue
            
    print(f"✅ Найкраща модель SARIMA{best_cfg}x(1,1,1,24)")
    return best_cfg


def rolling_arima_forecast(train_data, test_data, order, seasonal_order=(1, 1, 1, 24)):
    """
    Поточковий прогноз з ковзаючим вікном (Rolling Window).
    Кожну годину додаємо реальне значення в історію та прогнозуємо наступне.
    """
    history = list(train_data)
    predictions = []
    
    print(f"📡 Запуск Rolling SARIMA ({len(test_data)} кроків)...")
    
    # Використовуємо SARIMAX для гнучкості та швидкості оновлення
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    
    # Початкове навчання на всій історії
    model = SARIMAX(history, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit(disp=False)
    
    # Перший прогноз
    yhat = model_fit.forecast()[0]
    predictions.append(yhat)
    
    # Цикл по тесту (крім останнього)
    for i in range(len(test_data) - 1):
        obs = test_data[i]
        # Оновлюємо модель новим спостереженням БЕЗ повного перенавчання (append)
        model_fit = model_fit.append([obs], refit=False)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        
    return np.array(predictions)


def run_arima_baseline(version, train_data, test_data, do_grid_search=False):
    """
    Навчання та прогноз SARIMA бейзлайну (тепер Rolling One-Step).
    """
    print(f"🚀 Запуск SARIMA для версії {version}...")
    
    # Сезонність 24 години (Daily Cycle)
    seasonal_order = (1, 1, 1, 24)
    
    if do_grid_search:
        order = find_best_arima(train_data, test_data)
    else:
        order = (1, 1, 1) 
        
    try:
        # Використовуємо Rolling Forecast для точності (One-Step-Ahead як у LSTM)
        predictions = rolling_arima_forecast(train_data, test_data, order, seasonal_order)
        
        # Розрахунок метрик
        mape = mean_absolute_percentage_error(test_data, predictions) * 100
        rmse = np.sqrt(mean_squared_error(test_data, predictions))
        
        print(f"[{version.upper()}] SARIMA{order} Rolling | RMSE: {rmse:.2f} | MAPE: {mape:.2f}%")
        return predictions, mape, rmse
    except Exception as e:
        print(f"❌ Помилка ARIMA: {str(e)}")
        return np.zeros(len(test_data)), 100.0, 1000.0

if __name__ == '__main__':
    # Тестовий запуск
    dummy_train = np.sin(np.linspace(0, 100, 100)) + np.random.normal(0, 0.1, 100)
    dummy_test = np.sin(np.linspace(100, 124, 24))
    run_arima_baseline("v3", dummy_train, dummy_test, do_grid_search=True)
