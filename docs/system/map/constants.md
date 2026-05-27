# Технічна специфікація модуля: constants.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">FORECAST UI REGISTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">UI Registry: constants</h1>
            <p class="mega-subtitle">Централізоване сховище текстових міток та колірних схем для оформлення аналітичних звітів та графіків ШІ-моделей (v1-v3).</p>
            <div class="status-tags"><span class="tag tag-online">CONFIGURATION</span><span class="tag tag-version">v1.0.0</span><span class="tag tag-role">DICTIONARIES</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🏷️</div><div class="metric-info"><span class="metric-label">Labels</span><span class="metric-value">Unified Model Naming</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Colors</span><span class="metric-value">Brand Color Coding</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📌</div><div class="metric-info"><span class="metric-label">Role</span><span class="metric-value">Single Source of Truth</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Type</span><span class="metric-value">Static Dictionaries</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>constants.py</b> дуже маленький, але архітектурно важливий. Він гарантує, що у всьому додатку (на графіках, в легендах, в таблицях) версії моделей (v1, v2, v3) будуть називатися однаково і мати однаковий колір.</p>
        <p style="margin-top: 12px;">Це запобігає ситуаціям, коли на одному графіку v3 має зелений колір, а на іншому — синій, що сильно плутає користувача. Всі UI-компоненти, які малюють графіки, імпортують <code>MODEL_COLORS</code> з цього файлу.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічні словники</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>MODEL_LABELS</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Словник (dict), що зіставляє системні версії ('v1', 'v2', 'v3') з повними зрозумілими назвами, наприклад <code>"LSTM-v2 (5 ознак · Телеметрія)"</code>. Використовується в Select-боксах та легендах графіків.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>MODEL_COLORS</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Словник (dict) HEX-кодів. v1: "#ff9f43" (Помаранчевий), v2: "#ee5253" (Червоний), v3: "#10ac84" (Зелений). Використовується для Plotly <code>color_discrete_map</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <p style="color: var(--text-dim); margin-bottom: 0;"><i>Цей модуль не має зовнішніх залежностей.</i></p>
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
