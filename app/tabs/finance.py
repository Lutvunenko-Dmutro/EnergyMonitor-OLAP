import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Константи
COLOR_SUCCESS = "#22c55e"
COLOR_ALERT = "#ef4444"
COLOR_WARNING = "#f59e0b"
COLOR_HVDC = "#8b5cf6"
HVDC_THRESHOLD_MW = 3000 # Поріг, після якого лінія вважається високовольтною (HVDC)

def render(df_fin, df_lines):
    """Відображає вкладку 'Фінанси та Стан мереж'."""
    st.subheader("💰 Фінансова аналітика та Стан мереж")
    
    labels_ua = {
        "cost": "Вартість (грн)",
        "timestamp": "Час",
        "region_name": "Регіон",
        "load_pct": "Завантаження (%)",
        "status_color": "Статус",
        "line_name": "ЛЕП",
        "price_per_mwh": "Ціна (грн/МВт·год)",
        "hour": "Година доби",
        "day": "День",
        "line_type": "Тип струму",
        "losses_mw": "Втрати (МВт)"
    }
    
    # 1. Підготовка даних (HVDC Simulation)
    if not df_lines.empty:
        df_lines = df_lines.copy()
        # Автоматично визначаємо тип лінії, якщо його немає
        if 'line_type' not in df_lines.columns:
            df_lines['line_type'] = df_lines['max_load_mw'].apply(
                lambda x: 'HVDC (Постійний)' if x >= HVDC_THRESHOLD_MW else 'AC (Змінний)'
            )
        
        # Статус завантаження для кольорів
        df_lines['status_color'] = df_lines['load_pct'].apply(
            lambda x: 'Критично (>90%)' if x > 90 else ('Увага (>80%)' if x > 80 else 'Норма')
        )

    # --- ВЕРХНІЙ РЯД: ВИТРАТИ ТА ЗАВАНТАЖЕННЯ ---
    c1, c2 = st.columns(2)
    
    with c1:
        if not df_fin.empty:
            st.markdown("##### 💸 Динаміка витрат")
            df_fin_grouped = df_fin.groupby(['timestamp', 'region_name'])['cost'].sum().reset_index()
            
            fig_fin = px.area(
                df_fin_grouped, x='timestamp', y='cost', color='region_name',
                color_discrete_sequence=px.colors.qualitative.Pastel, labels=labels_ua
            )
            fig_fin.update_layout(hovermode="x unified", height=350, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_fin, use_container_width=True)
            
    with c2:
        if not df_lines.empty:
            st.markdown("##### 🔌 Навантаження: AC vs HVDC")
            fig_lines = px.scatter(
                df_lines, x='timestamp', y='load_pct', 
                color='line_type', symbol='line_type',
                color_discrete_map={'AC (Змінний)': '#3b82f6', 'HVDC (Постійний)': COLOR_HVDC},
                labels=labels_ua, opacity=0.7
            )
            # Порогові лінії
            fig_lines.add_hline(y=100, line_dash="solid", line_color=COLOR_ALERT)
            fig_lines.add_hline(y=80, line_dash="dot", line_color=COLOR_WARNING)
            fig_lines.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_lines, use_container_width=True)

    st.markdown("---")

    # --- НИЖНІЙ РЯД: ЦІНИ ТА ВТРАТИ ---
    c3, c4 = st.columns(2)

    with c3:
        if not df_fin.empty:
            st.markdown("##### 🔥 Теплова карта цін")
            df_fin['hour'] = df_fin['timestamp'].dt.hour
            df_fin['day'] = df_fin['timestamp'].dt.strftime('%Y-%m-%d')
            
            heatmap_data = df_fin.groupby(['day', 'hour'])['price_per_mwh'].mean().reset_index()
            
            fig_heat = px.density_heatmap(
                heatmap_data, x='hour', y='day', z='price_per_mwh', 
                color_continuous_scale="Magma", labels=labels_ua
            )
            fig_heat.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_heat, use_container_width=True)

    with c4:
        if not df_lines.empty:
            st.markdown("##### 📉 Ефективність передачі (Втрати)")
            
            # Модель втрат (Loss Physics)
            # AC: P_loss ~ I^2 (Квадратична залежність)
            # DC: P_loss ~ I (Лінійна, більш ефективна на піках)
            df_loss = df_lines.copy()
            
            # Векторизований розрахунок (швидше ніж цикл)
            is_hvdc = df_loss['line_type'] == 'HVDC (Постійний)'
            
            # Коефіцієнти втрат (умовні)
            loss_ac = (df_loss['actual_load_mw'] * 0.035) * (df_loss['load_pct'] / 100)**2
            loss_dc = (df_loss['actual_load_mw'] * 0.015) * (df_loss['load_pct'] / 100)
            
            df_loss['losses_mw'] = np.where(is_hvdc, loss_dc, loss_ac)
            
            fig_scatter = px.scatter(
                df_loss, x='load_pct', y='losses_mw', color='line_type',
                color_discrete_map={'AC (Змінний)': '#3b82f6', 'HVDC (Постійний)': COLOR_HVDC},
                labels=labels_ua, opacity=0.6,
                title="HVDC ефективніший при високому завантаженні"
            )
            fig_scatter.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_scatter, use_container_width=True)