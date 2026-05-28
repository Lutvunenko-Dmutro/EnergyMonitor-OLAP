# Технічна специфікація модуля: __init__.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CORE LOGIC PACKAGE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧠</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">core (System Kernel)</h1>
            <p class="mega-subtitle">Пакет системного ядра. Містить фундаментальні модулі, що забезпечують життєдіяльність системи Atlas.</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON PACKAGE</span><span class="tag tag-version">v3.5.0</span><span class="tag tag-role">KERNEL</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🗄️</div><div class="metric-info"><span class="metric-label">Database Layer</span><span class="metric-value">NeonGuard ORM</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Analytics</span><span class="metric-value">Physics & Models</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Logger & Config</span><span class="metric-value">Global Setup</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <b>core</b> — це Ядро (Kernel) платформи ATLAS. Воно абстрагує складні інженерні механізми (роботу з хмарними БД, складну фізико-математичну фільтрацію, аналітику) від високорівневих сервісів та інтерфейсу.</p>
        <p style="margin-top: 12px;">Цей пакет спроектований так, щоб бути максимально ізольованим: він не знає про існування Streamlit (UI) або сторонніх сервісів-утиліт. Це забезпечує чисту архітектуру та високу надійність (Solid Architecture).</p>
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
