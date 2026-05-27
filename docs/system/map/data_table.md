# Технічна специфікація модуля: data_table.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ARCHIVE DATA TABLE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📋</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Raw Data Export: data_table</h1>
            <p class="mega-subtitle">Інтерфейс для детального перегляду та експорту первинних даних з бази. Підтримує стилізацію числових показників та генерацію CSV-файлів.</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT UI</span><span class="tag tag-version">v1.0.0</span><span class="tag tag-role">EXPORT MANAGER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">👀</div><div class="metric-info"><span class="metric-label">View</span><span class="metric-value">Interactive DataFrame</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔤</div><div class="metric-info"><span class="metric-label">Mapping</span><span class="metric-value">Technical -> Human</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💾</div><div class="metric-info"><span class="metric-label">Export</span><span class="metric-value">CSV Download Button</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛠️</div><div class="metric-info"><span class="metric-label">Format</span><span class="metric-value">Precision {:.2f}</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>data_table.py</b> забезпечує прозорість аналітики. Графіки — це добре, але оператору або Data-інженеру часто потрібно подивитися на сирі, "голі" цифри, щоб зрозуміти, чи немає помилок у БД.</p>
        <p style="margin-top: 12px;">Модуль рендерить велику таблицю <code>st.dataframe</code> з "сирими" даними (Raw Data). Він автоматично перекладає системні імена колонок ("ts", "load_mw") на зрозумілі ("Дата / Час", "Навантаження (МВт)"), і форматує дробові числа до двох знаків після коми (<code>{:.2f}</code>). Окрім цього, він серіалізує таблицю у CSV-формат (UTF-8 bytes) і надає кнопку завантаження (<code>st.download_button</code>).</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_raw_data_table(df: pd.DataFrame, start_date: str, end_date: str) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Контролер відображення таблиці. Проходить по внутрішньому словнику <code>mapping</code> і обирає тільки ті колонки, які існують у <code>df</code>. Перейменовує колонки для UI. Заповнює <code>NaN</code> значення нулями (<code>fillna(0.0)</code>) для числових полів. Рендерить <code>df.style.format()</code>. Генерує бінарний CSV рядок через <code>df.to_csv().encode('utf-8')</code> та підключає його до <code>st.download_button</code>. Наприкінці вставляє порожній <code>&lt;div&gt;</code> для нормального скролінгу.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Трансформації Таблиці</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render_raw_data_table(df)") --> MAP("Apply Column Mapping\n(ts -> Дата/Час, etc.)")
    
    MAP --> FILLNA("Fill NA values\n(0.0 for numeric columns)")
    
    FILLNA --> STYLE("df.style.format('{:.2f}')")
    
    STYLE --> RENDER("st.dataframe(..., height=400)")
    
    FILLNA --> CSV("df.to_csv().encode('utf-8')")
    
    CSV --> BUTTON("st.download_button(file_name=...)")
    
    RENDER --> CSS_FIX("st.markdown(Bottom Spacer div)")
    BUTTON --> CSS_FIX
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas (implicit via df methods)</span>
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
