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


@st.fragment(run_every=5)
def fragment_live_map(data, active=False):
    """Фрагмент для живого оновлення карти."""
    if not active:
        return
    if not data.empty:
        tab_map.render(data)
    else:
        st.info("🌐 Завантаження геоданих... Очікуйте синхронізації.")


@st.fragment(run_every=5)
def fragment_live_consumption(data, group_col, active=False):
    """Фрагмент для живого оновлення графіка споживання."""
    if not active:
        return
    tab_consumption.render(data, group_col)


@st.fragment(run_every=5)
def fragment_live_alerts(data, active=False):
    """Фрагмент для живого оновлення журналу аварій."""
    if not active:
        return
    tab_alerts.render(data)


@st.fragment(run_every=10)
def fragment_live_ai(data, selected_substation, active=False):
    """Фрагмент для живого оновлення AI аналітики."""
    if not active:
        return
    tab_advanced.render_advanced_analysis(data, selected_substation)


def register_all_fragments_stably():
    """
    Технічна функція для 'Ghost-Busting'.
    Реєструє ВСІ фрагменти проекту на самому початку роботи програми.
    """
    import pandas as pd
    from ui.views.advanced import fragment_advanced_tab1, fragment_advanced_tab2
    
    dummy_df = pd.DataFrame()
    
    # Реєстрація через виклик з active=False
    live_telemetry_wrapper(active=False)
    fragment_live_map(dummy_df, active=False)
    fragment_live_consumption(dummy_df, "substation_name", active=False)
    fragment_live_alerts(dummy_df, active=False)
    fragment_live_ai(dummy_df, "Усі підстанції", active=False)
    
    # Фрагменти з вкладки AI-аналітики
    fragment_advanced_tab1(dummy_df, "Усі підстанції", active=False)
    fragment_advanced_tab2(dummy_df, "Усі підстанції", active=False)


def sync_nav():
    """
    Синхронізує стан навігації між елементами інтерфейсу.
    Запобігає 'розсипанню' індексів при завантаженні/зміні джерела даних.
    """
    options = st.session_state.get("current_options", [])
    if not options:
        return

    if "top_navigation" in st.session_state:
        try:
            st.session_state.nav_index = options.index(st.session_state.top_navigation)
        except ValueError:
            st.session_state.nav_index = 0
            # Скидаємо ключ, якщо стара назва вкладки зникла з нового списку опцій
            if "top_navigation" in st.session_state:
                del st.session_state["top_navigation"]


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
        live_telemetry_wrapper(active=True)

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

    # 🛒 DEBUG NAVIGATION (Hidden in production)
    # st.write(f"DEBUG: Selected={current_page} | Index={st.session_state.nav_index}")

    # ─── NAVIGATION ROUTING ───
    # Використовуємо явну перевірку рядка для надійності рендерингу

    # ─── NAVIGATION CONTENT (STABLE FRAGMENT REGISTRATION) ───
    # Викликаємо всі фрагменти послідовно. Ті, що не активні, просто нічого не рендерить.
    # Це гарантує стабільність Fragment ID для Streamlit.
    
    fragment_live_map(
        processed_data["load"], 
        active=(current_page == "🗺️ Карта мережі")
    )
    
    fragment_live_consumption(
        processed_data["load"], 
        group_col, 
        active=(current_page == "📉 Споживання")
    )
    
    if current_page == "🏭 Генерація":
        tab_generation.render(processed_data["gen"])

    fragment_live_alerts(
        processed_data["alerts"], 
        active=(current_page == "🚨 Журнал аварій")
    )
    
    if current_page == "💰 Економіка":
        tab_finance.render(processed_data["fin"], processed_data["lines"])

    fragment_live_ai(
        processed_data["load"], 
        selected_substation, 
        active=(current_page == "🤖 AI Аналітика")
    )

    if current_page == "🔮 Прогноз ШІ":
        tab_forecast.render(
            selected_substation=selected_substation, data_source=data_source
        )

    if current_page == "📜 Цифровий архів":
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
