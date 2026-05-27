# Технічна специфікація модуля: queries.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">OPTIMIZED SQL LIBRARY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📖</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">SQL Константи: queries</h1>
            <p class="mega-subtitle">Централізована бібліотека SQL-рядків для складних аналітичних операцій, корелятивних JOIN-запитів та денормалізації даних з OLAP-схеми.</p>
            <div class="status-tags"><span class="tag tag-online">MULTI-JOIN SQL</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">QUERY CONSTANTS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔗</div><div class="metric-info"><span class="metric-label">Load+Weather</span><span class="metric-value">5-Table JOIN</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Generation</span><span class="metric-value">LIMIT 50 000 Rows</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📏</div><div class="metric-info"><span class="metric-label">Lines</span><span class="metric-value">Dynamic Load_pct CASE</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💰</div><div class="metric-info"><span class="metric-label">Finance</span><span class="metric-value">Price × Load Cost Calc</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>queries.py</b> — це "Книга SQL-заклинань" системи. Замість того щоб писати сирі SQL-рядки всередині Python-функцій (де їх важко тестувати і знайти), всі складні запити централізовані тут як іменовані константи.</p>
        <p style="margin-top: 12px;">Це дозволяє: легко знайти і переписати запит без пошуку по всьому проєкту; скоротити ризик SQL-помилок через дублювання; використовувати SQL-синтаксичний підсвітлювач у IDE. Найцікавіший запит — <code>QUERY_LINES</code>: він динамічно рахує <code>load_pct</code> прямо в БД через <code>CASE WHEN max_load_mw > 0</code>, уникаючи ділення на нуль.</p>
    </div>
</div>

<!-- SECTION 02: SQL CATALOG -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Каталог SQL-Запитів</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>QUERY_LOAD_WEATHER</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Основний навантажувальний запит. JOIN між <code>LoadMeasurements</code>, <code>Substations</code>, <code>Regions</code> та <code>WeatherReports</code> (LEFT JOIN). Вибирає: timestamp, region_name, actual_load_mw, lat/lon, capacity_mw, temperature. Дані за останні 30 днів.</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>QUERY_GENERATION</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Генерація за типами. JOIN між <code>GenerationMeasurements</code>, <code>Generators</code>, <code>Substations</code>, <code>Regions</code>. Вибирає: timestamp, generator_type, actual_generation_mw, region_name. LIMIT 50000.</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>QUERY_LINES</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Топологія ліній. Динамічно обчислює <code>load_pct = actual_load_mw / max_load_mw * 100</code> через SQL CASE для захисту від ділення на 0. JOIN з <code>PowerLines</code>, <code>Substations</code>, <code>Regions</code>.</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>QUERY_FINANCE</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Фінансовий аналіз. JOIN з <code>EnergyPricing</code> по timestamp і region_id. Розраховує <code>cost = actual_load_mw * price_per_mwh</code> прямо в SQL.</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>QUERY_REAL_LOAD</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Реальні дані (Kaggle). Читає з ізольованої таблиці <code>RealLoadMeasurements</code>. Підставляє константну назву регіону 'Kaggle AEP (США)'. За останні 30 днів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(168, 162, 158, 0.1); border: 1px solid rgba(168, 162, 158, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: #a8a29e; margin: 4px;'>Немає імпортів — чистий модуль SQL-констант</span>
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
