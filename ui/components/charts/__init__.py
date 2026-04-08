"""
📈 CENTRAL CHARTS DISPATCHER (Package Entry)
Re-exports components from modular sub-files to keep imports clean.
"""
from ui.components.charts.base import render_dual_axis_chart, render_rhythm_chart
from ui.components.charts.forecast_plots import (
    _generate_forecast_figure, 
    _generate_multi_forecast_figure,
    _generate_mega_hybrid_figure,
    generate_comparison_plot
)
from ui.components.charts.academic import generate_academic_plots

# Re-exporting for compatibility with legacy calls
def render_forecast_chart(df_merged, sub_label):
    import plotly.express as px
    fig = px.line(df_merged, x="timestamp", y="actual_load_mw", color="type", 
                  color_discrete_map={"Історія": "#3b82f6", "Прогноз": "#ef4444"},
                  title=f"📈 {sub_label}")
    fig.update_layout(template="plotly_dark", height=320, margin=dict(l=10, r=10, t=40, b=10))
    return fig
