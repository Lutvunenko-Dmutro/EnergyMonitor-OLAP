import streamlit as st
import plotly.express as px

def render(df_load):
    """
    Малює карту з можливістю перемикання режимів.
    Код відформатовано згідно з PEP8 (читабельний).
    """
    
    # Header Layout
    c1, c2 = st.columns([3, 1])
    with c1:
        st.subheader("📍 Географічний моніторинг")
    with c2:
        map_mode = st.radio(
            "Режим карти:", 
            ["Маркери (Статус)", "Heatmap (Навантаження)"], 
            horizontal=True, 
            label_visibility="collapsed"
        )

    # Перевірка на дані
    if df_load.empty:
        st.info("Дані для відображення на карті відсутні.")
        return

    # Підготовка даних (останній запис для кожної підстанції)
    latest = df_load.sort_values('timestamp').groupby('substation_name').tail(1).copy()
    latest['load_pct'] = (latest['actual_load_mw'] / latest['capacity_mw']) * 100
    
    # Словник для гарних підписів (UA)
    labels_ua = {
        "load_pct": "Завантаження (%)",
        "actual_load_mw": "Навантаження (МВт)",
        "capacity_mw": "Потужність (МВт)",
        "substation_name": "Підстанція",
        "latitude": "Широта",
        "longitude": "Довгота"
    }

    # Логіка вибору карти
    if "Маркери" in map_mode:
        fig = px.scatter_mapbox(
            latest,
            lat="latitude",
            lon="longitude",
            color="load_pct",
            color_continuous_scale=["#22c55e", "#f59e0b", "#ef4444"], # Зелений -> Жовтий -> Червоний
            size="capacity_mw",
            size_max=25,
            zoom=5.5,
            center={"lat": 49.0, "lon": 31.0},
            mapbox_style="carto-darkmatter",
            hover_name="substation_name",
            hover_data={
                "actual_load_mw": True, 
                "capacity_mw": True, 
                "latitude": False, 
                "longitude": False,
                "load_pct": ":.1f" # Форматування до 1 знаку
            },
            labels=labels_ua
        )
    else:
        fig = px.density_mapbox(
            latest,
            lat="latitude",
            lon="longitude",
            z="actual_load_mw",
            radius=40,
            center={"lat": 49.0, "lon": 31.0},
            zoom=5.5,
            mapbox_style="carto-darkmatter",
            color_continuous_scale="Viridis",
            labels=labels_ua,
            title="Теплова карта споживання (МВт)"
        )
    
    fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
    
    # Рендер
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
