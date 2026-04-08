import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.optimizers import Adam

# ==============================================================================
# 1. ГЕНЕРАЦІЯ СИНТЕТИЧНИХ ДАНИХ (Synthetic Data Generation)
# ==============================================================================
def generate_synthetic_data(n_points=1500):
    """Генерує часовий ряд енергоспоживання (синусоїда + шум)."""
    t = np.arange(n_points)
    # Добова сезонність (цикл 24 точки)
    seasonal_cycle = 50 + 20 * np.sin(2 * np.pi * t / 24)
    # Випадковий шум
    noise = np.random.normal(0, 2, n_points)
    data = seasonal_cycle + noise
    
    # Нормалізація в діапазон [0, 1]
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data.reshape(-1, 1))
    
    return data_scaled, scaler

# ==============================================================================
# 2. ПІДГОТОВКА ВІКОН (Direct Multi-step Dataset)
# ==============================================================================
def create_dataset(dataset, look_back=24, forecast_horizon=24):
    """Розбиває ряд на вікна: X (історія 24) -> y (прогноз 24)."""
    X, y = [], []
    for i in range(len(dataset) - look_back - forecast_horizon + 1):
        X.append(dataset[i : i + look_back, 0])
        y.append(dataset[i + look_back : i + look_back + forecast_horizon, 0])
    
    X = np.array(X)
    y = np.array(y)
    
    # Решейпінг для Keras (samples, time_steps, features)
    X = X.reshape(X.shape[0], X.shape[1], 1)
    
    return X, y

# ==============================================================================
# 3. АРХІТЕКТУРА МОДЕЛІ (Scientific Architecture)
# ==============================================================================
def build_lstm_model(input_shape=(24, 1), output_size=24):
    """Будує модель згідно з вимогами наукової статті."""
    model = Sequential([
        # LSTM шар з recurrent_dropout
        LSTM(64, recurrent_dropout=0.2, input_shape=input_shape),
        # Стандартний Dropout
        Dropout(0.2),
        # Повнозв'язний шар для прогнозу на 24 години
        Dense(output_size)
    ])
    
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model

# ==============================================================================
# 4. ГОЛОВНИЙ ЦИКЛ (Execution & Visualization)
# ==============================================================================
def main():
    print("🚀 Крок 1: Генерація даних...")
    data_scaled, scaler = generate_synthetic_data(1500)
    
    print("📊 Крок 2: Формування вікон прогнозу (look_back=24, horizon=24)...")
    X, y = create_dataset(data_scaled, look_back=24, forecast_horizon=24)
    print(f"   Розмір вхідних даних X: {X.shape}")
    print(f"   Розмір цільових даних y: {y.shape}")
    
    print("🧠 Крок 3: Тренування моделі (50 епох, batch=16)...")
    model = build_lstm_model(input_shape=(24, 1), output_size=24)
    
    history = model.fit(
        X, y,
        epochs=50,
        batch_size=16,
        validation_split=0.2,
        verbose=1
    )
    
    # Візуалізація результатів
    print("📈 Крок 4: Побудова графіків...")
    plt.figure(figsize=(14, 6))
    
    # Графік 1: Лоси
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train Loss', color='blue')
    plt.plot(history.history['val_loss'], label='Val Loss', color='red')
    plt.title('Модель: Крива навчання (MSE)')
    plt.xlabel('Епоха')
    plt.ylabel('Втрати')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Графік 2: Перевірка прогнозу на випадковому зразку
    plt.subplot(1, 2, 2)
    sample_idx = np.random.randint(0, len(X))
    actual_y = y[sample_idx]
    predicted_y = model.predict(X[sample_idx].reshape(1, 24, 1), verbose=0)[0]
    
    # Повернення до реальних одиниць для графіку
    actual_real = scaler.inverse_transform(actual_y.reshape(-1, 1))
    predicted_real = scaler.inverse_transform(predicted_y.reshape(-1, 1))
    
    plt.plot(actual_real, label='Фактичне навантаження', marker='o', color='green')
    plt.plot(predicted_real, label='Прогноз LSTM', marker='x', linestyle='--', color='blue')
    plt.title('Прогноз 24 годин: LSTM vs Real')
    plt.xlabel('Година прогнозу')
    plt.ylabel('МВт')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    print("✅ Готово! Результати візуалізовано.")

if __name__ == "__main__":
    main()
