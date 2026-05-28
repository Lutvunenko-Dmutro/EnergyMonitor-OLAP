# Технічна специфікація модуля: config.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">GLOBAL CONFIG REGISTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">App Config (DataKeys)</h1>
            <p class="mega-subtitle">Централізоване сховище констант та ключів доступу до даних. Визначає структуру словників стану (State Dictionaries).</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON MODULE</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">CONFIG</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔑</div><div class="metric-info"><span class="metric-label">DataKeys</span><span class="metric-value">Enum Constants</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Data Routing</span><span class="metric-value">Key-based Mapping</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>config.py</b> є основним джерелом констант для іменування блоків даних у системі. Коли UI-компоненти отримують дані від Ядра (через словники типу <code>DataDict</code>), вони не повинні використовувати "магічні рядки" (magic strings) для доступу до них.</p>
        <p style="margin-top: 12px;">Використовуючи клас <code>DataKeys</code>, система гарантує, що ключ для доступу до даних про генерацію (наприклад, <code>DataKeys.GEN</code>) є ідентичним в усіх частинах коду. Це різко знижує ризик помилок доступу до пам'яті словників.</p>
    </div>
</div>

<!-- SECTION 02: CONFIGURATION CATALOG -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Реєстр Ключів (DataKeys)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>LOAD = "load"</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Ключ для доступу до даних споживання (Load Profile)</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>GEN = "gen"</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Ключ для доступу до даних генерації енергії</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>ALERTS = "alerts"</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Ключ для доступу до журналу аномалій та попереджень</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>LINES = "lines"</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Стан ліній електропередач</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>FINANCE = "fin"</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Економічні та фінансові показники системи</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>ALL_REGIONS = "Всі регіони"</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Системна константа для агрегації на національному рівні</span></div>
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
