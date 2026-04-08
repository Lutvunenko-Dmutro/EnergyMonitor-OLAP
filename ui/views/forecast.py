"""
🔮 UNIFIED FORECAST VIEW — AI Energy Monitor Ultimate
Integrated dispatcher-style UI for the main Dashboard tab.
"""
import streamlit as st
from utils.ui_helpers import safe_plotly_render
from ui.views.forecast_components.header import render_forecast_header
from ui.views.forecast_components.engine import run_reactive_forecast_engine, get_stations_to_process
from ui.views.forecast_components.grid import render_substation_grid
from ui.views.forecast_components.audits import _render_comparative_audit
from ui.views.forecast_components.layouts import render_single_forecast_results, render_backtest_execution_loop
from ml.forecast_controller import get_cached_history as _get_history
from ui.components.charts import _generate_forecast_figure, _generate_multi_forecast_figure

def render(selected_substation="Усі підстанції", data_source="Live"):
    """Main entry point for the Forecast & Audit tab."""
    # 1. Normalize Substation Selection
    is_multi = isinstance(selected_substation, list) and len(selected_substation) > 1
    if is_multi:
        sub_name, sub_label = selected_substation, f"Група ({len(selected_substation)} ПС)"
    else:
        sub_name = (selected_substation[0] if isinstance(selected_substation, list) and selected_substation 
                   else selected_substation or "Усі підстанції")
        sub_label = sub_name

    # 2. Render Header & get configuration
    version, scenario, is_multi_model, src_type = render_forecast_header(sub_name, sub_label, data_source)
    st.divider()

    # 3. Control Buttons
    c1, c2 = st.columns(2)
    btn_forecast = c1.button("⚡ Отримати прогноз", type="primary", width='stretch', key="tab_btn_fc")
    btn_backtest = c2.button("📊 Аудит точності", type="secondary", width='stretch', key="tab_btn_bt")

    if btn_forecast:
        st.session_state["tab_active_mode"] = "forecast"
        for k in ["tab_metrics", "tab_fc_df", "tab_hist_df", "tab_multi_fc_results"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

    # 4. Reactive Engine Dispatch
    active_mode = st.session_state.get("tab_active_mode")
    if active_mode in ["forecast", "multi_mode_finished", "multi_forecast_view"]:
        with st.spinner("🧠 Оновлення сценарію ШІ..."):
            stations_to_process = get_stations_to_process(sub_name, src_type)
            sub_id_hero = "Усі підстанції" if sub_name == "Усі підстанції" else sub_name
            hero_title = f"⚡ ГЛОБАЛЬНА СИСТЕМА ({version.upper()})" if sub_name == "Усі підстанції" else f"📍 {sub_label}"

            multi_hero, res_fc, multi_results = run_reactive_forecast_engine(
                sub_name, sub_id_hero, version, src_type, scenario, is_multi_model
            )

            if sub_name == "Усі підстанції" or is_multi:
                st.markdown(f"#### 🌍 {hero_title}")
                if is_multi_model:
                    fig_g = _generate_multi_forecast_figure(_get_history(sub_id_hero, src_type), multi_hero, hero_title)
                    safe_plotly_render(fig_g, key="hero_group_fc_multi")
                elif res_fc:
                    fig_g = _generate_forecast_figure(_get_history(sub_id_hero, src_type), res_fc[0], hero_title, version.upper())
                    safe_plotly_render(fig_g, key="hero_group_fc_single")
                render_substation_grid(stations_to_process, src_type, version, scenario, is_multi_model)
                st.session_state["tab_active_mode"] = "multi_mode_finished"
            else:
                if is_multi_model and multi_results:
                    st.session_state["tab_multi_fc_results"], st.session_state["tab_hist_df"] = multi_results, _get_history(sub_name, src_type)
                    st.session_state["tab_active_mode"] = "multi_forecast_view"
                elif res_fc:
                    df_fc, err = res_fc
                    if not err:
                        st.session_state["tab_fc_df"], st.session_state["tab_hist_df"] = df_fc, _get_history(sub_name, src_type)
                        st.session_state["tab_ver"], st.session_state["tab_sub_lbl"] = version, sub_name
                    else: st.error(err)

    # 5. Result Rendering (Mutually Exclusive Modes)
    current_mode = st.session_state.get("tab_active_mode")
    
    if current_mode == "comparison_audit":
        # Render Audit first to show 'how it counts' on a clean slate
        _render_comparative_audit(sub_name, src_type)
        
    elif current_mode == "multi_forecast_view" and "tab_multi_fc_results" in st.session_state:
        fig_m = _generate_multi_forecast_figure(st.session_state["tab_hist_df"], st.session_state["tab_multi_fc_results"], f"Порівняння: {sub_name}")
        safe_plotly_render(fig_m, key="multi_ver_fc_chart")
    
    elif current_mode == "forecast" and "tab_fc_df" in st.session_state and sub_name != "Усі підстанції":
        render_single_forecast_results(st.session_state["tab_fc_df"], st.session_state["tab_hist_df"], st.session_state["tab_ver"].upper(), st.session_state["tab_sub_lbl"], src_type, version)

    # 6. Backtest Logic
    if btn_backtest:
        from ml.forecast_controller import cached_fast_backtest
        # Switch to audit mode and clear forecast UI
        st.session_state["tab_active_mode"] = "audit"
        for k in ["tab_fc_df", "tab_multi_fc_results", "tab_hist_df", "tab_metrics"]:
            if k in st.session_state: del st.session_state[k]

        if sub_name == "Усі підстанції" or is_multi:
            stations = get_stations_to_process(sub_name, src_type)
            results = {}
            with st.status("🌍 Глобальний аудит мережі...", expanded=True) as status:
                p_bar = st.progress(0, text="Ініціалізація...")
                for i, s in enumerate(stations):
                    p_bar.progress((i + 1) / len(stations), text=f"Аналіз об'єкта: {s}...")
                    results[s] = cached_fast_backtest(s, version, src_type)
                status.update(label="✅ Глобальний аудит завершено!", state="complete")
                p_bar.empty()
            
            st.session_state["multi_bt_results"] = results
            st.session_state["bt_status"] = "multi_finished"
            st.session_state["tab_active_mode"] = "multi_audit_view"
        else:
            st.session_state["tab_active_mode"] = "comparison_audit"
        st.rerun()

    # 7. Final background loops
    render_backtest_execution_loop(sub_name, version, src_type)
    
    # Гарантований відступ внизу для скролінгу всього дашборду
    st.markdown('<div style="height: 300px;"></div>', unsafe_allow_html=True)
