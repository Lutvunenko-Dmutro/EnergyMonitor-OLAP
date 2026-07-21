import webview
import threading
import subprocess
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
STREAMLIT_SCRIPT = ROOT_DIR / "scripts" / "system" / "dev_dashboard.py"
PYTHON_EXE = ROOT_DIR / ".venv" / "Scripts" / "python.exe"

def run_streamlit():
    py_exe = str(PYTHON_EXE) if PYTHON_EXE.exists() else "python"
    # Запускаємо Streamlit на фіксованому порту без автоматичного відкриття браузера
    subprocess.Popen([py_exe, "-m", "streamlit", "run", str(STREAMLIT_SCRIPT), "--server.port=8501", "--server.headless=True"])

if __name__ == '__main__':
    # Запускаємо streamlit у фоні
    t = threading.Thread(target=run_streamlit)
    t.daemon = True
    t.start()
    
    # Чекаємо поки сервер підніметься
    time.sleep(3)
    
    # Відкриваємо нативне вікно, яке дивиться на Streamlit
    webview.create_window("Developer Dashboard (Streamlit + PyWebView)", "http://localhost:8501", width=1200, height=800)
    webview.start()
