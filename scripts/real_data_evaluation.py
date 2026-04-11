import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.stats import norm
import sys
import os

# Додаємо корінь проєкту до шляху пошуку модулів
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import run_query
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.optimizers import Adam

# ==============================================================================
# 1. ГЕНЕРАЦІЯ BASELINE МОДЕЛІ (Naive Persistence)
# ==============================================================================
def get_baseline_prediction(X_test_scaled, scaler):
    """
    Базова модель: Прогноз на завтра = Навантаження за сьогодні.
    Оскільки X_test має форму (samples, 24, 1), де 24 - це попередні 24 години,
    ми просто використовуємо ці самі 24 години як прогноз.
    """
    # X_test_scaled shape: (samples, 24, 1)
    # Повертаємо останній крок як прогноз на наступний період (спрощено)
    # Або просто повертаємо X як є (якщо це ідентичний добовий профіль)
    return X_test_scaled.reshape(X_test_scaled.shape[0], 24)

# ==============================================================================
# 2. ПІДГОТОВКА ДАНИХ ТА МОДЕЛІ (Data & Model)
# ==============================================================================
def fetch_real_data(substation_id=10):
    query = f"SELECT timestamp, actual_load_mw FROM LoadMeasurements WHERE substation_id = {substation_id} ORDER BY timestamp"
    df = run_query(query)
    return df[['actual_load_mw']].values

def create_dataset(dataset, look_back=24, forecast_horizon=24):
    X, y = [], []
    for i in range(len(dataset) - look_back - forecast_horizon + 1):
        X.append(dataset[i : i + look_back, 0])
        y.append(dataset[i + look_back : i + look_back + forecast_horizon, 0])
    return np.array(X).reshape(-1, 24, 1), np.array(y)

def build_model():
    model = Sequential([
        LSTM(64, recurrent_dropout=0.2, input_shape=(24, 1)),
        Dropout(0.2),
        Dense(24)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model

# ==============================================================================
# 5. ОСНОВНА ЛОГІКА (Main Workflow)
# ==============================================================================
def main():
    print("📈 Крок 1: Завантаження та передобробка...")
    data = fetch_real_data(substation_id=10)
    
    train_size = int(len(data) * 0.8)
    train_data, test_data = data[0:train_size], data[train_size:len(data)]
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    train_scaled = scaler.fit_transform(train_data)
    test_scaled = scaler.transform(test_data)
    
    X_train, y_train = create_dataset(train_scaled)
    X_test, y_test = create_dataset(test_scaled)
    
    print("🧠 Крок 2: Навчання LSTM (50 епох)...")
    model = build_model()
    model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=0)
    
    # ПЕРЕДБАЧЕННЯ
    print("🔮 Крок 3: Розрахунок прогнозів та метрик...")
    lstm_preds_scaled = model.predict(X_test, verbose=0)
    baseline_preds_scaled = get_baseline_prediction(X_test, scaler)
    
    # ЗВОРОТНЄ МАСШТАБУВАННЯ (Critical Fix)
    y_test_real = scaler.inverse_transform(y_test)
    lstm_preds_real = scaler.inverse_transform(lstm_preds_scaled)
    baseline_preds_real = scaler.inverse_transform(baseline_preds_scaled)
    
    # РОЗРАХУНОК МЕТРИК
    lstm_rmse = np.sqrt(mean_squared_error(y_test_real, lstm_preds_real))
    lstm_mae = mean_absolute_error(y_test_real, lstm_preds_real)
    
    base_rmse = np.sqrt(mean_squared_error(y_test_real, baseline_preds_real))
    base_mae = mean_absolute_error(y_test_real, baseline_preds_real)
    
    print("\n" + "="*40)
    print(f"📊 МЕТРИКИ LSTM:     RMSE = {lstm_rmse:.2f}, MAE = {lstm_mae:.2f}")
    print(f"📊 МЕТРИКИ BASELINE: RMSE = {base_rmse:.2f}, MAE = {base_mae:.2f}")
    print("="*40 + "\n")
    
    # ==========================================================================
    # FIGURE 5: ПЕРЕРОБЛЕНО (Continuous 14-day Forecast with Baseline)
    # ==========================================================================
    print("🖼️ Генерація Figure 5 (14-day Continuous)...")
    days_to_plot = 14
    points_to_plot = days_to_plot * 24
    
    stitched_actual = []
    stitched_forecast = []
    stitched_baseline = [] # Додано для Baseline
    
    for i in range(0, min(points_to_plot, len(y_test_real)), 24):
        stitched_actual.extend(y_test_real[i])
        stitched_forecast.extend(lstm_preds_real[i])
        stitched_baseline.extend(baseline_preds_real[i])
            
    plt.figure(figsize=(15, 6))
    plt.plot(stitched_actual, label='Actual Data', color='orange', linewidth=1.5)
    plt.plot(stitched_forecast, label='LSTM Forecast', color='red', linestyle='-', linewidth=1.5)
    plt.plot(stitched_baseline, label='Baseline Forecast', color='green', linestyle='-', linewidth=1.5)
    
    plt.title(f'Comparison of LSTM and Baseline forecasts with actual values ({days_to_plot} Days)')
    plt.xlabel('Time (Hours)')
    plt.ylabel('Load (MW)')
    plt.legend()
    plt.grid(True, linestyle='-', alpha=0.7)
    plt.tight_layout()
    plt.savefig('figure_5_continuous.png', dpi=300) # Висока роздільна здатність
    plt.close()
    
    # ==========================================================================
    # FIGURE 7: ПЕРЕРОБЛЕНО (Academic Style Distribution)
    # ==========================================================================
    print("🖼️ Генерація Figure 7 (Comparative Distribution)...")
    lstm_errors = (y_test_real - lstm_preds_real).flatten()
    base_errors = (y_test_real - baseline_preds_real).flatten()
    
    plt.figure(figsize=(10, 6))
    
    # Histogram for LSTM (Фіолетовий колір)
    _, bins_l, _ = plt.hist(lstm_errors, bins=50, density=True, alpha=0.5, color='purple', label='LSTM Errors')
    mu_l, std_l = norm.fit(lstm_errors)
    xl = np.linspace(min(lstm_errors), max(lstm_errors), 100)
    # Пунктирна червона лінія для розподілу LSTM + Peak
    peak_l = max(norm.pdf(xl, mu_l, std_l))
    plt.plot(xl, norm.pdf(xl, mu_l, std_l), color='red', linestyle='--', linewidth=2.5, label=rf'LSTM: $\mu$={mu_l:.2f}, $\sigma$={std_l:.2f}, peak={peak_l:.2f}')
    
    # Histogram for Baseline (Зелений колір)
    _, bins_b, _ = plt.hist(base_errors, bins=50, density=True, alpha=0.4, color='green', label='Baseline Errors')
    mu_b, std_b = norm.fit(base_errors)
    xb = np.linspace(min(base_errors), max(base_errors), 100)
    # Пунктирна зелена лінія для розподілу Baseline + Peak
    peak_b = max(norm.pdf(xb, mu_b, std_b))
    plt.plot(xb, norm.pdf(xb, mu_b, std_b), color='green', linestyle='--', linewidth=2.5, label=rf'Baseline: $\mu$={mu_b:.2f}, $\sigma$={std_b:.2f}, peak={peak_b:.2f}')
    
    plt.title('Histogram of forecast errors with fitted normal distributions')
    plt.xlabel('Forecast Error (MW)')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, linestyle='-', alpha=0.7)
    plt.tight_layout()
    plt.savefig('figure_7_comparison.png', dpi=300)
    plt.close()
    
    print("✅ Скрипт завершено. Файли figure_5_continuous.png та figure_7_comparison.png створено.")

if __name__ == "__main__":
    main()
