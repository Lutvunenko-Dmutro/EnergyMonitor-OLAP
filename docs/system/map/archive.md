# Технічна специфікація модуля: archive.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">HISTORICAL ARCHIVE ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📜</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">OLAP Data Sourcing: archive</h1>
            <p class="mega-subtitle">Механізм ретроспективних запитів. Здійснює агресивне кешування (st.cache_data) та об'єднання (Multidimensional Join) великих масивів історичних даних для аналізу трендів.</p>
            <div class="status-tags"><span class="tag tag-online">SQL ENGINE</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">DATA EXTRACTOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Cache</span><span class="metric-value">@st.cache_data (TTL: 600s)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔗</div><div class="metric-info"><span class="metric-label">Joins</span><span class="metric-value">Load + Assets + Weather</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🥁</div><div class="metric-info"><span class="metric-label">Rhythm</span><span class="metric-value">DOW x Hour Slicing</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📅</div><div class="metric-info"><span class="metric-label">Bounds</span><span class="metric-value">Min/Max Timestamp</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>archive.py</b> спеціалізується на <i>історичному зрізі даних</i> (Historical Archive). На відміну від лайв-дашборда, який оперує останніми 72 годинами, цей сервіс дозволяє витягувати дані за вибрані дати, накладаючи фільтри по регіонах чи підстанціях.</p>
        <p style="margin-top: 12px;">Головна особливість — використання інтенсивного кешування через <code>@st.cache_data(ttl=600)</code>. Це життєво необхідно, оскільки SQL-запити в цьому модулі об'єднують відразу декілька важких таблиць (LoadMeasurements, Substations, Regions, WeatherReports), і часте перемалювання UI без кешу "поклало" б базу даних.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@st.cache_data(ttl=3600)<br>def get_archive_bounds() → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Визначає календарні межі архіву. Робить швидкий запит до БД для отримання <code>MIN(timestamp)</code> та <code>MAX(timestamp)</code>. Використовується в UI для налаштування DatePicker-віджетів. Кешується на 1 годину.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@st.cache_data(ttl=600)<br>def load_archive_data(start: datetime.date, end: datetime.date, region: str) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний екстрактор. Виконує складний JOIN 4 таблиць. Витягує погодинні метрики: навантаження (МВт), температуру трансформатора (oil_temp), рівень газів (h2_ppm), індекс здоров'я (health) та метеодані (air_temp). Динамічно будує WHERE clauses в залежності від переданого регіону/підстанції.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@st.cache_data(ttl=600)<br>def load_rhythm_data(start: datetime.date, end: datetime.date, region: str) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Екстрактор для Heatmap. Використовує SQL-функцію <code>EXTRACT(ISODOW FROM timestamp)</code> для отримання дня тижня (1-7) та <code>EXTRACT(HOUR FROM timestamp)</code> для отримання години доби (0-23). Агрегує навантаження (AVG) по цих вимірах, дозволяючи візуалізувати "ритм" споживання.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема SQL Агрегацій</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI("UI Date/Region Picker") --> BOUNDS("get_archive_bounds()")
    UI --> BTN("User Clicks 'Load'")
    
    BTN --> CACHE{"In Streamlit\nCache?"}
    
    CACHE -->|Yes| RENDER("Render Dashboard")
    CACHE -->|No| SQL("Execute SQL Query")
    
    SQL --> DB[(PostgreSQL)]
    
    DB -.->|LoadMeasurements| JOIN("Multidimensional\nJOIN")
    DB -.->|Substations| JOIN
    DB -.->|Regions| JOIN
    DB -.->|WeatherReports| JOIN
    
    JOIN --> FILTERS("WHERE timestamp >= start\nAND region = :region")
    
    FILTERS --> RAW("load_archive_data()\n(Time Series)")
    FILTERS --> GRP("load_rhythm_data()\n(GROUP BY DOW, HOUR)")
    
    RAW --> CACHE2("Save to Cache (TTL 10m)")
    GRP --> CACHE2
    
    CACHE2 --> RENDER
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
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database</span>
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
