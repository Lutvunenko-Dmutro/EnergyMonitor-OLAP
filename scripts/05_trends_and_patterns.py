import os
import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
from contextlib import contextmanager
import psycopg2
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---
load_dotenv()

# Налаштування стилю графіків
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

# --- 2. DATABASE HELPER ---
@contextmanager
def get_db_connection():
    """Безпечне підключення до БД (як у генераторі)."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except Exception as e:
        logger.error(f"Помилка БД: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_data(query: str) -> pd.DataFrame:
    """Виконує SQL-запит і повертає Pandas DataFrame."""
    with get_db_connection() as conn:
        return pd.read_sql_query(query, conn)

# --- 3. ANALYSIS FUNCTIONS (Декомпозиція) ---

def analyze_consumption_trends():
    """Аналіз трендів споживання (Innovators/Early Adopters)."""
    logger.info("📈 Аналіз трендів споживання...")

    sql = """
    SELECT 
        s.substation_name,
        EXTRACT(WEEK FROM l.timestamp) as week_num,
        AVG(l.actual_load_mw) as avg_load
    FROM LoadMeasurements l
    JOIN Substations s ON l.substation_id = s.substation_id
    GROUP BY s.substation_name, week_num
    ORDER BY s.substation_name, week_num;
    """
    df = get_data(sql)

    if df.empty:
        logger.warning("Немає даних для аналізу трендів.")
        return

    # Візуалізація
    plt.figure(figsize=(14, 7))
    sns.lineplot(
        data=df, 
        x='week_num', 
        y='avg_load', 
        hue='substation_name', 
        marker='o', 
        palette='tab10',
        linewidth=2.5
    )
    
    plt.title('Динаміка середнього навантаження по тижнях', fontsize=16)
    plt.xlabel('Номер тижня', fontsize=12)
    plt.ylabel('Середнє навантаження (МВт)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    
    filename = 'trends_innovators.png'
    plt.savefig(filename)
    logger.info(f"✅ Графік збережено: {filename}")

def analyze_cascading_failures():
    """Пошук асоціативних правил та побудова теплової карти кореляцій."""
    logger.info("🔗 Аналіз каскадних аварій...")

    sql = """
    SELECT 
        date_trunc('hour', timestamp) as alert_time,
        s.substation_name
    FROM Alerts a
    JOIN Substations s ON a.substation_id = s.substation_id
    WHERE a.alert_type = 'Перевантаження'
    GROUP BY alert_time, s.substation_name;
    """
    df = get_data(sql)

    if df.empty:
        logger.warning("Немає даних про аварії.")
        return

    # Групуємо: Час -> Список підстанцій
    baskets = df.groupby('alert_time')['substation_name'].apply(list).values

    # Рахуємо пари
    pair_counts = Counter()
    all_substations = set()

    for basket in baskets:
        unique_subs = sorted(list(set(basket))) # Прибираємо дублі всередині однієї години
        all_substations.update(unique_subs)
        if len(unique_subs) > 1:
            pair_counts.update(combinations(unique_subs, 2))

    # Вивід текстового звіту
    print("\n" + "="*50)
    print(" ТОП-5 ПАР ПІДСТАНЦІЙ (Спільні аварії)")
    print("="*50)
    top_pairs = pair_counts.most_common(5)
    for (s1, s2), count in top_pairs:
        print(f"{s1:<25} + {s2:<25} | {count} разів")

    # --- ВІЗУАЛІЗАЦІЯ: ТЕПЛОВА КАРТА (Heatmap) ---
    subs_list = sorted(list(all_substations))
    matrix = pd.DataFrame(0, index=subs_list, columns=subs_list)

    for (s1, s2), count in pair_counts.items():
        matrix.loc[s1, s2] = count
        matrix.loc[s2, s1] = count # Симетрично

    if not matrix.empty and matrix.sum().sum() > 0:
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            matrix, 
            annot=True, 
            fmt="d", 
            cmap="Reds", 
            linewidths=.5,
            cbar_kws={'label': 'Кількість спільних інцидентів'}
        )
        plt.title('Матриця кореляції аварій (Хто падає разом?)', fontsize=16)
        plt.tight_layout()
        
        filename = 'heatmap_failures.png'
        plt.savefig(filename)
        logger.info(f"✅ Теплову карту збережено: {filename}")
    else:
        logger.info("Недостатньо даних для теплової карти.")

# --- 4. MAIN ---
if __name__ == "__main__":
    try:
        analyze_consumption_trends()
        analyze_cascading_failures()
        logger.info("🏁 Аналіз завершено успішно.")
    except Exception as e:
        logger.error(f"Критична помилка: {e}")
