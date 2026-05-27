# Технічна специфікація модуля: grid.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">GRID FORECAST VISUALIZER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔲</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Batch Renderer: grid</h1>
            <p class="mega-subtitle">Забезпечує пакетний рендеринг прогнозів для декількох об'єктів одночасно у вигляді динамічної 2-колонкової сітки з підтримкою мульті-моделей.</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT LAYOUT</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">VIEW COMPONENT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📐</div><div class="metric-info"><span class="metric-label">Layout</span><span class="metric-value">2-Column Responsive</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">Models</span><span class="metric-value">Single OR Multi (V1-V3)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Legend</span><span class="metric-value">Smart Hiding (Space)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Inference</span><span class="metric-value">Iterative Cached Calls</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Коли користувач вибирає в меню "Усі підстанції" і натискає "Прогноз", система має показати 10 різних графіків. <b>grid.py</b> відповідає за те, щоб ці графіки не йшли однією довгою "простирадлою" вниз, а акуратно розставлялись по 2 в ряд.</p>
        <p style="margin-top: 12px;">Модуль ітерується по списку станцій. Якщо увімкнено <code>is_multi_model</code>, він для кожної станції тричі викликає ШІ (V1, V2, V3) і будує мульти-графік. Щоб не захаращувати екран, він використовує <code>showlegend=(i == 0)</code>: легенда (опис кольорів) показується лише на найпершому графіку в сітці, а на інших — приховується.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_substation_grid(stations: list, src_type: str, version: str, scenario: dict, is_multi_model: bool) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний рендерер. Створює <code>g_cols = st.columns(2)</code>. Запускає цикл <code>enumerate(stations)</code>. За допомогою <code>with g_cols[i % 2]:</code> розкидає віджети. Якщо <code>is_multi_model</code>, збирає словник <code>multi_s</code> результатів V1-V3 і викликає <code>_generate_multi_forecast_figure</code>. Якщо сингл-модель — викликає <code>_generate_forecast_figure</code>. Використовує унікальні ключі (key) для рендеру через <code>safe_plotly_render</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Матричний Рендеринг</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render_substation_grid(stations)") --> COLS("g_cols = st.columns(2)")
    
    COLS --> LOOP("For i, station in enumerate(stations)")
    LOOP --> ASSIGN("with g_cols[i % 2]:")
    
    ASSIGN --> MODE{"is_multi_model?"}
    
    MODE -->|Yes| MULTI("For v in [v1,v2,v3]:\n_cached_ai_forecast()\nCollect to dict")
    MULTI --> MULTI_FIG("_generate_multi_forecast_figure()")
    MULTI_FIG --> LEGEND("update_layout(showlegend=(i==0))")
    
    MODE -->|No| SINGLE("_cached_ai_forecast(version)")
    SINGLE --> SINGLE_FIG("_generate_forecast_figure()")
    
    LEGEND --> RENDER("safe_plotly_render()")
    SINGLE_FIG --> RENDER
    
    RENDER --> LOOP
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.ui_helpers (safe_plotly_render)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.forecast_controller (cached_ai_forecast, get_cached_history)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.components.charts (_generate_forecast_figure, _generate_multi_forecast_figure)</span>
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
