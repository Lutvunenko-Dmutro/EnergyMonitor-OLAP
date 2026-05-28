# Технічна специфікація модуля: __init__.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATABASE ACCESS LAYER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🗄️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Database (NeonGuard)</h1>
            <p class="mega-subtitle">Рівень доступу до даних. Надає відмовостійкі механізми взаємодії з хмарною PostgreSQL (Neon DB), включаючи обробку "холодних стартів".</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON PACKAGE</span><span class="tag tag-version">v3.2.0</span><span class="tag tag-role">DATA LAYER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Retry Logic</span><span class="metric-value">Smart Backoff</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Memory Diet</span><span class="metric-value">Chunking Enabled</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔌</div><div class="metric-info"><span class="metric-label">Offline</span><span class="metric-value">Parquet Fallback</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <b>database</b> відповідає за взаємодію Системного Ядра з віддаленою базою даних PostgreSQL (хоститься на Neon DB). Він ізолює всю логіку з'єднань, обробки помилок мережі та транзакцій від решти коду.</p>
        <p style="margin-top: 12px;">Основна фіча пакету — система <b>NeonGuard</b>, яка автоматично обробляє проблему "холодного старту" безкоштовних інстансів Neon DB. Якщо база недоступна (502/504), система автоматично застосовує серію пауз із зростаючою затримкою та повторює запит.</p>
    </div>
</div>

<!-- SECTION 02: CORE MECHANICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Ключові Механіки</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>Memory Diet</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Читання масивів через <code>chunksize=5000</code> та примусовий збір сміття <code>gc.collect()</code>.</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>Offline Fallback</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Локальне кешування результатів запиту у `.parquet` файли для офлайн-режиму.</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>SQLAlchemy ORM</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Параметризовані SQL-команди для захисту від SQL Injection.</span></div>
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
