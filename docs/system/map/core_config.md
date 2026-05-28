# Технічна специфікація модуля: config.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM CONFIGURATION REGISTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Core Config</h1>
            <p class="mega-subtitle">Центральний модуль для управління параметрами середовища, базами даних та константами симуляції енергомережі.</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON MODULE</span><span class="tag tag-version">v3.2.0</span><span class="tag tag-role">CORE SETUP</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🗄️</div><div class="metric-info"><span class="metric-label">Database</span><span class="metric-value">.env Secrets</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⏳</div><div class="metric-info"><span class="metric-label">Horizon</span><span class="metric-value">90 Days (60min)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔋</div><div class="metric-info"><span class="metric-label">Profiles</span><span class="metric-value">Res, Ind, Com</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>config.py</b> у пакеті <code>core</code> виконує роль "Диспетчера налаштувань". На відміну від <code>app/config.py</code>, який містить легкі UI-константи, цей модуль відповідає за важку серверну конфігурацію: паролі до бази даних PostgreSQL (Neon DB), параметри часових горизонтів для генератора даних (START_DATE, END_DATE) та математичні масиви.</p>
        <p style="margin-top: 12px;">Служить єдиним джерелом істини для інфраструктурних параметрів.</p>
    </div>
</div>

<!-- SECTION 02: LOAD PROFILES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичні профілі (Load Profiles)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>RESIDENTIAL</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Побутове навантаження. Характеризується високими вечірніми піками (18:00 - 21:00) та ранковим сплеском.</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>INDUSTRIAL</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Промислове навантаження. Рівномірне, стабільне високе споживання протягом всього дня.</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>COMMERCIAL</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Комерційне навантаження. Синхронізоване з робочими годинами (09:00 - 18:00), різке падіння вночі.</span></div>
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
