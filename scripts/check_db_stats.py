import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_stats():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        
        # Database size
        cur.execute("SELECT pg_size_pretty(pg_database_size(%s))", (os.getenv("DB_NAME"),))
        db_size = cur.fetchone()[0]
        
        # Table sizes
        cur.execute("""
            SELECT
                relname AS "table_name",
                pg_size_pretty(pg_total_relation_size(relid)) AS "total_size"
            FROM pg_catalog.pg_statio_user_tables
            ORDER BY pg_total_relation_size(relid) DESC
            LIMIT 5;
        """)
        tables = cur.fetchall()
        
        print(f"Database: {os.getenv('DB_NAME')}")
        print(f"Total Size on Disk: {db_size}")
        print("\nTop 5 Largest Tables:")
        for table, size in tables:
            print(f"- {table}: {size}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_db_stats()
