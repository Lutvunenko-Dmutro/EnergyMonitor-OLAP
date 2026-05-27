# Технічна специфікація модуля: trend_view.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">TREND & SEASONALITY ANALYSIS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Time-Series Decomposer: trend_view</h1>
            <p class="mega-subtitle">Розбиває сигнал навантаження на компоненти: Тренд, Сезонність та Залишок. Statsmodels seasonal_decompose з 24-годинним вікном. Facet Row Plotly.</p>
            <div class="status-tags"><span class="tag tag-online">STATSMODELS</span><span class="tag tag-version">v1.0.0</span><span class="tag tag-role">DECOMPOSITION</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📐</div><div class="metric-info"><span class="metric-label">Model</span><span class="metric-value">Additive (period=24)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔢</div><div class="metric-info"><span class="metric-label">Min Data</span><span class="metric-value">> 48 годин</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌐</div><div class="metric-info"><span class="metric-label">Scope</span><span class="metric-value">Individual or Aggregate</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Chart</span><span class="metric-value">px.line facet_row</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>trend_view.py</b> відповідає на питання: <i>"Чи є в енергоспоживанні довгостроковий тренд зростання, або це просто річна сезонність?"</i>. Це принципово важливо для планування нових підстанцій.</p>
        <p style="margin-top: 12px;">Використовується класична адитивна декомпозиція (<code>seasonal_decompose(model="additive", period=24)</code>). Перш ніж передати дані до алгоритму, модуль виконує <b>Data Conditioning</b>: дедублює індекс, ресемплює до погодинної частоти (<code>resample("h").mean()</code>) та заповнює прогалини методом Forward Fill. Якщо обрано "Усі підстанції", дані попередньо агрегуються через <code>groupby("timestamp").agg(sum)</code>. Результат представлено у 3-рядковому Facet Plotly графіку.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_trend_decomposition(df, selected_substation, use_rel) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>1. Визначає режим: агрегований чи поодинока підстанція. 2. Фільтрує або агрегує <code>df</code>. 3. Перевіряє <code>len > 48</code> (мінімум для розкладу). 4. Конвертує індекс, дедублює, ресемплює. 5. Якщо <code>use_rel=True</code> — нормалізує до 0-100%. 6. Викликає <code>seasonal_decompose()</code> та перетворює на <code>df.melt()</code>. 7. Будує <code>px.line(facet_row="Компонент")</code>. 8. Передає через <code>safe_plotly_render()</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Часової Декомпозиції</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render_trend_decomposition(df, sub, use_rel)") --> MODE{"use_aggregate?"}
    
    MODE -->|Yes| AGG("groupby('timestamp').agg(sum)")
    MODE -->|No| FILTER("df[df['substation_name'] == sub]")
    
    AGG --> CHK_LEN{"len > 48?"}
    FILTER --> CHK_LEN
    
    CHK_LEN -->|No| WARN("st.info('Недостатньо даних')")
    CHK_LEN -->|Yes| COND("set_index('timestamp')\nDeduplicate index\nresample('h').mean().ffill()")
    
    COND --> REL{"use_rel?"}
    REL -->|Yes| NORM("/ max * 100")
    REL -->|No| DECOMP("seasonal_decompose\n(additive, period=24)")
    NORM --> DECOMP
    
    DECOMP --> MELT("pd.DataFrame → melt\n(Тренд, Сезонність, Залишок)")
    MELT --> CHART("px.line(facet_row='Компонент')")
    CHART --> RENDER("safe_plotly_render(fig)")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.express (px)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>statsmodels.tsa.seasonal (seasonal_decompose)</span>
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
