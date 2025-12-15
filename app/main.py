import streamlit as st
import database as db
import queries as q
import plotly.io as pio
from datetime import timedelta

# Імпорт модулів вкладок
from tabs import kpi as tab_kpi
from tabs import map as tab_map
from tabs import consumption as tab_consumption
from tabs import generation as tab_generation
from tabs import alerts as tab_alerts
from tabs import finance as tab_finance

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="Energy Monitor ULTIMATE",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# Глобальні налаштування графіків
pio.templates.default = "plotly_dark"

# CSS хаки для чистоти інтерфейсу
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    [data-testid="stMetricValue"] { font-size: 1.4rem; }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. ЗАВАНТАЖЕННЯ ДАНИХ ---
if st.sidebar.button("🔄 Оновити дані", type="primary"):
    st.cache_data.clear()
    st.rerun()

@st.cache_data(ttl=600)
def load_all_data():
    """Завантажує всі дані одним пакетом."""
    return {
        "load": db.run_query(q.QUERY_LOAD_WEATHER),
        "gen": db.run_query(q.QUERY_GENERATION),
        "alerts": db.run_query(q.QUERY_ALERTS),
        "lines": db.run_query(q.QUERY_LINES),
        "fin": db.run_query(q.QUERY_FINANCE)
    }

with st.spinner('Завантаження аналітики...'):
    data = load_all_data()

# Перевірка на пусту базу
if data["load"].empty:
    st.warning("⚠️ База даних порожня. Запустіть генератор даних.")
    st.stop()

# --- 3. САЙДБАР (ФІЛЬТРИ) ---
st.sidebar.header("🎛️ Фільтри")

# 3.1. Регіон
regions_list = ["Всі регіони"] + sorted(data["load"]['region_name'].unique().tolist())
selected_region = st.sidebar.selectbox("📍 Регіон:", regions_list)

# 3.2. Дата
min_date = data["load"]['timestamp'].min().date()
max_date = data["load"]['timestamp'].max().date()
# За замовчуванням показуємо останній тиждень
default_start = max(min_date, max_date - timedelta(days=7))

date_range = st.sidebar.date_input(
    "📅 Період:", 
    value=(default_start, max_date), 
    min_value=min_date, 
    max_value=max_date
)

# --- 4. ЛОГІКА ФІЛЬТРАЦІЇ (CLEAN LOGIC) ---
def filter_dataframe(df, region, dates, dataset_name):
    """
    Розумна фільтрація:
    - Графіки фільтруються по даті.
    - Аварії (alerts) ігнорують дату, щоб показати журнал повністю.
    """
    if df.empty: return df
    df_filtered = df.copy()
    
    # 1. Регіон (для всіх)
    if region != "Всі регіони" and 'region_name' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['region_name'] == region]
        
    # 2. Дата (для всього, КРІМ alerts)
    if dataset_name != 'alerts':
        if 'timestamp' in df_filtered.columns and isinstance(dates, tuple) and len(dates) == 2:
            mask = (df_filtered['timestamp'].dt.date >= dates[0]) & (df_filtered['timestamp'].dt.date <= dates[1])
            df_filtered = df_filtered.loc[mask]
        
    return df_filtered

# Застосовуємо фільтр до кожного датасету
filtered_data = {
    key: filter_dataframe(df, selected_region, date_range, key) 
    for key, df in data.items()
}

# Визначаємо колонку для групування на графіках
group_by_col = 'substation_name' if selected_region != "Всі регіони" else 'region_name'

# --- 5. ГОЛОВНИЙ ЕКРАН ---
st.title("⚡ Energy Monitor")
st.caption(f"Останнє оновлення: {data['load']['timestamp'].max().strftime('%Y-%m-%d %H:%M')}")

# KPI Block
tab_kpi.render(filtered_data["load"], filtered_data["gen"], filtered_data["fin"], filtered_data["lines"])

# Вкладки
tabs = st.tabs(["🗺️ Карта", "📉 Споживання", "🏭 Генерація", "🚨 Аварії", "💰 Економіка"])

with tabs[0]: 
    tab_map.render(filtered_data["load"])

with tabs[1]: 
    tab_consumption.render(filtered_data["load"], group_by_col)

with tabs[2]: 
    tab_generation.render(filtered_data["gen"])

with tabs[3]: 
    tab_alerts.render(filtered_data["alerts"])

with tabs[4]: 
    tab_finance.render(filtered_data["fin"], filtered_data["lines"])

st.divider()
st.markdown("<center>© 2025 Energy Systems Analytics</center>", unsafe_allow_html=True)
