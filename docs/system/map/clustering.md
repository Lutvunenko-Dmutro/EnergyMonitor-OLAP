# Технічна специфікація модуля: clustering.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ML CLUSTERING ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧩</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Pattern Recognition: clustering</h1>
            <p class="mega-subtitle">Інтелектуальна сегментація енергооб'єктів. Використовує некероване машинне навчання (K-Means) для виявлення патернів навантаження та ризиків.</p>
            <div class="status-tags"><span class="tag tag-online">SCIKIT-LEARN ENGINE</span><span class="tag tag-version">v2.3.0</span><span class="tag tag-role">ML PROFILER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🤖</div><div class="metric-info"><span class="metric-label">Algorithm</span><span class="metric-value">K-Means Clustering</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Profiling</span><span class="metric-value">Load & Temperature</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔴</div><div class="metric-info"><span class="metric-label">Ranking</span><span class="metric-value">Risk Status Zoning</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📐</div><div class="metric-info"><span class="metric-label">Scaling</span><span class="metric-value">StandardScaler</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>clustering.py</b> відповідає за автоматичне групування підстанцій за рівнем їх завантаженості (Risk Ranking). Використовує алгоритм <code>K-Means</code> з бібліотеки Scikit-Learn.</p>
        <p style="margin-top: 12px;">Замість жорстких порогових значень, алгоритм динамічно розбиває об'єкти на 3 кластери (Низьке навантаження, Штатний режим, Високе навантаження) на основі середнього (avg_load), пікового (max_load) навантаження та температури. Перед кластеризацією обов'язково застосовується <code>StandardScaler</code> для нормалізації шкал.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def cluster_substations(df: pd.DataFrame, n_clusters: int = 3) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний метод. Приймає DataFrame з історією навантажень. Відфільтровує агрегаційний вузол "AEP Region". Групує дані по підстанціях, обчислюючи <code>mean</code> та <code>max</code> навантаження. Нормалізує фічі через <code>StandardScaler</code>. Запускає <code>KMeans</code>. Ранжує отримані кластери за середнім навантаженням і мапить їх на текстові статуси (🔴 Високе, 🟡 Штатне, 🟢 Низьке). Повертає згрупований DF з колонками <code>cluster_id</code> та <code>Status</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема Кластеризації</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN(Raw DataFrame) --> GRP("Group By 'substation_name'\nAgg: mean, max")
    
    GRP --> FEAT("Extract Features:\navg_load, max_load, avg_temp")
    
    FEAT --> SCALER("StandardScaler()\nFit & Transform")
    
    SCALER --> KM("KMeans(n_clusters=3)\nfit_predict")
    
    KM --> RANK("Sort Clusters by avg_load\n(0 -> Min, 2 -> Max)")
    
    RANK --> MAP("Map Labels:\n2 = 🔴 High Risk\n1 = 🟡 Normal\n0 = 🟢 Low Risk")
    
    MAP --> OUT(DataFrame with 'Status' Column)
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sklearn.cluster.KMeans</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sklearn.preprocessing.StandardScaler</span>
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
