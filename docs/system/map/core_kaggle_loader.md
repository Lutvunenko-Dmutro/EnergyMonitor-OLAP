# Технічна специфікація: Конвеєр Імпорту Зовнішніх Даних (DATA INGESTION PIPELINE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATA ETL | KAGGLE CONNECTOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚚</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Завантажувач Kaggle</h1>
            <p class="mega-subtitle">Автоматизований ETL-конвеєр проекту ATLAS: імпорт, денормалізація та радикальна оптимізація еталонних наборів даних енергосистем США для аналітичного порівняння та навчання моделей</p>
            <div class="status-tags"><span class="tag tag-online">INGESTION ACTIVE</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">DATA INTEGRATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Mode</span><span class="metric-value">Automated Batch ETL</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🗺️</div><div class="metric-info"><span class="metric-label">Naming</span><span class="metric-value">Pretty-Name Mapping</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Optimization</span><span class="metric-value">Pre-concat Tail Slicing</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Resilience</span><span class="metric-value">Silent Error Bypass</span></div></div>
</div>

<!-- SECTION 01: DATA INGESTION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Імпорту Зовнішніх Даних</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>kaggle_loader.py</code> є "Портом" та "Перекладачем" проекту ATLAS. В енергетиці еталонні дані (Kaggle PJM/AEP) часто представлені у хаотичних форматах з різними назвами колонок та технічними абревіатурами. Наша філософія базується на <b>Стандартизації Хаосу</b>: ми автоматично скануємо файлову систему, уніфікуємо типи даних та перекладаємо інженерні коди (напр. "DOM", "PJME") на зрозумілу людині мову. Це перетворює набір розрізнених CSV-файлів на цілісний аналітичний шар, що дозволяє ATLAS порівнювати реальні показники української енергосистеми зі світовими еталонами.</p>
    </div>
</div>

<!-- SECTION 02: INGESTION PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема конвеєра імпорту (Ingestion Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DIR("data/ Directory") --> SCAN("glob.glob('*_hourly.csv')")
    SCAN --> LOOP("For each File in Batch")
    
    subgraph ETL_PROCESS["Atomic ETL Unit"]
        LOOP --> READ("pd.read_csv()")
        READ --> IDENT("Identify Prefix (AEP, DOM, etc.)")
        IDENT --> NORM_TS("Normalize Timestamp Column")
        NORM_TS --> NORM_MW("Normalize Load Column (MW)")
        NORM_MW --> MAP("Pretty-Name Mapping")
    end
    
    MAP --> OPTIMIZE("Radical Tail Slicing (Last 5000)")
    OPTIMIZE --> ACC("Accumulator List")
    
    ACC --> CONCAT("pd.concat(all_dfs)")
    CONCAT --> DIET("Memory Diet (Final Compression)")
    DIET --> OUTPUT("Unified Archive DataFrame")
    </div></div>
</div>

<!-- SECTION 03: PRETTY-NAME GEOGRAPHIC MAPPING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Географічний мапінг (Pretty Naming)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль містить інтелектуальний словник <code>KAGGLE_MAPPING</code>, який денормалізує технічні назви мереж США. Наприклад:</p>
        <ul>
            <li><b>AEP:</b> Американська електрична компанія (American Electric Power).</li>
            <li><b>COMED:</b> Commonwealth Edison (Чикаго) — одна з найбільших мереж Іллінойсу.</li>
            <li><b>DOM:</b> Dominion Energy (Вірджинія) — критичний вузол східного узбережжя.</li>
        </ul>
        <p>Такий підхід дозволяє оператору ATLAS працювати з географічними сутностями, а не з абстрактними скороченнями, що підвищує якість аналітичних висновків.</p>
    </div>
</div>

<!-- SECTION 04: KAGGLE MAPPING REFERENCE TABLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Довідкова таблиця мапінгу Kaggle</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Код префіксу</th>
                    <th>Офіційна назва оператора</th>
                    <th>Регіон охоплення</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>AEP</td><td>American Electric Power</td><td>Огайо, Кентуккі, Вірджинія</td></tr>
                <tr><td>COMED</td><td>Commonwealth Edison</td><td>Чикаго, Іллінойс</td></tr>
                <tr><td>PJME</td><td>PJM Eastern Region</td><td>Пенсільванія, Нью-Джерсі, Мериленд</td></tr>
                <tr><td>DEOK</td><td>Duke Energy</td><td>Огайо, Кентуккі</td></tr>
                <tr><td>DUQ</td><td>Duquesne Light</td><td>Піттсбург</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: RADICAL MEMORY OPTIMIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Радикальна оптимізація пам'яті</h2></div>
    <div class="glass-card flow-step">
        <p>Kaggle датасети часто містять записи за 10-15 років, що при об'єднанні 10+ файлів може миттєво вичерпати RAM сервера. У <code>kaggle_loader.py</code> реалізовано стратегію **Pre-concat Tail Slicing**. Ми обрізаємо кожен окремий файл до останніх 5000 записів (~7 місяців даних) <i>до</i> того, як додати його в загальний список для конкатенації. Це дозволяє завантажувати весь еталонний архів, витрачаючи лише кілька мегабайт пам'яті замість гігабайтів.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Завантажувача (Ingestion Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION load_kaggle_data():
    1. SCAN: Find all *_hourly.csv in /data
    2. LOOP file_path:
           TRY:
               df = read_csv(file_path)
               prefix = get_prefix(file_path)
               
               NORMALIZE_TIME(df) # Rename dt/timestamp
               NORMALIZE_LOAD(df, prefix) # MW column
               
               APPLY_MAPPING: df.substation = KAGGLE_MAPPING[prefix]
               
               SLICE: df = df.sort('ts').tail(5000)
               all_dfs.append(df)
           EXCEPT: CONTINUE (Skip corrupted files)
    3. FINAL:
           combined_df = concat(all_dfs)
           RETURN memory_diet(combined_df)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: ADAPTIVE COLUMN NORMALIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Адаптивна нормалізація колонок</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль використовує гнучкі правила пошуку ключових колонок. Для часу шукаються варіанти <code>datetime</code> або <code>timestamp</code>. Для навантаження використовується складний фільтр: назва повинна містити <code>_mw</code>, <code>load</code> або співпадати з префіксом файлу (напр. <code>AEP_MW</code>). Це дозволяє автоматично обробляти нові CSV-файли з Kaggle, навіть якщо їхня структура заголовків дещо відрізняється від стандартної, роблячи конвеєр імпорту самовідновлюваним та універсальним.</p>
    </div>
</div>

<!-- SECTION 08: SILENT RESILIENCE & ERROR BYPASS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Безшумна відмовостійкість (Silent Bypass)</h2></div>
    <div class="glass-card flow-step">
        <p>При пакетній обробці десятків файлів завжди існує ризик зустріти битий CSV або порожній файл. Завантажувач реалізує паттерн <b>Bypass Resilience</b>: будь-яка помилка при обробці окремого файлу ігнорується, система просто переходить до наступного. Це гарантує, що ATLAS завантажиться і покаже доступні дані, навіть якщо частина архівів була випадково пошкоджена, забезпечуючи безперервність роботи аналітичного дашборду.</p>
    </div>
</div>

<!-- SECTION 09: FINAL COMPRESSION (MEMORY DIET) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Фінальне стиснення (Memory Diet Sync)</h2></div>
    <div class="glass-card flow-step">
        <p>Після об'єднання всіх зрізів даних, результуючий датафрейм проходить через протокол <code>memory_diet</code>. Оскільки дані з Kaggle є статичними, ми агресивно перетворюємо назви підстанцій та регіонів у тип <code>Category</code>. Це зменшує розмір об'єкта в RAM ще на 60-70%, що дозволяє ATLAS тримати в пам'яті десятки еталонних сценаріїв одночасно без ризику вильоту програми через Out-Of-Memory (OOM).</p>
    </div>
</div>

<!-- SECTION 10: ROLE IN ACADEMIC COMPARISON -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Роль в академічному порівнянні</h2></div>
    <div class="glass-card flow-step">
        <p>У контексті тезисної роботи, <code>kaggle_loader.py</code> забезпечує **Верифікаційну базу**. Наявність еталонних даних PJM/AEP поруч із реальними даними української енергосистеми дозволяє проводити порівняльний аналіз (Benchmarking) та доводити ефективність розроблених алгоритмів прогнозування на світових стандартах даних, що є вагомим аргументом при науковому захисті архітектури ATLAS.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📂</div>
            <div class="role-content">
                <h4>Glob / OS</h4>
                <p>Низькорівнева навігація по файловій системі та пошук CSV-архівів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Pandas Core</h4>
                <p>Основний двигун ETL: парсинг, трансформація та конкатенація даних.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🧬</div>
            <div class="role-content">
                <h4>Database Diet</h4>
                <p>Використання спільних протоколів оптимізації пам'яті для фінального DF.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (CLOUD CLOUD SYNC) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Cloud Sync)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Cloud Data-Link**. Завантажувач зможе автоматично завантажувати свіжі версії датасетів безпосередньо з Kaggle API при їх оновленні. Також буде додано підтримку <b>Зональної класифікації</b>: автоматичне визначення кліматичної зони регіону на основі його коду та підбір відповідних погодних коефіцієнтів для ML-моделей.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Завантажувач Kaggle</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому я не бачу дані за 2010 рік?</b> — Модуль автоматично обрізає старі дані до останніх 5000 записів для збереження пам'яті.</p>
        <p><b>Як додати свій CSV-файл?</b> — Назвіть його за маскою <code>MYID_hourly.csv</code> та покладіть у папку <code>data/</code>; система знайде його автоматично.</p>
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
