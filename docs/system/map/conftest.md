# Технічний Паспорт Компонента: tests/conftest.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🧬 INFRASTRUCTURE & ISOLATION CORE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">conftest.py</h1>
            <p class="mega-subtitle">Оркестратор тестового середовища, ізоляції транзакцій та синтетичних Mock-пакетів</p>
            <div class="status-tags">
                <span class="tag tag-online">TEST RUNNER ENGINE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">QUALITY GATE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Isolation Strategy</span>
            <span class="metric-value">Full Rollback</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-info">
            <span class="metric-label">Session Scope</span>
            <span class="metric-value">Engine Level</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Mock Generatives</span>
            <span class="metric-value">Time-Series</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧠</div>
        <div class="metric-info">
            <span class="metric-label">Tensor Mocks</span>
            <span class="metric-value">shape=(24, 9)</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Системна архітектура та роль</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>tests/conftest.py</code> є фундаментом інфраструктури автоматизованого тестування проєкту <b>Energy Monitor Ultimate</b>. Він визначає набір глобальних фікстур (fixtures) для фреймворку Pytest, які вирішують дві головні проблеми:
        </p>
        <ol style="margin-left: 20px; color: var(--text-dim); margin-top: 10px;">
            <li><strong>Ізоляція стану бази даних (Database Hermeticity):</strong> Кожен окремий тест, що взаємодіє з базою PostgreSQL, виконується в межах окремої ізольованої транзакції. Після завершення тесту транзакція автоматично відкочується (Rollback), гарантуючи відсутність забруднення БД та побічних ефектів між тестами.</li>
            <li><strong>Уніфіковані джерела даних (Consistent Mocking):</strong> Надає готові синтетичні набори даних у форматах <code>pandas.DataFrame</code> та <code>numpy.ndarray</code>, що точно емулюють реальні структури даних енергосистеми та часові ряди для LSTM нейромережі.</li>
        </ol>
    </div>
</div>

<!-- SECTION 2: TRANSACTION FLOW & ARCHITECTURE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Життєвий цикл ізольованого тесту (Transaction Lifecycle)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема нижче демонструє, як фікстура <code>db_session</code> та <code>db_cursor</code> створюють герметичний контейнер виконання:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            sequenceDiagram
                autonumber
                participant Runner as Pytest Runner
                participant Conf as conftest.py
                participant Engine as SQLAlchemy Engine
                participant DB as PostgreSQL Server
                participant Test as Test Case
                
                Runner->>Conf: Запит фікстури db_session
                Conf->>Engine: Створення з'єднання (connect)
                Engine->>DB: Відкриття транзакції (BEGIN TRANSACTION)
                Conf->>Runner: yield session (передача в тест)
                Runner->>Test: Виконання операцій запису/зчитування
                Test->>DB: Зміна стану (INSERT/UPDATE/DELETE)
                Test->>Runner: Завершення Assertions
                Runner->>Conf: Повернення керування (Teardown)
                Conf->>DB: Скасування змін (ROLLBACK)
                Conf->>Engine: Закриття з'єднання (close)
                Note over DB,Engine: База даних повертається до початкового стану!
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Аналіз фікстур та математичних генераторів</h2>
    </div>
    <div class="glass-card">
        <p style="margin-bottom: 15px;">
            У модулі реалізовано 7 ключових фікстур, детальний опис яких наведено нижче:
        </p>
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. db_engine() (Scope: session)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Глобальна фікстура рівня сесії. Ініціалізує єдиний SQLAlchemy Engine через системний виклик <code>get_engine()</code>. Після проходження всіх тестів викликає <code>engine.dispose()</code>, звільняючи всі фізичні пули з'єднань.
                </p>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. db_session(db_engine) (Scope: function)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Фікстура для SQLAlchemy ORM. Відкриває окреме з'єднання, стартує транзакцію через <code>connection.begin()</code>, після чого створює інстанс <code>Session</code>. На Teardown-фазі виконує <code>transaction.rollback()</code> і закриває сесію.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. db_cursor() (Scope: function)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для низькорівневих сирих SQL-запитів через драйвер <code>psycopg2</code>. Ініціалізує чисте з'єднання до БД через системну конфігурацію <code>DB_CONFIG</code> та генерує cursor. Тест ізолюється аналогічним відкатом <code>conn.rollback()</code>.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">4. sample_dataframe() (Scope: function)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Генерує еталонний часовий ряд за 24 години для регіону "Київ" та підстанції "Київ ТЕС". Навантаження формується за лінійною функцією:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ L(t) = 100 + 2 * t, &nbsp;&nbsp;&nbsp; G(t) = 95 + 1.5 * t, &nbsp;&nbsp;&nbsp; H(t) = 0.9 &nbsp;&nbsp; (∀ t ∈ [0, 23]) $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Де L(t) - активне навантаження в МВт, G(t) - генерація в МВт, H(t) - індекс технічного стану (Health Score).
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">5. sample_forecast_data()</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Повертає рандомізований 3D-тензор для емуляції вхідних ознак (features) LSTM нейромережі. Форма тензора є наступною:
                </p>
                <div style="font-family: monospace; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; display: inline-block; color: var(--text-main); font-size: 13px;">
                    shape = (24, 9) -> dtype = np.float32
                </div>
                <p style="margin: 8px 0 0 0; font-size: 13.5px; color: var(--text-dim);">
                    Це відповідає вікну довжиною 24 години, що містить 9 ознак телеметрії (навантаження, генерація, температура, день тижня, циклічні косинуси/синуси тощо).
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE / BEHAVIOR -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму транзакційної ізоляції</h2>
    </div>
    <div class="glass-card">
        <p>
            Для розуміння низькорівневої механіки роботи фікстури <code>db_session</code> наведено спрощений псевдокод:
        </p>
        <pre><code class="language-python">
# Псевдокод життєвого циклу сесії в pytest
def db_session_lifecycle(engine):
    # Setup фаза
    connection = engine.connect()
    transaction = connection.start_transaction()
    session = Session(bind=connection)
    
    try:
        # Передача керування у тестовий випадок
        yield session
    finally:
        # Teardown фаза
        session.close()
        transaction.rollback()  # Скасовує абсолютно всі INSERT/UPDATE/DELETE операції
        connection.close()
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ & TROUBLESHOOTING -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Часті питання та розв'язання проблем (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому тести іноді блокують таблиці в базі даних?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Це зазвичай відбувається, якщо під час тесту сесія зависає або виникає дедлок (Deadlock) на рівні PostgreSQL через паралельні процеси. Фікстура <code>db_session</code> використовує <code>transaction.rollback()</code>, що автоматично знімає всі ексклюзивні блокування рядків (Row Locks), створені в межах цієї транзакції.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Для чого використовується scope="session" для db_engine?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Створення SQLAlchemy Engine - це відносно "дорога" операція, яка займає до 200-500мс і створює пул підключень. Перевикористання одного інстансу на рівні всієї тестової сесії оптимізує загальну швидкість виконання тестів у 10+ разів.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як правильно додати нову фікстуру даних?</h4>
        <p style="color: var(--text-dim);">
            A: Достатньо додати нову функцію з декоратором <code>@pytest.fixture</code> в <code>conftest.py</code>. Всі тестові файли в директорії <code>tests/</code> отримають до неї автоматичний доступ без явного імпорту.
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
