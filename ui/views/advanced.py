import streamlit as st
from ui.views.advanced_components.clustering_view import render_clustering_segment
from ui.views.advanced_components.trend_view import render_trend_decomposition


@st.fragment
def fragment_advanced_tab1(df, selected_substation, active=False):
    """Фрагмент для вкладки кластеризації."""
    if not active:
        return
    
    _, col_tools = st.columns([4, 1])
    with col_tools.popover("⚙️ Налаштування"):
        use_log = st.toggle("🪵 Логарифмічна шкала", value=False, key="adv_use_log")
    render_clustering_segment(df, use_log, selected_substation)


@st.fragment
def fragment_advanced_tab2(df, selected_substation, active=False):
    """Фрагмент для вкладки аналізу трендів."""
    if not active:
        return
    
    _, col_tools = st.columns([4, 1])
    with col_tools.popover("⚙️ Налаштування"):
        use_rel = st.toggle("📈 Відносне навантаження (%)", value=False, key="adv_use_rel")
    render_trend_decomposition(df, selected_substation, use_rel)

def render_advanced_analysis(df, selected_substation):
    """
    Dispatcher for advanced AI analytics tabs.
    """
    st.title("🧩 Поглиблена аналітика (AI & Trends)")

    if not all(col in df.columns for col in ["substation_name", "actual_load_mw", "timestamp"]):
        st.error("У даних відсутні необхідні колонки.")
        return

    if df.empty:
        st.warning("Недостатньо даних для аналізу.")
        return

    tab1, tab2 = st.tabs(["📊 Кластеризація (Сегментація)", "📈 Аналіз трендів"])

    # Register both fragments. st.tabs executes both paths by default, 
    # but we make it explicit for perfect stability.
    with tab1:
        fragment_advanced_tab1(df, selected_substation, active=True)
    with tab2:
        fragment_advanced_tab2(df, selected_substation, active=True)

    # [FIX]: Spacer для скролінгу в самому низу
    st.markdown('<div style="height: 300px;"></div>', unsafe_allow_html=True)
