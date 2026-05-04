# Технічна специфікація: Бібліотека Візуальних Компонентів (CHARTS LIBRARY DISPATCHER)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">VISUAL DISPATCHER | COMPONENT HUB</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏗️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Диспетчер Графіків</h1>
            <p class="mega-subtitle">Центральний хаб візуалізації проекту ATLAS: ініціалізація та ре-експорт аналітичних модулів, забезпечення зворотньої сумісності та уніфікований інтерфейс для базових, прогнозних та академічних графіків</p>
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

<!-- SECTION 01: CHARTS LIBRARY PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Диспетчера Візуалізації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>charts/__init__.py</code> є "Точкою входу" (Gateway) у світ візуалізації проекту ATLAS. В складних архітектурах важливо приховати складність реалізації від кінцевого розробника інтерфейсу. Наша філософія базується на <b>Уніфікованому Доступі</b>: замість імпорту з десяти різних файлів, представлення (Views) звертаються до єдиного хаба. Це не лише спрощує код, а й дозволяє централізовано керувати версіями графіків, впроваджувати глобальні стилі та забезпечувати стабільність рендерингу в масштабах всього додатку.</p>
    </div>
</div>

<!-- SECTION 02: LIBRARY EXPOSURE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема експозиції бібліотеки (Architecture Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    VIEW("UI View (e.g., forecast.py)") --> HUB("Charts Hub (__init__.py)")
    
    HUB --> BASE("base.py: Dual-Axis & Rhythm")
    HUB --> FC("forecast_plots.py: Hybrid & Multi-Model")
    HUB --> ACAD("academic.py: Error Stats & Regression")
    
    HUB --> LEGACY("Legacy: render_forecast_chart")
    
    BASE --> EXPORT("Unified API Export")
    FC --> EXPORT
    ACAD --> EXPORT
    LEGACY --> EXPORT
    
    EXPORT --> RENDER("Final Streamlit Dashboard")
    </div></div>
</div>

<!-- SECTION 03: UNIFIED INTERFACE & FACADE PATTERN -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Уніфікований інтерфейс та патерн Фасад</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль реалізує архітектурний патерн <b>Facade</b>. Це дозволяє розробнику:</p>
        <ul>
            <li><b>Simplify Imports:</b> Використовувати лаконічні виклики на кшталт <code>from src.ui.components import charts</code>.</li>
            <li><b>Internal Abstraction:</b> Змінювати реалізацію графіків (наприклад, переходити з Plotly на WebGL) без необхідності змінювати код у всіх вкладках дашборду.</li>
            <li><b>Controlled Visibility:</b> Експортувати тільки стабільні та протестовані функції, приховуючи внутрішні утиліти та допоміжні алгоритми.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: CORE DISPATCHER MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця диспетчеризації компонентів</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Категорія</th>
                    <th>Експортовані функції</th>
                    <th>Цільовий модуль</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>General Analytics</td><td>render_dual_axis_chart, render_rhythm_chart</td><td>base.py</td></tr>
                <tr><td>AI Forecasting</td><td>generate_comparison_plot, _generate_forecast...</td><td>forecast_plots.py</td></tr>
                <tr><td>Academic Thesis</td><td>generate_academic_plots</td><td>academic.py</td></tr>
                <tr><td>Legacy Ops</td><td>render_forecast_chart</td><td>__init__.py (Native)</td></tr>
                <tr><td>Validation</td><td>Safe Rendering Wrappers</td><td>utils/ui_helpers.py</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: BACKWARD COMPATIBILITY (LEGACY WRAPPERS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Зворотня сумісність (Legacy Wrappers)</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>charts/__init__.py</code> збережено нативну реалізацію <code>render_forecast_chart</code>. Це критично для підтримки старих частин коду та швидких прототипів. На відміну від складних гібридних графіків, ця функція використовує <code>plotly.express</code> для миттєвої побудови лінійних трендів без глибокої кастомізації. Це дозволяє розробнику вибрати між "швидким та простим" відображенням та "глибоким аналітичним" рендерингом залежно від завдання.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Диспетчера (Hub Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>MODULE src.ui.components.charts:
    1. IMPORT_AND_REEXPORT:
           FROM .base IMPORT *
           FROM .forecast_plots IMPORT *
           FROM .academic IMPORT *
           
    2. LEGACY_FALLBACK:
           FUNCTION render_forecast_chart(data, label):
               # Fast Plotly Express Implementation
               fig = px.line(data, title=label)
               fig.update_layout(template="plotly_dark")
               RETURN fig
               
    3. INTERFACE_SYNC:
           Ensure all exported functions accept (DataFrame, Title) pattern
END MODULE</code></pre>
    </div>
</div>

<!-- SECTION 07: GLOBAL STYLE SYNCHRONIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Глобальна синхронізація стилів</h2></div>
    <div class="glass-card flow-step">
        <p>Диспетчер гарантує, що всі графіки, незалежно від їх походження (Base або Academic), використовують єдиний <b>Dark Theme Layout</b>. У функціях ре-експорту примусово встановлюються параметри <code>template="plotly_dark"</code> та компактні відступи (Margins). Це запобігає ситуаціям, коли різні графіки на одній сторінці виглядають розрізнено, створюючи цілісний "заводський" вигляд професійного софту для енергетиків.</p>
    </div>
</div>

<!-- SECTION 08: IMPORT OPTIMIZATION & NAMESPACE CLEANING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Оптимізація імпортів та очищення простору імен</h2></div>
    <div class="glass-card flow-step">
        <p>Використання <code>__init__.py</code> як хаба дозволяє уникнути забруднення простору імен (Namespace pollution). Ми явно вказуємо, які функції доступні зовні, що допомагає IDE (VS Code, PyCharm) надавати точніші підказки через автодоповнення. Також це дозволяє відкласти імпорт важких бібліотек (наприклад, Scipy для академічних графіків) до моменту реального звернення до відповідної функції, прискорюючи холодний старт додатку.</p>
    </div>
</div>

<!-- SECTION 09: USER EXPERIENCE FOR DEVELOPERS (DX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">DX: Досвід розробника інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <p>Диспетчер розроблений з акцентом на <b>Developer Experience (DX)</b>. Кожна функція, що експортується, має уніфіковану сигнатуру виклику. Це означає, що розробнику не потрібно пам'ятати специфічні параметри для кожного типу графіка — вони всі працюють за принципом "Дані + Заголовок". Такий підхід значно знижує кількість помилок при розробці нових вкладок дашборду та робить код Атласу легким для підтримки та масштабування.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM SPACER & LAYOUT CONSISTENCY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Консистентність макетів та відступи</h2></div>
    <div class="glass-card flow-step">
        <p>Усі графіки, що проходять через диспетчер, мають уніфіковану висоту (зазвичай 400-550px) та відступи. Це гарантує, що при розміщенні графіків поруч у колонках Streamlit (<code>st.columns</code>), їхні осі та легенди будуть вирівняні по горизонталі. Така "візуальна сітка" є ознакою якісного проектування інтерфейсів і робить сприйняття складної аналітичної інформації більш природним для людського ока.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Chart Sub-modules</h4>
                <p>Базові модулі (base, forecast, academic), що надають реалізацію графіків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📈</div>
            <div class="role-content">
                <h4>Plotly Express</h4>
                <p>Легковаговий двигун для швидкої візуалізації у Legacy-функціях.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4>UI Helpers</h4>
                <p>Зовнішні утиліти для безпечного рендерингу та обробки винятків.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (DYNAMIC REGISTRY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Dynamic Registry)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Динамічного реєстру графіків</b>. Диспетчер буде автоматично реєструвати нові модулі графіків з папки <code>charts/</code>, що дозволить додавати нові типи візуалізації без зміни <code>__init__.py</code>. Також буде додано підтримку <b>Глобальних пресетів</b> (Global Presets), що дозволить одним викликом змінювати стиль усіх графіків у системі (наприклад, перемикатися між Dark та Light темами).</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Диспетчер Бібліотеки</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому краще імпортувати через хаб?</b> — Це гарантує, що ви використовуєте останню версію функції з усіма виправленнями та актуальними стилями ATLAS.</p>
        <p><b>Що таке Legacy функція?</b> — Це старий код, який ми залишили для підтримки сумісності; для нових частин проекту використовуйте спеціалізовані модулі.</p>
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
