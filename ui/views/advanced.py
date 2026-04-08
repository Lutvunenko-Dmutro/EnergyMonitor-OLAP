import streamlit as st
from ui.views.advanced_components.clustering_view import render_clustering_segment
from ui.views.advanced_components.trend_view import render_trend_decomposition

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

    @st.fragment
    def render_tab1():
        _, col_tools = st.columns([4, 1])
        with col_tools.popover("⚙️ Налаштування", width='stretch'):
            use_log = st.toggle("🪵 Логарифмічна шкала", value=False, key="adv_use_log")
        render_clustering_segment(df, use_log, selected_substation)

    @st.fragment
    def render_tab2():
        _, col_tools = st.columns([4, 1])
        with col_tools.popover("⚙️ Налаштування", width='stretch'):
            use_rel = st.toggle("📈 Відносне навантаження (%)", value=False, key="adv_use_rel")
        render_trend_decomposition(df, selected_substation, use_rel)

    with tab1: render_tab1()
    with tab2: render_tab2()
