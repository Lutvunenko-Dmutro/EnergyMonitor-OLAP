# Технічна специфікація модуля: ui/segments/live_kpi.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">REAL-TIME TELEMETRY ORCHESTRATOR & KPI TRACKER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛰️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Оркестратор Телеметрії KPI</h1>
            <p class="mega-subtitle">Система миттєвої візуалізації стану мережі: реактивне оновлення 5с, пряме зчитування JSON-стейту та робастний рівень Fallback-обробки</p>
            <div class="status-tags"><span class="tag tag-online">TELEMETRY STREAM ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">REAL-TIME ENGINE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Latency</span><span class="metric-value">< 100ms (JSON)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Polling</span><span class="metric-value">5s Fragment</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🤝</div><div class="metric-info"><span class="metric-label">Sync</span><span class="metric-value">Simulation State</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Safety</span><span class="metric-value">SQL Fallback</span></div></div>
</div>

<!-- SECTION 01: REAL-TIME TELEMETRY PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Телеметрії Реального Часу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>live_kpi.py</code> є "Очима" оператора ATLAS. В енергетиці затримка навіть у кілька секунд може бути критичною. Наша філософія базується на створенні ефекту "нульової затримки" через використання легких JSON-зліпків стану симуляції, що дозволяє UI-шару миттєво реагувати на зміни частоти, напруги та навантаження без перевантаження основної бази даних аналітичними запитами.</p>
    </div>
</div>

<!-- SECTION 02: ACTIVE TELEMETRY HANDSHAKE ARCHITECTURE -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Архітектура телеметрійного рукостискання</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    SENSORS("Симуляція Датчиків") --> JSON_STATE("live_state.json (Flash Storage)")
    JSON_STATE --> WRAPPER("live_telemetry_wrapper (5s Poll)")
    WRAPPER --> VALID{"JSON Свіжий (<15с)?"}
    VALID -- "Так" --> MAPPER("Simulation State Mapper")
    VALID -- "Ні" --> SQL_FALL("SQL Fallback: get_latest_measurements()")
    MAPPER & SQL_FALL --> RENDER("KPI Cards Render")
    </div></div>
</div>

<!-- SECTION 03: FRAGMENT-BASED POLLING STRATEGY -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Стратегія фрагментованого опитування</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення високої динаміки інтерфейсу без перезавантаження всієї сторінки, модуль використовує <code>st.fragment(run_every=5)</code>:</p>
        <ul>
            <li><b>Isolated Update:</b> Оновлюється лише блок KPI-карток, не перериваючи взаємодію користувача з іншими графіками.</li>
            <li><b>Frequency Sync:</b> Опитування синхронізоване з темпом генерації симуляції.</li>
            <li><b>Safe Wrapper:</b> Реалізовано <code>safe_fragment</code> декоратор для коректної роботи в середовищах з різними версіями Streamlit.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: SIMULATION STATE SYNC LOGIC -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Логіка синхронізації стану симуляції</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль виконує складне мапування сирих JSON-даних у формати, сумісні з аналітичними представленнями:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Вхід (JSON)</th>
                    <th>Вихід (DataFrame)</th>
                    <th>Фізичний показник</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>load</td><td>actual_load_mw</td><td>Активне навантаження (МВт)</td></tr>
                <tr><td>temp</td><td>temperature_c</td><td>Термічний стан масла (°C)</td></tr>
                <tr><td>h2</td><td>h2_ppm</td><td>Концентрація водню (DGA)</td></tr>
                <tr><td>voltage</td><td>voltage_kv</td><td>Рівень напруги на шинах (кВ)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: ROBUST FALLBACK LAYER (SQL VS STREAM) -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Робастний рівень Fallback-обробки</h2></div>
    <div class="glass-card flow-step">
        <p>Система має вбудований інтелект для вибору джерела даних. Якщо файл <code>live_state.json</code> відсутній або застарів (старше 15 секунд), <code>live_kpi.py</code> автоматично перемикається на запити до PostgreSQL через <code>get_latest_measurements()</code>. Це гарантує, що оператор ніколи не побачить порожнього екрана, навіть якщо сервіс датчиків було перезавантажено.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (TELEMETRY WRAPPER) -->
<div class="section-container">
    <div class="section-header":"06</span><h2 class="section-title">Псевдокод телеметрійної обгортки</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION live_telemetry_wrapper(active):
    IF NOT active: RETURN
    
    TRY:
        IF live_state_exists() AND is_fresh(< 15s):
            STATE = load_json("live_state.json")
            DF = map_to_analytics_format(STATE["substations"])
            INJECT_GLOBAL_METRICS(STATE["freq"], STATE["total_load"])
            RENDER tab_kpi(DF, filter=region)
        ELSE:
            DF = get_latest_measurements_from_db()
            IF DF IS EMPTY: SHOW "Waiting for Data"
            ELSE: RENDER tab_kpi(DF, filter=region)
    CATCH Error as e:
        LOG_ERROR(e)
        SHOW "Sensor Communication Error"
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: GLOBAL METRIC INJECTION (SESSION STATE) -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Ін'єкція глобальних метрик</h2></div>
    <div class="glass-card flow-step">
        <p>Окрім рендерингу карток, модуль оновлює глобальний <code>st.session_state</code> (наприклад, <code>live_total_mw</code> та <code>live_freq</code>). Це дозволяє іншим частинам системи (наприклад, анімаціям на карті) знати поточний стан мережі без повторних звернень до джерела даних.</p>
    </div>
</div>

<!-- SECTION 08: COSMETIC MONITORING & FRESHNESS CHECKS -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Косметичний моніторинг та перевірка свіжості</h2></div>
    <div class="glass-card flow-step">
        <p>Використання <code>mtime</code> (часу модифікації файлу) дозволяє системі миттєво відрізнити "активний потік" від "завислої симуляції". Якщо дані не оновлювалися більше 15 секунд, система вважає трансляцію офлайн і переходить у режим роботи з БД, що є критичним для достовірності моніторингу.</p>
    </div>
</div>

<!-- SECTION 09: SUBSTATION HEALTH SCORE CALCULATION -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Розрахунок індексу здоров'я об'єктів</h2></div>
    <div class="glass-card flow-step">
        <p>Живий стрім передає <code>health_score</code> для кожної підстанції. Модуль <code>live_kpi.py</code> агрегує ці дані, вираховуючи <code>live_avg_health</code> по всій системі. Це дозволяє диспетчеру бачити загальний тренд деградації мережі в реальному часі на головній панелі індикаторів.</p>
    </div>
</div>

<!-- SECTION 10: MEMORY HYGIENE IN RECURSIVE POLLING -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Гігієна пам'яті при рекурсивному опитуванні</h2></div>
    <div class="glass-card flow-step">
        <p>Для запобігання накопиченню сміття в пам'яті при частих оновленнях (кожні 5с), модуль використовує локальну область видимості для об'єктів DataFrame. Після кожного тіку фрагмента об'єкти автоматично видаляються, що забезпечує стабільну роботу додатка протягом багатьох годин без перезавантаження.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📟</div>
            <div class="role-content">
                <h4>KPI View</h4>
                <p>Низькорівневий компонент рендерингу карток та метрик.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📝</div>
            <div class="role-content">
                <h4>JSON State</h4>
                <p>Пряме джерело даних від сервісу симуляції датчиків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🗄️</div>
            <div class="role-content">
                <h4>DB Services</h4>
                <p>Забезпечує Fallback-логіку через <code>get_latest_measurements</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (WEBSOCKETS) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v3.0 (WebSockets)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується перехід на <b>WebSockets</b> для справжнього Real-time Push (замість 5с опитування), впровадження <b>звукових алярмів</b> при виході частоти за межі (49.8 - 50.2 Hz) та підтримка <b>багатокористувацької синхронізації KPI</b>.</p>
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
