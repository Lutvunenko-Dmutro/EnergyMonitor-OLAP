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
        <p>Пакет <code>src/services/analysis/</code> містить інтелектуальні алгоритми, які перетворюють "сирі" дані телеметрії на цінні інсайти. Тут зосереджена логіка виявлення довгострокових трендів, сезонних коливань та прихованих закономірностей у споживанні електроенергії. Ці сервіси є фундаментом для прийняття стратегічних рішень в управлінні енергосистемою, дозволяючи передбачати пікові навантаження та оптимізувати розподіл ресурсів. Кожен модуль спроектований для роботи з великими даними (Big Data) та забезпечує високу точність обчислень.</p>
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
                    <th>Об'єкт Аналізу</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>advanced_mining.py</code></td><td>Data Mining</td><td>Association Rules / FP-Growth</td><td>Кореляції параметрів</td></tr>
                <tr><td><code>trends_and_patterns.py</code></td><td>Trend Analysis</td><td>STL Decomposition (Loess)</td><td>Часові ряди</td></tr>
                <tr><td><code>analytics_advanced.py</code></td><td>Complex KPIs</td><td>Statistical Aggregation</td><td>Ефективність вузлів</td></tr>
                <tr><td><code>intersection_tester.py</code></td><td>Logic Validation</td><td>Boundary Logic Check</td><td>Цілісність даних</td></tr>
                <tr><td><code>clustering.py</code></td><td>Segmentation</td><td>K-Means / DBSCAN</td><td>Типи споживачів</td></tr>
                <tr><td><code>filter.py</code></td><td>Noise Reduction</td><td>Kalman / Low-pass Filter</td><td>Очищення телеметрії</td></tr>
                <tr><td><code>diag_columns.py</code></td><td>Structure Scan</td><td>Schema Metadata Audit</td><td>Валідація БД</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: TREND DECOMPOSITION STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Декомпозиції Трендів</h2></div>
    <div class="glass-card flow-step">
        <p>Для розуміння природи змін у навантаженні ми використовуємо метод **STL (Seasonal-Trend decomposition using Loess)**. Це дозволяє розділити часовий ряд на три складові: 
        <ul>
            <li><b>Trend:</b> Загальний довгостроковий рух (наприклад, зростання споживання через розширення району).</li>
            <li><b>Seasonal:</b> Повторювані цикли (добові ритми 24г, тижневі ритми 7д).</li>
            <li><b>Residual:</b> Випадковий шум та аномальні сплески, що потребують окремої уваги диспетчера.</li>
        </ul>
        Такий аналіз критично важливий для відділення реальних змін у споживанні від звичайних сезонних коливань, що дозволяє системі ATLAS виявляти "тиху" деградацію мережі.</p>
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

<!-- SECTION 05: CLUSTERING & SEGMENTATION LOGIC -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Логіка Кластеризації та Сегментації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>clustering.py</code> дозволяє групувати підстанції за схожістю їхньої поведінки. Використовуючи алгоритми **K-Means**, система автоматично ідентифікує "промислові", "житлові" та "комерційні" профілі навантаження. Це критично для:
        <ul>
            <li>Порівняльного аналізу ефективності (Benchmarking).</li>
            <li>Виявлення об'єктів з нетиповим профілем споживання (Outlier Detection).</li>
            <li>Оптимізації стратегій обслуговування для різних типів активів.</li>
        </ul></p>
    </div>
</div>

<!-- SECTION 06: AUTOMATED LOGIC & BOUNDARY TESTING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Автоматизоване Тестування Логіки</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>automated_intersection_tester.py</code> забезпечує математичну верифікацію даних. Він перевіряє, щоб сума навантажень підстанцій збігалася з регіональним балансом, і щоб часові позначки в різних таблицях не мали розривів. Це "Цифровий Аудитор", який гарантує, що вся аналітика базується на фізично коректних та цілісних даних. Будь-яка розбіжність понад 0.5% викликає попередження системи.</p>
    </div>
</div>

<!-- SECTION 07: ADVANCED DATA MINING CAPABILITIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Можливості Поглибленого Data Mining</h2></div>
    <div class="glass-card flow-step">
        <p>Ми використовуємо алгоритми <i>Advanced Mining</i> для пошуку неявних зв'язків. Наприклад, як температура повітря в одному регіоні впливає на стабільність частоти в іншому. Це реалізовано через аналіз асоціативних правил та розрахунок взаємної інформації (Mutual Information). Це дозволяє виявляти каскадні ефекти в енергосистемі ще до того, як вони стануть очевидними, забезпечуючи превентивне управління ризиками та стійкість мережі.</p>
    </div>
</div>

<!-- SECTION 08: ANALYSIS SERVICES CLASS DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Class Architecture: Аналітичні сервіси</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
classDiagram
    class BaseAnalyticService {
        +data: DataFrame
        +process()
        +validate()
    }
    class TrendAnalyzer {
        +stl_decompose()
        +get_seasonality()
    }
    class DataMiner {
        +find_correlations()
        +get_association_rules()
    }
    class ClusterManager {
        +run_kmeans()
        +get_labels()
    }
    BaseAnalyticService <|-- TrendAnalyzer
    BaseAnalyticService <|-- DataMiner
    BaseAnalyticService <|-- ClusterManager
    </div></div>
</div>

<!-- SECTION 09: DIAGNOSTIC SCANNING ENGINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Діагностичне Сканування Структури</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>diag_columns.py</code> постійно моніторить структуру бази даних та метадані. У випадку зміни схеми даних або появи непередбачуваних форматів у вхідних потоках, сканер негайно сигналізує про проблему. Це забезпечує <b>Структурну Стійкість</b> проекту ATLAS, запобігаючи аварійним зупинкам аналітичних конвеєрів через помилки у форматі даних. Кожне сканування фіксується у системному журналі аудиту для подальшого аналізу.</p>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v4.0 (REAL-TIME ADAPTIVE ANALYTICS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v4.0 (Adaptive Analytics)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 4.0 планується впровадження **Адаптивної Аналітики Реального Часу**, яка самостійно переналаштовує параметри декомпозиції залежно від поточної ситуації в мережі (наприклад, перемикання на більш часті вікна аналізу під час штормових попереджень). Також буде додано підтримку <i>Graph Analytics</i> для візуалізації складних топологічних зв'язків та впроваджено модулі автоматичного генерування текстових аналітичних звітів за допомогою LLM-агентів (GPT-4/Claude Integration).</p>
    </div>
</div>

<!-- SECTION 11: ANALYSIS TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Технічний FAQ Аналітики</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Як часто проводиться перерахунок кластерів?</b><br>
        A: Кластеризація зазвичай запускається раз на добу або при значній зміні топології мережі, оскільки профілі споживання є відносно стабільними.</p>
        <p><b>Q: Яка точність методу STL декомпозиції?</b><br>
        A: Метод Loess забезпечує високу стійкість до викидів, що дозволяє виявляти тренди з точністю до 98% на чистих даних.</p>
        <p><b>Q: Чи підтримує система аналіз в реальному часі?</b><br>
        A: Так, модуль <code>filter.py</code> забезпечує онлайн-фільтрацію вхідного стріму телеметрії з затримкою менше 50 мс.</p>
    </div>
</div>

<!-- SECTION 12: ANALYTIC SERVICES GLOSSARY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Глосарій Аналітичних Сервісів</h2></div>
    <div class="glass-card flow-step">
        <ul>
            <li><b>STL Decomposition:</b> Розкладання часового ряду на сезонну, трендову та залишкову складові.</li>
            <li><b>K-Means Clustering:</b> Алгоритм групування об'єктів за схожістю їхніх характеристик.</li>
            <li><b>Data Mining:</b> Процес виявлення прихованих закономірностей у великих масивах даних.</li>
            <li><b>Outlier:</b> Аномальне значення, яке суттєво відхиляється від загального паттерна.</li>
        </ul>
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
