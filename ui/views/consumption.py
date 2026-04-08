import pandas as pd
import plotly.express as px
import streamlit as st
from utils.ui_helpers import safe_plotly_render

from core.analytics.aggregator import add_relative_load, aggregate_consumption

COLOR_WORKDAY = "#3b82f6"
COLOR_WEEKEND = "#f59e0b"

_LABELS = {
    "actual_load_mw": "Навантаження (МВт)",
    "relative_load": "Навантаження (%)",
    "timestamp": "Час",
    "region_name": "Регіон",
    "substation_name": "Підстанція",
    "temperature": "Температура (°C)",
    "hour": "Година доби",
    "day_type": "Тип дня",
}


def render(df_load: pd.DataFrame, group_by_col: str):
    """
    Вкладка споживання з повним набором інструментів аналізу:
      - Multiselect для фільтрації регіонів/підстанцій
      - Нормалізація до відносних значень (%)
      - Facet-сітка з незалежними осями Y
      - Логарифмічна шкала
      - Scatter з окремими лініями регресії per-region
    """
    st.subheader("📈 Динаміка споживання")

    if df_load is None or df_load.empty:
        st.info("Дані про споживання відсутні.")
        return

    df_load = df_load.copy()
    df_load["timestamp"] = pd.to_datetime(df_load["timestamp"])

    # Фільтрація вхідного масиву даних
    df_sel = df_load.copy()

    # Формування елементів керування інтерфейсу (Grafana-style Header)
    is_rel = st.session_state.get("cons_rel", False)
    y_col = "actual_load_mw"  # Глобальна прив'язка до початку функції
    y_label = "Навантаження (% від піку)" if is_rel else "Навантаження (МВт)"

    col_title, col_tools = st.columns([4, 1])
    col_title.markdown(f"### 📊 Динаміка: {y_label}")

    with col_tools.popover("⚙️ Налаштування", width='stretch'):
        use_relative = st.toggle(
            "📈 Відносні показники (%)", value=False, key="cons_rel"
        )
        use_log = st.toggle("🪵 Логарифмічна шкала (Y)", value=False, key="cons_log")
        use_facet = st.toggle(
            "🔲 Сітка графіків (by Region)", value=False, key="cons_facet"
        )

    # Дискретизація та агрегація даних за годинами (Resample)
    num_cols = ["actual_load_mw"]
    if "temperature" in df_sel.columns:
        num_cols.append("temperature")

    df_plot = aggregate_consumption(df_sel, group_by_col, num_cols)

    # Масштабування та нормування показників (%)
    y_col = "actual_load_mw"
    if use_relative:
        df_plot = add_relative_load(df_plot, group_by_col)
        y_col = "relative_load"

    y_label = _LABELS.get(y_col, y_col)

    # Візуалізація лінійного графіка динаміки навантаження
    fig = px.line(
        df_plot,
        x="timestamp",
        y=y_col,
        color=group_by_col,
        facet_col=group_by_col if use_facet else None,
        facet_col_wrap=2 if use_facet else None,
        log_y=use_log,
        color_discrete_sequence=px.colors.qualitative.Prism,
        template="plotly_dark",
        labels={**_LABELS, y_col: y_label},
    )

    if not use_facet and not df_plot.empty:
        max_pt = df_plot.loc[df_plot[y_col].idxmax()]
        suffix = "%" if use_relative else " МВт"
        fig.add_annotation(
            x=max_pt["timestamp"],
            y=max_pt[y_col],
            text=f"🔥 Пік: {max_pt[y_col]:.1f}{suffix}",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            bgcolor="#ef4444",
            bordercolor="white",
            font=dict(color="white"),
        )

    fig.update_layout(
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            itemclick="toggleothers",
            itemdoubleclick="toggle",
        ),
        height=600 if use_facet else 480,
        margin=dict(l=20, r=20, t=80, b=20),
    )
    if use_facet:
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_yaxes(matches=None, showticklabels=True)

    safe_plotly_render(fig)
    st.markdown("---")

    # Аналіз статистичного розподілу (Boxplot + Scatter)
    col1, col2 = st.columns(2)

    with col1:
        st.caption("📦 Розподіл навантаження по годинах")
        df_stat = df_plot[["timestamp", y_col]].copy()
        df_stat["hour"] = df_stat["timestamp"].dt.hour
        df_stat["day_type"] = df_stat["timestamp"].dt.dayofweek.apply(
            lambda d: "Вихідний" if d >= 5 else "Робочий"
        )
        fig_box = px.box(
            df_stat,
            x="hour",
            y=y_col,
            color="day_type",
            color_discrete_map={"Робочий": COLOR_WORKDAY, "Вихідний": COLOR_WEEKEND},
            labels={**_LABELS, y_col: y_label},
            template="plotly_dark",
        )
        fig_box.update_layout(
            xaxis_title="Година доби",
            yaxis_title=y_label,
            legend=dict(orientation="h", y=1.1),
            margin=dict(l=10, r=10, t=30, b=10),
        )
        safe_plotly_render(fig_box)

    with col2:
        if "temperature" in df_plot.columns and df_plot["temperature"].notna().any():
            st.caption("🌡️ Залежність від температури (регресія per-region)")
            use_log_scat = st.toggle(
                "🪵 Логарифмічна шкала (Y)", value=False, key="cons_scatter_log"
            )
            fig_scat = px.scatter(
                df_plot,
                x="temperature",
                y=y_col,
                color=group_by_col,
                trendline="ols",
                opacity=0.5,
                log_y=use_log_scat,
                labels={**_LABELS, y_col: y_label},
                template="plotly_dark",
                title=f"{y_label} vs Температура",
            )
            fig_scat.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            safe_plotly_render(fig_scat)
        else:
            st.info("🌡️ Аналіз температури недоступний для Kaggle даних.")
