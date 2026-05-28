# Технічна специфікація модуля: __init__.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ROOT PACKAGE ENTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🌍</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">src (Root)</h1>
            <p class="mega-subtitle">Головний пакет системи ATLAS. Виконує роль глобального неймспейсу для всього вихідного коду (Source Package). Всі імпорти в системі базуються на абсолютних шляхах від цього модуля.</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON PACKAGE</span><span class="tag tag-version">v3.0.0</span><span class="tag tag-role">NAMESPACE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📦</div><div class="metric-info"><span class="metric-label">Subpackages</span><span class="metric-value">6 (app, core, ml, services, ui, utils)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔒</div><div class="metric-info"><span class="metric-label">Import Policy</span><span class="metric-value">Absolute Only (src.*)</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>__init__.py</b> у корені <code>src/</code> виконує роль ініціалізатора головного пакету. Він гарантує, що Python розпізнає директорію <code>src</code> як пакет (package), дозволяючи імпортувати модулі з будь-якого місця проекту.</p>
        <p style="margin-top: 12px;">Це забезпечує модульність та масштабованість, оскільки розробники завжди знають єдину правильну точку відліку для імпортів. Використання відносних імпортів (<code>..</code>) суворо заборонено політикою архітектури ATLAS.</p>
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
