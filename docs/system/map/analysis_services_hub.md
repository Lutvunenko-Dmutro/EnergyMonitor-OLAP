# Технічна специфікація: Хаб Просунутих Аналітичних Сервісів (ANALYSIS SERVICES HUB)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ANALYTICS ENGINE | DATA MINING & PATTERNS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔍</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Центр Аналітики</h1>
            <p class="mega-subtitle">Екосистема спеціалізованих сервісів для глибокого аналізу паттернів навантаження, виявлення аномалій та автоматизованого тестування енергосистеми ATLAS</p>
            <div class="status-tags"><span class="tag tag-online">MINING ACTIVE</span><span class="tag tag-version">v3.2.0</span><span class="tag tag-role">ANALYTIC SERVICES</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Decomposition</span><span class="metric-value">Seasonal & Trend Logic</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Segmentation</span><span class="metric-value">Automated Clustering</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧪</div><div class="metric-info"><span class="metric-label">Testing</span><span class="metric-value">Intersection Logic Checks</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Integrity</span><span class="metric-value">Diagnostic Scan Engine</span></div></div>
</div>

<!-- SECTION 01: FUNCTIONAL OVERVIEW -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Функціональний Огляд Сервісів</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/services/analysis/</code> містить інтелектуальні алгоритми, які перетворюють "сирі" дані телеметрії на цінні інсайти. Тут зосереджена логіка виявлення довгострокових трендів, сезонних коливань та прихованих закономірностей у споживанні електроенергії. Ці сервіси є фундаментом для прийняття стратегічних рішень в управлінні енергосистемою, дозволяючи передбачати пікові навантаження та оптимізувати розподіл ресурсів.</p>
    </div>
</div>

<!-- SECTION 02: ANALYSIS MODULES MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Матриця Аналітичних Модулів</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль</th>
                    <th>Функція</th>
                    <th>Методологія</th>
                    <th>Результат</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>advanced_mining.py</code></td><td>Data Mining</td><td>Association Rules</td><td>Виявлення кореляцій</td></tr>
                <tr><td><code>trends_and_patterns.py</code></td><td>Trend Analysis</td><td>STL Decomposition</td><td>Трендові графіки</td></tr>
                <tr><td><code>analytics_advanced.py</code></td><td>Complex KPIs</td><td>Aggregated Stats</td><td>Глибокі метрики</td></tr>
                <tr><td><code>intersection_tester.py</code></td><td>Logic Validation</td><td>Boundary Checks</td><td>Звіти про помилки</td></tr>
                <tr><td><code>diag_columns.py</code></td><td>Structure Scan</td><td>Metadata Audit</td><td>Цілісність БД</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: TREND DECOMPOSITION STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Декомпозиції Трендів</h2></div>
    <div class="glass-card flow-step">
        <p>Для розуміння природи змін у навантаженні ми використовуємо метод **STL (Seasonal-Trend decomposition using Loess)**. Це дозволяє розділити часовий ряд на три складові: <i>Trend</i> (загальний рух вгору чи вниз), <i>Seasonal</i> (повторювані цикли, наприклад, добові чи тижневі) та <i>Residual</i> (випадковий шум). Такий аналіз критично важливий для відділення реальних змін у споживанні від звичайних добових циклів.</p>
    </div>
</div>

<!-- SECTION 04: ANALYTIC PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема Аналітичного Конвеєра</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA_IN("Raw Telemetry Data") --> PRE_PROCESS("Data Cleansing & Normalization")
    PRE_PROCESS --> TREND_ENGINE("Trend & Pattern Analysis")
    PRE_PROCESS --> MINING_ENGINE("Advanced Data Mining")
    
    TREND_ENGINE --> DASHBOARD("UI Visualizations")
    MINING_ENGINE --> INSIGHTS("Strategic Insights Report")
    
    subgraph VALIDATION["Diagnostic & Logic Validation"]
        INTERSECT("Intersection Tester")
        DIAG_COLS("Column Integrity Scanner")
    end
    
    DATA_IN --> VALIDATION
    VALIDATION --> ALERTS("System Integrity Alerts")
    </div></div>
</div>

<!-- SECTION 05: AUTOMATED LOGIC & BOUNDARY TESTING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Автоматизоване Тестування Логіки</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>automated_intersection_tester.py</code> забезпечує математичну верифікацію даних. Він перевіряє, щоб сума навантажень підстанцій збігалася з регіональним балансом, і щоб часові позначки в різних таблицях не мали розривів. Це "Цифровий Аудитор", який гарантує, що вся аналітика базується на фізично коректних та цілісних даних.</p>
    </div>
</div>

<!-- SECTION 06: ADVANCED DATA MINING CAPABILITIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Можливості Поглибленого Data Mining</h2></div>
    <div class="glass-card flow-step">
        <p>Ми використовуємо алгоритми <i>Advanced Mining</i> для пошуку неявних зв'язків. Наприклад, як температура повітря в одному регіоні впливає на стабільність частоти в іншому. Це дозволяє виявляти каскадні ефекти в енергосистемі ще до того, як вони стануть очевидними, забезпечуючи превентивне управління ризиками.</p>
    </div>
</div>

<!-- SECTION 07: DIAGNOSTIC SCANNING ENGINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Діагностичне Сканування Структури</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>diag_columns.py</code> постійно моніторить структуру бази даних та метадані. У випадку зміни схеми даних або появи непередбачуваних форматів у вхідних потоках, сканер негайно сигналізує про проблему. Це забезпечує <b>Структурну Стійкість</b> проекту ATLAS, запобігаючи аварійним зупинкам аналітичних конвеєрів через помилки у форматі даних.</p>
    </div>
</div>

<!-- SECTION 08: SEASONALITY & PATTERN RECOGNITION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Розпізнавання Паттернів та Сезонності</h2></div>
    <div class="glass-card flow-step">
        <p>Аналітичне ядро здатне автоматично розрізняти "енергетичні профілі" різних типів споживачів (промислові зони, житлові масиви, адміністративні центри). Це досягається через аналіз добових ритмів та використання статистичних критеріїв подібності, що дозволяє більш точно налаштовувати моделі прогнозування для кожного конкретного об'єкта.</p>
    </div>
</div>

<!-- SECTION 09: SYSTEM INTEGRITY & DIAGNOSTICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Цілісність Системи та Діагностика</h2></div>
    <div class="glass-card flow-step">
        <p>Кожен аналітичний запит супроводжується внутрішньою діагностикою. Ми не просто видаємо результат, ми оцінюємо його вірогідність (Confidence Score) на основі якості вхідних даних. Якщо дані занадто зашумлені або мають пропуски, система сповіщає про це користувача, забезпечуючи прозорість та наукову достовірність результатів.</p>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v4.0 (REAL-TIME ADAPTIVE ANALYTICS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v4.0 (Adaptive Analytics)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 4.0 планується впровадження **Адаптивної Аналітики Реального Часу**, яка самостійно переналаштовує параметри декомпозиції залежно від поточної ситуації в мережі. Також буде додано підтримку <i>Graph Analytics</i> для візуалізації складних топологічних зв'язків та впроваджено модулі автоматичного генерування текстових аналітичних звітів за допомогою LLM-агентів.</p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="./atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
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
