# Технічна специфікація: Ядро Системних Операцій та Фізики (CORE KERNEL HUB)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM CORE | PHYSICS & DATA ACCESS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Ядро Системи</h1>
            <p class="mega-subtitle">Фундаментальний шар ATLAS: математичне моделювання фізичних процесів енергомережі, оркестрація низькорівневих SQL-запитів та інтелектуальне завантаження зовнішніх архівів Kaggle</p>
            <div class="status-tags"><span class="tag tag-online">KERNEL ACTIVE</span><span class="tag tag-version">v2.9.0</span><span class="tag tag-role">BASE INFRASTRUCTURE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⚛️</div><div class="metric-info"><span class="metric-label">Physics</span><span class="metric-value">Ohm & Joule Models</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Queries</span><span class="metric-value">Optimized SQL Bus</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Kaggle</span><span class="metric-value">Lazy CSV Loader</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Integrity</span><span class="metric-value">Atomic Data Access</span></div></div>
</div>

<!-- SECTION 01: ARCHITECTURAL FOUNDATION -->
<div class="section-container" id="main">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Архітектурний Фундамент Ядра</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/core/</code> є найнижчим та найбільш критичним шаром проекту ATLAS. Це "Двигун", на якому базується вся вища логіка. Тут визначаються закони фізики, за якими працює наша модель енергосистеми, та правила взаємодії з джерелами даних. Без цього шару ні ML-моделі, ні UI-компоненти не мали б твердого ґрунту для розрахунків та відображення інформації. Ядро забезпечує стабільність всієї екосистеми, виконуючи роль посередника між сирими даними та аналітичними сервісами.</p>
    </div>
</div>

<!-- SECTION 02: KERNEL COMPONENTS MATRIX -->
<div class="section-container" id="config">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Матриця Компонентів Ядра</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль</th>
                    <th>Функціональна Роль</th>
                    <th>Методологія</th>
                    <th>Ступінь критичності</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>physics.py</code></td><td>Фізичне моделювання</td><td>Математичні абстракції</td><td>Критичний (L1)</td></tr>
                <tr><td><code>queries.py</code></td><td>SQL-репозиторій</td><td>Pre-compiled Statements</td><td>Високий (L2)</td></tr>
                <tr><td><code>config.py</code></td><td>Оркестрація констант</td><td>Static Registry</td><td>Високий (L2)</td></tr>
                <tr><td><code>kaggle_loader.py</code></td><td>Зовнішні дані</td><td>Chunked Data Processing</td><td>Середній (L3)</td></tr>
                <tr><td><code>logger.py</code></td><td>Системний аудит</td><td>Structured Logging</td><td>Середній (L3)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: PHYSICS-DRIVEN MODELING STRATEGY -->
<div class="section-container" id="physics">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Фізично-орієнтованого Моделювання</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>physics.py</code> ми імплементуємо базові закони електротехніки. Ми моделюємо втрати енергії в лініях (Закон Джоуля-Ленца) та падіння напруги залежно від навантаження. Це робить систему ATLAS не просто візуалізатором таблиць, а **Справжнім Енергетичним Симулятором**. 
        Основні фізичні розрахунки включають:
        <ul>
            <li><b>Втрати на нагрів:</b> Q = I² * R * t, де навантаження (MW) корелює зі струмом (I).</li>
            <li><b>Температурна деградація:</b> Розрахунок впливу навколишнього середовища на охолодження трансформаторів.</li>
            <li><b>Закон Ома:</b> Моделювання падіння напруги в магістральних мережах при пікових навантаженнях.</li>
        </ul>
        Це дозволяє системі ATLAS розуміти фізичну природу процесів, що відбуваються в мережі.</p>
    </div>
</div>

<!-- SECTION 04: CORE DATA INTERACTION DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема Взаємодії Ядра з Даними</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI_REQ("UI / Service Request") --> QUERY_BUS("queries.py: Query Orchestrator")
    QUERY_BUS --> DB_LOCAL[("Local PostgreSQL")]
    QUERY_BUS --> DB_CLOUD[("Cloud Neon DB")]
    
    KAG_REQ("Archive Request") --> KAG_LOAD("kaggle_loader: Lazy CSV")
    KAG_LOAD --> CSV_STORAGE[("Kaggle Dataset Storage")]
    
    PHYS_ENG("physics.py: Engine") -- Rules --> SENSORS("Simulation Sensors")
    SENSORS -- Data --> DB_LOCAL
    </div></div>
</div>

<!-- SECTION 05: OPTIMIZED QUERY ORCHESTRATION -->
<div class="section-container" id="queries">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Оптимізована Оркестрація Запитів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>queries.py</code> містить бібліотеку пре-компільованих SQL-запитів. Ми уникаємо динамічного формування SQL-рядків у коді, що не лише підвищує продуктивність, а й захищає систему від SQL-ін'єкцій. Кожен запит оптимізовано для роботи з великими масивами часових рядів (Time-series optimization). Використовуються індекси по колонці <code>timestamp</code> та <code>substation_id</code>, що забезпечує миттєву агрегацію мільйонів записів навіть на скромному апаратному забезпеченні.</p>
    </div>
</div>

<!-- SECTION 06: SYSTEM CONFIGURATION & CONSTANTS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Системна Конфігурація та Константи</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>config.py</code> є центральним сховищем всіх параметрів ATLAS. Тут визначаються ліміти навантаження, межі безпечної температури обладнання та налаштування підключення до БД. Використання єдиного конфігураційного шару дозволяє змінювати поведінку всієї системи (наприклад, перемикатися між локальною БД та хмарою) одним рядком коду, не зачіпаючи бізнес-логіку.</p>
    </div>
</div>

<!-- SECTION 07: INTELLIGENT KAGGLE DATA HANDLING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Інтелектуальна Обробка Даних Kaggle</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>kaggle_loader.py</code> реалізує паттерн **Lazy Loading**. Оскільки архіви Kaggle можуть займати сотні мегабайт, ми не завантажуємо їх у пам'ять повністю. Замість цього система зчитує лише необхідні часові фрагменти та колонки (Columnar access). Це реалізовано через ефективну фільтрацію DataFrame за допомогою Pandas ще на етапі зчитування, що дозволяє проводити глибокий аналіз історичних даних навіть на пристроях з обмеженим обсягом RAM (наприклад, Edge-ноутбуки диспетчерів).</p>
    </div>
</div>

<!-- SECTION 08: SYSTEM-WIDE LOGGING & DIAGNOSTICS -->
<div class="section-container" id="logger">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Системне Логування та Діагностика</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки <code>logger.py</code> ядро забезпечує повну прозорість операцій. Будь-яка помилка фізичного розрахунку або збій при доступі до даних фіксується з максимальною деталізацією. Використовується багаторівневе логування (DEBUG/INFO/ERROR), що дозволяє команді підтримки ATLAS швидко виявляти вузькі місця в продуктивності та гарантувати надійність системи 24/7. Логи структуровані для легкого парсингу системами моніторингу на кшталт Grafana.</p>
    </div>
</div>

<!-- SECTION 09: KERNEL LIFECYCLE STATE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Sequence: Життєвий цикл запиту в Ядрі</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
stateDiagram-v2
    [*] --> Idle
    Idle --> Init: Load Config
    Init --> Active: Connect to DB
    Active --> Processing: UI/ML Request
    Processing --> QueryBus: SQL Fetch
    QueryBus --> Physics: Rule Validation
    Physics --> Processing: Result Ready
    Processing --> Active: Send JSON
    Active --> [*]: Shutdown
    </div></div>
</div>

<!-- SECTION 10: CORE INTEGRITY & ATOMICITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Цілісність та Атомарність Ядра</h2></div>
    <div class="glass-card flow-step">
        <p>Всі операції ядра побудовані на принципі атомарності. Ми гарантуємо, що кожна фізична симуляція або запит до даних завершується повністю або не змінює стан системи взагалі (ACID principles). Це критично для підтримки високої наукової достовірності аналітичних звітів та надійності роботи ML-конвеєрів. Спеціальний шар валідації в <code>physics.py</code> блокує "фізично неможливі" результати (наприклад, від'ємне навантаження), забезпечуючи чистоту даних.</p>
    </div>
</div>

<!-- SECTION 11: ROADMAP TO v3.0 (DISTRIBUTED KERNEL) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Дорожня карта v3.0 (Distributed Kernel)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується перехід на **Розподілене Ядро**, де фізичні розрахунки будуть паралелізуватися між декількома обчислювальними вузлами (Worker Nodes). Також буде додано підтримку <i>Complex Power Algebra</i> для більш точного моделювання реактивної потужності (VAR) та впроваджено модуль автоматичної інтеграції з API реальних операторів систем передачі (TSO) через протокол IEC 60870-5-104.</p>
    </div>
</div>

<!-- SECTION 12: KERNEL TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Технічний FAQ Ядра</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Чому використовується Raw SQL замість важких ORM?</b><br>
        A: Для забезпечення максимальної продуктивності при пакетній обробці мільйонів записів телеметрії. Raw SQL дозволяє використовувати специфічні оптимізації PostgreSQL.</p>
        <p><b>Q: Як ядро обробляє розриви з'єднання з БД?</b><br>
        A: Модуль <code>queries.py</code> реалізує стратегію <i>Retry with Exponential Backoff</i>, що дозволяє системі автоматично відновлювати роботу після короткочасних мережевих збоїв.</p>
        <p><b>Q: Які фізичні обмеження закладені в модель?</b><br>
        A: Ми обмежуємо напругу в діапазоні 0.8-1.2 від номіналу та не допускаємо від'ємних значень активної потужності.</p>
    </div>
</div>

<!-- SECTION 13: CORE ENGINE GLOSSARY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">Глосарій Системного Ядра</h2></div>
    <div class="glass-card flow-step">
        <ul>
            <li><b>Atomic Query:</b> Запит, який гарантує цілісність даних через транзакційні механізми.</li>
            <li><b>Lazy Loading:</b> Технологія завантаження даних лише в момент безпосереднього звернення до них.</li>
            <li><b>DDL (Data Definition Language):</b> Підмножина SQL для керування структурою таблиць та індексів.</li>
            <li><b>Joule Losses:</b> Теплові втрати в провідниках, що розраховуються ядром фізики.</li>
        </ul>
    </div>
</div>

<!-- SECTION 14: PROFESSIONAL USAGE GUIDELINES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">14</span><h2 class="section-title">Професійні настанови з використання Ядра</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення стабільної роботи системного ядра ATLAS:</p>
        <ul>
            <li><b>Query Optimization:</b> При написанні нових запитів у <code>queries.py</code> завжди виконуйте <code>EXPLAIN ANALYZE</code>.</li>
            <li><b>Physics Validity:</b> Будь-яка зміна в математичних моделях повинна бути погоджена з головним інженером проекту.</li>
            <li><b>Audit Logs:</b> Кожна критична помилка ядра повинна логуватися з повним Traceback для подальшого RCA.</li>
            <li><b>Security:</b> Не допускайте передачу невалідованих вхідних параметрів безпосередньо в SQL-запити.</li>
        </ul>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="./atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
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
