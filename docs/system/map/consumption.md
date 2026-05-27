# Технічна специфікація модуля: consumption.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CONSUMPTION ANALYTICS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Analytics Engine: consumption</h1>
            <p class="mega-subtitle">Детальна візуалізація та статистичний аналіз навантаження мережі. Підтримує нормалізацію (МВт vs %), фасетні графіки (Facet Grid) та регресійний аналіз погоди.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY EXPRESS</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">DASHBOARD VIEW</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📉</div><div class="metric-info"><span class="metric-label">Dynamics</span><span class="metric-value">px.line (Time Series)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚖️</div><div class="metric-info"><span class="metric-label">Mode</span><span class="metric-value">Absolute / Relative</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📦</div><div class="metric-info"><span class="metric-label">Seasonality</span><span class="metric-value">Hourly Boxplots</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌡️</div><div class="metric-info"><span class="metric-label">Correlation</span><span class="metric-value">OLS Trendlines</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>consumption.py</b> генерує основну аналітичну вкладку "Споживання". Його головне завдання — розкрити дані під різними кутами.</p>
        <p style="margin-top: 12px;">Оператор може подивитись на звичайний лінійний графік, увімкнути "Відносні показники" (щоб порівняти великі і малі підстанції в межах 0-100%), розбити загальний графік на окрему сітку для кожного об'єкта (Facet Grid), або включити логарифмічну шкалу (Log-Y). Нижче будуються статистичні діаграми розмаху (Boxplots) для аналізу поведінки в робочі/вихідні дні та точкові графіки залежності від температури (Scatter+OLS).</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render(df_load: pd.DataFrame, group_by_col: str) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний та єдиний метод-контролер UI. Приймає датафрейм історії навантажень. Формує <code>st.popover</code> з toggles (Відносні %, Логарифмічна шкала, Сітка). Викликає <code>aggregate_consumption</code> та <code>add_relative_load</code> (з <code>src.core.analytics.aggregator</code>). Будує три Plotly-діаграми: 1) Лінійну динаміку, 2) Boxplot розподілу по годинах, 3) Scatter-регресію по температурі. Обробляє Edge-кейси порожніх датафреймів (виводить UX-підказки).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Аналізу Споживання</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render(df_load, group_by)") --> CHECK{"Is df Empty?"}
    CHECK -->|Yes| WARN("st.warning + st.info\n[Guide User to Calendar]")
    
    CHECK -->|No| RESAMPLE("aggregate_consumption()\nResample to Hours")
    RESAMPLE --> REL{"Toggle:\nRelative %?"}
    
    REL -->|Yes| CALC_REL("add_relative_load()\ny_col = 'relative_load'")
    REL -->|No| CALC_ABS("y_col = 'actual_load_mw'")
    
    CALC_REL --> PLOT1("px.line(..., facet_col=...)")
    CALC_ABS --> PLOT1
    
    PLOT1 --> PEAK("Annotate Max Value (🔥)")
    
    PEAK --> PLOT2("px.box(x='hour', color='day_type')")
    PLOT2 --> PLOT3("px.scatter(x='temperature', trendline='ols')")
    
    PLOT3 --> DONE("safe_plotly_render()")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.express</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.ui_helpers (safe_plotly_render)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.analytics.aggregator (add_relative_load, aggregate_consumption)</span>
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
