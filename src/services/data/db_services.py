import random
import datetime
import pandas as pd
from sqlalchemy import text
from src.core.database import run_query, execute_update, get_engine
from src.core.logger import setup_logger

log = setup_logger(__name__)

def get_latest_measurements() -> pd.DataFrame:
    """
    Отримує останній запис телеметрії для кожної підстанції.
    Автоматично розраховує віртуальні показники (voltage, health, temp).
    """
    query = """
        SELECT DISTINCT ON (m.substation_id) 
            m.timestamp, 
            m.substation_id, 
            s.substation_name,
            s.capacity_mw,
            m.actual_load_mw,
            m.temperature_c,
            m.h2_ppm,
            m.health_score
        FROM LoadMeasurements m
        JOIN Substations s ON m.substation_id = s.substation_id
        ORDER BY m.substation_id, m.timestamp DESC
    """
    df = run_query(query)

    if df.empty:
        return df

    def calculate_synthetic_electrical(row):
        cap = float(row["capacity_mw"]) if row["capacity_mw"] else 100.0
        voltage = round(random.uniform(325.0, 335.0) if cap > 1000 else random.uniform(108.0, 112.0), 1)
        freq = round(random.uniform(49.95, 50.05), 2)
        return pd.Series([voltage, freq])

    cols = ["voltage_kv", "frequency_hz"]
    df[cols] = df.apply(calculate_synthetic_electrical, axis=1)

    return df

def create_custom_alert(sub_name: str, alert_type: str, description: str) -> tuple[bool, str]:
    """Створює нову аварію."""
    engine = get_engine()
    try:
        with engine.begin() as conn:
            res = conn.execute(
                text("SELECT substation_id FROM Substations WHERE substation_name = :name"),
                {"name": sub_name},
            ).fetchone()

            if not res:
                return False, f"Підстанцію '{sub_name}' не знайдено!"

            sub_id = res[0]
            sql = """
                INSERT INTO Alerts (timestamp, alert_type, description, substation_id, status)
                VALUES (:ts, :type, :desc, :sub_id, 'NEW')
            """
            params = {
                "ts": datetime.datetime.now(),
                "type": alert_type,
                "desc": description,
                "sub_id": sub_id,
            }
            conn.execute(text(sql), params)
        return True, "Інцидент успішно створено!"
    except Exception as e:
        log.error(f"Помилка бази даних: {e}", exc_info=True)
        return False, f"Помилка БД: {e}"

def update_alert_status(alert_id, new_status: str):
    """Оновлює статус існуючої аварії."""
    sql = "UPDATE Alerts SET status = :status WHERE alert_id = :id"
    execute_update(sql, {"status": new_status, "id": int(alert_id)})

def delete_alert(alert_id: int):
    """Видаляє конкретний запис за ID."""
    sql = "DELETE FROM Alerts WHERE alert_id = :id"
    execute_update(sql, {"id": int(alert_id)})

def cleanup_old_alerts(keep_last: int = 10) -> bool:
    """Видаляє старі записи, залишаючи N останніх."""
    engine = get_engine()
    try:
        with engine.connect() as conn:
            res = conn.execute(
                text("SELECT alert_id FROM Alerts ORDER BY alert_id DESC LIMIT :lim"),
                {"lim": keep_last},
            ).fetchall()
            keep_ids = [row[0] for row in res]

        if not keep_ids:
            return True

        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM Alerts WHERE alert_id NOT IN :ids"),
                {"ids": tuple(keep_ids)},
            )
        return True
    except Exception as e:
        log.error(f"Помилка очищення: {e}", exc_info=True)
        return False
