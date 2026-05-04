# Технічна специфікація: Сервісний Рівень Системи (SYSTEM SERVICE LAYER)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM MIDDLEWARE | SERVICE ORCHESTRATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛠️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Пакет Сервісів</h1>
            <p class="mega-subtitle">Оркестраційний шар проекту ATLAS: управління життєвим циклом даних, міграції, інтелектуальне наповнення (Seeding) та сервіси "Цифрового Двійника" для реалізації бізнес-логіки енергомоніторингу</p>
            <div class="status-tags"><span class="tag tag-online">SERVICES ACTIVE</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">SERVICE MIDDLEWARE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Data</span><span class="metric-value">Migration & Ingestion Services</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧪</div><div class="metric-info"><span class="metric-label">Simulation</span><span class="metric-value">Digital Twin Virtual Sensors</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Logic</span><span class="metric-value">Cross-Layer Orchestration</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Middleware Validation Layer</span></div></div>
</div>

<!-- SECTION 01: SERVICE LAYER PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Сервісного Рівня</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/services/</code> є "М'язами" та "Оркестром" проекту ATLAS. Якщо ядро (Core) забезпечує фундаментальні можливості, то сервісний рівень перетворює їх на корисні бізнес-функції. Наша філософія базується на <b>Ізоляції Бізнес-логіки</b>: сервіси виступають посередниками (Middleware), які координують потоки даних між "сирими" таблицями БД та високорівневими UI-компонентами. Це дозволяє реалізувати складні сценарії (як-от автоматична міграція схеми при оновленні версії або динамічна генерація телеметрії) без перевантаження коду інтерфейсу, забезпечуючи архітектурну чистоту та легкість підтримки системи.</p>
    </div>
</div>

<!-- SECTION 02: SERVICES ARCHITECTURE HIERARCHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Ієрархія архітектури сервісів (Service Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI("UI Layer (Views & Components)") --> SERV_ROOT("Services Root (__init__.py)")
    
    subgraph SERVICE_DOMAINS["Functional Service Modules"]
        SERV_ROOT --> DATA_SRV("data/: DB Migration & Seeding")
        SERV_ROOT --> SIM_SRV("simulation/: Digital Twin Engines")
        SERV_ROOT --> ANALY_SRV("analysis/: Expert Systems")
    end
    
    DATA_SRV --> CORE_DB("src.core.database")
    SIM_SRV --> CORE_PHYS("src.core.physics")
    
    CORE_DB --> STORAGE("Physical Persistence")
    CORE_PHYS --> REALITY("Virtual Grid State")
    </div></div>
</div>

<!-- SECTION 03: THE THREE SERVICE PILLARS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Три стовпи сервісного рівня ATLAS</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет реалізує три критичні домени для життєдіяльності системи:</p>
        <ul>
            <li><b>Data Lifecycle Services:</b> Повний цикл управління базою даних — від створення схеми (Migrate) до інтелектуального наповнення (Seeder) та імпорту реальних зовнішніх даних.</li>
            <li><b>Simulation & Virtualization:</b> Двигуни "Цифрового Двійника", які створюють віртуальну копію енергомережі, симулюючи роботу генераторів та навантаження підстанцій у реальному часі.</li>
            <li><b>Expert Analysis Logic:</b> Високорівневі алгоритми обробки інцидентів та координації аналітичних потоків, що готують дані для візуалізації.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: SERVICE RESPONSIBILITY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця відповідальності сервісів</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Підпакет / Модуль</th>
                    <th>Спеціалізація</th>
                    <th>Взаємодія з ядром</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>data/db_seeder.py</td><td>Data Synthesis</td><td>Core.Database / Core.Physics</td></tr>
                <tr><td>data/migrate_db.py</td><td>Schema Evolution</td><td>Core.Database (Raw Execute)</td></tr>
                <tr><td>simulation/</td><td>Virtual Telemetry</td><td>Core.Physics (Models)</td></tr>
                <tr><td>analysis/</td><td>Context Extraction</td><td>Core.Analytics (Engines)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: ORCHESTRATION & DATA FLOW REGISTRY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Оркестрація та реєстр потоків даних</h2></div>
    <div class="glass-card flow-step">
        <p>Сервісний рівень діє за принципом <b>Workflow Orchestration</b>. Наприклад, при старті системи сервіси <code>data</code> спочатку перевіряють версію бази, за потреби проводять міграцію, а потім викликають <code>seeder</code> для наповнення системи, якщо вона порожня. Весь цей складний ланцюжок ініціалізації прихований за простим інтерфейсом сервісного рівня, що дозволяє вищим шарам (UI) отримувати вже готову до роботи систему, не піклуючись про внутрішню послідовність кроків.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (SERVICE DISPATCHER) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Диспетчера Сервісів (Service Root Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>MODULE src.services:
    1. INITIALIZE_SERVICE_DOMAINS:
           REGISTER data_services (Seeding, Migrations)
           REGISTER simulation_services (Digital Twin)
           REGISTER expert_services (Analysis)
           
    2. COORDINATE_MIDDLEWARE:
           - Intercept UI requests
           - Prepare Core resources (DB/Physics)
           - Execute high-level business logic
           - Return enriched results to UI
           
    3. LIFECYCLE_MANAGEMENT:
           Handle graceful startup and shutdown of system services.
END MODULE</code></pre>
    </div>
</div>

<!-- SECTION 07: CROSS-LAYER INTEGRATION (THE MIDDLEWARE ROLE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Міжшарова інтеграція (Роль Middleware)</h2></div>
    <div class="glass-card flow-step">
        <p>Сервісний рівень ATLAS виконує критичну роль **Middleware**. Він захищає ядро від надмірних запитів UI та, навпаки, захищає UI від складності реалізації ядра. Наприклад, коли користувач натискає "Generate Data", UI не викликає SQL-команди безпосередньо. Він надсилає сигнал у сервісний рівень, який самостійно завантажує фізичні моделі, відкриває транзакції в БД та координує пакетний запис, повертаючи в UI лише статус успішного виконання операції.</p>
    </div>
</div>

<!-- SECTION 08: ERROR ABSTRACTION & SYSTEM STABILITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Абстракція помилок та стабільність системи</h2></div>
    <div class="glass-card flow-step">
        <p>Сервіси забезпечують уніфіковану обробку виняткових ситуацій. Замість того, щоб прокидати низькорівневі помилки <code>psycopg2</code> або <code>numpy</code> в інтерфейс, сервісний шар ловить їх, логує в <code>system.log</code> та трансформує у зрозумілі для користувача повідомлення про стан системи. Це підвищує надійність ATLAS: навіть якщо один сервіс (наприклад, імпорт зовнішніх даних) дає збій, інші сервіси продовжують функціонувати, а користувач отримує адекватний фідбек.</p>
    </div>
</div>

<!-- SECTION 09: EXTENSIBILITY & PLUGGABLE ARCHITECTURE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Розширюваність та плагінна архітектура</h2></div>
    <div class="glass-card flow-step">
        <p>Структура пакета <code>services/</code> розроблена для легкого масштабування. Якщо потрібно додати нову функціональність (наприклад, "Модуль прогнозування на базі нейромереж"), розробнику достатньо створити нову директорію всередині <code>src/services/</code> та зареєструвати її інтерфейси. Це дозволяє системі ATLAS рости модульно, не перетворюючи кодову базу на заплутаний моноліт, що є критичним для довготривалих інженерних проектів.</p>
    </div>
</div>

<!-- SECTION 10: ACADEMIC SIGNIFICANCE (BUSINESS LOGIC DECOUPLING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Академічна значущість (Business Logic Decoupling)</h2></div>
    <div class="glass-card flow-step">
        <p>Для академічного захисту пакет <code>services/</code> демонструє майстерність у **Розділенні відповідальностей** (Separation of Concerns). Наявність виділеного сервісного шару підтверджує, що архітектура проекту ATLAS спроектована за стандартами Enterprise-систем. Це дозволяє автору тезису аргументувати надійність, тестованість та гнучкість системи, демонструючи, як технічні можливості ядра трансформуються у прикладну цінність для енергетичного моніторингу через структуровані сервісні інтерфейси.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>System Core</h4>
                <p>Низькорівневі ресурси (БД, Логіка, Логер), на яких будуються сервіси.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🗺️</div>
            <div class="role-content">
                <h4>UI Layer</h4>
                <p>Головний споживач сервісів для реалізації користувацьких сценаріїв.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Data Stores</h4>
                <p>Кінцеві точки збереження результатів роботи сервісів (PostgreSQL).</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (DISTRIBUTED SERVICES) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v2.0 (Distributed Services)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується перехід до **Мікросервісного оркестру**. Окремі сервіси (наприклад, симуляція) будуть винесені в незалежні Docker-контейнери, що дозволить масштабувати ATLAS на великі кластери. Також буде додано підтримку <b>Event-driven архітектури</b> на базі Redis або RabbitMQ, де сервіси зможуть обмінюватися повідомленнями про події в мережі в асинхронному режимі, забезпечуючи ще вищу швидкість реакції системи.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Пакет Сервісів</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чи можна запустити ATLAS без сервісу симуляції?</b> — Так, але в такому випадку ви зможете працювати лише з уже наявними історичними даними в базі.</p>
        <p><b>Як додати нову міграцію БД?</b> — Додайте SQL-файл у папку <code>sql/</code> та оновіть логіку в <code>services/data/migrate_db.py</code>.</p>
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
