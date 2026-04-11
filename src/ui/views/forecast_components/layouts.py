import pandas as pd
import streamlit as st
from src.utils.ui_helpers import safe_plotly_render
from src.ui.components.charts import _generate_mega_hybrid_figure
from src.ml.forecast_controller import calculate_instant_metrics as _calculate_instant_metrics

def render_single_forecast_results(df_fc, df_hist, ver_lbl, sub_lbl, src_type, version):
    """Renders the detailed post-forecast accuracy audit and mega chart."""
    if "tab_bt_df" not in st.session_state:
        from src.ml.backtest import get_fast_backtest
        with st.status("🔍 Формування Мега-Графіка Потокової Аналітики..."):
            metrics, sigma = _calculate_instant_metrics(df_hist, version, sub_lbl, src_type)
            st.session_state["tab_metrics"] = metrics
            st.session_state["tab_sigma"] = sigma
            
            bt_res = get_fast_backtest(sub_lbl, version, src_type, offset_hours=0)
            if bt_res:
                _, _, _, _, _, df_bt = bt_res
                st.session_state["tab_bt_df"] = df_bt
            
            if not df_fc.empty:
                df_fc["upper_bond"] = df_fc["predicted_load_mw"] + (1.96 * sigma)
                df_fc["lower_bond"] = df_fc["predicted_load_mw"] - (1.96 * sigma)
            st.session_state["tab_fc_df"] = df_fc

    metrics = st.session_state.get("tab_metrics")
    df_bt = st.session_state.get("tab_bt_df")
    sigma = st.session_state.get("tab_sigma", 0.05)

    if df_bt is not None and not df_bt.empty:
        max_ts = df_fc["timestamp"].min()
        df_bt = df_bt[df_bt["timestamp"] >= (max_ts - pd.Timedelta(hours=168))]
        df_bt = df_bt[df_bt["timestamp"] <= max_ts]

    fig = _generate_mega_hybrid_figure(
        df_bt, df_fc, 
        f"⚡ {sub_lbl} — Потокова аналітика (7д Бектест + 1д Прогноз)", ver_lbl
    )
    safe_plotly_render(fig, key="mega_flow_chart")

    v = df_fc["predicted_load_mw"]
    last_real = float(df_hist["actual_load_mw"].iloc[-1]) if not df_hist.empty else None
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Зараз (факт)", f"{last_real:.1f} МВт" if last_real else "—")
    m2.metric("Пік (прогноз)", f"{v.max():.1f} МВт")
    m3.metric("Сер. темп помилки", f"±{sigma:.1f} МВт")
    m4.metric("Статус", "✅ Модель калібрована" if (metrics and metrics['r2'] > 0.8) else "⚠️ Потребує уваги")

    if metrics:
        st.info(f"📊 **Аудит точності на основі останніх 24 годин телеметрії:**")
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Точність (R²)", f"{metrics['r2']:.4f}")
        a2.metric("RMSE", f"{metrics['rmse']:.2f} МВт")
        a3.metric("MAE", f"{metrics['mae']:.2f} МВт", delta=f"{metrics['mae']-sigma:.1f}", delta_color="inverse")
        a4.metric("Довіра до прогнозу", f"{metrics['confidence']:.1f}%")
        
        with st.expander("📚 Додаткова математична аналітика точності", expanded=False):
            from src.ui.components.charts import generate_academic_plots
            df_bt = st.session_state.get("tab_bt_df")
            
            if df_bt is not None and not df_bt.empty:
                _, f_dist, f_scat = generate_academic_plots(df_bt)
                
                tc1, tc2 = st.columns(2)
                with tc1: safe_plotly_render(f_dist, key=f"hybrid_dist_{sub_lbl}")
                with tc2: safe_plotly_render(f_scat, key=f"hybrid_scat_{sub_lbl}")
            else:
                st.warning("⚠️ Академічні графіки недоступні (необхіден бектест).")

def render_backtest_execution_loop(sub_name, version, src_type):
    """Renders the iterative background backtest processing UI."""
    if st.session_state.get("bt_status") in ["running", "paused"]:
        from src.ml.backtest import run_backtest_step
        sv, slts = st.session_state["bt_shared_data"]
        curr_idx = st.session_state["bt_idx"]
        cl1, cl2, cl3 = st.columns([2, 1, 1])
        cl1.progress(curr_idx / 168, text=f"Обчислення: {curr_idx}/168 кроків...")
        
        if st.session_state["bt_status"] == "running":
            if cl2.button("⏸ Пауза"): st.session_state["bt_status"] = "paused"; st.rerun()
        else:
            if cl2.button("▶️ Продовжити"): st.session_state["bt_status"] = "running"; st.rerun()
            
        if cl3.button("⏹ Зупинити"): st.session_state["bt_status"] = "stopped"; st.rerun()

        if st.session_state["bt_status"] == "running":
            batch = run_backtest_step(version, sv, curr_idx, batch_size=24)
            if batch:
                st.session_state["bt_preds"].extend(batch)
                st.session_state["bt_idx"] += len(batch)
                if st.session_state["bt_idx"] >= 168: st.session_state["bt_status"] = "finalizing"
                st.rerun()
            else:
                st.session_state["bt_status"] = "finalizing"
                st.rerun()

    if st.session_state.get("bt_status") == "finalizing":
        from src.ml.backtest import finalize_backtest_metrics
        sv, slts = st.session_state["bt_shared_data"]
        all_preds = st.session_state["bt_preds"]
        with st.spinner("Фіналізація метрик..."):
            res = finalize_backtest_metrics(version, all_preds, sv, slts, sub_name, src_type)
            if res:
                rmse, mae, mape, r2, err, df_bt = res
                st.session_state["tab_bt_df"] = df_bt
                st.session_state["tab_bt_metrics"] = (rmse, mae, mape, r2)
                st.session_state["bt_status"] = "finished"
                st.rerun()
            else: st.session_state["bt_status"] = "stopped"

    if st.session_state.get("bt_status") == "multi_finished":
        st.success("🌍 Мульти-Бектест: Глибинна аналітика для всіх об'єктів")
        results = st.session_state.get("multi_bt_results", {})
        from src.ui.components.charts import generate_academic_plots
        for station, res_data in results.items():
            rmse, mae, mape, r2, _, df_bt = res_data
            with st.expander(f"📍 Аналітика точності: {station} (R²={r2:.4f})", expanded=False):
                st.markdown(f"**Метрики для {station}:** RMSE={rmse:.1f} | MAE={mae:.1f} | MAPE={mape:.2f}%")
                f_trend, f_dist, f_scat = generate_academic_plots(df_bt)
                safe_plotly_render(f_trend, key=f"bt_trend_{station}")
                col_a, col_b = st.columns(2)
                with col_a: safe_plotly_render(f_dist, key=f"bt_dist_{station}")
                with col_b: safe_plotly_render(f_scat, key=f"bt_scat_{station}")

    if st.session_state.get("bt_status") == "finished" and "tab_bt_df" in st.session_state:
        from src.ui.components.charts import generate_academic_plots
        df_bt = st.session_state["tab_bt_df"]
        rmse, mae, mape, r2 = st.session_state["tab_bt_metrics"]
        sub_lbl = st.session_state.get("tab_sub_lbl", sub_name)
        
        st.markdown(f"#### 🎓 Академічний звіт бектесту — Об'єкт: {sub_lbl}")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("RMSE", f"{rmse:.1f}"); k2.metric("MAE", f"{mae:.1f}")
        k3.metric("MAPE", f"{mape:.2f}%"); k4.metric("Коефіцієнт R²", f"{r2:.4f}")

        fig_trend, fig_dist, fig_scatter = generate_academic_plots(df_bt)
        tb1, tb2, tb3 = st.tabs(["📈 Часові ряди", "📊 Розподіл помилок", "🔵 Кореляція (Scatter)"])
        with tb1: safe_plotly_render(fig_trend, key="bt_academic_trend")
        with tb2: safe_plotly_render(fig_dist, key="bt_academic_dist")
        with tb3: safe_plotly_render(fig_scatter, key="bt_academic_scatter")
