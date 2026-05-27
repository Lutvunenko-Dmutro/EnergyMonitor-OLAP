# Технічна специфікація модуля: finance.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">FINANCIAL & GRID ANALYTICS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">💰</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Financial Audit: finance</h1>
            <p class="mega-subtitle">Інтегрований модуль для моніторингу економічної ефективності (тарифні сітки, втрати) та фізичного стану мереж (ЛEП, AC/HVDC) в реальному часі.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY COMPLEX</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">BUSINESS METRICS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📉</div><div class="metric-info"><span class="metric-label">Economy</span><span class="metric-value">Cost Stacked Bars</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Grid</span><span class="metric-value">Line Load (AC/HVDC)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌡️</div><div class="metric-info"><span class="metric-label">Pricing</span><span class="metric-value">Volatility Heatmap</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚖️</div><div class="metric-info"><span class="metric-label">Losses</span><span class="metric-value">Non-linear Scatter</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>finance.py</b> генерує дашборд "Фінанси та Мережі". Він пов'язує фізику (мегавати, перетоки) з економікою (гроші, втрати).</p>
        <p style="margin-top: 12px;">Візуально поділений на два яруси (2x2 Grid). <b>Верхній ярус:</b> Стовпчикова діаграма агрегованої добової вартості електроенергії по регіонах та лінійний графік завантаженості ліній електропередач (з виділенням критичних зон >95%). <b>Нижній ярус:</b> Теплова карта (Heatmap) погодинної волатильності цін (для оптимізації) та точковий графік (Scatter) що демонструє фізику процесу: як нелінійно зростають технічні втрати при наближенні ліній до 100% завантаження.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render(df_fin: pd.DataFrame, df_lines: pd.DataFrame) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний метод рендерингу. Спочатку збагачує <code>df_lines</code> через <code>calculate_line_losses</code>. Потім створює колонку <code>day</code>. Розподіляє UI на 4 колонки (2 ряди x 2 стовпці). Розраховує <code>groupby.sum()</code> для вартості (px.bar), <code>groupby.mean()</code> з відкиданням неповних днів для ліній (px.line), генерує <code>pivot</code> таблицю для <code>go.Heatmap</code>, та будує <code>px.scatter</code> для втрат. Для лінійного графіка використовує <code>add_hrect</code> для замальовки зон ризику.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Аналітики</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render(df_fin, df_lines)") --> PHYS("calculate_line_losses(df_lines)")
    
    PHYS --> TIME("Extract 'day' from timestamps")
    TIME --> ROW1("Row 1 Columns")
    TIME --> ROW2("Row 2 Columns")
    
    ROW1 --> COST("Group By day, region\nSum(cost)\n[px.bar stack]")
    ROW1 --> GRID("Group By day, type\nMean(load), Filter count >= 20\n[px.line + add_hrect]")
    
    ROW2 --> HEAT("Pivot(day, hour, price)\n[go.Heatmap]")
    ROW2 --> LOSS("Scatter: load vs loss\n[px.scatter]")
    
    COST --> RENDER("safe_plotly_render()")
    GRID --> RENDER
    HEAT --> RENDER
    LOSS --> RENDER
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
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.physics (calculate_line_losses)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.ui_helpers (safe_plotly_render)</span>
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
