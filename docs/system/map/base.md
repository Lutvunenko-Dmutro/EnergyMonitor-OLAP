# Технічна специфікація модуля: base.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CORE VISUALIZATION ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">UI Charts: base</h1>
            <p class="mega-subtitle">Фундаментальний графічний рушій системи. Реалізує базові аналітичні діаграми: порівняльні Dual-Axis графіки та профілі ритмічності споживання.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY BACKEND</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">UI COMPONENT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Backend</span><span class="metric-value">Plotly (Graph Objects)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌗</div><div class="metric-info"><span class="metric-label">Theme Mode</span><span class="metric-value">plotly_dark</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Interactivity</span><span class="metric-value">x unified hover</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛠️</div><div class="metric-info"><span class="metric-label">Data Format</span><span class="metric-value">Pandas DataFrame</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>base.py</b> є основою для всіх складніших візуалізацій в системі. Він надає універсальні функції-генератори Plotly-графіків, які використовуються на різних сторінках дашборду для відображення як сирих телеметричних даних, так і результатів машинного навчання.</p>
        <p style="margin-top: 12px;">Основні архітектурні принципи: <b>Dry (Don't Repeat Yourself)</b> у конфігураціях графіків (єдині відступи, легенди, темна тема), автоматичне відстеження режиму відображення однієї або декількох підстанцій, та використання Alpha-blending (прозорості) для заповнення областей під кривими.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_dual_axis_chart(df: pd.DataFrame, left_col: str, left_label: str, left_color: str, right_col: str, right_label: str, right_color: str, fill_left: bool = True) → go.Figure</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Генерує графік з двома осями Y (наприклад, Навантаження зліва, Температура справа). Автоматично обробляє випадок, коли в <code>df</code> присутні дані для кількох підстанцій (column: <code>substation</code>) — у такому випадку відключає <code>fill</code> для збереження читабельності та додає назви підстанцій в легенду.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_rhythm_chart(df_rhythm: pd.DataFrame) → go.Figure</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Аналізує ритмічність: порівнює середнє навантаження за кожну годину (0-23) для Понеділка (<code>dow=1</code>) та Суботи (<code>dow=6</code>). Використовується для виявлення структурних зсувів у споживанні електроенергії в залежності від дня тижня.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _hex_to_rgb(hex_color: str) → str</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Внутрішня утиліта. Конвертує HEX колір (напр. <code>#f97316</code>) у формат <code>r,g,b</code> для використання в RGBA стилях Plotly (наприклад, для напівпрозорого заповнення <code>fillcolor</code>).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема Dual-Axis Rendering</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN(DataFrame: df\nleft_col, right_col) --> INIT("make_subplots(secondary_y=True)")
    INIT --> CHECK_MULTI{"substation\ncolumn exists\n& unique > 1?"}
    
    CHECK_MULTI -->|Yes| LOOP("For each substation")
    LOOP --> TRACE_M1("Add Scatter(left_col)\nfill='none'")
    TRACE_M1 --> TRACE_M2("Add Scatter(right_col)\ndash='solid'")
    TRACE_M2 --> LOOP
    
    CHECK_MULTI -->|No| TRACE_S1("Add Scatter(left_col)\nfill='tozeroy' w/ alpha")
    TRACE_S1 --> TRACE_S2("Add Scatter(right_col)\ndash='dot'")
    
    LOOP --> LAYOUT("update_layout:\ndark theme, bottom legend\nhovermode='x unified'")
    TRACE_S2 --> LAYOUT
    
    LAYOUT --> OUT("Return Plotly go.Figure")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.express</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.graph_objects</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.subplots.make_subplots</span>
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
