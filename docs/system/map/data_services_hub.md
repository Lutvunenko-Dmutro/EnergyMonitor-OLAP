# 🗄️ Технічна специфікація: Шар Бази Даних (DATA SERVICES HUB / NEONGUARD)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATABASE SERVICES & CLOUD STORAGE ARCHITECTURE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🗄️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Центральний Хаб Даних</h1>
            <p class="mega-subtitle">Управління життєвим циклом даних: інтелектуальний доступ до Neon Cloud/PostgreSQL, транзакційні DDL-міграції, оптимізація RAM Memory Diet та стійке кешування</p>
            <div class="status-tags"><span class="tag tag-online">DATABASE ACTIVE</span><span class="tag tag-version">v3.2.0</span><span class="tag tag-role">DATA CORE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔌</div><div class="metric-info"><span class="metric-label">Engine</span><span class="metric-value">PostgreSQL / Neon</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧬</div><div class="metric-info"><span class="metric-label">RAM Savings</span><span class="metric-value">Memory Diet -70%</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Resilience</span><span class="metric-value">NeonGuard Retries</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Transactions</span><span class="metric-value">ACID Context Mgr</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальна Роль та Місія</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/core/database/</code> та сервіси <code>src/services/data/</code> забезпечують роботу «цифрового фундаменту» системи <b>ATLAS</b>. Цей шар відповідає за надійне зберігання телеметрії енергомереж, безшовну обробку транзакцій та забезпечення високої доступності як локального сховища PostgreSQL, так і хмарного кластера <b>Neon Cloud DB</b>. Завдяки механізмам динамічного перемикання та прогресивного очікування, інтерфейс користувача працює стабільно навіть під час холодного старту серверів бази даних.</p>
    </div>
</div>

<!-- SECTION 02: ADVANCED ALGORITHMS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математична та Системна Оптимізація</h2></div>
    <div class="glass-card flow-step">
        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-bottom: 10px;">1. Алгоритм прогресивного очікування (Neon Cold Start Delay)</h3>
        <p>Безкоштовні інстанси бази даних Neon Cloud «засинають» за відсутності активності. Для запобігання обриву з'єднання (Connection Refused), система реалізує прогресивну шкалу затримок повторних спроб підключення (Exponential Backoff):</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fff; margin: 15px 0; border: 1px solid var(--border);">
            $$ \text{WaitTime}(i) = i \cdot 6 + 4 \quad (\text{секунд}) $$
        </div>
        <p>Це забезпечує спроби з паузами <code>4c -> 10c -> 16c -> 22c</code>, даючи Neon DB до 60 секунд на повний запуск контейнера без падіння Streamlit-веб-додатка.</p>

        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-top: 20px; margin-bottom: 10px;">2. Протокол Memory Diet (RAM Optimization)</h3>
        <p>При імпорті великих аналітичних часових рядів, Pandas за замовчуванням виділяє надлишкову 64-бітну пам'ять. Наш метод <code>memory_diet()</code> оптимізує споживання RAM до 70%:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin: 15px 0;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Вихідний тип (Pandas)</th>
                    <th>Оптимізований тип</th>
                    <th>Результат економії</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>float64</code></td><td><code>float32</code></td><td>Зменшення ваги чисел на 50%</td></tr>
                <tr><td><code>int64</code></td><td><code>int16 / int32</code></td><td>Зменшення цілих чисел на 50% - 75%</td></tr>
                <tr><td><code>object</code> (повторювані рядки)</td><td><code>category</code></td><td>Економія до 80% за рахунок словникового стиснення</td></tr>
                <tr><td><code>datetime64[ns]</code></td><td><code>datetime64[s]</code></td><td>Зниження точності до секунд (економить 4x)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: ENTITY RELATIONSHIP DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема Бази Даних (ER-Diagram)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
erDiagram
    Regions ||--o{ Substations : "містить"
    Substations ||--o{ LoadMeasurements : "фіксує"
    Regions ||--o{ WeatherReports : "температура_в"
    
    Regions {
        int id PK
        string name "Назва регіону"
    }
    Substations {
        int id PK
        int region_id FK
        string name "Назва підстанції"
        float peak_load "Номінальна потужність МВт"
    }
    LoadMeasurements {
        int id PK
        int substation_id FK
        timestamp ts "Мітка часу UTC"
        float actual_load "Фактичне навантаження МВт"
        float health_score "Коефіцієнт зносу обладнання"
    }
    WeatherReports {
        int id PK
        int region_id FK
        timestamp ts "Час вимірювання"
        float temperature "Температура повітря C"
    }
</div></div>
</div>

<!-- SECTION 04: KEY METHODS & API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Сигнатури та Логіка Функцій API</h2></div>
    <div class="glass-card flow-step">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def run_query(query_text, params=None) -> pd.DataFrame</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);"><b>Основна точка доступу.</b> Виконує SQL-запити SELECT з інтелектуальними ретраями. При виникненні непереборної мережевої помилки автоматично підвантажує дані з локального Parquet-кешу.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def get_db_cursor() -> Generator[tuple, None, None]</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);"><b>Транзакційний Контекст-Менеджер.</b> Забезпечує ACID-сумісність операцій запису. При будь-якому збої (Exception) автоматично виконує операцію <code>ROLLBACK</code>, гарантуючи консистентність даних.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def memory_diet(df) -> pd.DataFrame</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);">Оптимізатор RAM. Проводить приведення типів даних та знижує навантаження на оперативну пам'ять веб-сервера.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 05: CONNECTION SEQUENCE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Життєвий Цикл Запиту до БД</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
sequenceDiagram
    participant App as Streamlit Application
    participant Core as Database Core
    participant Pool as SQLAlchemy Engine
    participant DB as Neon Cloud Cluster
    participant Cache as Parquet Fallback
    
    App->>Core: run_query(SQL, params)
    Core->>Pool: Request Connection
    Pool->>DB: Handshake (Connection Try)
    
    alt З'єднання успішне
        DB-->>Pool: Connected
        Pool-->>Core: Active Session
        Core->>DB: Execute Query
        DB-->>Core: Raw Result
        Core->>Cache: Save query_[hash].parquet
        Core-->>App: Pandas DataFrame (Memory Diet applied)
    else Neon DB спить / Мережева помилка
        DB-->>Pool: Timeout / Refused (Retry 1..5)
        Note over Core,Pool: Запуск NeonGuard Backoff
        Pool->>DB: Retry Connection
        DB-->>Pool: Connected (awake)
        Pool-->>Core: Active Session
        Core-->>App: Result DataFrame
    else База повністю офлайн (Всі спроби вичерпано)
        Core->>Cache: Read query_[hash].parquet
        Cache-->>Core: Cached Data
        Core-->>App: Fallback DataFrame (Offline Mode)
    end
</div></div>
</div>

<!-- SECTION 06: ETL SEED & DATA REPLICATION PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">ETL пайплайн та реплікація даних</h2></div>
    <div class="glass-card flow-step">
        <p>Для швидкого розгортання та тестування системи розроблено модуль <code>db_seeder.py</code>, який автоматично наповнює базу даних збалансованими синтетичними профілями споживання у випадку відсутності зв'язку з Kaggle. Алгоритм забезпечує консистентність завантажених даних на основі генераторів псевдовипадкових розподілів.</p>
        
        <h4 style="color: var(--accent); margin-top: 15px; font-family: 'Orbitron', sans-serif;">Реалізація транзакційного завантажувача (Seeder)</h4>
        <pre><code class="language-python">
# Псевдокод транзакційного імпорту та посіву даних
def seed_database(connection_string, num_days=30):
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # 1. Створення базових регіонів
        regions = [Region(name="AEP"), Region(name="COMED"), Region(name="DAYTON")]
        session.add_all(regions)
        session.flush() # Отримання ID без комміту
        
        # 2. Створення підстанцій для кожного регіону
        substations = []
        for r in regions:
            for s_idx in range(5):
                sub = Substation(
                    region_id=r.id, 
                    name=f"{r.name}_Sub_{s_idx}", 
                    peak_load=np.random.uniform(50.0, 500.0)
                )
                substations.append(sub)
        session.add_all(substations)
        session.flush()
        
        # 3. Транзакційний запис великого масиву вимірів
        start_time = datetime.now() - timedelta(days=num_days)
        batch = []
        for sub in substations:
            for hour in range(num_days * 24):
                ts = start_time + timedelta(hours=hour)
                load = sub.peak_load * (0.4 + 0.3 * math.sin(hour * math.pi / 12) + np.random.normal(0, 0.05))
                meas = LoadMeasurement(substation_id=sub.id, ts=ts, actual_load=max(0.0, load))
                batch.append(meas)
                
                # Запис батчами по 1000 записів для оптимізації швидкості
                if len(batch) >= 1000:
                    session.bulk_save_objects(batch)
                    batch = []
                    
        if batch:
            session.bulk_save_objects(batch)
            
        session.commit() # Фіксація всіх змін
        print("[SUCCESS] Seeding completed.")
    except Exception as e:
        session.rollback() # Скасування при будь-якій помилці
        print(f"[ERROR] Transaction rolled back: {e}")
    finally:
        session.close()
        </code></pre>
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
