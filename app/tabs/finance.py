import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Константи кольорів
COLOR_HVDC = "#8b5cf6"
COLOR_ALERT = "#ef4444"
COLOR_WARNING = "#f59e0b"

def render(df_fin, df_lines):
    """
    Рендеринг вкладки фінансів та стану мереж.
    Включає: вартість, heatmap цін, завантаження ліній та модель втрат.
    """
    st.subheader("💰 Фінансова аналітика")
    
    # Словник підписів
    labels_ua = {
        "cost": "Вартість (грн)",
        "timestamp": "Час",
        "region_name": "Регіон",
        "load_pct": "Завантаження (%)",
        "price_per_mwh": "Ціна (грн/МВт·год)",
        "hour": "Година",
        "losses_mw": "Втрати (МВт)"
    }
    
    # Визначення типу ліній (AC/DC), якщо ще не визначено
    if not df_lines.empty and 'line_type' not in df_lines.columns:
        df_lines['line_type'] = df_lines['max_load_mw'].apply(
            lambda x: 'HVDC' if x >= 3000 else 'AC'
        )

    # --- ВЕРХНІЙ РЯД ---
    c1, c2 = st.columns(2)
    
    with c1:
        if not df_fin.empty:
            df_cost = df_fin.groupby(['timestamp', 'region_name'])['cost'].sum().reset_index()
            
            fig_fin = px.area(
                df_cost, 
                x='timestamp', 
                y='cost', 
                color='region_name', 
                color_discrete_sequence=px.colors.qualitative.Pastel, 
                labels=labels_ua
            )
            fig_fin.update_layout(
                hovermode="x unified", 
                height=350, 
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_fin, use_container_width=True, config={'displayModeBar': False})
            
    with c2:
        if not df_lines.empty:
            fig_lines = px.scatter(
                df_lines, 
                x='timestamp', 
                y='load_pct', 
                color='line_type', 
                color_discrete_map={'AC': '#3b82f6', 'HVDC': COLOR_HVDC}, 
                labels=labels_ua, 
                opacity=0.7
            )
            # Додаємо лінію критичного порогу
            fig_lines.add_hline(y=100, line_dash="solid", line_color=COLOR_ALERT)
            fig_lines.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_lines, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")
    
    # --- НИЖНІЙ РЯД ---
    c3, c4 = st.columns(2)
    
    with c3:
        if not df_fin.empty:
            # Підготовка даних для Heatmap
            df_fin['hour'] = df_fin['timestamp'].dt.hour
            df_fin['day'] = df_fin['timestamp'].dt.strftime('%Y-%m-%d')
            
            hm_data = df_fin.groupby(['day', 'hour'])['price_per_mwh'].mean().reset_index()
            
            fig_heat = px.density_heatmap(
                hm_data, 
                x='hour', 
                y='day', 
                z='price_per_mwh', 
                color_continuous_scale="Magma", 
                labels=labels_ua
            )
            fig_heat.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
            
    with c4:
        if not df_lines.empty:
            # Розрахунок втрат (Розділили довгу формулу для читабельності)
            is_hvdc = df_lines['line_type'] == 'HVDC'
            
            # Втрати DC (лінійні) vs AC (квадратичні)
            loss_dc = (df_lines['actual_load_mw'] * 0.015) * (df_lines['load_pct'] / 100)
            loss_ac = (df_lines['actual_load_mw'] * 0.035) * (df_lines['load_pct'] / 100)**2
            
            df_lines['losses_mw'] = np.where(is_hvdc, loss_dc, loss_ac)
            
            fig_scat = px.scatter(
                df_lines, 
                x='load_pct', 
                y='losses_mw', 
                color='line_type', 
                color_discrete_map={'AC': '#3b82f6', 'HVDC': COLOR_HVDC}, 
                labels=labels_ua, 
                opacity=0.6
            )
            fig_scat.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_scat, use_container_width=True, config={'displayModeBar': False})
