import os
import sys
import time
import json
import random
from datetime import datetime
from pathlib import Path

import numpy as np
import psycopg2
from dotenv import load_dotenv

from src.core.config import DB_CONFIG
from src.core.physics import calculate_substation_load, calculate_transformer_health

load_dotenv()

# Шляхи до службових файлів
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
HEARTBEAT_FILE = LOGS_DIR / "heartbeat.txt"
LOCK_FILE = LOGS_DIR / "sensors.lock"
LIVE_STATE_FILE = LOGS_DIR / "live_state.json"
TIMEOUT_SECONDS = 120  # Авто-вимкнення

def run_cosmetic_collector():
    """
    Стабільний генератор для захисту диплому. 
    БЕЗ ШІ, БЕЗ запису в БД. Тільки "живий" транслятор стану.
    """
    if LOCK_FILE.exists():
        print(f"🛑 Error: Lock exists at {LOCK_FILE}")
        sys.exit(0)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT substation_id, substation_name, capacity_mw FROM Substations")
        substations = cur.fetchall()

        sub_profiles = {}
        prev_health = {}
        previous_factors = {}
        
        for sub in substations:
            sid = sub[0]
            prev_health[sid] = 95.4 # Базове здоров'я згідно запиту користувача
            previous_factors[sid] = 0.7
            sub_profiles[sid] = "RESIDENTIAL" if sid % 3 == 0 else ("INDUSTRIAL" if sid % 3 == 1 else "COMMERCIAL")

        print("-" * 50)
        print("🚀 LIVE MONITORING: COSMETIC MODE ACTIVE (No DB Writes)")
        print("-" * 50)

        while True:
            now = datetime.now()
            
            # Розрахунок глобальних метрик
            # Запит користувача: Health ~95.4%, Freq ~49.96 Hz, Total ~30,000 MW
            total_load = 0.0
            substation_states = []
            
            # Базова частота з невеликим коливанням
            frequency = 49.96 + random.uniform(-0.02, 0.04)

            for sub_id, name, capacity in substations:
                p_type = sub_profiles[sub_id]
                cap = float(capacity) if capacity else 100.0
                
                # Потужна "промислова" версія (множимо на коефіцієнт, щоб вийти на 30к МВт)
                # Сумарна потужність 12 підстанцій ~26.9к. Щоб мати стабільні 30к, множимо на 1.35
                boost_factor = 1.35
                actual_load, _ = calculate_substation_load(cap * boost_factor, p_type, now, 15.0, False, previous_factors[sub_id])
                
                # Діагностика
                temp_oil, h2, health = calculate_transformer_health(actual_load, cap * boost_factor, prev_health[sub_id])
                
                # Оновлюємо стани
                prev_health[sub_id] = health
                previous_factors[sub_id] = actual_load / (cap * boost_factor)
                total_load += actual_load
                
                substation_states.append({
                    "id": sub_id,
                    "name": name.replace("ПС ПС", "ПС"),
                    "load": round(actual_load, 2),
                    "health": round(health, 1),
                    "temp": round(temp_oil, 1),
                    "h2": round(h2, 1),
                    "voltage": 750.0 if "750" in name else (330.0 + random.uniform(-2, 2))
                })

            # Формуємо фінальний стан системи
            live_state = {
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "total_load_mw": round(total_load, 2),
                "avg_health_score": round(np.mean([s["health"] for s in substation_states]), 1),
                "frequency_hz": round(frequency, 2),
                "substations": substation_states
            }

            # Записуємо в JSON для UI (але НЕ в БД)
            with open(LIVE_STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(live_state, f, ensure_ascii=False, indent=2)

            print(f"[{now.strftime('%H:%M:%S')}] Глобальне навантаження: {total_load:.2f} MW | Freq: {frequency:.2f} Hz | JSON оновлено.")

            # Heartbeat check
            if HEARTBEAT_FILE.exists() and (time.time() - HEARTBEAT_FILE.stat().st_mtime) > TIMEOUT_SECONDS:
                print("💤 [AUTO-SHUTDOWN] Користувачі не активні. Вимикаюсь...")
                break
            elif not HEARTBEAT_FILE.exists():
                HEARTBEAT_FILE.touch()

            time.sleep(5)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn: conn.close()
        if LOCK_FILE.exists(): LOCK_FILE.unlink()
        if LIVE_STATE_FILE.exists(): LIVE_STATE_FILE.unlink() # Очищуємо стан при виході
        print("🛑 Collector stopped.")

if __name__ == "__main__":
    run_cosmetic_collector()
