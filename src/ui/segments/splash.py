import streamlit as st
import time

from src.core.database.loader import get_active_boot_data_generator

def show_boot_sequence():
    """
    Renders an active, data-driven splash screen with DB source selection.
    """
    # 0. Selection Stage
    # 0. Selection Stage
    if "db_mode" not in st.session_state:
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@400;700&display=swap');
            
            .stApp { background-color: #05070a; }
            
            .select-card {
                border: 1px solid rgba(0, 255, 136, 0.3); padding: 40px; 
                background: linear-gradient(180deg, rgba(5, 7, 10, 0.95) 0%, rgba(10, 20, 15, 0.9) 100%);
                box-shadow: 0 0 40px rgba(0, 255, 136, 0.05), inset 0 0 20px rgba(0, 255, 136, 0.02); 
                text-align: center; border-left: 4px solid #00ff88;
                position: relative; overflow: hidden; max-width: 600px; margin: auto;
            }
            .meta-line {
                font-family: 'Roboto Mono', monospace; font-size: 10px; color: #00d4ff;
                text-transform: uppercase; letter-spacing: 2px; margin-bottom: 25px;
                padding-bottom: 10px; border-bottom: 1px solid rgba(0, 212, 255, 0.1);
                display: flex; justify-content: space-between;
            }
            .select-title { 
                font-family: 'Orbitron', sans-serif; font-size: 28px; font-weight: 700;
                margin-bottom: 10px; letter-spacing: 6px; color: #00ff88;
                text-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
            }
            .select-subtitle { 
                color: #444; font-size: 10px; text-transform: uppercase; 
                letter-spacing: 3px; margin-bottom: 35px;
            }
            
            /* Button Styling Overrides */
            div.stButton > button {
                background: rgba(0, 255, 136, 0.02) !important;
                border: 1px solid rgba(0, 255, 136, 0.2) !important;
                color: #00ff88 !important;
                font-family: 'Orbitron', sans-serif !important;
                font-size: 12px !important; letter-spacing: 2px !important;
                transition: all 0.3s ease !important;
                height: 50px !important;
            }
            div.stButton > button:hover {
                border-color: #00ff88 !important;
                box-shadow: 0 0 15px rgba(0, 255, 136, 0.3) !important;
                background: rgba(0, 255, 136, 0.1) !important;
                transform: translateY(-2px);
            }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div style="height: 25vh;"></div>', unsafe_allow_html=True)
            col_l, col_c, col_r = st.columns([1, 4, 1])
        with col_c:
            # Об'єднуємо все в один блок контенту, щоб уникнути порожніх рамок
            st.markdown("""
                <div class="select-card">
                    <div class="meta-line">
                        <span>ID: 0x449-AUTH</span>
                        <span>ENC: AES-256</span>
                        <span>STATUS: WAITING</span>
                    </div>
                    <div class="select-title">ENERGY CORE</div>
                    <div class="select-subtitle">Identify Database Protocol...</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div style="margin-top: -30px; padding: 0 40px 40px 40px; background: rgba(5, 7, 10, 0.95); border: 1px solid rgba(0, 255, 136, 0.3); border-top: none; border-left: 4px solid #00ff88; max-width: 600px; margin: auto;">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.button("🏠 LOCAL NODE", use_container_width=True):
                st.session_state["db_mode"] = "local"
                st.rerun()
            if c2.button("🌐 CLOUD NEON", use_container_width=True):
                st.session_state["db_mode"] = "cloud"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    splash_html_template = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@400;700&display=swap');
        
        .boot-container {
            background-color: #05070a; 
            color: #00ff88; 
            font-family: 'Roboto Mono', monospace;
            height: 100vh; width: 100%; position: fixed; top: 0; left: 0; z-index: 9999;
            padding: 50px; display: flex; flex-direction: column; justify-content: flex-start; overflow: hidden;
        }

        /* CRT Scanline Effect */
        .boot-container::before {
            content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 10000; background-size: 100% 4px, 3px 100%; pointer-events: none;
        }

        .logo-box {
            border: 1px solid #00ff88; padding: 25px; margin-bottom: 30px; text-align: left;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.15); border-left: 5px solid #00ff88;
            background: rgba(0, 255, 136, 0.02);
        }

        .logo-text { 
            font-family: 'Orbitron', sans-serif;
            font-size: 28px; font-weight: 700; letter-spacing: 3px; 
            text-shadow: 0 0 8px #00ff88; color: #00ff88; 
        }

        .system-status {
            font-size: 10px; color: #00d4ff; margin-top: 5px; 
            text-transform: uppercase; letter-spacing: 2px;
        }

        .log-line { 
            font-size: 13px; margin-bottom: 6px; color: #aaa;
            opacity: 0; animation: fadeIn 0.2s forwards;
            display: flex; align-items: center;
        }
        .log-line::before { content: ">"; color: #00ff88; margin-right: 10px; font-weight: bold; }

        @keyframes fadeIn { to { opacity: 1; transform: translateX(5px); } }

        .progress-container { width: 100%; height: 2px; background: #1a1c23; margin-top: auto; }
        .progress-bar { 
            height: 100%; background: #00ff88; width: 0%; 
            box-shadow: 0 0 10px #00ff88; transition: width 0.3s ease; 
        }

        .boot-footer {
            display: flex; justify-content: space-between; margin-top: 15px;
            font-size: 10px; color: #444; text-transform: uppercase;
        }
    </style>
    <div class="boot-container">
        <div class="logo-box">
            <div class="logo-text">ENERGY CORE BOOTLOADER</div>
            <div class="system-status">Initialising Strategic OLAP Handshake... [v.2.8.5-STABLE]</div>
        </div>
        <div id="logs" style="flex-grow: 1;">LOGS_PLACEHOLDER</div>
        <div class="progress-container"><div class="progress-bar" style="width: PROGRESS_PLACEHOLDER%;"></div></div>
        <div class="boot-footer">
            <div>Auth Token: EXXXXX-449-ALPHA</div>
            <div>Cluster: NEON-CLOUD-UKRAINE-01</div>
        </div>
    </div>
    """
    
    placeholder = st.empty()
    log_acc = ""
    final_data = {}

    db_mode = st.session_state.get("db_mode", "local")
    cluster_label = "NEON-CLOUD-CENTRAL" if db_mode == "cloud" else "LOCAL-DEVELOPMENT-NODE"
    
    # Execute active boot sequence
    for msg, p, current_data in get_active_boot_data_generator():
        log_acc += f'<div class="log-line">{msg}</div>'
        html = splash_html_template.replace("LOGS_PLACEHOLDER", log_acc) \
                                   .replace("PROGRESS_PLACEHOLDER", str(p)) \
                                   .replace("NEON-CLOUD-UKRAINE-01", cluster_label)
        placeholder.markdown(html, unsafe_allow_html=True)
        final_data = current_data
        time.sleep(0.1) # Small delay for visual smoothness

    time.sleep(0.5)
    placeholder.empty()
    return final_data
