# Технічна специфікація: Оркестратор Живої Телеметрії та Показників KPI (REAL-TIME TELEMETRY SEGMENT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">REAL-TIME STREAMING | REACTIVE KPI BUS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📡</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Жива Телеметрія</h1>
            <p class="mega-subtitle">Високопродуктивний оркестратор реального часу: реактивне оновлення KPI через st.fragment, інтелектуальне зчитування JSON-стейту та дворівнева система Fallback для моніторингу енергосистеми</p>
            <div class="status-tags"><span class="tag tag-online">TELEMETRY STREAM ACTIVE</span><span class="tag tag-version">v2.7.0</span><span class="tag tag-role">REAL-TIME DISPATCHER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Update Rate</span><span class="metric-value">5s (Reactive)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Source</span><span class="metric-value">JSON State / SQL Fallback</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Fail-safe Wrapper</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Latency</span><span class="metric-value">Near-Zero (Memory Bus)</span></div></div>
</div>

<!-- SECTION 01: REAL-TIME ORCHESTRATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Живої Телеметрії</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>live_kpi.py</code> є "Сенсорним ядром" проєкту ATLAS. В енергетиці затримка навіть у кілька секунд може бути критичною. Наша філософія базується на <b>Реактивній Швидкодії</b>: замість виконання важких повторюваних запитів до бази даних кожну секунду, ми створили механізм прямого зчитування оперативного стану (Snapshot) з легковагового JSON-файлу симуляції. Використання ізольованих фрагментів Streamlit дозволяє оновлювати ключові метрики (Частота, Навантаження, Здоров'я) без перезавантаження всього інтерфейсу, забезпечуючи плавні візуальні переходи як у справжньому диспетчерському HUD.</p>
    </div>
</div>

<!-- SECTION 02: TELEMETRY DATA FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема потоків телеметрії (Data Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    SENSORS("Simulation Sensors Engine") --> SNAP("Live State Snapshot (logs/live_state.json)")
    SNAP --> WRAP("live_telemetry_wrapper(active=True)")
    
    WRAP --> SOURCE_CHECK{"Source check?"}
    SOURCE_CHECK -- "Kaggle" --> KAG_STOP("Show static info banner")
    SOURCE_CHECK -- "Live / Sim" --> FRESH_CHECK{"Is JSON fresh (< 15s)?"}
    
    FRESH_CHECK -- "Yes (JSON OK)" --> JSON_PROC("Fast JSON Parse")
    JSON_PROC --> MAP_COLUMNS("Map fields: name->substation_name, load->actual_load_mw, etc.")
    MAP_COLUMNS --> SYNC_STATE("Sync session state: total_mw, freq, avg_health")
    SYNC_STATE --> KPI_RENDER("tab_kpi.render(df_telemetry)")
    
    FRESH_CHECK -- "No (JSON Stale/Missing)" --> SQL_FALL("SQL DB Fallback: get_latest_measurements()")
    SQL_FALL --> SQL_CHECK{"Data found?"}
    SQL_CHECK -- "Yes" --> KPI_RENDER
    SQL_CHECK -- "No" --> WARN_BAN("Show warning banner 'System awaiting sensors'")
    
    KPI_RENDER --> UI("Dynamic HUD metrics & substation tables")
    </div></div>
</div>

<!-- SECTION 03: FRAGMENT-BASED POLLING (5s CYCLE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Фрагментарне опитування (Цикл 5с)</h2></div>
    <div class="glass-card flow-step">
        <p>Для мінімізації навантаження на браузер та сервер модуль використовує <code>st.fragment</code> з параметром <code>run_every=5</code>. Це створює повністю автономний потік оновлення:</p>
        <ul>
            <li><b>Isolated Reruns:</b> Кожні 5 секунд оновлюється тільки верхня панель KPI та таблиця підстанцій. Карти, графіки фінансів та аналітики не перерендериваються, зберігаючи стан скролінгу та фокус користувача.</li>
            <li><b>Safe Polling:</b> Система автоматично зупиняє опитування, якщо вкладка не є активною або користувач перейшов у режим Kaggle, економлячи ресурси CPU.</li>
            <li><b>Jitter Control:</b> Оновлення відбувається без мерехтіння інтерфейсу завдяки швидкому читанню даних безпосередньо в оперативну пам'ять Streamlit.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: TELEMETRY PROCESSING MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця обробки телеметрії (JSON mapping)</h2></div>
    <div class="glass-card flow-step">
        <p>Вхідні дані з файлу <code>logs/live_state.json</code> проходять швидке векторне перейменування для повної сумісності з представленням KPI:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Вхідне поле (JSON)</th>
                    <th>Цільове поле (DataFrame)</th>
                    <th>Тип даних</th>
                    <th>Значення за замовчуванням</th>
                    <th>Критичність для системи</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>name</code></td><td><code>substation_name</code></td><td>String (Object)</td><td>None</td><td>Висока (Ідентифікатор)</td></tr>
                <tr><td><code>load</code></td><td><code>actual_load_mw</code></td><td>Float64</td><td>0.0</td><td>Висока (Баланс мережі)</td></tr>
                <tr><td><code>health</code></td><td><code>health_score</code></td><td>Float64</td><td>0.0</td><td>Висока (Показник зносу)</td></tr>
                <tr><td><code>temp</code></td><td><code>temperature_c</code></td><td>Float64</td><td>0.0</td><td>Середня (Діагностична)</td></tr>
                <tr><td><code>voltage</code></td><td><code>voltage_kv</code></td><td>Float64</td><td>0.0</td><td>Середня (Якість струму)</td></tr>
                <tr><td><code>h2</code></td><td><code>h2_ppm</code></td><td>Float64</td><td>0.0</td><td>Низька (Розчинений водень)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: ROBUST TWO-LAYER FALLBACK SYSTEM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Дворівнева система резервування (Fallback)</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення безперервного моніторингу в <code>live_kpi.py</code> реалізовано стійкий <b>Fallback Layer</b>:</p>
        <ol>
            <li><b>Перший рівень (JSON Stream):</b> Спроба зчитати файл <code>logs/live_state.json</code>. Якщо він існує та час його останньої модифікації ($T_{mtime}$) свіжий:
                $$\Delta T = T_{current} - T_{mtime} < 15\text{ секунд}$$
                система парсить JSON. Це швидкий шлях (Fast Path), що займає всього ~1-2 мс.
            </li>
            <li><b>Другий рівень (SQLite Fallback):</b> Якщо файл застарів або відсутній (наприклад, симулятор перезавантажується), система виконує прямий SQL-запит <code>get_latest_measurements()</code> до локальної бази даних SQLite. Це повільніший шлях (~20-50 мс), який гарантує збереження телеметрії на екрані за будь-яких умов.</li>
        </ol>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE & DETAILS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Оркестратора (Telemetry Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code class="language-python"># Захист та реактивне зчитування телеметрії (live_kpi.py)
FUNCTION live_telemetry_wrapper(active):
    1. INITIALIZE & CHECKS:
           IF active == False: RETURN
           
           region_filter = get_selected_region_from_session_state()
           active_source = get_active_source_from_session_state()
           
           IF active_source == "Еталонні дані (Kaggle)":
               st.info("📊 Режим історичного аналізу активний")
               st.caption("Жива телеметрія вимкнена.")
               RETURN
               
    2. LEVEL 1: JSON STATE MONITORING (Fast Path)
           IF FileExists("logs/live_state.json") and (CurrentTime() - FileMTime()) < 15 seconds:
               TRY:
                   state = json.load("logs/live_state.json")
                   df_telemetry = ConvertToDataFrame(state["substations"])
                   
                   # Column mapping & safety defaults
                   RenameColumns(df_telemetry, {
                       "name": "substation_name", "load": "actual_load_mw",
                       "health": "health_score", "temp": "temperature_c",
                       "h2": "h2_ppm", "voltage": "voltage_kv"
                   })
                   EnsureColumnsExist(df_telemetry, ["voltage_kv", "temperature_c", "h2_ppm", "health_score"], default=0.0)
                   
                   df_telemetry["frequency_hz"] = state["frequency_hz"]
                   
                   # Sync session state variables globally
                   st.session_state["live_total_mw"] = state["total_load_mw"]
                   st.session_state["live_freq"] = state["frequency_hz"]
                   st.session_state["live_avg_health"] = state["avg_health_score"]
                   
                   # Render KPI elements
                   tab_kpi.render(df_telemetry, region_filter=region_filter)
                   RETURN
               EXCEPT Exception as json_error:
                   Log("JSON read failed, switching to SQLite fallback")
                   
    3. LEVEL 2: SQL DATABASE FALLBACK (Slow Path)
           TRY:
               telemetry_data = db_services.get_latest_measurements()
               IF telemetry_data IS empty:
                   st.warning("🔌 СИСТЕМА МОНІТОРИНГУ В ОЧІКУВАННІ ДАНИХ")
                   st.info("Запустіть датчики в боковій панелі (Sidebar) для старту симуляції.")
               ELSE:
                   tab_kpi.render(telemetry_data, region_filter=region_filter)
           EXCEPT Exception as db_error:
               st.error("Помилка зв'язку з датчиками.")
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: SESSION STATE SYNCHRONIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Синхронізація глобального стану (Global Sync)</h2></div>
    <div class="glass-card flow-step">
        <p>Окрім безпосередньої візуалізації, <code>live_kpi.py</code> виконує роль <b>State Provider</b>. Під час кожного 5-секундного тику він синхронізує агреговані метрики всієї системи у Streamlit <code>st.session_state</code>:</p>
        <ul>
            <li><code>st.session_state["live_total_mw"]</code>: сумарне навантаження енерговузла.</li>
            <li><code>st.session_state["live_freq"]</code>: поточна частота струму в мережі (Hz).</li>
            <li><code>st.session_state["live_avg_health"]</code>: середній індекс здоров'я трансформаторів.</li>
        </ul>
        <p>Це дозволяє іншим віджетам (наприклад, сайдбару чи інтерактивній карті) миттєво отримувати свіжі глобальні показники без виконання повторних математичних операцій.</p>
    </div>
</div>

<!-- SECTION 08: SAFE FRAGMENT WRAPPER (COMPATIBILITY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Захисна обгортка фрагментів (Safe Wrapper)</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення крос-платформності та сумісності із застарілими версіями бібліотек у хмарних контейнерах, у модулі реалізовано динамічний декоратор-запобіжник <code>safe_fragment</code>:</p>
        <pre><code class="language-python">def safe_fragment(run_every=None):
    def decorator(func):
        if hasattr(st, "fragment"):
            return st.fragment(run_every=run_every)(func)
        return func
    return decorator</code></pre>
        <p>Якщо Streamlit у поточному оточенні не має вбудованої підтримки <code>st.fragment</code>, система м'яко переходить на класичний повний рендеринг сторінки без збоїв імпорту та критичних помилок (graceful degradation).</p>
    </div>
</div>

<!-- SECTION 09: PERFORMANCE OPTIMIZATION (JSON vs SQL) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Оптимізація продуктивності (JSON vs SQL)</h2></div>
    <div class="glass-card flow-step">
        <p>Зчитування JSON-файлу з SSD/RAM-диска в 10-15 разів швидше за виконання SQL-запитів до реляційних баз даних SQLite, навіть з урахуванням індексів. Це досягається завдяки:</p>
        <ul>
            <li>Відсутності парсингу SQL-синтаксису та планування запитів СКБД.</li>
            <li>Однопотоковому прямому читанню структурованого бінарного потоку.</li>
            <li>Швидкому векторному мапуванню колонок через бібліотеку Pandas.</li>
            <li>Мінімізації блокувань файлу бази даних (database locks) при паралельному записі від симулятора датчиків.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: USER NOTIFICATION & STATUS CODES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Повідомлення та статус-коди (UX)</h2></div>
    <div class="glass-card flow-step">
        <p>При переході системи в очікування або втраті сигналу, користувач не стикається з порожнім екраном чи технічним трейсбеком помилок. Замість цього відображаються інформативні Cyber-HUD банери:</p>
        <div style="background: rgba(31, 111, 235, 0.1); border: 1px solid rgba(88, 166, 255, 0.2); padding: 12px; border-radius: 8px; margin-top: 10px;">
            <span>🔌</span> <b>СИСТЕМА МОНІТОРИНГУ В ОЧІКУВАННІ ДАНИХ</b><br>
            <span style="font-size: 12px; color: var(--text-dim);">Запустіть датчики в боковій панелі (Sidebar) для старту симуляції Digital Twin.</span>
        </div>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>tab_kpi.render()</h4>
                <p>Представлення KPI, безпосередній візуалізатор підготовленого DataFrame.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📂</div>
            <div class="role-content">
                <h4>logs/live_state.json</h4>
                <p>Файловий Snapshot оперативного стану симуляції датчиків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>db_services.py</h4>
                <p>Компонент прямого доступу до SQLite бази даних для резервного зчитування.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (WEBSOCKET STREAMING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (WebSocket Streaming)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується перехід від файлового опитування (Polling) до **WebSocket трансляції**:</p>
        <ul>
            <li>Датчики симулятора будуть транслювати дані безпосередньо в клієнтську частину браузера через веб-сокети.</li>
            <li>Це знизить затримку передачі до рекордних <b>50-100 мс</b>, забезпечуючи абсолютно плавне оновлення частотних коливань (без затримок опитування диска).</li>
            <li>Перехід на бінарні Protobuf пакети для максимального стиснення даних телеметрії при роботі через зовнішні мережі з низькою пропускною здатністю.</li>
        </ul>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Жива Телеметрія</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому дані оновлюються тільки кожні 5 секунд, а не кожну секунду?</b><br>— Опитування кожні 5 секунд є математично оптимальним для мінімізації навантаження на CPU сервера Streamlit та збереження плавності анімацій інтерфейсу без перевантаження мережевого каналу.</p>
        
        <p><b>Що відбудеться, якщо файл live_state.json буде пошкоджено під час перезапису?</b><br>— Система має блок перехоплення помилок <code>try-except</code>. При виникненні будь-яких проблем із читанням файлу, оркестратор миттєво перемкнеться на читання останніх вимірювань з бази даних.</p>
        
        <p><b>Чому жива телеметрія вимкнена в режимі Kaggle?</b><br>— Історичний набір даних Kaggle є статичним і не підтримує симуляцію реального часу, тому для нього виводиться інформаційний банер і фіксований зріз даних.</p>
        
        <p><b>Як часто симулятор оновлює JSON-файл?</b><br>— Симулятор Digital Twin перезаписує JSON Snapshot кожні 3-5 секунд, синхронізуючи показники частоти та навантаження ліній.</p>
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
