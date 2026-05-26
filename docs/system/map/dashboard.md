# Технічний Паспорт Компонента: scripts/thesis/dashboard.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🖥️ THESIS GRAPHICAL CONTROL CENTER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎛️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">dashboard.py</h1>
            <p class="mega-subtitle">Багатопотоковий графічний пульт управління збіркою дисертації, тестуванням формул та інтелектуальною санітацією</p>
            <div class="status-tags">
                <span class="tag tag-online">DESKTOP GUI</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">SYSTEM CONTROLLER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🎨</div>
        <div class="metric-info">
            <span class="metric-label">GUI Engine</span>
            <span class="metric-value">Tkinter / Custom ttk</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧵</div>
        <div class="metric-info">
            <span class="metric-label">Threading</span>
            <span class="metric-value">Daemon Workers</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-info">
            <span class="metric-label">Style Mode</span>
            <span class="metric-value">Consolas Matrix Dark</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🩹</div>
        <div class="metric-info">
            <span class="metric-label">Integration</span>
            <span class="metric-value">Subprocess IPC</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль та архітектурне призначення</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/thesis/dashboard.py</code> виконує роль <strong>центрального операційного пульта управління (Thesis Control Center)</strong> усього процесу академічної публікації. Він надає зручний графічний інтерфейс користувача (GUI) для запуску консольних утиліт збірки, автоматизуючи складні ручні команди розробника в один клік.
        </p>
        <p style="margin-top: 10px;">
            Основний функціонал графічного диспетчера:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Керування процесами (Build Orchestration):</strong> Запуск повної збірки диплома, що охоплює покрокову конвертацію Markdown розділів, їх злиття у моноліт та фінальну генерацію DOCX.</li>
            <li><strong>Аналітика практики (Practice Report compiler):</strong> Виділений конвеєр для зшивання 7 офіційних розділів звіту переддипломної практики (<code>PR_TITLE.md</code> до <code>PR_S6.md</code>).</li>
            <li><strong>Ізольоване тестування формул (Formula Validation):</strong> Можливість швидко перевірити правильність рендерингу математичних LaTeX формул у форматі Word через виклик тестового документа `FORMULA_TEST.md`.</li>
            <li><strong>Багатопотокове виконання (Non-blocking Threading):</strong> Всі фонові процеси та виклики Pandas/Word запускаються у фонових демонічних потоках (Daemon Threads), що повністю запобігає зависанню графічного інтерфейсу (UI Freezing) під час важких дискових операцій.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр виконання процесів (Multithreaded Build Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема демонструє, як головний потік GUI створює фонові робітники для виконання збірки та отримує логи в реальному часі через канали `stdout`:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск GUI (root.mainloop)") --> DRAW("1. Побудова віджетів (Tkinter ttk)")
                DRAW --> USER_CLICK{"2. Клік користувача на 'RUN FULL BUILD'"}
                
                USER_CLICK --> SPAWN_THREAD("3. Створення threading.Thread(daemon=True)")
                SPAWN_THREAD --> THREAD_RUN("4. Фоновий потік: Запуск run_build_process()")
                
                THREAD_RUN --> KILL_WORD("5. taskkill WINWORD.EXE (Очищення процесів)")
                KILL_WORD --> SUB_PROC("6. subprocess.Popen(convert_thesis.py --all)")
                
                SUB_PROC --> READ_OUT("7. Посимвольне зчитування stdout.readline()")
                READ_OUT --> UPDATE_LOG("8. root.after() / root.update(): Вивід логів у ScrolledText")
                
                UPDATE_LOG --> COMP_STEPS{"9. Чи завершено конвертацію?"}
                COMP_STEPS -- "Ні" --> READ_OUT
                COMP_STEPS -- "Так" --> MERGE("10. Запуск scripts/thesis/merge_thesis.py")
                
                MERGE --> OPEN_FILE("11. os.startfile(Литвиненко_YYYYMMDD.docx)")
                OPEN_FILE --> END("Завершення фонового потоку & розблокування кнопок")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математика багатопотоковості та інтеграція Windows DWM</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Синхронізація прогрес-бару (Linear Progress mapping)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Оскільки збірка складається з дискретних етапів різної тривалості, прогрес-бар оновлюється за кусково-лінійною функцією, де кожному етапу виділяється певний фіксований відсоток шкали $S$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    S(t) = \begin{cases} 
                      10, & t = \text{taskkill} \\
                      10 + 4 \cdot k, & k \in [1, N] \quad (\text{конвертація } k\text{-го розділу}) \\
                      80, & t = \text{злиття файлів} \\
                      90 + 10 \cdot p, & p \in [0, 1] \quad (\text{фінальна Word оптимізація}) 
                   \end{cases}
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Низькорівнева інтеграція Windows Dark Title Bar</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для забезпечення бездоганного Cyber-HUD дизайну, скрипт обходить стандартний білий заголовок вікна Windows за допомогою системних викликів `dwmapi.dll`. Атрибут `DWMWA_USE_IMMERSIVE_DARK_MODE` (код 35) примусово вмикає темну тему вікна:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{DwmSetWindowAttribute}(\text{HWND}, 35, \&\text{Enabled}(1), \text{sizeof}(\text{int})) $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод багатопотокового GUI контролера</h2>
    </div>
    <div class="glass-card">
        <p>
            Спрощена схема створення фонового потоку та зчитування логів через `subprocess`:
        </p>
        <pre><code class="language-python">
# Псевдокод асинхронного GUI дашборда
import threading
import subprocess

class AsyncThesisDashboard:
    def __init__(self):
        self.root = create_tkinter_window()
        self.log_widget = create_scroll_text()
        self.progress_bar = create_progress_bar()
        
    def log(self, text):
        # Вставка тексту з часовим штампом
        self.log_widget.insert_at_end(f"[{get_time()}] {text}")
        self.root.update_idletasks()

    def run_build_in_background(self):
        self.log("Starting Build...")
        self.progress_bar.set_value(10)
        
        # Запускаємо процес Pandoc/Word як підпроцес
        process = subprocess.Popen(
            ["python", "convert_thesis.py", "--all"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        
        # Зчитуємо по рядку, не блокуючи головний потік
        while True:
            line = process.stdout.readline()
            if not line:
                break
            self.log(f"  {line.strip()}")
            if "Processed" in line:
                self.progress_bar.increment(5)
                
        process.wait()
        self.progress_bar.set_value(100)
        self.log("Build Completed successfully!")

    def on_build_click(self):
        # Запуск у фоновому потоці для запобігання зависанню вікна
        worker = threading.Thread(target=self.run_build_in_background, daemon=True)
        worker.start()
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Часті питання (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому інтерфейс Tkinter не зависає під час тривалого процесу збірки (20-40 сек)?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Звичайні GUI програми на Python зависають (не реагують на кліки та перетягування), якщо тривалі розрахунки або файлові операції запускаються в основному потоці вікна. Дашборд вирішує це шляхом винесення всієї логіки збірки (`subprocess.Popen` та `merge_thesis`) у виділений фоновий потік `threading.Thread(daemon=True)`. Головний потік залишається повністю вільним для обробки подій вікна та відмальовки логів.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Що робить кнопка "TEST FORMULAS"?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Вона призначена для швидкого налагодження математичних формул LaTeX. Скрипт бере невеликий локальний файл `docs/thesis/FORMULA_TEST.md`, швидко конвертує його в `docs/thesis/FORMULA_TEST.docx` і автоматично відкриває результат у MS Word. Це дозволяє перевірити, як трансформуються складні дроби, інтеграли та грецькі літери перед великою генерацією всього диплома.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Що за дивні виклики бібліотеки `ctypes` в кінці файлу?</h4>
        <p style="color: var(--text-dim);">
            A: Ці системні виклики через C-сумісні типи (`ctypes`) звертаються безпосередньо до Windows API (`dwmapi.dll`). Вони перехоплюють дескриптор вікна Tkinter (HWND) та примусово встановлюють для верхньої системної рамки вікна темне оформлення. Це позбавляє додаток застарілого білого заголовка, створюючи цілісний Cyber-HUD стиль.
        </p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn">
        <span class="btn-icon">🔙</span>
        <span class="btn-text">Повернутися до Атласу</span>
    </a>
</div>

</div>

<script>
function setupMermaid() {
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({ startOnLoad: true, theme: 'dark' });
        mermaid.init(undefined, '.mermaid');
    }
}
document.addEventListener("DOMContentLoaded", setupMermaid);
document.addEventListener("DOMContentSwitch", setupMermaid);
setTimeout(setupMermaid, 1500);
</script>
