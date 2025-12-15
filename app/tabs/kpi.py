import streamlit as st
import plotly.graph_objects as go

def render(df_load, df_gen, df_fin, df_lines):
    """
    Рендеринг KPI панелі (верхній ряд).
    Включає метрики та gauge-діаграму завантаженості мережі.
    """
    if df_load.empty:
        return

    # --- 1. Розрахунки ---
    # Використовуємо iloc[0], бо дані вже відсортовані за часом (DESC) у запиті
    curr_load = df_load['actual_load_mw'].iloc[0]
    
    # Безпечні агрегації (суми та середні)
    total_gen = df_gen['actual_generation_mw'].sum() / 1e3 if not df_gen.empty else 0
    total_cost = df_fin['cost'].sum() / 1e6 if not df_fin.empty else 0
    avg_load_pct = df_lines['load_pct'].mean() if not df_lines.empty else 0

    # --- 2. Візуалізація ---
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric("⚡ Навантаження (Live)", f"{curr_load:,.0f} МВт".replace(",", " "))
    c2.metric("🏭 Генерація (Сума)", f"{total_gen:.2f} ГВт")
    c3.metric("💰 Витрати (Сума)", f"{total_cost:.1f} млн ₴")
    
    with c4:
        # Побудова спідометра (Gauge Chart)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_load_pct,
            title={'text': "Завант. мережі", 'font': {'size': 14}},
            number={'suffix': "%", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "#3b82f6"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 60], 'color': "rgba(34, 197, 94, 0.3)"},   # Зелений (OK)
                    {'range': [60, 85], 'color': "rgba(245, 158, 11, 0.3)"},  # Жовтий (Warning)
                    {'range': [85, 100], 'color': "rgba(239, 68, 68, 0.3)"}   # Червоний (Critical)
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        # Стилізація для темної теми
        fig.update_layout(
            height=130, 
            margin=dict(t=35, b=10, l=25, r=25), 
            paper_bgcolor="rgba(0,0,0,0)", 
            font={'color': "white"}
        )
        
        # Відображення без кнопок меню
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
