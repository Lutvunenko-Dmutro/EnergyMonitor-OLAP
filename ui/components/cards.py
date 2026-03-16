import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def make_health_bar(h):
    """Створює кастомний текстовий прогрес-бар для показника здоров'я."""
    if pd.isna(h):
        return "⚪ N/A"
    h = float(h)
    filled = int(max(0, min(10, round(h / 10))))
    bar = "🟩" * filled + "⬜" * (10 - filled)
    emoji = "🟢" if h >= 85 else "🟡" if h >= 60 else "🔴"
    return f"{emoji} {bar} {h:.1f}%"


def render_gauge(value):
    """Рендерить діаграму завантаженості (Gauge Chart)."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%", "font": {"size": 18}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#3b82f6"},
                "steps": [
                    {"range": [0, 70], "color": "rgba(34, 197, 94, 0.2)"},
                    {"range": [70, 90], "color": "rgba(245, 158, 11, 0.2)"},
                    {"range": [90, 100], "color": "rgba(239, 68, 68, 0.2)"},
                ],
            },
        )
    )
    fig.update_layout(
        height=120,
        margin=dict(t=25, b=5, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
