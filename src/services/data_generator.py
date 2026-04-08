import os
import random
import time
from datetime import datetime
from typing import Optional

from src.core.database import get_db_cursor
from src.core.logger import setup_logger
from src.core.physics import calculate_substation_load, calculate_weather
from src.services.generator_constants import BASE_CAPACITY_MAP

logger = setup_logger(__name__)

def run_realtime_sensors(sub_profiles: Optional[dict] = None, current_temps: Optional[dict] = None):
    """
    Симуляція реального часу (Continuous Digital Twin).
    """
    logger.info("=" * 60)
    logger.info("🚀 DIGITAL TWIN REALTIME SIMULATION STARTED")
    logger.info("=" * 60)

    with get_db_cursor() as (conn, cursor):
        if not cursor:
            logger.error("❌ Не вдалося підключитися для отримання списку підстанцій.")
            return

        cursor.execute("SELECT substation_id, substation_name, capacity_mw, region_id FROM Substations")
        substations = cursor.fetchall()
        logger.info(f"Знайдено підстанцій для моніторингу: {len(substations)}\n")

        if sub_profiles is None:
            sub_profiles = {sub[0]: "RESIDENTIAL" for sub in substations}

        previous_factors = {sub[0]: 0.5 for sub in substations}
        current_health = {sub[0]: 100.0 for sub in substations}

        if current_temps is None:
            cursor.execute("SELECT region_id FROM Regions")
            regions = [r[0] for r in cursor.fetchall()]
            current_temps = dict.fromkeys(regions, 10.0)

    last_weather_hour = -1
    weather_map = {}

    try:
        while True:
            now = datetime.now()
            current_hour = now.hour
            is_weekend = now.weekday() >= 5

            if current_hour != last_weather_hour:
                weather_map = calculate_weather(now, current_temps)
                last_weather_hour = current_hour

            print(f"\n[{now.strftime('%H:%M:%S')}] ⏳ Початок циклу (Година: {current_hour}:00)...")

            with get_db_cursor() as (conn, cursor):
                if not cursor:
                    logger.error("❌ Втрачено з'єднання з БД в live-режимі.")
                    time.sleep(5)
                    continue

                for sub_id, name, _cap, region_id in substations:
                    cap = BASE_CAPACITY_MAP.get(name, float(_cap))
                    p_type = sub_profiles.get(sub_id, "RESIDENTIAL")
                    temp, _ = weather_map[region_id]
                    prev_f = previous_factors.get(sub_id, 0.5)

                    actual_load, alert_info = calculate_substation_load(float(cap), p_type, now, temp, is_weekend, prev_f)

                    cap_f = float(cap) if cap else 100.0
                    previous_factors[sub_id] = actual_load / cap_f if cap_f > 0 else 0.5
                    factor = previous_factors[sub_id]

                    base_temp = 50.0 + (factor * 30.0)
                    temperature_c = round(base_temp + random.uniform(-2.0, 2.0), 1)

                    base_h2 = 10.0 + (factor * 20.0)
                    if factor > 1.1:
                        base_h2 += random.uniform(10.0, 25.0)
                    h2_ppm = round(base_h2 + random.uniform(-1.0, 1.0), 1)

                    target_health = 100.0
                    if temperature_c > 75.0:
                        target_health -= (temperature_c - 75.0) * 0.5
                    if h2_ppm > 50.0:
                        target_health -= (h2_ppm - 50.0) * 0.1
                    if factor > 1.0:
                        target_health -= (factor - 1.0) * 5.0

                    prev_h = current_health.get(sub_id, 100.0)
                    if target_health > prev_h:
                        new_h = min(target_health, prev_h + 5.0)
                    else:
                        new_h = target_health

                    current_health[sub_id] = max(0.0, min(round(new_h, 1), 100.0))
                    health_score = current_health[sub_id]

                    clean_name = name.replace("ПС ПС", "ПС").replace("ПС ", "")
                    print(f"   ⚡ [ПС {clean_name}] {p_type} | Load: {actual_load} MW, Здоров'я: {health_score}% (T: {temperature_c:.1f}°C)")

                    query = """
                        INSERT INTO LoadMeasurements 
                        (timestamp, substation_id, actual_load_mw, temperature_c, h2_ppm, health_score)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (now, sub_id, actual_load, temperature_c, h2_ppm, health_score))

                conn.commit()
                print(f"[{now.strftime('%H:%M:%S')}] ✅ Всі {len(substations)} записів успішно збережено.\n")

            time.sleep(5)

    except Exception as e:
        logger.critical(f"❌ КРИТИЧНА ПОМИЛКА: {e}", exc_info=True)


if __name__ == "__main__":
    import sys
    from src.services.db_seeder import generate_professional_data

    try:
        logger.info("🎬 ЗАПУСК СИМУЛЯЦІЇ ЕНЕРГОСИСТЕМИ...")
        sub_profiles, current_temps = generate_professional_data()

        logger.info("✅ Історія завершена.")
        logger.info("⏳ Пауза 3 секунди перед стартом Live-режиму...")
        time.sleep(3)

        logger.info("🟢 Старт Live-режиму!")
        run_realtime_sensors(sub_profiles, current_temps)

    except KeyboardInterrupt:
        logger.warning("🛑 Виконання перервано користувачем (Ctrl+C).")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"🔥 КРИТИЧНА ПОМИЛКА: {e}", exc_info=True)
        sys.exit(1)
