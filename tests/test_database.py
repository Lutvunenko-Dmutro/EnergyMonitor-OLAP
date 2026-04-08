import pytest
from sqlalchemy import text

def test_db_connection(db_engine):
    """Перевірка з'єднання з базою даних."""
    with db_engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).fetchone()
        assert result[0] == 1

def test_schema_integrity(db_engine):
    """Перевірка наявності основних таблиць у схемі."""
    tables = ["regions", "substations", "loadmeasurements", "generators", "alerts"]
    with db_engine.connect() as conn:
        for table in tables:
            query = text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :table)")
            result = conn.execute(query, {"table": table}).fetchone()
            assert result[0] is True, f"Таблиця {table} відсутня в схемі"

def test_static_data_presence(db_session):
    """Перевірка наявності еталонних даних (Static Data)."""
    # Перевіряємо ПС Київська-Центральна (ID 10 згідно зі схемою)
    res = db_session.execute(text("SELECT substation_name, capacity_mw FROM Substations WHERE substation_id = 10")).fetchone()
    assert res is not None, "Еталонна підстанція з ID 10 не знайдена"
    assert res[0] == 'ПС Київська-Центральна'
    assert float(res[1]) == 1500.0

def test_load_measurements_stats(db_session):
    """Перевірка наявності часових рядів (OLAP-базис)."""
    res = db_session.execute(text("SELECT COUNT(*) FROM LoadMeasurements")).fetchone()
    assert res[0] >= 0  # База може бути новою, але таблиця має бути доступна
    
    # Якщо дані є, перевіримо один запис
    if res[0] > 0:
        sample = db_session.execute(text("SELECT actual_load_mw FROM LoadMeasurements LIMIT 1")).fetchone()
        assert sample[0] is not None
