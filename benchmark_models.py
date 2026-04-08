import os
import sys
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import norm
from tensorflow.keras.models import load_model

# Додаємо корінь проєкту до шляху пошуку модулів
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml.train_lstm import load_data_from_db
from ml.baseline_arima import run_arima_baseline

# ==============================================================================
# 1. SETUP
# ==============================================================================
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)
SUBSTATION_ID = 10  # ПС Київська-Центральна

# ==============================================================================
# 2. АКАДЕМІЧНА ВІЗУАЛІЗАЦІЯ (Scientific Figures)
# ==============================================================================
import seaborn as sns

def generate_scientific_plots(model_name, actual, forecast, arima_pred):
    """Генерація 3 фінальних графіків у сучасному дата-саєнс стилі."""
    
    # Вмикаємо сучасний стиль
    sns.set_theme(style="whitegrid", palette="muted")
    
    # ==========================================
    # 1. Figure 5: Comparison (14 Days)
    # ==========================================
    plt.figure(figsize=(15, 6))
    
    # Використовуємо більш приємні кольори та товщину
    plt.plot(actual[:336], label='Actual Load', color='#ff9f43', linewidth=2.5, alpha=0.8)
    plt.plot(forecast[:336], label='LSTM Forecast', color='#ee5253', linewidth=2.5, alpha=0.9)
    plt.plot(arima_pred[:336], label='ARIMA Forecast', color='#10ac84', linewidth=2, linestyle='--', alpha=0.8)
    
    plt.title(f'Figure 5 ({model_name.upper()}): Comparison of forecasts (14 Days)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Time (Hours)', fontsize=12)
    plt.ylabel('Load (MW)', fontsize=12)
    plt.legend(frameon=True, shadow=True, fontsize=11)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/fig5_{model_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ==========================================
    # 2. Figure 7: Error Distribution
    # ==========================================
    lstm_errors = actual[:336] - forecast[:336]
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
             
    plt.title(f'Figure 7 ({model_name.upper()}): Error Distribution with Normal Fit', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Forecast Error (MW)', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.legend(frameon=True, shadow=True, fontsize=11)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/fig7_{model_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ==========================================
    # 3. Scatter Plot with R2
    # ==========================================
    r2 = r2_score(actual[:336], forecast[:336])
    
    plt.figure(figsize=(8, 8))
    plt.scatter(actual[:336], forecast[:336], color='#54a0ff', alpha=0.7, edgecolor='white', s=50, label='Predicted vs Actual')
    
    lims = [np.min([actual[:336], forecast[:336]]), np.max([actual[:336], forecast[:336]])]
    plt.plot(lims, lims, color='#ee5253', linestyle='--', linewidth=2.5, zorder=0, label='Ideal Fit (y=x)')
    
    plt.title(f'Scatter ({model_name.upper()}): Actual vs Predicted (R² = {r2:.4f})', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Actual Load (MW)', fontsize=12)
    plt.ylabel('LSTM Predicted Load (MW)', fontsize=12)
    plt.legend(frameon=True, shadow=True, fontsize=11)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/scatter_{model_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

# ==============================================================================
# 3. BENCHMARK EXECUTION
# ==============================================================================
def run_benchmark():
    versions = ["v1", "v2", "v3"]
    
    for ver in versions:
        print(f"\n🚀 БЕНЧМАРК МОДЕЛІ {ver.upper()} (One-Step-Ahead)...")
        
        model_file = f"models/substation_model_{ver}.h5" if ver != "v3" else "models/lstm_v3_multistep.keras"
        scaler_file = f"models/scaler_{ver}.pkl"
        
        if not os.path.exists(model_file) or not os.path.exists(scaler_file):
            print(f"⚠️ Модель або скалер для {ver} не знайдено.")
            continue
            
        # 1. Завантаження даних
        df = load_data_from_db(version=ver)
        data = df.values
        scaler = joblib.load(scaler_file)
        data_scaled = scaler.transform(data)
        
        # Тестова вибірка (останні 20%)
        test_size = int(len(data_scaled) * 0.2)
        train_scaled = data_scaled[: -test_size]
        test_scaled = data_scaled[-test_size:]
        
        # 2. Завантаження моделі
        model = load_model(model_file)
        model_output_size = model.output_shape[-1]
        print(f"   Інфо: Модель має {model_output_size} вихідний(их) нейрон(ів).")

        # 3. Оцінка (One-Step-Ahead: 336 годин)
        total_steps = 336
        WINDOW_SIZE = 24
        
        X_test, y_test = [], []
        for i in range(total_steps):
            X_test.append(test_scaled[i : i + WINDOW_SIZE, :])
            # Фактичне значення (завжди колонка 0: load_mw)
            y_test.append(test_scaled[i + WINDOW_SIZE, 0])
            
        X_test = np.array(X_test)
        y_test = np.array(y_test)
        
        # Прогноз
        preds_scaled = model.predict(X_test, verbose=0)
        
        # Якщо модель має кілька виходів (v2 має 2, v3 має 24), беремо ПЕРШИЙ (навантаження)
        if model_output_size > 1:
            preds_scaled = preds_scaled[:, 0]
        else:
            preds_scaled = preds_scaled.flatten()
            
        # Зворотне масштабування
        # Для inverse_transform потрібно мати ту ж кількість колонок
        def inverse(vals, sc, n_cols):
            dummy = np.zeros((len(vals), n_cols))
            dummy[:, 0] = vals
            return sc.inverse_transform(dummy)[:, 0]

        preds_unscaled = inverse(preds_scaled, scaler, data.shape[1])
        actual_unscaled = inverse(y_test, scaler, data.shape[1])
        
        # 4. ARIMA Baseline (Grid Search)
        train_unscaled = data[: -test_size, 0]
        print(f"   🔬 Пошук найкращої SARIMA для {ver}...")
        arima_preds, _, _ = run_arima_baseline(ver, train_unscaled, actual_unscaled, do_grid_search=True)
        
        # 5. Метрики
        rmse = np.sqrt(mean_squared_error(actual_unscaled, preds_unscaled))
        mae = mean_absolute_error(actual_unscaled, preds_unscaled)
        r2 = r2_score(actual_unscaled, preds_unscaled)
        
        print(f"📊 {ver.upper()} Result: RMSE = {rmse:.2f}, MAE = {mae:.2f}, R² = {r2:.4f}")
        
        # 6. Плоти
        generate_scientific_plots(ver, actual_unscaled, preds_unscaled, arima_preds)
        print(f"✅ Усі графіки для {ver.upper()} збережені у {RESULTS_DIR}/")

if __name__ == "__main__":
    run_benchmark()
