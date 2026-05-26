# Технічний Паспорт Активу: data/energy.db (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🗄️ LOCAL RELATIONAL DATA NODE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🗄️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">База даних: energy.db</h1>
            <p class="mega-subtitle">Локальне реляційне сховище телеметрії, генерації, аномалій та системних конфігурацій екосистеми ATLAS</p>
            <div class="status-tags">
                <span class="tag tag-online">DATABASE ACTIVE</span>
                <span class="tag tag-version">v3.5.0</span>
                <span class="tag tag-role">SQLITE STORAGE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">💾</div>
        <div class="metric-info">
            <span class="metric-label">Database Engine</span>
            <span class="metric-value">SQLite 3.x</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Data Tables</span>
            <span class="metric-value">5 Key Entities</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-info">
            <span class="metric-label">Primary Indexes</span>
            <span class="metric-value">Timestamp / Substation</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Integrity</span>
            <span class="metric-value">ACID Compliant</span>
        </div>
    </div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення та архітектурна роль</h2></div>
    <div class="glass-card flow-step">
        <p>
            Локальна база даних SQLite <code>data/energy.db</code> виконує роль головного автономного сховища даних для системи <i>Energy Monitor Ultimate</i>. Вона виступає локальним дзеркалом та кешованим шаром (Caching Layer) для хмарних даних, гарантуючи безперебійне функціонування інтерфейсів користувача та ML-моделей навіть за умов повної відсутності інтернет-з'єднання з Neon DB PostgreSQL. База даних зберігає часові ряди споживання електроенергії, дані про виробіток генерації, журнали аномальних подій (алертів) та топологію магістральних ліній електропередачі.
        </p>
        <p style="margin-top: 10px;">
            Основні функції реляційного вузла:
        </p>
        <ul>
            <li><strong>High-Speed Telemetry Retrieval:</strong> Надання швидкого доступу до часових рядів навантаження підстанцій для аналітичних розрахунків.</li>
            <li><strong>Incident Logging:</strong> Збереження історії системних аномалій, перевантажень та відхилень частоти/напруги від норми.</li>
            <li><strong>Grid Topology Sourcing:</strong> Опис фізичних параметрів ліній (опори, пропускна спроможність), які використовуються у фізичному двигуні <code>physics.py</code>.</li>
            <li><strong>Local Caching Node:</strong> Зниження навантаження на мережевий трафік шляхом кешування проміжних результатів та результатів прогнозування ML.</li>
        </ul>
    </div>
</div>

<!-- SECTION 02: DATABASE SCHEMAS & RELATIONSHIPS (ERD) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема даних (ERD топологія)</h2></div>
    <div class="glass-card">
        <p style="margin-bottom: 15px; color: var(--text-dim);">
            Нижче наведено реляційну структуру локальної бази даних, яка повністю відповідає концепції цифрового двійника (Digital Twin) енергосистеми:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            erDiagram
                load_data {
                    INTEGER id PK
                    TEXT timestamp
                    TEXT substation
                    REAL load_mw
                    TEXT region
                }
                generation_data {
                    INTEGER id PK
                    TEXT timestamp
                    TEXT source_type
                    REAL output_mw
                    REAL efficiency
                }
                alerts_data {
                    INTEGER id PK
                    TEXT timestamp
                    TEXT substation
                    TEXT alert_level
                    TEXT message
                    INTEGER resolved
                }
                transmission_lines {
                    INTEGER id PK
                    TEXT name
                    TEXT source_substation
                    TEXT target_substation
                    REAL capacity_mw
                    REAL resistance_ohm
                    REAL reactance_ohm
                }
                financial_data {
                    INTEGER id PK
                    TEXT timestamp
                    REAL tariff_rate
                    REAL revenue
                    REAL losses_cost
                }
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Математична модель втрат та фінансового аудиту</h2></div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Розрахунок вартості втрат у мережі</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Вартість втраченої електроенергії $C_{\text{loss}}$ на годину розраховується на основі фізичних втрат $P_{\text{loss}}$ (MW) та діючого тарифного плану $T_{\text{rate}}$ (USD/MWh):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ C_{\text{loss}} = P_{\text{loss}} \cdot T_{\text{rate}} \quad (\text{USD/h}) $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Співвідношення інтеграції даних</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Корисний відпуск електроенергії $E_{\text{net}}$ за період $\Delta t$ визначається інтегралом різниці між генерацією та втратами:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ E_{\text{net}} = \int_{t_1}^{t_2} \left( \sum P_{\text{gen}} - \sum P_{\text{loss}} \right) dt \quad (\text{MWh}) $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 04: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Псевдокод підключення та агрегації телеметрії</h2></div>
    <div class="glass-card">
        <p>
            Псевдокод демонструє приклад високопродуктивного зчитування та агрегації даних з <code>energy.db</code> за допомогою SQLite3 та Pandas:
        </p>
        <pre><code class="language-python">
# Псевдокод підключення та агрегації даних локальної БД
import sqlite3
import pandas as pd

def fetch_aggregated_load_stats(db_path: str, region: str) -> pd.DataFrame:
    """
    Здійснює підключення до локального реляційного вузла, 
    проводить агрегацію погодинних втрат та навантажень для вказаного регіону.
    """
    # 1. Створення стабільного з'єднання
    conn = sqlite3.connect(db_path)
    
    # 2. Оптимізований SQL-запит з використанням індексів
    query = """
        SELECT 
            strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
            substation,
            AVG(load_mw) as avg_load_mw,
            MAX(load_mw) as peak_load_mw
        FROM load_data
        WHERE region = ?
        GROUP BY hour, substation
        ORDER BY hour ASC
    """
    
    try:
        # 3. Виконання запиту та автоматична конвертація в DataFrame
        df = pd.read_sql_query(query, conn, params=(region,))
        df['hour'] = pd.to_datetime(df['hour'])
        return df
    finally:
        # Гарантоване закриття з'єднання (Hygiene)
        conn.close()
        </code></pre>
    </div>
</div>

<!-- SECTION 05: TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Часті питання (FAQ)</h2></div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому для локального кешування обрано SQLite, а не повноцінний PostgreSQL?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: SQLite є вбудованою базою даних (Serverless), яка зберігає весь масив даних в одному файлі на диску. Вона не вимагає запуску фонових системних процесів (демонів), адміністрування прав доступу або виділення мережевих портів. Це робить її ідеальною для використання на клієнтських комп'ютерах диспетчерів та забезпечує миттєвий старт додатка при локальному запуску.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Які індекси створено в базі даних для оптимізації швидкості запитів?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: База даних містить два складені індекси (Composite Indexes): <code>idx_load_time_sub</code> (по полях <code>timestamp</code> та <code>substation</code> у таблиці <code>load_data</code>) та <code>idx_gen_time_type</code> (у таблиці <code>generation_data</code>). Це скорочує час виконання інтервальних аналітичних запитів у середньому на 85% у порівнянні з неіндексованими таблицями.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Що відбувається при одночасному записі даних з декількох потоків?</h4>
        <p style="color: var(--text-dim);">
            A: SQLite підтримує блокування на рівні всього файлу бази даних (Database-level locking) при виконанні операцій запису. Для уникнення виникнення помилок <code>sqlite3.OperationalError: database is locked</code>, сервіси системи ATLAS використовують пул з'єднань з налаштованим параметром <code>timeout = 30.0</code> (секунд), що дозволяє потокам безпечно чекати завершення попередніх транзакцій у черзі.
        </p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">Повернутися до Атласу</span></a>
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
