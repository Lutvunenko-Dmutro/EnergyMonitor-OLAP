# Технічна специфікація: Система Аналізу Споживання (CONSUMPTION ANALYTICS VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DYNAMIC LOAD ANALYSIS | STATISTICAL SLICING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Аналіз Споживання</h1>
            <p class="mega-subtitle">Універсальний аналітичний двигун візуалізації енергоспоживання: інтерактивна динаміка, статистичне групування за типами днів та багатофакторна кореляція з метеоумовами</p>
            <div class="status-tags"><span class="tag tag-online">CONSUMPTION ACTIVE</span><span class="tag tag-version">v2.4.0</span><span class="tag tag-role">NETWORK ANALYST</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Dimensions</span><span class="metric-value">Temporal / Regional</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📦</div><div class="metric-info"><span class="metric-label">Methods</span><span class="metric-value">Boxplot / OLS Reg</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔥</div><div class="metric-info"><span class="metric-label">Features</span><span class="metric-value">Peak Annotation</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Scale</span><span class="metric-value">Log / Relative %</span></div></div>
</div>

<!-- SECTION 01: CONSUMPTION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Аналізу Споживання</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>consumption.py</code> є фундаментом системи моніторингу ATLAS. В енергетиці навантаження — це не просто лінія на графіку, це "пульс" життєдіяльності регіону. Наша філософія базується на <b>Багатовимірному Контексті</b>: ми розглядаємо споживання не ізольовано, а в тісному зв'язку з часом (година, робочий/вихідний день) та зовнішніми факторами (температура). Це дозволяє диспетчеру не лише бачити фактичний стан, а й розуміти статистичні межі норми для поточного періоду.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL METRICS NORMALIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математична нормалізація та регресійний аналіз</h2></div>
    <div class="glass-card flow-step">
        <p>Для коректного порівняння об'єктів різного масштабу та виявлення прихованих закономірностей реалізовано наступні математичні апарати:</p>
        
        <h4>1. Відносна нормалізація навантаження (%)</h4>
        <p>Кожне миттєве значення навантаження $L_{\text{actual}, t}$ ділиться на історичний максимум підстанції/регіону для приведення до єдиної шкали:</p>
        $$L_{\text{relative}, t} = \frac{L_{\text{actual}, t}}{\max_{k \in T} (L_{\text{actual}, k})} \times 100\%$$
        <p>Це дозволяє наочно порівнювати "завантаженість" гігаватного мегаполіса та локальної підстанції.</p>

        <h4>2. Термочутливість енергомережі (OLS Regression)</h4>
        <p>Кореляція між температурою повітря $X_{\text{temp}}$ та навантаженням $Y_{\text{load}}$ описується лінійною регресією за методом найменших квадратів (Ordinary Least Squares):</p>
        $$\hat{Y}_{\text{load}} = \beta_0 + \beta_1 X_{\text{temp}} + \epsilon$$
        <p>Коефіцієнт нахилу $\beta_1$ показує термочутливість системи ($\text{МВт}/^\circ\text{C}$). Від'ємне значення $\beta_1$ взимку вказує на переважання опалювального навантаження, тоді як додатне значення влітку свідчить про активне використання систем кондиціонування.</p>
    </div>
</div>

<!-- SECTION 03: ANALYTICAL PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Конвеєр Аналітичної Обробки (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Input DataFrame (Measurements)") --> AGGR("Hourly Resampling / Mean Aggregation")
    AGGR --> SCALE{Select Metric Mode}
    
    SCALE -- "Absolute Load (MW)" --> ABS("Use actual_load_mw")
    SCALE -- "Relative Load (%)" --> REL("Calculate relative_load via Peak Max")
    
    ABS --> PLOT("px.line (Plotly Dark Theme)")
    REL --> PLOT
    
    PLOT --> PEAK("Global Peak Search & Annotation ('🔥 Пік')")
    
    AGGR --> BOX["Add day_type (Workday vs Weekend)"]
    BOX --> REND_BOX("px.box (Hourly Distribution)")
    
    AGGR --> REG{"Temperature Exists?"}
    REG -- "Yes" --> OLS("px.scatter + trendline='ols'")
    REG -- "No" --> INFO("Display Ingestion Note")
    </div></div>
</div>

<!-- SECTION 04: FEATURE CAPABILITIES MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця аналітичного функціоналу</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Функція</th>
                    <th>Метод розрахунку</th>
                    <th>Діагностичне значення</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Peak Detection</b></td><td>Пошук глобального максимуму у вікні фільтрації</td><td>Локалізація моментів критичного навантаження для планування резервів</td></tr>
                <tr><td><b>Facet Gridding</b></td><td>Динамічна генерація підобластей рендерингу (by Region)</td><td>Паралельне порівняння профілів споживання без перевантаження одного графіка</td></tr>
                <tr><td><b>Boxplot Slicing</b></td><td>Обчислення міжквартильного розмаху (IQR) по годинах</td><td>Виявлення волатильності та меж нормального споживання системи</td></tr>
                <tr><td><b>OLS Regression</b></td><td>Метод найменших квадратів на базі Statsmodels</td><td>Визначення коефіцієнта температурного впливу на кожну підстанцію</td></tr>
                <tr><td><b>Day-Type Classifier</b></td><td>Мапування дня тижня: <code>dayofweek >= 5</code></td><td>Порівняння профілів буднього та вихідного дня для валідації ШІ-моделей</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: SEASONAL SLICING & DAY-TYPE ANALYSIS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Сезонне зрізування та типи днів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль автоматично класифікує кожен історичний таймстемп на "Робочий день" (будні) або "Вихідний". За допомогою діаграм "Ящик з вусами" (Boxplots) візуалізується погодинний розподіл навантаження. Це дозволяє диспетчеру побачити типовий "горб" вечірнього піку та зрозуміти, чи поточне споживання виходить за межі типового 75-го перцентиля, що може свідчити про нетипову ситуацію в енергосистемі.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Візуалізації (Consumption Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_consumption_view(df_load, group_by_col):
    1. // [DATA VALIDITY CHECK]
       IF df_load is NULL or Empty:
           show_ux_warning_and_instructions()
           RETURN
       
    2. // [DYNAMIC PREPARATION & INTERPOLATION]
       df_sel = df_load.copy()
       df_sel["timestamp"] = parse_to_datetime(df_sel["timestamp"])
       
    3. // [SETTINGS POPUP]
       with popover("⚙️ Налаштування"):
           use_relative = toggle("📈 Відносні показники (%)")
           use_log = toggle("🪵 Логарифмічна шкала (Y)")
           use_facet = toggle("🔲 Сітка графіків (by Region)")
           
    4. // [HOURLY RESAMPLING VIA AGGREGATOR]
       df_plot = aggregator.aggregate_consumption(df_sel, group_by_col, numeric_cols=["actual_load_mw"])
       
    5. // [SCALE SWITCHING]
       IF use_relative:
           df_plot = aggregator.add_relative_load(df_plot, group_by_col)
           y_col = "relative_load"
       ELSE:
           y_col = "actual_load_mw"
           
    6. // [LINE CHART RENDER WITH PEAK DETECT]
       fig = px.line(df_plot, x="timestamp", y=y_col, color=group_by_col, facet_col=(group_by_col IF use_facet ELSE None))
       IF NOT use_facet:
           max_point = df_plot.loc[df_plot[y_col].idxmax()]
           fig.add_annotation(x=max_point.timestamp, y=max_point[y_col], text="🔥 Пік")
       safe_plotly_render(fig)
       
    7. // [STATISTICAL BOXPLOTS & WEATHER CORRELATION]
       df_stat = enrich_with_hour_and_daytype(df_plot)
       render_boxplot_in_column_1(df_stat)
       IF "temperature" in df_plot.columns:
           render_scatter_with_ols_in_column_2(df_plot)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: SMART DATA IMPUTATION IN UI -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Розумна обробка пропусків (UI-Imputation)</h2></div>
    <div class="glass-card flow-step">
        <p>При візуалізації <code>consumption.py</code> використовує згладжування та агрегацію для заповнення короткочасних "дірок" у телеметрії. Це гарантує цілісність ліній на графіках та запобігає візуальному шуму, який міг би відволікати диспетчера. Якщо даних занадто мало, система виводить спеціальну UX-підказку щодо коригування фільтрів календаря у боковій панелі (Sidebar).</p>
    </div>
</div>

<!-- SECTION 08: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4><a href="analysis_services_hub.md">aggregator.py</a></h4>
                <p>Потужне ядро математичної агрегації даних: функції <code>aggregate_consumption</code> та <code>add_relative_load</code>.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Express</h4>
                <p>Основна бібліотека для побудови високопродуктивних інтерактивних лінійних графіків, boxplots та регресійних трендів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4><a href="utils_extended_toolkit.md">ui_helpers.py</a></h4>
                <p>Набір утиліт для стабільного рендерингу Plotly-графіків (<code>safe_plotly_render</code>) з інтегрованим оверлеєм помилок.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 09: ROADMAP TO v3.0 (HEATMAP LOAD CALENDAR) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Дорожня карта v3.0 (Heatmap Load Calendar)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступних версіях планується:</p>
        <ul>
            <li><b>Календарні теплокарти (Load Heatmaps):</b> Візуалізація навантаження у розрізі "День тижня / Година доби" для швидкого виявлення аномальних нічних споживань.</li>
            <li><b>Multi-target Overlay:</b> Порівняння лінії прогнозу від LSTM моделі безпосередньо з історичними статистичними межами Boxplot в реальному часі.</li>
            <li><b>Vectorized Outlier Detection:</b> Автоматичне маркування викидів споживання за критерієм $3\sigma$ (Правило трьох сигм).</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">FAQ: Технічні відповіді</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Чому при виборі Kaggle-джерела пише "Аналіз температури недоступний"?</b><br>
        A: Історичні CSV-файли Kaggle (наприклад, <code>AEP_hourly.csv</code>) містять лише часові позначки та навантаження у МВт, без метеорологічних даних. У такому разі система автоматично відключає блок OLS-регресії, щоб запобігти помилкам розрахунку, та виводить інформаційне повідомлення.</p>
        <p><b>Q: Як працює фільтрація неповних днів?</b><br>
        A: Агрегатор перевіряє кількість годинних записів для кожного дня. Якщо записів менше 20, цей день вважається "збійним" і не береться до розрахунку трендів, що запобігає появі помилкових різких спадів графіків у кінці часового вікна.</p>
        <p><b>Q: Як розраховується відносна шкала (%)?</b><br>
        A: Ми беремо максимальне значення навантаження для обраного об'єкта за весь обраний період і приймаємо його за 100%. Всі інші значення відображаються у відсотках від цього максимуму.</p>
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
