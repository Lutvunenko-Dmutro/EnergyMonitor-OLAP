import os
import random
import pandas as pd
from psycopg2.extras import execute_values

from src.core.config import END_DATE, FREQ, LOAD_PROFILES, START_DATE
from src.core.database import execute_sql_file, get_db_cursor
from src.core.logger import setup_logger
from src.core.physics import (
    calculate_energy_price,
    calculate_generator_output,
    calculate_substation_load,
    calculate_transformer_health,
    calculate_weather,
)
from src.services.generator_constants import BASE_CAPACITY_MAP

logger = setup_logger(__name__)

def generate_professional_data():
    """
    Головний конвеєр генерації даних (Main ETL Pipeline).
    Seed the database with historical data.
    """
    logger.info("Початок процесу генерації даних...")

    with get_db_cursor() as (conn, cursor):
        cursor.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'substations');"
        )
        schema_exists = cursor.fetchone()[0]

        if not schema_exists:
            logger.info("🏗️ Реєструємо відсутню схему бази даних (First Run)...")
            sql_dir = os.path.join(os.getcwd(), "sql")
            execute_sql_file(cursor, os.path.join(sql_dir, "01_create_schema.sql"))
            execute_sql_file(cursor, os.path.join(sql_dir, "02_insert_static_data.sql"))
        else:
            logger.info("🧹 Очищення бази: видалення старих часових рядів...")
            tables_to_truncate = [
                "LoadMeasurements", "GenerationMeasurements",
                "WeatherReports", "EnergyPricing",
                "LineMeasurements", "Alerts",
            ]
            cursor.execute(f"TRUNCATE TABLE {', '.join(tables_to_truncate)} CASCADE;")

        cursor.execute("SELECT substation_id, substation_name, capacity_mw, region_id FROM Substations")
        substations = cursor.fetchall()
        cursor.execute("SELECT generator_id, generator_type, max_output_mw FROM Generators")
        generators = cursor.fetchall()
        cursor.execute("SELECT line_id, max_load_mw FROM PowerLines")
        lines = cursor.fetchall()
        cursor.execute("SELECT region_id FROM Regions")
        regions = [r[0] for r in cursor.fetchall()]

        sub_profiles = {}
        for sub in substations:
            sid = sub[0]
            if sid % 3 == 0:
                sub_profiles[sid] = "RESIDENTIAL"
            elif sid % 3 == 1:
                sub_profiles[sid] = "INDUSTRIAL"
            else:
                sub_profiles[sid] = "COMMERCIAL"

        logger.info(f"🚀 Генерація серії даних: {START_DATE.date()} -> {END_DATE.date()}")
        timestamps = pd.date_range(START_DATE, END_DATE, freq=FREQ)

        data_weather, data_prices, data_loads = [], [], []
        data_generation, data_lines, data_alerts = [], [], []

        current_temps = dict.fromkeys(regions, 10.0)
        previous_factors = {sub[0]: 0.5 for sub in substations}
        current_health = {sub[0]: 100.0 for sub in substations}

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
                cap = BASE_CAPACITY_MAP.get(sname, float(_cap))
                p_type = sub_profiles[sid]
                temp, _ = weather_map[rid]
                prev_f = previous_factors[sid]
                actual_load, alert_info = calculate_substation_load(float(cap), p_type, ts, temp, is_weekend, prev_f)

                cap_f = float(cap) if cap else 100.0
                previous_factors[sid] = actual_load / cap_f if cap_f > 0 else 0.5
                
                # Використовуємо уніфіковану фізику здоров'я
                temperature_c, h2_ppm, health_score = calculate_transformer_health(
                    actual_load, cap_f, current_health[sid]
                )
                current_health[sid] = health_score

                data_loads.append((ts, actual_load, sid, temperature_c, h2_ppm, health_score))

                if alert_info:
                    a_type, a_desc, a_status = alert_info
                    data_alerts.append((ts, a_type, a_desc, sid, a_status))

            for gid, gtype, max_g in generators:
                gen_val = calculate_generator_output(gtype, float(max_g), ts)
                data_generation.append((ts, round(gen_val, 2), gid))

            for lid, max_l in lines:
                line_load = float(max_l) * LOAD_PROFILES["RESIDENTIAL"].get(hour, 0.5) * random.uniform(0.6, 0.9)
                data_lines.append((ts, round(line_load, 2), lid))

        logger.info("💾 Запис даних у базу (Batch Insert)...")

        insert_map = [
            ("WeatherReports", "timestamp, region_id, temperature, conditions", data_weather),
            ("EnergyPricing", "timestamp, region_id, price_per_mwh", data_prices),
            ("LoadMeasurements", "timestamp, actual_load_mw, substation_id, temperature_c, h2_ppm, health_score", data_loads),
            ("GenerationMeasurements", "timestamp, actual_generation_mw, generator_id", data_generation),
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
