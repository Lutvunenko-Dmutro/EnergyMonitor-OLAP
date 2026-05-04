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
        <p>Модуль <code>live_kpi.py</code> є "Сенсорним ядром" проекту ATLAS. В енергетиці затримка навіть у кілька секунд може бути критичною. Наша філософія базується на <b>Реактивній Швидкодії</b>: замість важких запитів до бази даних кожну секунду, ми створили механізм прямого зчитування оперативного стану (Snapshot) з JSON-файлу симуляції. Використання ізольованих фрагментів Streamlit дозволяє оновлювати ключові метрики (Частота, Навантаження, Здоров'я) без перезавантаження всього інтерфейсу, забезпечуючи плавність роботи як у справжньому диспетчерському HUD.</p>
    </div>
</div>

<!-- SECTION 02: TELEMETRY DATA FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема потоків телеметрії (Data Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    SENSORS("Simulation Sensors Engine") --> SNAP("Live State Snapshot (JSON)")
    SNAP --> WRAP("live_telemetry_wrapper (st.fragment)")
    
    WRAP --> CHECK{"Check Freshness?"}
    
    CHECK -- "< 15s (Fresh)" --> JSON_PROC("Fast JSON Parse & Map")
    CHECK -- "> 15s (Stale)" --> SQL_FALL("SQL DB Fallback Query")
    
    JSON_PROC --> STATE_SYNC("Session State Global Sync")
    SQL_FALL --> STATE_SYNC
    
    STATE_SYNC --> KPI_RENDER("KPI View Render (tab_kpi)")
    KPI_RENDER --> UI("Dynamic Dashboard Metrics")
    </div></div>
</div>

<!-- SECTION 03: FRAGMENT-BASED POLLING (5s CYCLE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Фрагментарне опитування (Цикл 5с)</h2></div>
    <div class="glass-card flow-step">
        <p>Для мінімізації навантаження на браузер та сервер модуль використовує <code>st.fragment</code> з параметром <code>run_every=5</code>. Це створює автономний потік оновлення:</p>
        <ul>
            <li><b>Isolated Reruns:</b> Оновлюється тільки верхня панель KPI та таблиця підстанцій. Карти та графіки аналітики залишаються нерухомими.</li>
            <li><b>Safe Polling:</b> Система автоматично зупиняє опитування, якщо вкладка не активна або користувач перейшов у режим "Kaggle", економлячи ресурси.</li>
            <li><b>Jitter Control:</b> Оновлення відбувається плавно, без мерехтіння інтерфейсу, завдяки використанню плейсхолдерів Streamlit.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: TELEMETRY PROCESSING MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця обробки телеметрії</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Параметр</th>
                    <th>Трансформація (Mapping)</th>
                    <th>Критичність</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>load</td><td>actual_load_mw</td><td>Висока (Баланс)</td></tr>
                <tr><td>health</td><td>health_score</td><td>Висока (Надійність)</td></tr>
                <tr><td>temp</td><td>temperature_c</td><td>Середня (Діагностика)</td></tr>
                <tr><td>voltage</td><td>voltage_kv</td><td>Середня (Якість)</td></tr>
                <tr><td>h2</td><td>h2_ppm</td><td>Низька (Превентивна)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: ROBUST TWO-LAYER FALLBACK SYSTEM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Дворівнева система резервування (Fallback)</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення безперервного моніторингу в <code>live_kpi.py</code> реалізовано <b>Fallback Layer</b>. Якщо файл <code>live_state.json</code> відсутній або застарів (старше 15 секунд), система автоматично перемикається на прямі SQL-запити до бази даних SQLite через <code>get_latest_measurements()</code>. Це гарантує, що оператор ніколи не побачить "порожній екран", навіть якщо двигун симуляції було перезавантажено або він тимчасово припинив трансляцію стріму.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Оркестратора (Telemetry Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION live_telemetry_wrapper(active):
    1. VALIDATE: IF mode == 'Kaggle' OR active == False: RETURN
    
    2. TRY_JSON_STREAM:
           IF file_exists(live_state.json) AND is_fresh:
               data = json.load(file)
               df = map_to_standard_schema(data)
               UPDATE_SESSION_STATE(totals, freq, health)
               RENDER_KPI(df)
               RETURN
               
    3. TRY_SQL_FALLBACK:
           df = db.get_latest_measurements()
           IF df exists:
               RENDER_KPI(df)
           ELSE:
               SHOW_WARNING("Sensors Offline")
               
    4. REPEAT: Trigger every 5 seconds (st.fragment)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: SESSION STATE SYNCHRONIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Синхронізація глобального стану (Global Sync)</h2></div>
    <div class="glass-card flow-step">
        <p>Окрім візуалізації, модуль виконує роль <b>State Provider</b>. Під час кожного циклу оновлення він записує агреговані системні показники (Total MW, Avg Health, Frequency) безпосередньо у <code>st.session_state</code>. Це дозволяє іншим частинам додатку (наприклад, Сайдбару або Карті) використовувати найсвіжіші дані без виконання власних дорогих запитів, створюючи єдину "Шину Даних" (Data Bus) всередині Атласу.</p>
    </div>
</div>

<!-- SECTION 08: SAFE FRAGMENT WRAPPER (COMPATIBILITY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Захисна обгортка фрагментів (Safe Wrapper)</h2></div>
    <div class="glass-card flow-step">
        <p>Оскільки <code>st.fragment</code> є відносно новою функцією, модуль містить декоратор-запобіжник <code>safe_fragment</code>. Він перевіряє наявність підтримки фрагментів у поточному середовищі виконання. Якщо версія Streamlit застаріла (наприклад, у деяких хмарних контейнерах), система автоматично переходить на звичайний рендеринг, не викликаючи критичних помилок імпорту, що робить ATLAS максимально крос-платформним.</p>
    </div>
</div>

<!-- SECTION 09: PERFORMANCE OPTIMIZATION (JSON vs SQL) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Оптимізація продуктивності (JSON vs SQL)</h2></div>
    <div class="glass-card flow-step">
        <p>Зчитування JSON-файлу з диска (RAM-диска в ідеалі) у 10-15 разів швидше за SQL-запит до SQLite з індексами. Модуль <code>live_kpi.py</code> експлуатує цю перевагу, роблячи ATLAS надзвичайно швидким. Всі маніпуляції з даними (rename, fillna, type conversion) виконуються у векторному режимі через Pandas, що гарантує низьке навантаження на процесор навіть при моніторингу сотень підстанцій у реальному часі.</p>
    </div>
</div>

<!-- SECTION 10: USER NOTIFICATION & STATUS CODES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Повідомлення та статус-коди (UX)</h2></div>
    <div class="glass-card flow-step">
        <p>При виникненні проблем зі стрімом даних модуль виводить спеціальні **Status Info** блоки. Наприклад, якщо датчики вимкнені, користувач бачить пораду запустити їх у сайдбарі. Це усуває стан невизначеності ("Чому нічого не показує?") та забезпечує високий рівень UX, ведучи оператора за руку через технічні нюанси роботи системи Digital Twin.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>KPI View</h4>
                <p>Кінцевий споживач та візуалізатор підготовлених даних.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📂</div>
            <div class="role-content">
                <h4>Live State JSON</h4>
                <p>Первинне джерело Snapshot-телеметрії симуляції.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>DB Services</h4>
                <p>Fallback-провайдер останніх вимірювань з БД.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (WEBSOCKET STREAMING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (WebSocket Streaming)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується перехід від опитування файлу (Polling) до **WebSocket трансляції**. Датчики будуть надсилати дані безпосередньо в браузер через сокети, що дозволить знизити частоту оновлення до 100 мс для плавної візуалізації частотних коливань. Також буде додано підтримку <b>Binary Protobuf</b> для стиснення телеметрії при передачі через глобальну мережу.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Жива Телеметрія</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому дані оновлюються тільки кожні 5 секунд?</b> — Це оптимальний баланс між швидкістю реагування та навантаженням на CPU сервера Streamlit.</p>
        <p><b>Що робити, якщо з'явилося попередження "Система в очікуванні"?</b> — Перейдіть у Sidebar та натисніть "Запустити Симуляцію Датчиків".</p>
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
