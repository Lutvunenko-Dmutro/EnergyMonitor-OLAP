# Технічна специфікація модуля: backtest.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">QUALITY ASSURANCE & AGGRESSIVE TESTING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🩺</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Тест-Сентинель: backtest</h1>
            <p class="mega-subtitle">Модуль автоматизованого верифікаційного контролю коду: backtest</p>
            <div class="status-tags"><span class="tag tag-online">DEFENSE EDITION</span><span class="tag tag-version">v5.0.0</span><span class="tag tag-role">TEST SENTINEL</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Engine</span><span class="metric-value">PyTest Suite</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Type</span><span class="metric-value">Unit / Integration</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧬</div><div class="metric-info"><span class="metric-label">Sentinel</span><span class="metric-value">Active Alert</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Coverage</span><span class="metric-value">Strict Validation</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>backtest</b> є критичним компонентом шару забезпечення якості (Quality Assurance). Його головна роль — автоматизована верифікація функціоналу модуля <code>backtest</code> на відповідність бізнес-вимогам та математичній точності.<br><br><b>Специфікація тесту:</b> 📉 HISTORICAL BACKTESTING ENGINE (ML Validation Hub). Модуль забезпечує наукову достовірність прогнозів через тестування моделей на історії.</p>
    </div>
</div>

<!-- SECTION 02: CODE DOCUMENTATION (SMART PARSED) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Системний опис з коду (Docstring)</h2></div>
    <div class="glass-card flow-step" style="border-left: 4px solid var(--accent); padding-left: 20px;">
        <p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'>📉 HISTORICAL BACKTESTING ENGINE (ML Validation Hub).</p>
<p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'>Модуль забезпечує наукову достовірність прогнозів через тестування моделей на історії.</p>
<h3 style='color: var(--accent); font-family: "Orbitron", sans-serif; font-size: 15px; margin-top: 22px; margin-bottom: 10px;'>Ключові можливості</h3>
<ol style='margin-left: 20px; margin-bottom: 15px;'>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>Historical Evaluation:</b> оцінка точності (1-Step-Ahead) на реальних замірах останніх періодів.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>Vectorized Batch Inference:</b> пакетне виконання прогнозів для миттєвого аудиту великих вікон даних.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>Statistical Audit:</b> розрахунок ключових метрик точності (RMSE, MAE, R-Squared) та похибок.</li>
<li style='margin-bottom: 6px; line-height: 1.5;'><b>Robust Handling:</b> інтеграція з Resilience Layer для стабільної роботи при перемиканні контекстів UI.</li>
</ol>
<p style='line-height: 1.7; margin-bottom: 12px; color: var(--text-main);'>Забезпечує доказову базу ефективності нейронних мереж для наукової звітності.</p>
    </div>
</div>

<!-- SECTION 03: API REFERENCE (INTERACTIVE BLOCK) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Інтерфейси та сигнатури коду</h2></div>
    <div class="glass-card flow-step">
        <p style="margin-bottom: 15px; color: var(--text-dim);">Документовані класи та методи, знайдені за допомогою статичного аналізу коду (AST):</p>
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def evaluate_last_24h()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Runs a 1-Step-Ahead vectorized evaluation strictly on the LAST 24 Hours.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def run_backtest_step()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Executes a segment of predictions for an interactive backtest session.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def get_fast_backtest()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>Batch-vectorized backtest for instant Multi-Dashboard metrics.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px; font-weight: 600;'>def get_backtest_metrics()</code>
                <p style='margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-dim);'>High-level wrapper for backtest execution (Compatibility layer).</p>
            </div>
            </div>
    </div>
</div>

<!-- SECTION 04: EXECUTION FLOW (DIAGRAM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Життєвий цикл виконання</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    RUNNER("PyTest Runner") --> INIT("Conftest Setup")
    INIT --> LOAD("Load Mocks / Database")
    LOAD --> TARGET("Test Target: backtest")
    TARGET --> ASSERT("Assertions: Verify Output")
    ASSERT --> PASS("Status: PASS / FAIL")
    </div></div>
</div>

<!-- SECTION 05: MODULE DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <p style="margin-bottom: 12px; color: var(--text-dim);">Бібліотеки та модулі, що імпортуються цим файлом:</p>
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>gc</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>numpy</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.metrics_engine</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.predict_v2</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.vectorizer</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.error_handlers</span><span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing</span>
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
