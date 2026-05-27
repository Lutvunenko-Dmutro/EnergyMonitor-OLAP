# Технічна специфікація модуля: loader.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">REAL-TIME DATA LOADER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📦</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">ETL Stream Handler: loader</h1>
            <p class="mega-subtitle">Центральний вузол управління життєвим циклом даних: поетапна ініціалізація, дворівневе кешування, та Lazy Loading історичних наборів.</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT CACHE</span><span class="tag tag-version">v2.3.0</span><span class="tag tag-role">BOOT ORCHESTRATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🏗️</div><div class="metric-info"><span class="metric-label">Boot</span><span class="metric-value">Granular Step Sequencer</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Cache</span><span class="metric-value">st.cache_data (TTL=1800s)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🦥</div><div class="metric-info"><span class="metric-label">Lazy</span><span class="metric-value">Kaggle Data On-Demand</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Errors</span><span class="metric-value">Robust DB Fallbacks</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>loader.py</b> управляє "завантажувальним екраном" та пам'яттю системи. Він гарантує, що при підключенні до бази даних (яка може бути на віддаленому сервері) UI не зависне без інформації.</p>
        <p style="margin-top: 12px;">Його серцем є <b>Active Boot Sequencing</b> — система розділення великого завантаження на 7 дрібних кроків (Load, Gen, Fin, Alerts, Lines, Telemetry). Це дає можливість відображати плавний прогрес-бар з кіберпанк-повідомленнями. Модуль також реалізує <i>Lazy Loading</i> для Kaggle-датасетів: історичні дані (Kaggle) не завантажуються під час старту, економлячи ~100 МБ пам'яті, і підтягуються лише тоді, коли користувач перемикає "Джерело даних".</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def fetch_granular_data(step_key: str) → Dict[str, pd.DataFrame]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Ізольований обробник запитів з <code>@robust_database_handler</code>. Валідує ключ, ловить Network, Timeout та Memory Errors. Якщо база відпала на конкретному запиті, повертає порожній dict, дозволяючи системі продовжити бутстрап з іншими модулями.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_active_boot_data_generator() → Generator</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Генератор (yield). Містить кортежі кроків <code>(message, progress_pct, key)</code>. На кожному кроці викликає <code>fetch_granular_data</code> та оновлює глобальний <code>final_data</code> dict. Повертає повідомлення для UI прогрес-бару.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_verified_data() → dict</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний оркестратор даних. Перевіряє режим Kaggle. Якщо Live — читає кешовану версію (<code>fetch_database_data</code>). Має потужний Fallback: якщо БД порожня (None), показує кнопку <b>"Згенерувати тестові дані"</b> (викликає seeder).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Життєвий Цикл Boot Orchestration</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("get_verified_data()") --> CHK_SRC{"is_kaggle?"}
    
    CHK_SRC -->|Yes| KAGGLE("Return st.session_state['active_data']")
    CHK_SRC -->|No| FETCH_DB("fetch_database_data()\n[st.cache_data]")
    
    FETCH_DB --> GEN("get_active_boot_data_generator()")
    GEN --> LOOP{"Yield Step"}
    
    LOOP -->|Next Step| FETCH_SQL("fetch_granular_data(step_key)")
    FETCH_SQL -.->|Exception Handled| FALLBACK("Log Error\nReturn {}")
    FETCH_SQL --> UPDATE("final_data.update(chunk)\ngc.collect()")
    UPDATE --> LOOP
    
    LOOP -->|Finished| CACHE("Return Aggregated Dict to Cache")
    CACHE --> VERIFY{"Is df.empty?"}
    
    VERIFY -->|Yes| BTN("st.warning + Button(Generate Data)\n-> db_seeder.generate_professional_data()")
    VERIFY -->|No| DONE("Return Verified Data to UI")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>gc</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>time</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database (run_query)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.queries (QUERY_*)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.services.data.db_services (get_latest_measurements)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.error_handlers (robust_database_handler, ErrorContext)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.services.data.db_seeder (generate_professional_data - lazy loaded)</span>
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
