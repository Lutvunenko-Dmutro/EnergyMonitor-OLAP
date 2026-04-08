import os
import sys
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import norm
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.models import Sequential, load_model

# Додаємо корінь проєкту до PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import get_db_cursor
from src.core.logger import setup_logger
from ml.baseline_arima import run_arima_baseline

logger = setup_logger(__name__)

WINDOW_SIZE = 24
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def get_paths():
    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
    return os.path.join(BASE_DIR, "models", "substation_model_v1.h5"), os.path.join(
        BASE_DIR, "models", "scaler_v1.pkl"
    )

def load_v1_data():
    """Витягує тільки навантаження з бази (1 ознака)."""
    logger.info("📡 Завантаження даних V1...")
    query = """
    SELECT 
        ts,
        SUM(avg_load) AS load_mw
    FROM (
        SELECT 
            DATE_TRUNC('hour', lm.timestamp) AS ts,
            lm.substation_id,
            AVG(lm.actual_load_mw)           AS avg_load
        FROM LoadMeasurements lm
        GROUP BY DATE_TRUNC('hour', lm.timestamp), lm.substation_id
    ) s
    GROUP BY ts
    ORDER BY ts ASC
    """
    with get_db_cursor() as (conn, cursor):
        cursor.execute(query)
        data = cursor.fetchall()

    df = pd.DataFrame(data, columns=["timestamp", "load_mw"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["load_mw"] = pd.to_numeric(df["load_mw"], errors="coerce")
    df.set_index("timestamp", inplace=True)
    df_hourly = df.resample("h").sum().replace(0, np.nan).interpolate(method="linear")
    return df_hourly

def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i : (i + seq_length)]
        y = data[i + seq_length, 0]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

import seaborn as sns

def generate_final_plots(actual, lstm_pred, arima_pred):
    """Генерація 3 фінальних графіків у сучасному дата-саєнс стилі."""
    
    # Вмикаємо сучасний стиль
    sns.set_theme(style="whitegrid", palette="muted")
    
    # ==========================================
    # 1. Figure 5: Comparison (14 Days)
    # ==========================================
    plt.figure(figsize=(15, 6))
    
    # Використовуємо більш приємні кольори та товщину
    plt.plot(actual[:336], label='Actual Load', color='#ff9f43', linewidth=2.5, alpha=0.8)
    plt.plot(lstm_pred[:336], label='LSTM Forecast', color='#ee5253', linewidth=2.5, alpha=0.9)
    plt.plot(arima_pred[:336], label='ARIMA Forecast', color='#10ac84', linewidth=2, linestyle='--', alpha=0.8)
    
    plt.title('Comparison of forecasts with actual values (14 Days Forecast)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Time (Hours)', fontsize=12)
    plt.ylabel('Load (MW)', fontsize=12)
    plt.legend(frameon=True, shadow=True, fontsize=11)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/fig5_v1_final.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ==========================================
    # 2. Figure 7: Error Distribution
    # ==========================================
    lstm_errors = actual[:336] - lstm_pred[:336]
    arima_errors = actual[:336] - arima_pred[:336]
    
    plt.figure(figsize=(10, 6))
    
    # Гістограми з м'якою прозорістю
    sns.histplot(lstm_errors, bins=40, stat="density", color='#5f27cd', alpha=0.4, label='LSTM Errors', edgecolor='white')
    sns.histplot(arima_errors, bins=40, stat="density", color='#10ac84', alpha=0.3, label='ARIMA Errors', edgecolor='white')
    
    # Криві нормального розподілу
    mu_l, std_l = norm.fit(lstm_errors)
    x_l = np.linspace(min(lstm_errors), max(lstm_errors), 100)
    peak_l = max(norm.pdf(x_l, mu_l, std_l))
    plt.plot(x_l, norm.pdf(x_l, mu_l, std_l), color='#ee5253', linestyle='-', linewidth=2.5, 
             label=rf'LSTM Fit: $\mu$={mu_l:.2f}, $\sigma$={std_l:.2f}, peak={peak_l:.2f}')
    
    mu_a, std_a = norm.fit(arima_errors)
    x_a = np.linspace(min(arima_errors), max(arima_errors), 100)
    peak_a = max(norm.pdf(x_a, mu_a, std_a))
    plt.plot(x_a, norm.pdf(x_a, mu_a, std_a), color='#222f3e', linestyle='--', linewidth=2.5, 
             label=rf'ARIMA Fit: $\mu$={mu_a:.2f}, $\sigma$={std_a:.2f}, peak={peak_a:.2f}')
             
    plt.title('Histogram of Forecast Errors with Normal Distribution', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Forecast Error (MW)', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.legend(frameon=True, shadow=True, fontsize=11)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/fig7_v1_final.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ==========================================
    # 3. Scatter Plot with R2
    # ==========================================
    r2 = r2_score(actual[:336], lstm_pred[:336])
    
    plt.figure(figsize=(8, 8))
    # Малюємо точки (робимо їх меншими і напівпрозорими для уникнення злиття)
    plt.scatter(actual[:336], lstm_pred[:336], color='#54a0ff', alpha=0.7, edgecolor='white', s=50, label='Predicted vs Actual')
    
    # Ідеальна діагональ
    lims = [np.min([actual[:336], lstm_pred[:336]]), np.max([actual[:336], lstm_pred[:336]])]
    plt.plot(lims, lims, color='#ee5253', linestyle='--', linewidth=2.5, zorder=0, label='Ideal Fit (y=x)')
    
    plt.title(f'Scatter Plot of Actual vs Predicted (R² = {r2:.4f})', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Actual Load (MW)', fontsize=12)
    plt.ylabel('LSTM Predicted Load (MW)', fontsize=12)
    plt.legend(frameon=True, shadow=True, fontsize=11)
    # Робимо пропорції квадратними
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/scatter_v1_final.png", dpi=300, bbox_inches='tight')
    plt.close()

def train_and_evaluate():
    model_path, scaler_path = get_paths()
    df = load_v1_data()
    data = df[["load_mw"]].values

    # Data Leakage Fix: Fit on 80%
    split_idx = int(0.8 * len(data))
    train_raw = data[:split_idx]
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(train_raw)
    scaled_data = scaler.transform(data)
    joblib.dump(scaler, scaler_path)

    xs, ys = create_sequences(scaled_data, WINDOW_SIZE)
    split = int(0.8 * len(xs))
    x_train, x_test = xs[:split], xs[split:]
    y_train, y_test = ys[:split], ys[split:]

    # ARCHITECTURE
    model = Sequential([
        Input(shape=(WINDOW_SIZE, 1)),
        LSTM(64, return_sequences=True),
        Dropout(0.2),
        LSTM(64, return_sequences=False),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mean_squared_error")

    logger.info("🚀 Тренування моделі (20 епох)...")
    model.fit(x_train, y_train, epochs=20, batch_size=32, validation_data=(x_test, y_test), verbose=1)
    model.save(model_path)

    # ==========================================
    # EVALUATION (One-Step-Ahead для 336 годин)
    # ==========================================
    logger.info("📡 Генерація поточкового прогнозу LSTM (One-Step-Ahead, 336 годин)...")
    
    # Беремо перші 14 днів (336 годин) з тестової вибірки
    X_test_sample = x_test[:336]
    y_test_sample = y_test[:336]
    
    # Робимо прогноз: на кожному кроці модель бачить РЕАЛЬНІ попередні 24 години
    lstm_preds_scaled = model.predict(X_test_sample, verbose=0)
    
    # Зворотне масштабування
    lstm_preds_unscaled = scaler.inverse_transform(lstm_preds_scaled).flatten()
    actual_test_unscaled = scaler.inverse_transform(y_test_sample.reshape(-1, 1)).flatten()
    
    # ==========================================
    # ARIMA Baseline
    # ==========================================
    logger.info("📡 Генерація прогнозу ARIMA...")
    # Для ARIMA потрібен просто одновимірний масив історії
    # Історія до початку X_test_sample
    split_idx_actual = split + WINDOW_SIZE
    train_unscaled = data[:split_idx_actual, 0]
    
    arima_preds_unscaled, _, _ = run_arima_baseline("v1_final", train_unscaled, actual_test_unscaled, do_grid_search=True)

    # ==========================================
    # PLOTTING
    # ==========================================
    generate_final_plots(actual_test_unscaled, lstm_preds_unscaled, arima_preds_unscaled)
    
    logger.info("✅ Усі графіки збережені у results/!")

if __name__ == "__main__":
    train_and_evaluate()
