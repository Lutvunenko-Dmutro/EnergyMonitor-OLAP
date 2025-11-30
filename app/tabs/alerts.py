import streamlit as st
import database as db
import pandas as pd

def render(df_alerts):
    """Панель інцидентів з розширеним керуванням (Optimized)."""
    st.subheader("🚨 Журнал інцидентів")
    
    # Синхронізація стану
    st.session_state["raw_alerts_df"] = df_alerts
    
    # --- БЛОК СТВОРЕННЯ АВАРІЇ ---
    with st.expander("🔥 Зареєструвати новий інцидент (Симуляція)", expanded=False):
        with st.form("new_alert_form"):
            c1, c2 = st.columns(2)
            
            # Оптимізований вибір підстанцій (використовуємо існуючі дані з df_alerts, якщо є)
            if not df_alerts.empty:
                sub_options = sorted(df_alerts['substation_name'].unique().tolist())
            else:
                sub_options = ["ПС Київська", "ПС Львівська"] # Fallback

            with c1:
                selected_sub = st.selectbox("📍 Об'єкт", sub_options)
                selected_type = st.selectbox("⚠️ Тип", ["Перевантаження", "Відмова обладнання", "Пожежа", "Кібератака"])
            
            with c2:
                desc = st.text_area("📝 Опис", "Зафіксовано аномалію...")
                
            if st.form_submit_button("🚀 Створити", type="primary"):
                db.create_custom_alert(selected_sub, selected_type, desc)
                st.success("Інцидент зареєстровано!")
                st.cache_data.clear()
                st.rerun()

    # --- KPI ---
    if not df_alerts.empty:
        k1, k2, k3 = st.columns(3)
        # Швидкий підрахунок
        counts = df_alerts['status'].value_counts()
        
        k1.metric("Всього", len(df_alerts))
        k2.metric("Активні", int(counts.get('NEW', 0)), delta="Увага", delta_color="inverse")
        k3.metric("Вирішено", int(counts.get('RESOLVED', 0)), delta="OK")
    
    # --- ТАБЛИЦЯ ---
    st.data_editor(
        df_alerts[['alert_id', 'timestamp', 'region_name', 'substation_name', 'alert_type', 'description', 'status']],
        use_container_width=True, 
        hide_index=True,
        column_config={
            "timestamp": st.column_config.DatetimeColumn("Час", format="DD.MM HH:mm"),
            "status": st.column_config.SelectboxColumn("Статус", options=["NEW", "ACKNOWLEDGED", "RESOLVED"], required=True)
        },
        disabled=['alert_id', 'timestamp', 'region_name', 'substation_name', 'alert_type', 'description'],
        key="alerts_editor",
        on_change=save_alert_changes
    )

def save_alert_changes():
    """Зберігає зміни статусів."""
    if "alerts_editor" in st.session_state and "raw_alerts_df" in st.session_state:
        changes = st.session_state["alerts_editor"]["edited_rows"]
        df = st.session_state["raw_alerts_df"]
        
        for idx, change in changes.items():
            if "status" in change:
                alert_id = df.iloc[idx]['alert_id']
                db.update_alert_status(alert_id, change["status"])
        
        st.cache_data.clear()