# Технічна специфікація модуля: __init__.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM SERVICE LAYER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛠️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">services (System Services)</h1>
            <p class="mega-subtitle">Сервісний рівень системи. Об'єднує функціональні сервіси, що керують життєвим циклом даних, симуляцією та міграціями.</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON PACKAGE</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">MIDDLEWARE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Data Services</span><span class="metric-value">Imports & Siding</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Simulation</span><span class="metric-value">Digital Twin</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔌</div><div class="metric-info"><span class="metric-label">Integration</span><span class="metric-value">Orchestrator</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <b>services</b> виступає в ролі Middleware (Проміжного ПЗ) між Системним Ядром (Core) та Інтерфейсом Користувача (UI). Якщо Core містить "голу математику" і прямі запити до БД, то Services інкапсулюють у собі складні бізнес-процеси (створення бази даних, міграції, генерацію синтетичних даних).</p>
        <p style="margin-top: 12px;">Цей рівень дозволяє керувати життєвим циклом системи та запускати скрипти як автономно з консолі (CLI), так і через фонові потоки всередині Streamlit-додатка.</p>
    </div>
</div>

<!-- SECTION 02: SUB-SYSTEMS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Внутрішні підсистеми</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>Simulation Engine</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Двигун "Цифрового двійника", що імітує датчики SCADA та генерує телеметрію в реальному часі.</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>Data Services</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Імпорт реальних даних з Kaggle (CSV), первинний сідінг бази (db_seeder).</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>Migration Logic</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Скрипти ініціалізації DDL SQL-схем.</span></div>
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
