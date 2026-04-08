import os
import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go

from core.analytics.aggregator import (
    get_history_csv as _get_history_csv,
    get_history_live as _get_history_live,
)
from ui.components.charts import render_forecast_chart
from ml.predict_v2 import get_ai_forecast
from ml.backtest import get_backtest_metrics
from utils.ui_helpers import safe_plotly_render


def _cached_backtest(
    version: str, shared_values: np.ndarray, shared_last_ts: pd.Timestamp, 
    substation_name: str | None, source_type: str
):
    """Проводить бектестинг та розраховує MAPE за допомогою Shared Data."""
    from ml.backtest import get_backtest_metrics
    
    # Hard Fallback for ML core safety
    if not substation_name:
        substation_name = "Усі підстанції"

    # get_backtest_metrics повертає (rmse, mae, mape, rmse_a, error_msg, df_merged)
    res = get_backtest_metrics(
        version=version, 
        shared_values=shared_values, 
        shared_last_ts=shared_last_ts,
        substation_name=substation_name, 
        source_type=source_type
    )
    if res is None:
        return None, "Помилка ML (Backtest)", None
    # Повертаємо (mape, error_msg, df_merged), як того очікує решта UI
    return res[2], res[4], res[5]


@st.fragment
def render_comparison(selected_subs, source_type, sub_all_list):
    """Преміум-перегляд порівняльного аналізу точності (Backtest MAPE)."""
    if source_type == "CSV":
        return

    import os
    import plotly.graph_objects as go

    st.divider()

    # ── Заголовок секції ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom: 0.25rem;">
        <span style="font-size:1.5rem; font-weight:700;">🏆 Аналіз точності моделей</span><br>
        <span style="color:#aaa; font-size:0.88rem;">
            One-Step-Ahead Backtest · 168-годинна тестова вибірка · LSTM vs ARIMA (SARIMA Rolling)
        </span>
    </div>
    """, unsafe_allow_html=True)

    compare_clicked = st.button(
        "📊 Запустити порівняльний бектест усіх трьох архітектур",
        type="primary",
        width="stretch",
    )

    if not compare_clicked and "bt_results" not in st.session_state:
        st.info("💡 Натисніть кнопку, щоб порівняти точність LSTM v1, v2 та v3 на 168-годинній тестовій вибірці.")
        return

    if compare_clicked:
        # ── SHARED DATA PROVIDER ─────────────────────────────────────────────
        test_sub = (selected_subs[0] if selected_subs else None)
        if test_sub == "Усі підстанції":
            test_sub = None

        with st.spinner("⏳ Завантаження даних…"):
            from ml.vectorizer import get_latest_window
            shared_values, _, shared_last_ts, _ = get_latest_window(
                test_sub, source_type, version="v3",
                offset_hours=168, window_size=192,
            )

        if shared_values is None:
            st.error("❌ Недостатньо даних для бектесту. Перевірте підключення до БД.")
            return

        with st.spinner("🤖 Нейромережа обчислює 168-крокові прогнози…"):
            mape_v1, err_v1, df_v1 = _cached_backtest("v1", shared_values, shared_last_ts, test_sub, source_type)
            mape_v2, err_v2, df_v2 = _cached_backtest("v2", shared_values, shared_last_ts, test_sub, source_type)
            mape_v3, err_v3, df_v3 = _cached_backtest("v3", shared_values, shared_last_ts, test_sub, source_type)

        st.session_state["bt_results"] = {
            "mape_v1": mape_v1, "mape_v2": mape_v2, "mape_v3": mape_v3,
            "df_v1": df_v1, "df_v2": df_v2, "df_v3": df_v3,
            "err_v1": err_v1, "err_v2": err_v2, "err_v3": err_v3,
        }

    # ── Читаємо з session_state ───────────────────────────────────────────────
    r = st.session_state["bt_results"]
    mape_v1, mape_v2, mape_v3 = r["mape_v1"], r["mape_v2"], r["mape_v3"]
    df_v1, df_v2, df_v3       = r["df_v1"],   r["df_v2"],   r["df_v3"]

    # Показуємо помилки тихо
    for v, e in [("V1", r["err_v1"]), ("V2", r["err_v2"]), ("V3", r["err_v3"])]:
        if e:
            st.warning(f"⚠️ {v}: {e}")

    mapes = {"v1": mape_v1, "v2": mape_v2, "v3": mape_v3}
    valid = {k: v for k, v in mapes.items() if v is not None}
    if not valid:
        st.error("Усі три моделі повернули помилки. Перевірте логи.")
        return

    best = min(valid, key=valid.get)

    # ── Модель-переможець — велика картка ─────────────────────────────────────
    model_colors = {"v1": "#ff9f43", "v2": "#ee5253", "v3": "#10ac84"}
    model_names  = {"v1": "Базова LSTM (1 ознака)", "v2": "Мультисенсорна (5 ознак)", "v3": "Smart-City (9 ознак)"}
    bc = model_colors[best]

    st.markdown(f"""
    <div style="
        border: 2px solid {bc};
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1.2rem 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
        display: flex; align-items: center; gap: 1.2rem;
    ">
        <div style="font-size:3rem; line-height:1;">🏅</div>
        <div>
            <div style="font-size:0.8rem; color:{bc}; font-weight:700; text-transform:uppercase; letter-spacing:1px;">
                Переможець · Найнижча MAPE
            </div>
            <div style="font-size:1.7rem; font-weight:800; color:#fff; line-height:1.2;">
                {best.upper()} — {model_names[best]}
            </div>
            <div style="font-size:1.1rem; color:{bc}; margin-top:0.2rem;">
                MAPE = <strong>{valid[best]:.2f}%</strong>
                &nbsp;·&nbsp; Точність = <strong>{100 - valid[best]:.2f}%</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 3 картки моделей ──────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    for col, ver, df_bt in [(c1, "v1", df_v1), (c2, "v2", df_v2), (c3, "v3", df_v3)]:
        clr  = model_colors[ver]
        mape = mapes[ver]
        is_win = (ver == best)
        badge = "👑 WIN" if is_win else ""

        with col:
            st.markdown(f"""
            <div style="
                border-left: 5px solid {clr};
                border-radius: 8px;
                padding: 0.9rem 1rem;
                background: rgba(255,255,255,0.03);
                min-height: 110px;
            ">
                <div style="font-size:0.7rem; color:{clr}; font-weight:700; text-transform:uppercase; letter-spacing:1px;">
                    {ver.upper()} &nbsp;{badge}
                </div>
                <div style="font-size:0.85rem; color:#ccc; margin-top:0.1rem;">
                    {model_names[ver]}
                </div>
                <div style="font-size:2rem; font-weight:800; color:#fff; margin-top:0.4rem; line-height:1;">
                    {"—" if mape is None else f"{mape:.2f}%"}
                </div>
                <div style="font-size:0.75rem; color:#888; margin-top:0.15rem;">MAPE (нижче = краще)</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    # ── Plotly: One-Step-Ahead Comparison кращої моделі ───────────────────────
    df_best = {"v1": df_v1, "v2": df_v2, "v3": df_v3}[best]
    if df_best is not None and not df_best.empty:
        st.markdown(f"#### 📈 One-Step-Ahead — {best.upper()} (кращий результат, 168 годин)")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_best["timestamp"], y=df_best["actual_load_mw"],
            name="Фактичне навантаження",
            mode="lines",
            line=dict(color="#ff9f43", width=2.5),
            hovertemplate="Факт: %{y:.0f} МВт<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=df_best["timestamp"], y=df_best["predicted_load_mw"],
            name=f"LSTM {best.upper()} One-Step",
            mode="lines",
            line=dict(color="#ee5253", width=2.5, dash="dash"),
            hovertemplate="Прогноз: %{y:.0f} МВт<extra></extra>",
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14,17,23,1)",
            height=420,
            hovermode="x unified",
            margin=dict(l=10, r=10, t=45, b=10),
            title=dict(
                text=f"One-Step-Ahead Forecast vs Actual — {best.upper()}  |  MAPE={valid[best]:.2f}%",
                font=dict(size=15, color="#ccc"), x=0.01,
            ),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", title="Час (7 днів)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", title="МВт"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        bgcolor="rgba(0,0,0,0)"),
        )
        safe_plotly_render(fig)

    # ── Academic PNG charts у табах ───────────────────────────────────────────
    st.divider()
    with st.expander("📸 Академічні графіки (LSTM vs ARIMA · для дипломного звіту)", expanded=False):
        st.caption("Розподіл Гаусових похибок та часовий ряд One-Step-Ahead для кожної архітектури. "
                   "Доводять перевагу нейромережевого підходу над класичним SARIMA.")

        tab_v1, tab_v2, tab_v3 = st.tabs(["V1 — Baseline", "V2 — Sensors", "V3 — Smart City ⭐"])

        def _render_imgs(v):
            fp_dist = f"lstm_error_dist_{v}.png"
            fp_comp = f"forecast_comparison_{v}.png"
            if os.path.exists(fp_dist) and os.path.exists(fp_comp):
                a, b = st.columns(2)
                a.image(fp_dist, caption=f"Розподіл похибок — {v.upper()}", width="stretch")
                b.image(fp_comp, caption=f"One-Step-Ahead — {v.upper()}", width="stretch")
            else:
                st.info(f"Графіки для {v.upper()} ще не згенеровані. Запустіть `scripts/baseline_arima.py`.")

        with tab_v1: _render_imgs("v1")
        with tab_v2: _render_imgs("v2")
        with tab_v3: _render_imgs("v3")


@st.cache_data(ttl=600)
def get_forecast_context(substation_name, source_type, version):
    """
    Unified Data Provider: завантажує всі дані для прогнозу за один раз.
    Повертає (df_forecast, df_hist, mape, capacity_mw, err)
    """
    # Hard Fallback for ML core safety
    if not substation_name:
        substation_name = "Усі підстанції"
    # 1. Прогноз
    res_fc = get_ai_forecast(
        hours_ahead=24, substation_name=substation_name, 
        source_type=source_type, version=version
    )
    if res_fc is None:
        return pd.DataFrame(), None, None, 1000.0, "Помилка ML (Forecast)"
    df_forecast, err = res_fc
    
    # 2. Історія (для графіка)
    df_hist = _get_history_csv(substation_name) if source_type == "CSV" else _get_history_live(substation_name)
    
    # 3. Точність (Backtest) — беремо з Shared Data Provider
    mape = None
    try:
        from ml.vectorizer import get_latest_window
        test_size = 168
        window_size = 24
        shared_values, _, shared_last_ts, _ = get_latest_window(
            substation_name, source_type, version="v3",
            offset_hours=test_size,
            window_size=window_size + test_size
        )
        if shared_values is not None:
            bt_res = get_backtest_metrics(
                version=version,
                shared_values=shared_values,
                shared_last_ts=shared_last_ts,
                substation_name=substation_name,
                source_type=source_type,
            )
            if bt_res is not None:
                mape = bt_res[2]
    except Exception:
        mape = None
    
    # 4. Місткість (Capacity)
    from src.core.database import run_query
    if substation_name:
        cap_q = "SELECT capacity_mw FROM Substations WHERE substation_name = :sub"
        cap_df = run_query(cap_q, {"sub": substation_name})
    else:
        cap_q = "SELECT SUM(capacity_mw) as capacity_mw FROM Substations"
        cap_df = run_query(cap_q)
    
    capacity_mw = cap_df["capacity_mw"].iloc[0] if not cap_df.empty else 1000.0
    
    return df_forecast, df_hist, mape, capacity_mw, err

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

    st.markdown("### 📊 Зведена таблиця (Unified Context)")
    table_placeholder = st.empty()

    st.markdown("### 📈 Детальний аналіз прогнозу")
    cols = st.columns(3)
    chart_placeholders = [cols[i % 3].empty() for i in range(len(selected_subs))]

    results_summary = []
    status_placeholder = st.empty()
    status_placeholder.info("⏳ Запит до Unified Data Provider...")

    with st.spinner("🤖 ШІ розраховує прогнози..."):
        for i, sub_label in enumerate(selected_subs):
            # Hard Fallback for ML core safety (No None passed)
            real_sub = sub_label if sub_label and sub_label != "Усі підстанції" else "Усі підстанції"

            # ВИКОРИСТОВУЄМО ОДИН ВИКЛИК ЗАМІСТЬ ТРЬОХ (Оптимізація)
            df_forecast, df_hist, mape, capacity_mw, err = get_forecast_context(
                real_sub, source_type, selected_version
            )

            if err:
                st.error(f"Помилка для {sub_label}: {err}")
                continue

            accuracy = max(0, 100 - mape) if mape is not None else None
            peak_mw = df_forecast["predicted_load_mw"].max() if not df_forecast.empty else None
            
            # Розрахунок стану безпеки (Health Score)
            curr_health = (df_hist["health_score"].iloc[-1] 
                           if not df_hist.empty and "health_score" in df_hist.columns else 100.0)
            
            # Визначаємо статус базуючись на відношенні прогнозу до місткості
            load_factor = (peak_mw / capacity_mw * 100) if capacity_mw and peak_mw else 0
            status_emoji = "🟢" if load_factor < 70 else "🟡" if load_factor < 90 else "🔴"

            results_summary.append({
                "Регіон": sub_label,
                "Завантаження (%)": f"{load_factor:.1f}%",
                "Здоров'я систем": f"{curr_health:.1f}%",
                "Точність (%)": f"{accuracy:.1f}%" if accuracy else "N/A",
                "Пік (МВт)": f"{peak_mw:.2f}" if peak_mw else "N/A",
                "Ліміт (МВт)": f"{capacity_mw:.0f}"
            })
            
            table_placeholder.dataframe(pd.DataFrame(results_summary), hide_index=True, width="stretch")

            if not df_hist.empty and not df_forecast.empty:
                # Зшивання для Plotly (вже оброблено в ML engine, просто готуємо дані)
                df_hist_plot = df_hist.copy()
                df_hist_plot["type"] = "Історія"
                
                df_fc_plot = df_forecast.copy()
                # Перейменовуємо для сумісності з Plotly (actual_load_mw очікується в render_forecast_chart)
                df_fc_plot = df_fc_plot.rename(columns={"predicted_load_mw": "actual_load_mw"})
                df_fc_plot["type"] = "Прогноз"
                
                df_merged = pd.concat([df_hist_plot, df_fc_plot], ignore_index=True)
                fig = render_forecast_chart(df_merged, sub_label)
                safe_plotly_render(fig, container=chart_placeholders[i])

    status_placeholder.success("✅ Усі прогнози успішно побудовано!")
