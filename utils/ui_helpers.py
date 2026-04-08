import streamlit as st

def safe_plotly_render(fig, container=st, **kwargs):
    """
    Єдина точка рендеру для всіх графіків проєкту.
    Виправляє Plotly Deprecation Warning та стандартизує вигляд. 
    Тепер підтримує **kwargs для передачі key, use_container_width тощо.
    """
    config = {
        'displayModeBar': True,
        'scrollZoom': False,  # Виключено, щоб не перехоплювати скрол сторінки
        'displaylogo': False,
        'modeBarButtonsToRemove': ['select2d', 'lasso2d']
    }
    container.plotly_chart(fig, use_container_width=True, config=config, **kwargs)
