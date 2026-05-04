# Технічна специфікація: Цифровий Архів та Система Фізичного Аудиту (HISTORICAL AUDIT VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DIGITAL ARCHIVE | MULTIDIMENSIONAL AUDIT</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📜</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Цифровий Архів</h1>
            <p class="mega-subtitle">Центр глибокої ретроспективної аналітики: крос-параметрична кореляція (навантаження, температура, гази), аудит техстану обладнання та аналіз ритміки енергосистеми</p>
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

<!-- SECTION 01: HISTORICAL AUDIT PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Цифрового Архіву</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>historical_audit.py</code> є "Пам'яттю" проекту ATLAS. В енергетиці аналіз минулого є ключем до розуміння майбутнього. Наша філософія базується на <b>Багатовимірному Зв'язку</b>: ми не просто дивимося на історію навантаження, а накладаємо її на фізичні параметри обладнання (температура масла, концентрація H2) та зовнішні чинники (погода). Це дозволяє виявити неявні дефекти та зрозуміти реальні межі надійності енергосистеми на основі історичних фактів, а не тільки моделей.</p>
    </div>
</div>

<!-- SECTION 02: AUDIT PROCESSING PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр Ретроспективного Аудиту (Flow)</h2></div>
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

<!-- SECTION 03: CROSS-PARAMETER CORRELATION (DUAL-AXIS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Крос-параметрична кореляція (Dual-Axis)</h2></div>
    <div class="glass-card flow-step">
        <p>Для виявлення прихованих залежностей модуль використовує графіки з подвійною віссю Y:</p>
        <ul>
            <li><b>Thermal Balance:</b> Порівняння навантаження з температурою масла. Дозволяє бачити теплову інерцію трансформаторів та виявляти перегрів при пікових навантаженнях.</li>
            <li><b>Weather Impact:</b> Накладання температури повітря на профіль споживання. Візуалізує термочутливість регіону (вплив обігріву/кондиціонування).</li>
            <li><b>DGA Audit (H2):</b> Зв'язок індексу здоров'я (Health Score) з концентрацією водню (H2). Рання діагностика внутрішніх дефектів через аналіз газів у маслі.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: ARCHIVE ANALYTICS MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця архівної аналітики</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Тип аналізу</th>
                    <th>Метод</th>
                    <th>Технічний результат</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Heat Load Audit</td><td>Dual-axis Line</td><td>Визначення перевантажувальної здатності</td></tr>
                <tr><td>H2 Gas Trend</td><td>Correlation scatter</td><td>Детекція деградації ізоляції</td></tr>
                <tr><td>Rhythm Compare</td><td>Day-type overlay</td><td>Валідація сезонних коефіцієнтів ШІ</td></tr>
                <tr><td>Health Monitor</td><td>Trend accumulation</td><td>Прогнозування терміну служби (MTBF)</td></tr>
                <tr><td>Raw Audit</td><td>Data Grid</td><td>Пряма звірка з первинними документами</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: ENERGY RHYTHM (WORKDAY VS WEEKEND) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Енергетичний ритм: Будні vs Вихідні</h2></div>
    <div class="glass-card flow-step">
        <p>Унікальною функцією <code>historical_audit.py</code> є графік "Енергетичного пульсу". Ми порівнюємо середні профілі навантаження робочих та вихідних днів на одному графіку. Це наочно демонструє вплив <code>day_multiplier</code> (зниження навантаження у вихідні через зупинку промислових підприємств) та допомагає верифікувати гіпотези, закладені в архітектуру нейромереж прогнозування.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Архівного Ядра (Audit Core Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_historical_audit(region, dates, substation):
    1. BOUNDS: (min_ts, max_ts) = db.get_archive_range()
    2. RESOLVE_TARGET: target = substation if not 'Global' else region
    
    3. DATA_LOAD:
           df = db_archive.load_data(target, start=dates.begin, end=dates.end)
           df_rhythm = db_archive.load_rhythm(target, dates)
           
    4. RENDER_METRICS:
           c1.metric("Peak Load", df.load.max())
           c2.metric("Avg Health", df.health.mean())
           
    5. CORRELATION_BLOCKS:
           render_dual_chart(df, load, air_temp, colors=(orange, blue))
           render_dual_chart(df, load, oil_temp, colors=(orange, red))
           render_dual_chart(df, health, h2_gas, colors=(green, purple))
           
    6. RHYTHM_BLOCK: render_rhythm_chart(df_rhythm)
    7. RAW_TABLE: render_data_table(df)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: ASSET HEALTH & H2 (DGA) DIAGNOSTICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Діагностика здоров'я та газів (DGA)</h2></div>
    <div class="glass-card flow-step">
        <p>Архівний модуль інтегрує дані **Dissolved Gas Analysis (DGA)**. На графіку "Здоров'я vs H2" оператор може побачити, як сплески концентрації водню (H2) корелюють з падінням індексу <code>Health Score</code>. Це дозволяє технічному персоналу обґрунтовано планувати позачергові огляди трансформаторів та запобігати аваріям до їх фактичного виникнення, використовуючи ретроспективні тренди як доказ.</p>
    </div>
</div>

<!-- SECTION 08: HANDLING MULTI-SUBSTATION AGGREGATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Обробка масової агрегації підстанцій</h2></div>
    <div class="glass-card flow-step">
        <p>При перегляді архіву для цілого регіону або групи підстанцій, модуль автоматично застосовує **Смарт-агрегацію (Mean Aggregation)**. Це прибирає "візуальний шум" (пилку) від окремих дрібних стрибків навантаження, залишаючи чистий системний тренд. Векторизована обробка в Pandas гарантує, що розрахунок середнього для 100+ об'єктів за місяць займає лічені частки секунди.</p>
    </div>
</div>

<!-- SECTION 09: INTERACTIVE DATA GRID (RAW ACCESS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Інтерактивна таблиця сирих даних (Raw Access)</h2></div>
    <div class="glass-card flow-step">
        <p>Для професійних аудиторів, яким потрібні точні цифри, <code>historical_audit.py</code> надає доступ до <b>Raw Data Table</b>. Таблиця підтримує вбудований пошук, сортування та фільтрацію. Користувач може знайти точне значення температури масла в конкретну хвилину інциденту і звірити його з логами в <code>alerts.py</code>, забезпечуючи повноцінний ланцюжок верифікації події.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM SPACER & SCROLLING (UX FIX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Комфорт скролінгу (UX Fix)</h2></div>
    <div class="glass-card flow-step">
        <p>Оскільки архівна вкладка містить багато розгорнутих графіків та велику таблицю в кінці, ми додали технічний Spacer (300px). Це дозволяє користувачеві прокрутити всю сторінку так, щоб нижні рядки таблиці даних або підписи осей останнього графіка знаходилися у комфортній зоні видимості, не перекриваючись елементами інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>Archive Service</h4>
                <p>SQL-провайдер історичних зрізів та меж даних.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📈</div>
            <div class="role-content">
                <h4>Chart Components</h4>
                <p>Бібліотека спеціалізованих Dual-Axis та Rhythm діаграм.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">⚙️</div>
            <div class="role-content">
                <h4>Pandas Core</h4>
                <p>Ядро для математичної агрегації та очищення масивів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (AI ANOMALY DETECTION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (AI Anomaly Detection)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Автоматичного детектора аномалій</b>. Архів буде не просто показувати графіки, а самостійно маркувати періоди, де кореляція між навантаженням та температурою масла була порушена (ознака дефекту системи охолодження). Також буде додано підтримку <b>Експорту в Excel/PDF</b> з автоматичною генерацією технічних висновків.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Архів та Аудит</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому дані за останню годину не відображаються?</b> — Архів оперує закритими годинами. Поточні дані дивіться у вкладці "Monitoring".</p>
        <p><b>Як порівняти дві різні підстанції в архіві?</b> — Оберіть їх у глобальному фільтрі, система автоматично побудує агрегований порівняльний тренд.</p>
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
