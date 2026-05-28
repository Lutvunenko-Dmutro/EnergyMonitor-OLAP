# Технічна специфікація модуля: __init__.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM UTILITIES</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛠️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">utils (Extended Toolkit)</h1>
            <p class="mega-subtitle">Пакет допоміжних утиліт. Набір інструментів для забезпечення стабільності, моніторингу та продуктивності всієї системи Atlas.</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON PACKAGE</span><span class="tag tag-version">v2.2.0</span><span class="tag tag-role">UTILITIES</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">💾</div><div class="metric-info"><span class="metric-label">Memory</span><span class="metric-value">GC & Optimization</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Errors</span><span class="metric-value">Safe Handlers</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">✔️</div><div class="metric-info"><span class="metric-label">Validation</span><span class="metric-value">Data Checking</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <b>utils</b> служить спільною "аптечкою" для всієї системи. Він містить низькорівневі функції, що можуть бути імпортовані в будь-який інший модуль (Core, UI, Services) без ризику утворення циклічних залежностей (Circular Dependency).</p>
        <p style="margin-top: 12px;">Ці утиліти не мають власного бізнес-контексту; вони просто виконують специфічні інженерні задачі: очищення пам'яті, логування, безпечне виконання функцій через try-except декоратори, форматування дат.</p>
    </div>
</div>

<!-- SECTION 02: TOOLKIT ARSENAL -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Арсенал Інструментів</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>memory_helper.py</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Оптимізація pd.DataFrame, збірка сміття (GC), моніторинг RAM.</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>cache_manager.py</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Логіка збереження результатів (Pickle/Parquet).</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>error_handlers.py</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Декоратори для безпечного перехоплення виключень.</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>ui_helpers.py</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Safe-рендеринг для Plotly та Streamlit.</span></div>
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
