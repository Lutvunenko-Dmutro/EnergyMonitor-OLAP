import streamlit as st
import plotly.express as px
import pandas as pd

# Палітра для типів днів
COLOR_WORKDAY = "#3b82f6" # Синій
COLOR_WEEKEND = "#f59e0b" # Помаранчевий

def render(df_load, group_by_col):
    """Графіки споживання з поглибленою аналітикою (Optimized)."""
    st.subheader("📈 Динаміка споживання")
    
    # Словник перекладу
    labels_ua = {
        "actual_load_mw": "Навантаження (МВт)",
        "timestamp": "Час",
        "region_name": "Регіон",
        "substation_name": "Підстанція",
        "temperature": "Температура (°C)",
        "hour": "Година доби",
        "day_type": "Тип дня"
    }

    # 1. Основний графік (Line Chart)
    fig = px.line(
        df_load, 
        x='timestamp', 
        y='actual_load_mw', 
        color=group_by_col,
        color_discrete_sequence=px.colors.qualitative.Prism,
        labels=labels_ua
    )
    
    if not df_load.empty:
        # Лінія середнього
        mean_val = df_load['actual_load_mw'].mean()
        fig.add_hline(y=mean_val, line_dash="dash", line_color="white", opacity=0.5, annotation_text="Середнє")
        
        # --- Маркер Піку (Peak Annotation) ---
        # Знаходимо точку максимуму
        max_idx = df_load['actual_load_mw'].idxmax()
        max_point = df_load.loc[max_idx]
        
        fig.add_annotation(
            x=max_point['timestamp'],
            y=max_point['actual_load_mw'],
            text=f"🔥 Max: {max_point['actual_load_mw']:.0f} МВт",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            ax=0, ay=-40,
            bgcolor="#ef4444", bordercolor="white"
        )

    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1),
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---") 
    
    # Розділ статистики
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("##### 📊 Добовий профіль (Робочі vs Вихідні)")
        if not df_load.empty:
            # Працюємо з копією потрібних колонок (швидше)
            df_stat = df_load[['timestamp', 'actual_load_mw']].copy()
            df_stat['hour'] = df_stat['timestamp'].dt.hour
            
            # Визначення типу дня (0-4: будні, 5-6: вихідні)
            df_stat['day_type'] = df_stat['timestamp'].dt.dayofweek.map(lambda x: 'Вихідний' if x >= 5 else 'Робочий')
            
            fig_box = px.box(
                df_stat, 
                x='hour', 
                y='actual_load_mw', 
                color='day_type', 
                color_discrete_map={'Робочий': COLOR_WORKDAY, 'Вихідний': COLOR_WEEKEND},
                labels=labels_ua
            )
            
            # Маркер критичної зони (95% від максимуму)
            peak_load = df_stat['actual_load_mw'].max()
            fig_box.add_hline(y=peak_load*0.95, line_dash="dot", line_color="red", annotation_text="Зона піків")
            
            fig_box.update_layout(
                xaxis_title="Година доби (0-23)", 
                yaxis_title="Потужність (МВт)", 
                legend=dict(orientation="h", y=1.1),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_box, use_container_width=True)

    with c2:
        # --- АНАЛІТИКА: Кореляція ---
        corr_text = ""
        if not df_load.empty and 'temperature' in df_load.columns:
            # Безпечний розрахунок (ігноруємо пропуски)
            valid_data = df_load.dropna(subset=['actual_load_mw', 'temperature'])
            if not valid_data.empty:
                corr = valid_data['actual_load_mw'].corr(valid_data['temperature'])
                corr_text = f"(Коеф. кореляції: **{corr:.2f}**)"

        st.markdown(f"##### 🌡️ Вплив температури {corr_text}")
        
        if 'temperature' in df_load.columns:
            fig_scatter = px.scatter(
                df_load, 
                x='temperature', 
                y='actual_load_mw', 
                color='region_name' if 'region_name' in df_load.columns else None, 
                trendline="ols", 
                opacity=0.6,
                labels=labels_ua,
                title="Залежність споживання від температури"
            )
            fig_scatter.update_layout(margin=dict(l=20, r=20, t=40, b=20))

            st.plotly_chart(fig_scatter, use_container_width=True)
