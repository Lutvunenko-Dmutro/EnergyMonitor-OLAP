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
        <p>Модуль <code>sidebar.py</code> є "Командним пульсом" проєкту ATLAS. В складній системі ситуаційного моніторингу інтерфейс повинен не просто показувати статичні графіки, а давати інструменти для миттєвої зміни аналітичного контексту. Наша філософія базується на <b>Контекстній Динаміці</b>: кожне рішення в сайдбарі (вибір регіону, часового діапазону або джерела даних) негайно перебудовує аналітичну модель всього дашборду. Сайдбар також виконує роль консолі системного адміністратора, дозволяючи диспетчеру безпосередньо керувати фоновими процесами емуляції та відстежувати технічне здоров'я самого додатку.</p>
    </div>
</div>

<!-- SECTION 02: CONTROL FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема потоків управління (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    USER("Dispatcher Interaction") --> SRC_SW("Data Source Switch (Live/Kaggle)")
    
    SRC_SW -- "Kaggle Mode" --> KAG_SET("Fix region to US (PJM)<br>Lazy Load Kaggle timestamp bounds")
    SRC_SW -- "Live / Sim Mode" --> LIVE_SET("Extract regions list from local DB")
    
    KAG_SET --> SUB_RESOLVE("Cascade Substation Resolver (SQL)")
    LIVE_SET --> SUB_RESOLVE
    
    SUB_RESOLVE --> SUB_LIST("Multiselect: Choose specific substations")
    SUB_LIST --> DATE_INPUT("Date Range input (Dynamic date key check)")
    
    USER --> HEARTBEAT("Touch logs/heartbeat.txt (Activity signal)")
    USER --> SIM_CONTROL{"Sim Control Action?"}
    
    SIM_CONTROL -- "▶️ Start Simulation" --> SPAWN_PROC("Spawn sensors_db.py subprocess")
    SPAWN_PROC --> LOCK_WRITE("Write PID to logs/sensors.lock")
    
    SIM_CONTROL -- "🛑 Stop Simulation" --> READ_PID("Read PID from sensors.lock")
    READ_PID --> KILL_PROC("os.kill(pid, SIGTERM)")
    KILL_PROC --> LOCK_DEL("Unlink sensors.lock")
    
    USER --> ETL_ACTION("Click Reset Database")
    ETL_ACTION --> ETL_RUN("Run generate_professional_data() ETL")
    
    DATE_INPUT --> RETURN_VALS("Return: selected_region, date_range, data_source, substations")
    RETURN_VALS --> DASHBOARD("Main UI Update Trigger")
    </div></div>
</div>

<!-- SECTION 03: CASCADING FILTER ENGINE (SQL-DRIVEN) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Каскадний двигун фільтрації (SQL)</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення цілісності вибору в <code>sidebar.py</code> реалізовано механізм каскадної фільтрації:</p>
        <ul>
            <li><b>Dynamic Regions:</b> Список регіонів автоматично формується на основі реального вмісту бази даних.</li>
            <li><b>Substation Resolver (Зв'язаний SQL-запит):</b> Після вибору регіону система виконує зв'язаний SQL-запит для отримання списку підстанцій, що належать саме цьому регіону. Це унеможливлює вибір неіснуючих комбінацій:
            <pre><code class="language-sql">SELECT s.substation_name 
FROM Substations s
JOIN Regions r ON s.region_id = r.region_id
WHERE r.region_name = :r
ORDER BY s.substation_name</code></pre>
            </li>
            <li><b>Safe Defaults:</b> Якщо підстанції у списку не обрані, система автоматично переходить у режим "Всі об'єкти", забезпечуючи безперервність аналізу без збоїв рендерингу.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: LIFECYCLE MANAGEMENT MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця управління життєвим циклом системи</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Контрольований об'єкт</th>
                    <th>Джерело керування / Дія</th>
                    <th>Технічний механізм реалізації</th>
                    <th>Операційне призначення</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Sensor Simulation</b></td><td>Кнопка "Запустити Симуляцію Датчиків"</td><td><code>subprocess.Popen</code> з <code>CREATE_NO_WINDOW</code>, PID запис у lock-файл.</td><td>Ініціалізація емулятора фонового потоку вимірювань підстанцій.</td></tr>
                <tr><td><b>Active Telemetry Kill</b></td><td>Кнопка "Зупинити Датчики"</td><td><code>os.kill(pid, signal.SIGTERM)</code>, видалення lock-файлу.</td><td>Зупинка фонового емулятора для економії ресурсів хоста.</td></tr>
                <tr><td><b>Data Source</b></td><td>Радіо-перемикач 📂 Джерело даних</td><td>Streamlit <code>session_state.active_source</code> з динамічним індексом.</td><td>Перемикання між Live-симуляцією та Kaggle-архівом PJM.</td></tr>
                <tr><td><b>Database ETL Seeder</b></td><td>Кнопка "Перегенерувати Базу Даних"</td><td><code>generate_professional_data()</code>, повне очищення БД.</td><td>Скидання бази до еталонного стану для ML-тестування.</td></tr>
                <tr><td><b>RAM Watchdog</b></td><td>Індикатор Render Health</td><td><code>get_resource_status()</code>, кольорове зонування.</td><td>Попередження диспетчера про вичерпання ліміту пам'яті (512MB).</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: SENSOR SIMULATION CONTROLLER (SUBPROCESS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Контролер фонової симуляції датчиків</h2></div>
    <div class="glass-card flow-step">
        <p>Сайдбар керує життєвим циклом фонового процесу <code>src.services.sensors_db</code>. Використовуючи <b>lock-file стратегію</b> (файл <code>logs/sensors.lock</code>), система точно знає, чи запущена зараз симуляція:</p>
        <ol>
            <li><b>Запуск:</b> При натисканні кнопки "▶️ Запустити Симуляцію Датчиків" створюється ізольований фоновий процес за допомогою <code>subprocess.Popen</code>. Для Windows додається прапор <code>creationflags=subprocess.CREATE_NO_WINDOW</code>, щоб приховати зайві консольні вікна.</li>
            <li><b>Зупинка:</b> При натисканні кнопки "🛑 Зупинити Датчики" система зчитує PID з файлу <code>logs/sensors.lock</code> та виконує м'яке припинення роботи процесу через <code>os.kill(pid, signal.SIGTERM)</code>, після чого lock-файл видаляється з диска.</li>
        </ol>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE & AST DETAILS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Управління (Sidebar Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code class="language-python"># Оркестрація панелі управління (sidebar.py)
FUNCTION render_sidebar(data):
    1. INJECT STYLES & TOUCH HEARTBEAT:
           apply_custom_css()
           touch("logs/heartbeat.txt") # Signal UI activity to helper cron
           
    2. MANUAL RERUN BUTTON:
           IF st.sidebar.button("🔄 Оновити дані"):
               st.cache_data.clear()
               st.rerun()
               
    3. DATA SOURCE PROTOCOL SWITCH:
           options = ["Локальна БД (Симуляція)", "Еталонні дані (Kaggle)"]
           source = st.sidebar.radio("📂 Джерело даних:", options, key="active_source")
           
    4. CASCADING REGION & SUBSTATIONS RESOLVER:
           IF source == "Еталонні дані (Kaggle)":
               selected_region = "США (PJM Interconnection)" # Fixed region
               active_load_df = load_kaggle_lazy()
               sub_names = GetUniqueSubstationsList(active_load_df)
           ELSE:
               active_load_df = data["load"]
               regions_list = ["Всі регіони"] + GetRegionsListFromDB(active_load_df)
               selected_region = st.sidebar.selectbox("📍 Регіон:", regions_list)
               
               # Cascade SQL Query depending on selected region
               IF selected_region != "Всі регіони":
                   substations_df = db.run_query("SELECT substation_name FROM Substations s JOIN Regions r ON s.region_id = r.region_id WHERE r.region_name = :r", {"r": selected_region})
               ELSE:
                   substations_df = db.run_query("SELECT substation_name FROM Substations")
               sub_names = GetSubstationsList(substations_df)
               
    5. MULTISELECT SUBSTATIONS:
           selected_sub = st.sidebar.multiselect("🔍 Підстанція:", options=sub_names, default=[])
           IF selected_sub IS empty:
               selected_sub = ["Усі підстанції"]
               
    6. DYNAMIC DATE CALENDAR CONFIG:
           Get min_date and max_date from active_load_df timestamps
           default_start = max_date - 30 days
           date_key = f"date_filter_{source_first_word}"
           
           date_range = st.sidebar.date_input("📅 Період:", value=(default_start, max_date), min=min_date, max=max_date, key=date_key)
           
    7. SUBPROCESS LIFE CYCLE MANAGER:
           lock_file = Path("logs/sensors.lock")
           IF NOT lock_file.exists():
               IF st.sidebar.button("▶️ Запустити Симуляцію Датчиків"):
                   SpawnSubprocess("src.services.sensors_db", creationflags=CREATE_NO_WINDOW)
                   st.rerun()
           ELSE:
               ShowSuccess("✅ Симуляція активна (15 хв)")
               IF st.sidebar.button("🛑 Зупинити Датчики"):
                   pid = ReadPID(lock_file)
                   os.kill(pid, SIGTERM)
                   DeleteLock(lock_file)
                   st.rerun()
                   
    8. ADMIN ETL BUTTON (Data Seeder):
           WITH expander("⚙️ Системні Дії"):
               IF st.button("♻️ Перегенерувати Базу Даних"):
                   st.spinner("⏳ Генерація (ETL)...")
                   generate_professional_data()
                   st.cache_data.clear()
                   st.rerun()
                   
    9. RESOURCE STATUS (Render Health):
           status, usage, color, top_objs = get_resource_status()
           st.sidebar.write(f"RAM Usage: :{color}[**{usage:.1f} MB**]")
           IF top_objs:
               WITH expander("🔍 Top Objects"):
                   FOR name, size in top_objs:
                       st.caption(f"{name}: {size:.1f} MB")
                       
    10. RETURN selected_region, date_range, source, selected_sub
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: HYBRID DATA SOURCE SWITCHING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Гібридне перемикання джерел даних</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль реалізує складну логіку перемикання між <b>Live-симуляцією</b> та <b>Kaggle-архівом</b>. При перемиканні система миттєво оновлює межі календаря та список доступних регіонів. Наприклад, при переході на Kaggle, список регіонів фіксується на "США (PJM Interconnection)", а календар підлаштовується під часові межі американського енергоринку. Це забезпечує безшовний досвід дослідження різних типів даних в єдиному інтерфейсі.</p>
    </div>
</div>

<!-- SECTION 08: RENDER HEALTH & RAM MONITORING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Моніторинг здоров'я рендерингу (RAM)</h2></div>
    <div class="glass-card flow-step">
        <p>В нижній частині сайдбара інтегровано блок <b>Render Health</b>. Він у реальному часі відображає обсяг оперативної пам'яті, що використовується додатком. Використовується колірна індикація (Зелений / Оранжевий / Червоний) залежно від близькості до ліміту в 512MB.</p>
        <p>Також доступна розширювана секція "Top Objects", яка показує, які саме масиви даних (DataFrame) займають найбільше місця у пам'яті, допомагаючи адміністратору контролювати стабільність системи та вчасно застосовувати очищення кешу.</p>
    </div>
</div>

<!-- SECTION 09: ADMINISTRATIVE ETL TOOLS (DATA SEEDER) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Адміністративні інструменти ETL</h2></div>
    <div class="glass-card flow-step">
        <p>Для розробників та аудиторів передбачено кнопку "♻️ Перегенерувати Базу Даних". Вона запускає складний процес <b>ETL (Extract, Transform, Load)</b>, який повністю очищує SQLite базу та засіває її "ідеальними" синтетичними даними. Це необхідно для тестування нових ML-моделей на стабільному наборі даних, де гарантовано присутні всі типи аномалій, а також фізичні залежності та аварійні ситуації.</p>
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
                <p>Низькорівневий провайдер SQL-запитів для фільтрації та каскадного розв'язання підстанцій.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Data Seeder</h4>
                <p>ETL сервіс генерації та засівання професійних навчальних датасетів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🔍</div>
            <div class="role-content">
                <h4>Memory Helper</h4>
                <p>Інструмент діагностики оперативної пам'яті (RAM) та моніторингу об'єктів Streamlit.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>styles.py CSS</h4>
                <p>Постачальник кастомних CSS-стилів для кнопок, радіо-груп та сайдбару.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (VOICE COMMANDS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Voice Commands)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Голосового управління фільтрами</b>:</p>
        <ul>
            <li>Диспетчер зможе сказати: "Покажи підстанцію Дніпровська за минулий вівторок", і сайдбар автоматично оновить всі селектори та календарні віджети.</li>
            <li>Реалізація механізму <b>Мульти-профілів (User Presets)</b>, що дозволить одним кліком зберігати та завантажувати складні набори фільтрів для різних типів чергувань.</li>
        </ul>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Сайдбар та Управління</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому кнопка "Запустити Симуляцію Датчиків" не активна або не запускає процес?</b><br>— Перевірте наявність прав запису у папку <code>logs/</code> на вашому сервері. Симулятору необхідно створити файл <code>sensors.lock</code> з поточним PID для контролю фонового процесу.</p>
        
        <p><b>Чому при виборі Kaggle-джерела регіон США стає неактивним?</b><br>— Еталонний історичний датасет Kaggle містить виключно дані енергоринку PJM США, тому вибір інших регіонів заблоковано на рівні логіки сайдбару для уникнення помилок сумісності.</p>
        
        <p><b>Що робить кнопка "Оновити дані"?</b><br>— Вона повністю очищує внутрішній кеш пам'яті Streamlit (<code>st.cache_data.clear()</code>) та ініціює повний перечит файлів бази даних, скидаючи всі застарілі обчислення.</p>
        
        <p><b>Чому RAM Usage відображається червоним кольором?</b><br>— Це означає, що використання оперативної пам'яті наближається до хмарного ліміту (наприклад, > 400 MB). Натисніть "Оновити дані" або перезавантажте сторінку для очищення пам'яті.</p>
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
