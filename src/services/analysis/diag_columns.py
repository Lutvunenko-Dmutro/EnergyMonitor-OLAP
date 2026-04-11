import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def check_columns():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM LoadMeasurements LIMIT 0")
        colnames = [desc[0] for desc in cur.description]
        print(f"COLUMNS: {colnames}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    check_columns()
