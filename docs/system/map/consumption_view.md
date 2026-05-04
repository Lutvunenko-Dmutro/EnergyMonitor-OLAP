# Технічна специфікація: Система Аналізу Споживання (CONSUMPTION ANALYTICS VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DYNAMIC LOAD ANALYSIS | STATISTICAL SLICING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Аналіз Споживання</h1>
            <p class="mega-subtitle">Універсальний двигун візуалізації енергоспоживання: інтерактивна динаміка, статистичне групування за типами днів та багатофакторна кореляція з погодою</p>
            <div class="status-tags"><span class="tag tag-online">CONSUMPTION ACTIVE</span><span class="tag tag-version">v2.4.0</span><span class="tag tag-role">NETWORK ANALYST</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Dimensions</span><span class="metric-value">Temporal / Region</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📦</div><div class="metric-info"><span class="metric-label">Methods</span><span class="metric-value">Boxplot / OLS</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔥</div><div class="metric-info"><span class="metric-label">Features</span><span class="metric-value">Peak Detection</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Scale</span><span class="metric-value">Log / Relative</span></div></div>
</div>

<!-- SECTION 01: CONSUMPTION VIEW PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Аналізу Споживання</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>consumption.py</code> є фундаментом системи моніторингу ATLAS. В енергетиці навантаження — це не просто лінія на графіку, це "пульс" життєдіяльності регіону. Наша філософія базується на <b>Багатовимірному Контексті</b>: ми розглядаємо споживання не ізольовано, а в тісному зв'язку з часом (година, тип дня) та зовнішніми факторами (температура). Це дозволяє диспетчеру не лише бачити фактичний стан, а й розуміти статистичні межі норми для поточного періоду.</p>
    </div>
</div>

<!-- SECTION 02: ANALYTICAL PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр Аналітичної Обробки (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Input Dataframe (Cleaned)") --> AGGR("Temporal Aggregation (Hourly)")
    AGGR --> MODE{Mode Selection?}
    
    MODE -- "Relative (%)" --> NORM("Normalization by Peak Load")
    MODE -- "Absolute (MW)" --> RAW("Raw Load Series")
    
    NORM --> VIS_LINE("Interactive Line Chart")
    RAW --> VIS_LINE
    
    VIS_LINE --> PEAK("Automatic Peak Annotation")
    
    AGGR --> STAT("Statistical Slicing (Boxplots)")
    STAT --> DAY_TYPE("Workday vs Weekend Split")
    
    AGGR --> WEATH("Weather Correlation (Scatter)")
    WEATH --> REGR("OLS Regression Analysis")
    </div></div>
</div>

<!-- SECTION 03: METRIC NORMALIZATION (MW vs %) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Нормалізація та масштабування метрик</h2></div>
    <div class="glass-card flow-step">
        <p>Для ефективного порівняння об'єктів різного масштабу модуль реалізує два режими відображення:</p>
        <ul>
            <li><b>Абсолютне навантаження (МВт):</b> Пряма візуалізація потужності, необхідна для оперативного управління генерацією та резервами.</li>
            <li><b>Відносне навантаження (%):</b> Нормалізація відносно максимального історичного піку об'єкта. Дозволяє порівнювати "напруженість" роботи великих регіонів та малих підстанцій на одній шкалі.</li>
            <li><b>Logarithmic Scale:</b> Підтримка логарифмічної осі Y для виявлення мікро-патернів у періоди нічних мінімумів.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: FEATURE CAPABILITIES MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця функціональних можливостей</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Функція</th>
                    <th>Механізм реалізації</th>
                    <th>Цільовий інсайт</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Peak Detection</td><td>Annotated Max Search</td><td>Виявлення критичних навантажень</td></tr>
                <tr><td>Facet Grids</td><td>Region-based Splitting</td><td>Паралельне порівняння територій</td></tr>
                <tr><td>Boxplots</td><td>Interquartile Range (IQR)</td><td>Аналіз волатильності споживання</td></tr>
                <tr><td>Regression</td><td>Ordinary Least Squares (OLS)</td><td>Оцінка термочутливості мережі</td></tr>
                <tr><td>Day-type Split</td><td>Calendar Mapping</td><td>Різниця патернів (Будні/Вихідні)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: SEASONAL SLICING & DAY-TYPE ANALYSIS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Сезонне зрізування та типи днів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль автоматично класифікує дані на "Робочі" та "Вихідні". За допомогою діаграм "Ящик з вусами" (Boxplots) візуалізується погодинний розподіл навантаження. Це дозволяє диспетчеру побачити типовий "горб" вечірнього піку та зрозуміти, чи поточне споживання виходить за межі типового 75-го перцентиля, що може свідчити про нетипову ситуацію в енергосистемі.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Візуалізації (Consumption Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_consumption_view(df, group_col):
    1. PREPARE: Normalize timestamps & drop empty data
    2. UI_CONTROLS: Use Popover for scale settings (Log, Rel, Facet)
    
    3. AGGREGATE: df_hourly = aggregate_by_hour(df, group_col)
    
    4. MAIN_CHART: 
           fig = px.line(df_hourly, y=mode_col, facet=facet_mode)
           ANNOTATE(fig, max_load_point, "🔥 PEAK")
           safe_render(fig)
           
    5. STAT_ANALYSIS:
           df_stat = enrich_with_day_type(df_hourly)
           fig_box = px.box(df_stat, x="hour", color="day_type")
           safe_render(fig_box)
           
    6. WEATHER_CORR:
           IF temperature_exists:
               px.scatter(df_hourly, x="temp", y="load", trendline="ols")
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: WEATHER CORRELATION & REGRESSION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Кореляція з погодою та регресія</h2></div>
    <div class="glass-card flow-step">
        <p>Важливою частиною аналізу є блок <b>Weather Correlation</b>. Система будує діаграму розсіювання (Scatter Plot) з лінією тренду (OLS Regression) для кожного регіону. Нахил цієї лінії показує "температурну чутливість" енергосистеми: скільки МВт навантаження додається на кожний градус зниження температури. Це база для довгострокового планування паливних запасів на ТЕС/ТЕЦ.</p>
    </div>
</div>

<!-- SECTION 08: PEAK DETECTION & ANNOTATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Виявлення піків та анотування</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль автоматично шукає точку глобального максимуму в обраному часовому вікні. Ця точка позначається яскравою анотацією "🔥 Пік" з точним значенням. Це дозволяє уникнути помилок при візуальному читанні графіка та миттєво зафіксувати екстремальні режими роботи мережі, що є критичним для звітності перед керівництвом енергокомпанії.</p>
    </div>
</div>

<!-- SECTION 09: SMART DATA IMPUTATION IN UI -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Розумна обробка пропусків (UI-Imputation)</h2></div>
    <div class="glass-card flow-step">
        <p>При візуалізації <code>consumption.py</code> використовує методи згладжування та інтерполяції для заповнення короткочасних "дирок" у телеметрії. Це гарантує цілісність ліній на графіках та запобігає візуальному шуму, який міг би відволікати диспетчера. Якщо даних занадто мало, система виводить спеціальну UX-підказку щодо коригування фільтрів календаря.</p>
    </div>
</div>

<!-- SECTION 10: MULTI-REGION FACET GRIDDING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Сітки фасетних графіків (Facet Grids)</h2></div>
    <div class="glass-card flow-step">
        <p>Для порівняння декількох регіонів одночасно, модуль підтримує режим <b>Facet Grid</b>. Замість того, щоб малювати 10 ліній на одному перевантаженому графіку, система створює сітку маленьких діаграм для кожного об'єкта. Це дозволяє легко ідентифікувати аномальну поведінку в окремому регіоні, яка могла б "загубитися" у сумарному графіку всієї країни.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Aggregator Engine</h4>
                <p>Постачальник агрегованих та нормалізованих даних.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Express</h4>
                <p>Основна бібліотека для швидкої та інтерактивної візуалізації.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4>UI Helpers</h4>
                <p>Набір утиліт для безпечного рендерингу Plotly-контенту.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (PREDICTIVE COMPARISON) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Predictive Comparison)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Гібридної візуалізації</b>. Ми будемо накладати прогнозні інтервали від ШІ безпосередньо на історичні статистичні Boxplots. Також буде додано підтримку <b>Heatmaps</b> (теплових карт) для аналізу інтенсивності навантаження у розрізі "День тижня / Година", що є ідеальним для виявлення системних зсувів графіків споживання.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Аналіз Споживання</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому лінія графіка розривається?</b> — Це свідчить про великі пропуски в даних телеметрії, які неможливо заповнити автоматично. Спробуйте змінити період або джерело даних.</p>
        <p><b>Як вимкнути легенду?</b> — Натисніть подвійним кліком на будь-який елемент легенди, щоб ізолювати його, або скористайтеся налаштуваннями у поповері.</p>
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
