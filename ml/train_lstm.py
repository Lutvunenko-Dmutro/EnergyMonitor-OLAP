import os
import sys

# Додаємо корінь проекту до PATH, щоб скрипт бачив модулі database та config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential

from src.core.database import get_db_cursor
from src.core.logger import setup_logger

logger = setup_logger(__name__)

import argparse

# --- 1. CONFIGURATION ---
LOOK_BACK = 24
EPOCHS = 50
BATCH_SIZE = 32


def get_paths(version="v3"):
    """Повертає шляхи до моделі та скалера за версією."""
    return f"models/substation_model_{version}.h5", f"models/scaler_{version}.pkl"


def load_data_from_db(version="v3"):
    """Витягує ознаки з банку історичних даних залежно від версії."""
    logger.info(
        "📡 Завантаження мультимодальних даних з LoadMeasurements + WeatherReports..."
    )

    query = """
    SELECT 
        DATE_TRUNC('hour', lm.timestamp) AS ts,
        SUM(lm.actual_load_mw)           AS load_mw,
        AVG(lm.temperature_c)            AS oil_temp,
        AVG(lm.h2_ppm)                   AS h2_ppm,
        AVG(lm.health_score)             AS health,
        AVG(wr.temperature)              AS air_temp
    FROM LoadMeasurements lm
    JOIN Substations s ON lm.substation_id = s.substation_id
    JOIN Regions r     ON s.region_id = r.region_id
    LEFT JOIN WeatherReports wr 
           ON DATE_TRUNC('hour', wr.timestamp) = DATE_TRUNC('hour', lm.timestamp)
           AND wr.region_id = r.region_id
    GROUP BY DATE_TRUNC('hour', lm.timestamp)
    ORDER BY ts ASC
    """

    with get_db_cursor() as (conn, cursor):
        cursor.execute(query)
        data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=["timestamp", "load_mw", "oil_temp", "h2_ppm", "health", "air_temp"],
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Приводимо до чисел
    for col in ["load_mw", "oil_temp", "h2_ppm", "health", "air_temp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.set_index("timestamp", inplace=True)
    df_hourly = df.resample("h").mean().interpolate(method="linear")

    if version == "v3":
        # --- CYCLICAL FEATURES (Seasonal Waves) ---
        df_hourly["hour"] = df_hourly.index.hour
        df_hourly["day"] = df_hourly.index.weekday

        df_hourly["hour_sin"] = np.sin(2 * np.pi * df_hourly["hour"] / 24)
        df_hourly["hour_cos"] = np.cos(2 * np.pi * df_hourly["hour"] / 24)
        df_hourly["day_sin"] = np.sin(2 * np.pi * df_hourly["day"] / 7)
        df_hourly["day_cos"] = np.cos(2 * np.pi * df_hourly["day"] / 7)

        # Видаляємо допоміжні
        df_hourly = df_hourly.drop(columns=["hour", "day"])

    return df_hourly


def create_dataset(dataset, look_back=24):
    """Створює x, y з урахуванням 9 ознак та 2 таргети (Навантаження [0], Здоров'я [3])."""
    x, y = [], []
    for i in range(len(dataset) - look_back):
        x.append(dataset[i : (i + look_back), :])  # 9 ознак
        y.append(dataset[i + look_back, [0, 3]])  # Load + Health
    return np.array(x), np.array(y)


def train_lstm(version="v3"):
    """Підготовка даних та навчання мультимодальної моделі Keras."""
    os.makedirs("models", exist_ok=True)
    model_path, scaler_path = get_paths(version)

    df = load_data_from_db(version=version)
    if df.empty:
        logger.error("❌ База даних порожня. Навчання неможливе.")
        return

    # 4. Нормалізація для всіх 5 колонок
    values = df.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)

    # Збереження скалера
    joblib.dump(scaler, scaler_path)
    logger.info(f"💾 Скалер збережено у {scaler_path}")

    # 5. Підготовка часових вікон
    x, y = create_dataset(scaled, LOOK_BACK)

    # x має форму [samples, look_back, 5] - вже готово з create_dataset
    # Масштаб 80/20
    train_size = int(len(x) * 0.8)
    x_train, x_test = x[:train_size], x[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    n_features = x_train.shape[2]
    logger.info(
        f"🏗️ Модель {n_features} inputs -> 2 outputs (Train samples: {len(x_train)})..."
    )

    from tensorflow.keras.layers import Dropout

    # 6. Створення моделі
    model = Sequential(
        [
            LSTM(64, return_sequences=True, input_shape=(LOOK_BACK, n_features)),
            Dropout(0.2),
            LSTM(32, return_sequences=False),
            Dropout(0.1),
            Dense(2),  # Прогнозуємо [Load, Health]
        ]
    )

    model.compile(optimizer="adam", loss="mean_squared_error")

    # 7. Навчання
    logger.info(f"🚀 Початок навчання ({EPOCHS} епох)...")
    model.fit(
        x_train,
        y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(x_test, y_test),
        verbose=1,
    )

    model.save(model_path)
    logger.info(f"✅ Модель збережена: {model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Навчання LSTM моделей")
    parser.add_argument(
        "--version", type=str, default="v3", help="Версія моделі (v1, v2, v3)"
    )
    args = parser.parse_args()

    logger.info(
        f"🔧 Мультимодальний режим: Напруга + Здоров'я | Версія: {args.version.upper()}"
    )
    train_lstm(version=args.version)
