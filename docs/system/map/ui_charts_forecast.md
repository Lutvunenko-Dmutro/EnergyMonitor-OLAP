# Технічна специфікація: Двигун Візуалізації Прогнозів (ADVANCED FORECAST VISUALIZATION ENGINE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">FORECAST VISUALIZATION | HYBRID RENDERING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔮</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Візуалізатор Прогнозів</h1>
            <p class="mega-subtitle">Складний аналітичний двигун для представлення результатів ШІ-прогнозування: гібридний рендеринг історії та майбутнього, візуалізація довірчих інтервалів та багатомодельний аудит точності нейромереж</p>
            <div class="status-tags"><span class="tag tag-online">FORECAST VIZ ACTIVE</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">PREDICTIVE ANALYST</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📉</div><div class="metric-info"><span class="metric-label">Mode</span><span class="metric-value">Hybrid Multi-layer</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Confidence</span><span class="metric-value">RGBA Bond Filling</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Audit</span><span class="metric-value">V1 / V2 / V3 Compare</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Layout</span><span class="metric-value">Mega-Flow Seamless</span></div></div>
</div>

<!-- SECTION 01: FORECAST VISUALIZATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Візуалізації Прогнозів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>forecast_plots.py</code> є "Вікном у майбутнє" проекту ATLAS. В предиктивній аналітиці критично важливо не просто показати лінію прогнозу, а надати контекст. Наша філософія базується на <b>Безперервності Аналізу</b>: ми візуалізуємо перехід від реальної історії до майбутніх значень як єдиний потік (Mega-Flow). Додавання довірчих інтервалів (Confidence Bands) дозволяє оператору оцінити рівень невизначеності ШІ, перетворюючи "сухий" прогноз на інструмент оцінки ризиків при балансуванні енергосистеми.</p>
    </div>
</div>

<!-- SECTION 02: FORECAST PLOTTING PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр побудови прогнозних графіків (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("History + Forecast Dataframes") --> SELECT{"Chart Configuration"}
    
    SELECT -- "Single Model" --> HYBRID("_generate_forecast_figure")
    HYBRID --> HIST_TRACE("Plot History (Solid Blue)")
    HYBRID --> BAND_TRACE("Plot Confidence Band (RGBA Red)")
    HYBRID --> FC_TRACE("Plot Forecast (Dash Red)")
    
    SELECT -- "Audit Mode" --> MULTI("_generate_multi_forecast_figure")
    MULTI --> COMPARE("Plot V1 (Dot), V2 (Dash), V3 (Solid)")
    
    SELECT -- "Mega Hybrid" --> MEGA("_generate_mega_hybrid_figure")
    MEGA --> SEAMLESS("Connect Backtest with Live Forecast")
    
    HIST_TRACE --> RENDER("Final Interactive Plotly Object")
    COMPARE --> RENDER
    SEAMLESS --> RENDER
    </div></div>
</div>

<!-- SECTION 03: HYBRID MULTI-LAYER RENDERING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Гібридний багатошаровий рендеринг</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>_generate_forecast_figure</code> реалізує тришарову структуру візуалізації:</p>
        <ul>
            <li><b>Layer 1 (History):</b> Солідна синя лінія (2.5px), що відображає фактичне навантаження за останні 24-48 годин.</li>
            <li><b>Layer 2 (Confidence):</b> Заливка області <code>upper_bond</code> та <code>lower_bond</code> з використанням <code>rgba(231,76,60,0.08)</code>. Це візуалізує математичну ймовірність відхилення.</li>
            <li><b>Layer 3 (Forecast):</b> Пунктирна червона лінія, що починається точно в точці завершення історії, створюючи ефект "передбачення".</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: FORECAST STYLE & VERSION MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця стилів та версій моделей</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модель</th>
                    <th>Стиль лінії</th>
                    <th>Колір (Hex)</th>
                    <th>Роль в аудиті</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>LSTM Baseline (v1)</td><td>Dot (2px)</td><td>#00cec9</td><td>Еталонна точність</td></tr>
                <tr><td>LSTM Diagnostic (v2)</td><td>Dash (2px)</td><td>#0984e3</td><td>Аналіз аномалій</td></tr>
                <tr><td>LSTM Hybrid (v3)</td><td>Solid (3.5px)</td><td>#d63031</td><td>Фінальний прогноз (Production)</td></tr>
                <tr><td>Ground Truth</td><td>Solid (3px)</td><td>#ff9f43</td><td>Фактичне порівняння</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: COMPARATIVE AUDIT PLOTTING (V1-V3) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Порівняльний аудит нейромереж (v1-v3)</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>generate_comparison_plot</code> дозволяє на одному полотні порівняти точність всіх трьох архітектур LSTM. Ми використовуємо **Диференційовані стилі** для кожної версії: v1 (дрібний пунктир), v2 (широкий пунктир) та v3 (товста суцільна лінія). Це дозволяє оператору візуально підтвердити, що гібридна модель v3 найкраще слідує за формою фактичного навантаження ("Ground Truth"), виправдовуючи її статус основної моделі прогнозування.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Двигуна (Forecast Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION _generate_forecast_figure(history, forecast, label):
    1. INIT: fig = go.Figure()
    
    2. RENDER_HISTORY:
           fig.add_trace(Scatter(x=history.ts, y=history.actual, color='blue'))
           
    3. RENDER_BANDS (Confidence Interval):
           y_area = concat([upper_bond, lower_bond_reverse])
           fig.add_trace(Scatter(x=ts_wrap, y=y_area, fill='toself', alpha=0.08))
           
    4. RENDER_FORECAST:
           fig.add_trace(Scatter(x=forecast.ts, y=forecast.pred, color='red', dash='dash'))
           
    5. STYLE:
           SET template = "plotly_dark"
           SET hovermode = "x unified"
           RETURN fig
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: MEGA-FLOW SEAMLESS VISUALIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Безшовна візуалізація Mega-Flow</h2></div>
    <div class="glass-card flow-step">
        <p>Унікальною функцією <code>_generate_mega_hybrid_figure</code> є об'єднання результатів бектестування (Backtest) та реального прогнозу (Live Forecast) в єдиний графік. Ми використовуємо однакову колірну схему для обох частин прогнозу, але змінюємо стиль лінії з суцільної на пунктирну в точці "Зараз". Це створює інтуїтивне відчуття того, що система продовжує тренд, який вже був успішно перевірений на історичних даних.</p>
    </div>
</div>

<!-- SECTION 08: RGBA ALPHA-BLENDING FOR CONFIDENCE BANDS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">RGBA Alpha-blending для довірчих інтервалів</h2></div>
    <div class="glass-card flow-step">
        <p>Для візуалізації інтервалів невизначеності ми застосовуємо техніку **Polygonal Filling**. Замість двох ліній (Upper/Lower), ми створюємо один замкнений багатокутник. Використання <code>rgba(231,76,60,0.08)</code> гарантує, що "тінь" прогнозу буде ледь помітною, не перекриваючи історію та не захаращуючи графік. Також реалізовано <code>clip</code> логіку для запобігання візуальних артефактів при аномальних викидах ШІ-моделі.</p>
    </div>
</div>

<!-- SECTION 09: INTERACTIVE AUDIT UX (LEGEND SYNC) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Інтерактивний UX Аудиту (Синхронізація легенди)</h2></div>
    <div class="glass-card flow-step">
        <p>Прогнозні графіки в <code>forecast_plots.py</code> розроблені для глибокого дослідження. Ми винесли легенду в горизонтальний блок під графік з <code>xanchor="center"</code>. Це дозволяє оператору легко вмикати/вимикати різні версії прогнозів. Особлива увага приділена тултипам: при наведенні показується не лише значення МВт, а й мітка версії моделі, що дозволяє проводити миттєвий порівняльний аудит у будь-якій часовій точці.</p>
    </div>
</div>

<!-- SECTION 10: LAYOUT & PERFORMANCE (FPS OPTIMIZATION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Макет та продуктивність (FPS Optimization)</h2></div>
    <div class="glass-card flow-step">
        <p>Графіки прогнозу зазвичай мають велику кількість точок (особливо при відображенні 7 днів історії з кроком 5хв). Модуль використовує оптимізовані макети <code>margin(l=10, r=10, t=80, b=100)</code> для максимізації корисної площі візуалізації. Векторизація через Pandas при підготовці координат для <code>fill="toself"</code> забезпечує швидкий рендеринг (менше 100мс) навіть для найскладніших гібридних композицій.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Plotly Graph Objects</h4>
                <p>Основний двигун для побудови складних багатошарових Scatter-діаграм.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">⚙️</div>
            <div class="role-content">
                <h4>Pandas Core</h4>
                <p>Обробка часових рядів, конкатенація та кліпінг довірчих інтервалів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🧠</div>
            <div class="role-content">
                <h4>ML Predictors</h4>
                <p>Провайдери прогнозних значень та інтервалів для візуалізації.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (PROBABILISTIC FAN CHARTS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Probabilistic Fan Charts)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Ймовірнісних Fan-чартів**. Замість одного інтервалу невизначеності ми будемо візуалізувати кілька шарів (наприклад, 50%, 90% та 99% ймовірності) з градієнтною заливкою. Також буде додано підтримку <b>Інтерактивного перепланування</b>: можливість "тягнути" лінію прогнозу мишкою для проведення "What-if" аналізу сценаріїв навантаження.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Візуалізація Прогнозів</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому довірчий інтервал такий широкий?</b> — Це означає, що ШІ-модель має низьку впевненість у прогнозі (можливо, через зміну погодних умов або аномалії в історії).</p>
        <p><b>Як побачити тільки прогноз v3?</b> — Вимкніть інші версії (v1, v2), натиснувши на них у легенді під графіком.</p>
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
