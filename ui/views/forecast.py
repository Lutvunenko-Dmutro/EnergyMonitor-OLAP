"""
🔮 UNIFIED FORECAST VIEW — AI Energy Monitor Ultimate
Integrated dispatcher-style UI for the main Dashboard tab.
"""
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from utils.ui_helpers import safe_plotly_render
from ui.views.forecast_components.constants import MODEL_LABELS, MODEL_COLORS
from ui.views.forecast_components.audits import _render_comparative_audit, _render_group_comparison
from ui.views.forecast_components.layouts import render_single_forecast_results, render_backtest_execution_loop

from ml.forecast_controller import cached_ai_forecast as _cached_ai_forecast
from ml.forecast_controller import get_cached_history as _get_history
from ui.components.charts import _generate_mega_hybrid_figure, _generate_forecast_figure

def render(selected_substation="Усі підстанції", data_source="Live"):
    """
    Main entry point from dashboard.py
    """
    is_multi = isinstance(selected_substation, list) and len(selected_substation) > 1
    
    if is_multi:
        sub_name = selected_substation  
        sub_label = f"Група ({len(sub_name)} ПС)"
    else:
        if isinstance(selected_substation, list):
            sub_name = selected_substation[0] if selected_substation else "Усі підстанції"
        else:
            sub_name = selected_substation or "Усі підстанції"
        sub_label = sub_name

    src_type = "CSV" if "Kaggle" in data_source or "CSV" in data_source else "Live"

    st.markdown("### ⚡ Оперативний прогноз та аудит точності")
    col_cfg1, col_cfg2 = st.columns([2, 3])
    
    if src_type == "CSV":
        available_models = {"v1": "LSTM-v1 (1 ознака - Базова)"}
        model_notice = "💡 Для еталонних даних (Kaggle) використовується архітектура V1, оскільки CSV не містить телеметрії датчиків."
    else:
        available_models = MODEL_LABELS
        model_notice = None

    with col_cfg1:
        ver_label = st.selectbox(
            "🧠 Архітектура моделі", list(available_models.items()), 
            index=0, format_func=lambda x: x[1], key="tab_model_select"
        )
        version = ver_label[0]
    
    with col_cfg2:
        st.info(f"📍 Об'єкт: **{sub_label}** | 📡 Джерело: **{src_type}**")
        if model_notice: st.caption(model_notice)
        elif sub_name == "Усі підстанції": st.success("🌍 Режим: Мульти-Дашборд (Прогноз для всіх об'єктів системи)")
        elif is_multi: st.warning(f"⚖️ Режим: Груповий аналіз ({len(sub_name)} об'єктів)")

    if src_type != "CSV":
        with st.expander("⚙️ Параметри симуляції сценарію (Температура, Стан ПС)", expanded=False):
            s1, s2, s3 = st.columns(3)
            sim_temp   = s1.slider("🌡️ Температура (°C)", -20, 45, 15, key="tab_s_temp")
            sim_h2     = s2.slider("💨 H₂ (ppm)",          0, 500, 20, 5, key="tab_s_h2")
            sim_health = s3.slider("🩺 Стан обладн. (%)",   0, 100, 100, key="tab_s_health")
        scenario = {"air_temp": sim_temp, "h2_ppm": sim_h2, "health_score": sim_health}
    else:
        st.info("💡 Інтерактивна симуляція сценаріїв недоступна для еталонних даних (відсутні датчики).")
        scenario = {"air_temp": 15, "h2_ppm": 5, "health_score": 100}

    st.divider()

    c1, c2 = st.columns(2)
    btn_forecast = c1.button("⚡ Отримати прогноз", type="primary", use_container_width=True, key="tab_btn_fc")
    
    if sub_name == "Усі підстанції":
        bt_label = "🌍 Глобальний аудит системи (Всі ПС)"
        bt_help = "Запускає масовий перерахунок точності для кожної підстанції в базі даних для комплексного аналізу мережі."
    elif is_multi:
        bt_label = f"⚖️ Груповий аналіз ({len(sub_name)} ПС)"
        bt_help = "Порівнює навантаження обраних станцій на одному графіку для виявлення дисбалансів."
    else:
        if src_type == "CSV":
            bt_label = f"🎯 Детальний аудит точності V1 ({sub_name})"
            bt_help = f"Запускає глибоку перевірку базової моделі V1 на еталонних даних {sub_name}."
        else:
            bt_label = f"📊 Порівняти моделі для {sub_name}"
            bt_help = f"Виконує паралельний запуск V1, V2 та V3 для {sub_name}, щоб визначити найефективнішу архітектуру ШІ."
        
    btn_backtest = c2.button(bt_label, type="secondary", use_container_width=True, key="tab_btn_bt", help=bt_help)

    if btn_forecast:
        st.session_state["tab_active_mode"] = "forecast"
        st.session_state["bt_status"] = "stopped"
        for k in ["tab_metrics", "tab_sigma", "tab_bt_df", "tab_fc_df", "tab_hist_df"]:
            if k in st.session_state: del st.session_state[k]
            
        with st.spinner("🧠 Генерація прогнозу для групи..."):
            from src.core import database as db
            
            if sub_name == "Усі підстанції":
                if src_type == "CSV":
                    from src.core.kaggle_loader import load_kaggle_data
                    k_df = load_kaggle_data()
                    stations_to_process = k_df["substation_name"].unique().tolist() if not k_df.empty else []
                else:
                    sub_df = db.run_query("SELECT substation_name FROM Substations ORDER BY substation_name")
                    stations_to_process = sub_df["substation_name"].tolist() if not sub_df.empty else []
                
                hero_title = f"⚡ ГЛОБАЛЬНА СИСТЕМА — Сумарний прогноз ({version.upper()})"
                sub_id_for_hero = "Усі підстанції"
            elif is_multi:
                stations_to_process = sub_name 
                hero_title = f"⚖️ ГРУПА {len(sub_name)} ПС — Сумарний прогноз ({version.upper()})"
                sub_id_for_hero = sub_name 
            else:
                stations_to_process = [] 
                hero_title = f"📍 {sub_name} — Оперативний прогноз ({version.upper()})"
                sub_id_for_hero = sub_name

            if sub_name == "Усі підстанції" or is_multi:
                st.markdown(f"#### 🌍 {hero_title.split(' — ')[0]}")
                res_global = _cached_ai_forecast(
                    hours_ahead=24, substation_name=sub_id_for_hero, 
                    source_type=src_type, version=version, scenario=scenario
                )
                if res_global:
                    df_fc_g, _ = res_global
                    df_hist_g = _get_history(sub_id_for_hero, src_type)
                    fig_g = _generate_forecast_figure(
                        df_hist_g, df_fc_g, hero_title, version.upper()
                    )
                    safe_plotly_render(fig_g, key="hero_group_fc")
                
                if stations_to_process:
                    st.divider()
                    st.markdown("#### 🏢 Деталізація по об'єктах")
                    g_cols = st.columns(2)
                    for i, station in enumerate(stations_to_process):
                        res_s = _cached_ai_forecast(
                            hours_ahead=24, substation_name=station, 
                            source_type=src_type, version=version, scenario=scenario
                        )
                        if res_s:
                            df_f, _ = res_s
                            df_h = _get_history(station, src_type)
                            if not df_f.empty:
                                with g_cols[i % 2]:
                                    fig_s = _generate_forecast_figure(
                                        df_h, df_f, f"📍 {station}", version.upper()
                                    )
                                    fig_s.update_layout(height=350)
                                    safe_plotly_render(fig_s, key=f"grid_fc_{station}")
                                    st.divider()
                st.session_state["tab_active_mode"] = "multi_mode_finished"
            else:
                res_fc = _cached_ai_forecast(
                    hours_ahead=24, substation_name=sub_name, 
                    source_type=src_type, version=version, scenario=scenario
                )
                if res_fc:
                    df_fc, err = res_fc
                    df_hist = _get_history(sub_name, src_type)
                    if not err and not df_fc.empty:
                        st.session_state["tab_fc_df"] = df_fc
                        st.session_state["tab_hist_df"] = df_hist
                        st.session_state["tab_ver"] = version
                        st.session_state["tab_sub_lbl"] = sub_name
                    elif err: st.error(f"❌ {err}")

    if sub_name != "Усі підстанції" and st.session_state.get("tab_active_mode") == "forecast" and "tab_fc_df" in st.session_state:
        df_fc = st.session_state["tab_fc_df"]
        df_hist = st.session_state["tab_hist_df"]
        ver_lbl = st.session_state["tab_ver"].upper()
        sub_lbl = st.session_state["tab_sub_lbl"]
        
        render_single_forecast_results(df_fc, df_hist, ver_lbl, sub_lbl, src_type, version)

    if btn_backtest:
        from src.core import database as db
        from ml.forecast_controller import cached_fast_backtest
        st.session_state["tab_active_mode"] = "backtest"
        
        if sub_name == "Усі підстанції" or is_multi:
            st.session_state["bt_status"] = "multi_running"
            st.session_state["multi_bt_results"] = {}
            
            if sub_name == "Усі підстанції":
                if src_type == "CSV":
                    from src.core.kaggle_loader import load_kaggle_data
                    k_df = load_kaggle_data()
                    stations = k_df["substation_name"].unique().tolist() if not k_df.empty else []
                else:
                    sub_df = db.run_query("SELECT substation_name FROM Substations ORDER BY substation_name")
                    stations = sub_df["substation_name"].tolist() if not sub_df.empty else []
                pr_text = "🌍 Глобальний аудит системи..."
            else:
                stations = sub_name 
                pr_text = f"⚖️ Груповий аудит ({len(stations)} об'єктів)..."
            
            progress_bar = st.progress(0, text=pr_text)
            try:
                for i, station in enumerate(stations):
                    progress_bar.progress((i+1)/len(stations), text=f"📊 Аналіз точності: {station} ({i+1}/{len(stations)})")
                    res = cached_fast_backtest(station, version, src_type)
                    if res:
                        st.session_state["multi_bt_results"][station] = res
            except Exception as e:
                st.error(f"⚠️ Помилка виконання Аудиту: {e}")
            
            st.session_state["bt_status"] = "multi_finished"
            st.rerun()
        else:
            st.session_state["tab_active_mode"] = "comparison_audit"
            if "bt_status" in st.session_state: del st.session_state["bt_status"]
            st.rerun()

    if st.session_state.get("tab_active_mode") == "comparison_audit":
        _render_comparative_audit(sub_name, src_type)
        if st.button("⬅️ Повернутись до прогнозу"):
            st.session_state["tab_active_mode"] = "forecast"
            st.rerun()

    render_backtest_execution_loop(sub_name, version, src_type)
