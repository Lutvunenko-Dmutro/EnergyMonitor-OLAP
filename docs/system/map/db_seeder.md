# Технічна специфікація модуля: db_seeder.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATA SYNTHESIS CORE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🌱</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">ETL & Seed Engine: db_seeder</h1>
            <p class="mega-subtitle">Повноцикловий конвеєр розгортання та інтелектуального наповнення бази даних реалістичними часовими рядами (фізична симуляція навантажень, погоди, зносу).</p>
            <div class="status-tags"><span class="tag tag-online">POSTGRES BATCH</span><span class="tag tag-version">v3.1.0</span><span class="tag tag-role">PIPELINE AUTODEPLOY</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🏗️</div><div class="metric-info"><span class="metric-label">Init</span><span class="metric-value">Schema Auto-Deployment</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧬</div><div class="metric-info"><span class="metric-label">Engine</span><span class="metric-value">Physics Simulation</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Ingestion</span><span class="metric-value">execute_values (Batch)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Hygiene</span><span class="metric-value">Truncate Cascade</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>db_seeder.py</b> — це інструмент "холодного старту" системи. Якщо база даних порожня, він автоматично створює всі таблиці (через SQL-скрипти з папки <code>/sql</code>) і наповнює їх базовими об'єктами (підстанції, генератори).</p>
        <p style="margin-top: 12px;">Основна його магія — генерація історичних даних (Simulation). Він ітерується по кожній годині в заданому проміжку (<code>START_DATE</code> -> <code>END_DATE</code>), вираховує погоду, стан трансформаторів (H2, Temp), та рівень споживання на основі профілів (Residential, Commercial, Industrial). Після цього записує мільйони рядків у Postgres "пачками" через високошвидкісний метод <code>psycopg2.extras.execute_values</code>.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def generate_professional_data() → tuple</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний оркестратор конвеєра. Викликається вручну або зі скрипта запуску. Керує підключенням до БД (<code>get_db_cursor</code>) та послідовно викликає етапи: перевірка схеми (<code>_ensure_schema</code>), завантаження довідників, симуляція (<code>_simulate_timeseries</code>) та пакетний запис (<code>_batch_insert</code>). Повертає профілі підстанцій та початкові температури для подальшого live-режиму.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _simulate_timeseries(...) → tuple</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Ядро симуляції. Генерує <code>pd.date_range</code>. Для кожної позначки часу обчислює погоду, ціни, навантаження підстанцій, стан зносу (H2, Temperature) та генерує алерти. Робота виконується в пам'яті (створюються масиви кортежів) для максимальної швидкості перед записом.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема генерації даних</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("generate_professional_data()") --> SCHEMA{"Schema Exists?"}
    
    SCHEMA -->|No| INIT("Execute:\n01_create_schema.sql\n02_insert_static_data.sql")
    SCHEMA -->|Yes| TRUNC("TRUNCATE ... CASCADE")
    
    INIT --> LOAD_STATIC("_load_static_data()")
    TRUNC --> LOAD_STATIC
    
    LOAD_STATIC --> SIMULATE("_simulate_timeseries()")
    
    SIMULATE --> LOOP{"For every Hour in\nDate Range"}
    
    LOOP --> PHYS_W("calculate_weather()")
    LOOP --> PHYS_L("calculate_substation_load()")
    LOOP --> PHYS_H("calculate_transformer_health()")
    
    PHYS_H --> LISTS("Append to In-Memory Lists")
    LISTS --> LOOP
    
    LOOP -->|Done| BATCH("_batch_insert()")
    BATCH --> PG("execute_values()\nHigh-Speed Bulk Insert")
    PG --> END_SUCCESS("Return State for Live Mode")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>psycopg2.extras.execute_values</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database (execute_sql_file, get_db_cursor)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.physics (calculate_*)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.config (END_DATE, START_DATE, FREQ)</span>
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
