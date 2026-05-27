# Технічна специфікація модуля: diag_columns.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATABASE DIAGNOSTIC TOOL</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔍</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">DB Inspector: diag_columns</h1>
            <p class="mega-subtitle">Утиліта прямого доступу для діагностики схеми бази даних. Швидко зчитує метадані таблиці <code>LoadMeasurements</code> для перевірки наявності необхідних колонок.</p>
            <div class="status-tags"><span class="tag tag-online">CLI UTILITY</span><span class="tag tag-version">v1.0.0</span><span class="tag tag-role">DB DIAGNOSTICS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔌</div><div class="metric-info"><span class="metric-label">Driver</span><span class="metric-value">psycopg2</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Execution Time</span><span class="metric-value">< 100ms</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Safety</span><span class="metric-value">Read-Only (LIMIT 0)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🖥️</div><div class="metric-info"><span class="metric-label">Interface</span><span class="metric-value">CLI / Print</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>diag_columns.py</b> — це легковаговий діагностичний скрипт, створений для швидкої перевірки актуального стану схеми бази даних в оточеннях, де немає прямого доступу до <code>psql</code> або pgAdmin.</p>
        <p style="margin-top: 12px;">Основна фіча: він використовує оптимізований запит <code>SELECT * FROM LoadMeasurements LIMIT 0</code>, який миттєво повертає <b>лише структуру (метадані)</b> таблиці без завантаження самих даних у пам'ять. Це робить скрипт безпечним для запуску на продакшені в будь-який момент.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def check_columns() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Ініціалізує пряме psycopg2-підключення (минаючи шар ORM або пулу підключень), зчитує змінні оточення (DB_HOST, DB_USER, etc.), виконує LIMIT 0 запит та друкує список колонок у <code>stdout</code>. У разі помилки підключення логує її без падіння скрипта.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема роботи діагностики</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("python diag_columns.py") --> ENV("load_dotenv()\nRead DB credentials")
    ENV --> CONN("psycopg2.connect()")
    
    CONN -->|Success| QUERY("SELECT * FROM\nLoadMeasurements LIMIT 0")
    CONN -->|Failure| ERR("print(ERROR)")
    
    QUERY --> EXTRACT("Extract col names\nfrom cur.description")
    EXTRACT --> PRINT("print(COLUMNS: [...])")
    
    PRINT --> CLOSE("Close Cursor\nClose Connection")
    ERR --> DONE("Exit")
    CLOSE --> DONE
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>psycopg2</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>dotenv.load_dotenv</span>
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
