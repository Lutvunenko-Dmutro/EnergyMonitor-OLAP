# Технічна специфікація модуля: analytics_advanced.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">TREND & ASSOCIATION RULE ANALYSIS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🕸️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Structural Analytics: analytics_advanced</h1>
            <p class="mega-subtitle">Автономний аналітичний сервіс (Data Mining Script). Призначений для виявлення прихованих структурних зв'язків: довгострокових трендів споживання та каскадних ризиків у мережі.</p>
            <div class="status-tags"><span class="tag tag-online">DATA MINING</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">OFFLINE ANALYTICS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Trends</span><span class="metric-value">Weekly Aggregation</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔗</div><div class="metric-info"><span class="metric-label">Association</span><span class="metric-value">Frequent Patterns</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚠️</div><div class="metric-info"><span class="metric-label">Risk Focus</span><span class="metric-value">Cascade Failures</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🖼️</div><div class="metric-info"><span class="metric-label">Output</span><span class="metric-value">Seaborn / Console</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>analytics_advanced.py</b> — це скрипт для офлайн-аналізу (Data Mining). На відміну від дашбордів реального часу, він призначений для періодичного запуску з метою стратегічного планування.</p>
        <p style="margin-top: 12px;">Він вирішує дві задачі: по-перше, виявляє <i>"Early Adopters"</i> (підстанції з аномально зростаючим трендом споживання тиждень до тижня). По-друге, використовує комбінаторний аналіз (Frequent Pattern Mining) для пошуку пар підстанцій, які часто падають одночасно, що свідчить про наявність <b>каскадних вразливостей</b> у топології мережі.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def analyze_trends() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Аналіз тижневих трендів. Виконує SQL-запит з групуванням <code>EXTRACT(WEEK FROM timestamp)</code>. Збирає агреговані значення середнього навантаження і будує лінійний графік за допомогою Seaborn (<code>sns.lineplot</code>). Зберігає результат як <code>trends_innovators.png</code>.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def analyze_association_rules() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Аналіз каскадних аварій (Market Basket Analysis для інцидентів). Витягує з БД усі аварії типу "Перевантаження", групує їх по годинах (бакети/baskets). За допомогою <code>itertools.combinations</code> та <code>collections.Counter</code> підраховує частоту появи пар підстанцій в межах однієї години. Виводить ТОП-5 найтісніше пов'язаних пар у лог.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема комбінаторного аналізу (Association Rules)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DB[(PostgreSQL\nTable: Alerts)] --> |SELECT date_trunc('hour')| SQL_GRP("Grouping\nby Hour (Baskets)")
    
    SQL_GRP --> B1["Hour 1: [Sub_A, Sub_B]"]
    SQL_GRP --> B2["Hour 2: [Sub_A, Sub_C, Sub_B]"]
    SQL_GRP --> B3["Hour 3: [Sub_C]"]
    
    B1 --> COMB("itertools.combinations\n(size=2)")
    B2 --> COMB
    B3 --> COMB
    
    COMB --> C1("(Sub_A, Sub_B) +1")
    COMB --> C2("(Sub_A, Sub_C) +1")
    COMB --> C3("(Sub_B, Sub_C) +1")
    
    C1 --> COUNT("collections.Counter")
    C2 --> COUNT
    C3 --> COUNT
    
    COUNT --> TOP("most_common(5)")
    TOP --> LOG("Logger:\nTOP-5 Cascade Risks")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>collections (Counter)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>itertools (combinations)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>matplotlib.pyplot</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>seaborn</span>
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
