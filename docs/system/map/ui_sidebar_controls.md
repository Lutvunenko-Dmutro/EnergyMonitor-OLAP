# Технічна специфікація: Панель Стратегічного Управління (COMMAND CENTER SIDEBAR)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM CONTROL | FILTERING ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎛️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Панель Управління</h1>
            <p class="mega-subtitle">Головний інтерфейсний вузол керування станом системи: динамічна фільтрація об'єктів, управління життєвим циклом датчиків та моніторинг системних ресурсів</p>
            <div class="status-tags"><span class="tag tag-online">CONTROL SIDEBAR ACTIVE</span><span class="tag tag-version">v2.4.0</span><span class="tag tag-role">COMMAND CENTER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Filters</span><span class="metric-value">Cascading SQL-Validated</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Sources</span><span class="metric-value">Live / Kaggle Hybrid</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📡</div><div class="metric-info"><span class="metric-label">Sensors</span><span class="metric-value">Subprocess Controller</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Health</span><span class="metric-value">RAM / CPU Analytics</span></div></div>
</div>

<!-- SECTION 01: SIDEBAR PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Стратегічного Управління</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>sidebar.py</code> є "Командним пульсом" проекту ATLAS. В складній системі моніторингу інтерфейс повинен не просто показувати дані, а давати інструменти для зміни контексту. Наша філософія базується на <b>Контекстній Динаміці</b>: кожне рішення в сайдбарі (вибір регіону, дати або джерела даних) миттєво змінює поведінку всього дашборду. Сайдбар також виконує роль адміністративної консолі, дозволяючи диспетчеру керувати фоновими процесами симуляції та стежити за технічним "здоров'ям" самого додатку.</p>
    </div>
</div>

<!-- SECTION 02: CONTROL FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема потоків управління (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    USER("Dispatcher Interaction") --> SRC("Data Source Switch (Live/Kaggle)")
    SRC --> FILTER("Cascade Filter Engine")
    
    FILTER --> REGION("Region Selection")
    REGION --> SQL("SQL Substation Resolver")
    SQL --> SUB("Substation Multiselect")
    
    FILTER --> DATE("Date Range Picker (Dynamic Bounds)")
    
    USER --> SENSOR("Simulation Controller (Subprocess)")
    SENSOR --> LOCK("Lock-file Management (sensors.lock)")
    
    USER --> ADMIN("Admin Actions (ETL/Seeder)")
    
    FILTER --> OUTPUT("(Region, Dates, Source, Sub)")
    OUTPUT --> DASHBOARD("Main UI Update")
    </div></div>
</div>

<!-- SECTION 03: CASCADING FILTER ENGINE (SQL-DRIVEN) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Каскадний двигун фільтрації (SQL)</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення цілісності вибору в <code>sidebar.py</code> реалізовано механізм каскадної фільтрації:</p>
        <ul>
            <li><b>Dynamic Regions:</b> Список регіонів формується на основі реального вмісту бази даних.</li>
            <li><b>Substation Resolver:</b> Після вибору регіону система виконує SQL-запит для отримання списку підстанцій, що належать саме цьому регіону. Це унеможливлює вибір неіснуючих комбінацій.</li>
            <li><b>Safe Defaults:</b> Якщо підстанції не обрані, система автоматично переходить у режим "Всі об'єкти", забезпечуючи безперервність аналізу.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: LIFECYCLE MANAGEMENT MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця управління життєвим циклом</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Компонент</th>
                    <th>Метод управління</th>
                    <th>Цільова функція</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Sensor Simulation</td><td>Subprocess / PID Kill</td><td>Емуляція потоку телеметрії</td></tr>
                <tr><td>Data Source</td><td>Session State Switch</td><td>Гібридний режим (Live/Archive)</td></tr>
                <tr><td>Date Filter</td><td>Dynamic Calendar Bounds</td><td>Вибір вікна спостереження</td></tr>
                <tr><td>RAM Monitor</td><td>Memory Helper Utility</td><td>Попередження про вичерпання RAM</td></tr>
                <tr><td>Database ETL</td><td>Professional Seeder</td><td>Скидання системи до еталону</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: SENSOR SIMULATION CONTROLLER (SUBPROCESS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Контролер симуляції датчиків (Subprocess)</h2></div>
    <div class="glass-card flow-step">
        <p>Сайдбар керує фоновим процесом <code>sensors_db.py</code>. Використовуючи <b>Lock-file</b> стратегію (файл <code>sensors.lock</code>), система точно знає, чи запущена зараз симуляція. Управління відбувається через <code>subprocess.Popen</code> з прапорами <code>CREATE_NO_WINDOW</code> (для Windows), що дозволяє симуляції працювати у фоновому режимі, не заважаючи оператору та не відкриваючи зайвих вікон консолі.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Управління (Sidebar Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_sidebar(data):
    1. HEARTBEAT: Touch logs/heartbeat.txt to signal UI activity
    
    2. SOURCE_SELECTION:
           source = radio("Data Source", options=[Live, Kaggle])
           st.session_state.active_source = source
           
    3. CASCADE_FILTERS:
           region = selectbox("Region", db.get_regions())
           sub_list = db.get_substations(region)
           selected_subs = multiselect("Substations", sub_list)
           
    4. DATE_CONTROL:
           dates = date_input("Range", min=df.min_ts, max=df.max_ts)
           
    5. PROCESS_MGMT:
           IF is_running(sensors.lock):
               IF btn_stop: kill_process(pid); remove_lock()
           ELSE:
               IF btn_start: spawn_subprocess("sensors_db.py")
               
    6. RETURN: (region, dates, source, selected_subs)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: HYBRID DATA SOURCE SWITCHING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Гібридне перемикання джерел даних</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль реалізує складну логіку перемикання між <b>Live-симуляцією</b> та <b>Kaggle-архівом</b>. При перемиканні система миттєво оновлює межі календаря та список доступних регіонів. Наприклад, при переході на Kaggle, список регіонів фіксується на "PJM Interconnection", а календар підлаштовується під часові межі американського енергоринку. Це забезпечує безшовний досвід дослідження різних типів даних в єдиному інтерфейсі.</p>
    </div>
</div>

<!-- SECTION 08: RENDER HEALTH & RAM MONITORING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Моніторинг здоров'я рендерингу (RAM)</h2></div>
    <div class="glass-card flow-step">
        <p>В нижній частині сайдбара інтегровано блок <b>Render Health</b>. Він у реальному часі відображає обсяг оперативної пам'яті, що використовується додатком. Використовується колірна індикація (Зелений/Оранжевий/Червоний) залежно від близькості до ліміту в 512MB. Також доступна секція "Top Objects", яка показує, які саме масиви даних (DataFrame) займають найбільше місця, допомагаючи адміністратору контролювати стабільність системи.</p>
    </div>
</div>

<!-- SECTION 09: ADMINISTRATIVE ETL TOOLS (DATA SEEDER) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Адміністративні інструменти ETL</h2></div>
    <div class="glass-card flow-step">
        <p>Для розробників та аудиторів передбачено кнопку "Перегенерувати Базу Даних". Вона запускає складний процес <b>ETL (Extract, Transform, Load)</b>, який повністю очищує SQLite базу та засіває її "ідеальними" синтетичними даними. Це необхідно для тестування нових ML-моделей на стабільному наборі даних, де гарантовано присутні всі типи аномалій та аварійних ситуацій.</p>
    </div>
</div>

<!-- SECTION 10: USER EXPERIENCE & ACCESSIBILITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Користувацький досвід (UX)</h2></div>
    <div class="glass-card flow-step">
        <p>Дизайн сайдбара сфокусований на швидкості доступу. Використовуються <code>expander</code>-блоки для приховування рідко використовуваних технічних дій, що дозволяє тримати основні фільтри завжди видимими. Кожен елемент має розширені підказки (Help Tooltips), які пояснюють, на які саме графіки вплине та чи інша зміна, забезпечуючи низький поріг входження для нових диспетчерів.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>Database Core</h4>
                <p>Низькорівневий провайдер SQL-запитів для фільтрації.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Data Seeder</h4>
                <p>Сервіс генерації професійних навчальних датасетів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🔍</div>
            <div class="role-content">
                <h4>Memory Helper</h4>
                <p>Інструмент діагностики системних ресурсів Python.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (VOICE COMMANDS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Voice Commands)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Голосового управління фільтрами</b>. Диспетчер зможе сказати: "Покажи підстанцію Дніпровська за вчора", і сайдбар автоматично оновить всі параметри. Також буде додано підтримку <b>Мульти-профілів</b> (User Presets), що дозволить одним кліком завантажувати складні набори фільтрів для різних сценаріїв аналізу.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Сайдбар та Управління</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому кнопка симуляції не активна?</b> — Перевірте наявність прав запису у папку <code>logs/</code> для створення lock-файлу.</p>
        <p><b>Як скинути всі фільтри відразу?</b> — Натисніть кнопку "Оновити дані" у самому верху сайдбара, це очистить кеш сесії.</p>
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
