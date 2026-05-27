# Технічна специфікація модуля: kpi.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SITUATIONAL AWARENESS VIEW</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Live Diagnostics: kpi</h1>
            <p class="mega-subtitle">Візуалізатор оперативного моніторингу. Збирає метрики з усього масиву телеметрії та відображає індекси здоров'я, частоту та навантаження об'єктів.</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT UI</span><span class="tag tag-version">v1.8.0</span><span class="tag tag-role">DASHBOARD GRID</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Top KPIs</span><span class="metric-value">4 Columns (st.metric)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📋</div><div class="metric-info"><span class="metric-label">Data Grid</span><span class="metric-value">st.dataframe with Progress Bars</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Failsafe</span><span class="metric-value">pd.to_numeric Coercion</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Adaptation</span><span class="metric-value">Kaggle vs Live Modes</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>kpi.py</b> (перебуває у папці views) відповідає виключно за рендеринг того датафрейму, який йому передає <code>live_kpi</code> оркестратор. Це головний екран диспетчера, куди він дивиться найбільше.</p>
        <p style="margin-top: 12px;">Модуль поділений на дві частини. <b>Верхній ярус:</b> агреговані показники (середнє здоров'я, глобальна частота мережі, сумарна потужність та UI-спідометр навантаження). <b>Нижній ярус:</b> деталізована інтерактивна таблиця <code>st.dataframe</code> всіх підстанцій. Особливість цієї таблиці в тому, що замість сухих цифр здоров'я (напр. 85%), вона містить вбудовані візуальні прогрес-бари, використовуючи <code>st.column_config.TextColumn</code> та утиліту <code>make_health_bar</code>.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render(df_latest: pd.DataFrame, region_filter: str | None = None) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний метод. 1. Перевіряє чи ми в Kaggle mode (немає колонки <code>health_score</code>). Якщо так, відмальовує лише загальне навантаження. 2. Виконує Failsafe чистку даних (<code>pd.to_numeric(errors='coerce').fillna(0.0)</code>) для уникнення падінь на NaN значеннях. 3. Розраховує KPI (mean/sum). 4. Будує 4 колонки: Здоров'я, Частота, Навантаження та render_gauge(). 5. Фільтрує df_latest за регіоном. 6. Застосовує <code>df_table['Стан (Здоров'я)'] = df_table['health_score'].apply(make_health_bar)</code>. 7. Рендерить <code>st.dataframe</code> з розширеним форматуванням <code>column_config</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Внутрішній Пайплайн Рендерингу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render(df, region_filter)") --> CHK_KAG{"'health_score'\nin df.columns?"}
    
    CHK_KAG -->|No| KAGGLE("Render ONLY total load\nShow Warning")
    CHK_KAG -->|Yes| CLEAN("Cleanse Data\npd.to_numeric(coerce).fillna(0.0)")
    
    CLEAN --> AGG("Calculate avg_health, sum(load)\nextract freq")
    
    AGG --> TOP_ROW("Render 4 Metrics\n[Health, Freq, Load, Gauge]")
    
    TOP_ROW --> FILTER("Filter df by region_filter")
    
    FILTER --> APPLY("Apply make_health_bar() to\ncreate 'Стан' Column")
    
    APPLY --> GRID("Render st.dataframe\nusing column_config formatters")
    
    GRID --> DONE("st.markdown(Spacer 300px)")
    KAGGLE --> DONE
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.components.cards (make_health_bar, render_gauge)</span>
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
