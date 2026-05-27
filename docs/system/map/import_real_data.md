# Технічна специфікація модуля: import_real_data.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">REAL-WORLD DATA INGESTION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📥</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">External Data Importer: import_real_data</h1>
            <p class="mega-subtitle">Сервіс інтеграції зовнішніх історичних датасетів (напр. Kaggle AEP_hourly.csv) в ізольовану таблицю системи для валідації ШІ-моделей.</p>
            <div class="status-tags"><span class="tag tag-online">PSYCOPG2 BATCH</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">ETL SCRIPT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Parser</span><span class="metric-value">Pandas CSV Read</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Cleanse</span><span class="metric-value">Sort & Deduplicate</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🏗️</div><div class="metric-info"><span class="metric-label">Schema</span><span class="metric-value">RealLoadMeasurements</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Ingest</span><span class="metric-value">execute_values (Fast)</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>import_real_data.py</b> потрібен для того, щоб тестувати прогнози не тільки на синтетиці, а й на "бойових" даних з реального світу (наприклад, з відкритого датасету AEP або PJM).</p>
        <p style="margin-top: 12px;">Скрипт читає важкий CSV-файл, стандартизує час, і заливає дані у спеціально виділену таблицю <code>RealLoadMeasurements</code>. Ця таблиця повністю ізольована від основної (синтетичної), що гарантує відсутність конфліктів у системі. Головна перевага — використання <code>execute_values</code> для миттєвої вставки десятків тисяч рядків та <code>ON CONFLICT DO NOTHING</code> для безпечних повторних запусків.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def import_real_data(csv_path: str = "AEP_hourly.csv") → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний скрипт (ETL). 1. Перевіряє наявність файлу. 2. Читає датасет через <code>pd.read_csv</code>. 3. Конвертує колонку "Datetime", сортує та видаляє дублікати (<code>drop_duplicates</code>). 4. Відкриває <code>psycopg2.connect</code>. 5. Створює таблицю <code>RealLoadMeasurements</code> з індексом. 6. Конвертує pandas-рядки у масив кортежів <code>itertuples</code>. 7. Виконує <code>execute_values</code> з опцією ігнорування конфліктів. 8. Здійснює <code>commit()</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Ізольованого Завантаження</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("import_real_data()") --> CHK{"File Exists?"}
    
    CHK -->|No| ERR("Print Error & Exit")
    CHK -->|Yes| READ("pd.read_csv(csv_path)")
    
    READ --> CLN("df['Datetime'] = to_datetime()\ndf.sort_values()\ndf.drop_duplicates()")
    
    CLN --> DB("psycopg2.connect(**DB_CONFIG)")
    
    DB --> SQL("CREATE TABLE IF NOT EXISTS\nRealLoadMeasurements")
    
    SQL --> TUPLES("data_tuples = list(df.itertuples())")
    
    TUPLES --> INSERT("execute_values(cursor, query,\ndata_tuples)")
    
    INSERT --> CONFLICT("ON CONFLICT (timestamp)\nDO NOTHING")
    
    CONFLICT --> DONE("conn.commit()")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>psycopg2</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>dotenv (load_dotenv)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>psycopg2.extras.execute_values</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.config (DB_CONFIG)</span>
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
