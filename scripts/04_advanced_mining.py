import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
from dotenv import load_dotenv

# Налаштування
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
# ЧАСТИНА 1: КЛАСТЕРИЗАЦІЯ ПІДСТАНЦІЙ (K-MEANS)
# ==========================================
print("🔄 Запуск кластеризації (K-Means)...")

# 1. Збираємо дані для RFM-аналізу (Recency -> Volatility, Frequency -> Load, Monetary -> Alerts)
sql_clustering = """
SELECT 
    s.substation_name,
    AVG(l.actual_load_mw) as avg_load,
    STDDEV(l.actual_load_mw) as load_volatility, -- Наскільки "стрибає" навантаження
    COUNT(a.alert_id) as alert_count
FROM Substations s
LEFT JOIN LoadMeasurements l ON s.substation_id = l.substation_id
LEFT JOIN Alerts a ON s.substation_id = a.substation_id
GROUP BY s.substation_name;
"""
df_cluster = get_data(sql_clustering).fillna(0)

# 2. Нормалізація даних (щоб великі числа не "забивали" малі)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster[['avg_load', 'load_volatility', 'alert_count']])

# 3. Алгоритм K-Means (шукаємо 3 типи підстанцій)
kmeans = KMeans(n_clusters=3, random_state=42)
df_cluster['Cluster'] = kmeans.fit_predict(X_scaled)

# 4. Візуалізація
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cluster, x='avg_load', y='alert_count', hue='Cluster', palette='viridis', s=100)
plt.title('Кластеризація Підстанцій: Навантаження vs Аварійність')
plt.xlabel('Середнє навантаження (МВт)')
plt.ylabel('Кількість аварій')
plt.grid(True)
plt.savefig('clustering_result.png') # Зберігаємо картинку для звіту
print("✅ Графік збережено як 'clustering_result.png'")

# Вивід опису кластерів
print("\n--- ОПИС КЛАСТЕРІВ ---")
print(df_cluster.groupby('Cluster')[['avg_load', 'alert_count']].mean())

# ==========================================
# ЧАСТИНА 2: ДЕРЕВО РІШЕНЬ (CLASSIFICATION)
# ==========================================
print("\n🔄 Запуск прогнозування (Decision Tree)...")

# 1. Готуємо дані: Вхід (Погода, Час) -> Вихід (Чи є перевантаження?)
sql_classification = """
SELECT 
    EXTRACT(HOUR FROM l.timestamp) as hour_of_day,
    w.temperature,
    CASE WHEN (l.actual_load_mw / s.capacity_mw) > 0.95 THEN 1 ELSE 0 END as is_critical
FROM LoadMeasurements l
JOIN Substations s ON l.substation_id = s.substation_id
JOIN WeatherReports w ON l.timestamp = w.timestamp AND s.region_id = w.region_id
LIMIT 50000; -- Беремо вибірку для швидкості
"""
df_class = get_data(sql_classification)

# 2. Тренування моделі
X = df_class[['hour_of_day', 'temperature']]
y = df_class['is_critical']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

clf = DecisionTreeClassifier(max_depth=3, random_state=42) # Неглибоке дерево, щоб було зрозуміло
clf.fit(X_train, y_train)

# 3. Оцінка точності
y_pred = clf.predict(X_test)
print("\n--- Звіт класифікації ---")
print(classification_report(y_test, y_pred))

# 4. Малюємо дерево
plt.figure(figsize=(12, 8))
plot_tree(clf, feature_names=['Година', 'Температура'], class_names=['Норма', 'Аварія'], filled=True)
plt.title('Дерево рішень: Прогноз аварійного стану')
plt.savefig('decision_tree.png')
print("✅ Дерево збережено як 'decision_tree.png'")
