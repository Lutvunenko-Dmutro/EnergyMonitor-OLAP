# Технічна специфікація модуля: forecast_plots.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ADVANCED VISUALIZATION ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Forecast Plots: forecast_plots</h1>
            <p class="mega-subtitle">Рушій візуалізації прогнозів машинного навчання. Створює гібридні графіки, що поєднують історичні дані, передбачення моделей та довірчі інтервали на єдиному таймлайні.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY BACKEND</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">ML VISUALIZATION</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Rendering</span><span class="metric-value">Plotly Go</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Precision</span><span class="metric-value">Multi-layer Hybrid</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Styling</span><span class="metric-value">Smart Dash Lines</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Bounds</span><span class="metric-value">Auto-clipped</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>forecast_plots.py</b> відповідає за те, як кінцевий користувач бачить результати передбачень нейромереж. На відміну від базових графіків, тут реалізована складна логіка "зшивання" двох різних часових рядів: факт (минуле) та прогноз (майбутнє).</p>
        <p style="margin-top: 12px;">Основна фіча: модуль автоматично генерує напівпрозорі "коридори" довірчих інтервалів (upper_bond/lower_bond) навколо лінії прогнозу, використовуючи SVG-заливку (<code>fill="toself"</code>). Він також керує колірним кодуванням різних версій моделей (V1, V2, V3) для візуального аудиту.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _generate_forecast_figure(df_hist: pd.DataFrame, df_fc: pd.DataFrame, title: str, version_lbl: str) → go.Figure</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Основний графік прогнозу. Малює суцільну лінію <code>df_hist</code> та пунктирну <code>df_fc</code>. Додає полігон (коридор похибки) використовуючи координати <code>timestamp + timestamp[::-1]</code> та значення <code>upper_bond + lower_bond[::-1]</code>. Включає автоматичне відсікання аномальних піків похибки (clip).</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def generate_comparison_plot(results: dict, substation_name: str) → go.Figure</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Створює графік для аудиту моделей на сторінці Backtest. На вхід приймає словник <code>{"v1": df, "v2": df, "v3": df}</code>. Малює "Ground Truth" помаранчевою лінією і накладає зверху прогнози різних версій з різним рівнем пунктиру (dot, dash, solid) для зручного візуального порівняння точності.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _generate_mega_hybrid_figure(df_bt: pd.DataFrame, df_fc: pd.DataFrame, title: str, version_lbl: str) → go.Figure</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Будує "Наскрізний таймлайн": одночасно показує результати бектесту (як модель відпрацювала вчора) та прогноз (що модель очікує завтра) на одному суцільному графіку. Використовує колір <code>#ee5253</code> для маркування зони впливу ML.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема побудови довірчого інтервалу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("df_hist (Actuals)\ndf_fc (Forecast + Bounds)") --> ADD_HIST("Add Trace: Actual Load\n(Solid Line, #3498db)")
    
    ADD_HIST --> CLIP("Calculate max values\nclip(upper=max*1.5)")
    
    CLIP --> CONCAT_X("Concat X:\ntimestamp + reversed(timestamp)")
    CONCAT_X --> CONCAT_Y("Concat Y:\nupper_bond + reversed(lower_bond)")
    
    CONCAT_Y --> POLYGON("Add Trace: Polygon\n(fill='toself', Red 8% Alpha)")
    
    POLYGON --> ADD_FC("Add Trace: Forecast\n(Dash Line, #e74c3c)")
    
    ADD_FC --> LAYOUT("update_layout:\nplotly_dark, x unified")
    LAYOUT --> OUT("Return Plotly Figure")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.graph_objects</span>
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
