import os
import sys

# Додаємо корінь проекту до PATH ПЕРЕД імпортами локальних модулів
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential

from src.core.database import get_db_cursor
from src.core.logger import setup_logger

logger = setup_logger(__name__)

WINDOW_SIZE = 24


def get_paths():
    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
    return os.path.join(BASE_DIR, "models", "substation_model_v1.h5"), os.path.join(
        BASE_DIR, "models", "scaler_v1.pkl"
    )


def load_v1_data():
    """Витягує тільки навантаження з бази (1 ознака)."""
    logger.info("📡 Завантаження базових даних V1 (Тільки LoadMeasurements)...")
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

    # Інтерполяція пропусків
    df_hourly = df.resample("h").sum().replace(0, np.nan).interpolate(method="linear")
    return df_hourly[["load_mw"]].values  # Формат (N, 1)


def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i : (i + seq_length)]
        y = data[i + seq_length, 0]  # Передбачаємо 1 число
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


def train_lstm_v1():
    model_path, scaler_path = get_paths()
    data = load_v1_data()

    if len(data) < WINDOW_SIZE * 2:
        logger.error("❌ Недостатньо даних для навчання V1!")
        return

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    logger.info(
        f"💾 Зафіксовано розмірність scaler_v1: {scaler.n_features_in_} features"
    )
    joblib.dump(scaler, scaler_path)

    x, y = create_sequences(scaled_data, WINDOW_SIZE)
    split = int(0.8 * len(x))
    x_train, x_test = x[:split], x[split:]
    y_train, y_test = y[:split], y[split:]

    logger.info(f"🏗️ Модель V1 (1 input -> 1 output) Shape: {x_train.shape}")

    model = Sequential(
        [
            LSTM(64, input_shape=(WINDOW_SIZE, 1), return_sequences=True),
            LSTM(32),
            Dense(16, activation="relu"),
            Dense(1),  # ОДИН ВИХІД
        ]
    )

    model.compile(optimizer="adam", loss="mse")

    logger.info("🚀 Початок навчання Baseline V1 (50 епох)...")
    model.fit(
        x_train,
        y_train,
        epochs=50,
        batch_size=32,
        validation_data=(x_test, y_test),
        verbose=1,
    )

    model.save(model_path)
    logger.info(f"✅ Модель збережена: {model_path}")


if __name__ == "__main__":
    train_lstm_v1()
