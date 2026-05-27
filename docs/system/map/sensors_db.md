# Технічна специфікація модуля: sensors_db.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DIGITAL TWIN REAL-TIME ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📡</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Telemetry Emulator: sensors_db</h1>
            <p class="mega-subtitle">Фоновий процес (Subprocess) для симуляції потокової телеметрії. Singleton-захист PID-lock. Передача через JSON-буфер без запису в БД.</p>
            <div class="status-tags"><span class="tag tag-online">SUBPROCESS</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">COSMETIC MODE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔒</div><div class="metric-info"><span class="metric-label">Singleton</span><span class="metric-value">PID Lock File</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Transport</span><span class="metric-value">JSON Buffer (No DB)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💓</div><div class="metric-info"><span class="metric-label">Heartbeat</span><span class="metric-value">Auto-shutdown 15min</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧮</div><div class="metric-info"><span class="metric-label">Physics</span><span class="metric-value">calculate_substation_load</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>sensors_db.py</b> — це "Серце Цифрового Двійника". На відміну від <code>sensors.py</code> (який є лише класом-моделлю), цей модуль запускається як <b>окремий фоновий процес</b> та безперервно генерує показники для всіх підстанцій в БД кожні 5 секунд.</p>
        <p style="margin-top: 12px;">Ключовий архітектурний вибір — режим <b>"Cosmetic Mode"</b>: дані не записуються в SQL-базу даних (щоб не перевантажувати її рядами нових інсертів), а зберігаються лише у швидкому JSON-файлі <code>live_state.json</code>. Цей файл щосекунди читає <code>live_kpi.py</code>. Захист від подвійного запуску — PID Lock File (<code>sensors.lock</code>), який видаляється після зупинки. Автоматичне вимкнення через 15 хв (Heartbeat timeout) для економії ресурсів хмари.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def run_cosmetic_collector() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний цикл. 1. Перевіряє <code>sensors.lock</code> (Singleton Guard). 2. Записує власний PID у lock-файл. 3. Підключається до БД та завантажує список підстанцій (один раз). 4. Запускає нескінченний цикл: для кожної підстанції викликає <code>calculate_substation_load()</code> та <code>calculate_transformer_health()</code>. 5. Серіалізує стан у JSON. 6. Перевіряє Heartbeat кожного циклу. При виході — видаляє lock і JSON.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Lifecycle Фонового Процесу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("python -m src.services.sensors_db") --> CHK_LOCK{"sensors.lock\nexists?"}
    CHK_LOCK -->|Yes| EXIT("sys.exit(0)\nSingleton Guard")
    CHK_LOCK -->|No| LOCK_W("Write PID to sensors.lock")
    LOCK_W --> DB_CONN("psycopg2.connect(DB_CONFIG)")
    DB_CONN --> INIT("Load Substations list\nInit prev_health, profiles")
    INIT --> LOOP("While True (every 5s):")
    LOOP --> CALC("calculate_substation_load()\ncalculate_transformer_health()")
    CALC --> JSON_W("json.dump(live_state)\n→ live_state.json")
    JSON_W --> HB{"heartbeat.txt\nstale > 900s?"}
    HB -->|Yes| STOP("Break loop\nAuto-shutdown")
    HB -->|No| SLEEP("time.sleep(5)")
    SLEEP --> LOOP
    STOP --> CLEAN("Delete lock + json\nClose DB conn")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>json, time, os, sys, random, logging</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pathlib.Path</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>numpy</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>psycopg2</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>dotenv (load_dotenv)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.config (DB_CONFIG)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.physics (calculate_substation_load, calculate_transformer_health)</span>
        </div>
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
