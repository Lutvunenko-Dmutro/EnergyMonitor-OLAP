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
    initial_sidebar_state="auto"
)

# Глобальні налаштування графіків
pio.templates.default = "plotly_dark"

# --- MOBILE OPTIMIZATION ---
st.markdown("""
<style>
    @media (max-width: 600px) {
        div[data-testid="column"] { width: 50% !important; flex: 1 1 50% !important; min-width: 50% !important; }
        .block-container { padding-top: 2rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
        div[data-testid="stMetricValue"] { font-size: 1.2rem !important; }
        div[data-testid="stMetricLabel"] { font-size: 0.8rem !important; }
        button[data-baseweb="tab"] { padding: 0.5rem !important; margin: 0 !important; }
    }
    .modebar { display: none !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. ЗАВАНТАЖЕННЯ ДАНИХ ---
if st.sidebar.button("🔄 Оновити дані"):
    st.cache_data.clear()

with st.spinner('Завантаження даних...'):
    # Завантажуємо всі датафрейми в словник для зручності
    data = {
        "load": db.run_query(q.QUERY_LOAD_WEATHER),
        "gen": db.run_query(q.QUERY_GENERATION),
        "alerts": db.run_query(q.QUERY_ALERTS),
        "lines": db.run_query(q.QUERY_LINES),
        "fin": db.run_query(q.QUERY_FINANCE)
    }

if data["load"].empty:
    st.error("⚠️ **Увага:** Дані відсутні! Запустіть генератор (03_generate...).")
    st.stop()

# --- 3. САЙДБАР (ФІЛЬТРИ) ---
st.sidebar.header("🎛️ Налаштування")

regions_list = ["Всі регіони"] + sorted(data["load"]['region_name'].unique().tolist())
selected_region = st.sidebar.selectbox("📍 Регіон:", regions_list)

min_date = data["load"]['timestamp'].min().date()
max_date = data["load"]['timestamp'].max().date()
default_start = max_date - timedelta(days=7)
if default_start < min_date: default_start = min_date

date_range = st.sidebar.date_input("📅 Період:", value=(default_start, max_date), min_value=min_date, max_value=max_date)

# --- 4. ФІЛЬТРАЦІЯ (ОПТИМІЗОВАНО) ---
def apply_filters(df, region, date_range):
    """Фільтрує датафрейм за регіоном та датою."""
    if df.empty: return df
    
    # Фільтр регіону
    if region != "Всі регіони" and 'region_name' in df.columns:
        df = df[df['region_name'] == region]
        
    # Фільтр дати
    if 'timestamp' in df.columns and date_range and len(date_range) == 2:
        mask = (df['timestamp'].dt.date >= date_range[0]) & (df['timestamp'].dt.date <= date_range[1])
        df = df.loc[mask]
        
    return df

# Застосовуємо фільтр до всіх датафреймів у циклі
filtered_data = {key: apply_filters(df, selected_region, date_range) for key, df in data.items()}

group_by_col = 'substation_name' if selected_region != "Всі регіони" else 'region_name'

# --- 5. ГОЛОВНИЙ ЕКРАН ---
st.title("⚡ Energy Monitor")

last_update = data["load"]['timestamp'].max().strftime('%d.%m %H:%M')
period_str = f"{date_range[0].strftime('%d.%m')} - {date_range[1].strftime('%d.%m')}" if len(date_range) == 2 else "..."

st.caption(f"🟢 ONLINE | 🕒 {last_update} | 📅 {period_str}")

# --- МОДУЛІ ---
# KPI
tab_kpi.render(filtered_data["load"], filtered_data["gen"], filtered_data["fin"], filtered_data["lines"])

# Вкладки
tabs = st.tabs(["🗺️ Карта", "📉 Спожив.", "🏭 Генер.", "🚨 Аварії", "💰 Фінанси"])

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
st.caption("© 2025 Energy Systems")