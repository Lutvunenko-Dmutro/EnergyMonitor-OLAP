import datetime
import random
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd

from src.core.config import LOAD_PROFILES


def calculate_line_losses(df_lines: pd.DataFrame) -> pd.DataFrame:
    """
    Розраховує втрати потужності в мережі для AC та HVDC ліній.
    Математична модель: 
    - AC: Losses ~ I^2 * R (квадратична залежність від навантаження)
    - HVDC: Losses ~ I * R (більш лінійна, менші втрати на дистанції)
    """
    if df_lines.empty:
        return df_lines

    df = df_lines.copy()

    # Визначення типу ліній (HVDC для магістралей > 3000 МВт)
    if "line_type" not in df.columns and "max_load_mw" in df.columns:
        df["line_type"] = df["max_load_mw"].apply(
            lambda x: "HVDC" if x >= 3000 else "AC"
        )

    if "line_type" not in df.columns:
        df["line_type"] = "AC"

    is_hvdc = df["line_type"] == "HVDC"
    # Базис втрат: 1.5% для DC, 3.5% для AC при піку
    loss_dc = (df["actual_load_mw"] * 0.015) * (df["load_pct"] / 100)
    loss_ac = (df["actual_load_mw"] * 0.035) * (df["load_pct"] / 100) ** 2
    
    df["losses_mw"] = np.where(is_hvdc, loss_dc, loss_ac)

    return df


def estimate_grid_stability(load_mw: float, gen_mw: float) -> str:
    """
    Оцінює стабільність енергосистеми на основі балансу генерації та споживання.
    """
    if gen_mw <= 0: return "Критично"
    ratio = load_mw / gen_mw
    
    if ratio > 1.2: return "Критично"  # Дефіцит > 20%
    if ratio > 1.05: return "Попередження" # Ризик каскадного відключення
    if ratio < 0.8: return "Попередження"  # Надлишок (ризик зростання частоти)
    
    return "Стабільно"


def calculate_weather(
    ts: datetime.datetime, current_temps: Dict[int, float]
) -> Dict[int, Tuple[float, str]]:
    """
    Розраховує погодні умови з інерцією та плавними переходами.
    """
    weather_map = {}
    hour = ts.hour
    minute = ts.minute
    time_val = hour + minute / 60.0

    for region_id, current_temp in current_temps.items():
        # Добовий цикл температури (синусоїда)
        amplitude = 5.0
        peak_hour = 14.0
        daily_cycle = amplitude * np.sin((time_val - peak_hour + 6) * np.pi / 12)

        # Випадковий тренд (зміна базової температури)
        current_temps[region_id] += np.random.normal(0, 0.02)

        # Мікро-флуктуації
        jitter = np.random.normal(0, 0.1)

        final_temp = float(current_temps[region_id] + daily_cycle + jitter)

        # Умови залежать від часу та вологості (умовної)
        is_daylight = 6 < hour < 20
        chance = random.random()
        if chance > 0.8:
            condition = "Дощ" if final_temp > 0 else "Сніг"
        elif chance > 0.5:
            condition = "Хмарно"
        else:
            condition = "Сонячно" if is_daylight else "Ясно"

        weather_map[region_id] = (round(final_temp, 2), condition)

    return weather_map


def calculate_energy_price(hour: int, is_weekend: bool, region_id: int) -> float:
    """
    Розрахунок ціни згідно з постановою НКРЕКП № 949.
    """
    if 0 <= hour < 7:  # Ніч
        base_price, max_cap = 4000, 5600
    elif 7 <= hour < 11:  # Ранковий пік
        base_price, max_cap = 5800, 6900
    elif 11 <= hour < 17:  # ДЕННИЙ ПРОВАЛ
        base_price, max_cap = 3500, 5600
    elif 17 <= hour < 23:  # Вечірній пік
        base_price, max_cap = 7500, 9000
    else:  # 23:00 - 24:00
        base_price, max_cap = 5000, 6900

    weekend_factor = 0.9 if is_weekend else 1.0
    volatility = random.uniform(0.95, 1.15) + (region_id * 0.005)
    final_price = base_price * weekend_factor * volatility

    if final_price > max_cap:
        final_price = max_cap

    return round(final_price, 2)


def calculate_substation_load(
    capacity: float,
    profile_type: str,
    ts: datetime.datetime,
    temp: float,
    is_weekend: bool,
    previous_factor: float = 0.5,
) -> Tuple[float, Optional[Tuple]]:
    """
    Розраховує навантаження з урахуванням часу, температури та інерції мережі.
    Математична модель: Load = Base_Capacity * Hourly_Profile * Day_Multiplier * Temp_Multiplier ± Noise
    """
    hour = ts.hour
    minute = ts.minute

    # 1. Hourly Profile (з інтерполяцією хвилин для плавності)
    current_h_factor = LOAD_PROFILES[profile_type].get(hour, 0.5)
    next_h_factor = LOAD_PROFILES[profile_type].get((hour + 1) % 24, 0.5)
    hourly_profile = current_h_factor + (next_h_factor - current_h_factor) * (
        minute / 60.0
    )

    # 2. Day Multiplier
    day_multiplier = 0.8 if is_weekend else 1.0

    # 3. Temp Multiplier (U-Shape Curve)
    temp_multiplier = 1.0
    if temp < 20.0:
        temp_multiplier += (
            20.0 - temp
        ) * 0.015  # Холодніше 20°C -> +1.5% на кожен градус
    elif temp > 22.0:
        temp_multiplier += (temp - 22.0) * 0.02  # Гарячіше 22°C -> +2% на кожен градус

    # 4. Noise (Гауссівський шум ± 2-5%)
    # Використовуємо 3% стандартне відхилення
    noise = np.random.normal(0, 0.03)

    final_factor = hourly_profile * day_multiplier * temp_multiplier + noise

    # Ефект інерції (Grid Momentum) - змішуємо нове значення з попереднім для плавності стрічки
    smoothed_factor = (final_factor * 0.8) + (previous_factor * 0.2)
    smoothed_factor = max(0.05, smoothed_factor)

    actual_load = float(capacity * smoothed_factor)

    # Генерація випадкових аварійних аномалій (Spikes/Dips)
    alert = None
    if random.random() < 0.001:
        actual_load *= random.uniform(1.2, 1.5)
        alert = ("Critical", "Раптовий стрибок навантаження (Transient Event)", "NEW")

    return round(actual_load, 2), alert


def calculate_transformer_health(
    actual_load: float,
    capacity: float,
    prev_health: float = 100.0
) -> Tuple[float, float, float]:
    """
    Розраховує діагностичні показники (температура масла, H2, здоров'я) 
    на основі поточного навантаження.
    """
    factor = actual_load / capacity if capacity > 0 else 0.5
    
    # 1. Температура масла (база 50 C + приріст від навантаження)
    base_temp = 50.0 + (factor * 30.0)
    temperature_c = round(base_temp + random.uniform(-2.0, 2.0), 1)

    # 2. Вміст водню H2 (ppm)
    base_h2 = 10.0 + (factor * 20.0)
    if factor > 1.1: # Перевантаження
        base_h2 += random.uniform(10.0, 25.0)
    h2_ppm = round(base_h2 + random.uniform(-1.0, 1.0), 1)

    # 3. Health Score (0-100)
    target_health = 100.0
    if temperature_c > 75.0:
        target_health -= (temperature_c - 75.0) * 0.5
    if h2_ppm > 50.0:
        target_health -= (h2_ppm - 50.0) * 0.1
    if factor > 1.0:
        target_health -= (factor - 1.0) * 5.0

    # Плавне відновлення/деградація здоров'я
    if target_health > prev_health:
        new_h = min(target_health, prev_health + 5.0)
    else:
        new_h = target_health

    final_health = max(0.0, min(round(new_h, 1), 100.0))
    
    return temperature_c, h2_ppm, final_health


def calculate_generator_output(
    gen_type: str, max_mw: float, ts: datetime.datetime
) -> float:
    """
    Розрахунок генерації з урахуванням хмарності та вітру.
    """
    hour = ts.hour
    minute = ts.minute
    time_val = hour + minute / 60.0

    if gen_type == "solar":
        if 6 <= time_val <= 19:
            # Плавна крива сонця
            sun_pos = np.sin((time_val - 6) * np.pi / 13)
            # Хмарність (випадково змінюється)
            cloud_impact = random.uniform(0.6, 1.0)
            return float(max_mw * sun_pos * cloud_impact)
        return 0.0

    if gen_type == "wind":
        # Вітер зазвичай сильніший вночі та вранці
        base_wind = 7.0 + 4.0 * np.cos(time_val * np.pi / 12)
        wind_speed = max(0, base_wind + np.random.normal(0, 2.0))
        # Спрощена крива потужності
        if 3.5 < wind_speed < 25:
            eff = (wind_speed - 3.5) / 10.0
            return float(max_mw * min(1.0, eff))
        return 0.0

    if gen_type == "nuclear":
        # АЕС працюють в базі, але мають мікро-коливання
        return float(max_mw * (0.98 + random.uniform(-0.005, 0.005)))

    if gen_type == "thermal":
        # ТЕС підлаштовуються під графік, але з затримкою
        load_ref = LOAD_PROFILES["RESIDENTIAL"].get(hour, 0.5)
        return float(max_mw * load_ref * random.uniform(0.85, 1.0))

    return float(max_mw * 0.5)
