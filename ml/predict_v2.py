import logging
import os

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s",
)
logger = logging.getLogger(__name__)

from ml.vectorizer import (
    get_latest_window,
    get_local_scalers,
    inverse_scale_predictions,
)

# Конфігурація моделювання
WINDOW_SIZE = 24
V1_DIPLOMA_FREEZE_LOCKED = (
    True  # Блокування модифікацій базової версії V1 для забезпечення стабільності
)

# Шляхи до збережених ваг моделей
MODEL_PATH = "models/substation_model_v2.h5"
SCALER_PATH = "models/scaler_v2.pkl"


def load_resources(version: str = "v3") -> tuple:
    """
    Завантажує оптимізовані ваги ШІ-моделі та відповідний скалер ознак.

    :param version: Версія архітектури моделі ('v1', 'v2', 'v3').
    :return: Кортеж (tf.keras.Model, MinMaxScaler).
    """
    m = f"models/substation_model_{version}.h5"
    s = f"models/scaler_{version}.pkl"
    if not os.path.exists(m) or not os.path.exists(s):
        raise FileNotFoundError(
            f"Файли для версії {version} не знайдено. Потрібно виконати тренування моделі."
        )
    return tf.keras.models.load_model(m, compile=False), joblib.load(s)


def get_ai_forecast(
    hours_ahead: int = 24,
    substation_name: str | None = None,
    source_type: str = "Live",
    version: str = "v3",
) -> tuple[pd.DataFrame, str | None]:
    """
    Основна точка входу для генерації прогнозу навантаження на N годин вперед.

    :param hours_ahead: Горизонт прогнозування (годин).
    :param substation_name: Назва підстанції.
    :param source_type: Джерело даних ('Live' / 'CSV').
    :param version: Версія ШІ-моделі.
    :return: Кортеж (pd.DataFrame, str | None) — прогноз та помилка.
    """
    try:
        model, scaler = load_resources(version)
        values, constants, last_ts, features = get_latest_window(
            substation_name, source_type, version
        )
        if values is None:
            return pd.DataFrame(), "Недостатньо історичних даних для аналізу."

        logger.info(
            f"🔄 Запуск прогнозу (Версія: {version}, Об'єкт: {substation_name})"
        )
        formatted_data = (
            np.array2string(
                values[-1].flatten(), precision=2, separator=", ", suppress_small=True
            )
            if values is not None
            else "None"
        )
        logger.info(f"🧠 Вхідний вектор: [{formatted_data}]")

        local_scaler, target_scaler, scaled_window = get_local_scalers(version, values)
        logger.debug(f"Дані після scaler.transform: {scaled_window[-1]}")
        current_window = scaled_window.copy()
        predictions = []
        n_features = 9 if version == "v3" else (1 if version == "v1" else 5)

        for i in range(hours_ahead):
            x_input = current_window.reshape(1, WINDOW_SIZE, n_features)
            pred_s = model.predict(x_input, verbose=0)[0]
            pred_s[0] = np.clip(pred_s[0], 0, 1.1)  # Захист від розгону
            predictions.append(pred_s)

            placeholder = np.zeros((1, n_features))
            placeholder[0, 0] = pred_s[0]  # Load

            if version == "v1":
                unscaled = local_scaler.inverse_transform([[pred_s[0]]])[0]
                load_u, health_u = unscaled[0], 100.0
            elif version == "v3":
                load_u = target_scaler.inverse_transform([[pred_s[0]]])[0, 0]
                p_inside = np.zeros((1, 9))
                p_inside[0, 0] = pred_s[0]
                p_inside[0, 3] = pred_s[1]
                health_u = local_scaler.inverse_transform(p_inside)[0][3]
            elif version == "v2":
                load_u = target_scaler.inverse_transform([[pred_s[0]]])[0, 0]
                p_inside = np.zeros((1, 5))
                p_inside[0, 0] = pred_s[0]
                p_inside[0, 3] = pred_s[1]
                health_u = local_scaler.inverse_transform(p_inside)[0][3]
            else:
                unscaled = scaler.inverse_transform(placeholder)[0]
                load_u = unscaled[0]
                placeholder[0, 3] = pred_s[1]
                unscaled = scaler.inverse_transform(placeholder)[0]
                health_u = unscaled[3]

            # Корекція прогнозного значення відповідно до останнього історичного показника
            damping = 0.95
            last_load = values[-1, 0]
            load_u = last_load + (load_u - last_load) * (damping ** (i + 1))

            # Динамічний час для наступного кроку
            next_ts = last_ts + pd.Timedelta(hours=i + 1)
            h_n = next_ts.hour
            d_n = next_ts.weekday()

            if version == "v3":
                new_row_u = np.array(
                    [
                        [
                            load_u,
                            constants["oil"],
                            constants["h2"],
                            health_u,
                            constants["air"],
                            np.sin(2 * np.pi * h_n / 24),
                            np.cos(2 * np.pi * h_n / 24),
                            np.sin(2 * np.pi * d_n / 7),
                            np.cos(2 * np.pi * d_n / 7),
                        ]
                    ]
                )
            elif version == "v1":
                new_row_u = np.array([[load_u]])
            else:
                new_row_u = np.array(
                    [
                        [
                            load_u,
                            constants["oil"],
                            constants["h2"],
                            health_u,
                            constants["air"],
                        ]
                    ]
                )

            if version in ["v1", "v2", "v3"]:
                new_row_s = local_scaler.transform(new_row_u)
            else:
                new_row_s = scaler.transform(new_row_u)
            current_window = np.vstack([current_window[1:], new_row_s])

        # ---------------------------------------------------------------------
        # Секція зворотного масштабування відповідно до версії
        # ---------------------------------------------------------------------
        predictions = np.array(predictions)

        load_fc, health_fc = inverse_scale_predictions(
            predictions, version, local_scaler, target_scaler, scaler, hours_ahead
        )

        # Запобіжник від помилок екстраполяції для версій V2/V3
        if version in ["v2", "v3"]:
            max_historical_load = np.max(values[:, 0])
            safe_limit = max_historical_load * 1.5
            load_fc = np.clip(load_fc, a_min=0, a_max=safe_limit)
            logger.info(
                f"📊 [Аналіз {substation_name}]: Історія Макс={max_historical_load:.2f} МВт | Ліміт={safe_limit:.2f} МВт | Прогноз Макс={np.max(load_fc):.2f} МВт"
            )

        # Корекція розриву між іст. та прог. значеннями (Smart Stitching)
        last_real_load = values[-1, 0]
        gap = last_real_load - load_fc[0]

        logger.info(
            f"🎯 Прогноз успішно згенеровано. Рядків: {hours_ahead} (Gap: {gap:.2f} МВт)"
        )

        decay = np.exp(-np.arange(hours_ahead) / 6.0)
        load_fc = load_fc + (gap * decay)

        # Страховка від від'ємних значень
        load_fc = np.maximum(load_fc, 0)

        # Розрахунок довірчих інтервалів
        std_dev = np.std(values[:, 0]) if len(values) > 0 else 10.0
        upper_bond = load_fc + (std_dev * (1 + np.arange(hours_ahead) / 24))
        lower_bond = np.maximum(
            load_fc - (std_dev * (1 + np.arange(hours_ahead) / 24)), 0
        )

        # Генеруємо таймстемпи вперед
        forecast_ts = [last_ts + pd.Timedelta(hours=i + 1) for i in range(hours_ahead)]

        df_forecast = pd.DataFrame(
            {
                "timestamp": forecast_ts,
                "predicted_load_mw": load_fc,
                "predicted_health_score": health_fc,
                "upper_bond": upper_bond,
                "lower_bond": lower_bond,
            }
        )
        return df_forecast, None

    except Exception as e:
        logger.error(f"Помилка в get_ai_forecast: {str(e)}", exc_info=True)
        return pd.DataFrame(), str(e)
