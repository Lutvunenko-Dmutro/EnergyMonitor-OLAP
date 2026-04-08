import time

import streamlit as st

from src.services.db_services import (
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

    # Панель адміністрування (Admin Tools)
    # Згорнутий блок для економії місця на екрані
    with st.expander("🛠️ Панель дій (Додати / Очистити)", expanded=False):
        tab_add, tab_clean = st.tabs(["➕ Додати запис", "🗑️ Очистка бази"])

        # Вкладка 1: Форма додавання
        with tab_add:
            with st.form("quick_add_form"):
                c1, c2 = st.columns(2)

                # Завантаження актуального списку підстанцій
                subs_df = db.run_query(
                    "SELECT substation_name FROM Substations ORDER BY substation_name"
                )
                sub_options = (
                    subs_df["substation_name"].tolist()
                    if not subs_df.empty
                    else ["Немає даних"]
                )

                selected_sub = c1.selectbox("Об'єкт", sub_options)
                selected_type = c1.selectbox(
                    "Тип", ["Перевантаження", "Аварія", "Кібер-атака", "Пожежа"]
                )
                input_desc = c2.text_input("Короткий опис", "Фіксація інциденту")

                if st.form_submit_button("Створити", type="primary"):
                    success, msg = db.create_custom_alert(
                        selected_sub, selected_type, input_desc
                    )
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

    df_display["alert_type"] = df_display["alert_type"].apply(
        lambda x: type_emoji.get(x, x)
    )
    df_display["status"] = df_display["status"].apply(lambda x: status_emoji.get(x, x))

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
        width="stretch",
        key="alerts_table",
        on_change=lambda: save_changes(
            st.session_state["alerts_table"]["edited_rows"], df_alerts
        ),
    )


def save_changes(changes, df):
    """Обробник подій: зберігає зміни статусів у БД, очищаючи емодзі."""
    clean_map = {
        "🔴 NEW": "NEW",
        "🟡 IN PROGRESS": "IN PROGRESS",
        "🟢 RESOLVED": "RESOLVED",
    }
    for idx, change in changes.items():
        if "status" in change:
            try:
                alert_id = df.iloc[int(idx)]["alert_id"]
                raw_status = clean_map.get(change["status"], change["status"])
                db.update_alert_status(alert_id, raw_status)
            except Exception as e:
                st.error(f"Помилка оновлення: {e}")

    st.toast("Статус оновлено!")
    st.cache_data.clear()
