# Технічна специфікація: Модуль Поглибленої AI-Аналітики (ADVANCED AI VIEW GIGA-PASSPORT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CLUSTERING & TREND DECOMPOSITION | ADVANCED AI VIEW</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧩</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Поглиблена AI-Аналітика</h1>
            <p class="mega-subtitle">Система інтелектуальної сегментації мережі: автоматична кластеризація підстанцій (K-Means), декомпозиція часових рядів на тренди/сезонність та багатовимірний аналіз профілів навантаження</p>
            <div class="status-tags"><span class="tag tag-online">ADVANCED AI ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">DATA SCIENTIST</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Clustering</span><span class="metric-value">K-Means Segments</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Decomposition</span><span class="metric-value">Seasonal-Trend LOESS</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">UI Safety</span><span class="metric-value">Fragmented Rendering</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Scale</span><span class="metric-value">Logarithmic Analysis</span></div></div>
</div>

<!-- SECTION 01: ADVANCED AI ANALYTICS PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Поглибленої AI-Аналітики</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>advanced.py</code> є "Дослідницькою лабораторією" проекту ATLAS. Його мета — вийти за межі простого моніторингу та надати відповіді на питання "Чому?". Ми використовуємо методи <b>Unsupervised Learning</b> (навчання без учителя) для пошуку прихованих закономірностей у поведінці мережі. Наша філософія базується на **Сегментації Складності**: розбиваючи сотні підстанцій на декілька характерних кластерів та розкладаючи сигнали на складові, ми перетворюємо хаотичний потік даних на структуровану карту знань про енергосистему.</p>
    </div>
</div>

<!-- SECTION 02: ADVANCED ANALYTICAL PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр поглибленого аналізу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Load Time Series Data") --> DISPATCH("AI Tab Dispatcher")
    
    DISPATCH --> TAB_1("Fragment 1: Clustering Segment")
    DISPATCH --> TAB_2("Fragment 2: Trend Decomposition")
    
    TAB_1 --> FEAT("Feature Engineering (Profiles)")
    FEAT --> KMEANS("K-Means Clustering Logic")
    KMEANS --> CLUST_VIS("Cluster Map & Profile Charts")
    
    TAB_2 --> STL("Trend/Seasonal Decomposition")
    STL --> TREND_VIS("Component Breakdown Plots")
    
    CLUST_VIS --> UI("Advanced AI Dashboard")
    TREND_VIS --> UI
    </div></div>
</div>

<!-- SECTION 03: CLUSTERING & SEGMENTATION STRATEGY (📊) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія кластеризації та сегментації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль реалізує автоматичне групування об'єктів енергосистеми:</p>
        <ul>
            <li><b>K-Means Core:</b> Використання алгоритму K-Means для виділення типових профілів споживання (наприклад, "Промисловий", "Побутовий", "Змішаний").</li>
            <li><b>Feature Matrix:</b> Перетворення часового ряду в матрицю ознак, де кожна година доби є виміром у багатовимірному просторі.</li>
            <li><b>Visual Feedback:</b> Відображення центроїдів кластерів, що дозволяє оператору бачити "ідеальну середню" поведінку для кожної групи підстанцій.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: TREND DECOMPOSITION (STL ANALYSIS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Декомпозиція трендів (STL Аналіз)</h2></div>
    <div class="glass-card flow-step">
        <p>Аналітичне розкладання складного сигналу на складові:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Компонент</th>
                    <th>Опис</th>
                    <th>Аналітичне значення</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Trend</td><td>Довгостроковий напрямок</td><td>Виявлення зростання/падіння промисловості</td></tr>
                <tr><td>Seasonality</td><td>Добові/Тижневі цикли</td><td>Аналіз ритмічності життя регіону</td></tr>
                <tr><td>Residue (Noise)</td><td>Залишкові відхилення</td><td>Пошук аномалій та непередбачуваних викидів</td></tr>
                <tr><td>Multi-scale</td><td>Log/Relative toggle</td><td>Адаптація масштабу для мікро- та макро-об'єктів</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: FRAGMENT-BASED UI STABILITY (🛡️) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Стабільність інтерфейсу через фрагменти</h2></div>
    <div class="glass-card flow-step">
        <p>Для запобігання "фризам" при виконанні важких математичних розрахунків, модуль використовує <code>@st.fragment</code>. Кожна вкладка (Кластеризація та Тренди) працює в ізольованому потоці оновлення. Це гарантує, що зміна параметрів кластеризації не призведе до повного перезавантаження всього дашборду ATLAS, зберігаючи плавність UX та стан інших віджетів.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (ADVANCED ANALYTICS CORE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод ядра поглибленої аналітики</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_advanced_ai(df, selected_sub):
    1. VALIDATE columns (substation_name, actual_load, timestamp)
    
    2. CREATE TABS ["Clustering", "Trend Analysis"]
    
    3. @st.fragment TAB_1 (Clustering):
           GET use_log = toggle("Log Scale")
           CALL clustering_view.render(df, use_log) # ML Logic
           
    4. @st.fragment TAB_2 (Trends):
           GET use_rel = toggle("Relative Load")
           CALL trend_view.render(df, selected_sub, use_rel) # STL Logic
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: MULTIDIMENSIONAL SCALING LOGIC -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Логіка багатовимірного масштабування</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль підтримує перемикання між <b>лінійною</b> та <b>логарифмічною</b> шкалами для кластерного аналізу. Логарифмічне масштабування є критичним при одночасному аналізі об'єктів різного порядку (наприклад, магістральних підстанцій та локальних вузлів), дозволяючи виявити схожість патернів поведінки навіть при величезній різниці в абсолютній потужності.</p>
    </div>
</div>

<!-- SECTION 08: INTELLIGENT DATA VALIDATION (🩸) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Інтелектуальна валідація даних</h2></div>
    <div class="glass-card flow-step">
        <p>Перед запуском ML-алгоритмів модуль проводить перевірку цілісності. Якщо в DataFrame відсутні критичні колонки (наприклад, <code>substation_name</code>) або даних недостатньо для навчання кластеризатора, система видає інформативне попередження замість системної помилки Python, що робить ШІ-блок надійним та зручним для користувача-не-програміста.</p>
    </div>
</div>

<!-- SECTION 09: CUSTOM POPOVER TOOLSETS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Кастомні набори інструментів (Popovers)</h2></div>
    <div class="glass-card flow-step">
        <p>Для збереження чистоти HUD-інтерфейсу, всі складні налаштування ML-алгоритмів (тогли масштабування, вибір метрик) винесені у <b>Popovers</b>. Це дозволяє оператору бачити графіки на весь екран, маючи швидкий доступ до тюнінгу параметрів аналізу через спливаючі панелі управління.</p>
    </div>
</div>

<!-- SECTION 10: MEMORY-EFFICIENT ML DISPATCHING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Енергоефективна ML-диспетчеризація</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль реалізує принцип "Обчислюй за запитом". Розрахунок кластерів або декомпозиція трендів не запускається автоматично при завантаженні ATLAS. Обчислювальний конвеєр активується лише при відкритті відповідної вкладки "Advanced Analysis", що економить ресурси CPU/RAM сервера для основних задач моніторингу.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Clustering View</h4>
                <p>Низькорівнева реалізація K-Means та візуалізації центроїдів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📈</div>
            <div class="role-content">
                <h4>Trend View</h4>
                <p>Математичний модуль декомпозиції часових рядів (STL/Seasonality).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🧬</div>
            <div class="role-content">
                <h4>Scikit-learn / Statsmodels</h4>
                <p>Фундаментальні ML-бібліотеки для поглибленої аналітики.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (ANOMALY CLUSTERING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v2.0 (Anomaly Clustering & 3D)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується впровадження <b>3D-візуалізації кластерів</b> (через PCA-проекцію), автоматична <b>детекція кластерних аномалій</b> (Outlier Detection) та інтеграція <b>спільного аналізу з кореляцією погодних полів</b> для пояснення причин зсуву профілів споживання.</p>
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
