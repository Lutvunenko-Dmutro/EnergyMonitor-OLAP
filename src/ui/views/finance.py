import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src.utils.ui_helpers import safe_plotly_render

from src.core.physics import calculate_line_losses

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
        "losses_mw": "Втрати (МВт)",
    }

    # Розрахунок типу ліній та фізичних втрат потужності
    df_lines = calculate_line_losses(df_lines)

    st.markdown("---")

    if not df_fin.empty:
        df_fin["day"] = df_fin["timestamp"].dt.strftime("%Y-%m-%d")
    if not df_lines.empty:
        df_lines["day"] = df_lines["timestamp"].dt.strftime("%Y-%m-%d")

    # Візуалізація верхнього ярусу показників (Вартість та Завантаження)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("##### 📊 Вартість генерації по днях")
        if not df_fin.empty:
            df_cost = df_fin.groupby(["day", "region_name"])["cost"].sum().reset_index()

            fig_fin = px.bar(
                df_cost,
                x="day",
                y="cost",
                color="region_name",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                labels=labels_ua,
            )
            fig_fin.update_layout(
                barmode="stack",
                hovermode="x unified",
                height=350,
                margin=dict(l=0, r=0, t=10, b=0),
            )
            fig_fin.update_xaxes(title_text="Дата")
            safe_plotly_render(fig_fin)

    with c2:
        st.markdown("##### 📈 Середньодобове завантаження ліній")
        if not df_lines.empty:
            df_l_mean = (
                df_lines.groupby(["day", "line_type"])["load_pct"].mean().reset_index()
            )

            fig_lines = px.line(
                df_l_mean,
                x="day",
                y="load_pct",
                color="line_type",
                color_discrete_map={"AC": "#3b82f6", "HVDC": COLOR_HVDC},
                labels=labels_ua,
                markers=True,
            )
            fig_lines.add_hline(y=100, line_dash="solid", line_color=COLOR_ALERT)
            fig_lines.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=0))
            fig_lines.update_xaxes(title_text="Дата")
            safe_plotly_render(fig_lines)

    st.markdown("---")

    # Візуалізація нижнього ярусу показників (Ціна та Втрати)
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("##### 🌡️ Теплова карта цін")
        if not df_fin.empty:
            df_fin["hour"] = df_fin["timestamp"].dt.hour
            df_heat = (
                df_fin.groupby(["day", "hour"])["price_per_mwh"].mean().reset_index()
            )
            # Pivot для жорсткої сітки
            heat_pivot = df_heat.pivot(
                index="day", columns="hour", values="price_per_mwh"
            )

            fig_heat = go.Figure(
                data=go.Heatmap(
                    z=heat_pivot.values,
                    x=heat_pivot.columns,
                    y=heat_pivot.index,
                    colorscale="Inferno",
                    xgap=2,
                    ygap=2,
                    colorbar=dict(title="Ціна (грн)"),
                )
            )
            fig_heat.update_layout(
                xaxis=dict(title="Година доби (0-23)", tickmode="linear", dtick=1),
                yaxis=dict(title="Дата", autorange="reversed"),
                height=400,
                margin=dict(l=0, r=0, t=10, b=0),
            )
            safe_plotly_render(fig_heat)

    with c4:
        st.markdown("##### ⚖️ Характеристика втрат")
        # Втрати losses_mw розраховано у модулі physics.py
        if not df_lines.empty:
            fig_scat = px.scatter(
                df_lines,
                x="load_pct",
                y="losses_mw",
                color="line_type",
                color_discrete_map={"AC": "#3b82f6", "HVDC": COLOR_HVDC},
                labels=labels_ua,
                opacity=0.6,
            )
            fig_scat.update_layout(
                legend_title_text="Тип лінії",
                height=400,
                margin=dict(l=0, r=0, t=10, b=0),
            )
            safe_plotly_render(fig_scat)

    # [FIX]: Spacer для скролінгу в самому низу
    st.markdown('<div style="height: 300px;"></div>', unsafe_allow_html=True)
