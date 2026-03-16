import pandas as pd
import streamlit as st

from core.analytics.aggregator import (
    get_history_csv as _get_history_csv,
)
from core.analytics.aggregator import (
    get_history_live as _get_history_live,
)


def _cached_forecast(
    substation_name: str | None, source_type: str, version: str = "v3"
):
    """Генерує короткостроковий прогноз споживання електроенергії."""
    from ml.predict_v2 import get_ai_forecast

    return get_ai_forecast(
        hours_ahead=24,
        substation_name=substation_name,
        source_type=source_type,
        version=version,
    )


def _cached_backtest(
    substation_name: str | None, source_type: str, version: str = "v3"
):
    """Проводить бектестинг та розраховує MAPE."""
    from ml.backtest import get_backtest_metrics

    return get_backtest_metrics(
        substation_name=substation_name, source_type=source_type, version=version
    )


@st.fragment
def render_comparison(selected_subs, source_type, sub_all_list):
    """Візуалізація порівняльного аналізу похибок моделей."""
    if source_type == "CSV":
        return  # Для Kaggle даних доступна тільки V1

    st.divider()
    col_bt_title, col_bt_btn = st.columns([2, 1])

    with col_bt_title:
        st.markdown("### 🏆 Аналіз точності (Backtest MAPE)")
        st.caption(
            "Порівняння середньої абсолютної похибки (MAPE) трьох архітектур нейромережі..."
        )

    with col_bt_btn:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        compare_clicked = st.button(
            "📊 Порівняти моделі", type="primary", width="stretch"
        )

    if compare_clicked:
        with st.spinner("Проводимо бектест усіх архітектур..."):
            current_selected = selected_subs if selected_subs else []
            sub_list = sub_all_list

            if source_type == "Live" and not current_selected:
                st.warning("Будь ласка, оберіть хоча б одну підстанцію!")
            else:
                test_sub = (
                    current_selected[0]
                    if current_selected
                    else (sub_list[0] if sub_list else "AEP Region")
                )
                if test_sub == "Усі підстанції":
                    test_sub = sub_list[1] if len(sub_list) > 1 else "AEP Region"

                mape_v1, _ = _cached_backtest(test_sub, source_type, version="v1")
                mape_v2, _ = _cached_backtest(test_sub, source_type, version="v2")
                mape_v3, _ = _cached_backtest(test_sub, source_type, version="v3")

                col1, col2, col3 = st.columns(3)
                val_v1 = f"{mape_v1:.2f}%" if mape_v1 is not None else "Помилка"
                val_v2 = f"{mape_v2:.2f}%" if mape_v2 is not None else "Помилка"
                val_v3 = f"{mape_v3:.2f}%" if mape_v3 is not None else "Помилка"

                mapes = {"v1": mape_v1, "v2": mape_v2, "v3": mape_v3}
                valid_mapes = {k: v for k, v in mapes.items() if v is not None}
                best_model = (
                    min(valid_mapes, key=valid_mapes.get) if valid_mapes else None
                )

                col1.metric(
                    label="Відстала (V1) 🧠",
                    value=val_v1,
                    delta="- Кращий результат!" if best_model == "v1" else None,
                    delta_color="inverse",
                )
                col2.metric(
                    label="Погода+Залізо (V2) 🌤️",
                    value=val_v2,
                    delta="- Кращий результат!" if best_model == "v2" else None,
                    delta_color="inverse",
                )
                col3.metric(
                    label="Advanced+Час (V3) ⏱️",
                    value=val_v3,
                    delta="- Кращий результат!" if best_model == "v3" else None,
                    delta_color="inverse",
                )


@st.fragment
def render_forecast_results(selected_subs, source_type, selected_version):
    """Метод генерації та відображення результатів прогностування."""
    st.divider()
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        submit_button = st.button(
            "🚀 Побудувати прогноз", type="primary", width="stretch"
        )

    if not submit_button:
        st.info("Оберіть підстанції та натисніть 'Побудувати прогноз'.")
        return

    st.markdown("### 📊 Зведена таблиця (Live Update)")
    table_placeholder = st.empty()

    st.markdown("### 📈 Детальний аналіз прогнозу (Live Update)")
    cols = st.columns(3)
    chart_placeholders = [cols[i % 3].empty() for i in range(len(selected_subs))]

    results_summary = []
    status_placeholder = st.empty()
    status_placeholder.info("⏳ Генерую ШІ прогноз...")

    with st.spinner("🤖 ШІ розраховує прогнози. Результати з'являтимуться миттєво..."):
        for i, sub_label in enumerate(selected_subs):
            real_sub = None if sub_label == "Усі підстанції" else sub_label

            df_forecast, _ = _cached_forecast(
                real_sub, source_type, version=selected_version
            )
            df_hist = (
                _get_history_csv(real_sub)
                if source_type == "CSV"
                else _get_history_live(real_sub)
            )
            mape, _ = _cached_backtest(real_sub, source_type, version=selected_version)

            accuracy = max(0, 100 - mape) if mape is not None else None
            peak_mw = (
                df_forecast["predicted_load_mw"].max()
                if (
                    not df_forecast.empty and "predicted_load_mw" in df_forecast.columns
                )
                else None
            )
            curr_temp = (
                df_hist["temperature_c"].iloc[-1]
                if (not df_hist.empty and "temperature_c" in df_hist.columns)
                else None
            )
            curr_health = (
                df_hist["health_score"].iloc[-1]
                if (not df_hist.empty and "health_score" in df_hist.columns)
                else None
            )
            status_emoji = (
                "🟢"
                if curr_health and curr_health > 85
                else "🟡"
                if curr_health and curr_health > 60
                else "🔴"
                if curr_health
                else "⚪"
            )

            results_summary.append(
                {
                    "Регіон": sub_label,
                    "Стан": f"{status_emoji} {curr_health:.1f}%"
                    if curr_health is not None
                    else "N/A",
                    "Темп. (°C)": f"{curr_temp:.1f}"
                    if curr_temp is not None
                    else "N/A",
                    "Точність прогнозу (%)": f"{accuracy:.1f}%"
                    if accuracy is not None
                    else "N/A",
                    "Очікуваний Максимум (МВт)": f"{peak_mw:.2f}"
                    if peak_mw is not None
                    else "Помилка",
                }
            )
            df_summary = pd.DataFrame(results_summary)
            if source_type == "CSV":
                df_summary = df_summary.drop(
                    columns=["Стан", "Темп. (°C)"], errors="ignore"
                )
            table_placeholder.dataframe(df_summary, hide_index=True, width="stretch")

            if not df_hist.empty and not df_forecast.empty:
                df_hist["timestamp"] = pd.to_datetime(df_hist["timestamp"])
                df_hist = (
                    df_hist.resample("h", on="timestamp")
                    .mean(numeric_only=True)
                    .reset_index()
                )
                df_hist["type"] = "Історія"
                df_fc_plot = df_forecast.rename(
                    columns={"predicted_load_mw": "actual_load_mw"}
                )
                df_fc_plot["type"] = "Прогноз"
                df_merged = pd.concat([df_hist, df_fc_plot], ignore_index=True)

                from ui.components.charts import render_forecast_chart

                fig = render_forecast_chart(df_merged, sub_label)
                chart_placeholders[i].plotly_chart(fig, use_container_width=True)

    status_placeholder.success("✅ Усі прогнози успішно побудовано!")
