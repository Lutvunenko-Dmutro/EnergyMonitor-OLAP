# Технічна специфікація модуля: academic.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ACADEMIC RESEARCH VISUALIZATION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎓</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Thesis Charts: academic</h1>
            <p class="mega-subtitle">Візуалізатор академічної звітності. Реалізує спеціалізовані графіки (Trend, Distribution, Scatter) зі строгим форматуванням для наукового обґрунтування точності нейромереж у дипломній роботі.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY COMPONENT</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">THESIS EXPORT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Fig. 5</span><span class="metric-value">Temporal Tracking</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Fig. 7</span><span class="metric-value">Error Density (PDF)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔵</div><div class="metric-info"><span class="metric-label">Fig. 8</span><span class="metric-value">Regression Scatter</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">Support</span><span class="metric-value">Multi-Model Compare</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>academic.py</b> створений спеціально для генерації "красивих" та науково достовірних графіків, готових для вставки у дипломну роботу (Thesis-ready Formatting). На відміну від звичайних UI-графіків, ці візуалізації мають строгу нумерацію (Figure 5, 7, 8) та академічні підписи осей.</p>
        <p style="margin-top: 12px;">Унікальна особливість модуля — вбудована підтримка <b>мультимодельного порівняння</b>. Якщо передати словник з прогнозами різних версій моделей (V1, V2, V3), модуль автоматично побудує графіки, де на одному полотні можна порівняти щільність помилок (PDF) та тренди різних архітектур, використовуючи заздалегідь визначену колірну палітру.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def generate_academic_plots(data: Union[pd.DataFrame, dict], substation_name="Selected Object") → Tuple[go.Figure, go.Figure, go.Figure]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Єдина точка входу модуля. Повертає кортеж із 3-х фігур Plotly. Приймає або один DataFrame (для режиму однієї моделі), або словник <code>{"v1": df1, "v2": df2}</code> (для порівняльного режиму). Використовує бібліотеку <code>scipy.stats</code> для розрахунку функції щільності ймовірності (PDF) нормального розподілу при побудові гістограми помилок.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: VISUALIZATIONS GENERATED -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Математична база графіків</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th style="padding: 8px; text-align: left;">Фігура</th>
                    <th style="padding: 8px; text-align: left;">Опис та Логіка</th>
                    <th style="padding: 8px; text-align: left;">Plotly Traces</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px; font-weight: 600;">Figure 5</td>
                    <td style="padding: 8px;"><b>Temporal Load Dynamics:</b> Візуалізує Ground Truth суцільною лінією (#ff9f43), а прогнози нейромереж пунктиром.</td>
                    <td style="padding: 8px;"><code>go.Scatter(mode='lines')</code></td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px; font-weight: 600;">Figure 7</td>
                    <td style="padding: 8px;"><b>Statistical Error Analysis:</b> Вираховує помилку <code>err = actual - predicted</code>. Будує нормовану гістограму та лінію PDF Гауса.</td>
                    <td style="padding: 8px;"><code>go.Histogram(histnorm)</code> + <code>go.Scatter(scipy.stats.norm)</code></td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px; font-weight: 600;">Figure 8</td>
                    <td style="padding: 8px;"><b>Neural Regression Correlation:</b> Діаграма розсіювання, що показує відхилення точок від ідеальної лінії <code>y = x</code>.</td>
                    <td style="padding: 8px;"><code>go.Scatter(mode='lines', y=x)</code> + <code>go.Scatter(mode='markers')</code></td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.graph_objects</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>numpy</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>scipy.stats (inline)</span>
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
