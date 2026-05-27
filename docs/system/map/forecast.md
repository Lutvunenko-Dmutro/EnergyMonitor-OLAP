# Технічна специфікація модуля: forecast.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AI FORECAST & BACKTEST CENTER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧠</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Intelligence Hub: forecast</h1>
            <p class="mega-subtitle">Головний інтерфейсний модуль для взаємодії з ML-моделями (V1-V3). Забезпечує управління реактивним інференц-двигуном, порівняльним аналізом та Historical Backtesting.</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT APP</span><span class="tag tag-version">v3.0.0</span><span class="tag tag-role">ORCHESTRATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Mode 1</span><span class="metric-value">Reactive Inference</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚖️</div><div class="metric-info"><span class="metric-label">Mode 2</span><span class="metric-value">Architecture Comparison</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Mode 3</span><span class="metric-value">Historical Backtest</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌍</div><div class="metric-info"><span class="metric-label">Scope</span><span class="metric-value">Single / Global Network</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>forecast.py</b> — це головний маршрутизатор (Orchestrator) найскладнішої вкладки "Прогнозування". Він не малює графіки напряму і не робить ML-обчислень. Його єдина мета — <b>керувати станами (State Management)</b>.</p>
        <p style="margin-top: 12px;">Залежно від того, що вибрав юзер (одна станція чи всі, одна модель чи порівняння, прогноз у майбутнє чи бектест минулого), модуль розбирає цей набір умов, зберігає прапорці в <code>st.session_state</code> (наприклад, <code>tab_active_mode</code>), викликає відповідний двигун (<code>run_reactive_forecast_engine</code> або <code>cached_fast_backtest</code>) та передає результат у компоненти відображення (Grid, Layouts, Audits). Також має захист від переривань через <code>engine_active</code>.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render(selected_substation="Усі підстанції", data_source="Live") → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Єдина точка входу. 1. Перевіряє "Interruption Monitor". 2. Нормалізує ввід (list vs string). 3. Рендерить Header. 4. Обробляє кнопки "Прогноз" та "Аудит". 5. В залежності від <code>tab_active_mode</code> викликає: <code>run_reactive_forecast_engine</code> (для майбутнього), <code>_render_comparative_audit</code> (для порівняння моделей), або <code>render_backtest_execution_loop</code> (для глобального аудиту). Розподіляє малювання графіків між <code>hero</code> компонентом та <code>grid</code> компонентами.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Диспетчеризація станів (State Machine)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("User Action") --> STATE("st.session_state\n[tab_active_mode]")
    
    STATE --> FORECAST["Mode: 'forecast'"]
    STATE --> AUDIT_COMP["Mode: 'comparison_audit'"]
    STATE --> AUDIT_GLOB["Mode: 'multi_audit_view'"]
    
    FORECAST --> FC_ENG("run_reactive_forecast_engine()")
    FC_ENG --> FC_SCOPE{"Scope?"}
    
    FC_SCOPE -->|Single| RENDER_S("render_single_forecast_results()")
    FC_SCOPE -->|Global| RENDER_G("render_substation_grid()")
    
    AUDIT_COMP --> AUD_C("_render_comparative_audit()")
    
    AUDIT_GLOB --> BT_LOOP("cached_fast_backtest()\nin a Loop + ProgressBar")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.ui_helpers (safe_plotly_render)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.views.forecast_components.* (header, engine, grid, audits, layouts)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.forecast_controller (get_cached_history, cached_fast_backtest)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.components.charts (_generate_*)</span>
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
