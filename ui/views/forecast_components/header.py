import streamlit as st
from ui.views.forecast_components.constants import MODEL_LABELS

def render_forecast_header(sub_name, sub_label, data_source):
    """
    Renders the configuration header and manages station change detection.
    """
    # 1. Advanced Change Detector
    if "last_sub_selection" not in st.session_state:
        st.session_state["last_sub_selection"] = sub_name
    if "last_data_source" not in st.session_state:
        st.session_state["last_data_source"] = data_source
    if "last_version" not in st.session_state:
        st.session_state["last_version"] = None 
    if "last_multi_mode" not in st.session_state:
        st.session_state["last_multi_mode"] = False

    # Detection logic
    src_type = "CSV" if "Kaggle" in data_source or "CSV" in data_source else "Live"
    
    st.markdown("### ⚡ Оперативний прогноз та аудит точності")
    col1, col2 = st.columns([2, 3])
    
    with col1:
        is_multi_model = st.toggle("🧪 Порівняльний аналіз (Всі моделі)", value=False, key="tab_multi_model_toggle")
        available_models = {"v1": "LSTM-v1 (Базова)"} if src_type == "CSV" else MODEL_LABELS
        ver_label = st.selectbox(
            "🧠 Архітектура моделі", list(available_models.items()), 
            index=0, format_func=lambda x: x[1], key="tab_model_select",
            disabled=is_multi_model
        )
        version = ver_label[0]

    # Check for changes in fundamental state
    changed = (st.session_state["last_sub_selection"] != sub_name or 
               st.session_state["last_data_source"] != data_source or
               st.session_state["last_version"] != version or
               st.session_state["last_multi_mode"] != is_multi_model)
               
    if changed:
        st.session_state["tab_active_mode"] = "idle"
        st.session_state["last_sub_selection"] = sub_name
        st.session_state["last_data_source"] = data_source
        st.session_state["last_version"] = version
        st.session_state["last_multi_mode"] = is_multi_model
        
        # Comprehensive wipe
        keys_to_clear = [
            "tab_fc_df", "tab_multi_fc_results", "tab_hist_df", "tab_metrics", 
            "tab_sigma", "tab_bt_df", "tab_bt_metrics", "bt_status", "bt_idx", 
            "bt_preds", "bt_shared_data", "multi_bt_results"
        ]
        for k in keys_to_clear:
            if k in st.session_state: del st.session_state[k]
        st.rerun()
    
    with col2:
        st.info(f"📍 Об'єкт: **{sub_label}** | 📡 Джерело: **{src_type}**")
        if is_multi_model: st.warning("⚡ Режим порівняння активний")

    # 2. Scenario Parameters
    scenario = {"air_temp": 15, "h2_ppm": 5, "health_score": 100}
    if src_type != "CSV" and (version != "v1" or is_multi_model):
        with st.expander("⚙️ Параметри симуляції сценарію", expanded=False):
            s1, s2, s3 = st.columns(3)
            sim_temp = s1.slider("🌡️ Температура (°C)", -20, 45, 15, key="tab_s_temp")
            sim_h2 = s2.slider("💨 H₂ (ppm)", 0, 500, 20, 5, key="tab_s_h2")
            sim_health = s3.slider("🩺 Стан обладн. (%)", 0, 100, 100, key="tab_s_health")
            scenario = {"air_temp": sim_temp, "h2_ppm": sim_h2, "health_score": sim_health}
            
    return version, scenario, is_multi_model, src_type
