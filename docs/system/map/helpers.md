# Технічна специфікація модуля: helpers.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SHARED UTILITIES & HELPERS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛠️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Extended Toolkit: helpers</h1>
            <p class="mega-subtitle">Глобальна збірка універсальних інструментів та fallback-обгорток для дотримання принципу DRY та захисту від системних збоїв.</p>
            <div class="status-tags"><span class="tag tag-online">CORE UTILS</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">DRY ARCHITECTURE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Cleanse</span><span class="metric-value">Selection Normalizer</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">➗</div><div class="metric-info"><span class="metric-label">Math</span><span class="metric-value">Safe Division & Clip</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Pandas</span><span class="metric-value">Dry Date Filtering</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚨</div><div class="metric-info"><span class="metric-label">Fallback</span><span class="metric-value">Streamlit Exceptions</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>helpers.py</b> був створений для видалення "boilerplate" коду (коду, що постійно повторюється). Раніше кожен модуль сам перевіряв "А чи це нуль, коли я ділю?", або "А як юзер обрав станцію, масивом чи строкою?".</p>
        <p style="margin-top: 12px;">Тепер ці перевірки централізовані. Модуль містить безпечні математичні операції (<code>safe_divide</code>, <code>clip_value</code>), парсери "Все" (<code>is_all_keyword</code>), швидкі Pandas-фільтри (<code>filter_by_column</code>, <code>filter_by_date</code>) та інструменти пакетної обробки (<code>batch_list</code>). Унікальна риса — блок Fallbacks у кінці файлу, який експортує <code>RerunException</code> та <code>StopException</code> незалежно від версії Streamlit, гарантуючи сумісність.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def normalize_substation_selection(substation: str|list) → str|None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Витягує перший елемент зі списку, якщо передано масив. Якщо порожній масив — повертає "Усі підстанції". Це усуває потребу перевіряти типи об'єкта в кожному UI-компоненті.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def filter_by_date(df: pd.DataFrame, col: str, start: date, end: date) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Централізований фільтр. Перевіряє існування колонки, примусово конвертує її у <code>datetime64</code> (через <code>pd.to_datetime</code>), будує булеву маску <code>&gt;= start & &lt;= end</code> та повертає безпечну копію масиву.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def safe_divide(num: int|float, den: int|float, default: float = 0.0) → float</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Обгортка <code>try...except</code> для ділення. Якщо знаменник == 0, або передані нечислові типи (TypeError), або NaN — акуратно повертає <code>default</code> без падіння програми.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing (Union, List, Optional, Any, Tuple)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime.date</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>numpy</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit.runtime.scriptrunner (RerunException, StopException)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.app.types (SubstationSelection)</span>
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
