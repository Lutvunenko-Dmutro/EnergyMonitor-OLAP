# Технічна специфікація модуля: __init__.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">UI COMPONENTS LIBRARY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">💠</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">components (Shared UI)</h1>
            <p class="mega-subtitle">Бібліотека спільних UI-компонентів. Забезпечує візуальну консистентність (Design System) та швидку збірку нових екранів.</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON PACKAGE</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">DESIGN SYSTEM</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🃏</div><div class="metric-info"><span class="metric-label">Cards</span><span class="metric-value">Metrics & Alerts</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Charts</span><span class="metric-value">Plotly Engines</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Styles</span><span class="metric-value">CSS & Neon Glow</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <b>components</b> містить низькорівневі "цеглинки" (Widgets) для побудови інтерфейсу. Замість того, щоб кожна сторінка (View) сама малювала свої графіки або картки з нуля, вона звертається до цього пакету.</p>
        <p style="margin-top: 12px;">Це гарантує, що графік трендів завжди виглядає однаково на будь-якій сторінці додатку. Також тут зосереджене управління CSS-ін'єкціями (Glassmorphism), що створюють унікальну естетику.</p>
    </div>
</div>

<!-- SECTION 02: CATEGORIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Категорії Елементів</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>cards</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Стилізовані HUD-контейнери для `st.metric`.</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>charts</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Фабрика графіків Plotly (Trend, Heatmaps, Hybrid Forecast).</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>styles.py</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Централізована система CSS-тем.</span></div>
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
