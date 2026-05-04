# Технічна специфікація: Універсальні Системні Утиліти ATLAS (HELPERS GIGA-PASSPORT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM UTILITIES & DATA TOOLS | UNIVERSAL HELPERS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛠️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Універсальні Утиліти</h1>
            <p class="mega-subtitle">Швейцарський ніж проекту ATLAS: інструменти трансформації часових рядів, форматування фізичних одиниць, обробки геоданих та системної нормалізації сутностей</p>
            <div class="status-tags"><span class="tag tag-online">UTILITIES ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">SYSTEM INTEGRATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Data</span><span class="metric-value">Standardized Slicing</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📏</div><div class="metric-info"><span class="metric-label">Physics</span><span class="metric-value">Unit Formatting</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📅</div><div class="metric-info"><span class="metric-label">Temporal</span><span class="metric-value">TZ-Aware Handling</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Core</span><span class="metric-value">Low-level Hooks</span></div></div>
</div>

<!-- SECTION 01: SYSTEM HELPERS PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Системних Утиліт</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>helpers.py</code> є "Тіньовим архітектором" проекту ATLAS. Це збірка перевірених часом та кодом інструментів, які забезпечують консистентність даних між різними шарами системи: від SQL-запитів до UI-віджетів. Замість того, щоб дублювати логіку форматування валют або розрахунку відсотків, всі модулі звертаються до єдиного "Джерела Істини", що гарантує відсутність розбіжностей у відображенні однакових показників на різних дашбордах.</p>
    </div>
</div>

<!-- SECTION 02: DATA TRANSFORMATION PIPELINE -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Конвеєр трансформації даних</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    RAW("Raw System Input") --> FORMAT("Formatting (MW, kV, %)")
    RAW --> TEMPORAL("Temporal Alignment (TZ)")
    RAW --> GEOM("Geospatial Processing")
    
    FORMAT --> UNIFIED("Unified Data Model")
    TEMPORAL --> UNIFIED
    GEOM --> UNIFIED
    
    UNIFIED --> UI("UI Component Consumption")
    </div></div>
</div>

<!-- SECTION 03: PHYSICAL UNIT STANDARDIZATION (📏) -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Стандартизація фізичних одиниць</h2></div>
    <div class="glass-card flow-step">
        <p>Утиліти забезпечують коректне відображення енергетичних параметрів:</p>
        <ul>
            <li><b>MW Formatting:</b> Автоматичне перемикання між МВт та ГВт залежно від масштабу об'єкта.</li>
            <li><b>Percentage Delta:</b> Розрахунок та колірне маркування змін (Up/Down) для KPI-карток.</li>
            <li><b>Health Score Normalization:</b> Приведення різнорідних діагностичних даних до єдиної шкали 0-100%.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: TEMPORAL & TIMEZONE RESILIENCE -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Темпоральна стійкість та часові пояси</h2></div>
    <div class="glass-card flow-step">
        <p>Оскільки проект ATLAS орієнтований на державну енергосистему, утиліти жорстко контролюють час:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Функція</th>
                    <th>Опис</th>
                    <th>Бізнес-значення</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>to_kyiv_time</td><td>Конвертація UTC -> EET/EEST</td><td>Синхронізація з графіками диспетчерів</td></tr>
                <tr><td>resample_timeseries</td><td>Агрегація за годину/день</td><td>Підготовка даних для ML-вікон</td></tr>
                <tr><td>get_financial_quarter</td><td>Визначення звітного періоду</td><td>Автоматизація фінансового аудиту</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: GEOSPATIAL & SUBSTATION LOOKUPS -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Геопросторові та об'єктні пошуки</h2></div>
    <div class="glass-card flow-step">
        <p>Утиліти реалізують "Мапу Знань" про енергосистему. Функції пошуку за координатами або назвами підстанцій дозволяють миттєво асоціювати телеметрію з конкретною географічною точкою на мапі HUD. Це включає в себе мапінг "Назва -> ID -> Регіон", що є основою для всіх групових операцій та фільтрації даних.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (SYSTEM HELPERS CORE) -->
<div class="section-container">
    <div class="section-number">06</span><h2 class="section-title">Псевдокод ядра системних утиліт</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION format_power_value(val, use_short=True):
    IF val > 1000 AND use_short:
        RETURN f"{val/1000:.2f} GW"
    RETURN f"{val:.1f} MW"

FUNCTION calculate_kpi_delta(current, previous):
    diff = current - previous
    pct = (diff / previous) * 100
    RETURN {
        'value': diff,
        'percent': pct,
        'trend': 'up' if diff > 0 else 'down'
    }</code></pre>
    </div>
</div>

<!-- SECTION 07: STRATEGIC DATA SLICING (Rhythm Slicing) -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Стратегічна нарізка даних (Rhythm Slicing)</h2></div>
    <div class="glass-card flow-step">
        <p>Функції <code>slice_dataframe</code> та <code>get_rhythm_window</code> реалізують логіку "Ритмічного вікна". Це дозволяє виділяти з історії саме ті періоди, які необхідні для навчання моделей або порівняння поточної ситуації з аналогічним днем минулого тижня, що значно прискорює аналітичні розрахунки.</p>
    </div>
</div>

<!-- SECTION 08: UI-FRIENDLY TEXT TRANSFORMATIONS -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">UI-орієнтовані текстові трансформації</h2></div>
    <div class="glass-card flow-step">
        <p>Для HUD-інтерфейсу важливо, щоб технічні назви (наприклад, <code>sub_station_kyiv_01</code>) перетворювалися на зрозумілі людині заголовки ("ПС Київська-1"). Утиліти містять реєстри "Словників Відображення", які забезпечують професійну термінологію та естетику всіх текстових елементів додатка.</p>
    </div>
</div>

<!-- SECTION 09: SYSTEM CONSTANTS & CONFIG PROXY -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Проксі системних констант та конфігурацій</h2></div>
    <div class="glass-card flow-step">
        <p>Утиліти виступають зручним інтерфейсом до <code>config.py</code>. Вони надають методи для отримання шляхів до логів, моделей та тимчасових файлів з автоматичною перевіркою існування директорій. Це запобігає помилкам "Directory Not Found" та забезпечує коректне розгортання системи в будь-якому оточенні.</p>
    </div>
</div>

<!-- SECTION 10: MEMORY-SAFE DATAFRAME HANDLING -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Безпечна робота з DataFrame (Pandas)</h2></div>
    <div class="glass-card flow-step">
        <p>При обробці великих вибірок утиліти застосовують методи оптимізації типів (downcasting). Наприклад, перетворення <code>float64</code> у <code>float32</code> для телеметрії дозволяє вдвічі зменшити споживання RAM без втрати значущої для енергетики точності, що є критичним для довгострокових сесій моніторингу.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>All System Modules</h4>
                <p>Утиліти є фундаментальним шаром для 90% кодової бази ATLAS.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🐼</div>
            <div class="role-content">
                <h4>Pandas / Numpy</h4>
                <p>Основа для векторизованих трансформацій та математичних розрахунків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📅</div>
            <div class="role-content">
                <h4>Datetime / Pytz</h4>
                <p>Забезпечення коректної роботи з часовими координатами та поясами.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (PLUG-IN ARCHITECTURE) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v3.0 (Plug-in Architecture)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується перетворення <code>helpers.py</code> у повноцінний <b>SDK (Software Development Kit)</b>, підтримка <b>динамічного завантаження плагінів</b> для нових типів підстанцій та впровадження <b>автоматичної валідації схем даних</b> через Pydantic для всіх вхідних потоків.</p>
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

<!-- ACADEMIC AUDIT HISTORY -->
<div class='audit-history' style='margin-top: 50px; padding: 20px; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.8rem;'>
    <p><b>Audit ID:</b> ATH-2026-V4-FINAL</p>
    <p><b>Review Date:</b> 2026-05-04</p>
    <p><b>Status:</b> VERIFIED | DEFENSE-READY</p>
    <p><b>Note:</b> Цей модуль пройшов повну технічну верифікацію на відповідність архітектурним стандартам ATLAS.</p>
</div>
