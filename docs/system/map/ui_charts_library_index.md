# Технічна специфікація: Бібліотека Візуальних Компонентів (CHARTS LIBRARY DISPATCHER)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">VISUAL DISPATCHER | COMPONENT HUB</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏗️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Диспетчер Графіків</h1>
            <p class="mega-subtitle">Центральний хаб візуалізації проєкту ATLAS: ініціалізація та ре-експорт аналітичних модулів, забезпечення зворотної сумісності та уніфікований інтерфейс для базових, прогнозних та академічних графіків</p>
            <div class="status-tags"><span class="tag tag-online">LIBRARY HUB ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">VISUAL ARCHITECT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Pattern</span><span class="metric-value">Facade Dispatcher</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Exposed</span><span class="metric-value">8+ Chart Types</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Legacy</span><span class="metric-value">Backward Compatible</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Import</span><span class="metric-value">Clean Module API</span></div></div>
</div>

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Диспетчера Візуалізації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>charts/__init__.py</code> є "Точкою входу" (Gateway) у світ візуалізації проєкту ATLAS. В складних архітектурах важливо приховати складність реалізації від кінцевого розробника інтерфейсу. Наша філософія базується на <b>Уніфікованому Доступі</b>: замість імпорту з десяти різних файлів, представлення (Views) звертаються до єдиного хаба. Це не лише спрощує код, а й дозволяє централізовано керувати версіями графіків, впроваджувати глобальні стилі та забезпечувати стабільність рендерингу в масштабах всього додатку.</p>
    </div>
</div>

<!-- SECTION 02: FACADE MATHEMATICAL ABSTRACT MODEL -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математична модель та паттерн Фасад</h2></div>
    <div class="glass-card flow-step">
        <p>Диспетчер приховує складність внутрішніх підсистем візуалізації за допомогою оператора Фасаду $\mathbf{\Phi}_{\text{facade}}$:</p>
        $$\mathbf{\Phi}_{\text{facade}}: \sum_{k \in \text{Libraries}} \mathbf{Lib}_k \longrightarrow \text{Unified Public API}$$
        <p>Кожна експортована функція візуалізації приводиться до суворого математичного та програмного контракту:</p>
        $$\mathbf{Figure} = f(\mathbf{DataFrame}, \mathbf{Config}_{\text{axes}}, \mathbf{Theme}_{\text{dark}})$$
        <p>Це дозволяє повністю відокремити внутрішні алгоритми побудови довірчих інтервалів чи щільностей розподілу помилок відStreamlit-представлень сторінок. Заміна бібліотеки рендерингу (наприклад, з Plotly на Bokeh або WebGL примітиви) відбувається локально всередині субмодулів без потреби рефакторингу логіки вкладки.</p>
    </div>
</div>

<!-- SECTION 03: LIBRARY EXPOSURE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема експозиції бібліотеки (Architecture Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    VIEW("UI View (e.g., forecast.py, academic_view.md)") --> HUB("Charts Hub (charts/__init__.py)")
    
    HUB --> BASE("base.py: Dual-Axis & Rhythm Charts")
    HUB --> FC("forecast_plots.py: Hybrid & Multi-Model Curves")
    HUB --> ACAD("academic.py: Normal Fit Error & OLS Regression")
    
    HUB --> LEGACY("Legacy: render_forecast_chart fallback")
    
    BASE --> EXPORT("Unified API Export Namespace")
    FC --> EXPORT
    ACAD --> EXPORT
    LEGACY --> EXPORT
    
    EXPORT --> RENDER("Final Streamlit Dashboard Render")
    </div></div>
</div>

<!-- SECTION 04: CORE DISPATCHER MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця диспетчеризації компонентів</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Категорія</th>
                    <th>Експортовані функції API</th>
                    <th>Оригінальний модуль-провайдер</th>
                    <th>Діагностична цінність</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>General Analytics</b></td><td><code>render_dual_axis_chart</code>, <code>render_rhythm_chart</code></td><td><code>base.py</code></td><td>Співвідношення навантаження з погодою, аналіз ритміки споживання Будні/Вихідні</td></tr>
                <tr><td><b>AI Forecasting</b></td><td><code>_generate_forecast_figure</code>, <code>_generate_multi_forecast_figure</code>, <code>_generate_mega_hybrid_figure</code>, <code>generate_comparison_plot</code></td><td><code>forecast_plots.py</code></td><td>Гібридне ШІ-прогнозування, порівняння точності LSTM-моделей та ARIMA</td></tr>
                <tr><td><b>Academic Thesis</b></td><td><code>generate_academic_plots</code></td><td><code>academic.py</code></td><td>Апроксимація розподілу похибок прогнозу, побудова графіків для дисертації</td></tr>
                <tr><td><b>Legacy Operations</b></td><td><code>render_forecast_chart</code></td><td><code>__init__.py</code> (Native fallback)</td><td>Зворотна сумісність для швидкого малювання лінійних трендів без кастомізації</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: BACKWARD COMPATIBILITY (LEGACY WRAPPERS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Зворотна сумісність (Legacy Fallbacks)</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>charts/__init__.py</code> збережено нативну реалізацію <code>render_forecast_chart</code>. Це критично для підтримки старих частин коду та швидких прототипів. На відміну від складних гібридних графіків, ця функція використовує <code>plotly.express</code> для миттєвої побудови лінійних трендів без глибокої кастомізації. Це дозволяє розробнику вибрати між "швидким та простим" відображенням та "глибоким аналітичним" рендерингом залежно від завдання.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Диспетчера (Charts API Hub)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>PACKAGE src.ui.components.charts:
    1. // [CLEAN FACADE RE-EXPORTS]
       IMPORT render_dual_axis_chart, render_rhythm_chart FROM .base
       IMPORT generate_comparison_plot FROM .forecast_plots
       IMPORT generate_academic_plots FROM .academic
       
    2. // [LEGACY BACKWARD COMPATIBLE FALLBACK IMPLEMENTATION]
       FUNCTION render_forecast_chart(df_merged, sub_label):
           IMPORT plotly.express as px
           
           // Color map for immediate visual differentiation
           color_map = {"Історія": "#3b82f6", "Прогноз": "#ef4444"}
           
           fig = px.line(
               df_merged, x="timestamp", y="actual_load_mw", color="type",
               color_discrete_map=color_map, title=f"📈 {sub_label}"
           )
           
           // Apply uniform dark themed configuration
           fig.update_layout(
               template="plotly_dark",
               height=320,
               margin=dict(l=10, r=10, t=40, b=10)
           )
           RETURN fig
END PACKAGE</code></pre>
    </div>
</div>

<!-- SECTION 07: GLOBAL STYLE SYNCHRONIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Глобальна синхронізація стилів</h2></div>
    <div class="glass-card flow-step">
        <p>Диспетчер гарантує, що всі графіки, незалежно від їх походження (Base або Academic), використовують єдиний <b>Dark Theme Layout</b>. У функціях ре-експорту примусово встановлюються параметри <code>template="plotly_dark"</code> та компактні відступи (Margins). Це запобігає ситуаціям, коли різні графіки на одній сторінці виглядають розрізнено, створюючи цілісний "заводський" вигляд професійного софту для енергетиків.</p>
    </div>
</div>

<!-- SECTION 08: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4><a href="ui_charts_base.md">charts/base.py</a></h4>
                <p>Базові аналітичні графіки (Dual-Axis Y, Rhythm profiles).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🔮</div>
            <div class="role-content">
                <h4><a href="ui_charts_forecast.md">charts/forecast_plots.py</a></h4>
                <p>Ші-прогнозні графіки (Confidence Bands, Multi-model, Mega Hybrid).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🎓</div>
            <div class="role-content">
                <h4><a href="ui_charts_academic.md">charts/academic.py</a></h4>
                <p>Академічні наукові графіки (Normal Fit, OLS Regression, Error Density).</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 09: ROADMAP TO v3.0 (PLUGGABLE DYNAMIC CHARTS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Дорожня карта v3.0 (Dynamic Pluggable Charts)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 заплановано:</p>
        <ul>
            <li><b>Dynamic Sub-package Discovery:</b> Автоматична реєстрація нових файлів з папки <code>charts/</code> через рефлексію простору імен, що дозволить розширювати бібліотеку без редагування <code>__init__.py</code>.</li>
            <li><b>Plotly WebGL Autoconfig:</b> Автоматичне перемикання рендерингу великих датасетів (&gt;100 000 точок) на WebGL (<code>go.Scattergl</code>) для підтримки FPS.</li>
            <li><b>Interactive Color Themes:</b> Зв'язування легенд Plotly з глобальними пресетами CSS-тем з <code>styles.py</code> для автоматичного перефарбування кривих при зміні теми користувачем.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">FAQ: Технічні відповіді</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Чому краще імпортувати графіки через хаб-диспетчер?</b><br>
        A: Це гарантує, що ви отримуєте стабільне API з підключеними глобальними стилями темної теми, мінімальними відступами та безпечним рендерингом, усуваючи дублювання коду імпортів.</p>
        <p><b>Q: Як працює зворотна сумісність у Legacy функції?</b><br>
        A: Функція <code>render_forecast_chart</code> приймає два параметри (DataFrame та підпис). Якщо стара версія коду викличе цю функцію, вона миттєво побудує лінійний графік Plotly Express, пофарбує історію в синій, а прогноз — в червоний, і поверне об'єкт фігури без жодних збоїв сумісності.</p>
        <p><b>Q: Чому Plotly є пріоритетним вибором перед Matplotlib?</b><br>
        A: Plotly будує повністю інтерактивні векторні SVG/HTML графіки. Користувач може зумувати ділянки, ізолювати окремі лінії кліком по легенді та бачити HUD-тултипи при наведенні, що критично для диспетчерського моніторингу і неможливо зробити у статичному Matplotlib.</p>
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
