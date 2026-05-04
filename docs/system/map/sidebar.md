# Технічна специфікація модуля: ui/segments/sidebar.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">COMMAND CENTER SIDEBAR & STRATEGIC CONTROL</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎛️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Панель Управління ATLAS</h1>
            <p class="mega-subtitle">Головний вузол стратегічного контролю: динамічна фільтрація, управління життєвим циклом датчиків та моніторинг здоров'я рендерингу</p>
            <div class="status-tags"><span class="tag tag-online">SIDEBAR ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">COMMAND CENTER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Filter</span><span class="metric-value">SQL-Validated</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Lifecycle</span><span class="metric-value">Sensor Control</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Source</span><span class="metric-value">Hybrid Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Health</span><span class="metric-value">RAM Monitor</span></div></div>
</div>

<!-- SECTION 01: COMMAND CENTER PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Стратегічного Управління</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>sidebar.py</code> є "Командним Центром" проекту ATLAS. В системах моніторингу енергомереж управління контекстом (вибір регіону, об'єкта, часу) є критично важливим для оперативності. Сайдбар забезпечує цілісність цього контексту, інтегруючи інструменти фільтрації з низькорівневим керуванням фоновими сервісами та діагностикою ресурсів сервера, створюючи єдину точку входу для всіх адміністративних та аналітичних дій.</p>
    </div>
</div>

<!-- SECTION 02: DYNAMIC FILTERING ARCHITECTURE -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Архітектура динамічної фільтрації</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI_SRC("Data Source Selection") --> SQL_REG("SQL: Fetch Regions")
    SQL_REG --> UI_REG("Region Dropdown")
    UI_REG --> SQL_SUB("SQL: Fetch Substations (by Region ID)")
    SQL_SUB --> UI_SUB("Multiselect Substation")
    UI_SUB --> CONTEXT("Active System Context")
    CONTEXT --> DASH("Dashboard Render Update")
    </div></div>
</div>

<!-- SECTION 03: SENSOR LIFECYCLE MANAGEMENT (SUBPROCESS API) -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Управління життєвим циклом датчиків</h2></div>
    <div class="glass-card flow-step">
        <p>Для реалізації "живого" моніторингу без блокування основного UI-потоку, сайдбар використовує <b>Subprocess API</b>:</p>
        <ul>
            <li><b>Simulation Start:</b> Запуск окремого процесу <code>sensors_db.py</code> з ізольованим оточенням та прихованим вікном (Windows-safe).</li>
            <li><b>Lock Mechanism:</b> Використання <code>sensors.lock</code> з PID-ідентифікатором для запобігання дублюванню процесів.</li>
            <li><b>Signal Control:</b> Коректна зупинка симуляції через <code>SIGTERM</code>, що гарантує цілісність бази даних при виключенні.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: HYBRID DATA SOURCE SWITCHING -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Гібридне перемикання джерел даних</h2></div>
    <div class="glass-card flow-step">
        <p>Система підтримує миттєву зміну аналітичної парадигми:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Джерело</th>
                    <th>Режим роботи</th>
                    <th>Механізм завантаження</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Локальна БД</td><td>Реактивний (Live)</td><td>SQL Alchemy / Live JSON</td></tr>
                <tr><td>Kaggle Archive</td><td>Історичний (Audit)</td><td>Lazy Parquet / Pandas</td></tr>
            </tbody>
        </table>
        <p class="section-desc">При зміні джерела сайдбар автоматично скидає кеш та переналаштовує діапазони дат під обраний масив даних.</p>
    </div>
</div>

<!-- SECTION 05: RENDER HEALTH & RAM MONITORING -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Моніторинг здоров'я рендерингу (Render Health)</h2></div>
    <div class="glass-card flow-step">
        <p>Інтегрований блок <b>Render Health</b> забезпечує прозорість використання ресурсів:</p>
        <ul>
            <li><b>RAM Tracking:</b> Візуалізація споживання пам'яті з кольоровою індикацією (Green < 256MB < Yellow < 512MB < Red).</li>
            <li><b>Top Objects:</b> Можливість розкрити список найбільших об'єктів у пам'яті (DataFrames/Models) для швидкої діагностики Memory Leaks.</li>
            <li><b>Cache Cleaning:</b> Кнопка швидкого очищення <code>st.cache_data.clear()</code> для примусового оновлення стану.</li>
        </ul>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (SIDEBAR RENDER LOGIC) -->
<div class="section-container">
    <div class="section-header":"06</span><h2 class="section-title">Псевдокод логіки рендерингу Сайдбара</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_sidebar(data):
    1. APPLY_CUSTOM_CSS()
    2. UPDATE_HEARTBEAT()
    
    3. RENDER Data Source Radio (Live vs Kaggle)
    4. IF mode == "Live":
           REGIONS = QUERY("SELECT name FROM Regions")
           SELECTED_REG = SELECTBOX(REGIONS)
           SUBSTATIONS = QUERY("SELECT name FROM Substations WHERE region = SELECTED_REG")
           SELECTED_SUB = MULTISELECT(SUBSTATIONS)
           
    5. RENDER Simulation Controls:
           IF NOT sensors_running: SHOW "Start Simulation" (Spawn Subprocess)
           ELSE: SHOW "Stop Simulation" (Kill PID from Lock)
           
    6. RENDER Health Monitor (RAM Status, GC Info)
    7. RETURN (selected_reg, selected_sub, date_range, source)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: CASCADING SQL VALIDATION -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Каскадна SQL-валідація фільтрів</h2></div>
    <div class="glass-card flow-step">
        <p>Для запобігання вибору підстанцій, що не належать до обраного регіону, сайдбар використовує каскадну логіку. Кожна зміна в селектбоксі регіону тригерує миттєвий SQL-запит до таблиці <code>Substations</code> з фільтром по <code>region_id</code>, що гарантує цілісність запитів у майбутніх аналітичних зрізах.</p>
    </div>
</div>

<!-- SECTION 08: SYSTEM HYGIENE & DATA SEEDER INTEGRATION -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Системна гігієна та ETL-інтеграція</h2></div>
    <div class="glass-card flow-step">
        <p>Сайдбар надає доступ до критичних ETL-інструментів через блок "Системні дії". Користувач може ініціювати повну перегенерацію бази даних (Data Seeder), що корисно для скидання системи до еталонного стану перед демонстрацією ML-можливостей.</p>
    </div>
</div>

<!-- SECTION 09: DATE PICKER BOUNDS OPTIMIZATION -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Оптимізація меж календаря</h2></div>
    <div class="glass-card flow-step">
        <p>Система автоматично вираховує <code>min_date</code> та <code>max_date</code> на основі наявного масиву завантажених даних. Це унеможливлює вибір дат, для яких відсутня телеметрія, що суттєво покращує UX, запобігаючи відображенню порожніх графіків.</p>
    </div>
</div>

<!-- SECTION 10: ADMINISTRATIVE ACTIONS LOGGING -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Логування адміністративних дій</h2></div>
    <div class="glass-card flow-step">
        <p>Будь-яка критична зміна (запуск симуляції, перегенерація БД) фіксується у системних логах. Сайдбар також оновлює <code>heartbeat.txt</code> при кожному рендері, що дозволяє іншим сервісам (наприклад, Watchdog) знати, що UI-сесія активна.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Database Engine</h4>
                <p>Використовує <code>db.run_query</code> для динамічних фільтрів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📦</div>
            <div class="role-content">
                <h4>Subprocess API</h4>
                <p>Управління життєвим циклом фонової симуляції датчиків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🩺</div>
            <div class="role-content">
                <h4>Memory Helper</h4>
                <p>Джерело даних для блоку Render Health.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (USER AUTH) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v3.0 (User Auth)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>авторизації користувачів</b> з різними рівнями доступу (Оператор/Адмін), додавання <b>збереження пресетів фільтрів</b> та інтеграція <b>голосового управління</b> навігацією через Speech-to-Text API.</p>
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
