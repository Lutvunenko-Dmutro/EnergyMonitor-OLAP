# Технічна специфікація: Ядро Системних Операцій та Фізики (CORE KERNEL HUB) (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">⚛️ SYSTEM CORE | PHYSICS & DATA ACCESS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Ядро Системи (core)</h1>
            <p class="mega-subtitle">Фундаментальний шар ATLAS: математичне моделювання фізичних процесів енергомережі, оркестрація низькорівневих SQL-запитів та інтелектуальне завантаження великих архівів Kaggle</p>
            <div class="status-tags">
                <span class="tag tag-online">KERNEL ACTIVE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">BASE INFRASTRUCTURE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">⚛️</div>
        <div class="metric-info">
            <span class="metric-label">Physics Engine</span>
            <span class="metric-value">Joule & Ohm Losses</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔍</div>
        <div class="metric-info">
            <span class="metric-label">Queries Bus</span>
            <span class="metric-value">Pre-compiled SQL Statements</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📂</div>
        <div class="metric-info">
            <span class="metric-label">Kaggle Loader</span>
            <span class="metric-value">Lazy Chunked CSV Reader</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Load Profiles</span>
            <span class="metric-value">Residential / Industrial / Commercial</span>
        </div>
    </div>
</div>

<!-- SECTION 01: ARCHITECTURAL FOUNDATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Архітектурний Фундамент Ядра</h2></div>
    <div class="glass-card flow-step">
        <p>
            Пакет <code>src/core/</code> є найнижчим та найбільш критичним шаром проєкту ATLAS. Це когнітивно-фізичний двигун системи, на якому базується вся вища бізнес-логіка. Тут реалізовано математичні абстракції законів електротехніки та здійснюється оркестрація роботи з персистентним сховищем даних (PostgreSQL/SQLite). Ядро забезпечує ізоляцію інфраструктури від інтерфейсу користувача та гарантує наукову та фізичну достовірність розрахованих параметрів мережі.
        </p>
        <p style="margin-top: 10px;">
            Основні компоненти шару <code>src/core/</code>:
        </p>
        <ul>
            <li><strong>physics.py:</strong> Фізичний симулятор втрат та падіння напруги в магістральних мережах на основі законів Джоуля-Ленца та Ома.</li>
            <li><strong>queries.py:</strong> Бібліотека оптимізованих, параметризованих та безпечних від SQL-ін'єкцій запитів до PostgreSQL.</li>
            <li><strong>config.py:</strong> Глобальний реєстр констант, параметрів симуляції та математичних добових Load Profiles для різних типів споживачів.</li>
            <li><strong>kaggle_loader.py:</strong> Розумний конвеєр імпорту великих часових рядів енергоспоживання (PJM datasets) з підтримкою Lazy Loading.</li>
            <li><strong>logger.py:</strong> Централізована система структурованого логування з фільтрацією подій за рівнями пріоритету.</li>
        </ul>
    </div>
</div>

<!-- SECTION 02: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичне моделювання та фізичні закони</h2></div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Розрахунок теплових втрат у лініях (Закон Джоуля-Ленца)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Теплові втрати активної потужності $P_{\text{loss}, i}$ для лінії $i$ з активним опором $R_i$ при проходженні струму $I_i$ розраховуються за формулою:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ P_{\text{loss}, i} = I_i^2 \cdot R_i \cdot 10^{-6} \quad (\text{MW}) $$
                </div>
                <p style="margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);">
                    Де струм $I_i$ виражається через активну потужність навантаження $P_i$ та номінальну лінійну напругу $U_{\text{nom}}$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ I_i = \frac{P_i}{\sqrt{3} \cdot U_{\text{nom}} \cdot \cos\varphi} \quad (\text{A}) $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Падіння напруги в магістралях (Закон Ома)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Падіння напруги $\Delta U_i$ на ділянці з повним імпедансом $Z_i = R_i + j X_i$ складає:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \Delta U_i = \frac{P_i \cdot R_i + Q_i \cdot X_i}{U_{\text{nom}}} \quad (\text{kV}) $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: INTERACTION PIPELINE (DIAGRAM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Життєвий цикл запиту в Ядрі</h2></div>
    <div class="glass-card">
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                UI_REQ("Користувацький запит (UI)") --> Q_ORCH["queries.py: Query Orchestrator"]
                Q_ORCH --> PG_DB[(PostgreSQL Analytics)]
                
                KAG_REQ("Запит на архівні дані") --> K_LOAD["kaggle_loader.py: Chunked Lazy Loader"]
                K_LOAD --> CSV_FILE[("PJM_hourly.csv Storage")]
                
                PG_DB & CSV_FILE --> DATA_FLOW["Потік сирих часових рядів"]
                DATA_FLOW --> PHYS_ENG["physics.py: Physics Simulator"]
                
                PHYS_ENG --> JOULE["Розрахунок втрат Джоуля-Ленца"]
                PHYS_ENG --> VOLT_DROP["Розрахунок падіння напруги"]
                
                JOULE & VOLT_DROP --> AN_OUT["Формування аналітичного DataFrame"]
                AN_OUT --> UI_RESP("Відображення на дашборді / Вхід для ML")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 04: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Алгоритм Lazy Chunked завантаження даних</h2></div>
    <div class="glass-card">
        <p>
            Псевдокод описує логіку роботи <code>kaggle_loader.py</code> для ефективного зчитування великих масивів часових рядів без перевантаження оперативної пам'яті:
        </p>
        <pre><code class="language-python">
def lazy_load_hourly_data(file_path, chunk_size=10000):
    """
    Покроково зчитує гігантський CSV-файл Kaggle чанками, 
    проводить фільтрацію на рівні ітератора та повертає оптимізований DataFrame.
    """
    import pandas as pd
    
    selected_columns = ['Datetime', 'PJME_MW']
    filtered_chunks = []
    
    # Використовуємо ітератор для економії RAM
    for chunk in pd.read_csv(file_path, chunksize=chunk_size, usecols=selected_columns):
        # 1. Приведення типів для економії пам'яті (Memory Diet)
        chunk['Datetime'] = pd.to_datetime(chunk['Datetime'])
        chunk['PJME_MW'] = chunk['PJME_MW'].astype('float32')
        
        # 2. Фільтрація аномальних значень (нульові або від'ємні навантаження)
        valid_data = chunk[chunk['PJME_MW'] > 0]
        filtered_chunks.append(valid_data)
        
    # Об'єднуємо відфільтровані фрагменти
    full_df = pd.concat(filtered_chunks, ignore_index=True)
    
    # Сортування за часом для забезпечення монотонності часового ряду
    full_df.sort_values(by='Datetime', inplace=True)
    return full_df
        </code></pre>
    </div>
</div>

<!-- SECTION 05: TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Технічний FAQ Ядра</h2></div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому Load Profiles у `config.py` захардкоджені по годинах, а не розраховуються динамічно?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Ці профілі (Residential, Industrial, Commercial) є нормалізованими математичними очікуваннями добового споживання. Вони виступають в ролі базових моделей (Baselines) для генератора симуляції та дозволяють оцінити відхилення реальних показників від теоретичних нормативів енергосистеми.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Яким чином `queries.py` запобігає SQL-ін'єкціям без використання ORM?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Замість конкатенації рядків типу <code>f"SELECT * FROM load WHERE id = {user_input}"</code>, ми використовуємо виключно параметризовані запити бібліотеки <code>psycopg2</code>: <code>cursor.execute("SELECT * FROM load WHERE id = %s", (user_input,))</code>. Драйвер бази даних автоматично екранує всі вхідні аргументи, що повністю блокує будь-які спроби впровадження шкідливого SQL-коду.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як забезпечується стабільність ядра при падінні з'єднання з базою даних?</h4>
        <p style="color: var(--text-dim);">
            A: Всі критичні операції з базою даних обгорнуті в декоратори стійкості, які реалізують стратегію <i>Retry with Exponential Backoff</i>. При виникненні мережевої помилки ядро робить до 5 спроб перепідключення з геометрично зростаючою паузою (1с, 2с, 4с, 8с), запобігаючи аварійному завершенню роботи всього додатку.
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
