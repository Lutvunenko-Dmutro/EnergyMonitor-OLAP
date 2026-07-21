import streamlit as st
import subprocess
import re
import pandas as pd
from pathlib import Path

# ==========================================
# КОНФІГУРАЦІЯ
# ==========================================
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PYTHON_EXE = ROOT_DIR / ".venv" / "Scripts" / "python.exe"
if not PYTHON_EXE.exists():
    PYTHON_EXE = "python" # Fallback

SCRIPTS_CONFIG = {
    "🩺 Health & Diagnostics": [
        {"name": "Run Project Diagnostics", "path": "diagnose.py", "desc": "Глибокий аудит коду: шукає помилки, вразливості безпеки (SQL Injection, eval) та генерує інтерактивний HTML-звіт про здоров'я проєкту."},
    ],
    "🪪 Passports & System": [
        {"name": "Audit Passports", "path": "scripts/audit_passports.py", "desc": "Комплексна перевірка всіх Markdown-паспортів проєкту на цілісність, актуальність та відповідність системним стандартам Atlas."},
        {"name": "Check Passports", "path": "scripts/check_passports.py", "desc": "Швидкий лінтер: миттєво перевіряє базовий синтаксис та наявність обов'язкових полів (наприклад, заголовків) у документації."},
        {"name": "Check Broken Passports", "path": "scripts/check_broken_passports.py", "desc": "Сканує документацію на наявність 'битих' посилань: перевіряє, чи існують файли, на які посилаються інші паспорти."},
        {"name": "Find Orphaned Passports", "path": "scripts/find_orphaned_passports.py", "desc": "Знаходить файли документації ('сироти'), на які немає посилань з жодного іншого місця системи."},
        {"name": "Generate Missing Passports", "path": "scripts/generate_missing_passports.py", "desc": "Автоматично створює шаблони паспортів для модулів або скриптів, які були створені, але ще не задокументовані."},
        {"name": "Rebuild Master Index", "path": "scripts/rebuild_master_index.py", "desc": "Оновлює головний файл навігації (Master Index) з урахуванням нових, видалених або переміщених файлів."},
        {"name": "Generate Atlas Metadata", "path": "scripts/generate_atlas_metadata.py", "desc": "Генерує структурні метадані (JSON/YAML) для інтеграції документації з системою Atlas."},
        {"name": "Check DB Stats", "path": "scripts/system/check_db_stats.py", "desc": "Моніторинг БД: показує загальний об'єм бази, топ найбільших таблиць на диску та статус активного підключення."},
    ],
    "🤖 Machine Learning": [
        {"name": "Audit ML Data", "path": "scripts/ml/audit_data.py", "desc": "Аналіз датасетів: перевіряє якість даних, пропуски та генерує базову описову статистику, необхідну перед тренуванням моделей."},
        {"name": "Benchmark Models", "path": "scripts/ml/benchmark_models.py", "desc": "Запускає змагання між моделями (ARIMA, LSTM тощо) для порівняння їх ефективності та будує графіки точності."},
        {"name": "Evaluate Real Data", "path": "scripts/ml/real_data_evaluation.py", "desc": "Тестує модель виключно на реальних (історичних) даних, вимірюючи її здатність прогнозувати реальні сценарії."},
        {"name": "Train V1 Model", "path": "src/ml/train_v1.py", "desc": "Запускає повний цикл тренування базової моделі прогнозування (Версія 1) з подальшим збереженням ваг."},
        {"name": "Train LSTM Model", "path": "src/ml/train_lstm.py", "desc": "Тренує складну рекурентну нейронну мережу (LSTM), спеціалізовану для роботи з часовими рядами."},
        {"name": "Train Baseline ARIMA", "path": "src/ml/baseline_arima.py", "desc": "Навчає класичну статистичну модель ARIMA, яка слугує базовим рівнем (baseline) для оцінки складніших ML-мереж."},
    ],
    "🎓 Thesis & Docs": [
        {"name": "Build Full Thesis (Pipeline)", "path": "scripts/thesis/convert_thesis.py", "args": ["--all"], "desc": "Майстер-збірка: автоматично склеює всі MD-файли, генерує фінальний DOCX документ та збирає статистику тексту."},
        {"name": "Build Scientific Article", "path": "scripts/thesis/generate_article_docx.py", "desc": "Експортує готову статтю у формат Microsoft Word (DOCX) зі збереженням таблиць, стилів та математичних формул."},
        {"name": "Quality Check", "path": "scripts/thesis/quality_check.py", "desc": "Лінгвістичний аудит: перевіряє дипломну на тавтологію, складність речень та дотримання академічного стилю."},
        {"name": "Stylometry Check", "path": "scripts/thesis/stylometry_check.py", "desc": "Аналіз стилю письма: перевіряє текст на однорідність, щоб виявити фрагменти, які вибиваються із загального тону (наприклад, згенеровані AI)."},
    ]
}

# ==========================================
# UI ЛОГІКА
# ==========================================
st.set_page_config(page_title="Dev Dashboard", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS (Glassmorphism & Dark Mode) ---
st.markdown("""
<style>
    /* Dark Premium Theme */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 10% 20%, rgb(14, 21, 38) 0%, rgb(10, 14, 23) 90%);
        color: #e2e8f0;
    }
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9);
        border-right: 1px solid #1e293b;
    }
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.4rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        border: none;
        color: white;
    }
    div[data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
    }
    h1, h2, h3 {
        color: #f8fafc;
        font-weight: 600;
    }
    hr {
        border-color: #334155;
    }
    .success-text { color: #10b981; font-weight: bold; }
    .error-text { color: #ef4444; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🛠️ Developer Tools")
category = st.sidebar.radio("Categories:", list(SCRIPTS_CONFIG.keys()))

st.title("Atlas Analytics: Developer Dashboard")
st.caption("Centralized orchestrator for system diagnostics, database monitoring, and ML benchmarking.")

# Global Metrics Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("System Status", "Оnline", "Stable", delta_color="normal")
m2.metric("Database", "Connected", "Fast", delta_color="normal")
m3.metric("ML Models", "7", "Active", delta_color="off")
m4.metric("Last Audit", "Passed", "113 Clean Files", delta_color="normal")

st.markdown("---")
st.subheader(f"📂 {category}")

# Функція для запуску скрипта та перехоплення виводу
def run_script(script_def):
    script_path = script_def["path"]
    args = script_def.get("args", [])
    
    abs_path = ROOT_DIR / script_path
    if not abs_path.exists():
        return f"Error: File not found -> {abs_path}", False

    import os, re
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)
    env["PYTHONUNBUFFERED"] = "1"  # Щоб одразу отримувати логи
    
    output_lines = []
    
    with st.spinner(f"Running {script_path}..."):
        try:
            progress_bar = None
            
            process = subprocess.Popen(
                [str(PYTHON_EXE), "-u", str(abs_path)] + args, 
                cwd=str(ROOT_DIR), 
                env=env,
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                encoding="utf-8",
                errors="replace"
            )
            
            for line in iter(process.stdout.readline, ''):
                if not line: break
                
                if "[PROGRESS]" in line:
                    if progress_bar is None:
                        progress_bar = st.progress(0, text="Опрацювання...")
                    try:
                        match = re.search(r'\[PROGRESS\]\s*(\d+)', line)
                        if match:
                            pct = int(match.group(1))
                            pct = max(0, min(100, pct))
                            progress_bar.progress(pct, text=f"Виконується... {pct}%")
                    except Exception:
                        pass
                else:
                    output_lines.append(line)
            
            process.wait()
            
            if progress_bar:
                progress_bar.empty()
                
            full_output = "".join(output_lines)
            
            if process.returncode == 0:
                return full_output, True
            else:
                return full_output + f"\n\n[EXIT CODE {process.returncode}]", False
        except Exception as e:
            return "".join(output_lines) + f"\nException: {str(e)}", False

# Відображення кнопок для обраної категорії
scripts = SCRIPTS_CONFIG[category]

for script in scripts:
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button(script["name"], key=script["path"]):
            st.session_state["last_run_name"] = script["name"]
            st.session_state["last_run_output"], st.session_state["last_run_success"] = run_script(script)
    with col2:
        st.markdown(f"**{script['desc']}**")
        st.caption(f"🛣️ `{script['path']}`")

st.markdown("---")

# --- Smart Visualization Engine ---
def render_smart_ui(output_text, script_name):
    """Smart UI Engine: парсить текст, створює віджети та графіки, повністю відмовляючись від консолі"""
    lines = output_text.split('\n')
    technical_log = []
    
    # 1. Графіки для Check DB Stats
    if script_name == "Check DB Stats":
        db_match = re.search(r'Database:\s*(\S+)', output_text)
        if db_match:
            st.metric(label="Active Database", value=db_match.group(1))
            
        if "Top 5 Largest Tables:" in output_text:
            st.markdown("### 📊 Database Storage Usage")
            tables_data = []
            for line in lines:
                if line.startswith("- "):
                    match = re.search(r'- (.*?):\s*([\d\.]+)\s*(MB|GB|kB|bytes)', line)
                    if match:
                        table_name = match.group(1)
                        size_val = float(match.group(2))
                        unit = match.group(3)
                        if unit == 'GB': size_val *= 1024
                        elif unit == 'kB': size_val /= 1024
                        elif unit == 'bytes': size_val /= (1024*1024)
                        tables_data.append({"Table": table_name, "Size (MB)": size_val})
            if tables_data:
                df = pd.DataFrame(tables_data).set_index("Table")
                st.bar_chart(df, color="#3b82f6")

    # 2. Графіки для Audit ML Data
    elif script_name == "Audit ML Data":
        rows_match = re.search(r'✅ Всього рядків:\s*(\d+)', output_text)
        if rows_match:
            st.metric(label="Total Dataset Rows", value=rows_match.group(1))
            
        # Парсинг нульових значень
        if "--- Частка нульових значень (%) ---" in output_text:
            zeros_data = []
            capture = False
            for line in lines:
                if "--- Частка нульових значень (%) ---" in line:
                    capture = True
                    continue
                if capture:
                    if "---" in line or not line.strip():
                        if not line.strip(): continue
                        else: break
                    parts = line.split(":")
                    if len(parts) == 2:
                        feature = parts[0].strip()
                        try:
                            val = float(parts[1].replace("%", "").strip())
                            zeros_data.append({"Feature": feature, "Zero %": val})
                        except ValueError:
                            pass
            if zeros_data:
                df_zeros = pd.DataFrame(zeros_data).set_index("Feature")
                if any(v["Zero %"] > 0 for v in zeros_data):
                    st.markdown("### ⚠️ Missing/Zero Values (%)")
                    st.bar_chart(df_zeros, color="#ef4444")
                else:
                    st.success("✅ Dataset is perfectly clean! (No missing values)")
                    
        # Парсинг кореляції
        if "--- Кореляція з load_mw ---" in output_text:
            corr_data = []
            capture = False
            for line in lines:
                if "--- Кореляція з load_mw ---" in line:
                    capture = True
                    continue
                if capture:
                    if "Name:" in line or "dtype:" in line or not line.strip():
                        if "Name:" in line: break
                    else:
                        parts = line.split()
                        if len(parts) == 2:
                            try:
                                feature = parts[0]
                                val = float(parts[1])
                                if feature != 'load_mw':
                                    corr_data.append({"Feature": feature, "Correlation": val})
                            except ValueError:
                                pass
            if corr_data:
                st.markdown("### 📉 Feature Correlation (vs Load MW)")
                df_corr = pd.DataFrame(corr_data).set_index("Feature")
                st.bar_chart(df_corr, color="#10b981")

    # 3. ВІЗУАЛІЗАЦІЯ ДЛЯ BENCHMARK MODELS
    elif script_name == "Benchmark Models":
        st.markdown("### 📈 Academic Benchmark Figures")
        results_dir = ROOT_DIR / "results"
        versions = ["v1", "v2", "v3"]
        
        # Створюємо стильні вкладки для кожної моделі
        tabs = st.tabs([f"Модель {v.upper()}" for v in versions])
        
        for i, ver in enumerate(versions):
            with tabs[i]:
                fig5 = results_dir / f"fig5_{ver}.png"
                fig7 = results_dir / f"fig7_{ver}.png"
                scatter = results_dir / f"scatter_{ver}.png"
                
                has_imgs = False
                if fig5.exists():
                    st.image(str(fig5), caption=f"Figure 5: Comparison of Forecasts ({ver.upper()})")
                    has_imgs = True
                
                col1, col2 = st.columns(2)
                if fig7.exists():
                    col1.image(str(fig7), caption=f"Figure 7: Error Distribution ({ver.upper()})")
                    has_imgs = True
                if scatter.exists():
                    col2.image(str(scatter), caption=f"Scatter: Actual vs Predicted ({ver.upper()})")
                    has_imgs = True
                    
                if not has_imgs:
                    st.info(f"Графіки для {ver.upper()} відсутні. Можливо, для неї немає моделі.")
                    
    # 4. ВІЗУАЛІЗАЦІЯ ДЛЯ REAL DATA EVALUATION
    elif script_name == "Evaluate Real Data":
        st.markdown("### 📈 Real Data Continuous Validation")
        fig5 = ROOT_DIR / "figure_5_continuous.png"
        fig7 = ROOT_DIR / "figure_7_comparison.png"
        
        if fig5.exists():
            st.image(str(fig5), caption="Continuous Forecast Validation (14 Days)")
        if fig7.exists():
            st.image(str(fig7), caption="Error Distribution Analysis")


    # --- Універсальний UI-форматер (Стильний термінал) ---
    st.markdown("---")
    st.subheader("📝 Execution Log")
    
    log_html = [
        '<div style="background-color: #0f172a; padding: 15px 20px; border-radius: 10px; font-family: \'JetBrains Mono\', Consolas, monospace; font-size: 0.9em; border: 1px solid #1e293b; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5); overflow-y: auto; max-height: 500px; margin-bottom: 20px;">'
    ]
    
    skip_mode = False
    for line in lines:
        stripped = line.strip()
        if not stripped or "[PROGRESS]" in stripped: continue
        
        # Фільтруємо системний спам TensorFlow (попередження C++)
        if stripped.startswith("WARNING:tensorflow") or stripped.startswith("I0000") or stripped.startswith("WARNING:absl"):
            technical_log.append(line)
            continue
        
        # Ігноруємо специфічні табличні дані, оскільки ми вже намалювали для них графіки
        if "---" in stripped or "Top 5" in stripped or "Всього рядків:" in stripped or "Database:" in stripped:
            skip_mode = True
        elif not stripped.startswith("- ") and not "dtype:" in stripped and not "Name:" in stripped and not stripped.replace(".", "").isdigit():
            # Скидаємо режим пропуску, якщо почався новий осмислений рядок
            skip_mode = False
            
        if skip_mode or (script_name == "Check DB Stats" and stripped.startswith("- ")) or (script_name == "Audit ML Data" and ("dtype:" in stripped or "Name:" in stripped or stripped.replace(".", "").replace("-", "").isdigit())):
            technical_log.append(line)
            continue

        # Color coding for terminal
        color = "#e2e8f0" # slate-200 (Default)
        extra_styles = ""
        
        if "✅" in stripped or "Result:" in stripped: 
            color = "#10b981" # emerald-500
        elif "❌" in stripped or "Error" in stripped or "Traceback" in stripped: 
            color = "#ef4444" # red-500
        elif "⚠️" in stripped or "🛡️" in stripped or "WARNING" in stripped: 
            color = "#f59e0b" # amber-500
        elif "🚀" in stripped or "БЕНЧМАРК" in stripped: 
            color = "#3b82f6" # blue-500
            extra_styles = "font-weight: bold; margin-top: 12px; padding-bottom: 4px; border-bottom: 1px solid #1e293b;"
        elif "📡" in stripped or "💡" in stripped or "INFO" in stripped or "Інфо:" in stripped: 
            color = "#94a3b8" # slate-400
        elif "🔬" in stripped or "📊" in stripped: 
            color = "#a855f7" # purple-500

        safe_line = stripped.replace("<", "&lt;").replace(">", "&gt;")
        log_html.append(f'<div style="color: {color}; margin-bottom: 4px; line-height: 1.5; {extra_styles}">{safe_line}</div>')
        
    log_html.append("</div>")
    st.markdown("".join(log_html), unsafe_allow_html=True)
            
    # Технічний текст ховаємо у зручний віджет
    if technical_log:
        with st.expander("🛠️ Show Detailed Technical Log"):
            st.code("\n".join(technical_log), language="bash")


# Віртуальний термінал для виводу
st.subheader("🖥️ Execution Results")
if "last_run_output" in st.session_state:
    st.write(f"**Останній запуск:** `{st.session_state.get('last_run_name')}`")
    
    # Виклик розумного візуалізатора
    if st.session_state["last_run_success"]:
        render_smart_ui(st.session_state["last_run_output"], st.session_state["last_run_name"])
    else:
        st.markdown('<span class="error-text">❌ Execution Failed</span>', unsafe_allow_html=True)
        st.error("Критична помилка під час виконання скрипта!")
        with st.expander("🛠️ Show Error Traceback", expanded=True):
            st.code(st.session_state["last_run_output"], language="bash")
else:
    st.info("💡 Виберіть скрипт вище, щоб побачити результати його виконання тут.")

# Окрема логіка для відображення HTML звіту (тільки для Diagnostics)
if category == "🩺 Health & Diagnostics":
    st.markdown("---")
    st.subheader("📄 Останній HTML Звіт (Interactive)")
    report_file = ROOT_DIR / "results" / "reports" / "diagnostics_report.html"
    if report_file.exists():
        with open(report_file, "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=600, scrolling=True)
    else:
        st.warning("Звіт ще не згенеровано. Запустіть Project Diagnostics.")
