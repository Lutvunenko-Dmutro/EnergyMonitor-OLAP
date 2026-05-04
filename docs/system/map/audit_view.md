# Технічна специфікація модуля: ui/views/historical_audit.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DIGITAL ARCHIVE & PHYSICAL AUDIT SYSTEM</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📜</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Цифровий Архів ATLAS</h1>
            <p class="mega-subtitle">Система поглибленого ретроспективного аналізу: термодинамічна діагностика, крос-параметрична кореляція, аналіз ритмів та фізичний аудит активів</p>
            <div class="status-tags"><span class="tag tag-online">ARCHIVE HUB ACTIVE</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">AUDIT OFFICER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Audit</span><span class="metric-value">Cross-Correlation</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌡️</div><div class="metric-info"><span class="metric-label">Thermal</span><span class="metric-value">Oil-Load Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⏳</div><div class="metric-info"><span class="metric-label">Pulse</span><span class="metric-value">Rhythm Analysis</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📑</div><div class="metric-info"><span class="metric-label">Data</span><span class="metric-value">Raw Data Access</span></div></div>
</div>

<!-- SECTION 01: DIGITAL ARCHIVE & PHYSICAL AUDIT PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Цифрового Архіву та Аудиту</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>historical_audit.py</code> є "Пам'яттю та Слідчим" проекту ATLAS. В енергетиці справжнє розуміння проблем приходить лише через аналіз минулого. Цифровий архів дозволяє проводити глибокий фізичний аудит: відстежувати, як погодні умови впливали на навантаження рік тому, або як критичні перевантаження прискорювали деградацію (збільшення H2) трансформаторів. Це не просто база даних, а інструмент доказової аналітики для розслідування інцидентів та верифікації моделей прогнозування.</p>
    </div>
</div>

<!-- SECTION 02: CROSS-PARAMETER CORRELATION ARCHITECTURE -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Архітектура крос-параметричної кореляції</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    ARCH("Archive DB: load_archive_data") --> CLEAN("Data Normalization & Cleaning")
    CLEAN --> CORR_1("Correlation: Load vs Air Temp")
    CLEAN --> CORR_2("Correlation: Load vs Oil Temp")
    CLEAN --> CORR_3("Correlation: Health vs H2 PPM")
    CORR_1 & CORR_2 & CORR_3 --> DUAL("Dual-Axis Visualization Engine")
    DUAL --> UI("Interactive Audit Report")
    </div></div>
</div>

<!-- SECTION 03: ASSET HEALTH AUDIT (HISTORICAL DEGRADATION) -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Аудит здоров'я активів (Історична деградація)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль реалізує унікальний аналіз зв'язку між навантаженням та фізичним зносом. Через <b>Dual-Axis графіки</b> оператор бачить:</p>
        <ul>
            <li><b>Health Score Decay:</b> Тренди зниження надійності об'єкта протягом місяців.</li>
            <li><b>H2 PPM Correlation:</b> Прямий зв'язок між піковими навантаженнями та сплесками концентрації газів у маслі (індикатор внутрішніх пошкоджень).</li>
            <li><b>Predictive Validation:</b> Можливість порівняти, чи передбачив ШІ реальну деградацію об'єкта, зафіксовану в архіві.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: RHYTHM ANALYSIS (ENERGY PULSE) -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Аналіз енергетичних ритмів (Energy Pulse)</h2></div>
    <div class="glass-card flow-step">
        <p>Механізм <b>Rhythm Analysis</b> дозволяє верифікувати математичну модель <code>day_multiplier</code>:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Параметр</th>
                    <th>Опис ритму</th>
                    <th>Значення для аудиту</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Будні дні</td><td>Високоамплітудні добові коливання</td><td>Верифікація промислових навантажень</td></tr>
                <tr><td>Вихідні дні</td><td>Згладжений профіль зі зниженим базовим рівнем</td><td>Верифікація побутового сектору</td></tr>
                <tr><td>Shift Factor</td><td>Зсув фази піку між типами днів</td><td>Тонке налаштування ML-моделей</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: THERMODYNAMIC DIAGNOSTICS (OIL-LOAD SYNC) -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Термодинамічна діагностика: Теплове мапування</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль фокусується на <b>Тепловій Діагностиці</b> трансформаторного парку. Візуалізація кореляції <code>Load vs Oil Temp</code> дозволяє виявити об'єкти з порушеною системою охолодження: якщо температура масла зростає непропорційно швидко при помірному навантаженні — об'єкт потребує негайного технічного обслуговування.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (ARCHIVE LOADER & ANALYZER) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод завантажувача та аналізатора архіву</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render(region, date_range, substation):
    1. GET_ARCHIVE_BOUNDS() from database
    2. NORMALIZE date_range to actual data presence
    
    3. LOAD_DATA:
           df = load_archive_data(start, end, target_sub)
           df_rhythm = load_rhythm_data(start, end, target_sub)
           
    4. CALCULATE Historical Metrics (Max Load, Min Air Temp, Avg Health)
    
    5. RENDER DUAL-AXIS CHARTS:
           CHART_1: Load vs Air Temperature (Weather Impact)
           CHART_2: Load vs Oil Temperature (Cooling Integrity)
           CHART_3: Health vs H2 Concentration (Degradation Tracking)
           
    6. RENDER Rhythm_Chart (Workdays vs Weekends)
    7. EXPOSE Raw_Data_Table (Sortable/Filterable)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: CROSS-PARAMETER DUAL-AXIS ENGINE -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Двигун крос-параметричної візуалізації (Dual-Axis)</h2></div>
    <div class="glass-card flow-step">
        <p>Для порівняння параметрів з різними одиницями виміру (наприклад, МВт та ppm) використовується <b>Dual-Axis Engine</b>. Це дозволяє накладати дві криві на одне часове поле з різними шкалами Y (ліворуч та праворуч). Такий підхід робить візуально очевидними моменти, коли зміна одного параметра (температури) тригерує зміну іншого (споживання).</p>
    </div>
</div>

<!-- SECTION 08: RAW DATA ACCESS & EXPORT INTERFACE -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Інтерфейс доступу та експорту сирих даних</h2></div>
    <div class="glass-card flow-step">
        <p>В кінці звіту модуль надає прямий доступ до агрегованого масиву через <code>render_raw_data_table</code>. Користувач може сортувати записи, фільтрувати їх та переглядати точні цифри, що стояли за графіками. Це забезпечує "Прозорість Аудиту" — можливість перевірити будь-яку точку на графіку через табличне представлення.</p>
    </div>
</div>

<!-- SECTION 09: DYNAMIC REPORT HEADER (CONTEXT AWARE) -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Динамічний заголовок звіту (Context Aware)</h2></div>
    <div class="glass-card flow-step">
        <p>Система автоматично формує заголовок на основі фільтрів: "Аналіз для Київського регіону", "Аналіз для ПС 'Північна'" тощо. Це дозволяє створювати готові до друку звіти, які вже містять весь необхідний контекст аналізу (об'єкт, період, тип даних).</p>
    </div>
</div>

<!-- SECTION 10: MEMORY OPTIMIZATION FOR LONG-RANGE QUERIES -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Оптимізація пам'яті для довготривалих запитів</h2></div>
    <div class="glass-card flow-step">
        <p>При запитах за великі періоди (наприклад, рік), система виконує <b>серверну агрегацію</b> (Mean per Hour) на рівні SQL. Це зменшує обсяг даних, що передаються по мережі та завантажуються в RAM браузера, у 60 разів (похвилинна -> погодинна), зберігаючи при цьому всі ключові аналітичні тренди.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🗄️</div>
            <div class="role-content">
                <h4>Archive Engine</h4>
                <p>Низькорівневі SQL-запити для завантаження та агрегації великих масивів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📉</div>
            <div class="role-content">
                <h4>Chart Library</h4>
                <p>Забезпечує рендер Dual-Axis та Rhythm діаграм.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛡️</div>
            <div class="role-content">
                <h4>UI Helpers</h4>
                <p>Гарантує стабільність відображення через <code>safe_plotly_render</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (BLOCKCHAIN AUDIT) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v2.0 (Blockchain & Legal Compliance)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується впровадження <b>Blockchain-логізації</b> для незмінності архівних даних (Legal Compliance), підтримка <b>автоматичного пошуку кореляційних аномалій</b> через AI та інтеграція <b>системи генерації PDF-звітів</b> одним кліком для подання в органи контролю.</p>
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
