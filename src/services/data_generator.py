import os
import random
import time
from datetime import datetime
from typing import Optional

import pandas as pd
from psycopg2.extras import execute_values

from src.core.config import END_DATE, FREQ, LOAD_PROFILES, START_DATE
from src.core.database import execute_sql_file, get_db_cursor
from src.core.logger import setup_logger
from src.core.physics import (
    calculate_energy_price,
    calculate_generator_output,
    calculate_substation_load,
    calculate_weather,
)

logger = setup_logger(__name__)

# Реалістичні потужності для конкретних підстанцій
BASE_CAPACITY_MAP = {
    "ПС Північна (Київ)": 1500.0,
    "ПС Дніпровська-750": 2000.0,
    "ПС Західна (Львів)": 800.0,
    "ПС Бровари": 50.0,
    "ПС Полтава-Центр": 120.0,
    "ПС Черкаси": 150.0,
    "ПС Вінниця": 250.0,
    "ПС Слобожанська (Харків)": 1200.0,
    "ПС Портова (Одеса)": 950.0,
    "ПС Запорізька": 3200.0,
}


def generate_professional_data():
    """
    Головний конвеєр генерації даних (Main ETL Pipeline).
    """
    logger.info("Початок процесу генерації даних...")

    with get_db_cursor() as (conn, cursor):
        logger.info("🧹 Очищення бази: видалення старих часових рядів...")

        tables_to_truncate = [
            "LoadMeasurements",
            "GenerationMeasurements",
            "WeatherReports",
            "EnergyPricing",
            "LineMeasurements",
            "Alerts",
        ]
        cursor.execute(f"TRUNCATE TABLE {', '.join(tables_to_truncate)} CASCADE;")

        cursor.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'substations');"
        )
        if not cursor.fetchone()[0]:
            logger.info("🏗️ Реєструємо відсутню схему бази даних (First Run)...")
            # Визначаємо шлях до папки sql відносно кореня проекту
            sql_dir = os.path.join(os.getcwd(), "sql")
            execute_sql_file(cursor, os.path.join(sql_dir, "01_create_schema.sql"))
            execute_sql_file(cursor, os.path.join(sql_dir, "02_insert_static_data.sql"))

        cursor.execute(
            "SELECT substation_id, substation_name, capacity_mw, region_id FROM Substations"
        )
        substations = cursor.fetchall()

        cursor.execute(
            "SELECT generator_id, generator_type, max_output_mw FROM Generators"
        )
        generators = cursor.fetchall()

        cursor.execute("SELECT line_id, max_load_mw FROM PowerLines")
        lines = cursor.fetchall()

        cursor.execute("SELECT region_id FROM Regions")
        regions = [r[0] for r in cursor.fetchall()]

        sub_profiles = {}
        for sub in substations:
            sid = sub[0]
            # Детермінований вибір профілю на основі ID
            if sid % 3 == 0:
                sub_profiles[sid] = "RESIDENTIAL"
            elif sid % 3 == 1:
                sub_profiles[sid] = "INDUSTRIAL"
            else:
                sub_profiles[sid] = "COMMERCIAL"

        logger.info(
            f"🚀 Генерація серії даних: {START_DATE.date()} -> {END_DATE.date()}"
        )

        timestamps = pd.date_range(START_DATE, END_DATE, freq=FREQ)

        data_weather, data_prices, data_loads = [], [], []
        data_generation, data_lines, data_alerts = [], [], []

        current_temps = dict.fromkeys(regions, 10.0)
        previous_factors = {sub[0]: 0.5 for sub in substations}
        current_health = {
            sub[0]: 100.0 for sub in substations
        }  # Показник для відновлення працездатності

        for ts in timestamps:
            hour = ts.hour
            is_weekend = ts.weekday() >= 5

            weather_map = calculate_weather(ts, current_temps)

            for rid in regions:
                temp, cond = weather_map[rid]
                data_weather.append((ts, rid, temp, cond))
                price = calculate_energy_price(hour, is_weekend, rid)
                data_prices.append((ts, rid, price))

            for sid, sname, _cap, rid in substations:
                # Перевизначаємо ліміт реалістичним словником, якщо є
                cap = BASE_CAPACITY_MAP.get(sname, float(_cap))
                p_type = sub_profiles[sid]
                temp, _ = weather_map[rid]
                prev_f = previous_factors[sid]
                actual_load, alert_info = calculate_substation_load(
                    float(cap), p_type, ts, temp, is_weekend, prev_f
                )

                # Оновлюємо фактор для наступного кроку (інерція)
                cap_f = float(cap) if cap else 100.0
                previous_factors[sid] = actual_load / cap_f if cap_f > 0 else 0.5
                factor = previous_factors[sid]

                # Розрахунок апаратних метрик
                base_temp = 50.0 + (factor * 30.0)
                temperature_c = round(base_temp + random.uniform(-2.0, 2.0), 1)

                base_h2 = 10.0 + (factor * 20.0)
                if factor > 1.1:
                    base_h2 += random.uniform(10.0, 25.0)  # Збалансовано (10-25)
                h2_ppm = round(base_h2 + random.uniform(-1.0, 1.0), 1)

                target_health = 100.0
                if temperature_c > 75.0:
                    target_health -= (temperature_c - 75.0) * 0.5  # 0.5 замість 2.0
                if h2_ppm > 50.0:
                    target_health -= (h2_ppm - 50.0) * 0.1  # 0.1 замість 0.5
                if factor > 1.0:
                    target_health -= (factor - 1.0) * 5.0

                prev_h = current_health[sid]
                # Стабілізація: приріст до +5% за годину
                if target_health > prev_h:
                    new_h = min(target_health, prev_h + 5.0)
                else:
                    new_h = target_health  # Падіння миттєве

                current_health[sid] = max(0.0, min(round(new_h, 1), 100.0))
                health_score = current_health[sid]

                data_loads.append(
                    (ts, actual_load, sid, temperature_c, h2_ppm, health_score)
                )

                if alert_info:
                    a_type, a_desc, a_status = alert_info
                    data_alerts.append((ts, a_type, a_desc, sid, a_status))

            for gid, gtype, max_g in generators:
                gen_val = calculate_generator_output(gtype, float(max_g), ts)
                data_generation.append((ts, round(gen_val, 2), gid))

            for lid, max_l in lines:
                line_load = (
                    float(max_l)
                    * LOAD_PROFILES["RESIDENTIAL"].get(hour, 0.5)
                    * random.uniform(0.6, 0.9)
                )
                data_lines.append((ts, round(line_load, 2), lid))

        logger.info("💾 Запис даних у базу (Batch Insert)...")

        insert_map = [
            (
                "WeatherReports",
                "timestamp, region_id, temperature, conditions",
                data_weather,
            ),
            ("EnergyPricing", "timestamp, region_id, price_per_mwh", data_prices),
            (
                "LoadMeasurements",
                "timestamp, actual_load_mw, substation_id, temperature_c, h2_ppm, health_score",
                data_loads,
            ),
            (
                "GenerationMeasurements",
                "timestamp, actual_generation_mw, generator_id",
                data_generation,
            ),
            ("LineMeasurements", "timestamp, actual_load_mw, line_id", data_lines),
        ]

        for table, columns, data in insert_map:
            query = f"INSERT INTO {table} ({columns}) VALUES %s"
            execute_values(cursor, query, data)

        if data_alerts:
            query_alerts = "INSERT INTO Alerts (timestamp, alert_type, description, substation_id, status) VALUES %s"
            execute_values(cursor, query_alerts, data_alerts)

    logger.info(f"✅ Успішно! Згенеровано {len(data_loads)} записів навантаження.")
    return sub_profiles, current_temps


def run_realtime_sensors(
    sub_profiles: Optional[dict] = None, current_temps: Optional[dict] = None
):
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

        cursor.execute(
            "SELECT substation_id, substation_name, capacity_mw, region_id FROM Substations"
        )
        substations = cursor.fetchall()
        logger.info(f"Знайдено підстанцій для моніторингу: {len(substations)}\n")

        if sub_profiles is None:
            sub_profiles = {sub[0]: "RESIDENTIAL" for sub in substations}

        # Ініціалізуємо фактори для інерції (Grid Momentum)
        previous_factors = {sub[0]: 0.5 for sub in substations}
        current_health = {
            sub[0]: 100.0 for sub in substations
        }  # Показник для відновлення працездатності

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

            print(
                f"\n[{now.strftime('%H:%M:%S')}] ⏳ Початок циклу (Година: {current_hour}:00)..."
            )

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

                    # Використовуємо нову фізику з часом (now) та інерцією (prev_f)
                    actual_load, alert_info = calculate_substation_load(
                        float(cap), p_type, now, temp, is_weekend, prev_f
                    )

                    # Оновлюємо фактор для наступного кроку
                    cap = float(cap) if cap else 100.0
                    previous_factors[sub_id] = actual_load / cap if cap > 0 else 0.5
                    factor = previous_factors[sub_id]

                    round(
                        random.uniform(320.0, 340.0)
                        if cap > 1000
                        else random.uniform(105.0, 115.0),
                        1,
                    )
                    round(random.uniform(49.85, 50.15), 2)

                    base_temp = 50.0 + (factor * 30.0)
                    temperature_c = round(base_temp + random.uniform(-2.0, 2.0), 1)

                    base_h2 = 10.0 + (factor * 20.0)
                    if factor > 1.1:
                        base_h2 += random.uniform(10.0, 25.0)  # Збалансовано (10-25)
                    h2_ppm = round(base_h2 + random.uniform(-1.0, 1.0), 1)

                    target_health = 100.0
                    if temperature_c > 75.0:
                        target_health -= (temperature_c - 75.0) * 0.5  # 0.5 замість 2.0
                    if h2_ppm > 50.0:
                        target_health -= (h2_ppm - 50.0) * 0.1  # 0.1 замість 0.5
                    if factor > 1.0:
                        target_health -= (factor - 1.0) * 5.0

                    prev_h = current_health.get(sub_id, 100.0)
                    # Стабілізація: приріст до +5% за цикл
                    if target_health > prev_h:
                        new_h = min(target_health, prev_h + 5.0)
                    else:
                        new_h = target_health  # Падіння миттєве

                    current_health[sub_id] = max(0.0, min(round(new_h, 1), 100.0))
                    health_score = current_health[sub_id]


                    # Прибираємо подвійне "ПС", якщо воно вже є в назві
                    clean_name = name.replace("ПС ПС", "ПС").replace("ПС ", "")
                    print(
                        f"   ⚡ [ПС {clean_name}] {p_type} | Load: {actual_load} MW, Здоров'я: {health_score}% (T: {temperature_c:.1f}°C)"
                    )

                    query = """
                        INSERT INTO LoadMeasurements 
                        (timestamp, substation_id, actual_load_mw, temperature_c, h2_ppm, health_score)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(
                        query,
                        (now, sub_id, actual_load, temperature_c, h2_ppm, health_score),
                    )

                conn.commit()
                print(
                    f"[{now.strftime('%H:%M:%S')}] ✅ Всі {len(substations)} записів успішно збережено.\n"
                )

            time.sleep(5)

    except Exception as e:
        logger.critical(f"❌ КРИТИЧНА ПОМИЛКА: {e}", exc_info=True)


if __name__ == "__main__":
    import sys

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
