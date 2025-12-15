import streamlit as st
import plotly.express as px
import pandas as pd

# Палітра кольорів
COLOR_WORKDAY = "#3b82f6"
COLOR_WEEKEND = "#f59e0b"

def render(df_load, group_by_col):
    """
    Рендеринг вкладки споживання.
    Включає: лінійний графік, box-plot розподілу та кореляцію з температурою.
    """
    st.subheader("📈 Динаміка споживання")
    
    if df_load.empty:
        st.info("Дані про споживання відсутні.")
        return

    # Словник підписів (форматований для читабельності)
    labels_ua = {
        "actual_load_mw": "Навантаження (МВт)",
        "timestamp": "Час",
        "region_name": "Регіон",
        "substation_name": "Підстанція",
        "temperature": "Температура (°C)",
        "hour": "Година доби",
        "day_type": "Тип дня"
    }

    # --- 1. ГОЛОВНИЙ ГРАФІК (Line Chart) ---
    fig = px.line(
        df_load, 
        x='timestamp', 
        y='actual_load_mw', 
        color=group_by_col,
        color_discrete_sequence=px.colors.qualitative.Prism,
        labels=labels_ua
    )
    
    # Додавання анотації піку
    if not df_load.empty:
        max_pt = df_load.loc[df_load['actual_load_mw'].idxmax()]
        fig.add_annotation(
            x=max_pt['timestamp'], 
            y=max_pt['actual_load_mw'], 
            text=f"🔥 Max: {max_pt['actual_load_mw']:.0f}", 
            showarrow=True, 
            arrowhead=2, 
            ax=0, ay=-40, 
            bgcolor="#ef4444", 
            bordercolor="white"
        )
    
    fig.update_layout(
        hovermode="x unified", 
        legend=dict(orientation="h", y=1.1), 
        height=500, 
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---") 

    # --- 2. СТАТИСТИКА (Box Plot & Scatter) ---
    c1, c2 = st.columns(2)
    
    with c1:
        # Підготовка даних для Box Plot
        df_stat = df_load[['timestamp', 'actual_load_mw']].copy()
        df_stat['hour'] = df_stat['timestamp'].dt.hour
        df_stat['day_type'] = df_stat['timestamp'].dt.dayofweek.map(
            lambda x: 'Вихідний' if x >= 5 else 'Робочий'
        )
        
        fig_box = px.box(
            df_stat, 
            x='hour', 
            y='actual_load_mw', 
            color='day_type', 
            color_discrete_map={'Робочий': COLOR_WORKDAY, 'Вихідний': COLOR_WEEKEND}, 
            labels=labels_ua
        )
        fig_box.update_layout(
            xaxis_title="Година доби", 
            yaxis_title="Потужність (МВт)", 
            legend=dict(orientation="h", y=1.1), 
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_box, use_container_width=True, config={'displayModeBar': False})

    with c2:
        # Графік кореляції (Scatter)
        if 'temperature' in df_load.columns:
            fig_scat = px.scatter(
                df_load, 
                x='temperature', 
                y='actual_load_mw', 
                color='region_name' if 'region_name' in df_load.columns else None, 
                trendline="ols", 
                opacity=0.6, 
                labels=labels_ua
            )
            fig_scat.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_scat, use_container_width=True, config={'displayModeBar': False})
