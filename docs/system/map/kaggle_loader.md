# Технічна специфікація модуля: kaggle_loader.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATA INGESTION PIPELINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚚</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Kaggle Dataset Connector: kaggle_loader</h1>
            <p class="mega-subtitle">Автоматизований імпорт, стандартизація та оптимізація історичних наборів даних (напр. Kaggle PJM Energy Consumption) для аналітичного ядра.</p>
            <div class="status-tags"><span class="tag tag-online">PANDAS ETL</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">DATA NORMALIZER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Scan</span><span class="metric-value">Glob Directory Masking</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🗺️</div><div class="metric-info"><span class="metric-label">Mapping</span><span class="metric-value">Pretty-Name Translation</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Optimiz</span><span class="metric-value">Tail Truncation (5000 rows)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">Diet</span><span class="metric-value">Memory Diet Applier</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>kaggle_loader.py</b> — це міст між "диким" інтернетом і впорядкованою архітектурою Atlas. Його завдання — взяти сирі, різні за структурою файли відкритого датасету PJM Hourly Energy Consumption (Kaggle), і перетворити їх на ідеально чистий Pandas DataFrame, з яким можуть працювати наші графіки.</p>
        <p style="margin-top: 12px;">Головна інновація модуля — <b>Memory Diet (Радикальна оптимізація)</b>. Кожен з файлів Kaggle містить 100k+ рядків, і якщо завантажити всі файли, Streamlit впаде з нестачею оперативної пам'яті (MemoryError). Тому <code>kaggle_loader</code> застосовує <code>.tail(5000)</code> ще до об'єднання файлів, забираючи лише найсвіжіші дані, і додатково стискає типи колонок через <code>memory_diet()</code>.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def load_kaggle_data() → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Шукає всі файли за маскою <code>data/*_hourly.csv</code>. Для кожного знайденого файлу: 1. Визначає префікс (наприклад AEP, PJME). 2. Інтелектуально шукає колонку дати (datetime/timestamp) та конвертує її. 3. Шукає колонку навантаження (load_mw/AEP_MW). 4. Перекладає префікс у зручну назву через <code>KAGGLE_MAPPING</code>. 5. Видаляє биті рядки (<code>dropna</code>). 6. Сортує і бере останні 5000 рядків. В кінці виконує <code>pd.concat</code> всіх підготовлених фреймів та пропускає їх через <code>src.core.database.memory_diet</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">ETL Пайплайн Завантаження</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("load_kaggle_data()") --> GLOB("glob.glob('data/*_hourly.csv')")
    
    GLOB --> LOOP{"For each file:"}
    
    LOOP --> READ("pd.read_csv()")
    READ --> NAME("Extract Prefix\n(e.g., 'AEP')")
    
    NAME --> COLS("Identify Time & Load cols\nRename to Standard")
    COLS --> MAP("Translate 'AEP' to\n'Американська електрична...'")
    
    MAP --> DROP("dropna()")
    DROP --> TAIL("Sort Time -> .tail(5000)\nMemory Preservation!")
    
    TAIL --> APPEND("Append to all_dfs list")
    APPEND --> LOOP
    
    LOOP -->|All Done| CONCAT("pd.concat(all_dfs)")
    CONCAT --> DIET("memory_diet()\n(Downcast int64 to int32)")
    DIET --> OUT("Return Clean df")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>glob</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database (memory_diet)</span>
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
