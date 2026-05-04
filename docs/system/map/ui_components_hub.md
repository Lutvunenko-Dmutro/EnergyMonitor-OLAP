# Технічна специфікація: Бібліотека UI-Компонентів (SHARED UI COMPONENTS HUB)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">COMPONENTS HUB | ATOMIC DESIGN</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧩</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Хаб UI-Компонентів</h1>
            <p class="mega-subtitle">Центральний вузол багаторазових візуальних елементів проекту ATLAS: координація бібліотек графіків, карток KPI та дизайн-системи для забезпечення візуальної цілісності HUD-інтерфейсів</p>
            <div class="status-tags"><span class="tag tag-online">COMPONENTS HUB ACTIVE</span><span class="tag tag-version">v2.2.0</span><span class="tag tag-role">DESIGN SYSTEM LEAD</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Design</span><span class="metric-value">Atomic UI System</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Library</span><span class="metric-value">Charts & Indicators</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Integrity</span><span class="metric-value">Global Style Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Reuse</span><span class="metric-value">Cross-View Sharing</span></div></div>
</div>

<!-- SECTION 01: SHARED COMPONENTS PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Спільних Компонентів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>components/__init__.py</code> є "Складським центром" (Hub) для всіх візуальних будівельних блоків проекту ATLAS. Наша філософія базується на <b>Атомарному Дизайні</b>: ми розробляємо компоненти як незалежні, самодостатні одиниці, які можна легко комбінувати для створення нових аналітичних екранів. Такий підхід гарантує, що кожна карта KPI або графік тренду виглядає і працює однаково у будь-якій частині системи, що критично важливо для професійного сприйняття інженерного програмного забезпечення та зниження витрат на розробку нових функцій.</p>
    </div>
</div>

<!-- SECTION 02: COMPONENTS ARCHITECTURE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Архітектурна схема хаба (Architecture Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    VIEWS("UI Views (forecast, map, etc)") --> HUB("Components Hub (__init__.py)")
    
    HUB --> CARDS("cards.py: KPI & Health Indicators")
    HUB --> CHARTS("charts/ sub-package: Analytics")
    HUB --> STYLES("styles.py: CSS & Theming Engine")
    
    CARDS --> ATOMIC("Atomic Visual Units")
    CHARTS --> ATOMIC
    STYLES --> ATOMIC
    
    ATOMIC --> UI("Unified Cyber-HUD Interface")
    </div></div>
</div>

<!-- SECTION 03: THE SHARED UI ECOSYSTEM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Екосистема спільних UI-компонентів</h2></div>
    <div class="glass-card flow-step">
        <p>Хаб компонентів об'єднує три фундаментальні напрямки візуалізації:</p>
        <ul>
            <li><b>Visual Feedback (Cards):</b> Миттєва передача стану через колірні коди та емодзі-бари.</li>
            <li><b>Deep Insights (Charts):</b> Потужні інструменти для дослідження трендів, кореляцій та ШІ-прогнозів.</li>
            <li><b>Design Language (Styles):</b> Глобальна "шкіра" додатку, що визначає його футуристичний Cyber-HUD вигляд.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: COMPONENT DISPATCHER MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця диспетчеризації компонентів</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Бібліотека</th>
                    <th>Тип компонентів</th>
                    <th>Роль у системі</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>cards.py</td><td>Gauges, Health Bars</td><td>Миттєвий моніторинг статусів</td></tr>
                <tr><td>charts/</td><td>Line, Scatter, Histograms</td><td>Глибокий аналіз та аудит</td></tr>
                <tr><td>styles.py</td><td>CSS Injectors, Page Config</td><td>Фундамент візуальної ідентичності</td></tr>
                <tr><td>__init__.py</td><td>Central Namespace</td><td>Управління експортом та доступом</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: GLOBAL STYLE CONSISTENCY (UI UNIFORM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Глобальна цілісність стилів (UI Uniform)</h2></div>
    <div class="glass-card flow-step">
        <p>Хаб компонентів є "Охоронцем" візуальної ідентичності ATLAS. Через <code>__init__.py</code> ми гарантуємо, що будь-який новий компонент, доданий у систему, автоматично наслідує глобальні стилі з <code>styles.py</code>. Це стосується колірних палітр, шрифтів <b>Orbitron</b> та <b>Inter</b>, а також специфічних для Cyber-HUD ефектів Glassmorphism. Така стандартизація робить інтерфейс ATLAS цілісним та професійним, усуваючи "візуальний хаос", характерний для неструктурованих проектів.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Хаба (Components Hub Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>MODULE src.ui.components:
    1. PACKAGE_INITIALIZATION:
           Define shared UI blocks for HUD building.
           
    2. EXPOSE_SUBPACKAGES:
           REGISTER cards (KPI containers)
           REGISTER charts (Trend & Stat libraries)
           REGISTER styles (CSS & Identity engine)
           
    3. ACCESS_STRATEGY:
           Provide single entry-point for all UI Views.
           Ensure consistent look-and-feel across re-exports.
END MODULE</code></pre>
    </div>
</div>

<!-- SECTION 07: MODULE REUSABILITY & SCALABILITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Перевикористання модулів та масштабованість</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки централізованому хабу, ATLAS може масштабуватися без збільшення складності коду представлень. Якщо нам потрібно оновити вигляд усіх карток здоров'я в системі, ми робимо це в одному файлі <code>cards.py</code>, і зміни миттєво відображаються у всіх View. Це демонструє високий рівень **Engineering Excellence**, дозволяючи системі еволюціонувати від простого прототипу до складного індустріального рішення без накопичення технічного боргу в UI-шарі.</p>
    </div>
</div>

<!-- SECTION 08: THE HUB AS A DEVELOPER TOOLKIT (DX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Хаб як інструментарій розробника (DX)</h2></div>
    <div class="glass-card flow-step">
        <p>Для розробника, <code>components/__init__.py</code> служить **Toolkit-ом**. Замість того, щоб шукати потрібний графік або кнопку по всьому проекту, розробник звертається до хаба. Ясні та влучні описи категорій компонентів у коментарях пакету допомагають швидко вибрати правильний візуальний елемент для конкретного типу даних. Це робить процес створення нових аналітичних панелей в Атласі швидким, передбачуваним та приємним процесом (high Developer Experience).</p>
    </div>
</div>

<!-- SECTION 09: USER-CENTRIC DESIGN COHESION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Користувацька цілісність дизайну</h2></div>
    <div class="glass-card flow-step">
        <p>З точки зору кінцевого користувача (оператора), хаб компонентів забезпечує <b>Передбачуваність</b>. Якщо він бачить червоний колір на картці KPI, він знає, що цей самий відтінок червоного буде використаний на графіку помилок і на карті підстанцій. Така когнітивна консистентність є критичною для систем моніторингу реального часу, оскільки вона дозволяє мозку оператора швидше розпізнавати патерни небезпеки та приймати вірні рішення без додаткових зусиль на дешифрування інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 10: ACADEMIC SIGNIFICANCE (MODULARITY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Академічна значущість (Модульність)</h2></div>
    <div class="glass-card flow-step">
        <p>В рамках академічного дослідження, структура <code>src/ui/components/</code> є втіленням принципу **Separation of Concerns** (Розділення відповідальностей). Ми відокремили логіку візуалізації від логіки представлення сторінок. Це дозволяє проводити ізольоване тестування компонентів, що є важливою частиною верифікації системи. Така архітектура високо оцінюється на захисті дипломних проектів як доказ глибокого розуміння розробником сучасних патернів проектування ПЗ.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Sub-libraries</h4>
                <p>Реалізації карток, графіків та стилів (cards.py, charts/, styles.py).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>UI Views</h4>
                <p>Основні споживачі компонентів для побудови сторінок дашборду.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>Styling Engine</h4>
                <p>Глобальний CSS ін'єктор, що забезпечує єдність Cyber-HUD.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (COMPONENTS PLAYGROUND) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Components Playground)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Components Playground</b> — спеціальної сервісної сторінки для розробників, де можна буде протестувати будь-який компонент з хаба на тестових даних. Також буде додано підтримку <b>Тематичних пакетів</b>: можливість "на льоту" змінювати візуальний стиль усіх компонентів хаба (наприклад, перемикання з "Cyber-HUD" на "Classic Lab") для адаптації під різні умови освітлення в диспетчерських залах.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Хаб Компонентів</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чи можу я використовувати свій CSS у View?</b> — Рекомендується додавати стилі через <code>styles.py</code> для збереження цілісності проекту ATLAS.</p>
        <p><b>Як додати новий тип графіка?</b> — Створіть його в <code>charts/</code> та переконайтеся, що він доступний через ре-експорт у хабі компонентів.</p>
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
