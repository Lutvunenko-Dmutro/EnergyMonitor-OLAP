# Технічна специфікація: Кореневий Пакет Системи (ROOT SOURCE PACKAGE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM ARCHITECTURE | ROOT SOURCE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏢</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Корінь Системи</h1>
            <p class="mega-subtitle">Верховний архітектурний простір проекту ATLAS: координація всіх підсистем Energy Monitor Ultimate, визначення логічної ієрархії та забезпечення імпортної цілісності всього програмного комплексу</p>
            <div class="status-tags"><span class="tag tag-online">ROOT ACTIVE</span><span class="tag tag-version">v1.0.0</span><span class="tag tag-role">SYSTEM ARCHITECT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🗺️</div><div class="metric-info"><span class="metric-label">Scope</span><span class="metric-value">6 Major Sub-packages</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🏗️</div><div class="metric-info"><span class="metric-label">Architecture</span><span class="metric-value">Modular Monolith</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔗</div><div class="metric-info"><span class="metric-label">Imports</span><span class="metric-value">Namespace Optimization</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Status</span><span class="metric-value">Foundation Ready</span></div></div>
</div>

<!-- SECTION 01: ROOT PACKAGE PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Кореневого Пакета</h2></div>
    <div class="glass-card flow-step">
        <p>Директорія <code>src/</code> та файл <code>__init__.py</code> є "Фундаментом" та "Генеральним Планом" проекту ATLAS. В системах такого масштабу неможливо підтримувати хаотичну структуру файлів. Наша філософія базується на <b>Логічній Сегрегації</b>: кожна підсистема (Ядро, ML, UI, Сервіси) має своє чітко визначене місце в ієрархії. Кореневий пакет забезпечує те, що Python сприймає весь проект як цілісну екосистему, де компоненти можуть вільно взаємодіяти через структуровані імпорти, зберігаючи при цьому свою автономність та високу модульність, що є критичним для довгострокової розробки та наукової чистоти архітектури.</p>
    </div>
</div>

<!-- SECTION 02: SYSTEM HIERARCHY DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Глобальна ієрархія системи (System Topology)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    ROOT("src/ (System Root)") --> CORE("core/: Analytical Engine")
    ROOT --> ML("ml/: Prediction Intelligence")
    ROOT --> UI("ui/: Immersive Visuals")
    ROOT --> SERV("services/: Orchestration Layer")
    ROOT --> UTILS("utils/: System Toolkit")
    ROOT --> APP("app/: Entry Points")
    
    CORE --> DB("Database & SQL")
    ML --> MODELS("Neural Nets & Clustering")
    UI --> VIEWS("HUD Dashboards & Maps")
    SERV --> SEED("Data Ingestion & Sim")
    </div></div>
</div>

<!-- SECTION 03: THE SIX PILLARS OF ATLAS STRUCTURE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Шість стовпів структури ATLAS</h2></div>
    <div class="glass-card flow-step">
        <p>Кореневий пакет об'єднує наступні стратегічні зони:</p>
        <ul>
            <li><b>Core (Ядро):</b> Фундаментальні алгоритми та низькорівнева робота з базами даних.</li>
            <li><b>ML (Інтелект):</b> Моделі машинного навчання для прогнозування та сегментації активів.</li>
            <li><b>UI (Інтерфейс):</b> Високорівнева візуалізація, карти та HUD-компоненти.</li>
            <li><b>Services (Оркестрація):</b> Сервіси управління життєвим циклом системи та даними.</li>
            <li><b>Utils (Інструментарій):</b> Спільні ресурси для безпеки, валідації та оптимізації.</li>
            <li><b>App (Точки входу):</b> Модулі запуску та головні контролери Streamlit-додатка.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: PACKAGE RESPONSIBILITY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця відповідальності підсистем</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Директорія</th>
                    <th>Роль у проекті</th>
                    <th>Взаємозв'язок</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>src/core/</td><td>Джерело істини та логіки</td><td>База для всіх інших шарів</td></tr>
                <tr><td>src/ml/</td><td>Аналітичний інтелект</td><td>Споживає Core, надає UI</td></tr>
                <tr><td>src/ui/</td><td>Вікно в систему</td><td>Споживає Core, ML, Services</td></tr>
                <tr><td>src/services/</td><td>Робочий персонал</td><td>Координує Core та дані</td></tr>
                <tr><td>src/utils/</td><td>Гвардія безпеки</td><td>Забезпечує стабільність усіх</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: NAMESPACE ISOLATION & IMPORT HYGIENE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Ізоляція просторів імен та гігієна імпортів</h2></div>
    <div class="glass-card flow-step">
        <p>Кореневий пакет <code>src</code> реалізує суворий контроль <b>Просторів імен (Namespaces)</b>. Всі внутрішні імпорти починаються з префікса <code>src.</code> (напр. <code>from src.core.logger import setup_logger</code>). Це усуває конфлікти з зовнішніми бібліотеками та дозволяє Python-інтерпретатору однозначно ідентифікувати компоненти системи. Така ієрархія є запорукою того, що проект ATLAS залишається стабільним при масштабуванні: ми можемо додавати сотні нових файлів, і система імпортів залишиться чистою та передбачуваною.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (ROOT INITIALIZER) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Кореневого Ініціалізатора (Root Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>MODULE src:
    1. DEFINE_LOGICAL_HIERARCHY:
           Identify sub-packages: core, ml, ui, services, utils, app
           
    2. ESTABLISH_BASE_IMPORTS:
           Enable relative and absolute addressing via src.*
           
    3. COORDINATE_ARCHITECTURAL_INTEGRITY:
           - core handles Data/Physics
           - ml handles Forecasting
           - ui handles Presentation
           - services handles ETL/Seeding
           - utils handles Stability/Shielding
           
    4. BOOTSTRAP_READY:
           Provide the foundation for top-level entry points (main.py)
END MODULE</code></pre>
    </div>
</div>

<!-- SECTION 07: ARCHITECTURAL DECOUPLING (THE MODULAR MONOLITH) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Архітектурна розв'язка (Модульний Моноліт)</h2></div>
    <div class="glass-card flow-step">
        <p>Структура <code>src/</code> реалізує паттерн **Модульного Моноліту**. Хоча весь код знаходиться в одному репозиторії, кожна папка всередині є функціонально незалежною. Це дозволяє команді розробників працювати паралельно: ML-інженер може змінювати моделі в <code>src/ml/</code>, не впливаючи на код візуалізації в <code>src/ui/</code>. Кореневий пакет виступає "клеєм", який з'єднує ці незалежні світи в єдину, потужну платформу Energy Monitor Ultimate.</p>
    </div>
</div>

<!-- SECTION 08: THE GATEWAY TO SYSTEM EXECUTION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Шлюз до виконання системи</h2></div>
    <div class="glass-card flow-step">
        <p>Будь-який процес у проекті ATLAS починається з розкриття структури пакета <code>src</code>. Будь то запуск веб-інтерфейсу через Streamlit, виконання тестів або запуск генератора даних — всі вони покладаються на коректну реєстрацію цього пакета в <code>PYTHONPATH</code>. Файл <code>__init__.py</code> у корені <code>src/</code> служить офіційним підтвердженням того, що дана директорія є серцем програмного коду, де кожен байт логіки знаходиться під контролем архітектора.</p>
    </div>
</div>

<!-- SECTION 09: SYSTEM STABILITY & COHESION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Стабільність та згуртованість системи</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки централізованій структурі, ATLAS демонструє високий рівень <b>Згуртованості (Cohesion)</b>. Споріднена логіка згрупована в пакетах, а взаємозв'язки між пакетами зведені до необхідного мінімуму (Loose Coupling). Пакет <code>src</code> оркеструє цей баланс, гарантуючи, що "Ядро" залишається ядром, а "Інтерфейс" — інтерфейсом, запобігаючи перетворенню коду на "спагетті", де все залежить від усього.</p>
    </div>
</div>

<!-- SECTION 10: ACADEMIC SIGNIFICANCE (ARCHITECTURAL PROOF) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Академічна значущість (Архітектурний доказ)</h2></div>
    <div class="glass-card flow-step">
        <p>Для академічного захисту тезису, структура пакету <code>src/</code> є живим доказом **Грамотного інженерного проектування**. Вона демонструє здатність автора організовувати складні програмні комплекси за стандартами Clean Architecture. Чітка ієрархія, розділення на Core, ML та UI шари, а також прозорість взаємодій між ними є вагомим аргументом на користь професійності та наукової обґрунтованості розробленого рішення Energy Monitor Ultimate.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Core Layer</h4>
                <p>Фундаментальний шар істини, на якому будується вся ієрархія src.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🧬</div>
            <div class="role-content">
                <h4>ML & Intelligence</h4>
                <p>Інтелектуальна надбудова, інтегрована в загальну структуру проекту.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>UI Presentation</h4>
                <p>Верхній шар ієрархії, що візуалізує роботу всіх підсистем src.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (DISTRIBUTED PACKAGING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v2.0 (Distributed Packaging)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується перехід до **Розподілених пакетів** (Distributed Packages). Окремі підпакети (напр. <code>src.ml</code>) зможуть бути винесені в окремі репозиторії та встановлюватися як незалежні Python-бібліотеки. Кореневий пакет <code>src</code> при цьому трансформується в <b>Систему Оркестрації Плагінів</b>, що дозволить ATLAS стати справжньою платформою, де нові аналітичні модулі зможуть підключатися динамічно без доступу до основного коду ядра.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Корінь Системи</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому весь код у папці src/?</b> — Це стандартна практика для Python-проектів, яка запобігає конфліктам імпортів та полегшує упаковку додатку.</p>
        <p><b>Як додати нову підсистему?</b> — Створіть папку в <code>src/</code>, додайте <code>__init__.py</code> та опишіть її роль у цій технічній специфікації.</p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
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
