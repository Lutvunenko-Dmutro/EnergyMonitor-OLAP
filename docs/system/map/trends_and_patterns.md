# Технічна специфікація модуля: trends_and_patterns.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CONSUMPTION PATTERNS & FAILURE CORRELATION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔗</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Cascading Failure Analyzer: trends_and_patterns</h1>
            <p class="mega-subtitle">Дослідження циклічних закономірностей та аварійних кореляцій. Асоціативні правила між підстанціями через Counter + combinations. Seaborn Heatmap.</p>
            <div class="status-tags"><span class="tag tag-online">SEABORN HEATMAP</span><span class="tag tag-version">v1.5.0</span><span class="tag tag-role">STANDALONE ANALYTICS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Trends</span><span class="metric-value">Weekly Load by Station</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💥</div><div class="metric-info"><span class="metric-label">Failures</span><span class="metric-value">Pair Correlation Counter</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔥</div><div class="metric-info"><span class="metric-label">Heatmap</span><span class="metric-value">Symmetric NxN Matrix</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💾</div><div class="metric-info"><span class="metric-label">Output</span><span class="metric-value">PNG (savefig)</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>trends_and_patterns.py</b> — це окремий автономний аналітичний скрипт (запускається через <code>if __name__ == "__main__"</code>), не є частиною Streamlit-UI. Він призначений для глибокого оффлайн-аналізу, результатами якого є PNG-файли.</p>
        <p style="margin-top: 12px;">Основна ідея <code>analyze_cascading_failures()</code>: з БД вибираються всі аварії типу 'Перевантаження', групуються по годині. Якщо в одну годину одночасно впало кілька підстанцій — вони вважаються "парою". Пари рахуються через <code>Counter + combinations</code>. Результат: симетрична матриця кореляцій N×N, де N — кількість підстанцій. Візуалізується через <code>sns.heatmap</code> з анотаціями (ціфри в клітинках) та зберігається у <code>heatmap_failures.png</code>.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def analyze_consumption_trends() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>SQL: <code>AVG(actual_load_mw) GROUP BY substation, EXTRACT(WEEK)</code>. Будує лінійний графік (Seaborn lineplot) з групуванням по підстанціях. Зберігає у <code>trends_innovators.png</code>.</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def analyze_cascading_failures() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>SQL: Всі 'Перевантаження' аварії з <code>date_trunc('hour')</code>. Групує по годині → список підстанцій. Для кожного списку з 2+ станцій генерує всі пари через <code>itertools.combinations</code>. Рахує через <code>Counter</code>. Будує симетричну матрицю. Рендерить <code>sns.heatmap(annot=True, cmap="Reds")</code>. Виводить текстовий ТОП-5 пар. Зберігає у <code>heatmap_failures.png</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Аналізу Каскадних Аварій</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("analyze_cascading_failures()") --> SQL("SELECT date_trunc('hour',ts), sub_name\nFROM Alerts WHERE type='Перевантаження'")
    SQL --> GROUP("groupby('alert_time')['sub_name'].apply(list)")
    GROUP --> PAIRS("For basket in baskets:\ncombinations(unique_subs, 2)")
    PAIRS --> COUNT("pair_counts.update(pairs)\nCounter accumulation")
    COUNT --> REPORT("Print TOP-5 pairs")
    REPORT --> MATRIX("Build N×N DataFrame matrix\n(symmetric fill)")
    MATRIX --> HEAT("sns.heatmap(annot=True, fmt='d'\ncmap='Reds')")
    HEAT --> SAVE("plt.savefig('heatmap_failures.png')")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging, os, contextlib</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>collections.Counter</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>itertools.combinations</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>matplotlib.pyplot (plt)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>psycopg2</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>seaborn (sns.heatmap)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>dotenv (load_dotenv)</span>
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
