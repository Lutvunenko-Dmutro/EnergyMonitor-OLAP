# Технічна специфікація модуля: ui/segments/dashboard.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">APPLICATION UI HUB & NAVIGATION ORCHESTRATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎮</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Оркестратор Інтерфейсу ATLAS</h1>
            <p class="mega-subtitle">Головний вузол візуалізації: фрагментований рендеринг, стабільна шина навігації та лінива фільтрація телеметрії</p>
            <div class="status-tags"><span class="tag tag-online">UI BUS ACTIVE</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">UI ORCHESTRATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Logic</span><span class="metric-value">Fragment-Based</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Perf</span><span class="metric-value">Lazy Filtering</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛰️</div><div class="metric-info"><span class="metric-label">Sync</span><span class="metric-value">Stable Nav Bus</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">Routing</span><span class="metric-value">Intelligent Mode</span></div></div>
</div>

<!-- SECTION 01: APPLICATION UI HUB PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Оркестрації Інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>dashboard.py</code> є "Диригентом" візуального шару ATLAS. У складних аналітичних системах на базі Streamlit критично важливо уникати повного перезавантаження сторінки при зміні дрібних елементів. Наша архітектура базується на принципі <b>ізольованих фрагментів</b>, де кожна частина інтерфейсу (Карта, Графіки, AI) працює як автономний мікро-додаток, синхронізований через глобальну шину стану, що забезпечує UX рівня нативних десктопних додатків.</p>
    </div>
</div>

<!-- SECTION 02: FRAGMENT-BASED RENDERING ARCHITECTURE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Архітектура фрагментованого рендерингу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    MAIN("Main UI Loop") --> BUS("Stable Fragment Bus")
    BUS --> F_MAP("Fragment: Map (Active/Sleep)")
    BUS --> F_CONS("Fragment: Consumption (Active/Sleep)")
    BUS --> F_AI("Fragment: AI Analytics (Active/Sleep)")
    F_MAP & F_CONS & F_AI --> DATA("Lazy Data Fetcher")
    DATA --> RENDER("Target View Render")
    </div></div>
</div>

<!-- SECTION 03: STABLE NAVIGATION BUS & SYNC LOGIC -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стабільна шина навігації та синхронізація</h2></div>
    <div class="glass-card flow-step">
        <p>Для запобігання критичній помилці <code>DuplicateWidgetID</code>, модуль реалізує паттерн <b>Stable Navigation Bus</b>. Всі фрагменти викликаються в ідентичному порядку незалежно від поточної сторінки, але рендериться лише активний. Це гарантує стабільність дерева віджетів Streamlit та дозволяє реалізувати плавне перемикання між вкладками без втрати контексту.</p>
    </div>
</div>

<!-- SECTION 04: LAZY FILTERING ENGINE STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Стратегія "Лінивої Фільтрації" (Memory Diet)</h2></div>
    <div class="glass-card flow-step">
        <p>На відміну від класичних підходів, де відфільтровані дані передаються як аргументи, наш <code>dashboard.py</code> використовує <b>Lazy Filtering</b>:</p>
        <ul>
            <li>Фрагменти отримують лише <b>ключ даних</b> та <b>параметри фільтрації</b> (словник).</li>
            <li>Фільтрація відбувається безпосередньо всередині фрагмента перед рендерингом.</li>
            <li>Це усуває необхідність копіювання великих DataFrame між контекстами функцій, радикально знижуючи споживання RAM.</li>
        </ul>
    </div>
</div>

<!-- SECTION 05: INTELLIGENT ROUTING (LIVE VS KAGGLE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Інтелектуальний роутінг режимів</h2></div>
    <div class="glass-card flow-step">
        <p>Система автоматично переналаштовує навігаційну панель залежно від джерела даних:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Режим</th>
                    <th>Доступні сервіси</th>
                    <th>Особливості UI</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Live Simulation</td><td>Повний набір (Map, Econ, Alerts...)</td><td>Реактивне оновлення 5с</td></tr>
                <tr><td>Kaggle Archive</td><td>Analytics, AI, Forecast</td><td>Статичний історичний аналіз</td></tr>
                <tr><td>Fallback</td><td>Emergency UI</td><td>Мінімалістичний режим доступу</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (FRAGMENT ORCHESTRATION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод оркестрації фрагментів</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_dashboard_ui(data, params):
    1. SYNC_NAVIGATION_STATE()
    2. RENDER top_navigation_bar
    
    # THE STABLE BUS (Always in this order)
    CALL fragment_live_map(key="load", params, active=(page == "MAP"))
    CALL fragment_live_consumption(key="load", params, active=(page == "CONS"))
    CALL fragment_live_ai(key="load", params, active=(page == "AI"))
    
    # 3. ROUTE static pages (Not fragments)
    IF page == "ECONOMY":
        RENDER static_finance_view(data["fin"])
        TRIGGER garbage_collector()
        
    4. RENDER footer with system_meta
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: FRAGMENT ISOLATION & GC TRIGGER -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Ізоляція фрагментів та тригери GC</h2></div>
    <div class="glass-card flow-step">
        <p>Кожен фрагмент після завершення рендерингу виконує примусове видалення локальних посилань на дані та викликає <code>gc.collect()</code>. Це критично для Streamlit, оскільки дозволяє тримати RAM-футпринт у межах 512MB навіть при активному перемиканні між важкими аналітичними вкладками.</p>
    </div>
</div>

<!-- SECTION 08: THE NAVIGATION SYNC PROTOCOL -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Протокол синхронізації навігації</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>sync_nav</code> забезпечує двосторонній зв'язок між <code>session_state</code> та віджетом <code>st.radio</code>. Це дозволяє програмно змінювати сторінки (наприклад, перехід до Журналу Аварій при натисканні на KPI-карту) без збоїв у стані інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 09: LIVE TELEMETRY WRAPPER INTEGRATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Інтеграція обгортки живої телеметрії</h2></div>
    <div class="glass-card flow-step">
        <p>Оркестратор інтегрує <code>live_telemetry_wrapper</code> всередині expander-блоку "Деталізація по підстанціях". Це дозволяє тримати стрім даних активним у фоні, забезпечуючи оновлення KPI-показників навіть тоді, коли користувач працює з іншими вкладками (наприклад, аналізує архів).</p>
    </div>
</div>

<!-- SECTION 10: USER-CENTRIC DESIGN (UX/UI) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Користувачо-центрований дизайн</h2></div>
    <div class="glass-card flow-step">
        <p>Інтерфейс спроектований для роботи в режимі "Ситуаційного Центру":</p>
        <ul>
            <li><b>Horizontal Navigation:</b> Швидкий доступ до всіх аналітичних зрізів.</li>
            <li><b>Status Captions:</b> Візуалізація часу останньої синхронізації БД.</li>
            <li><b>Visual Dividers:</b> Чітке розмежування між керуванням та візуалізацією.</li>
        </ul>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>Styles System</h4>
                <p>Забезпечує Cyber-HUD візуалізацію через <code>apply_custom_css</code>.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🗄️</div>
            <div class="role-content">
                <h4>Data Loader</h4>
                <p>Надає верифіковані дані для лінивого завантаження.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📈</div>
            <div class="role-content">
                <h4>View Components</h4>
                <p>Бібліотека спеціалізованих представлень (Map, Forecast, Finance).</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (MODULAR VIEWS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Modular Views)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>динамічної ін'єкції вкладок</b> (Plugin-based UI), підтримка <b>PWA (Progressive Web App)</b> для роботи на мобільних пристроях диспетчерів та впровадження <b>Dark/Light адаптивної схеми</b>.</p>
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
