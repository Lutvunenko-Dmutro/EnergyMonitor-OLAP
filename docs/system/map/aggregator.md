# Технічна специфікація модуля: aggregator.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ANALYTICAL DATA AGGREGATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">OLAP Engine: aggregator</h1>
            <p class="mega-subtitle">Високопродуктивна обробка, ресемплінг та нормалізація сирих метрик. Формує агреговані зрізи (OLAP) для формування цілісної аналітичної картини в дашбордах.</p>
            <div class="status-tags"><span class="tag tag-online">PANDAS ENGINE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">ETL AGGREGATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⏳</div><div class="metric-info"><span class="metric-label">Resampling</span><span class="metric-value">1h-window (mean)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📏</div><div class="metric-info"><span class="metric-label">Normalization</span><span class="metric-value">Relative Load (%)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">ETL Hybrid</span><span class="metric-value">DB 72h / Kaggle 48h</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Synthesis</span><span class="metric-value">Global SUM / AVG</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>aggregator.py</b> працює на рівні проміжної обробки даних (Business Logic). Його головна задача — прийняти сирі (або частково відфільтровані) дані з БД чи Kaggle та перетворити їх на зручний для графіків формат.</p>
        <p style="margin-top: 12px;">Зокрема, модуль згладжує "шум" у часових рядах, дискретизуючи (Resampling) дані за годинними інтервалами (<code>1h</code>). Він також дозволяє перевести абсолютні значення мегават (МВт) у відносні відсотки (Relative Load), що критично важливо для порівняльного аналізу маленьких та великих підстанцій на одному графіку.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def aggregate_consumption(df: pd.DataFrame, group_by_col: str, num_cols: list) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Конвертує стовпець часу у <code>datetime</code>, групує за вказаним полем (напр. підстанція чи регіон) і застосовує <code>.resample("1h").mean()</code> до числових колонок. Повертає відсортований датафрейм без NaN значень.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def add_relative_load(df: pd.DataFrame, group_by_col: str) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Нормалізує навантаження. Для кожної групи (<code>group_by_col</code>) знаходить максимум і розраховує <code>x / max * 100</code>. Використовує <code>.replace</code> замість <code>.fillna</code> для безпечної роботи з Categorical Dtypes.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_history_live(substation_name: str | None) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>SQL-екстрактор. Завантажує останні <b>72 години</b> з PostgreSQL. Якщо обрано список "Всі", виконує глобальну агрегацію <code>SUM(load)</code>, якщо конкретні — фільтрує через <code>ANY(:sub)</code>.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_history_csv(substation_name: str | None = None) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Екстрактор локальних архівів. Завантажує дані з Kaggle датасету (через <code>load_kaggle_data()</code>) і повертає зріз за останні <b>48 годин</b>. Також підтримує глобальну агрегацію (SUM).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">ETL пайплайн агрегації</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI("UI Request\n(Substation/Region)") --> SRC{"Source?"}
    
    SRC -->|Live DB| LIVE("get_history_live(sub_name)\nSQL: SELECT ... WHERE >= NOW() - 72h")
    SRC -->|Kaggle CSV| CSV("get_history_csv(sub_name)\nPandas: filter >= MAX - 48h")
    
    LIVE --> RAW(Raw DataFrame)
    CSV --> RAW
    
    RAW --> RESAMP("aggregate_consumption(df)\n.resample('1h').mean()")
    
    RESAMP --> REL("add_relative_load(df)\nGroup Transform (x/max*100)")
    
    REL --> FINAL("Final Aggregated Data\nfor Plotly Charts")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.kaggle_loader (inline)</span>
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
