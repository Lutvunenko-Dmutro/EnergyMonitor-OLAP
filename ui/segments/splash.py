import streamlit as st
import time

def show_boot_sequence():
    """
    Renders a high-tech animated splash screen before the main UI loads.
    """
    # HTML/CSS for the "Matrix/Cyberpunk" boot animation
    splash_html = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
        
        .boot-container {
            background-color: #0c0e14;
            color: #00ff88;
            font-family: 'Roboto Mono', monospace;
            height: 100vh;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 9999;
            padding: 50px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            overflow: hidden;
        }

        .logo-box {
            border: 2px solid #00ff88;
            padding: 20px;
            margin-bottom: 40px;
            text-align: center;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
            animation: pulse 2s infinite;
        }

        .logo-text {
            font-size: 32px;
            font-weight: 700;
            letter-spacing: 5px;
            text-shadow: 0 0 10px #00ff88;
        }

        .log-line {
            font-size: 14px;
            margin-bottom: 8px;
            opacity: 0;
            animation: fadeIn 0.3s forwards;
        }

        .status-ok { color: #00d4ff; font-weight: bold; }
        .status-warn { color: #ffa502; }

        @keyframes fadeIn {
            to { opacity: 1; transform: translateX(10px); }
        }

        @keyframes pulse {
            0% { border-color: #00ff88; box-shadow: 0 0 10px rgba(0, 255, 136, 0.2); }
            50% { border-color: #00d4ff; box-shadow: 0 0 30px rgba(0, 212, 255, 0.4); }
            100% { border-color: #00ff88; box-shadow: 0 0 10px rgba(0, 255, 136, 0.2); }
        }

        .progress-container {
            width: 100%;
            height: 4px;
            background: #1a1c23;
            margin-top: auto;
            position: relative;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00d4ff);
            width: 0%;
            box-shadow: 0 0 15px #00d4ff;
            transition: width 0.4s ease;
        }
    </style>
    
    <div class="boot-container">
        <div class="logo-box">
            <div class="logo-text">ENERGY MONITOR ULTIMATE</div>
            <div style="font-size: 10px; color: #aaa; margin-top: 5px;">STRATEGIC OLAP ENGINE v2.4.0</div>
        </div>
        <div id="logs"></div>
        <div class="progress-container">
            <div id="pbar" class="progress-bar"></div>
        </div>
    </div>
    """
    
    placeholder = st.empty()
    placeholder.markdown(splash_html, unsafe_allow_html=True)

    # Boot Sequence Simulation
    boot_steps = [
        ("> Initializing Kernel...", 10),
        ("> System Handshake: Neon DB v4.1... [OK]", 25),
        ("> Loading Neural Networks (LSTM V1, V2, V3)...", 45),
        ("> Calibrating Physics-Informed Digital Twin...", 60),
        ("> Injecting Cyber-Security Sanity Layers...", 75),
        ("> Routing Real-time Telemetry Streams...", 90),
        ("> UI ORCHESTRATOR READY.", 100)
    ]

    log_acc = ""
    for msg, p in boot_steps:
        log_acc += f'<div class="log-line">{msg}</div>'
        # Update progress and log
        p_html = splash_html.replace('width: 0%;', f'width: {p}%;').replace('<div id="logs"></div>', f'<div id="logs">{log_acc}</div>')
        placeholder.markdown(p_html, unsafe_allow_html=True)
        time.sleep(0.4) # Control speed of animation

    time.sleep(0.5)
    placeholder.empty()
