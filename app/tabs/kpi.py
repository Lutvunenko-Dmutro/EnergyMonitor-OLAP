import streamlit as st
import plotly.graph_objects as go

# --- КОНСТАНТИ ДИЗАЙНУ ---
COLOR_PRIMARY = "#3b82f6"
COLOR_ALERT = "#ef4444"

# Напівпрозорі кольори для зон спідометра
GAUGE_GREEN = "rgba(34, 197, 94, 0.2)"
GAUGE_YELLOW = "rgba(245, 158, 11, 0.2)"
GAUGE_RED = "rgba(239, 68, 68, 0.2)"

def render(df_load, df_gen, df_fin, df_lines):
    """Відображає розширену панель KPI."""
    
    # 1. Розрахунок метрик (безпечний доступ до даних)
    # Використовуємо .sum() / 1e3 замість / 1000 для лаконічності
    curr_load = df_load['actual_load_mw'].iloc[0] if not df_load.empty else 0
    total_gen = df_gen['actual_generation_mw'].sum() / 1e3 if not df_gen.empty else 0
    total_cost = df_fin['cost'].sum() / 1e6 if not df_fin.empty else 0
    avg_line = df_lines['load_pct'].mean() if not df_lines.empty else 0
    
    # 2. Візуалізація
    k1, k2, k3, k4 = st.columns(4)
    
    k1.metric("⚡ Навантаження", f"{curr_load:,.0f} МВт".replace(",", " "), "Стабільно")
    k2.metric("🏭 Генерація", f"{total_gen:.1f} ГВт", "В нормі", delta_color="off")
    k3.metric("💰 Витрати", f"{total_cost:.1f} млн ₴", "-1.2%", delta_color="inverse")
    
    with k4:
        _render_gauge_chart(avg_line)
    
    st.markdown("---")

def _render_gauge_chart(value):
    """Допоміжна функція для малювання спідометра (Gauge Chart)."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Завант. мережі", 'font': {'size': 14, 'color': "white"}},
        number={'suffix': "%", 'font': {'size': 20, 'color': "white", 'weight': 'bold'}},
        gauge={
            'axis': {
                'range': [0, 100], 
                'tickwidth': 1, 
                'tickcolor': "white", 
                'tickfont': {'color': "white", 'size': 10}
            },
            'bar': {'color': COLOR_PRIMARY, 'thickness': 0.5},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': GAUGE_GREEN},
                {'range': [50, 80], 'color': GAUGE_YELLOW},
                {'range': [80, 100], 'color': GAUGE_RED}
            ],
            'threshold': {
                'line': {'color': COLOR_ALERT, 'width': 3},
                'thickness': 0.5,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=130,
        margin={'t': 35, 'b': 10, 'l': 25, 'r': 25},
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"}
    )
    st.plotly_chart(fig, use_container_width=True)