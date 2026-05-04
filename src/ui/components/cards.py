# ATLAS_PASSPORT: docs/system/map/ui_cards_library.md
"""
БІБЛІОТЕКА ІНТЕРАКТИВНИХ КАРТОК ТА ІНДИКАТОРІВ (UI Indicators Library)
====================================================================
Модуль реалізує компактні візуальні елементи для швидкої оцінки стану об'єктів мережі.
Забезпечує:
1. Gauge Indicators: кругові діаграми поточного завантаження з колірним зонуванням статусів.
2. Asset Health Bars: символьні прогрес-бари для візуалізації показника Health Score через емодзі-графіку.
3. Lightweight UI: оптимізовані Plotly-індикатори для вбудовування в аналітичні дашборди.
Допомагає оператору миттєво ідентифікувати аномалії та критичні режими роботи обладнання.
"""
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
    try:
        from src.utils.ui_helpers import safe_plotly_render
    except ImportError:
        safe_plotly_render = st.plotly_chart

    safe_plotly_render(fig)
