# Технічна специфікація модуля: historical_audit.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DIGITAL ARCHIVE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📜</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">System Audit: historical_audit</h1>
            <p class="mega-subtitle">Панель цифрового архіву з підтримкою глибокого кореляційного аналізу, візуалізації "ритмів" споживання (Day Multipliers) та теплової діагностики активів.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY DUAL-AXIS</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">RETROSPECTIVE VIEW</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🌡️</div><div class="metric-info"><span class="metric-label">Weather</span><span class="metric-value">Load vs Air Temp</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛢️</div><div class="metric-info"><span class="metric-label">Physics</span><span class="metric-value">Load vs Oil Temp</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Health</span><span class="metric-value">Score vs H2 ppm</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⏳</div><div class="metric-info"><span class="metric-label">Rhythm</span><span class="metric-value">Weekday vs Weekend</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>historical_audit.py</b> — це інструмент для Data Scientists та Інженерів. Його головна мета — показати <i>причинно-наслідкові зв'язки</i> в історії енергосистеми.</p>
        <p style="margin-top: 12px;">Замість звичайних графіків тут активно використовуються Dual-Axis (дві шкали Y) візуалізації, щоб накласти один параметр на інший. Наприклад, як навантаження корелює з температурою повітря, або як виділення H2 вбиває Health Score трансформатора. Також модуль рендерить спеціальний "Ритмічний" графік, який показує патерни споживання у будні (працюють заводи) порівняно з вихідними днями (типовий спад). В кінці завжди виводиться Data Table з сирими даними.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render(selected_region: str, date_range=None, selected_substation: list|str) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Контролер архіву. 1. Викликає <code>_get_archive_bounds</code> для валідації дати. 2. Нормалізує цільовий об'єкт (конкретна станція чи всі разом). 3. Викликає <code>_load_archive_data</code>. Якщо станцій декілька — агрегує метрики через <code>groupby('ts').mean()</code>. 4. Формує 4 верхніх KPI-метрики (st.metric). 5. Виводить 3 блоки кореляцій через <code>render_dual_axis_chart</code>. 6. Завантажує дані для ритмів через <code>_load_rhythm_data</code> та будує <code>render_rhythm_chart</code>. 7. Виводить <code>render_raw_data_table</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Конвеєр Аналізу Архіву</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render(region, date_range, sub)") --> DB1("_get_archive_bounds()")
    
    DB1 --> TIME("Calculate effective\nstart_date, end_date")
    
    TIME --> DB2("_load_archive_data()")
    
    DB2 --> AGG{"Multiple Substations?"}
    AGG -->|Yes| GROUP("df.groupby('ts').mean()")
    AGG -->|No| KPI("Render st.metric KPIs")
    GROUP --> KPI
    
    KPI --> DUAL1("render_dual_axis_chart\n(Load vs Air Temp)")
    DUAL1 --> DUAL2("render_dual_axis_chart\n(Load vs Oil Temp)")
    DUAL2 --> DUAL3("render_dual_axis_chart\n(Health vs H2)")
    
    DUAL3 --> DB3("_load_rhythm_data()")
    DB3 --> RHYTHM("render_rhythm_chart()")
    
    RHYTHM --> RAW("render_raw_data_table()")
    RAW --> DONE("Spacer Height 300px")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.ui_helpers (safe_plotly_render)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database.archive (_get_archive_bounds, _load_archive_data, _load_rhythm_data)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.components.charts (render_dual_axis_chart, render_rhythm_chart)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.views.historical_audit_components.data_table (render_raw_data_table)</span>
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
