# ATLAS_PASSPORT: docs/system/map/migrate_db.md
"""
СИСТЕМА ЕВОЛЮЦІЇ СХЕМИ БАЗИ ДАНИХ (Database Migration Engine)
============================================================
Модуль забезпечує автоматичне оновлення структури БД для підтримки аналітики.
Ключові можливості:
1. Digital Twin Expansion: розширення таблиць фізичними параметрами (напруга, частота, H2).
2. Idempotent Updates: використання конструкцій IF NOT EXISTS для безпечних оновлень.
3. ML Compatibility: синхронізація схеми телеметрії з вимогами моделей V2 та V3.
Забезпечує актуальність структури даних при розширенні функціоналу системи.
"""
from src.core.database import execute_update


def migrate():
    print("Running DB Migration: Adding missing Digital Twin columns...")

    queries = [
        "ALTER TABLE LoadMeasurements ADD COLUMN IF NOT EXISTS voltage_kv DECIMAL(10, 2);",
        "ALTER TABLE LoadMeasurements ADD COLUMN IF NOT EXISTS frequency_hz DECIMAL(10, 2);",
        "ALTER TABLE LoadMeasurements ADD COLUMN IF NOT EXISTS temperature_c DECIMAL(10, 2);",
        "ALTER TABLE LoadMeasurements ADD COLUMN IF NOT EXISTS h2_ppm DECIMAL(10, 2);",
        "ALTER TABLE LoadMeasurements ADD COLUMN IF NOT EXISTS health_score DECIMAL(10, 2);",
        "ALTER TABLE LoadMeasurements ADD COLUMN IF NOT EXISTS sensor_status VARCHAR(50);",
    ]

    for q in queries:
        success = execute_update(q)
        print(f"Executed: {q} -> {'SUCCESS' if success else 'FAILED'}")


if __name__ == "__main__":
    migrate()
    print("Migration complete.")
