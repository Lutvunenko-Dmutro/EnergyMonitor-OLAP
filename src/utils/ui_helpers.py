"""
СИСТЕМА СТАБІЛІЗАЦІЇ ТА КАСТОМІЗАЦІЇ ІНТЕРФЕЙСУ (UI Resilience & Styling)
========================================================================
Модуль реалізує допоміжні функції для забезпечення візуальної консистентності додатка.
Ключові можливості:
1. Unified Chart Rendering: безпечна обгортка для Plotly з оптимальними налаштуваннями панелі інструментів.
2. Interactive Controls Tuning: конфігурація поведінки графіків (Responsive mode, Scroll Zoom, Branding removal).
3. UI Guardrails: запобігання типовим помилкам рендерингу в динамічних контейнерах Streamlit.
Допомагає підтримувати професійний рівень UX та візуальну чистоту концепції "Cyber-HUD".
"""
# ATLAS_PASSPORT: docs/system/map/utils_extended_toolkit.md
import streamlit as st

def safe_plotly_render(fig, container=st, **kwargs):
    """
    Стандартизований рендер для Plotly без застарілих аргументів.
    """
    config = {
        'displayModeBar': True,
        'scrollZoom': False,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
        'responsive': True
    }
    
    # Використовуємо лише базові та найнадійніші аргументи
    container.plotly_chart(
        fig, 
        config=config,
        key=kwargs.get("key")
    )
