# Технічна специфікація: Хаб Сервісів Управління Даними (DATA SERVICES HUB)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATA LIFECYCLE | ETL & MIGRATION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">💾</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Центр Даних</h1>
            <p class="mega-subtitle">Оркестрація життєвого циклу даних ATLAS: від інтелектуального засівання бази (Seeding) до міграції схем та імпорту реальних промислових датасетів</p>
            <div class="status-tags"><span class="tag tag-online">ETL ACTIVE</span><span class="tag tag-version">v2.8.0</span><span class="tag tag-role">DATA LOGISTICS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🌱</div><div class="metric-info"><span class="metric-label">Seeding</span><span class="metric-value">Synthetic Data Engine</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Migration</span><span class="metric-value">Schema Evolution Logic</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📥</div><div class="metric-info"><span class="metric-label">Import</span><span class="metric-value">Real-world Data Sourcing</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Integrity</span><span class="metric-value">ACID Compliance Checks</span></div></div>
</div>

<!-- SECTION 01: ARCHITECTURAL SIGNIFICANCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Архітектурна Значущість Сервісів Даних</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/services/data/</code> є фундаментом "Цифрового Фундаменту" проекту. В системах масштабу ATLAS дані є найціннішим активом. Ці сервіси забезпечують, щоб база даних завжди була актуальною, структурованою та готовою до аналітики. Ми автоматизуємо процеси наповнення системи тестовими даними (Seeding), що критично для розробки ML-моделей, та керуємо еволюцією схеми БД (Migration) без зупинки основного сервісу.</p>
    </div>
</div>

<!-- SECTION 02: DATA MANAGEMENT MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Матриця Управління Даними</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль</th>
                    <th>Призначення</th>
                    <th>Ключові Технології</th>
                    <th>Операція</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>db_seeder.py</code></td><td>Генерація еталонів</td><td>Numpy / Random / SQL</td><td>Наповнення</td></tr>
                <tr><td><code>db_services.py</code></td><td>Бізнес-логіка БД</td><td>SQLAlchemy / Raw SQL</td><td>CRUD</td></tr>
                <tr><td><code>migrate_db.py</code></td><td>Еволюція схеми</td><td>DDL Scripts</td><td>Міграція</td></tr>
                <tr><td><code>import_real_data.py</code></td><td>Зовнішня інтеграція</td><td>Pandas / CSV / ETL</td><td>Імпорт</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: SYNTHETIC DATA SEEDING STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Засівання Синтетичних Даних</h2></div>
    <div class="glass-card flow-step">
        <p>Для навчання моделей та тестування інтерфейсу ми розробили <b>Intelligent Seeder</b>. Він не просто створює випадкові числа, він генерує фізично коректні часові ряди, враховуючи добові ритми, сезонні тренди та кореляцію між навантаженням та температурою. Це дозволяє розробникам працювати в середовищі, максимально наближеному до реальності, навіть за відсутності живого стріму даних.</p>
    </div>
</div>

<!-- SECTION 04: DATA PIPELINE ARCHITECTURE -->
<div class="section-container" id="db-seeder">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Архітектура Конвеєра Даних</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    SEED("db_seeder.py: Seed Data") --> DB[("PostgreSQL / Neon")]
    IMPORT("import_real_data.py: Real Data") --> DB
    
    subgraph DB_MGMT["Database Lifecycle Management"]
        MIGRATE("migrate_db.py: Schema Evolution")
        SERVICES("db_services.py: Domain Operations")
    end
    
    DB <--> DB_MGMT
    DB_MGMT --> ANALYTICS("Analytics Layer")
    DB_MGMT --> UI("User Interface")
    </div></div>
</div>

<!-- SECTION 05: DATABASE SERVICES & DOMAIN LOGIC -->
<div class="section-container" id="database">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Сервіси БД та Доменна Логіка</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>db_services.py</code> інкапсулює складні SQL-запити у високорівневі Python-функції. Замість написання JOIN-ів у кожному UI-модулі, розробник просто викликає <code>get_latest_measurements()</code>. Це забезпечує чисту архітектуру (Clean Architecture) та дозволяє централізовано оптимізувати продуктивність запитів, впроваджуючи індекси та кешування там, де це необхідно.</p>
    </div>
</div>

<!-- SECTION 06: SCHEMA EVOLUTION & MIGRATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Еволюція Схеми та Міграції</h2></div>
    <div class="glass-card flow-step">
        <p>Проект ATLAS постійно розвивається, що вимагає змін у структурі таблиць. <code>migrate_db.py</code> керує цим процесом, забезпечуючи безпечне оновлення бази даних. Кожна міграція є ідемпотентною та супроводжується логуванням результатів, що гарантує цілісність структури даних при розгортанні на нових інстансах або хмарних вузлах.</p>
    </div>
</div>

<!-- SECTION 07: REAL-WORLD DATA IMPORT (ETL) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Імпорт Реальних Даних (ETL Процеси)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>import_real_data.py</code> реалізує повноцінний **ETL-конвеєр (Extract, Transform, Load)**. Він здатен обробляти промислові вибірки даних (наприклад, з систем SCADA або архівів енергокомпаній), проводити їх нормалізацію, валідацію типів та пакетну вставку (Batch Insert) у базу ATLAS. Це забезпечує можливість проведення ретроспективного аналізу реальних історичних подій в енергомережі.</p>
    </div>
</div>

<!-- SECTION 08: DATA CONSISTENCY & TRANSACTIONAL INTEGRITY -->
<div class="section-container" id="archive">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Консистентність та Транзакційна Цілісність</h2></div>
    <div class="glass-card flow-step">
        <p>Всі операції запису в сервісах даних захищені механізмами транзакцій. Якщо під час засівання бази або міграції стається збій, система автоматично відкочується до стабільного стану. Це запобігає появі "фрагментованих" даних, які могли б призвести до критичних помилок в аналітичних розрахунках або візуалізаціях.</p>
    </div>
</div>

<!-- SECTION 09: PERFORMANCE OPTIMIZATION (BATCH PROCESSING) -->
<div class="section-container" id="loader">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Оптимізація Продуктивності (Пакетна Обробка)</h2></div>
    <div class="glass-card flow-step">
        <p>При роботі з мільйонами записів телеметрії продуктивність є критичною. Наші сервіси використовують пакетну обробку даних (Bulk Operations), що в десятки разів швидше за поштучну вставку рядків. Це дозволяє системі ATLAS залишатися чутливою та швидко оновлювати аналітичні представлення навіть при масовому надходженні нових вимірів.</p>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v3.0 (AUTONOMOUS DATA STEWARD) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v3.0 (Data Steward)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Автономного Стюарда Даних**, який автоматично видалятиме застарілі архіви та оптимізуватиме індекси на основі статистики запитів користувачів. Також буде додано підтримку <i>Streaming ETL</i> для безпосередньої обробки потоків Kafka та впроваджено модулі автоматичної анонімізації персональних даних споживачів для відповідності GDPR.</p>
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
