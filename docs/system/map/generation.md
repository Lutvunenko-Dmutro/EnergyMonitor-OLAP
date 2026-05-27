# Технічна специфікація модуля: generation.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">GENERATION MIX MONITOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏭</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">UI Component: Generation View</h1>
            <p class="mega-subtitle">Візуалізаційний UI-компонент (Streamlit). Забезпечує інтерактивний аналіз структури генерації, потоків потужності між джерелами та регіонами, а також динаміки Energy Mix.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY COMPONENT</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">UI VIEW</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🌊</div><div class="metric-info"><span class="metric-label">Flows</span><span class="metric-value">Sankey Diagram</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🍰</div><div class="metric-info"><span class="metric-label">Mix</span><span class="metric-value">Donut Chart</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Dynamics</span><span class="metric-value">Stacked Area Chart</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Theming</span><span class="metric-value">MASTER_COLORS Sync</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>generation.py</b> відповідає за відображення вкладки "Структура генерації" в основному UI. Його головна мета — дати користувачу розуміння, <i>звідки</i> береться електроенергія та <i>куди</i> вона йде.</p>
        <p style="margin-top: 12px;">Архітектурна особливість модуля — використання єдиної колірної палітри (<code>MASTER_COLORS</code>) для всіх типів генерації (Nuclear=Жовтий, Thermal=Фіолетовий і т.д.), що забезпечує візуальну консистентність між Sankey, Pie та Area графіками. Якщо даних немає (не включена симуляція), модуль граціозно відображає заглушку.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render(df_gen: pd.DataFrame) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний метод рендерингу вкладки. Приймає DataFrame з даними про генерацію. Спочатку перевіряє датафрейм на порожнечу. Якщо дані є, генерує 3 Plotly графіки: <br>1. <code>go.Sankey</code> (потоки від типу генератора до регіону)<br>2. <code>px.pie</code> (загальна частка генерації)<br>3. <code>go.Scatter(stackgroup='one')</code> (динаміка потужності у часі).</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def hex_to_rgba(h: str, alpha: float) → str</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Внутрішня утиліта (defined inside render). Конвертує HEX-кольори з <code>MASTER_COLORS</code> у RGBA-формат, необхідний для коректного відображення напівпрозорих зв'язків у Sankey та заливки в Area Chart.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн рендерингу (UI Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render(df_gen)") --> CHECK{df_gen.empty?}
    CHECK -->|Yes| WARN("st.warning('No Data')\nst.info('Run Live Sim')")
    
    CHECK -->|No| RENDER_SANKEY("Build Sankey Diagram\nGroup by Generator -> Region")
    RENDER_SANKEY --> SYNC_COLOR("Map MASTER_COLORS\nConvert to RGBA")
    
    SYNC_COLOR --> COLS("Split layout: st.columns([1, 2])")
    
    COLS -->|Col 1 (1/3)| RENDER_PIE("Build Pie Chart\nTotal Energy Mix")
    COLS -->|Col 2 (2/3)| RENDER_AREA("Build Stacked Area\nTime Series by Source")
    
    RENDER_PIE --> SAFE_RENDER1("safe_plotly_render()")
    RENDER_AREA --> SAFE_RENDER2("safe_plotly_render()")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.express</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.graph_objects</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.ui_helpers.safe_plotly_render</span>
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
