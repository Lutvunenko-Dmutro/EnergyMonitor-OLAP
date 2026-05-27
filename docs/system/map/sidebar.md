# Технічна специфікація модуля: sidebar.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">COMMAND CENTER SIDEBAR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎛️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Strategic Control Panel: sidebar</h1>
            <p class="mega-subtitle">Головний інтерфейсний вузол для керування станом системи: каскадні фільтри, lifecycle симулятора датчиків, перемикання джерел даних та RAM-моніторинг.</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT SIDEBAR</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">CONTROL CENTER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔗</div><div class="metric-info"><span class="metric-label">Filters</span><span class="metric-value">Cascading Region→Station</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Sensors</span><span class="metric-value">subprocess.Popen</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🗄️</div><div class="metric-info"><span class="metric-label">Sources</span><span class="metric-value">Live DB ↔ Kaggle</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">RAM</span><span class="metric-value">psutil Health Widget</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>sidebar.py</b> — це "Пульт управління" диспетчера. Всі глобальні рішення (що відображати, за який час, по якому регіону) приймаються тут і передаються решті системи як кортеж повернених значень.</p>
        <p style="margin-top: 12px;">Каскадна фільтрація: спочатку юзер обирає <b>Регіон</b>, після чого система виконує SQL-запит до <code>Substations JOIN Regions</code> і динамічно формує список лише тих підстанцій, що належать цьому регіону. Управління симулятором: кнопка "▶️ Запустити" запускає <code>sensors_db</code> через <code>subprocess.Popen</code> з прихованим вікном на Windows (<code>CREATE_NO_WINDOW</code>). Наявність запуску визначається через перевірку lock-файлу.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_sidebar(data: dict) → tuple</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Повертає <code>(selected_region, date_range, data_source, selected_substation)</code>. 1. <code>apply_custom_css()</code>. 2. Оновлює Heartbeat-файл. 3. Radio-перемикач джерела даних. 4. Якщо Kaggle — завантажує через <code>load_kaggle_lazy()</code>. 5. Selectbox регіону. 6. SQL-запит для списку підстанцій конкретного регіону. 7. Multiselect підстанцій. 8. DatePicker з динамічним ключем. 9. Кнопки Lifecycle симулятора (перевірка lock-файлу). 10. RAM-виджет через <code>get_resource_status()</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Контрольної Панелі</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render_sidebar(data)") --> CSS("apply_custom_css()")
    CSS --> HB("heartbeat.txt.touch()")
    HB --> SRC("Radio: DB / Kaggle")
    SRC --> REG("Selectbox: Region\n(from load df)")
    REG --> SQL_SUB("SQL: SELECT sub_name\nJOIN Regions WHERE region=X")
    SQL_SUB --> MULTI("Multiselect: Substations\nDefault='Усі підстанції'")
    MULTI --> DATE("DatePicker\n(dynamic key per source)")
    DATE --> SIM{"sensors.lock exists?"}
    SIM -->|No| BTN_START("▶️ Start → subprocess.Popen\n(CREATE_NO_WINDOW)")
    SIM -->|Yes| BTN_STOP("🛑 Stop → os.kill(pid, SIGTERM)")
    BTN_START --> RAM("get_resource_status()\nRAM widget")
    BTN_STOP --> RAM
    DATE --> RAM
    RAM --> RETURN("Return (region, dates, source, sub)")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os, sys, signal, subprocess, datetime</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas, streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.app.config (DataKeys)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database (run_query)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.components.styles (apply_custom_css)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.services.data.db_seeder (generate_professional_data)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database.loader (load_kaggle_lazy)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.memory_helper (get_resource_status)</span>
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
