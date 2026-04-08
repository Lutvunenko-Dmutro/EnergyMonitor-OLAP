import pytest
import os
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
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
