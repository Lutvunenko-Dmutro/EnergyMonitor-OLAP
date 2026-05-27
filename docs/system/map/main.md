# Технічна специфікація модуля: main.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">STRATEGIC ORCHESTRATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚀</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Command & Control Center: main</h1>
            <p class="mega-subtitle">Високорівнева оркестрація життєвого циклу системи. Управління потоками даних, конфігурація середовища, та ініціалізація HUD-інтерфейсу.</p>
            <div class="status-tags"><span class="tag tag-online">DEFENSE EDITION</span><span class="tag tag-version">v5.0.0</span><span class="tag tag-role">ENTRY POINT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Watchdog</span><span class="metric-value">RAM Garbage Collection</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Threading</span><span class="metric-value">Single-thread Math (Cloud-Safe)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧬</div><div class="metric-info"><span class="metric-label">Data</span><span class="metric-value">Hybrid (Live/Kaggle)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Execution</span><span class="metric-value">Main Event Loop</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>main.py</b> — це єдина точка входу до всього додатку ATLAS. Його ключове завдання — не малювати графіки чи діставати дані з бази, а <i>оркеструвати</i> ці процеси, створюючи стабільне операційне середовище.</p>
        <p style="margin-top: 12px;">У "Defense Edition" модуль бере на себе обов'язки "Watchdog Sentinel": при старті він примусово обмежує кількість потоків для важких математичних бібліотек (NumPy, OpenBLAS) до 1, що критично запобігає крашам через OOM (Out Of Memory) у хмарних контейнерах Streamlit. Також він динамічно керує гібридною стратегією даних, перемикаючись між локальною симуляцією та великими архівами Kaggle.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def system_startup() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Процедура Bootstrapping. Запускається до основного циклу. Відповідає за виклик менеджера кешу (<code>startup_cache_cleanup(ttl_hours=24)</code>) для видалення застарілих тимчасових файлів, щоб запобігти розростанню дискового простору.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def main() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний Event Loop додатку Streamlit. Виконує строгу послідовність: 1) <code>init_page_config()</code>, 2) запуск <code>auto_gc(380MB)</code>, 3) ін'єкція CSS, 4) рендеринг Splash-екрану (одноразово), 5) завантаження даних, 6) рендеринг Sidebar, 7) рендеринг Dashboard.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Архітектура життєвого циклу (Lifecycle)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("streamlit run main.py") --> OS_ENV("os.environ.update\n(Limit Math Threads = 1)")
    
    OS_ENV --> SYS_START("system_startup()\n[Clear old cache]")
    SYS_START --> MAIN("main()")
    
    MAIN --> PG_CONF("init_page_config()\nauto_gc(380MB)\napply_custom_css()")
    
    PG_CONF --> SESSION{"st.session_state\n'booted'?"}
    SESSION -->|No| SPLASH("show_boot_sequence()\nLoad initial data")
    SESSION -->|Yes| LOAD("get_verified_data()\nfrom cache/DB")
    
    SPLASH --> HYBRID
    LOAD --> HYBRID
    
    HYBRID{"active_source\n== 'Kaggle'?"}
    HYBRID -->|Yes| KAGGLE("load_kaggle_lazy()")
    HYBRID -->|No| LIVE("Use Local DB/Sim")
    
    KAGGLE --> UI
    LIVE --> UI
    
    UI("render_sidebar()\nrender_dashboard_ui()")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.logging_config</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database.loader</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.components.styles</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.segments.dashboard</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.segments.sidebar</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.segments.splash</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.memory_helper</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os, sys, logging, warnings</span>
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
