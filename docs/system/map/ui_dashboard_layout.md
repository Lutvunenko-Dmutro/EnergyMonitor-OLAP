# Технічна специфікація: Головний Оркестратор Інтерфейсу (DASHBOARD LAYOUT ENGINE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">UI ORCHESTRATION | FRAGMENT ARCHITECTURE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏗️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Оркестратор Інтерфейсу</h1>
            <p class="mega-subtitle">Центральний хаб візуалізації проекту ATLAS: координація багатосторінкової навігації, стабільний рендеринг через фрагменти та інтелектуальний роутинг аналітичних модулів</p>
            <div class="status-tags"><span class="tag tag-online">ORCHESTRATOR ACTIVE</span><span class="tag tag-version">v2.9.0</span><span class="tag tag-role">CORE UI ENGINE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Pattern</span><span class="metric-value">Fragment-Based UI</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Performance</span><span class="metric-value">Lazy Filtering</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Ghost-Busting Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">State</span><span class="metric-value">Session-Safe Bus</span></div></div>
</div>

<!-- SECTION 01: UI ORCHESTRATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Оркестрації Інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>dashboard.py</code> є "Скелетом" та "Нервовою системою" проекту ATLAS. В складних аналітичних системах на базі Streamlit головною проблемою є повний рендеринг сторінки при кожній зміні віджета. Наша філософія базується на <b>Ізольованому Рендерингу</b>: ми розділили інтерфейс на незалежні фрагменти (st.fragment), які оновлюються автономно. Це дозволяє карті, графікам споживання та AI-моделям працювати паралельно, не блокуючи один одного та забезпечуючи миттєвий відгук системи на дії диспетчера.</p>
    </div>
</div>

<!-- SECTION 02: APPLICATION ARCHITECTURE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Архітектурна схема UI-двигуна (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    APP("Main Entry (app.py)") --> SIDE("Sidebar (Filters/Mode)")
    SIDE --> DASH("Dashboard Orchestrator (dashboard.py)")
    
    DASH --> NAV("Stable Navigation Bus (Radio Sync)")
    NAV --> FRAG_BUS{"Stable Fragment Bus"}
    
    FRAG_BUS --> MAP("fragment_live_map")
    FRAG_BUS --> CONS("fragment_live_consumption")
    FRAG_BUS --> AI("fragment_live_ai")
    
    DASH --> STATIC("Static Route Handler")
    STATIC --> GEN("tab_generation")
    STATIC --> FIN("tab_finance")
    STATIC --> FOR("tab_forecast")
    
    SUB("Sub-fragments (Tab Stability)") --> AI
    </div></div>
</div>

<!-- SECTION 03: FRAGMENT-BASED RENDERING STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія фрагментарного рендерингу</h2></div>
    <div class="glass-card flow-step">
        <p>Для досягнення максимальної продуктивності в <code>dashboard.py</code> реалізовано наступні підходи:</p>
        <ul>
            <li><b>Stable Fragment IDs:</b> Всі фрагменти викликаються в коді ЗАВЖДИ в однаковій послідовності, незалежно від активної вкладки. Це гарантує стабільність дельта-індексів Streamlit і запобігає "зникненню" віджетів.</li>
            <li><b>Lazy Data Access:</b> Фрагменти не отримують DataFrame як аргумент (щоб уникнути копіювання пам'яті). Вони отримують лише ключі та параметри фільтрації, самостійно звертаючись до <code>get_verified_data()</code>.</li>
            <li><b>Ghost-Busting:</b> Механізм очищення пам'яті через <code>gc.collect()</code> після завершення роботи кожного фрагмента для запобігання витокам RAM при тривалій роботі дашборду.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: NAVIGATION & ROUTING MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця навігації та роутингу</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Вкладка</th>
                    <th>Тип рендерингу</th>
                    <th>Режим доступності</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Map View</td><td>st.fragment (Interactive)</td><td>Live Mode Only</td></tr>
                <tr><td>Consumption</td><td>st.fragment (Lazy)</td><td>Universal</td></tr>
                <tr><td>AI Analytics</td><td>Nested Fragments</td><td>Universal</td></tr>
                <tr><td>Generation</td><td>Static Route</td><td>Live Mode Only</td></tr>
                <tr><td>Forecast AI</td><td>Controller Dispatch</td><td>Universal</td></tr>
                <tr><td>Finance</td><td>Static Route</td><td>Live Mode Only</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: THE STABLE FRAGMENT BUS (CORE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Шина стабільних фрагментів (Stable Bus)</h2></div>
    <div class="glass-card flow-step">
        <p>Критичною особливістю <code>dashboard.py</code> є блок <b>Stable Fragment Bus</b>. У Streamlit порядок виклику функцій визначає ідентифікатори об'єктів. Якщо ми будемо викликати фрагмент "Карта" тільки коли вибрана вкладка карти, то при переході на "Споживання" всі ID змістяться. Ми вирішили це через виклик ВСІХ фрагментів з прапором <code>active=False</code>, що зберігає дерево віджетів незмінним та забезпечує безшовне перемикання між аналітичними панелями.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Головного Оркестратора (Dashboard Core)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_dashboard_ui(data, mode, filters):
    1. INITIALIZE: st.title and Global Sync Metadata
    
    2. NAVIGATION:
           options = get_adaptive_options(mode)
           current_page = st.radio(options, horizontal=True)
           sync_nav_index()
           
    3. FRAGMENT_BUS (Registration Phase):
           fragment_map(data_key, filters, active=(page == 'Map'))
           fragment_consumption(data_key, filters, active=(page == 'Cons'))
           fragment_ai(data_key, filters, active=(page == 'AI'))
           
    4. STATIC_ROUTING (Legacy Phase):
           IF page == 'Generation': render_gen_tab()
           IF page == 'Finance': render_fin_tab()
           
    5. FOOTER: Apply global styles and copyright notice
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: ADAPTIVE INTERFACE LOGIC (LIVE vs KAGGLE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Логіка адаптації інтерфейсу (Dynamic Routing)</h2></div>
    <div class="glass-card flow-step">
        <p>Двигун <code>dashboard.py</code> автоматично змінює набір доступних вкладок залежно від джерела даних. В режимі "Kaggle" система приховує вкладки "Карта", "Генерація", "Аварії" та "Фінанси", оскільки історичні набори даних не містять необхідних полів (гео-координати, типи джерел тощо). Це запобігає спробам рендерингу порожніх сторінок та фокусує користувача на доступних інструментах аналізу споживання та AI-прогнозування.</p>
    </div>
</div>

<!-- SECTION 08: INTELLIGENT NAVIGATION SYNC (SYNC_NAV) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Інтелектуальна синхронізація навігації</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>sync_nav</code> відповідає за "пам'ять" інтерфейсу. При перемиканні режимів даних (Live <-> Kaggle) набір опцій у <code>st.radio</code> змінюється. Система автоматично перераховує індекси, щоб користувач залишався на логічно відповідній сторінці, або скидає індекс на 0, якщо поточна сторінка стала недоступною. Це виключає виникнення "Value Error" у віджетах Streamlit та гарантує стабільність навігації.</p>
    </div>
</div>

<!-- SECTION 09: MEMORY MANAGEMENT & GC (STABILITY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Управління пам'яттю та GC (Stability)</h2></div>
    <div class="glass-card flow-step">
        <p>Оскільки проект ATLAS працює з великими обсягами телеметрії, модуль <code>dashboard.py</code> активно використовує <b>Garbage Collection</b>. Після рендерингу кожної важкої вкладки (наприклад, "Генерація" або "Фінанси") ми примусово викликаємо <code>gc.collect()</code>. Це критично для систем, що працюють у режимі 24/7, оскільки запобігає поступовому "роздуванню" процесу Python та гарантує стабільно низьке використання RAM сервером.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM DESIGN & COPYRIGHT -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дизайн підвалу (Footer & UX)</h2></div>
    <div class="glass-card flow-step">
        <p>Кожна сторінка, згенерована через <code>dashboard.py</code>, завершується уніфікованим роздільником (Divider) та футером. Футер містить інформацію про авторські права та приналежність проекту. Це створює відчуття цілісного професійного додатку, а не розрізнених скриптів. Також тут забезпечується фінальний відступ для комфортного скролінгу на всіх типах пристроїв.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>UI Components</h4>
                <p>Постачальник стилів (CSS) та базових віджетів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>Data Loader</h4>
                <p>Центральне джерело перевірених та валідованих даних.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📂</div>
            <div class="role-content">
                <h4>Views Registry</h4>
                <p>Набір імпортованих модулів для кожної аналітичної вкладки.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (MULTI-WINDOW SUPPORT) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Multi-window Support)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Багатовіконного режиму**. Користувач зможе від'єднати будь-який фрагмент (наприклад, Карту або KPI) в окреме браузерне вікно для побудови професійної відеостіни в диспетчерській. Також буде додано підтримку <b>Hotkeys</b> (гарячих клавіш) для миттєвого перемикання між вкладками без використання миші.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Оркестратор Інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому вкладки перемикаються повільно?</b> — Це може статися при дуже великих часових діапазонах фільтрації. Спробуйте зменшити період у календарі.</p>
        <p><b>Куди зникла вкладка "Карта"?</b> — Ви перемкнулися в режим Kaggle. Карта доступна тільки для Live-даних Digital Twin.</p>
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
