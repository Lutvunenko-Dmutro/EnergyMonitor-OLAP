import streamlit as st
import plotly.express as px

def render(df_load):
    """Малює карту з можливістю перемикання режимів."""
    
    c1, c2 = st.columns([3, 1])
    with c1:
        st.subheader("📍 Географічний моніторинг")
    with c2:
        map_mode = st.radio("Режим карти:", ["Маркери (Статус)", "Heatmap (Навантаження)"], horizontal=True, label_visibility="collapsed")

    if df_load.empty:
        st.warning("Дані відсутні.")
        return

    latest = df_load.sort_values('timestamp').groupby('substation_name').tail(1).copy()
    latest['load_pct'] = (latest['actual_load_mw'] / latest['capacity_mw']) * 100
    
    # Словник перекладу для карти
    labels_ua = {
        "load_pct": "Завантаження (%)",
        "actual_load_mw": "Навантаження (МВт)",
        "capacity_mw": "Потужність (МВт)",
        "substation_name": "Підстанція",
        "latitude": "Широта",
        "longitude": "Довгота"
    }

    if "Маркери" in map_mode:
        fig = px.scatter_map(
            latest,
            lat="latitude",
            lon="longitude",
            color="load_pct",
            color_continuous_scale=["#22c55e", "#f59e0b", "#ef4444"],
            size="capacity_mw",
            size_max=25,
            zoom=5.5,
            center={"lat": 49.0, "lon": 31.0},
            map_style="carto-darkmatter",
            hover_name="substation_name",
            hover_data={"actual_load_mw": True, "capacity_mw": True, "latitude": False},
            labels=labels_ua # <--- Додано переклад
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
            labels=labels_ua, # <--- Додано переклад
            title="Теплова карта споживання (МВт)"
        )
    
    fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)