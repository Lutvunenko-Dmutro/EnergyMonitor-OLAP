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
