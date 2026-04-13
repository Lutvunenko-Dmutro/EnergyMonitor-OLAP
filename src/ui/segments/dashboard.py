import gc

import pandas as pd
import streamlit as st

from src.ui.components.styles import apply_custom_css
from src.core.database.loader import get_verified_data
from src.ui.segments.live_kpi import live_telemetry_wrapper
from src.ui.views import advanced as tab_advanced
from src.ui.views import alerts as tab_alerts
from src.ui.views import consumption as tab_consumption
from src.ui.views import finance as tab_finance
from src.ui.views import forecast as tab_forecast
from src.ui.views import generation as tab_generation
from src.ui.views import historical_audit as tab_audit
from src.ui.views import map as tab_map


# ─── FRAGMENTS ───────────────────────────────────────────────────────────────
# [ОПТИМІЗОВАНО v2]: Фрагменти НЕ отримують DataFrame як аргумент.
# Вони отримують КЛЮЧ + параметри фільтрації, і самі фільтрують при кожному тіку.
# Це унеможливлює копіювання великих DF при кожному run_every=N.

@st.fragment
def fragment_live_map(data_key, filter_params: dict, active=False):
    """Фрагмент живої карти — отримує ключ та параметри, фільтрує сам."""
    if not active:
        return
    
    apply_custom_css()
    
    data = get_verified_data()
    df = data.get(data_key, pd.DataFrame())
    if not df.empty:
        from src.core.analytics.filter import filter_dataframe
        df = filter_dataframe(
            df,
            filter_params.get("region"),
            filter_params.get("dates"),
            data_key,
            filter_params.get("substation", "Усі підстанції")
        )
        tab_map.render(df)
    else:
        st.info("🌐 Завантаження геоданих... Очікуйте синхронізації.")
    del df; gc.collect()


@st.fragment
def fragment_live_consumption(data_key, group_col: str, filter_params: dict, active=False):
    """Фрагмент споживання — ліниве читання з session_state."""
    if not active:
        return
        
    apply_custom_css()
        
    data = get_verified_data()
    df = data.get(data_key, pd.DataFrame())
    if not df.empty:
        from src.core.analytics.filter import filter_dataframe
        df = filter_dataframe(
            df,
            filter_params.get("region"),
            filter_params.get("dates"),
            data_key,
            filter_params.get("substation", "Усі підстанції")
        )
    tab_consumption.render(df, group_col)
    del df; gc.collect()


@st.fragment
def fragment_live_alerts(data_key, filter_params: dict, active=False):
    """Фрагмент аварій — оновлюється при клавіші Refresh або зміні фільтрів."""
    if not active:
        return
        
    apply_custom_css()
        
    data = get_verified_data()
    df = data.get(data_key, pd.DataFrame())
    tab_alerts.render(df)
    del df; gc.collect()


@st.fragment
def fragment_live_ai(data_key, selected_substation: str, filter_params: dict, active=False):
    """Фрагмент AI — оновлюється при клавіші Refresh або зміні фільтрів."""
    if not active:
        return
    
    apply_custom_css()
    
    data = get_verified_data()
    df = data.get(data_key, pd.DataFrame())
    if not df.empty:
        from src.core.analytics.filter import filter_dataframe
        df = filter_dataframe(
            df,
            filter_params.get("region"),
            filter_params.get("dates"),
            data_key,
            filter_params.get("substation", "Усі підстанції")
        )
    tab_advanced.render_advanced_analysis(df, selected_substation)
    del df; gc.collect()


# ─── GHOST-BUSTING ───────────────────────────────────────────────────────────
# [ФІКС]: register_all_fragments_stably видалено. Тепер фрагменти реєструються динамічно в render_dashboard_ui.


# ─── NAVIGATION ──────────────────────────────────────────────────────────────
def sync_nav():
    """Синхронізує стан навігації між елементами інтерфейсу."""
    options = st.session_state.get("current_options", [])
    if not options:
        return
    if "top_navigation" in st.session_state:
        try:
            st.session_state.nav_index = options.index(st.session_state.top_navigation)
        except ValueError:
            st.session_state.nav_index = 0
            if "top_navigation" in st.session_state:
                del st.session_state["top_navigation"]


# ─── MAIN RENDER ─────────────────────────────────────────────────────────────
def render_dashboard_ui(
    data: dict,
    group_col: str,
    data_source: str = "Синтетична модель (Smart City)",
    selected_region=None,
    date_range=None,
    selected_substation: str = "Усі підстанції",
    filter_fn=None,
):
    """
    Головний UI. 

    [ОПТИМІЗОВАНО v2]:
    - filtered_data НЕ передається ззовні — фільтрація відбувається lazy
      безпосередньо у кожній вкладці при рендері
    - Фрагменти отримують params-dict замість DataFrame
    """
    st.title("⚡ Energy Monitor")

    load_df = data.get("load", pd.DataFrame())
    if not load_df.empty:
        last_update = load_df["timestamp"].max()
        st.caption(f"🕒 Базова синхронізація: {last_update.strftime('%Y-%m-%d %H:%M')}")

    st.session_state["selected_region"] = selected_region

    with st.expander("📊 Деталізація по підстанціях (Live)", expanded=False):
        # [STABILITY]: Виклик завжди активний для реєстрації ID
        live_telemetry_wrapper(active=True)

    # Параметри фільтрації (передаємо dict, а не DF)
    filter_params = {
        "region": selected_region,
        "dates": date_range,
        "substation": selected_substation,
    }

    if "nav_index" not in st.session_state:
        st.session_state.nav_index = 0

    if data_source == "Еталонні дані (Kaggle)":
        options = ["📉 Споживання", "🤖 AI Аналітика", "🔮 Прогноз ШІ"]
        cur_idx = st.session_state.get("nav_index", 0)
        if cur_idx >= len(options):
            # [ОПТИМІЗОВАНО]: Встановлюємо індекс без st.rerun()
            st.session_state.nav_index = 0
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

    # ─── THE STABLE FRAGMENT BUS ──────────────────────────────────────────────
    # [КРИТИЧНО]: Всі фрагменти викликаються ТУТ і ЗАВЖДИ в однаковому порядку.
    # Це єдиний спосіб гарантувати стабільні ідентифікатори ID у Streamlit
    # та уникнути помилок з віджетами (st.radio тощо).
    
    # 1. Map
    fragment_live_map(
        "load",
        filter_params,
        active=(current_page == "🗺️ Карта мережі")
    )

    # 2. Consumption
    fragment_live_consumption(
        "load",
        group_col,
        filter_params,
        active=(current_page == "📉 Споживання")
    )

    # 3. Alerts (Винесено з фрагментів для стабільності редактора статусів)
    # fragment_live_alerts(
    #     "alerts",
    #     filter_params,
    #     active=(current_page == "🚨 Журнал аварій")
    # )

    # 4. Advanced AI Orchestrator
    fragment_live_ai(
        "load",
        selected_substation,
        filter_params,
        active=(current_page == "🤖 AI Аналітика")
    )

    # 5. Advanced Sub-fragments (Internal stability)
    # Зберігаємо стабільність ID для внутрішніх вкладок AI-аналітики.
    from src.ui.views.advanced import fragment_advanced_tab1, fragment_advanced_tab2
    fragment_advanced_tab1(load_df, selected_substation, active=False)
    fragment_advanced_tab2(load_df, selected_substation, active=False)

    # ─── STANDARD/STATIC NAVIGATION ROUTING ───
    # Ці сторінки не є фрагментами і розміщені ПІСЛЯ блоку фрагментів,
    # щоб не "зсувати" дельта-індекси у дереві Streamlit.
    if current_page == "🏭 Генерація":
        gen_df = data.get("gen", pd.DataFrame())
        if filter_fn:
            gen_df = filter_fn(gen_df, selected_region, date_range, "gen", selected_substation)
        tab_generation.render(gen_df)
        del gen_df; gc.collect()

    elif current_page == "🚨 Журнал аварій":
        alerts_df = data.get("alerts", pd.DataFrame())
        if filter_fn:
            alerts_df = filter_fn(alerts_df, selected_region, date_range, "alerts", selected_substation)
        tab_alerts.render(alerts_df)
        del alerts_df; gc.collect()

    elif current_page == "💰 Економіка":
        fin_df = data.get("fin", pd.DataFrame())
        lines_df = data.get("lines", pd.DataFrame())
        if filter_fn:
            fin_df = filter_fn(fin_df, selected_region, date_range, "fin", selected_substation)
        tab_finance.render(fin_df, lines_df)
        del fin_df, lines_df; gc.collect()

    elif current_page == "🔮 Прогноз ШІ":
        tab_forecast.render(
            selected_substation=selected_substation, data_source=data_source
        )

    elif current_page == "📜 Цифровий архів":
        tab_audit.render(
            selected_region=selected_region,
            date_range=date_range,
            selected_substation=selected_substation,
        )

    st.divider()
    st.markdown(
        "<div style='text-align: center; color: grey;'>© 2025 Energy Systems Analytics | Diploma Project</div>",
        unsafe_allow_html=True,
    )
