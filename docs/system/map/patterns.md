# Технічна специфікація модуля: patterns.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SECURITY & QUALITY SIGNATURES</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛡️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Diagnostic Pattern Registry: patterns</h1>
            <p class="mega-subtitle">Централізоване сховище евристичних правил та regex-сигнатур вразливостей для системи автоматичного аудиту безпеки коду.</p>
            <div class="status-tags"><span class="tag tag-online">REGEX PATTERNS</span><span class="tag tag-version">v2.2.0</span><span class="tag tag-role">GUARDIAN RULES</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Scan dirs</span><span class="metric-value">7 директорій</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📦</div><div class="metric-info"><span class="metric-label">Whitelist</span><span class="metric-value">16 ThirdParty Libs</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚠️</div><div class="metric-info"><span class="metric-label">SQL Rules</span><span class="metric-value">F-String & % Injection</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔑</div><div class="metric-info"><span class="metric-label">Secrets</span><span class="metric-value">Hardcoded Password Detect</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>patterns.py</b> — це "Посвідчення" для системи аудиту. Сам по собі він не сканує нічого. Він лише декларує <b>правила</b>, за якими сканер (<code>scanner.py</code>) проводить перевірку.</p>
        <p style="margin-top: 12px;">Модуль містить: список директорій для обходу (<code>SCAN_DIRS</code>), список відомих бібліотек (<code>KNOWN_THIRD_PARTY</code>) для уникнення хибних "missing import" помилок, та найголовніше — список <code>SECURITY_PATTERNS</code>: кортежів <code>(regex, severity, code, message)</code>. Ці патерни можуть виловлювати SQL ін'єкції через f-strings, хардкодовані паролі, небезпечні <code>eval()</code> виклики та HTTP-запити без таймауту.</p>
    </div>
</div>

<!-- SECTION 02: SECURITY CATALOG -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Каталог Сигнатур Безпеки</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(248, 81, 73, 0.08); border-left: 3px solid #f85149;'><code style='color: #f85149; font-size: 13px; font-weight: 600;'>⛔ SQL_INJECTION_FSTRING</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>f-string всередині execute() — ERROR</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(210, 153, 34, 0.08); border-left: 3px solid #d29922;'><code style='color: #d29922; font-size: 13px; font-weight: 600;'>⚠️ SQL_INJECTION_FORMAT</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>% форматування в SQL — WARNING</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(248, 81, 73, 0.08); border-left: 3px solid #f85149;'><code style='color: #f85149; font-size: 13px; font-weight: 600;'>🔑 HARDCODED_SECRET</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>Рядковий літерал у password=... — ERROR</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(248, 81, 73, 0.08); border-left: 3px solid #f85149;'><code style='color: #f85149; font-size: 13px; font-weight: 600;'>☠️ DANGEROUS_EVAL</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>Виклик eval() або exec() — ERROR</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(210, 153, 34, 0.08); border-left: 3px solid #d29922;'><code style='color: #d29922; font-size: 13px; font-weight: 600;'>⚠️ UNSAFE_DESERIALIZATION</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>pickle.load або yaml.load — WARNING</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(210, 153, 34, 0.08); border-left: 3px solid #d29922;'><code style='color: #d29922; font-size: 13px; font-weight: 600;'>⏱️ MISSING_TIMEOUT</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>HTTP requests.get() без timeout= — WARNING</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(248, 81, 73, 0.08); border-left: 3px solid #f85149;'><code style='color: #f85149; font-size: 13px; font-weight: 600;'>🔑 EXPOSED_CONN_STRING</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>Відкритий рядок підключення postgresql:// — ERROR</span></div>
        </div>
    </div>
</div>

<!-- SECTION 03: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>re</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sys (stdlib_module_names)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pathlib.Path</span>
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
