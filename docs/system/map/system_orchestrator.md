# Технічний Паспорт Компонента: main.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🚀 ATLAS SYSTEM COMMAND & CONTROL CENTER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">main.py</h1>
            <p class="mega-subtitle">Глобальний системний оркестратор, диспетчер обчислювальних потоків та операційний центр HUD-інтерфейсу</p>
            <div class="status-tags">
                <span class="tag tag-online">SYSTEM ORCHESTRATOR</span>
                <span class="tag tag-version">v5.0.0</span>
                <span class="tag tag-role">STRATEGIC COMMAND</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Thread Limit</span>
            <span class="metric-value">Single-Threaded (1)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧠</div>
        <div class="metric-info">
            <span class="metric-label">RAM Watchdog</span>
            <span class="metric-value">Threshold 380 MB</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧬</div>
        <div class="metric-info">
            <span class="metric-label">Data Engine</span>
            <span class="metric-value">Hybrid (Live / Lazy)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-info">
            <span class="metric-label">UI Engine</span>
            <span class="metric-value">Streamlit Event Loop</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль та оркестрація ядра</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>main.py</code> є **стратегічним командним центром** (Strategic Orchestrator) платформи <b>Energy Monitor Ultimate</b>. Він виступає головною точкою входу (Entry Point), яка координує весь життєвий цикл додатку, керує обчислювальними ресурсами, ініціалізує кастомні стилі, фільтрує системні логи та зв'язує докупи всі інфраструктурні, аналітичні та графічні шари системи в єдиний реактивний інтерфейс Streamlit.
        </p>
        <p style="margin-top: 10px;">
            Головні стратегічні технології оркестратора:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Хмарна стабілізація потоків (MKL/OpenBLAS Threading Defense):</strong> Примусове обмеження паралелізму математичних бібліотек в один потік для виключення Memory Spike у контейнеризованих хмарних сервісах.</li>
            <li><strong>Watchdog оперативної пам'яті (RAM Watchdog):</strong> Превентивний запуск збирача сміття <code>auto_gc</code> при досягненні порогу 380 MB для захисту від витоків пам'яті (Memory Leaks).</li>
            <li><strong>Гібридна стратегія даних (Hybrid Data Strategy):</strong> Динамічне перемикання та ліниве завантаження (Lazy Loading) великих архівних пакетів Kaggle поверх швидкої локальної симуляції.</li>
            <li><strong>Контроль заставки (Splash Screen State Boot):</strong> Уникнення циклічного повторення анімацій завантаження при кожній реактивній взаємодії з користувачем через механізм Streamlit Session State.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: EVENT LOOP SEQUENCE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Життєвий цикл оркестрації (Main Event Loop Sequence)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема відображає послідовність етапів ініціалізації та виконання основного циклу Streamlit:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            sequenceDiagram
                autonumber
                participant OS as OS Environment
                participant Init as system_startup()
                participant Main as main.py (main loop)
                participant RAM as Watchdog RAM
                participant Boot as Splash Screen
                participant Data as Data Selector
                participant UI as Dashboard UI
                
                OS->>Init: Обмеження потоків math-бібліотек = 1
                Init->>Init: Очищення кешу БД (startup_cache_cleanup)
                Main->>Main: st.set_page_config()
                Main->>RAM: auto_gc(threshold_mb=380)
                RAM->>RAM: Очищення невикористовуваної пам'яті
                Main->>Boot: show_boot_sequence() (тільки 1 раз)
                Boot->>Main: Save state 'booted'=True
                Main->>Data: get_verified_data() / load_kaggle_lazy()
                Data->>Main: Заповнення st.session_state['active_data']
                Main->>UI: render_dashboard_ui(active_data, filters...)
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Детальний розбір обчислювальної стабілізації</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Конфігурація обчислювального середовища (Thread Limiter)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Математичні бібліотеки (NumPy, Scipy, TensorFlow) за замовчуванням намагаються захопити всі доступні ядра процесора для розрахунків, що викликає вибухове зростання пам'яті (Memory Spikes). Для стабільності у безкоштовних обмежених хмарах (Streamlit Cloud, Heroku) оркестратор блокує мультипотоковість на рівні ОС:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{OPENBLAS\_NUM\_THREADS} = 1, \quad \text{MKL\_NUM\_THREADS} = 1, \quad \text{OMP\_NUM\_THREADS} = 1 $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Watchdog RAM (auto_gc)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Реактивна модель Streamlit перезапускає весь скрипт `main.py` при кожному кліку користувача. Це призводить до накопичення сміття у оперативній пам'яті. Метод <code>auto_gc(threshold_mb=380)</code> перевіряє поточне споживання RAM процесом і примусово запускає очищення <code>gc.collect()</code> при досягненні 380 MB.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Гібридна стратегія даних (Hybrid Data Strategy)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Оркестратор координує роботу з двома джерелами даних. За замовчуванням використовується локальна швидка БД симулятора. Якщо користувач обирає режим <i>"Еталонні дані (Kaggle)"</i>, оркестратор здійснює лінивий імпорт методу <code>load_kaggle_lazy</code>, підвантажує гігантські архіви часових рядів, замінює вимір навантаження і передає оновлений масив у сесію.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод головного циклу обробки</h2>
    </div>
    <div class="glass-card">
        <p>
            Спрощений псевдокод головної функції <code>main()</code> відображає архітектуру реактивного оновлення інтерфейсу:
        </p>
        <pre><code class="language-python">
# Псевдокод головної точки входу та роутингу
def main():
    # 1. Підготовка візуальних стилів
    setup_streamlit_theme()
    
    # 2. Watchdog RAM: контроль витоків
    enforce_ram_limits(max_mb=380)
    
    # 3. Splash Screen: запобігання циклічним анімаціям
    if not is_already_booted(session_state):
        data = run_interactive_boot_sequence()
        save_boot_status(session_state, status=True)
    else:
        data = get_cached_telemetry()
        
    # 4. Гібридне джерело даних
    if user_selected_source == "Kaggle":
        data = load_kaggle_lazy_and_merge(data)
        
    # 5. Сайдбар та Фільтри
    selected_filters = render_sidebar_filters(data)
    
    # 6. Динамічне групування
    group_by = "substation_name" if selected_filters.region != "ALL" else "region_name"
    
    # 7. Фінальний рендеринг дашборду
    render_dashboard_ui(data, group_by, selected_filters)
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому обмеження потоків математичних бібліотек прописано першим кодом у файлі?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Змінні середовища ОС (наприклад, <code>OPENBLAS_NUM_THREADS</code>) мають зчитуватися під час початкового завантаження NumPy. Якщо прописати їх після першого імпорту NumPy або Scikit-Learn, бібліотека вже ініціалізує свій внутрішній пул потоків відповідно до ядер CPU, і зміна змінних в <code>os.environ</code> не матиме жодного ефекту.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Для чого потрібна очистка кешу при запуску (startup_cache_cleanup)?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Локальна база даних SQLite <code>energy.db</code> використовується як проміжний кеш обчислень. При тривалій роботі системи кеш може застарівати або містити пошкоджені транзакційні записи. Очищення кешу з TTL 24 години при старті гарантує свіжість даних для аналізу.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як зреагує система, якщо ліміт RAM буде перевищено навіть після auto_gc?</h4>
        <p style="color: var(--text-dim);">
            A: Якщо споживання пам'яті продовжує рости, Watchdog здійснить аварійне вивільнення великих об'єктів з <code>st.session_state</code> і запише статус критичної аномалії в системний лог, захищаючи процес від примусового завершення операційною системою (OOM Killer).
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
