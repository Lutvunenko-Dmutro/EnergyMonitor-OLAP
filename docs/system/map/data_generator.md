# Технічна специфікація модуля: data_generator.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AUTOMATION ENGINE & UTILITY NODE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Служба автоматизації: data_generator</h1>
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
        <p>Модуль <b>data_generator</b> забезпечує інтеграцію та виконання наступних обчислювальних процесів системи: <i>ДВИГУН БЕЗПЕРЕРВНОЇ СИМУЛЯЦІЇ (Continuous Digital Twin Engine) Ядро системи для імітації роботи енергомережі в режимі реального часу.</i><br><br><b>Архітектурний інтерфейс:</b> надає методи <code>_init_sensor_state()</code>, <code>_process_sensor_tick()</code>.</p>
    </div>
</div>

<!-- SECTION 02: CODE DOCUMENTATION (SMART PARSED) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Системний опис з коду (Docstring)</h2></div>
    <div class="glass-card flow-step" style="border-left: 4px solid var(--accent); padding-left: 20px;">
        <p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'>ДВИГУН БЕЗПЕРЕРВНОЇ СИМУЛЯЦІЇ (Continuous Digital Twin Engine)</p>
<p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'>Ядро системи для імітації роботи енергомережі в режимі реального часу.</p>
<h3 style='color: var(--accent); font-family: "Orbitron", sans-serif; font-size: 15px; margin-top: 22px; margin-bottom: 10px;'>Ключові можливості</h3>
<ol style='margin-left: 20px; margin-bottom: 15px;'>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>Real-time Telemetry Synthesis:</b> щосекундна генерація замірів для всіх підстанцій.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>Asset Stress Modeling:</b> динамічний розрахунок фізичних параметрів (Temp, H2) від навантаження.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>Stateful Cycle Management:</b> підтримка стану "цифрового двійника" між ітераціями.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>Autonomous Operation:</b> автоматичне оновлення метеоумов та цінових трендів.</li>
</ol>
<p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'>Створює живий потік даних для тестування ШІ-алгоритмів та інтерфейсів у динаміці.</p>
    </div>
</div>

<!-- SECTION 03: API REFERENCE (INTERACTIVE BLOCK) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Інтерфейси та сигнатури коду</h2></div>
    <div class="glass-card flow-step">
        <p style="margin-bottom: 15px; color: var(--text-dim);">Документовані класи та методи, знайдені за допомогою статичного аналізу коду (AST):</p>
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def _init_sensor_state()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Ініціалізує початковий стан сенсорів:</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def _process_sensor_tick()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Один тік симуляції: розраховує стан кожної підстанції та записує у БД.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def run_realtime_sensors()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Симуляція реального часу (Continuous Digital Twin).</p>
            </div>
            </div>
    </div>
</div>

<!-- SECTION 04: EXECUTION FLOW (DIAGRAM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Життєвий цикл виконання</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("Запуск data_generator.py") --> CONFIG("Ініціалізація оточення")
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
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>random</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.logger</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.physics</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.services.simulation.generator_constants</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>time</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing</span>
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
