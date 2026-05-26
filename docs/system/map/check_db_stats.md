# Технічний Паспорт Компонента: scripts/system/check_db_stats.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">📊 DATABASE STATISTICS & HEALTH MONITOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🗄️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">check_db_stats.py</h1>
            <p class="mega-subtitle">Утиліта глибокого аудиту фізичного об'єму та моніторингу системних таблиць бази даних PostgreSQL</p>
            <div class="status-tags">
                <span class="tag tag-online">DATABASE UTILITY</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">PERFORMANCE WATCHDOG</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">💾</div>
        <div class="metric-info">
            <span class="metric-label">Target Engine</span>
            <span class="metric-value">PostgreSQL 15+</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔍</div>
        <div class="metric-info">
            <span class="metric-label">Metric API</span>
            <span class="metric-value">pg_catalog</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-info">
            <span class="metric-label">Execution Time</span>
            <span class="metric-value">&lt; 150 ms</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Security Scope</span>
            <span class="metric-value">Read-Only Audit</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль та архітектурне призначення</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/system/check_db_stats.py</code> виконує роль <strong>оперативного монітора та аудитора фізичного стану</strong> бази даних PostgreSQL платформи <i>Energy Monitor Ultimate</i>. Він надає розробникам та адміністраторам точну інформацію про об'єм пам'яті на диску, що є критично важливим при безперервній високочастотній генерації телеметричних даних (до 100 000 записів щоденно).
        </p>
        <p style="margin-top: 10px;">
            Ключові технічні обов'язки утиліти:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Аудит дискового простору (Disk Space Auditing):</strong> Виклик низькорівневих функцій PostgreSQL для розрахунку повного об'єму файлів бази даних на фізичному накопичувачі.</li>
            <li><strong>Рейтинговий аналіз таблиць (Table Size Ranking):</strong> Виявлення топ-5 найбільших таблиць системи за сумарним об'ємом (включаючи TOAST-дані та індекси) для виявлення потенційних витоків або необхідності вакуумізації (VACUUM).</li>
            <li><strong>Діагностика підключень (Health Check):</strong> Швидке тестування працездатності та латентності PostgreSQL з'єднання через параметри оточення <code>.env</code>.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Процес аудиту бази даних (Database Audit Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Наступна схема демонструє послідовність кроків від ініціалізації з'єднання до форматованого виводу статистики в інтерфейс командного рядка (CLI):
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск check_db_stats.py") --> ENV("1. Завантаження параметрів з .env")
                ENV --> CONN("2. Встановлення з'єднання (psycopg2.connect)")
                
                CONN -- "Помилка авторизації / хоста" --> ERR("3a. Перехоплення виключення (Exception) & Вивід помилки")
                CONN -- "Успішно" --> CURS("3b. Створення системного курсору (cursor)")
                
                CURS --> SQL_DB("4. Запит pg_database_size: Загальний об'єм БД")
                SQL_DB --> SQL_TBL("5. Запит pg_total_relation_size: Топ-5 таблиць")
                
                SQL_TBL --> FORMAT("6. pg_size_pretty: Перетворення байтів у читабельний формат")
                FORMAT --> PRINT("7. Форматований вивід в консоль (stdout)")
                
                PRINT --> CLOSE("8. Закриття курсору та з'єднання (close)")
                CLOSE --> END("Завершення роботи")
                ERR --> END
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математика системних запитів та PostgreSQL функції</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Розрахунок фізичного розміру бази даних</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для визначення загального об'єму файлів на диску, що відповідають базі даних $D$, використовується функція <code>pg_database_size</code>. Вона підсумовує розмір усіх файлів у директорії <code>base/$OID</code>:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ S_{\text{total}} = \text{pg\_database\_size}(D) = \sum_{f \in \text{files}(D)} \text{size}(f) $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Сумарний розмір відношення (Table Relation Size)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для отримання чесного розміру таблиці $R$ використовується функція <code>pg_total_relation_size</code>. На відміну від <code>pg_relation_size</code>, вона враховує не лише основні дані (main fork), а й розмір індексів, TOAST-таблиці та карти вільних просторів (FSM/VM):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ S_{\text{relation}}(R) = S_{\text{data}}(R) + S_{\text{toast}}(R) + S_{\text{index}}(R) + S_{\text{fsm\_vm}}(R) $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Конвертація розмірів (Human Readable conversion)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Функція <code>pg_size_pretty</code> виконує логарифмічне масштабування байтів у кіло-, мега- чи гігабайти за базою $1024$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{Unit} = \left\lfloor \frac{\log_2(bytes)}{10} \right\rfloor \quad \implies \quad \text{Value} = \frac{bytes}{1024^{\text{Unit}}} $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму аудиту</h2>
    </div>
    <div class="glass-card">
        <p>
            Структура логіки запиту та виведення інформації:
        </p>
        <pre><code class="language-python">
# Псевдокод моніторингу простору БД
def run_db_size_audit():
    connection = connect_to_postgres(env_credentials)
    cursor = connection.cursor()
    
    # 1. Отримуємо загальний розмір БД
    cursor.execute("SELECT pg_size_pretty(pg_database_size('energy_monitor'))")
    db_size = cursor.fetchone()[0]
    print("Database total size:", db_size)
    
    # 2. Знаходимо найбільші таблиці
    cursor.execute("""
        SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
        FROM pg_catalog.pg_statio_user_tables
        ORDER BY pg_total_relation_size(relid) DESC
        LIMIT 5
    """)
    
    for table_name, table_size in cursor.fetchall():
        print(f"Table: {table_name} -> {table_size}")
        
    cursor.close()
    connection.close()
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Часті питання (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому використовується таблиця `pg_catalog.pg_statio_user_tables`?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Ця системна таблиця містить інформацію про статистику вводу-виводу для всіх користувацьких таблиць у поточному просторі імен. Звідси ми можемо отримати унікальний ідентифікатор відношення `relid`, необхідний для точного виклику `pg_total_relation_size`.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому важливо використовувати саме `pg_total_relation_size`, а не `pg_relation_size`?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Функція `pg_relation_size` повертає розмір виключно самої таблиці (тільки рядки даних). Проте індекси (особливо B-Tree індекси на великих таблицях телеметрії) та TOAST-сегменти (де зберігаються великі об'єми стиснутого тексту або JSON) можуть займати в 2-3 рази більше місця, ніж сама таблиця. `pg_total_relation_size` дає чесний сумарний об'єм дискового простору.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Що робити, якщо одна з таблиць телеметрії раптово виросла в розмірах?</h4>
        <p style="color: var(--text-dim);">
            A: Це може свідчити про накопичення "мертвих" рядків після масових операцій UPDATE чи DELETE (так зване роздуття - Table Bloat). У такому випадку рекомендується виконати очищення бази даних за допомогою команди `VACUUM FULL <table_name>` або скористатися утилітою `pg_repack` для відновлення місця на диску без блокування таблиці.
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
