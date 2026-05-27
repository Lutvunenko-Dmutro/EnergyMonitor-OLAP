# Технічна специфікація модуля: clustering_view.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CLUSTERING VISUALIZATION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">👁️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">UI View: clustering_view</h1>
            <p class="mega-subtitle">Графічне представлення результатів AI-сегментації (K-Means). Забезпечує миттєве виявлення аномальних та перевантажених об'єктів через Multidimensional Scatter Plots.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY EXPRESS</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">ANALYTICS UI</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📐</div><div class="metric-info"><span class="metric-label">Plot Type</span><span class="metric-value">px.scatter (2D)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Color Coding</span><span class="metric-value">Risk Status Zoning</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📏</div><div class="metric-info"><span class="metric-label">Scaling</span><span class="metric-value">Logarithmic Toggle</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📋</div><div class="metric-info"><span class="metric-label">Stats</span><span class="metric-value">Top 5 Loaded</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>clustering_view.py</b> є UI-обгорткою для ML-движка <code>cluster_substations</code>. Його мета — зробити результати роботи K-Means зрозумілими для диспетчера без технічного бекграунду.</p>
        <p style="margin-top: 12px;">Він будує інтерактивну діаграму розсіювання (Scatter Plot), де кожна точка — це підстанція. Осі показують середнє та пікове навантаження, розмір точки — температуру, а колір відповідає кластеру ризику. Окрім графіка, модуль генерує текстову статистику: підраховує кількість підстанцій у кожній зоні та виводить "Топ-5" найважчих об'єктів.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_clustering_segment(df: pd.DataFrame, use_log: bool, selected_substation: str) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Оркестратор інтерфейсу кластеризації. Викликає ML-метод <code>cluster_substations(df, n_clusters=3)</code>. Розділяє екран на дві колонки: графік (3/4 ширини) та статистика (1/4 ширини). Будує <code>px.scatter</code> з підтримкою логарифмічних шкал (<code>log_x</code>, <code>log_y</code>). В колонці статистики виводить <code>value_counts()</code> по статусах та відсортований датафрейм (Top-5 <code>avg_load</code>).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема рендерингу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render_clustering_segment(df)") --> ML("cluster_substations(df)\n[K-Means Engine]")
    
    ML --> COLS("st.columns([3, 1])")
    
    COLS --> CHART["Column 1: Chart"]
    COLS --> STATS["Column 2: Stats"]
    
    CHART --> PX("px.scatter()\ncolor='Status'\nsize='avg_temp'\nlog_scale=use_log")
    PX --> PLOT("safe_plotly_render()")
    
    STATS --> CNT("df['Status'].value_counts()")
    CNT --> ST_WARN("st.error / st.warning / st.success\n(Based on Risk Level)")
    
    STATS --> TOP("df.sort_values('avg_load').head(5)")
    TOP --> ST_DF("st.dataframe(Top-5)")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.express</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.analytics.clustering (cluster_substations)</span>
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
