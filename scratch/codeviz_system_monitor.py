import psutil
import json
import time
import os

def check_project_processes():
    status = {
        "ml_engine": "offline",
        "ui_dashboard": "offline",
        "simulation": "offline",
        "database": "online", # Завжди онлайн, якщо є файл БД
        "timestamp": time.time()
    }
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info['cmdline'] or [])
            if "streamlit" in cmdline and "main.py" in cmdline:
                status["ui_dashboard"] = "online"
            if "train_lstm" in cmdline or "backtest" in cmdline:
                status["ml_engine"] = "online"
            if "data_generator" in cmdline or "simulate" in cmdline:
                status["simulation"] = "online"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    return status

if __name__ == "__main__":
    print("Starting System Monitor for CodeViz...")
    output_path = r"d:\yhoba\1\Test\Py\docs\atlas\status.js"
    
    while True:
        status_data = check_project_processes()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"const SYSTEM_STATUS = {json.dumps(status_data, indent=4)};")
        
        # print(f"Status updated: {status_data['timestamp']}")
        time.sleep(2) # Оновлення кожні 2 секунди
