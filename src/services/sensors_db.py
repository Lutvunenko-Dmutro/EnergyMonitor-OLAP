import time
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

from src.core.config import DB_CONFIG
from src.core.physics import calculate_substation_load

load_dotenv()


def run_production_collector():
    # Підключення до бази PostgreSQL через DB_CONFIG
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        "SELECT substation_id, substation_name, capacity_mw, region_id FROM Substations"
    )
    substations = cur.fetchall()

    # Детермінований вибір профілю на основі ID
    sub_profiles = {}
    previous_factors = {}
    for sub in substations:
        sid = sub[0]
        previous_factors[sid] = 0.5
        if sid % 3 == 0:
            sub_profiles[sid] = "RESIDENTIAL"
        elif sid % 3 == 1:
            sub_profiles[sid] = "INDUSTRIAL"
        else:
            sub_profiles[sid] = "COMMERCIAL"

    print("=" * 60)
    print("🚀 ENERGY MONITOR ULTIMATE: LIVE SENSORS STARTED")
    print("=" * 60)
    print(f"Знайдено підстанцій для моніторингу: {len(substations)}\n")

    try:
        while True:
            now = datetime.now()
            is_weekend = now.weekday() >= 5

            # Температура (заглушка 15 градусів, якщо немає WeatherReports)
            temp = 15.0

            print(f"[{now.strftime('%H:%M:%S')}] ⏳ Початок циклу опитування...")

            for sub_id, name, capacity, rid in substations:
                p_type = sub_profiles[sub_id]
                cap = float(capacity) if capacity else 100.0
                prev_f = previous_factors[sub_id]

                # Використовуємо уніфіковану фізику з інерцією
                actual_load, alert = calculate_substation_load(
                    cap, p_type, now, temp, is_weekend, prev_f
                )

                # Оновлюємо фактор для наступного кроку
                previous_factors[sub_id] = actual_load / cap if cap > 0 else 0.5

                # Прибираємо подвійне "ПС", якщо воно вже є в назві
                clean_name = name.replace("ПС ПС", "ПС").replace("ПС ", "")

                # Логування
                alert_flag = "⚠️" if alert else "⚡"
                print(
                    f"   {alert_flag} [ПС {clean_name}] {p_type} | Навантаження: {actual_load} MW (Фактор: {actual_load / cap:.2f})"
                )

                # Запис у БД
                query = """
                    INSERT INTO LoadMeasurements 
                    (timestamp, substation_id, actual_load_mw)
                    VALUES (%s, %s, %s)
                """
                cur.execute(query, (now, sub_id, actual_load))

            conn.commit()
            print(
                f"[{now.strftime('%H:%M:%S')}] ✅ Всі {len(substations)} записів успішно збережено в БД.\n"
            )

            time.sleep(5)

    except Exception as e:
        print(f"\n❌ КРИТИЧНА ПОМИЛКА: {e}")
    finally:
        cur.close()
        conn.close()
        print("🛑 Роботу колектора завершено, з'єднання закрито.")


if __name__ == "__main__":
    run_production_collector()
