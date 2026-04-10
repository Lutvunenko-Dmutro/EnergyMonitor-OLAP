import pytest
import os
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime, timedelta

from core.database.loader import fetch_granular_data
from src.core.database import get_engine
from src.core.config import DB_CONFIG

@pytest.fixture(scope="session")
def db_engine():
    """Fixture for SQLAlchemy engine."""
    engine = get_engine()
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    """Fixture for isolated SQLAlchemy session (rolls back after each test)."""
    connection = db_engine.connect()
    transaction = connection.begin()
    
    Session = sessionmaker(bind=connection)
    session = Session()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def db_cursor():
    """Fixture for isolated psycopg2 cursor (rolls back after each test)."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    yield cursor
    
    conn.rollback()
    conn.close()


# ───────────────────────────────────────────────────────────────
# DATA FIXTURES
# ───────────────────────────────────────────────────────────────

@pytest.fixture
def sample_dataframe():
    """Створює sample DataFrame для тестування."""
    dates = [datetime(2024, 1, 1) + timedelta(hours=i) for i in range(24)]
    return pd.DataFrame({
        'timestamp': dates,
        'region_name': ['Київ'] * 24,
        'substation_name': ['Київ ТЕС'] * 24,
        'load': [100 + i*2 for i in range(24)],
        'gen': [95 + i*1.5 for i in range(24)],
        'actual_load_mw': [100 + i*2 for i in range(24)],
        'health_score': [0.9] * 24,
    })


@pytest.fixture
def sample_forecast_data():
    """Sample даних для LSTM предиктору."""
    import numpy as np
    return np.random.randn(24, 9).astype(np.float32)


@pytest.fixture
def empty_dataframe():
    """Порожний DataFrame для edge case тестування."""
    return pd.DataFrame()


@pytest.fixture
def date_range():
    """Кортеж дат для фільтрації."""
    return (datetime(2024, 1, 1).date(), datetime(2024, 1, 31).date())
