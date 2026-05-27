# Технічна специфікація модуля: map.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">GEOSPATIAL GRID MONITOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📍</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Geospatial Visualizer: map</h1>
            <p class="mega-subtitle">Забезпечує інтерактивне відображення об'єктів енергосистеми на карті. Підтримує Plotly Mapbox з двома режимами: Статус-маркери та Heatmap.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY MAPBOX</span><span class="tag tag-version">v1.5.0</span><span class="tag tag-role">MAP COMPONENT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🗺️</div><div class="metric-info"><span class="metric-label">Engine</span><span class="metric-value">Carto-Darkmatter</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔴</div><div class="metric-info"><span class="metric-label">Markers</span><span class="metric-value">scatter_mapbox (Load %)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔥</div><div class="metric-info"><span class="metric-label">Heatmap</span><span class="metric-value">density_mapbox</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Safety</span><span class="metric-value">Coord Existence Check</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>map.py</b> відповідає за просторову оцінку енергомережі. Це дозволяє диспетчеру поглянути на країну зверху та побачити, де саме зараз виникає дефіцит енергії або критичне перевантаження підстанції.</p>
        <p style="margin-top: 12px;">У модулі реалізовано динамічний парсинг: він автоматично визначає, чи є в даних колонки <code>capacity_mw</code>, <code>temperature_c</code> тощо, і якщо є — збагачує ними спливаючі підказки (hover data) та визначає розмір і колір маркерів. За замовчуванням карта має темний сучасний стиль <code>carto-darkmatter</code>, а користувач може перемикатися між точковими маркерами (зелений-жовтий-червоний) та плавною тепловою картою (Viridis heatmap).</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render(df_load: pd.DataFrame) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Рендерить карту. 1. Створює Radio-перемикач режимів (Маркери/Heatmap). 2. Фільтрує дані: знаходить останній timestamp для кожної станції через <code>groupby().tail(1)</code>. 3. Перевіряє наявність <code>latitude</code>/<code>longitude</code> (захист від крашу). 4. Динамічно рахує <code>load_pct</code> (відсоток завантаження) якщо є <code>capacity_mw</code>. 5. Визначає hover_name (substation_name або region_name). 6. Викликає <code>px.scatter_mapbox</code> або <code>px.density_mapbox</code>. 7. Рендерить через <code>safe_plotly_render</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Побудови Карти</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render(df_load)") --> UI("Radio Toggle: Marker / Heatmap")
    
    UI --> CHK_EMPTY{"df_load.empty?"}
    CHK_EMPTY -->|Yes| STOP("Warning: No Data")
    
    CHK_EMPTY -->|No| GROUP("groupby('substation_name').tail(1)\nGet latest state only")
    
    GROUP --> CHK_LL{"Has lat/lon cols?"}
    CHK_LL -->|No| STOP2("Warning: No Geodata")
    
    CHK_LL -->|Yes| DYNAMIC("Inject hover_data params\nCalculate load_pct if capacity_mw exists")
    
    DYNAMIC --> R_MODE{"map_mode"}
    
    R_MODE -->|Marker| SCATTER("px.scatter_mapbox()\nColor: Green->Red\nSize: load/capacity")
    R_MODE -->|Heatmap| DENSITY("px.density_mapbox()\nColor: Viridis\nZ: actual_load_mw")
    
    SCATTER --> RENDER("safe_plotly_render(fig)")
    DENSITY --> RENDER
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.express (px)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.ui_helpers (safe_plotly_render)</span>
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
