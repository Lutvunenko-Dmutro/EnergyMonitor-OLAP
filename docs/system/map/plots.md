# Технічна специфікація модуля: plots.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">LEGACY UTILITY SCRIPT</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📉</span><div class="pulse-ring" style="border-color: rgba(255,165,2,0.3);"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Matplotlib Utils: plots</h1>
            <p class="mega-subtitle">Проста утиліта на базі Matplotlib для швидкого відмальовування та збереження статичних PNG-графіків під час тренування моделей.</p>
            <div class="status-tags"><span class="tag tag-online" style="background: rgba(255,165,2,0.1); color: #ffa502;">LEGACY / OFFLINE</span><span class="tag tag-version">v0.5.0</span><span class="tag tag-role">TRAINING UTIL</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Backend</span><span class="metric-value">Matplotlib</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🖼️</div><div class="metric-info"><span class="metric-label">Output</span><span class="metric-value">Static Image (.png)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Interactivity</span><span class="metric-value">None</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚠️</div><div class="metric-info"><span class="metric-label">Status</span><span class="metric-value">Deprecated in UI</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>plots.py</b> є спадковою (legacy) утилітою, яка використовувалась на ранніх етапах розробки (або зараз використовується виключно в Jupyter Notebooks чи CLI-скриптах тренування) для швидкої перевірки результатів "факт vs прогноз".</p>
        <p style="margin-top: 12px;">На відміну від сучасних інтерактивних компонентів (<code>forecast_plots.py</code>, що базуються на Plotly), ця утиліта створює звичайні "плоскі" графіки без можливості наведення (hover) чи масштабування, але вміє автоматично зберігати їх у файли на диск.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def plot_forecast(actual: pd.Series, predicted: pd.Series, title: str = "Forecast", save_path: str = None) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Ініціалізує полотно фіксованого розміру (12x6). Накладає дві криві: Actual та Predicted. Додає базову легенду та заголовок. Якщо вказано <code>save_path</code>, зберігає графік за вказаним шляхом і закриває фігуру для вивільнення пам'яті (<code>plt.close()</code>).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема рендерингу (Matplotlib)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("actual_series, predicted_series") --> INIT("plt.figure(figsize=(12, 6))")
    
    INIT --> PLOT_A("plt.plot(actual, label='Actual')")
    PLOT_A --> PLOT_P("plt.plot(predicted, label='Predicted')")
    
    PLOT_P --> DECO("plt.title()\nplt.legend()")
    
    DECO --> CHECK_SAVE{"save_path\nprovided?"}
    
    CHECK_SAVE -->|Yes| SAVE("plt.savefig(save_path)")
    CHECK_SAVE -->|No| SKIP("Skip save")
    
    SAVE --> CLOSE("plt.close()")
    SKIP --> CLOSE
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>matplotlib.pyplot</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os</span>
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
