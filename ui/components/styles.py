import plotly.io as pio
import streamlit as st


def setup_streamlit_page():
    """
    Виконує глобальне налаштування візуального стилю додатка (UI/UX Configuration).

    Ця функція об'єднує всі параметри відображення в одному місці:
    1. Конфігурація сторінки (Page Config)
    2. Тема графіків (Plotly)
    3. CSS-ін'єкція (Custom Styles)
    """
    # 1. Сторінка
    st.set_page_config(
        page_title="Energy Monitor ULTIMATE",
        layout="wide",
        page_icon="⚡",
        initial_sidebar_state="expanded",
    )

    # 2. Тема
    pio.templates.default = "plotly_dark"

    # 3. CSS (Тонке налаштування стилів)
    st.markdown(
        """
    <style>
        /* 1. Загальний контейнер */
        .block-container { padding-top: 1.5rem; }
        [data-testid="stMetricValue"] { font-size: 1.4rem; }
        footer {visibility: hidden;}

        /* 2. ГАРНИЙ САЙДБАР */
        [data-testid="stSidebar"] {
            background-color: #0d1117 !important;
            background-image: linear-gradient(180deg, #0d1117 0%, #161b22 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: 0.05rem !important;
            color: #58a6ff !important;
            text-transform: uppercase;
            font-size: 0.82rem !important;
            margin-bottom: 12px !important;
            margin-top: 20px !important;
        }

        /* 3. КНОПКА "ОНОВИТИ ДАНІ" */
        [data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(135deg, #1f6feb 0%, #114e9e 100%) !important;
            border: none !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 12px rgba(31, 111, 235, 0.25) !important;
            width: 100% !important;
            font-weight: bold !important;
            transition: transform 0.2s, box-shadow 0.2s !important;
        }
        [data-testid="stSidebar"] button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(31, 111, 235, 0.45) !important;
        }

        /* 4. СЕЛЕКТБОКСИ І ДАТИ */
        .stSelectbox div[data-baseweb="select"], .stDateInput div[data-baseweb="input"] {
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            background-color: rgba(255, 255, 255, 0.02) !important;
            transition: all 0.2s ease-in-out !important;
        }
        .stSelectbox div[data-baseweb="select"]:hover, .stDateInput div[data-baseweb="input"]:hover {
            border-color: #58a6ff !important;
        }

        /* 5. ТОП НАВІГАЦІЯ */
        div[role="radiogroup"] { gap: 12px !important; }
        div[role="radiogroup"] label > div:first-child { display: none !important; }
        div[role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            padding: 10px 16px !important;
            margin: 0 !important;
            cursor: pointer !important;
            transition: all 0.25s ease-in-out !important;
        }
        div[role="radiogroup"] label:hover {
            background: rgba(31, 111, 235, 0.1) !important;
            border-color: #58a6ff !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(88, 166, 255, 0.15) !important;
        }
        div[role="radiogroup"] label[data-checked="true"], div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(135deg, #1f6feb 0%, #114e9e 100%) !important;
            border-color: #58a6ff !important;
            color: white !important;
            font-weight: bold !important;
            box-shadow: 0 5px 20px rgba(31, 111, 235, 0.4) !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
