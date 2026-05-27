# Технічна специфікація модуля: logger.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM AUDIT SYSTEM</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📡</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Logging Orchestrator: logger</h1>
            <p class="mega-subtitle">Централізована реєстрація подій, моніторинг стану та аудит помилок у всіх компонентах Atlas з подвійним виводом (Console + File).</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON LOGGING</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">TELEMETRY</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📺</div><div class="metric-info"><span class="metric-label">Outputs</span><span class="metric-value">sys.stdout + system.log</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Redundancy</span><span class="metric-value">Handler Dup-Protection</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔇</div><div class="metric-info"><span class="metric-label">Noise</span><span class="metric-value">Suppress PIL / Streamlit</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⏱️</div><div class="metric-info"><span class="metric-label">Format</span><span class="metric-value">Time | Level | Module</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>logger.py</b> — це "Чорна скринька" системи. Замість звичайних <code>print()</code>, всі компоненти Atlas використовують цей логер для запису своїх дій. Це дозволяє легко відслідкувати, де сталася помилка, навіть якщо система впала.</p>
        <p style="margin-top: 12px;">У Streamlit є специфічна проблема: при кожному кліку в UI, він перезапускає скрипти. Якщо не додати захист, логер кожного разу створював би новий <code>Handler</code>, що призвело б до дублювання повідомлень (1 клік = 1 лог, 2 кліки = 2 однакових логи, 3 кліки = 3 і т.д.). Модуль блокує це через перевірку <code>if not logger.handlers:</code>. Крім того, він примусово "глушить" зайвий спам від зовнішніх бібліотек (Streamlit, PIL), залишаючи в логах лише чисту інформацію від Atlas.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def setup_logger(module_name: str) → logging.Logger</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний конструктор. Отримує <code>module_name</code> (зазвичай <code>__name__</code>). Перевіряє наявність обробників. Створює єдиний форматер (<code>[Час] ⚡ РІВЕНЬ | Модуль -> Текст</code>). Додає <code>StreamHandler(sys.stdout)</code> для перегляду в консолі та <code>FileHandler("system.log")</code> для запису на диск. Задає рівні логування для інших бібліотек: <code>streamlit=ERROR</code>, <code>PIL=WARNING</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Ініціалізації Логера</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("setup_logger(__name__)") --> GET("logging.getLogger()")
    
    GET --> CHK{"logger.handlers\nis empty?"}
    
    CHK -->|No| RETURN("Return Existing Logger\n(Prevents duplication)")
    
    CHK -->|Yes| FMT("Create Formatter\n'[Time] LEVEL | Module -> Msg'")
    
    FMT --> H1("StreamHandler (sys.stdout)")
    FMT --> H2("FileHandler ('system.log')")
    
    H1 --> ADD("logger.addHandler()")
    H2 --> ADD
    
    ADD --> NOISE("Mute 3rd-party noise\n(streamlit->ERROR, PIL->WARN)")
    
    NOISE --> SET_PROP("logger.propagate = False")
    SET_PROP --> RETURN
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sys (sys.stdout)</span>
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
