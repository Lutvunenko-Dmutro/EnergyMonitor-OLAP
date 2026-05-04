# Технічна специфікація: Реєстр Аналітичних Представлень (ANALYTICAL VIEWS REGISTRY)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">VIEWS REGISTRY | DASHBOARD HUB</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏗️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Реєстр Представлень</h1>
            <p class="mega-subtitle">Центральний пакетний хаб аналітичних модулів проекту ATLAS: об'єднання виконавчих дашбордів, інтерфейсів ШІ-прогнозування та діагностичних панелей в єдину екосистему візуалізації</p>
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

<!-- SECTION 01: VIEWS REGISTRY PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Реєстру Представлень</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>views/__init__.py</code> є "Збірним пунктом" для всієї бізнес-логіки візуалізації проекту ATLAS. В складних системах важливо мати чітку ієрархію модулів. Наша філософія базується на <b>Модульній Повноті</b>: кожна вкладка дашборду — це окремий, незалежний світ (View), який інкапсулює власні алгоритми аналізу та графічні компоненти. Реєстр забезпечує їх гармонійне співіснування, дозволяючи Головному Оркестратору легко перемикатися між ними, зберігаючи єдиний стандарт взаємодії через уніфікований метод <code>render()</code>.</p>
    </div>
</div>

<!-- SECTION 02: REGISTRY ARCHITECTURE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Архітектурна схема реєстру (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DASH("Dashboard Engine (dashboard.py)") --> HUB("Views Registry (views/__init__.py)")
    
    HUB --> MONITOR("Executive Monitoring: kpi.py, map.py")
    HUB --> ANALYTICS("Deep Analytics: consumption.py, finance.py")
    HUB --> AI_CORE("AI Power: forecast.py, advanced.py")
    HUB --> DIAGNOSTICS("Diagnostics: historical_audit.py, alerts.py")
    
    MONITOR --> RENDER("Unified render(data) Interface")
    ANALYTICS --> RENDER
    AI_CORE --> RENDER
    DIAGNOSTICS --> RENDER
    
    RENDER --> UI("Final Screen Output")
    </div></div>
</div>

<!-- SECTION 03: THE UNIFIED RENDER() CONTRACT -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Контракт уніфікованого методу render()</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення стабільності та простоти підтримки, всі модулі в реєстрі дотримуються суворого контракту:</p>
        <ul>
            <li><b>Standard Input:</b> Кожна функція <code>render()</code> приймає очищений DataFrame та необов'язкові параметри фільтрації.</li>
            <li><b>Encapsulated Logic:</b> Модуль сам відповідає за внутрішні агрегації, виклик графічних компонентів та обробку NaN-значень.</li>
            <li><b>UX Consistency:</b> Кожне представлення зобов'язане додавати Spacer в кінці сторінки для комфортного скролінгу, що гарантується через перевірку в реєстрі.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: VIEW CLASSIFICATION MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця класифікації представлень</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Категорія</th>
                    <th>Модулі (Views)</th>
                    <th>Цільова аудиторія</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Executive Monitoring</td><td>kpi.py, map.py, generation.py</td><td>Топ-менеджмент, Диспетчери</td></tr>
                <tr><td>AI & Forecasting</td><td>forecast.py, advanced.py</td><td>ML-інженери, Аналітики</td></tr>
                <tr><td>Technical Audit</td><td>historical_audit.py, consumption.py</td><td>Інженери з експлуатації</td></tr>
                <tr><td>Safety & Economy</td><td>alerts.py, finance.py</td><td>Служба безпеки, Економісти</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: THE HUB OF ANALYTICAL DIVERSITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Хаб аналітичного різноманіття</h2></div>
    <div class="glass-card flow-step">
        <p>Реєстр представлень об'єднує чотири ключові напрямки аналізу. Від <b>Live-моніторингу</b> підстанцій на карті до <b>Глибокого ШІ-аудиту</b> LSTM-моделей. Таке групування дозволяє розробникам ATLAS додавати нові типи аналізу, просто створюючи новий файл у папці <code>views/</code>, не ламаючи при цьому існуючу логіку навігації та роутингу, що робить систему надзвичайно гнучкою та придатною для довгострокового розвитку.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Реєстру (Registry Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>MODULE src.ui.views:
    1. PACKAGE_DESCRIPTION:
           Define metadata for monitoring, forecasting, diagnostics.
           
    2. IMPORT_STRATEGY:
           # Explicit imports in dashboard.py for better tree-shaking
           IMPORT advanced, alerts, consumption, finance, 
                  forecast, generation, audit, kpi, map
                  
    3. INTERFACE_STANDARD:
           ALL modules MUST implement:
               render(df_data, filter_params, **kwargs)
               
    4. UX_ENFORCEMENT:
           Ensure bottom spacer <div height=300px> is present in all views.
END MODULE</code></pre>
    </div>
</div>

<!-- SECTION 07: MODULE ISOLATION & DATA SECURITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Ізоляція модулів та безпека даних</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки реєстровій структурі, кожне представлення працює в <b>Ізольованому контексті</b>. Це означає, що помилка рендерингу в модулі "Економіка" не призведе до падіння модуля "Карта". Також це дозволяє впроваджувати рольову модель доступу (RBAC) на рівні реєстру: система може просто не імпортувати або не відображати певні модулі для користувачів без відповідних прав доступу до фінансових або режимних даних.</p>
    </div>
</div>

<!-- SECTION 08: THE EVOLUTION OF ATLAS VISUALS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Еволюція візуальних представлень ATLAS</h2></div>
    <div class="glass-card flow-step">
        <p>Реєстр <code>views/</code> пройшов еволюцію від простого списку скриптів до складної ієрархічної системи. Сьогодні він підтримує як **Статичні сторінки** (Архів, Економіка), так і **Реактивні фрагменти** (Карта, KPI). Це стало можливим завдяки гнучкому опису пакету в <code>__init__.py</code>, який служить "Живою документацією" для розробників, вказуючи на призначення та можливості кожного аналітичного представлення.</p>
    </div>
</div>

<!-- SECTION 09: DEVELOPER EXPERIENCE (DX) & REGISTRY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Досвід розробника (DX) та роль Реєстру</h2></div>
    <div class="glass-card flow-step">
        <p>Для нових учасників команди розробки Атласу, <code>views/__init__.py</code> є основною картою проекту. Короткі та влучні описи категорій представлень допомагають швидко зорієнтуватися в структурі візуалізації. Використання стандартизованих імен модулів (consumption, generation, finance) робить код самодокументованим, що є критично важливим для академічних проектів, де чистота та зрозумілість архітектури оцінюються нарівні з функціональністю.</p>
    </div>
</div>

<!-- SECTION 10: UX STANDARDIZATION ACROSS VIEWS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Стандартизація UX у всіх представленнях</h2></div>
    <div class="glass-card flow-step">
        <p>Реєстр не просто об'єднує файли, він задає **Стандарт Користувацького Досвіду**. Кожне представлення, зареєстроване тут, дотримується єдиної колірної палітри, використовує однакові типи заголовків та роздільників. Це створює відчуття "безшовного" переходу між різними аналітичними інструментами — користувач не відчуває, що він перемикається між різними програмами, а працює в єдиному інтелектуальному просторі ATLAS.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Dashboard Orchestrator</h4>
                <p>Головний споживач реєстру, що керує відображенням модулів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📂</div>
            <div class="role-content">
                <h4>View Sub-modules</h4>
                <p>Набір файлів (kpi.py, map.py тощо), що реалізують конкретні UI.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4>UI Components</h4>
                <p>Бібліотека графіків та стилів, що використовується всіма View.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (PLUGGABLE VIEWS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Pluggable Views)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Плагінної архітектури представлень</b>. Реєстр буде автоматично сканувати папку <code>views/</code> та динамічно додавати нові представлення до інтерфейсу без необхідності перезапуску сервера. Також буде додано підтримку <b>Користувацьких представлень</b>: оператори зможуть створювати власні компоновки графіків (Custom Dashboards) та реєструвати їх у системі як нові Views.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Реєстр Представлень</h2></div>
    <div class="glass-card flow-step">
        <p><b>Як додати нову вкладку в Атлас?</b> — Створіть файл у <code>src/ui/views/</code>, реалізуйте функцію <code>render()</code> та додайте його в <code>dashboard.py</code>.</p>
        <p><b>Чи можна змінити порядок вкладок?</b> — Так, це робиться у списку <code>options</code> всередині <code>render_dashboard_ui()</code> у файлі <code>dashboard.py</code>.</p>
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
