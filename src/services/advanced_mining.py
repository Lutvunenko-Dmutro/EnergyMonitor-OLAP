import logging
import os
from contextlib import contextmanager

import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import seaborn as sns
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree

# --- 1. CONFIGURATION ---
load_dotenv()

# Стилізація графіків
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 8)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}


# --- 2. DATABASE HELPER ---
@contextmanager
def get_db_connection():
    """Безпечне підключення до БД."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except Exception as e:
        logger.error(f"Помилка підключення до БД: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_data(query: str) -> pd.DataFrame:
    """Отримання даних у DataFrame."""
    with get_db_connection() as conn:
        return pd.read_sql_query(query, conn)


# --- 3. ML FUNCTIONS ---


def run_clustering_analysis():
    """Кластеризація підстанцій (K-Means)."""
    logger.info("🔄 Запуск кластеризації (K-Means)...")

    sql = """
    SELECT 
        s.substation_name,
        AVG(l.actual_load_mw) as avg_load,
        STDDEV(l.actual_load_mw) as load_volatility,
        COUNT(a.alert_id) as alert_count
    FROM Substations s
    LEFT JOIN LoadMeasurements l ON s.substation_id = l.substation_id
    LEFT JOIN Alerts a ON s.substation_id = a.substation_id
    GROUP BY s.substation_name;
    """
    df = get_data(sql)
    # [FIX]: Використовуємо replace для числових колонок, щоб не тригерети діагностику Categorical
    num_cols = df.select_dtypes(include=['number']).columns
    df[num_cols] = df[num_cols].replace({np.nan: 0, None: 0})

    if df.empty:
        logger.warning("Немає даних для кластеризації.")
        return

    # Нормалізація
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(df[["avg_load", "load_volatility", "alert_count"]])

    # K-Means (n_clusters=3)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(x_scaled)

    # Візуалізація
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=df,
        x="avg_load",
        y="alert_count",
        hue="Cluster",
        palette="viridis",
        s=150,
        edgecolor="black",
    )
    plt.title("Кластеризація Підстанцій: Навантаження vs Аварійність", fontsize=16)
    plt.xlabel("Середнє навантаження (МВт)")
    plt.ylabel("Кількість аварій")
    plt.grid(True, linestyle="--", alpha=0.7)

    filename = "clustering_result.png"
    plt.savefig(filename)
    logger.info(f"✅ Графік кластеризації збережено: {filename}")

    # Вивід опису кластерів
    logger.info("Середні показники по кластерах:")
    print(df.groupby("Cluster")[["avg_load", "alert_count"]].mean())


def run_classification_prediction():
    """Побудова дерева рішень (Decision Tree) з КОМПАКТНИМ дизайном."""
    logger.info("🔄 Запуск прогнозування (Decision Tree)...")

    sql = """
    SELECT 
        EXTRACT(HOUR FROM l.timestamp) as hour_of_day,
        w.temperature,
        CASE WHEN (l.actual_load_mw / s.capacity_mw) > 0.95 THEN 1 ELSE 0 END as is_critical
    FROM LoadMeasurements l
    JOIN Substations s ON l.substation_id = s.substation_id
    JOIN WeatherReports w ON l.timestamp = w.timestamp AND s.region_id = w.region_id
    LIMIT 50000;
    """
    df = get_data(sql)

    if df.empty or df["is_critical"].sum() == 0:
        logger.warning("Недостатньо даних (або аварійних станів) для навчання моделі.")
        return

    x = df[["hour_of_day", "temperature"]]
    y = df["is_critical"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=42
    )

    clf = DecisionTreeClassifier(max_depth=3, random_state=42, class_weight="balanced")
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)
    print("\n--- Звіт класифікації ---")
    print(classification_report(y_test, y_pred, zero_division=0))

    # --- ВІЗУАЛІЗАЦІЯ (COMPACT STYLE) ---
    plt.figure(figsize=(12, 6), dpi=300)

    plot_tree(
        clf,
        feature_names=["Година", "Темп. (°C)"],
        class_names=["Норма", "Аварія"],
        filled=True,
        rounded=True,
        impurity=False,
        proportion=False,
        precision=1,
        fontsize=10,
        node_ids=False,
        label="root",
    )

    plt.title("Модель прогнозування аварійних станів", fontsize=14, fontweight="bold")

    filename = "decision_tree.png"
    plt.savefig(filename, bbox_inches="tight", dpi=300)
    logger.info(f"✅ Компактне дерево збережено: {filename}")


# --- 4. MAIN ---
if __name__ == "__main__":
    try:
        run_clustering_analysis()
        run_classification_prediction()
        logger.info("🏁 ML аналіз завершено успішно.")
    except Exception as e:
        logger.critical(f"Критична помилка: {e}")
