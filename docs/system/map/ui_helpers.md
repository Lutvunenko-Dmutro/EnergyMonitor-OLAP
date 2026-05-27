# Технічна специфікація модуля: ui_helpers.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">UI RESILIENCE & STYLING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🖼️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Chart Rendering Guard: ui_helpers</h1>
            <p class="mega-subtitle">Єдина точка рендерингу Plotly-графіків у системі. Уніфікована конфігурація панелі інструментів, видалення логотипу Plotly та Responsive режим.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY WRAPPER</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">UI GUARDRAIL</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🎛️</div><div class="metric-info"><span class="metric-label">Config</span><span class="metric-value">displayModeBar = True</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚫</div><div class="metric-info"><span class="metric-label">Branding</span><span class="metric-value">displaylogo = False</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔲</div><div class="metric-info"><span class="metric-label">Tools</span><span class="metric-value">Remove select2d / lasso2d</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📱</div><div class="metric-info"><span class="metric-label">Layout</span><span class="metric-value">responsive = True</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>ui_helpers.py</b> реалізує принцип DRY (Don't Repeat Yourself) для рендерингу. Без нього кожен модуль мав би самостійно передавати <code>config=...</code> до <code>st.plotly_chart()</code>, і в кожному місці можна було б написати трохи по-різному.</p>
        <p style="margin-top: 12px;">Функція <code>safe_plotly_render()</code> є єдиним місцем у системі, де <code>st.plotly_chart()</code> викликається напряму. Вона завжди передає стандартну конфігурацію: вмикає Toolbar (для zoom/pan), вимикає Scroll Zoom (бо на сторінці є прокрутка), приховує логотип Plotly (заради Cyber-HUD стилю). Крім того, вона приймає довільний <code>**kwargs</code> і прокидає <code>key=</code>, що дозволяє уникнути конфліктів ключів Streamlit при кількох графіках на одній сторінці.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def safe_plotly_render(fig, container=st, **kwargs) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Уніфікований рендерер графіків. Визначає стандартний <code>config</code> dict з налаштуваннями ModeBar. Викликає <code>container.plotly_chart(fig, config=config, key=kwargs.get("key"))</code>. Параметр <code>container</code> дозволяє рендерити в довільний Streamlit-контейнер (st, st.sidebar, col).</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Уніфікований Рендеринг Plotly</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph LR
    CALLER("Any Module\n(map.py, plots.py, etc.)") --> CALL("safe_plotly_render(fig)")

    CALL --> CFG("config = {\n  displayModeBar: True\n  scrollZoom: False\n  displaylogo: False\n  modeBarButtonsToRemove:\n  ['select2d','lasso2d']\n  responsive: True\n}")

    CFG --> RENDER("container.plotly_chart(\n  fig,\n  config=config,\n  key=kwargs.get('key')\n)")

    RENDER --> UI("🖥️ Streamlit UI")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
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
