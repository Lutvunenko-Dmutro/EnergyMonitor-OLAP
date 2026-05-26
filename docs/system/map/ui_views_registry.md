# Технічна специфікація: Реєстр Аналітичних Представлень (ANALYTICAL VIEWS REGISTRY)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">VIEWS REGISTRY | DASHBOARD HUB</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏗️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Реєстр Представлень</h1>
            <p class="mega-subtitle">Центральний пакетний хаб аналітичних сторінок проєкту ATLAS: об'єднання виконавчих дашбордів, ШІ-прогнозування та діагностичних панелей в єдину екосистему візуалізації</p>
            <div class="status-tags"><span class="tag tag-online">REGISTRY ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">UI ARCHITECT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Components</span><span class="metric-value">9+ Full-Page Views</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Interface</span><span class="metric-value">Unified render() API</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">Focus</span><span class="metric-value">AI / Audit / Security</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Pattern</span><span class="metric-value">Package Dispatcher</span></div></div>
</div>

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Реєстру Представлень</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>views/__init__.py</code> є "Збірним пунктом" для всієї бізнес-логіки візуалізації проєкту ATLAS. В складних веб-додатках критично мати чітку ієрархію модулів. Наша філософія базується на <b>Модульній Повноті</b>: кожна вкладка дашборду — це окремий, незалежний світ (View), який інкапсулює власні алгоритми аналізу та графічні компоненти. Реєстр забезпечує їх гармонійне співіснування, дозволяючи Головному Оркестратору легко перемикатися між ними, зберігаючи єдиний стандарт взаємодії через уніфікований метод <code>render()</code>.</p>
    </div>
</div>

<!-- SECTION 02: FORMAL PIPELINE CONTRACT -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичний контракт та функціональна модель</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення абсолютної гнучкості та стійкості до відмов, кожне представлення $V_k$ в реєстрі моделюється як чиста функція рендерингу:</p>
        $$V_k: (\mathbf{D}, \mathbf{P}, \mathbf{\Theta}) \to \mathbf{HTML}_{\text{Streamlit}}$$
        <p>де:</p>
        <ul>
            <li>$\mathbf{D}$ — багатовимірний Pandas DataFrame, що містить очищені та агреговані історичні чи поточні телеметричні дані.</li>
            <li>$\mathbf{P}$ — словник параметрів фільтрації (активний регіон, обрана підстанція, межі календаря).</li>
            <li>$\mathbf{\Theta}$ — поточний стан сесії користувача (<code>st.session_state</code>), що містить конфігурації шкал та зворотний зв'язок.</li>
        </ul>
        <p>Така модель забезпечує повну ізоляцію представлень: збій або виняток усередині $V_i$ локалізується та перехоплюється оркестратором, не впливаючи на працездатність інших зареєстрованих Views.</p>
    </div>
</div>

<!-- SECTION 03: REGISTRY ARCHITECTURE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Архітектурна схема реєстру (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DASH("Dashboard Engine (dashboard.py)") --> HUB("Views Registry (views/__init__.py)")
    
    HUB --> MONITOR("Executive Monitoring: kpi.py, map.py, generation.py")
    HUB --> ANALYTICS("Deep Analytics: consumption.py, finance.py")
    HUB --> AI_CORE("AI Power: forecast.py, advanced.py")
    HUB --> DIAGNOSTICS("Diagnostics: historical_audit.py, alerts.py")
    
    MONITOR --> RENDER("Unified render(data) Interface")
    ANALYTICS --> RENDER
    AI_CORE --> RENDER
    DIAGNOSTICS --> RENDER
    
    RENDER --> UI("Final Screen Output (Streamlit App)")
    </div></div>
</div>

<!-- SECTION 04: VIEW CLASSIFICATION MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця класифікації представлень</h2></div>
    <div class="glass-card flow-step">
        <p>Реєстр розбиває представлення на чотири функціональні категорії відповідно до завдань користувача:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Категорія</th>
                    <th>Зареєстровані модулі (Views)</th>
                    <th>Роль у системі</th>
                    <th>Цільовий користувач</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Executive Monitoring</b></td><td><code>kpi.py</code>, <code>map.py</code>, <code>generation.py</code></td><td>Ситуаційна обізнаність, живі потоки енергії, географічний контроль</td><td>Топ-менеджмент, Черговий диспетчер</td></tr>
                <tr><td><b>AI & Forecasting</b></td><td><code>forecast.py</code>, <code>advanced.py</code></td><td>LSTM-прогнозування, декомпозиція трендів, кластеризація споживачів</td><td>ШІ-інженер, Аналітик</td></tr>
                <tr><td><b>Technical Audit</b></td><td><code>historical_audit.py</code>, <code>consumption.py</code></td><td>Аналіз зносу ізоляції (DGA), теплові карти, добові ритми споживання</td><td>Інженер з експлуатації ЛЕП</td></tr>
                <tr><td><b>Safety & Economy</b></td><td><code>alerts.py</code>, <code>finance.py</code></td><td>Реєстрація аварій, керування статусами, фінансовий аналіз втрат в мережі</td><td>Офіцер безпеки, Економіст</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: DEVELOPER EXPERIENCE (DX) & MODULE ISOLATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Ізоляція модулів та безпека даних (DX)</h2></div>
    <div class="glass-card flow-step">
        <p>Для нових учасників команди розробки Атласу, <code>views/__init__.py</code> є основною картою проєкту. Короткі та влучні описи категорій представлень допомагають швидко зорієнтуватися в структурі візуалізації. Використання стандартизованих імен модулів робить код самодокументованим, що є критично важливим для академічних проєктів, де чистота та зрозумілість архітектури оцінюються нарівні з функціональністю.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Реєстру (Registry & Safe Calling)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>PACKAGE src.ui.views:
    1. // [TREE-SHAKING EXPLICIT IMPORTS]
       IMPORT advanced_view   FROM src.ui.views.advanced
       IMPORT alerts_view     FROM src.ui.views.alerts
       IMPORT consumption_view FROM src.ui.views.consumption
       IMPORT finance_view     FROM src.ui.views.finance
       IMPORT forecast_view    FROM src.ui.views.forecast
       IMPORT generation_view  FROM src.ui.views.generation
       IMPORT audit_view       FROM src.ui.views.historical_audit
       IMPORT kpi_view         FROM src.ui.views.kpi
       IMPORT map_view         FROM src.ui.views.map
       
    2. // [UNIFIED CONTRACT VERIFICATION]
       FUNCTION safe_execute_view(view_func, df_data, *args, **kwargs):
           TRY:
               view_func(df_data, *args, **kwargs)
               // [UX COMPLIANCE STANDARD: SCROLL SPACER]
               st.markdown('&lt;div style="height: 300px;"&gt;&lt;/div&gt;', unsafe_allow_html=True)
           EXCEPT Exception as e:
               // [ISOLATION GUARD: ONE TAB ZONING ERROR]
               st.error(f"⚠️ Помилка завантаження модуля: {e}")
               log_to_observability_hub(e)
END PACKAGE</code></pre>
    </div>
</div>

<!-- SECTION 07: UX STANDARDIZATION & DESIGN CONSISTENCY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Стандартизація UX у всіх представленнях</h2></div>
    <div class="glass-card flow-step">
        <p>Реєстр не просто об'єднує файли, він задає **Стандарт Користувацького Досвіду**. Кожне представлення, зареєстроване тут, дотримується єдиної колірної палітри, використовує однакові типи заголовків та роздільників. Це створює відчуття "безшовного" переходу між різними аналітичними інструментами — користувач не відчуває, що він перемикається між різними програмами, а працює в єдиному інтелектуальному просторі ATLAS.</p>
    </div>
</div>

<!-- SECTION 08: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4><a href="ui_dashboard_layout.md">dashboard.py</a></h4>
                <p>Головний оркестратор інтерфейсу, що здійснює навігацію та послідовно викликає зареєстровані представлення.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📂</div>
            <div class="role-content">
                <h4>View Sub-modules</h4>
                <p>Набір файлів (kpi.py, map.py, finance.py тощо), що реалізують бізнес-інтерфейси системи.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4><a href="ui_design_system.md">styles.py</a></h4>
                <p>Дизайн-система Cyber-HUD, яка забезпечує єдиний візуальний код для всіх представлень.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 09: ROADMAP TO v3.0 (DYNAMIC PLUGIN SYSTEM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Дорожня карта v3.0 (Dynamic Pluggable Views)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступних версіях заплановано:</p>
        <ul>
            <li><b>Dynamic Directory Scan:</b> Автоматичне сканування директорії <code>views/</code> та динамічне підключення нових вкладок без ручного редагування <code>dashboard.py</code>.</li>
            <li><b>Custom Dashboard Builder:</b> Можливість для оператора самостійно перетягувати (Drag-and-Drop) окремі віджети з різних представлень на один екран.</li>
            <li><b>Role-Based Tab Visibility (RBAC):</b> Автоматичне приховування фінансових (finance) або інженерних (historical_audit) вкладок для користувачів без відповідного рівня доступу.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">FAQ: Технічні відповіді про Реєстр</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Як зареєструвати нову аналітичну вкладку?</b><br>
        A: 1) Створіть новий файл у папці <code>src/ui/views/</code> (наприклад, <code>security.py</code>); 2) Реалізуйте всередині функцію <code>render(df, ...)</code>; 3) Імпортуйте її у <code>dashboard.py</code> та додайте у вибір роутингу. У майбутній версії 3.0 реєстрація буде повністю автоматичною.</p>
        <p><b>Q: Як реалізована ізоляція помилок між вкладками?</b><br>
        A: Кожен виклик представлення у <code>dashboard.py</code> обгорнутий блоком try-except. Якщо у вкладці "Карта" виникне критична помилка (наприклад, збій WebGL в браузері оператора), це призведе до показу попередження тільки всередині цієї вкладки. Всі інші вкладки (KPI, Генерація тощо) залишаться повністю працездатними.</p>
        <p><b>Q: Навіщо потрібні імпорти безпосередньо у dashboard.py, а не всередині __init__.py?</b><br>
        A: Це дозволяє оптимізувати пам'ять при завантаженні (Tree-Shaking) та запобігає виникненню циклічних імпортів між допоміжними утилітами UI та бізнес-моделями.</p>
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
