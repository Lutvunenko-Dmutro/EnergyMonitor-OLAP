"""
ВІЗУАЛІЗАТОР СІТКИ ПРОГНОЗІВ (Grid Forecast Visualizer)
=====================================================
Модуль забезпечує пакетний рендеринг прогнозів для декількох об'єктів у вигляді сітки.
Ключові можливості:
1. Batch Forecast Visualization: автоматичне формування 2-колонкового лейауту для порівняння об'єктів.
2. Dynamic Layout Orchestration: інтелектуальний розподіл графіків по колонках інтерфейсу.
3. Multi-context Rendering: підтримка як поодиноких прогнозів, так і мульти-модельних порівнянь (V1-V3).
4. Smart Legend Management: оптимізація відображення легенд графіків для економії екранного простору.
Забезпечує диспетчеру швидкий огляд всієї енергосистеми через "дзеркало" прогнозів.
"""
# ATLAS_PASSPORT: docs/system/map/forecast_view.md
import streamlit as st
from src.utils.ui_helpers import safe_plotly_render
from src.ml.forecast_controller import cached_ai_forecast as _cached_ai_forecast
from src.ml.forecast_controller import get_cached_history as _get_history
from src.ui.components.charts import _generate_forecast_figure, _generate_multi_forecast_figure

def render_substation_grid(stations, src_type, version, scenario, is_multi_model):
    """Renders a 2-column grid of forecasts for multiple substations."""
    if not stations:
        return
        
    st.divider()
    st.markdown("#### 🏢 Деталізація по об'єктах")
    g_cols = st.columns(2)
    
    for i, station in enumerate(stations):
        with g_cols[i % 2]:
            if is_multi_model:
                multi_s = {}
                for v in ["v1", "v2", "v3"]:
                    res_s = _cached_ai_forecast(
                        hours_ahead=24, substation_name=station, 
                        source_type=src_type, version=v, scenario=scenario
                    )
                    if res_s: multi_s[v] = res_s[0]
                
                df_h_s = _get_history(station, src_type)
                fig_s = _generate_multi_forecast_figure(df_h_s, multi_s, f"📍 {station}")
                fig_s.update_layout(height=400, showlegend=(i == 0))
                safe_plotly_render(fig_s, key=f"grid_fc_multi_re_{station}")
            else:
                res_s = _cached_ai_forecast(
                    hours_ahead=24, substation_name=station, 
                    source_type=src_type, version=version, scenario=scenario
                )
                if res_s:
                    df_f, _ = res_s
                    df_h = _get_history(station, src_type)
                    fig_s = _generate_forecast_figure(
                        df_h, df_f, f"📍 {station}", version.upper()
                    )
                    fig_s.update_layout(height=350)
                    safe_plotly_render(fig_s, key=f"grid_fc_re_{station}")
            st.divider()
