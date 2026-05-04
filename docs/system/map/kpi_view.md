# Технічна специфікація: Візуалізатор Оперативного Моніторингу та KPI (SITUATIONAL AWARENESS VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">OPERATIONAL MONITORING | DIGITAL TWIN KPI</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Оперативний Моніторинг</h1>
            <p class="mega-subtitle">Система контролю ключових показників ефективності (KPI) в реальному часі: ситуаційна обізнаність про здоров'я мережі, стабільність частоти та інтелектуальна діагностика стану підстанцій</p>
            <div class="status-tags"><span class="tag tag-online">KPI ENGINE ACTIVE</span><span class="tag tag-version">v2.6.0</span><span class="tag tag-role">SYSTEM OPERATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🏥</div><div class="metric-info"><span class="metric-label">Health</span><span class="metric-value">Network Integrity %</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💓</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Frequency (Hz) Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Load</span><span class="metric-value">Total Power (MW)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛠️</div><div class="metric-info"><span class="metric-label">Method</span><span class="metric-value">Digital Twin Feed</span></div></div>
</div>

<!-- SECTION 01: KPI VIEW PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Оперативного Моніторингу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>kpi.py</code> є "Пульсом" проекту ATLAS. В енергетиці ситуаційна обізнаність (Situational Awareness) є критичною: оператор повинен за секунди зрозуміти, чи знаходиться система в безпечному режимі. Наша філософія базується на <b>Когнітивній Швидкості</b>: ми використовуємо великі метрики (Big Numbers), колірну індикацію (Зелений/Жовтий/Червоний) та графічні спідометри (Gauges) для миттєвої передачі стану системи, мінімізуючи час на інтерпретацію цифр.</p>
    </div>
</div>

<!-- SECTION 02: KPI PROCESSING PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр Обробки Метрик (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    LIVE("Digital Twin Live Stream") --> CLEAN("Fail-safe Data Cleaning (NaN Handling)")
    KAG("Kaggle Historical Feed") --> MODE_DETECT{"Detect Data Mode?"}
    
    MODE_DETECT -- "Live (Full)" --> CALC_FULL("Calc: Health, Freq, Voltage, DGA")
    MODE_DETECT -- "Kaggle (Limited)" --> CALC_MIN("Calc: Total Load Only")
    
    CALC_FULL --> KPI_CARDS("Top KPI Metrics Grid")
    CALC_FULL --> GAUGE("System Load Gauge")
    CALC_FULL --> TWIN_TABLE("Digital Twin Substation Table")
    
    TWIN_TABLE --> HEALTH_BAR("AI Health Progress Bars")
    KPI_CARDS --> RENDER("Situational Dashboard")
    GAUGE --> RENDER
    </div></div>
</div>

<!-- SECTION 03: DIGITAL TWIN INTEGRATION (REAL-TIME) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Інтеграція з Цифровими Двійниками</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль KPI є основним споживачем даних від двигуна **Digital Twin**. У режимі Live-симуляції кожна підстанція представлена як цифровий двійник, що передає:</p>
        <ul>
            <li><b>AI Health Score:</b> Комплексний індекс стабільності вузла, розрахований на основі 12 фізичних параметрів.</li>
            <li><b>Frequency (Hz):</b> Реальна частота системи з відстеженням дельти відносно еталонних 50.00 Гц.</li>
            <li><b>Thermal/DGA Feed:</b> Дані про температуру масла та концентрацію розчинених газів (H2) для предиктивної діагностики.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: CORE METRICS DEFINITION MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця визначення ключових метрик</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Метрика</th>
                    <th>Джерело</th>
                    <th>Поріг тривоги</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>🏥 Network Health</td><td>AI Analytics Engine</td><td>< 85% (Warning)</td></tr>
                <tr><td>💓 Frequency</td><td>System Oscillator Sync</td><td>±0.2 Hz (Critical)</td></tr>
                <tr><td>⚡ Total Power</td><td>Load Aggregator</td><td>> 95% Capacity</td></tr>
                <tr><td>🌡️ Oil Temperature</td><td>Transformer Sensors</td><td>> 85°C (Action Required)</td></tr>
                <tr><td>🛡️ H2 Concentration</td><td>DGA Chemical Sensors</td><td>> 100 ppm (Investigation)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: ADAPTIVE INTERFACE MODES (LIVE vs KAGGLE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Адаптивні режими інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль реалізує <b>Інтелектуальну адаптацію</b>. При роботі з історичними даними (Kaggle), де відсутні параметри здоров'я обладнання, інтерфейс автоматично перемикається у спрощений режим. Замість "порожніх" віджетів, система виводить інформативне повідомлення про те, які метрики доступні тільки в режимі Digital Twin, зберігаючи при цьому фокус на фактичному навантаженні регіону.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Моніторингу (KPI Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_situational_awareness(df_latest, region):
    1. CLEAN: df_clean = convert_to_numeric(df_latest, fill_na=0.0)
    
    2. CHECK_MODE:
           IF 'health_score' NOT IN columns:
               RENDER_SIMPLE_LOAD_METRIC(df_clean.sum())
               RETURN
               
    3. TOP_GRID:
           m1.metric("Network Health", avg(health))
           m2.metric("System Frequency", current_hz, delta=hz-50)
           m3.metric("Total Load", sum(load_mw))
           m4.render_gauge(current_load / max_capacity)
           
    4. SUBSTATION_TABLE:
           df_table = select_columns(['name', 'load', 'temp', 'h2', 'health'])
           df_table['Visual Status'] = map_to_progress_bars(health)
           st.dataframe(df_table, config=column_styles)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: DIGITAL TWIN SUBSTATION TABLE (AI-INDEX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Таблиця підстанцій з AI-індексом</h2></div>
    <div class="glass-card flow-step">
        <p>Центральним елементом аналізу є детальна таблиця підстанцій. Вона використовує компонент <code>make_health_bar</code> для візуалізації техстану через прогрес-бари. Кожен рядок таблиці — це "зріз" стану конкретного вузла мережі, де поєднуються фізичні параметри (Напруга, Навантаження) та інтелектуальні висновки (AI Health). Це дозволяє оператору миттєво ідентифікувати найслабшу ланку в системі.</p>
    </div>
</div>

<!-- SECTION 08: FAIL-SAFE DATA PROCESSING (STABILITY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Захищена обробка даних (Stability)</h2></div>
    <div class="glass-card flow-step">
        <p>Для запобігання "білим екранам" при рендерингу, <code>kpi.py</code> реалізує багаторівневу очистку даних. Функція <code>pd.to_numeric</code> з параметром <code>errors="coerce"</code> гарантує, що несподівані текстові дані або пропуски в телеметрії не викличуть падіння Streamlit, а будуть безпечно замінені на 0.0 або N/A, зберігаючи працездатність інтерфейсу в критичних ситуаціях.</p>
    </div>
</div>

<!-- SECTION 09: SYSTEM LOAD GAUGE (VISUAL BUDGETING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Спідометр навантаження (Visual Budgeting)</h2></div>
    <div class="glass-card flow-step">
        <p>У правому верхньому куті розташовано <b>System Gauge</b>. Він візуалізує "запас міцності" всієї енергосистеми. Навіть не дивлячись на цифри, оператор бачить положення стрілки в кольорових секторах. Якщо стрілка входить у червону зону (>90% завантаження), система автоматично активує візуальні акценти на метриках, вимагаючи негайного втручання або підключення маневреної генерації.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM SPACER & SCROLLING (UX FIX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Комфорт скролінгу (UX Fix)</h2></div>
    <div class="glass-card flow-step">
        <p>Враховуючи, що таблиця підстанцій може бути досить довгою (при виборі "Всі регіони"), у нижній частині додано технічний Spacer (300px). Це дозволяє користувачеві прокрутити таблицю так, щоб останні рядки знаходилися посередині екрана, забезпечуючи зручний доступ до детальної інформації про кожну підстанцію без напруження шиї та очей.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>UI Components</h4>
                <p>Провайдер віджетів Gauge, Health-bar та KPI карток.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>Data Aggregator</h4>
                <p>Постачальник останніх актуальних зрізів станів об'єктів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">⚙️</div>
            <div class="role-content">
                <h4>Pandas Core</h4>
                <p>Двигун для швидкої очистки та агрегації числових масивів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (PREDICTIVE KPI) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Predictive KPI)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Прогнозних KPI</b>. Поряд з поточними значеннями система буде виводити "Тіньові метрики" — очікуваний стан через 60 хвилин на основі ШІ-прогнозу. Це дозволить перейти від реактивного до проактивного управління енергосистемою. Також буде додано підтримку <b>Голосових оповіщень</b> про критичні виходи частоти за межі норми.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Моніторинг та KPI</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому здоров'я показує 0%?</b> — Ймовірно, ви перебуваєте в режимі Kaggle, або датчики підстанції ще не передали перший пакет телеметрії.</p>
        <p><b>Що означає дельта у частоті?</b> — Це відхилення від еталону 50 Гц. Позитивна дельта — надлишок генерації, негативна — дефіцит.</p>
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
