import logging

import streamlit as st

from src.core import database as db
from ui.views import kpi as tab_kpi
from src.services.db_services import get_latest_measurements

logger = logging.getLogger("ENERGY_MONITOR")


@st.fragment(run_every=5)
def live_telemetry_wrapper():
    """
    Автономний фрагмент для живого оновлення показників (KPI).
    Використовує динамічне зчитування region_filter з st.session_state.
    """
    region_filter = st.session_state.get("selected_region", None)

    try:
        telemetry_data = get_latest_measurements()

        if telemetry_data is None or telemetry_data.empty:
            st.warning("🔌 СИСТЕМА МОНІТОРИНГУ В ОЧІКУВАННІ ДАНИХ")
            with st.expander("ℹ️ Як активувати систему?", expanded=False):
                st.write(
                    "Запустіть `python sensors_db.py` у терміналі для старту датчиків."
                )
        else:
            tab_kpi.render(telemetry_data, region_filter=region_filter)

    except Exception as e:
        logger.error(f"Помилка зв'язку з датчиками: {e}", exc_info=True)
