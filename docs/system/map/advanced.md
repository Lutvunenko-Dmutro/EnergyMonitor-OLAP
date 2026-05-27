# Технічна специфікація модуля: advanced.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ADVANCED AI ANALYTICS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧩</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">UI View: Advanced Analytics</h1>
            <p class="mega-subtitle">Диспетчер поглибленої аналітики. Розподіляє обчислювально важкі завдання (кластеризацію та декомпозицію трендів) по ізольованих Streamlit-фрагментах для забезпечення плавності інтерфейсу.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY / AI VIEW</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">UI DISPATCHER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Performance</span><span class="metric-value">st.fragment Isolated</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Clustering</span><span class="metric-value">Load Profiles Segments</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Trends</span><span class="metric-value">Decomposition (STL)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Config</span><span class="metric-value">Log / Relative Scales</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>advanced.py</b> є головним оркестратором розділу "Поглиблена аналітика". Оскільки алгоритми машинного навчання (особливо декомпозиція часових рядів) є важкими для рендерингу, модуль використовує декоратор <code>@st.fragment</code>.</p>
        <p style="margin-top: 12px;">Це архітектурне рішення означає, що перемикання тумблерів ("Логарифмічна шкала" або "Відносне навантаження") всередині конкретної вкладки перемальовує <i>лише цю вкладку</i>, а не весь додаток, зберігаючи високу чуйність UI навіть на великих датасетах.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_advanced_analysis(df: pd.DataFrame, selected_substation: str) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Точка входу View. Перевіряє наявність базових колонок (<code>substation_name, actual_load_mw, timestamp</code>). Створює вкладки <code>st.tabs</code> і диспетчеризує виклики до відповідних фрагментів.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@st.fragment<br>def fragment_advanced_tab1(df, selected_substation, active=False)</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Ізольований UI-контекст для "Кластеризації". Додає кнопку-поповер (Popover) для ввімкнення логарифмічної шкали. Делегує важкий рендеринг у <code>render_clustering_segment()</code>.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@st.fragment<br>def fragment_advanced_tab2(df, selected_substation, active=False)</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Ізольований UI-контекст для "Аналізу трендів". Додає тумблер відносного навантаження (%). Делегує побудову STL-декомпозиції у <code>render_trend_decomposition()</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Архітектура фрагментації (Streamlit)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    MAIN("render_advanced_analysis(df, sub)") --> CHECK{"Valid cols & Data?"}
    CHECK -->|No| ERR("st.error / st.warning")
    
    CHECK -->|Yes| TABS("st.tabs(['Clustering', 'Trends'])")
    
    TABS --> TAB1("Tab 1")
    TABS --> TAB2("Tab 2")
    
    subgraph "Fragment 1 (Isolated State)"
        TAB1 --> FRAG1("@st.fragment_advanced_tab1")
        FRAG1 --> TOGGLE1("Toggle: Log Scale")
        TOGGLE1 --> COMP1("render_clustering_segment()")
    end
    
    subgraph "Fragment 2 (Isolated State)"
        TAB2 --> FRAG2("@st.fragment_advanced_tab2")
        FRAG2 --> TOGGLE2("Toggle: Relative %")
        TOGGLE2 --> COMP2("render_trend_decomposition()")
    end
    
    %% Note on partial rerender
    FRAG1 -.->|Rerender ONLY this node\non Toggle| FRAG1
    FRAG2 -.->|Rerender ONLY this node\non Toggle| FRAG2
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.views.advanced_components.clustering_view</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.views.advanced_components.trend_view</span>
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
