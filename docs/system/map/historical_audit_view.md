# Технічна специфікація: Цифровий Архів та Система Фізичного Аудиту (HISTORICAL AUDIT VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DIGITAL ARCHIVE | MULTIDIMENSIONAL AUDIT</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📜</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Цифровий Архів</h1>
            <p class="mega-subtitle">Центр глибокої ретроспективної аналітики та аудиту: крос-параметрична кореляція, контроль технічного стану обладнання та дослідження добових ритмів системи</p>
            <div class="status-tags"><span class="tag tag-online">ARCHIVE ACTIVE</span><span class="tag tag-version">v2.1.5</span><span class="tag tag-role">RELIABILITY AUDITOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Audit Type</span><span class="metric-value">Physical Correlation</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌡️</div><div class="metric-info"><span class="metric-label">Diagnostics</span><span class="metric-value">Thermal / DGA</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⏳</div><div class="metric-info"><span class="metric-label">Temporal</span><span class="metric-value">Workday vs Weekend</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Access</span><span class="metric-value">Raw Data Export</span></div></div>
</div>

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Цифрового Архіву</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>historical_audit.py</code> є "Пам'яттю" проєкту ATLAS. В енергетиці аналіз минулого є єдиним ключем до точного прогнозування майбутнього. Наша філософія базується на <b>Багатовимірному Фізичному Зв'язку</b>: ми не просто накопичуємо історію навантаження, а накладаємо її на фізичні параметри обладнання (температура масла, концентрація H2) та зовнішні чинники (температура повітря). Це дозволяє диспетчеру виявляти приховані дефекти ізоляції та розуміти реальні межі стійкості мережі на основі історичних фактів.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL MODELING & AGGREGATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичний апарат аналізу та агрегації</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення високої точності аналізу великих масивів даних використовуються наступні математичні моделі:</p>
        
        <h4>1. Згладжування шумів групового навантаження (Mean Aggregation)</h4>
        <p>При виборі декількох підстанцій одночасно система розраховує середньозважену лінію навантаження для придушення високочастотних імпульсних завад (шумів телеметрії):</p>
        $$\bar{L}_{t} = \frac{1}{N} \sum_{i=1}^{N} L_{i, t}$$
        <p>де $L_{i, t}$ — навантаження підстанції $i$ в момент часу $t$, а $N$ — загальна кількість вибраних об'єктів.</p>

        <h4>2. Оцінка здоров'я обладнання за воднем (DGA Degradation Model)</h4>
        <p>Індекс здоров'я трансформатора $H_t$ (%) має обернену нелінійну залежність від концентрації розчиненого водню (H₂) у маслі за стандартом IEC 60599 (Dissolved Gas Analysis):</p>
        $$H_t = H_{0} - \gamma \ln\left(1 + \frac{[\text{H}_2]_t}{[\text{H}_2]_{\text{threshold}}}\right)$$
        <p>де $H_{0} = 100\%$ — базовий стан нового обладнання, $[\text{H}_2]_t$ — виміряна концентрація водню (ppm), а $\gamma$ — емпіричний коефіцієнт деградації ізоляції.</p>
    </div>
</div>

<!-- SECTION 03: RETROSPECTIVE AUDIT PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Конвеєр Ретроспективного Аудиту (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DB("SQL Archive Database") --> BOUNDS("Get Time Bounds (ts_min/ts_max)")
    BOUNDS --> FILTER("User Selection: Target & Range")
    FILTER --> LOAD("Aggregated Data Extraction")
    
    LOAD --> STATS("Key Performance Metrics (Max/Min/Avg)")
    STATS --> DUAL_AXIS("Multi-Axis Correlation Charts")
    
    DUAL_AXIS --> THERMAL("Thermal Balance (Load vs Oil)")
    DUAL_AXIS --> WEATHER("Weather Impact (Load vs Air)")
    DUAL_AXIS --> HEALTH("Asset Health (Health vs H2)")
    
    LOAD --> RHYTHM("Temporal Rhythm Analysis")
    LOAD --> EXPORT("Raw Data Table & CSV Export")
    </div></div>
</div>

<!-- SECTION 04: ARCHIVE ANALYTICS MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця методів архівної аналітики</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Тип аналізу</th>
                    <th>Метод та візуалізація</th>
                    <th>Діагностичне значення результату</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>🌤️ Weather Correlation</b></td><td>Dual-axis Line Chart (Orange vs Blue)</td><td>Аналіз термочутливості та впливу кліматичних циклів на енергоспоживання</td></tr>
                <tr><td><b>🛢️ Thermal Diagnostic</b></td><td>Dual-axis Line Chart (Orange vs Red)</td><td>Виявлення теплової інерції трансформаторів, детекція перегріву масла</td></tr>
                <tr><td><b>🛡️ Asset Health DGA</b></td><td>Dual-axis Line Chart (Green vs Purple)</td><td>Раннє виявлення дефектів ізоляції за допомогою концентрації водню (H₂)</td></tr>
                <tr><td><b>⏳ Rhythm Pulse</b></td><td>Day-type Overlay Profile</td><td>Валідація сезонних ШІ-коефіцієнтів та коефіцієнта <code>day_multiplier</code></td></tr>
                <tr><td><b>📂 Raw Audit Data</b></td><td>Interactive Grid with CSV Exporter</td><td>Експорт первинної інформації для зовнішнього аудиту регуляторів</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: CROSS-PARAMETER DUAL-AXIS CORRELATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Крос-параметричний аналіз (Dual-Axis Y)</h2></div>
    <div class="glass-card flow-step">
        <p>Для одночасного дослідження процесів різної фізичної природи модуль використовує спеціалізовані **Dual-Axis графіки** (дві осі Y з незалежним масштабуванням):</p>
        <ul>
            <li><b>Weather Impact:</b> Накладання температури повітря (°C) на навантаження (МВт). Дозволяє бачити піки споживання через температурні аномалії.</li>
            <li><b>Thermal Balance:</b> Порівняння температури масла трансформаторів з навантаженням. Дає можливість оцінити здатність обладнання витримувати тривалі перевантаження.</li>
            <li><b>DGA Audit:</b> Кореляція індексу здоров'я (%) та концентрації водню (ppm). Підсвічує періоди прискореної деградації ізоляції при виникненні внутрішніх мікро-дуг.</li>
        </ul>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Архівного Ядра (Audit Core Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_historical_audit(selected_region, date_range, selected_substation):
    1. // [LOAD TIME BOUNDS]
       df_bounds = db.get_archive_bounds()
       IF df_bounds is Empty:
           show_data_ingestion_warning()
           RETURN
           
    2. // [RESOLVE TARGETS & DATE LIMITS]
       start_date, end_date = resolve_dates(date_range, df_bounds)
       use_aggregate = check_if_all_substations(selected_substation)
       active_target = selected_substation IF NOT use_aggregate ELSE selected_region
       
    3. // [FETCH ARCHIVE DATA VIA MULTIDIMENSIONAL SQL QUERY]
       df = db.load_archive_data(start_date, end_date, active_target)
       IF df is Empty:
           show_no_data_warning()
           RETURN
           
    4. // [CONVERT NUMERIC & GROUP MULTI-SUBSTATIONS TO ELIMINATE NOISE]
       convert_columns_to_numeric(df, ["load_mw", "oil_temp", "h2_ppm", "health", "air_temp"])
       IF count_unique_substations(df) > 1:
           df = df.groupby("ts").mean(numeric_only=True).reset_index()
           
    5. // [KPI METRICS CARDS]
       render_kpi_cards(df.load_mw.max(), df.air_temp.min(), df.oil_temp.max(), df.health.mean())
       
    6. // [RENDER DUAL-AXIS CORRELATION CHARTS]
       render_dual_axis(df, "load_mw", "air_temp", colors=["#f97316", "#38bdf8"])
       render_dual_axis(df, "load_mw", "oil_temp", colors=["#f97316", "#f43f5e"])
       render_dual_axis(df, "health", "h2_ppm", colors=["#22c55e", "#a855f7"])
       
    7. // [RHYTHM CHART - WORKDAY VS WEEKEND]
       df_rhythm = db.load_rhythm_data(start_date, end_date, active_target)
       IF NOT df_rhythm.empty:
           render_rhythm_chart(df_rhythm)
           
    8. // [RENDER RAW DATA TABLE & DATA EXPORTER]
       render_raw_data_table(df, start_date, end_date)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: ENERGY RHYTHM & DAY-MULTIPLIER VALIDATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Енергетичний ритм: Будні vs Вихідні</h2></div>
    <div class="glass-card flow-step">
        <p>Для верифікації моделей машинного навчання модуль будує <b>Rhythm Chart</b>. Графік накладає середній погодинний профіль споживання робочих днів на вихідні. Це дозволяє наочно валідувати ШІ-коефіцієнти (наприклад, <code>day_multiplier</code>, що знижує прогноз у вихідні дні через зупинку промисловості) та калібрувати нейронні мережі на реальних профілях ритміки енергосистеми.</p>
    </div>
</div>

<!-- SECTION 08: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4><a href="data_services_hub.md">archive.py</a></h4>
                <p>Низькорівневий SQL-калькулятор архіву: функції <code>get_archive_bounds</code>, <code>load_archive_data</code> та <code>load_rhythm_data</code>.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📈</div>
            <div class="role-content">
                <h4><a href="ui_charts_base.md">charts/base.py</a></h4>
                <p>Експортер графічних примітивів: функції побудови Dual-Axis графіків та профілів енергетичних ритмів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📂</div>
            <div class="role-content">
                <h4><a href="historical_audit_view.md">data_table.py</a></h4>
                <p>Компонент рендерингу інтерактивної таблиці з вбудованим фільтром пошуку та генератором CSV-файлів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 09: ROADMAP TO v3.0 (AI ANOMALY & OUTLIER DETECTION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Дорожня карта v3.0 (AI Anomaly & Outlier Detection)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 заплановано:</p>
        <ul>
            <li><b>Automated DGA Diagnostic:</b> Класифікація дефектів за методом трикутника Дюваля (Duval's Triangle) на основі історичних зрізів газів.</li>
            <li><b>AI Anomaly Highlighting:</b> Автоматичне підсвічування ділянок графіків, де кореляція між навантаженням та температурою масла була порушена (ознака виходу з ладу системи охолодження).</li>
            <li><b>Direct Excel Export:</b> Генерація форматованих звітів у форматі XLSX з автоматичною побудовою діаграм для керівництва.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">FAQ: Технічні відповіді</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Чому на початку роботи графіки порожні або видають попередження?</b><br>
        A: Архів оперує даними з SQLite бази <code>energy.db</code>. Якщо ви щойно запустили проєкт вперше, генератор даних у <code>sidebar.py</code> має попрацювати принаймні кілька секунд, щоб записати початкові вимірювання. Спробуйте почекати та натиснути "Оновити".</p>
        <p><b>Q: Як працює придушення "пилки" при виборі декількох об'єктів?</b><br>
        A: Якщо запит повертає дані для декількох підстанцій одночасно, малювати їх на одному графіку призведе до накладання ліній ("пилки"). Система автоматично виконує операцію <code>groupby("ts").mean()</code>, розраховуючи єдиний середній фізичний тренд для всього регіону.</p>
        <p><b>Q: Як розраховується індекс здоров'я (Health Score) в архіві?</b><br>
        A: Це інтегральний показник технічного стану трансформатора. Він обчислюється на базі поточної концентрації газів (H₂), температури масла та кількості зафіксованих перевантажень протягом роботи підстанції.</p>
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
