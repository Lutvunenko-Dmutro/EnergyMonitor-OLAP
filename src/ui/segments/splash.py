import streamlit as st
import time

from src.core.database.loader import get_active_boot_data_generator

def show_boot_sequence():
    """
    Renders an active, data-driven splash screen.
    Executes real tasks and returns the final data.
    """
    splash_html_template = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
        .boot-container {
            background-color: #0c0e14; color: #00ff88; font-family: 'Roboto Mono', monospace;
            height: 100vh; width: 100%; position: fixed; top: 0; left: 0; z-index: 9999;
            padding: 50px; display: flex; flex-direction: column; justify-content: flex-start; overflow: hidden;
        }
        .logo-box {
            border: 2px solid #00ff88; padding: 20px; margin-bottom: 40px; text-align: center;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.2); animation: pulse 2s infinite;
        }
        .logo-text { font-size: 32px; font-weight: 700; letter-spacing: 5px; text-shadow: 0 0 10px #00ff88; }
        .log-line { font-size: 14px; margin-bottom: 8px; opacity: 0; animation: fadeIn 0.3s forwards; }
        @keyframes fadeIn { to { opacity: 1; transform: translateX(10px); } }
        @keyframes pulse {
            0% { border-color: #00ff88; }
            50% { border-color: #00d4ff; }
            100% { border-color: #00ff88; }
        }
        .progress-container { width: 100%; height: 4px; background: #1a1c23; margin-top: auto; }
        .progress-bar { height: 100%; background: linear-gradient(90deg, #00ff88, #00d4ff); width: 0%; transition: width 0.4s ease; }
    </style>
    <div class="boot-container">
        <div class="logo-box">
            <div class="logo-text">ENERGY MONITOR ULTIMATE</div>
            <div style="font-size: 10px; color: #aaa; margin-top: 5px;">STRATEGIC OLAP ENGINE v2.4.0</div>
        </div>
        <div id="logs">LOGS_PLACEHOLDER</div>
        <div class="progress-container"><div class="progress-bar" style="width: PROGRESS_PLACEHOLDER%;"></div></div>
    </div>
    """
    
    placeholder = st.empty()
    log_acc = ""
    final_data = {}

    # Execute active boot sequence
    for msg, p, current_data in get_active_boot_data_generator():
        log_acc += f'<div class="log-line">{msg}</div>'
        html = splash_html_template.replace("LOGS_PLACEHOLDER", log_acc).replace("PROGRESS_PLACEHOLDER", str(p))
        placeholder.markdown(html, unsafe_allow_html=True)
        final_data = current_data
        time.sleep(0.1) # Small delay for visual smoothness

    time.sleep(0.5)
    placeholder.empty()
    return final_data
