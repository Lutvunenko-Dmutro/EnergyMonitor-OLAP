# Технічна специфікація модуля: logger.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AUTOMATION ENGINE & UTILITY NODE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Служба автоматизації: logger</h1>
            <p class="mega-subtitle">Технічний скрипт автоматизації процесів збирання, аналізу або конвертації в екосистемі ATLAS</p>
            <div class="status-tags"><span class="tag tag-online">DEFENSE EDITION</span><span class="tag tag-version">v5.0.0</span><span class="tag tag-role">UTILITY SCRIPT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Runtime</span><span class="metric-value">Python 3.11+</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Execution</span><span class="metric-value">Automated Task</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧬</div><div class="metric-info"><span class="metric-label">Priority</span><span class="metric-value">High Performance</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Interface</span><span class="metric-value">CLI / Script</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>logger</b> забезпечує інтеграцію та виконання наступних обчислювальних процесів системи: <i>📡 LOGGING ORCHESTRATOR (System Audit System). Призначення: Централізована реєстрація подій, моніторинг стану та аудит помилок у всіх компонентах Atlas.</i><br><br><b>Архітектурний інтерфейс:</b> надає методи <code>setup_logger()</code>.</p>
    </div>
</div>

<!-- SECTION 02: CODE DOCUMENTATION (SMART PARSED) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Системний опис з коду (Docstring)</h2></div>
    <div class="glass-card flow-step" style="border-left: 4px solid var(--accent); padding-left: 20px;">
        <p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'>📡 LOGGING ORCHESTRATOR (System Audit System).</p>
<p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'><b>Призначення:</b> Централізована реєстрація подій, моніторинг стану та аудит помилок у всіх компонентах Atlas.</p>
<h3 style='color: var(--accent); font-family: "Orbitron", sans-serif; font-size: 15px; margin-top: 22px; margin-bottom: 10px;'>Ключові можливості</h3>
<ul style='margin-left: 20px; margin-bottom: 15px; list-style-type: square;'>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>🏗️ Unified Interface:</b> Стандартизований логер для забезпечення консистентності журналів.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>📺 Multi-channel Output:</b> Паралельний вивід у консоль (Real-time) та файл system.log (History).</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>🛡️ Redundancy Protection:</b> Захист від дублювання обробників при перезапусках Streamlit.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>🔇 Noise Reduction:</b> Фільтрація службових повідомлень від зовнішніх бібліотек (PIL, SQLAlchemy).</li>
</ul>
    </div>
</div>

<!-- SECTION 03: API REFERENCE (INTERACTIVE BLOCK) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Інтерфейси та сигнатури коду</h2></div>
    <div class="glass-card flow-step">
        <p style="margin-bottom: 15px; color: var(--text-dim);">Документовані класи та методи, знайдені за допомогою статичного аналізу коду (AST):</p>
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def setup_logger()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Налаштовує глобальний логер для проєкту.</p>
            </div>
            </div>
    </div>
</div>

<!-- SECTION 04: EXECUTION FLOW (DIAGRAM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Життєвий цикл виконання</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("Запуск logger.py") --> CONFIG("Ініціалізація оточення")
    CONFIG --> RUN("Основний алгоритм")
    RUN --> COMP("Завершення завдання")
    </div></div>
</div>

<!-- SECTION 05: MODULE DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <p style="margin-bottom: 12px; color: var(--text-dim);">Бібліотеки та модулі, що імпортуються цим файлом:</p>
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sys</span>
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
