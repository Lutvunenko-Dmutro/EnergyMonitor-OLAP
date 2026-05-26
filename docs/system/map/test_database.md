# Технічний Паспорт Компонента: tests/test_database.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🗄️ DATABASE SCHEMA & INTEGRITY AUDITOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">💾</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">test_database.py</h1>
            <p class="mega-subtitle">Система верифікації цілісності схеми даних, довідників та OLAP-архівів</p>
            <div class="status-tags">
                <span class="tag tag-online">DATABASE SHIELD</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">INTEGRITY GUARD</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-info">
            <span class="metric-label">Driver</span>
            <span class="metric-value">SQLAlchemy / pg</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📂</div>
        <div class="metric-info">
            <span class="metric-label">Monitored Tables</span>
            <span class="metric-value">5 Core Tables</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">💎</div>
        <div class="metric-info">
            <span class="metric-label">Static Substation</span>
            <span class="metric-value">ID 10 (1500 MW)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📈</div>
        <div class="metric-info">
            <span class="metric-label">OLAP Database</span>
            <span class="metric-value">LoadMeasurements</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Системний аудит та стабільність бази даних</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>tests/test_database.py</code> є виділеним сенсором якості для перевірки працездатності, схеми та базового наповнення бази даних <b>PostgreSQL</b>. Будучи фундаментом всієї системи моніторингу енергоспоживання, база даних має відповідати суворим вимогам цілісності структури та наявності незмінних системних констант (Static Data).
        </p>
        <p style="margin-top: 10px;">
            Він виконує 4 рівні верифікації:
        </p>
        <ol style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Низькорівневий коннект (L1 Connectivity):</strong> Перевіряє фізичну доступність порту СУБД та можливість виконання базових операцій (<code>SELECT 1</code>).</li>
            <li><strong>Цілісність схеми (L2 Schema Integrity):</strong> Автоматично зчитує системний каталог PostgreSQL <code>information_schema.tables</code> для перевірки наявності всіх життєво важливих таблиць.</li>
            <li><strong>Статичний референс (L3 Reference Verification):</strong> Переконується, що еталонні географічні та інженерні вузли (наприклад, опорна підстанція з ID 10) присутні в базі та мають правильну паспортну потужність.</li>
            <li><strong>OLAP-базис (L4 Time-Series Presence):</strong> Валідує доступність таблиці телеметричних вимірювань <code>LoadMeasurements</code>.</li>
        </ol>
    </div>
</div>

<!-- SECTION 2: GRAPHICAL SCHEMA CHECK -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Схема валідації СУБД (Postgres Schema Verification Structure)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема відображає ієрархічну перевірку бази даних від підключення до конкретних записів:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                DB_ENGINE("SQLAlchemy db_engine") --> TEST_CONN("1. Test connection: SELECT 1")
                
                TEST_CONN -- "Успішно (1)" --> TEST_SCHEMA("2. Test Schema Integrity")
                TEST_CONN -- "Помилка" --> FAIL_CONN("Connection Fail")
                
                TEST_SCHEMA --> T_REG("regions")
                TEST_SCHEMA --> T_SUB("substations")
                TEST_SCHEMA --> T_LOAD("loadmeasurements")
                TEST_SCHEMA --> T_GEN("generators")
                TEST_SCHEMA --> T_ALERTS("alerts")
                
                T_REG & T_SUB & T_LOAD & T_GEN & T_ALERTS -- "Всі таблиці присутні" --> TEST_STATIC("3. Test Static Reference Data")
                
                TEST_STATIC --> CHECK_SUB10("ПС Київська-Центральна (ID=10)")
                CHECK_SUB10 -- "Capacity = 1500.0 MW" --> TEST_OLAP("4. Test LoadMeasurements (OLAP)")
                
                TEST_OLAP --> COUNT_ROWS("SELECT COUNT(*)")
                COUNT_ROWS -- "Count > 0" --> READ_FIRST("SELECT actual_load_mw LIMIT 1")
                READ_FIRST -- "Not None" --> SUCCESS("Database Status: OK")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Детальний розбір валідаційних тестів</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. test_db_connection(db_engine)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Використовує підключення <code>db_engine.connect()</code> для виконання найшвидшого SQL-запиту:
                </p>
                <div style="font-family: monospace; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; display: inline-block; color: var(--accent); font-size: 13px; margin-bottom: 8px;">
                    SELECT 1
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Цей тест гарантує, що драйвери psycopg2 та конфігурація з'єднання в файлі <code>properdocs.yml</code> або системних змінних налаштовані правильно, а база даних готова приймати запити.
                </p>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. test_schema_integrity(db_engine)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Верифікує наявність 5 основних таблиць. Замість ризикованого прямого запиту в таблиці, який може завісити сесію через велику кількість рядків, тест опитує системну мета-таблицю <code>information_schema.tables</code>:
                </p>
                <div style="font-family: monospace; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; display: block; color: var(--text-main); font-size: 13px; overflow-x: auto; margin-bottom: 8px;">
                    SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :table)
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Параметризований запит передає кожну назву таблиці окремо. Якщо повертається <code>False</code>, тест видає детальне повідомлення про помилку: <i>"Таблиця {table} відсутня в схемі"</i>.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. test_static_data_presence(db_session)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Перевіряє коректність ініціалізації бази даних статичним сідером (seeder). Звертається до підстанції з ID=10:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ substation_name = 'ПС Київська-Центральна' &nbsp;&nbsp;&nbsp;&amp;&nbsp;&nbsp;&nbsp; capacity_mw = 1500.0 $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Якщо цей запис відсутній або значення полів відрізняються від еталонних, це вказує на те, що процедура первинного розгортання схеми (ETL / Migration) пройшла некоректно.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">4. test_load_measurements_stats(db_session)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Перевіряє таблицю вимірювань <code>LoadMeasurements</code>. Тест є стійким до порожньої бази даних: спочатку перевіряється, що кількість рядків є невід'ємною <code>res[0] >= 0</code>. Якщо база наповнена (рядків > 0), виконується додатковий запит для верифікації першого значення навантаження, переконуючись, що воно не є порожнім (<code>not None</code>).
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод запиту метаданих схеми</h2>
    </div>
    <div class="glass-card">
        <p>
            Для перевірки наявності таблиць використовується наступний параметризований SQL-шаблон:
        </p>
        <pre><code class="language-sql">
-- Псевдокод запиту перевірки схеми
SELECT EXISTS (
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
      AND table_name = :table_name
);
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ & SYSTEM TUNING -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Часті питання (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому перевіряється саме підстанція з ID 10?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Згідно зі специфікацією проєкту <code>generator_constants.py</code>, ПС Київська-Центральна з ID=10 є головним вузлом балансування столичного регіону. Її номінальна потужність (1500 МВт) є опорним обмеженням для розрахунку перевантажень та генерації аномальних алертів. Відсутність цієї підстанції у довіднику унеможливить будь-які симуляційні розрахунки.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Що робити, якщо тест схеми падає з помилкою відсутності таблиці?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Це означає, що база даних не була проініціалізована. Вам необхідно запустити оркестратор міграцій та посіву даних: <code>python src/services/data/db_seeder.py</code> для відновлення еталонної структури схеми.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Чи можу я паралельно запустити ці тести з іншими?</h4>
        <p style="color: var(--text-dim);">
            A: Так. Оскільки всі тести бази даних використовують фікстуру <code>db_session</code> з автоматичним відкатом транзакції, будь-які паралельні запити не будуть заважати один одному і не створять конфліктів даних.
        </p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn">
        <span class="btn-icon">🔙</span>
        <span class="btn-text">Повернутися до Атласу</span>
    </a>
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
