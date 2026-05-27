# Технічна специфікація модуля: error_handlers.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">RESILIENCE LAYER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🩹</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Fault Tolerance: error_handlers</h1>
            <p class="mega-subtitle">Шар відмовостійкості. Забезпечує захисне програмування (defensive programming) для критичних вузлів (ML, DB, I/O) через ізоляцію помилок та контекстне логування.</p>
            <div class="status-tags"><span class="tag tag-online">DEFENSE EDITION</span><span class="tag tag-version">v1.8.0</span><span class="tag tag-role">ERROR HANDLER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🤖</div><div class="metric-info"><span class="metric-label">ML Defense</span><span class="metric-value">Shape/Model Fallbacks</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔌</div><div class="metric-info"><span class="metric-label">DB Fault</span><span class="metric-value">Timeout/Conn Catch</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⏱️</div><div class="metric-info"><span class="metric-label">Audit</span><span class="metric-value">Context Timing (s)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Dicts/Obj</span><span class="metric-value">Safe Accessors</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>error_handlers.py</b> виконує роль "подушки безпеки" системи. Його завдання — не допустити "падіння" всього Streamlit-додатку (білий екран з трейсбеком) у випадку локальних збоїв: відсутності файлу моделі, розриву з'єднання з БД або невідповідності розмірностей тензорів.</p>
        <p style="margin-top: 12px;">Усі декоратори спеціально пропускають винятки <code>StopException</code> та <code>StreamlitAPIException</code>, оскільки вони є частиною нормального життєвого циклу Streamlit, і ловлять лише специфічні помилки, підміняючи результат на <code>default_value</code> або <code>None</code>.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def robust_ml_handler(func: Callable) → Callable</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Захисний декоратор для машинного навчання. Перехоплює <code>FileNotFoundError</code> (модель/скейлер не знайдені) та <code>ValueError</code> (наприклад, Shape Mismatch при предикті). При помилці логує її, виводить <code>st.error</code> та повертає <code>None</code>.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def robust_database_handler(func=None, default_value=None) → Callable</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Декоратор з підтримкою параметрів для БД. Перехоплює <code>ConnectionError</code> та <code>TimeoutError</code>. Замість "падіння" повертає заданий <code>default_value</code> (наприклад порожній словник чи 0), дозволяючи UI відрендерити порожні графіки.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>class ErrorContext</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Context Manager (використання з <code>with</code>). Логує старт операції (▶️), вимірює час її виконання, і логує завершення (✅) або помилку (❌) разом із типом винятку.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def safe_dict_access(d: dict, path: str, default=None)</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Утиліта для безпечного доступу до глибоко вкладених словників через dot-нотацію (напр., <code>"user.profile.age"</code>). Повертає default при KeyError.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема перехоплення (ML Handler)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    CALL("Виклик функції з @robust_ml_handler") --> TRY("try: execute func()")
    
    TRY --> SUCCESS{"Success?"}
    SUCCESS -->|Yes| RET("Return Result")
    
    SUCCESS -->|No| CHECK_ST{"Is Streamlit\nAPI Exception?"}
    CHECK_ST -->|Yes| RAISE("raise (let UI handle)")
    
    CHECK_ST -->|No| CATCH_IO{"Is FileNotFoundError?"}
    CATCH_IO -->|Yes| ERR1("Log: Model missing\nUI: st.error()\nReturn None")
    
    CATCH_IO -->|No| CATCH_VAL{"Is ValueError?"}
    CATCH_VAL -->|Yes| ERR2("Log: Shape mismatch\nUI: st.warning()\nReturn None")
    
    CATCH_VAL -->|No| ERR3("Generic Exception\nLog: traceback\nReturn None")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>functools</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime</span>
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
