# Технічна специфікація модуля: live_kpi.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">REAL-TIME TELEMETRY ORCHESTRATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📡</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Live Data Syncer: live_kpi</h1>
            <p class="mega-subtitle">Забезпечує миттєву візуалізацію стану енергосистеми через реактивне оновлення метрик. Читає JSON-стейт симулятора з нульовою затримкою (Zero Latency).</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT FRAGMENT</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">POLLING ENGINE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Polling</span><span class="metric-value">st.fragment (5s)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Transport</span><span class="metric-value">JSON State File Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Fallback</span><span class="metric-value">SQL Recovery</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Integration</span><span class="metric-value">Session State Global</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>live_kpi.py</b> відповідає за ефект "Живої Симуляції". Замість того, щоб перезавантажувати весь великий дашборд кожні кілька секунд, він використовує <code>@st.fragment(run_every=5)</code> — спеціальну фічу Streamlit, яка оновлює лише одну конкретну частину екрану.</p>
        <p style="margin-top: 12px;">Архітектурна знахідка цього модуля — читання даних безпосередньо з <code>live_state.json</code>. SQL бази даних можуть мати затримки кешу (latency) під час масових інсертів, але JSON-файл оновлюється симулятором (data_generator.py) миттєво. Модуль зчитує цей JSON, перетворює його на Pandas DataFrame, підганяє назви колонок, і віддає візуалізатору (<code>tab_kpi.render()</code>). Якщо JSON старий або зламаний — вмикається SQL Fallback.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@safe_fragment(run_every=5)<br>def live_telemetry_wrapper(active=False) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Циклічний оркестратор. 1. Блокується, якщо <code>active=False</code> або режим Kaggle. 2. Перевіряє вік файлу <code>live_state.json</code> через <code>st_mtime</code> (<15 сек). 3. Читає JSON та створює Pandas DataFrame <code>df_telemetry</code>. 4. Ренеймить колонки (temp -> temperature_c) для уніфікації з БД. 5. Записує глобальні метрики в <code>st.session_state</code> (<code>live_total_mw</code>, <code>live_freq</code>). 6. Викликає рендеринг KPI. 7. Fallback: якщо JSON немає — викликає <code>get_latest_measurements()</code> з БД.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Живої Синхронізації</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    LOOP("Auto-Run (every 5s)") --> IN("live_telemetry_wrapper()")
    
    IN --> CHK_MODE{"Kaggle Mode?"}
    CHK_MODE -->|Yes| OUT_WARN("Show Warning & Stop")
    
    CHK_MODE -->|No| CHK_JSON{"live_state.json exists\n& fresh (<15s)?"}
    
    CHK_JSON -->|Yes| READ_J("json.load(f)")
    READ_J --> DF("pd.DataFrame(state['substations'])")
    DF --> RENAME("Rename columns\n(load -> actual_load_mw)")
    
    RENAME --> S_STATE("Sync Globals\n(st.session_state['live_freq'] = freq)")
    
    CHK_JSON -->|No| FALLBACK("get_latest_measurements()\n[SQL Fallback]")
    
    S_STATE --> RENDER("tab_kpi.render(df, region_filter)")
    FALLBACK --> RENDER
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>json</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>time</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pathlib.Path</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.views.kpi (tab_kpi)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.services.data.db_services (get_latest_measurements - SQL fallback)</span>
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
