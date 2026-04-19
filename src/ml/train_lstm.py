import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential
import argparse
import datetime
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint

# Додаємо корінь проекту до PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.database import get_db_cursor
from src.core.logger import setup_logger

logger = setup_logger(__name__)

# --- CONFIGURATION ---
LOOK_BACK = 48 
EPOCHS = 100
BATCH_SIZE = 32

def get_paths(version="v3"):
    """Повертає шляхи до моделі та скалера за версією."""
    if version == "v3":
        return "models/substation_model_v3_final.h5", "models/scaler_v3_final.pkl"
    return f"models/substation_model_{version}.h5", f"models/scaler_{version}.pkl"

def load_data_from_db(version="v3"):
    """Витягує ознаки з БД, зберігаючи ізоляцію кожної підстанції (Шлях Б)."""
    logger.info(f"📡 Завантаження даних з ізоляцією по підстанціях (Версія: {version})...")

    query = """
    SELECT 
        DATE_TRUNC('hour', lm.timestamp) AS ts,
        s.substation_name,
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
    GROUP BY DATE_TRUNC('hour', lm.timestamp), s.substation_name
    ORDER BY s.substation_name, ts ASC
    """

    with get_db_cursor() as (conn, cursor):
        cursor.execute(query)
        data = cursor.fetchall()

    df = pd.DataFrame(data, columns=["timestamp", "substation_name", "load_mw", "oil_temp", "h2_ppm", "health", "air_temp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    for col in ["load_mw", "oil_temp", "h2_ppm", "health", "air_temp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    processed_dfs = []
    for sub_name, group in df.groupby("substation_name"):
        # Окрема обробка кожної станції
        group = group.set_index("timestamp").resample("h").mean(numeric_only=True).interpolate(method="linear")
        group["substation_name"] = sub_name
        
        if version == "v3":
            # --- CYCLICAL FEATURES ---
            group["hour_sin"] = np.sin(2 * np.pi * group.index.hour / 24)
            group["hour_cos"] = np.cos(2 * np.pi * group.index.hour / 24)
            group["day_sin"] = np.sin(2 * np.pi * group.index.weekday / 7)
            group["day_cos"] = np.cos(2 * np.pi * group.index.weekday / 7)

        # Визначаємо набір колонок
        if version == "v1":
            cols = ["load_mw", "substation_name"]
        elif version == "v2":
            cols = ["load_mw", "oil_temp", "h2_ppm", "health", "air_temp", "substation_name"]
        else: # v3
            cols = ["load_mw", "oil_temp", "h2_ppm", "health", "air_temp", "hour_sin", "hour_cos", "day_sin", "day_cos", "substation_name"]
            
        processed_dfs.append(group[cols].dropna())

    return pd.concat(processed_dfs)

def create_dataset(dataset, look_back=48):
    """Створює x, y на основі масиву. Тепер УСІ версії роблять 1 крок вперед."""
    x, y = [], []
    forecast_horizon = 1 
    
    for i in range(len(dataset) - look_back - forecast_horizon + 1):
        x.append(dataset[i : (i + look_back), :])
        y.append(dataset[i + look_back, 0])  # Тільки індекс 0 (load_mw)
            
    return np.array(x), np.array(y)

def train_lstm(version="v3", look_back=48):
    """Підготовка даних та навчання УНІВЕРСАЛЬНОЇ моделі."""
    os.makedirs("models", exist_ok=True)
    model_path, scaler_path = get_paths(version)

    df = load_data_from_db(version=version)
    if df.empty:
        logger.error("❌ База даних порожня. Навчання неможливе.")
        return

    # 1. Створюємо єдиний скейлер для всієї країни (рівень підстанції)
    features_only = df.drop(columns=["substation_name"]).values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(features_only)
    
    joblib.dump(scaler, scaler_path)
    logger.info(f"💾 Універсальний скалер збережено у {scaler_path}")

    # 2. Нарізаємо вікна ізольовано для кожної станції
    all_x, all_y = [], []
    for sub_name, group in df.groupby("substation_name"):
        group_features = group.drop(columns=["substation_name"]).values
        scaled_group = scaler.transform(group_features)
        
        sub_x, sub_y = create_dataset(scaled_group, look_back=look_back)
        if len(sub_x) > 0:
            all_x.append(sub_x)
            all_y.append(sub_y)
            
    X = np.vstack(all_x)
    Y = np.concatenate(all_y)

    # Shuffle
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    X, Y = X[indices], Y[indices]

    train_size = int(len(X) * 0.8)
    x_train, x_test = X[:train_size], X[train_size:]
    y_train, y_test = Y[:train_size], Y[train_size:]

    n_features = x_train.shape[2]
    logger.info(f"🏗️ Модель {n_features} inputs -> 1 output (Samples: {len(x_train)})...")

    # 3. АРХІТЕКТУРА БЕЗ ГЛУШНИКІВ
    if version == "v3":
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=(look_back, n_features)),
            LSTM(64, return_sequences=False),
            Dense(32, activation='relu'),
            Dense(1) 
        ])
    else:
        # ОНОВЛЕНА АРХІТЕКТУРА ДЛЯ V1 / V2 — Виправлення "Наївного прогнозу"
        model = Sequential([
            LSTM(128, return_sequences=False, input_shape=(look_back, n_features)),
            Dropout(0.1),
            Dense(32, activation='relu'),
            Dense(1)
        ])

    # Динамічний вибір функції втрат: MAE для V1 (чіткість), Huber для V3 (стійкість)
    loss_fn = "huber" if version == "v3" else "mae"
    model.compile(optimizer="adam", loss=loss_fn)

    logger.info(f"🚀 Початок навчання Універсальної Моделі {version.upper()} ({EPOCHS} епох)...")
    
    # --- CALLBACKS ---
    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    os.makedirs("models/checkpoints", exist_ok=True)
    
    callbacks = [
        TensorBoard(log_dir=log_dir, histogram_freq=1),
        EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
        ModelCheckpoint(
            filepath=f"models/checkpoints/best_{version}.keras",
            monitor='val_loss',
            save_best_only=True
        )
    ]

    model.fit(
        x_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(x_test, y_test),
        verbose=1,
        callbacks=callbacks
    )

    final_model_p = "models/substation_model_v3_final.keras" if version == "v3" else model_path
    model.save(final_model_p)
    logger.info(f"✅ Універсальна модель збережена: {final_model_p}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Навчання універсальних LSTM моделей")
    parser.add_argument("--version", type=str, default="v3", help="Версія моделі (v1, v2, v3)")
    parser.add_argument("--window_size", type=int, default=48, help="Розмір LOOK_BACK (годин)")
    args = parser.parse_args()

    train_lstm(version=args.version, look_back=args.window_size)
