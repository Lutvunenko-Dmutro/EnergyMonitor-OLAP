# Технічна специфікація модуля: main.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">STRATEGIC COMMAND & CONTROL CENTER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚀</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Оркестратор ATLAS</h1>
            <p class="mega-subtitle">Центральний командний центр системи: управління життєвим циклом додатку, ресурсами RAM та гібридними потоками даних</p>
            <div class="status-tags"><span class="tag tag-online">DEFENSE EDITION</span><span class="tag tag-version">v5.0.0</span><span class="tag tag-role">ORCHESTRATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Watchdog</span><span class="metric-value">Active Sentinel</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Cloud Safe</span><span class="metric-value">Single-Threaded</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧬</div><div class="metric-info"><span class="metric-label">Strategy</span><span class="metric-value">Hybrid Data</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Health</span><span class="metric-value">Auto Diagnostic</span></div></div>
</div>

<!-- SECTION 01: STRATEGIC ORCHESTRATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Стратегічної Оркестрації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>main.py</code> є "диригентом" всього аналітичного комплексу ATLAS. Його роль виходить далеко за межі простої точки входу. Він відповідає за підготовку обчислювального середовища, моніторинг критичних ресурсів сервера, управління станами сесій та безшовну інтеграцію між ML-ядром, базою даних та UI-компонентами. Це гарантує стабільність системи "Defense Edition" навіть при екстремальних навантаженнях.</p>
    </div>
</div>

<!-- SECTION 02: WATCHDOG SENTINEL (MEMORY GUARD) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Watchdog Sentinel: Захист Пам'яті</h2></div>
    <div class="glass-card flow-step">
        <p>Однією з ключових інновацій версії 5.0 є впровадження активного вартівника пам'яті. В обмежених хмарних середовищах (наприклад, Streamlit Cloud або Docker-контейнери) виток пам'яті може призвести до миттєвої зупинки сервісу.</p>
        <ul>
            <li><b>Threshold Monitoring:</b> Система постійно відстежує обсяг RAM, зайнятий процесом.</li>
            <li><b>Preemptive GC:</b> При досягненні порогу <b>380 MB</b> автоматично ініціюється глибоке очищення об'єктів та тензорів через <code>auto_gc</code>.</li>
            <li><b>Thread Hardening:</b> Примусове обмеження <code>OPENBLAS_NUM_THREADS = 1</code> запобігає неконтрольованому паралелізму, який є головною причиною Memory Spikes.</li>
        </ul>
    </div>
</div>

<!-- SECTION 03: BOOTSTRAPPING & STARTUP SEQUENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Протокол Бутстрапінгу (Startup Sequence)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("Запуск (main.py)") --> ENV("Конфігурація оточення (Threads/Logs)")
    ENV --> DIAG("Діагностика: Cache Cleanup (TTL 24h)")
    DIAG --> CONFIG("Page Config (Init)")
    CONFIG --> SPLASH("Splash Screen (Boot Sequence)")
    SPLASH --> DATA("Hybrid Data Resolution")
    DATA --> RENDER("Dashboard UI Rendering")
    </div></div>
</div>

<!-- SECTION 04: MAIN EVENT LOOP ARCHITECTURE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Архітектура Головного Циклу (Event Loop)</h2></div>
    <div class="glass-card flow-step">
        <p>Головний цикл ATLAS побудований за принципом "Single State Source". Будь-яка взаємодія користувача з інтерфейсом тригерує повторне виконання циклу, але завдяки розумному кешуванню в <code>st.session_state</code>, важкі операції (такі як анімація завантаження або SQL-запити) не повторюються.</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Етап</th>
                    <th>Механізм</th>
                    <th>Результат</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Ініціалізація</td><td><code>init_page_config</code></td><td>Налаштування метаданих та іконки</td></tr>
                <tr><td>Стилізація</td><td><code>apply_custom_css</code></td><td>Ін'єкція Cyber-HUD стилів</td></tr>
                <tr><td>Резолюція даних</td><td><code>get_verified_data</code></td><td>Вибір між Live та Kaggle джерелами</td></tr>
                <tr><td>Рендеринг</td><td><code>render_dashboard_ui</code></td><td>Побудова фінального аналітичного простору</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: HYBRID DATA STRATEGY (LIFECYCLE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Реалізація Гібридної Стратегії Даних</h2></div>
    <div class="glass-card flow-step">
        <p>Оркестратор динамічно керує джерелами правди. Якщо користувач обирає "Еталонні дані (Kaggle)", <code>main.py</code> виконує підміну потоку даних через <code>load_kaggle_lazy</code>, гарантуючи, що всі аналітичні віджети миттєво перемкнуться на новий контекст без перезавантаження всього додатку.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (CORE ORCHESTRATOR) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Головного Оркестратора</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION main():
    1. INITIALIZE streamlit_page(title, layout='wide')
    2. CHECK memory_usage()
        IF usage > 380MB: TRIGGER garbage_collection()
    3. INJECT Cyber-HUD CSS themes
    4. IF NOT session.booted:
        session.data = run_boot_sequence_animation()
        session.booted = True
    5. DATA = resolve_active_source(session.data)
    6. RENDER_SIDEBAR(DATA) -> GET user_filters
    7. ANALYZE context (Region vs Substation)
    8. INVOKE dashboard_ui(DATA, filters)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: CLOUD-SAFE ENGINE OPTIMIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Оптимізація Cloud-Safe Engine</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення "армійської" надійності, модуль примусово встановлює змінні оточення для бібліотек <code>OpenBLAS</code>, <code>MKL</code> та <code>OMP</code>. Це запобігає конфліктам паралелізму, які часто виникають при роботі <code>onnxruntime</code> та <code>numpy</code> в багатокористувацьких веб-сесіях.</p>
    </div>
</div>

<!-- SECTION 08: RESOURCE MONITORING MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Матриця моніторингу ресурсів</h2></div>
    <div class="glass-card flow-step">
        <ul>
            <li><b>RAM Hard Limit:</b> 380 MB (Тригер <code>auto_gc</code>).</li>
            <li><b>Thread Limit:</b> 1 (Single-threaded math core).</li>
            <li><b>Cache TTL:</b> 24 години (Авто-очищення при старті).</li>
            <li><b>Session Persistence:</b> Дані зберігаються в <code>st.session_state</code> для UX-стабільності.</li>
        </ul>
    </div>
</div>

<!-- SECTION 09: SYSTEM DIAGNOSTICS & LOGGING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Системна діагностика та Логування</h2></div>
    <div class="glass-card flow-step">
        <p>При старті <code>main.py</code> ініціює централізовану систему логування <code>setup_logging</code>. Рівень логування (DEBUG/INFO/ERROR) може динамічно змінюватися через змінні оточення, що дозволяє проводити глибокий дебаг системи на сервері без зміни коду.</p>
    </div>
</div>

<!-- SECTION 10: DYNAMIC AGGREGATION RESOLUTION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Динамічна резолюція агрегації</h2></div>
    <div class="glass-card flow-step">
        <p>Оркестратор реалізує "інтелектуальний фокус": якщо користувач обирає фільтр "Усі регіони", система автоматично перемикає всі групування на <code>region_name</code>. Як тільки обирається конкретний регіон — фокус зміщується на рівень <code>substation_name</code>. Це забезпечує природну глибину аналізу (Drill-down).</p>
    </div>
</div>

<!-- SECTION 11: MODULE ORCHESTRATION MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця оркестрації модулів</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>UI Components</h4>
                <p>main.py координує послідовність рендерингу від Sidebar до Dashboard.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🗄️</div>
            <div class="role-content">
                <h4>Core Data</h4>
                <p>main.py відповідає за Handshake з Loader та верифікацію цілісності даних.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🩺</div>
            <div class="role-content">
                <h4>Memory Utils</h4>
                <p>main.py виступає тригером для засобів примусового вивільнення RAM.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v6.0 (DISTRIBUTED ATLAS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v6.0 (Distributed Atlas)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 6.0 планується перехід на <b>розподілену чергу завдань (Celery/Redis)</b> для винесення ML-обчислень в окремі воркери, що дозволить <code>main.py</code> фокусуватися виключно на UI-оркестрації та підтримувати тисячі одночасних користувачів.</p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
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
