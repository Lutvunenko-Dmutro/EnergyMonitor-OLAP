# Технічна специфікація модуля: __init__.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">APP PACKAGE ENTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📦</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">app (Application Core Interface)</h1>
            <p class="mega-subtitle">Кореневий вузол рівня додатка, що визначає глобальні контракти, типи даних та конфігурації Atlas.</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON PACKAGE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">APP CORE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Data Types</span><span class="metric-value">Unified Contracts</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Constants</span><span class="metric-value">Global Parameters</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🏗️</div><div class="metric-info"><span class="metric-label">Build</span><span class="metric-value">Orchestration</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <b>app</b> служить точкою об'єднання (Application Core Interface). Він забезпечує синхронізацію між Ядром (Core) та Інтерфейсом (UI) за допомогою чітко визначених контрактів обміну даними.</p>
        <p style="margin-top: 12px;">Кожен запит з UI до бази даних чи машинного навчання базується на структурах, визначених у цьому пакеті. Це дозволяє здійснювати строгий статичний аналіз коду та уникати помилок типу <code>KeyError</code> чи <code>TypeError</code> на етапі виконання.</p>
    </div>
</div>

<!-- SECTION 02: PACKAGE COMPONENTS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Внутрішні компоненти</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>types.py</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Реєстр типізованих аліасів (TypeAlias)</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>config.py</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Глобальний реєстр конфігурацій (DataKeys)</span></div>
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
