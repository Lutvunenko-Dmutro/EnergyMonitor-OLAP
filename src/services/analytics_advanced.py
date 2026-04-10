"""
analytics_advanced.py — Автономний скрипт аналізу трендів та асоціативних правил.
Запускати ЛИШЕ як standalone: python -m src.services.analytics_advanced
"""
from collections import Counter
from itertools import combinations
import logging

import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

load_dotenv()
from src.core.database import run_query

logger = logging.getLogger(__name__)


def analyze_trends():
    """Аналіз трендів споживання (Early Adopters)."""
    logger.info("📈 Аналіз трендів (Early Adopters)...")

    sql_trends = """
SELECT 
    s.substation_name,
    EXTRACT(WEEK FROM l.timestamp) as week_num,
    AVG(l.actual_load_mw) as avg_load
FROM LoadMeasurements l
JOIN Substations s ON l.substation_id = s.substation_id
GROUP BY s.substation_name, week_num
ORDER BY s.substation_name, week_num;
"""
    df_trends = run_query(sql_trends)

    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=df_trends, x="week_num", y="avg_load", hue="substation_name", marker="o"
    )
    plt.title("Динаміка споживання: Виявлення зростаючих трендів")
    plt.xlabel("Номер тижня")
    plt.ylabel("Середнє навантаження (МВт)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("trends_innovators.png")
    logger.info("✅ Графік збережено як 'trends_innovators.png'")


def analyze_association_rules():
    """Пошук асоціативних правил (Каскадні аварії)."""
    logger.info("🔗 Пошук асоціативних правил (Frequent Patterns)...")

    sql_alerts = """
SELECT 
    date_trunc('hour', timestamp) as alert_time,
    s.substation_name
FROM Alerts a
JOIN Substations s ON a.substation_id = s.substation_id
WHERE a.alert_type = 'Перевантаження'
GROUP BY alert_time, s.substation_name;
"""
    df_alerts = run_query(sql_alerts)

    baskets = df_alerts.groupby("alert_time")["substation_name"].apply(list).values

    pair_counts = Counter()
    for basket in baskets:
        basket = sorted(basket)
        if len(basket) > 1:
            pairs = combinations(basket, 2)
            pair_counts.update(pairs)

    logger.info("--- ТОП-5 АСОЦІАТИВНИХ ПРАВИЛ (Каскадні аварії) ---")
    logger.info(f"{'Підстанція А':<30} + {'Підстанція Б':<30} | {'Кількість спільних аварій'}")
    logger.info("-" * 80)
    for (item1, item2), count in pair_counts.most_common(5):
        logger.info(f"{item1:<30} + {item2:<30} | {count}")

    logger.info(
        "Висновки: Ці пари підстанцій є структурно пов'язаними. "
        "Аварія на одній часто супроводжується аварією на іншій."
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
    analyze_trends()
    analyze_association_rules()
