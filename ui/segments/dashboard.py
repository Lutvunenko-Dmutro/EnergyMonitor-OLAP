import streamlit as st

from ui.segments.live_kpi import live_telemetry_wrapper
from ui.views import (
    advanced as tab_advanced,
)
from ui.views import (
    alerts as tab_alerts,
)
from ui.views import (
    consumption as tab_consumption,
)
from ui.views import (
    finance as tab_finance,
)
from ui.views import (
    forecast as tab_forecast,
)
from ui.views import (
    generation as tab_generation,
)
from ui.views import (
    historical_audit as tab_audit,
)
from ui.views import (
    map as tab_map,
)


def sync_nav():
    """
    Синхронізує стан навігації між елементами інтерфейсу.
    """
    options = st.session_state.get(
        "current_options",
        [
            "🗺️ Карта мережі",
            "📉 Споживання",
            "🏭 Генерація",
            "🚨 Журнал аварій",
            "💰 Економіка",
            "🤖 AI Аналітика",
            "🔮 Прогноз ШІ",
            "📜 Цифровий архів",
        ],
    )
    if "top_navigation" in st.session_state:
        try:
            st.session_state.nav_index = options.index(st.session_state.top_navigation)
        except ValueError:
            st.session_state.nav_index = 0


def render_dashboard_ui(
    original_data,
    processed_data,
    group_col,
    data_source="Синтетична модель (Smart City)",
    selected_region=None,
    date_range=None,
    selected_substation="Усі підстанції",
):
    """
    Відповідає за рендеринг головного інтерфейсу та навігації.
    """
    st.title("⚡ Energy Monitor")

    if not original_data["load"].empty:
        last_update = original_data["load"]["timestamp"].max()
        st.caption(f"🕒 Базова синхронізація: {last_update.strftime('%Y-%m-%d %H:%M')}")

    st.session_state["selected_region"] = selected_region
    with st.expander("📊 Деталізація по підстанціях (Live)", expanded=False):
        live_telemetry_wrapper()

    if "nav_index" not in st.session_state:
        st.session_state.nav_index = 0

    if data_source == "Еталонні дані (Kaggle)":
        options = ["📉 Споживання", "🤖 AI Аналітика", "🔮 Прогноз ШІ"]
        cur_idx = st.session_state.get("nav_index", 0)
        if cur_idx >= len(options):
            st.session_state.nav_index = 0
            st.rerun()
    else:
        options = [
            "🗺️ Карта мережі",
            "📉 Споживання",
            "🏭 Генерація",
            "🚨 Журнал аварій",
            "💰 Економіка",
            "🤖 AI Аналітика",
            "🔮 Прогноз ШІ",
            "📜 Цифровий архів",
        ]

    st.session_state["current_options"] = options

    current_page = st.radio(
        label="🗂️ Навігація",
        options=options,
        index=st.session_state.nav_index,
        key="top_navigation",
        on_change=sync_nav,
        horizontal=True,
        label_visibility="collapsed",
    )

    # Вкладка 1: Карта мережі
    if current_page == "🗺️ Карта мережі":

        @st.fragment(run_every=5)
        def live_map():
            if not processed_data["load"].empty:
                tab_map.render(processed_data["load"])
            else:
                st.info("Завантаження геоданих...")

        live_map()

    # Вкладка 2: Споживання
    elif current_page == "📉 Споживання":

        @st.fragment(run_every=5)
        def live_consumption():
            tab_consumption.render(processed_data["load"], group_col)

        live_consumption()

    # Вкладка 3: Генерація
    elif current_page == "🏭 Генерація":
        tab_generation.render(processed_data["gen"])

    # Вкладка 4: Журнал аварій
    elif current_page == "🚨 Журнал аварій":

        @st.fragment(run_every=5)
        def live_alerts():
            tab_alerts.render(processed_data["alerts"])

        live_alerts()

    # Вкладка 5: Економіка
    elif current_page == "💰 Економіка":
        tab_finance.render(processed_data["fin"], processed_data["lines"])

    # Вкладка 6: AI Аналітика
    elif current_page == "🤖 AI Аналітика":

        @st.fragment(run_every=10)
        def live_ai():
            tab_advanced.render_advanced_analysis(
                processed_data["load"], selected_substation
            )

        live_ai()

    # Вкладка 7: Прогноз ШІ
    elif current_page == "🔮 Прогноз ШІ":
        tab_forecast.render(
            selected_substation=selected_substation, data_source=data_source
        )

    # Вкладка 8: Цифровий архів
    elif current_page == "📜 Цифровий архів":
        tab_audit.render(
            selected_region=selected_region,
            date_range=date_range,
            selected_substation=selected_substation,
        )

    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: grey;'>
            © 2025 Energy Systems Analytics | Diploma Project
        </div>
        """,
        unsafe_allow_html=True,
    )
