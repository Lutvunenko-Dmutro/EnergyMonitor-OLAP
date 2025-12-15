import streamlit as st
import database as db
import time
import pandas as pd

def render(df_alerts):
    """
    Рендеринг вкладки керування аваріями.
    Функціонал:
    1. Адмін-панель (Додавання/Очистка) у згорнутому стані.
    2. Інтерактивна таблиця для зміни статусів аварій.
    """
    st.subheader("🚨 Центр керування аваріями")

    # --- 1. ПАНЕЛЬ КЕРУВАННЯ (Admin Tools) ---
    # Згорнутий блок для економії місця на екрані
    with st.expander("🛠️ Панель дій (Додати / Очистити)", expanded=False):
        tab_add, tab_clean = st.tabs(["➕ Додати запис", "🗑️ Очистка бази"])
        
        # Вкладка 1: Форма додавання
        with tab_add:
            with st.form("quick_add_form"):
                c1, c2 = st.columns(2)
                
                # Завантаження актуального списку підстанцій
                subs_df = db.run_query("SELECT substation_name FROM Substations ORDER BY substation_name")
                sub_options = subs_df['substation_name'].tolist() if not subs_df.empty else ["Немає даних"]
                
                selected_sub = c1.selectbox("Об'єкт", sub_options)
                selected_type = c1.selectbox("Тип", ["Перевантаження", "Аварія", "Кібер-атака", "Пожежа"])
                input_desc = c2.text_input("Короткий опис", "Фіксація інциденту")
                
                if st.form_submit_button("Створити", type="primary"):
                    success, msg = db.create_custom_alert(selected_sub, selected_type, input_desc)
                    if success:
                        st.toast("✅ Додано! Перевірте таблицю нижче.", icon="📅")
                        st.cache_data.clear()
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(msg)

        # Вкладка 2: Інструменти очистки
        with tab_clean:
            st.caption("Інструмент для видалення старих тестових даних.")
            if st.button("🧹 Залишити тільки 10 останніх записів"):
                db.cleanup_old_alerts(keep_last=10)
                st.toast("База очищена!", icon="🗑️")
                st.cache_data.clear()
                time.sleep(0.5)
                st.rerun()

    # --- 2. ГОЛОВНА ТАБЛИЦЯ (Main Table) ---
    
    if df_alerts.empty:
        st.info("📭 Журнал порожній або записи приховані фільтром дати (зліва).")
        return

    st.markdown(f"##### 📋 Журнал подій ({len(df_alerts)} записів)")

    # Інтерактивний редактор даних
    st.data_editor(
        df_alerts[['alert_id', 'timestamp', 'substation_name', 'alert_type', 'description', 'status']],
        column_config={
            "status": st.column_config.SelectboxColumn(
                "Статус",
                help="Змінюйте статус обробки інциденту тут",
                width="medium",
                options=["NEW", "ACKNOWLEDGED", "RESOLVED"],
                required=True,
            ),
            "timestamp": st.column_config.DatetimeColumn(
                "Час",
                format="DD.MM HH:mm",
                width="small"
            ),
            "alert_type": st.column_config.TextColumn("Тип", width="medium"),
            "substation_name": st.column_config.TextColumn("Підстанція", width="medium"),
            "description": st.column_config.TextColumn("Опис", width="large"),
            "alert_id": st.column_config.NumberColumn("ID", width="small"),
        },
        disabled=['alert_id', 'timestamp', 'substation_name', 'alert_type', 'description'],
        hide_index=True,
        use_container_width=True,
        key="alerts_table",
        on_change=lambda: save_changes(st.session_state["alerts_table"]["edited_rows"], df_alerts)
    )

def save_changes(changes, df):
    """Обробник подій: зберігає зміни статусів у БД."""
    for idx, change in changes.items():
        if "status" in change:
            try:
                alert_id = df.iloc[idx]['alert_id']
                db.update_alert_status(alert_id, change["status"])
            except Exception as e:
                st.error(f"Помилка оновлення: {e}")
    
    st.toast("Статус оновлено!")
    st.cache_data.clear()
