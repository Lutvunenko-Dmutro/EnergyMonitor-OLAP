# Технічна специфікація модуля: audits.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">FORECAST COMPARATIVE AUDITS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚖️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Model Diagnostics: audits</h1>
            <p class="mega-subtitle">Підсистема глибинного аналізу точності різних поколінь нейромережевих моделей (LSTM V1, V2, V3). Забезпечує порівняльну діагностику архітектур та розрахунок метрик ефективності.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY UI</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">DIAGNOSTICS PANEL</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Evaluation</span><span class="metric-value">V1 vs V2 vs V3</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Metrics</span><span class="metric-value">RMSE, MAE, R², MAPE</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Visualization</span><span class="metric-value">Multi-Trace Plotly</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Academic</span><span class="metric-value">Distributions & Scatter</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>audits.py</b> працює в межах вкладки "Прогнозування" та відповідає за відображення результатів <i>порівняльного тестування (Backtesting)</i>. Він дозволяє аналітику наочно побачити різницю між базовою моделлю та покращеною архітектурою, яка враховує погодні умови.</p>
        <p style="margin-top: 12px;">Основна задача — викликати функції швидкого бектестингу (через <code>cached_fast_backtest</code>) для кожної доступної версії моделі, зібрати метрики, та відрендерити комплексний UI: графік порівняння, академічні графіки розподілу похибок, та зведену таблицю метрик.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _render_comparative_audit(substation_name: str, source_type: str) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний UI-контролер. В залежності від <code>source_type</code> (Live/CSV) та перемикача в session_state, тестує 1 або 3 моделі. Рендерить 3 вкладки: 1) "Порівняння" (загальний графік), 2) "Діагностика" (гістограми та розсіювання помилок через модуль `academic.py`), 3) "Метрики" (таблиця з підсвіткою кращого R²).</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _render_group_comparison(stations_list: list, source_type: str, version: str) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Рендерить єдиний лінійний Plotly-графік (go.Figure), на якому суміщені історичні дані навантаження відразу для декількох підстанцій (дозволяє диспетчеру порівняти піки споживання в різних вузлах).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Логіка побудови аудиту</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI("User selects 'Compare Models'") --> AUDIT("_render_comparative_audit()")
    
    AUDIT --> LOOP{"For version in\n[v1, v2, v3]"}
    
    LOOP --> BT("cached_fast_backtest(v)")
    BT --> METRICS["Extract: RMSE, MAE, R², df_bt"]
    METRICS --> COL["Append to res_dict & mlist"]
    COL --> LOOP
    
    LOOP -->|All Done| TABS("st.tabs: 📈 | 📊 | 📋")
    
    TABS --> TAB1("Tab 1:\ngenerate_comparison_plot()")
    TABS --> TAB2("Tab 2:\ngenerate_academic_plots()")
    TABS --> TAB3("Tab 3:\npd.DataFrame(mlist).style...")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.graph_objects</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.forecast_controller</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.ui_helpers</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.components.charts.academic (Inline)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.views.forecast_components.engine (Inline)</span>
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
