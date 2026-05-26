# Технічна специфікація модуля: reporter.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AUTOMATION ENGINE & UTILITY NODE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Служба автоматизації: reporter</h1>
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
        <p>Модуль <b>reporter</b> забезпечує інтеграцію та виконання наступних обчислювальних процесів системи: <i>📊 DIAGNOSTICS REPORTING ENGINE (Health Auditor). py | Версія: 1.5.0 Призначення: Трансформація результатів технічного аудиту в інтерактивні HTML-звіти з використанням сучасних стандартів візуалізації.</i><br><br><b>Архітектурний інтерфейс:</b> реалізує класи <code>HtmlReporter</code>.</p>
    </div>
</div>

<!-- SECTION 02: CODE DOCUMENTATION (SMART PARSED) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Системний опис з коду (Docstring)</h2></div>
    <div class="glass-card flow-step" style="border-left: 4px solid var(--accent); padding-left: 20px;">
        <p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'>📊 DIAGNOSTICS REPORTING ENGINE (Health Auditor).</p>
<p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'><b>py | Версія:</b> 1.5.0</p>
<p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'><b>Призначення:</b> Трансформація результатів технічного аудиту в інтерактивні HTML-звіти з використанням сучасних стандартів візуалізації.</p>
<h3 style='color: var(--accent); font-family: "Orbitron", sans-serif; font-size: 15px; margin-top: 22px; margin-bottom: 10px;'>Ключові можливості</h3>
<ul style='margin-left: 20px; margin-bottom: 15px; list-style-type: square;'>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>📊 State Aggregation:</b> Підрахунок глобальних метрик здоров'я проєкту (OK/Warning/Error).</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>🎨 Visual Highlighting:</b> Кольорова індикація проблем за рівнем критичності (GitHub-style).</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>🛡️ Security Focused reporting:</b> Окреме виділення вразливостей безпеки.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>📄 Automated Documentation:</b> Формування автономного файлу diagnostics_report.html.</li>
</ul>
    </div>
</div>

<!-- SECTION 03: API REFERENCE (INTERACTIVE BLOCK) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Інтерфейси та сигнатури коду</h2></div>
    <div class="glass-card flow-step">
        <p style="margin-bottom: 15px; color: var(--text-dim);">Документовані класи та методи, знайдені за допомогою статичного аналізу коду (AST):</p>
        
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 15px;'>
                <span style='color: #fb923c; font-weight: bold;'>class HtmlReporter</span>
                <p style='margin: 5px 0 10px 0; font-size: 13.5px; color: var(--text-dim);'>Клас об'єктної моделі.</p>
                <div style='margin-left: 15px;'>
            
                    <div style='margin-bottom: 8px; border-left: 2px solid var(--accent); padding-left: 10px;'>
                        <code style='color: var(--accent); font-weight: 600;'>def generate()</code>
                        <p style='margin: 2px 0 0 0; font-size: 12px; color: var(--text-dim);'>Метод класу.</p>
                    </div>
                
                    <div style='margin-bottom: 8px; border-left: 2px solid var(--accent); padding-left: 10px;'>
                        <code style='color: var(--accent); font-weight: 600;'>def _file_row()</code>
                        <p style='margin: 2px 0 0 0; font-size: 12px; color: var(--text-dim);'>Метод класу.</p>
                    </div>
                </div></div>
    </div>
</div>

<!-- SECTION 04: EXECUTION FLOW (DIAGRAM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Життєвий цикл виконання</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("Запуск reporter.py") --> CONFIG("Ініціалізація оточення")
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
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>models</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pathlib</span>
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
