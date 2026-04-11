import plotly.express as px
import streamlit as st
from src.utils.ui_helpers import safe_plotly_render


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
            label_visibility="collapsed",
        )

    # Перевірка на дані
    if df_load.empty:
        st.info("Дані для відображення на карті відсутні.")
        return

    # Підготовка даних (останній запис для кожної підстанції або регіону)
    group_col = (
        "substation_name"
        if "substation_name" in df_load.columns
        else (
            "substation_id"
            if "substation_id" in df_load.columns
            else ("region_name" if "region_name" in df_load.columns else None)
        )
    )

    # Якщо немає жодної колонки для групування, беремо просто останній запис
    if group_col:
        latest = df_load.sort_values("timestamp").groupby(group_col).tail(1).copy()
    else:
        latest = df_load.sort_values("timestamp").tail(1).copy()

    # Якщо немає локації, малювати карту немає сенсу
    if "latitude" not in latest.columns or "longitude" not in latest.columns:
        st.warning(
            "Географічні дані (latitude/longitude) недоступні у цьому джерелі даних."
        )
        return

    # Якщо немає capacity, ставимо дефолтні значення для карток і розміру
    hover_data_params = {"actual_load_mw": True, "latitude": False, "longitude": False}

    if "capacity_mw" in latest.columns:
        latest["load_pct"] = (latest["actual_load_mw"] / latest["capacity_mw"]) * 100
        size_col = "capacity_mw"
        color_col = "load_pct"
        size_max_val = 25
        hover_data_params["capacity_mw"] = True
        hover_data_params["load_pct"] = ":.1f"
    else:
        latest["marker_size"] = 10
        size_col = "marker_size"
        color_col = "actual_load_mw"
        size_max_val = 15

    # Додаємо додаткові колонки в hover, якщо вони існують:
    for extra_col in ["temperature_c", "health_score", "voltage_kv"]:
        if extra_col in latest.columns:
            hover_data_params[extra_col] = True

    # Формування імені для відображення
    if "substation_name" in latest.columns:
        hover_name_col = "substation_name"
    elif "region_name" in latest.columns:
        hover_name_col = "region_name"
    else:
        # Резервний варіант, якщо і substation_name немає
        if "substation_id" in latest.columns:
            latest["display_name"] = "Підстанція ID " + latest["substation_id"].astype(
                str
            )
        else:
            latest["display_name"] = "Невідома локація"
        hover_name_col = "display_name"

    # Словник для гарних підписів (UA)
    labels_ua = {
        "load_pct": "Завантаження (%)",
        "actual_load_mw": "Навантаження (МВт)",
        "capacity_mw": "Потужність (МВт)",
        "substation_name": "Підстанція",
        "latitude": "Широта",
        "longitude": "Довгота",
    }

    # Логіка вибору карти
    if "Маркери" in map_mode:
        fig = px.scatter_mapbox(
            latest,
            lat="latitude",
            lon="longitude",
            color=color_col,
            color_continuous_scale=[
                "#22c55e",
                "#f59e0b",
                "#ef4444",
            ],  # Зелений -> Жовтий -> Червоний
            size=size_col,
            size_max=size_max_val,
            zoom=5.5,
            center={"lat": 49.0, "lon": 31.0},
            mapbox_style="carto-darkmatter",
            hover_name=hover_name_col,
            hover_data=hover_data_params,
            labels=labels_ua,
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
            title="Теплова карта споживання (МВт)",
        )

    fig.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Рендер
    safe_plotly_render(fig)

    # [FIX]: Spacer для скролінгу в самому низу
    st.markdown('<div style="height: 300px;"></div>', unsafe_allow_html=True)
