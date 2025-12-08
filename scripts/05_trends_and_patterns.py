import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

def get_data(query):
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ==========================================
# ЧАСТИНА 1: ІННОВАТОРИ (ТРЕНДИ СПОЖИВАННЯ)
# ==========================================
print("📈 Аналіз трендів (Early Adopters)...")

# Беремо середнє навантаження по тижнях для кожної підстанції
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
df_trends = get_data(sql_trends)

# Візуалізація
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_trends, x='week_num', y='avg_load', hue='substation_name', marker='o')
plt.title('Динаміка споживання: Виявлення зростаючих трендів')
plt.xlabel('Номер тижня')
plt.ylabel('Середнє навантаження (МВт)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig('trends_innovators.png')
print("✅ Графік збережено як 'trends_innovators.png'")

# ==========================================
# ЧАСТИНА 2: АСОЦІАТИВНІ ПРАВИЛА (КАСКАДНІ АВАРІЇ)
# ==========================================
print("\n🔗 Пошук асоціативних правил (Frequent Patterns)...")

# Шукаємо підстанції, які мали аварії в одну й ту ж годину
sql_alerts = """
SELECT 
    date_trunc('hour', timestamp) as alert_time,
    s.substation_name
FROM Alerts a
JOIN Substations s ON a.substation_id = s.substation_id
WHERE a.alert_type = 'Перевантаження'
GROUP BY alert_time, s.substation_name;
"""
df_alerts = get_data(sql_alerts)

# Групуємо: Час -> Список підстанцій з аваріями [{ПС1, ПС2}, {ПС1}, {ПС3, ПС4}...]
baskets = df_alerts.groupby('alert_time')['substation_name'].apply(list).values

# Рахуємо пари
pair_counts = Counter()
for basket in baskets:
    basket = sorted(basket) # Сортуємо, щоб ПС1-ПС2 і ПС2-ПС1 були однаковими
    if len(basket) > 1:
        # Генеруємо всі можливі пари в цій годині
        pairs = combinations(basket, 2)
        pair_counts.update(pairs)

# Виводимо ТОП-5 правил
print("\n--- ТОП-5 АСОЦІАТИВНИХ ПРАВИЛ (Каскадні аварії) ---")
print(f"{'Підстанція А':<30} + {'Підстанція Б':<30} | {'Кількість спільних аварій'}")
print("-" * 80)
for (item1, item2), count in pair_counts.most_common(5):
    print(f"{item1:<30} + {item2:<30} | {count}")

print("\nВисновки для звіту: Ці пари підстанцій є структурно пов'язаними. Аварія на одній часто супроводжується аварією на іншій.")
