# Технічна специфікація модуля: splash.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ACTIVE BOOT SEQUENCE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚀</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Boot Screen: splash</h1>
            <p class="mega-subtitle">Інтерактивна заставка завантаження у стилі "Cyber-HUD". CRT-ефекти, живі лог-рядки, прогрес-бар та вибір вузла підключення (Local / Cloud).</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT HTML</span><span class="tag tag-version">v2.8.5</span><span class="tag tag-role">BOOT IMMERSION</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Style</span><span class="metric-value">Orbitron + CRT Scanlines</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🖥️</div><div class="metric-info"><span class="metric-label">Node</span><span class="metric-value">LOCAL / CLOUD NEON</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Progress</span><span class="metric-value">Live Boot Generator</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Integration</span><span class="metric-value">Data Collector Loop</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>splash.py</b> відповідає за <b>перше враження</b> від системи. Оскільки підключення до БД може займати 5-15 секунд, просто показати "порожній екран" — неприпустимо. Замість цього юзер бачить анімований екран у стилі голлівудського хакерського фільму.</p>
        <p style="margin-top: 12px;">Архітектурний прийом — <code>st.empty()</code> placeholder: він займає місце на екрані, і модуль постійно перезаписує його вміст через <code>placeholder.markdown(html)</code>. Це імітує <i>живий поток логів</i>, хоча насправді кожен новий рядок просто додається до HTML-шаблону. Паралельно з анімацією, відбувається реальне завантаження даних через генератор <code>get_active_boot_data_generator()</code>. Результат — і красиво, і продуктивно.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def show_boot_sequence() → dict</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Повна точка входу. <b>Фаза 0 — Вибір вузла:</b> якщо немає <code>db_mode</code> в session_state, відображає вибір LOCAL/CLOUD через два кнопкові блоки зі стилізованим HTML (Orbitron font, зелена неон-рамка). <b>Фаза 1 — Активний Бут:</b> ітерується через <code>get_active_boot_data_generator()</code>. На кожній ітерації додає лог-рядок до акумулятора <code>log_acc</code> та оновлює <code>placeholder</code>. <b>Після завершення:</b> чекає 0.5 сек, прибирає заставку (<code>placeholder.empty()</code>). Повертає завантажені дані <code>final_data</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Boot Sequence Lifecycle</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("show_boot_sequence()") --> CHK_MODE{"db_mode in\nsession_state?"}
    CHK_MODE -->|No| SELECT("Show Node Selection\nLOCAL / CLOUD buttons")
    SELECT --> RERUN("User clicks → st.rerun()")
    CHK_MODE -->|Yes| PH("placeholder = st.empty()")
    PH --> BOOT_GEN("for msg, p, data in\nget_active_boot_data_generator():")
    BOOT_GEN --> ACCUM("log_acc += log_line HTML")
    ACCUM --> RENDER("placeholder.markdown\n(HTML with progress)")
    RENDER --> SLEEP("time.sleep(0.1)")
    SLEEP --> BOOT_GEN
    BOOT_GEN -->|Done| FINAL("time.sleep(0.5)\nplaceholder.empty()")
    FINAL --> RETURN("Return final_data dict")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>time</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database.loader (get_active_boot_data_generator)</span>
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
