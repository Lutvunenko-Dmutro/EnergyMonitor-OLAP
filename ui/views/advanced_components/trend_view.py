import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose
from utils.ui_helpers import safe_plotly_render

def render_trend_decomposition(df, selected_substation, use_rel):
    """
    Renders the time-series seasonal decomposition segment.
    """
    st.subheader("📈 Декомпозиція часового ряду")

    use_aggregate = ("Усі підстанції" in selected_substation or not selected_substation 
                    if isinstance(selected_substation, list) else selected_substation == "Усі підстанції")

    if not use_aggregate:
        sub_to_analyze = selected_substation[0] if isinstance(selected_substation, list) else selected_substation
        st.success(f"🎯 Аналіз тренду для об'єкта: **{sub_to_analyze}**")
        df_sub = df[df["substation_name"] == sub_to_analyze].copy()
        title_text = f"Декомпозиція: {sub_to_analyze}"
    else:
        st.info("💡 Агрегований тренд для всієї мережі (Сумарне навантаження)")
        df_sub = df.copy()
        df_sub["timestamp"] = pd.to_datetime(df_sub["timestamp"])
        df_sub = df_sub.groupby("timestamp").agg({"actual_load_mw": "sum"}).reset_index()
        title_text = "Декомпозиція: Вся мережа"

    if not df_sub.empty and len(df_sub) > 48:
        df_sub["timestamp"] = pd.to_datetime(df_sub["timestamp"])
        df_sub = df_sub.sort_values("timestamp").set_index("timestamp").pipe(lambda x: x[~x.index.duplicated(keep="first")])
        resampled = df_sub["actual_load_mw"].resample("h").mean().ffill()

        if use_rel and resampled.max() > 0:
            resampled = resampled / resampled.max() * 100

        try:
            result = seasonal_decompose(resampled, model="additive", period=24)
            df_decomp = pd.DataFrame({
                "timestamp": resampled.index,
                "Тренд": result.trend.values, "Сезонність": result.seasonal.values, "Залишок": result.resid.values,
            }).melt(id_vars="timestamp", var_name="Компонент", value_name="Значення")

            fig = px.line(df_decomp, x="timestamp", y="Значення", facet_row="Компонент", color="Компонент",
                         template="plotly_dark", height=650, title=title_text)
            fig.update_yaxes(title_text="", matches=None)
            fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            safe_plotly_render(fig)
        except Exception as e:
            st.warning(f"Помилка розрахунку тренду: {e}")
    else:
        st.info("Недостатньо даних (потрібно > 48 годин).")
