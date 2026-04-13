import time

import streamlit as st

from src.services.data.db_services import (
    cleanup_old_alerts,
    create_custom_alert,
    delete_alert,
    update_alert_status,
)
from src.core import database as db


def render(df_alerts):
    """
    Рендеринг вкладки керування аваріями.
    Функціонал:
    1. Адмін-панель (Додавання/Очистка) у згорнутому стані.
    2. Інтерактивна таблиця для зміни статусів аварій.
    """
    st.subheader("🚨 Центр керування аваріями")
    
    # [SAFE FEEDBACK]: Відображення сповіщень з сесії (unblocks fragment UI warnings)
    if "alerts_feedback" in st.session_state:
        msg, icon, type_ = st.session_state.alerts_feedback
        if type_ == "toast":
            st.toast(msg, icon=icon)
        elif type_ == "error":
            st.error(msg)
        del st.session_state.alerts_feedback

    # [MODULIZED CONTROLS]: Винесення форми за межі розгортки для стабільності Streamlit
    c_form, c_clean = st.columns([3, 1])

    with c_form:
        # Секція додавання - ТЕПЕР ІЗОЛЬОВАНА ТА ПРЯМА
        # [SAFETY]: Завантаження списку об'єктів
        subs_df = db.run_query(
            "SELECT substation_name FROM Substations ORDER BY substation_name"
        )
        sub_options = (
            subs_df["substation_name"].tolist()
            if not subs_df.empty
            else ["Немає даних"]
        )

        with st.container(border=True):
            st.caption("➕ Додати новий запис про інцидент")
            f1, f2, f3 = st.columns([1, 1, 2])
            selected_sub = f1.selectbox("Об'єкт", sub_options)
            selected_type = f2.selectbox(
                "Тип", ["Перевантаження", "Аварія", "Кібер-атака", "Пожежа"]
            )
            input_desc = f3.text_input("Короткий опис", "Фіксація інциденту")
            
            submitted = st.button("📢 Зареєструвати аварію", type="primary", use_container_width=True)

        if submitted:
            success, msg = create_custom_alert(
                selected_sub, selected_type, input_desc
            )
            if success:
                st.toast("✅ Додано! Перевірте таблицю нижче.", icon="📅")
                st.cache_data.clear()
                if "boot_data" in st.session_state: del st.session_state["boot_data"]
                if "active_data" in st.session_state: del st.session_state["active_data"]
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(msg)

    with c_clean:
        # Секція очистки - Швидка дія
        st.write("") # Вирівнювання
        st.write("") 
        if st.button("🧹 Очистка (TOP-10)", use_container_width=True, help="Залишити тільки 10 останніх записів"):
            cleanup_old_alerts(keep_last=10)
            st.toast("База очищена!", icon="🗑️")
            st.cache_data.clear()
            if "boot_data" in st.session_state: del st.session_state["boot_data"]
            if "active_data" in st.session_state: del st.session_state["active_data"]
            time.sleep(0.5)
            st.rerun()

    # Журнал подій (Incident Log)

    if df_alerts.empty:
        st.info("📭 Журнал порожній або записи приховані фільтром дати (зліва).")
        return

    st.markdown(f"##### 📋 Журнал подій ({len(df_alerts)} записів)")

    # Робимо індекси безпечними перед будь-якими операціями
    df_alerts = df_alerts.reset_index(drop=True)

    # Координація кольорової схеми та піктограм для покращення сприйняття
    df_display = df_alerts[
        [
            "alert_id",
            "timestamp",
            "substation_name",
            "alert_type",
            "description",
            "status",
        ]
    ].copy()

    type_emoji = {
        "Перевантаження": "🟠 Перевантаження",
        "Аварія": "🔴 Аварія",
        "Кібер-атака": "☠️ Кібер-атака",
        "Пожежа": "🔥 Пожежа",
    }
    status_emoji = {
        "NEW": "🔴 NEW",
        "ACKNOWLEDGED": "🟡 IN PROGRESS",
        "RESOLVED": "🟢 RESOLVED",
        "IN PROGRESS": "🟡 IN PROGRESS",
    }

    # [ОПТИМІЗАЦІЯ]: Перетворення в String для уникнення "Cannot setitem on a Categorical"
    df_display["alert_type"] = df_display["alert_type"].astype(str).apply(
        lambda x: type_emoji.get(x, x)
    )
    df_display["status"] = df_display["status"].astype(str).apply(
        lambda x: status_emoji.get(x, x)
    )

    # Інтерактивний редактор даних
    st.data_editor(
        df_display,
        column_config={
            "status": st.column_config.SelectboxColumn(
                "Статус (Клікніть для зміни)",
                help="Змінюйте статус обробки інциденту тут",
                width="medium",
                options=["🔴 NEW", "🟡 IN PROGRESS", "🟢 RESOLVED"],
                required=True,
            ),
            "timestamp": st.column_config.DatetimeColumn(
                "Час фіксації", format="YYYY-MM-DD HH:mm", width="small"
            ),
            "alert_type": st.column_config.TextColumn("Рівень", width="medium"),
            "substation_name": st.column_config.TextColumn("Об'єкт", width="medium"),
            "description": st.column_config.TextColumn("Опис інциденту", width="large"),
            "alert_id": st.column_config.NumberColumn("ID", width="small"),
        },
        disabled=[
            "alert_id",
            "timestamp",
            "substation_name",
            "alert_type",
            "description",
        ],
        hide_index=True,
        use_container_width=True,
        key="alerts_table",
        on_change=lambda: save_changes(
            st.session_state["alerts_table"]["edited_rows"], df_alerts
        ),
    )

    # [FIX]: Гарантований відступ внизу для скролінгу (перенесено з callback)
    st.markdown('<div style="height: 300px;"></div>', unsafe_allow_html=True)


def save_changes(changes, df):
    """Обробник подій: зберігає зміни статусів у БД, очищаючи емодзі."""
    clean_map = {
        "🔴 NEW": "NEW",
        "🟡 IN PROGRESS": "ACKNOWLEDGED",
        "🟢 RESOLVED": "RESOLVED",
    }
    for idx, change in changes.items():
        if "status" in change:
            try:
                alert_id = df.iloc[int(idx)]["alert_id"]
                raw_status = clean_map.get(change["status"], change["status"])
                update_alert_status(alert_id, raw_status)
            except Exception as e:
                st.session_state.alerts_feedback = (f"Помилка оновлення: {e}", None, "error")

    st.session_state.alerts_feedback = ("Статус оновлено!", "✅", "toast")
    st.cache_data.clear()
    if "boot_data" in st.session_state: del st.session_state["boot_data"]
    if "active_data" in st.session_state: del st.session_state["active_data"]
