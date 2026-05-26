# Технічна специфікація модуля: validators.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AUTOMATION ENGINE & UTILITY NODE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Служба автоматизації: validators</h1>
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
        <p>Модуль <b>validators</b> забезпечує інтеграцію та виконання наступних обчислювальних процесів системи: <i>🛡️ SECURITY & VALIDATION LAYER (Input Shield). Модуль: validators.py | Версія: 2.2.0 "SafeGuard" Призначення: Забезпечення кібербезпеки та цілісності даних через багатошарову валідацію користувацького вводу та системних параметрів.</i><br><br><b>Архітектурний інтерфейс:</b> реалізує класи <code>ValidationError</code>; надає методи <code>_has_dangerous_patterns()</code>, <code>validate_step_key()</code>.</p>
    </div>
</div>

<!-- SECTION 02: CODE DOCUMENTATION (SMART PARSED) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Системний опис з коду (Docstring)</h2></div>
    <div class="glass-card flow-step" style="border-left: 4px solid var(--accent); padding-left: 20px;">
        <p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'>🛡️ SECURITY & VALIDATION LAYER (Input Shield).</p>
<p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'><b>Модуль:</b> validators.py | Версія: 2.2.0 "SafeGuard"</p>
<p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'><b>Призначення:</b> Забезпечення кібербезпеки та цілісності даних через багатошарову валідацію користувацького вводу та системних параметрів.</p>
<h3 style='color: var(--accent); font-family: "Orbitron", sans-serif; font-size: 15px; margin-top: 22px; margin-bottom: 10px;'>Ключові механізми</h3>
<ul style='margin-left: 20px; margin-bottom: 15px; list-style-type: square;'>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>🚫 Anti-Injection Engine:</b> Глибоке сканування вводу на наявність небезпечних SQL-патернів.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>⚪ Whitelist Validation:</b> Верифікація ідентифікаторів об'єктів за еталонними реєстрами.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>📏 Bounds Checking:</b> Суворий контроль числових меж для фізичних та енергетичних показників.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>🧹 SQL Sanitization:</b> Очищення ідентифікаторів перед використанням у динамічних запитах.</li>
</ul>
    </div>
</div>

<!-- SECTION 03: API REFERENCE (INTERACTIVE BLOCK) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Інтерфейси та сигнатури коду</h2></div>
    <div class="glass-card flow-step">
        <p style="margin-bottom: 15px; color: var(--text-dim);">Документовані класи та методи, знайдені за допомогою статичного аналізу коду (AST):</p>
        
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 15px;'>
                <span style='color: #fb923c; font-weight: bold;'>class ValidationError</span>
                <p style='margin: 5px 0 10px 0; font-size: 13.5px; color: var(--text-dim);'>Raised when input validation fails.</p>
                <div style='margin-left: 15px;'>
            </div></div><div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def _has_dangerous_patterns()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Check if text contains SQL injection patterns.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def validate_step_key()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Validate step key against whitelist.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def validate_substation_name()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Validate substation name(s) against whitelist.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def validate_region_name()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Validate region name.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def validate_date_range()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Validate date range.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def validate_data_source()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Validate data source name.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def sanitize_column_name()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Sanitize column name for safe SQL use.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def validate_numeric_input()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Validate numeric input with bounds checking.</p>
            </div>
            </div>
    </div>
</div>

<!-- SECTION 04: EXECUTION FLOW (DIAGRAM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Життєвий цикл виконання</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("Запуск validators.py") --> CONFIG("Ініціалізація оточення")
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
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing</span>
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
