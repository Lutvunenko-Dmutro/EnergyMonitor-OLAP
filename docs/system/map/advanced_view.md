# Технічна специфікація: Модуль Поглибленого Аналізу (ADVANCED ANALYSIS VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ADVANCED AI ANALYTICS | PATTERN DISCOVERY CORE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧩</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Поглиблений Аналіз</h1>
            <p class="mega-subtitle">Інтелектуальна підсистема декомпозиції та сегментації: виявлення прихованих закономірностей у поведінці енергосистеми через кластеризацію та аналіз трендів</p>
            <div class="status-tags"><span class="tag tag-online">ANALYTICS ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">DATA SCIENTIST</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Methods</span><span class="metric-value">Clustering / STL</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Fragment-Based</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Scale</span><span class="metric-value">Logarithmic Toggle</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Performance</span><span class="metric-value">Parallel Fragmenting</span></div></div>
</div>

<!-- SECTION 01: ADVANCED VIEW PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Поглибленого Аналізу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>advanced.py</code> є дослідницьким центром проекту ATLAS. Його мета — надати диспетчеру та аналітику інструменти для відповіді на питання "Чому це відбувається?". Ми використовуємо методи навчання без учителя (Unsupervised Learning) для групування схожих об'єктів та складну математичну декомпозицію сигналу на тренди та сезонність. Наша філософія базується на <b>Ізоляції Обчислень</b>: кожна важка аналітична вкладка працює у власному фрагменті Streamlit, не заважаючи іншим частинам інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 02: ANALYTICS DISPATCHER DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Диспетчеризація Аналітики (Architecture)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    MAIN("Main Dashboard") --> DISP("Advanced Dispatcher")
    DISP --> TAB_1("Clustering Tab (Fragment 1)")
    DISP --> TAB_2("Trend Analysis (Fragment 2)")
    
    TAB_1 --> TOOLS_1("Settings Popover (Log/Lin)")
    TOOLS_1 --> CLUST_ENGINE("Clustering Engine")
    CLUST_ENGINE --> VIS_1("Cluster Profiles & Centroids")
    
    TAB_2 --> TOOLS_2("Settings Popover (Rel/Abs)")
    TOOLS_2 --> TREND_ENGINE("STL Decomposition")
    TREND_ENGINE --> VIS_2("Trend/Seasonal/Residue Plots")
    </div></div>
</div>

<!-- SECTION 03: CLUSTERING & SEGMENTATION STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія кластеризації та сегментації</h2></div>
    <div class="glass-card flow-step">
        <p>Для розуміння структури споживання ми впровадили автоматичну сегментацію:</p>
        <ul>
            <li><b>K-Means Integration:</b> Виявлення типових профілів навантаження (промисловий, житловий, змішаний).</li>
            <li><b>Dynamic Centroids:</b> Візуалізація "ідеальної середньої" поведінки для кожного кластера.</li>
            <li><b>Substation Mapping:</b> Прив'язка обраної підстанції до її кластерного оточення для порівняльного аналізу.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: ANALYTICAL TOOLS MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця аналітичних інструментів</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Інструмент</th>
                    <th>Опис</th>
                    <th>Бізнес-цінність</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Log Scale</td><td>Перехід до логарифмічної шкали</td><td>Аналіз малих та великих об'єктів разом</td></tr>
                <tr><td>STL Decomposition</td><td>Розклад на Trend/Season/Noise</td><td>Виявлення аномальних відхилень від норми</td></tr>
                <tr><td>Fragment Cache</td><td>Ізольований рендеринг</td><td>Збереження стану при перемиканні вкладок</td></tr>
                <tr><td>Relative View</td><td>Відображення у % від номіналу</td><td>Порівняння об'єктів різної потужності</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: FRAGMENT-BASED STABILITY (UX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Стабільність через фрагменти (UX)</h2></div>
    <div class="glass-card flow-step">
        <p>Аналіз великих обсягів даних може спричиняти затримки. Завдяки декоратору <code>@st.fragment</code>, зміна параметрів (наприклад, перемикання на логарифмічну шкалу) оновлює тільки графік у межах поточної вкладки. Це запобігає повному перезавантаженню дашборду, що критично для збереження фокусу аналітика під час роботи з великою кількістю даних.</p>
    </div>
</div>

<!-- SECTION 06: CORE DISPATCHER LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Диспетчера (Dispatcher Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_advanced_analysis(df, selected_sub):
    1. VALIDATE: Ensure columns [name, load, ts] exist
    
    2. CREATE_TABS: ["Clustering", "Trend Analysis"]
    
    3. @st.fragment TAB_1:
           settings = popover("Clustering Settings")
           CALL clustering_engine.render(df, settings.use_log)
           
    4. @st.fragment TAB_2:
           settings = popover("Trend Settings")
           CALL trend_engine.render(df, selected_sub, settings.use_rel)
           
    5. ADD_SPACER: Extra 300px for scroll comfort
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: MULTIDIMENSIONAL SCALING LOGIC -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Логіка багатовимірного масштабування</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль підтримує інтелектуальне масштабування. При порівнянні підстанції 330кВ та 10кВ на одному графіку, звичайна лінійна шкала зробить меншу підстанцію невидимою. Логарифмічний тогл (Log Scale) в <code>advanced.py</code> вирівнює візуальну вагу об'єктів, дозволяючи аналітику бачити спільні патерни поведінки незалежно від їхньої абсолютної потужності.</p>
    </div>
</div>

<!-- SECTION 08: INTELLIGENT ERROR HANDLING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Інтелектуальна обробка помилок</h2></div>
    <div class="glass-card flow-step">
        <p>Перед запуском важких математичних операцій, модуль проводить "швидку перевірку". Якщо даних недостатньо (наприклад, менше 24 точок для STL-декомпозиції), система видає інформативне попередження з підказкою, замість технічного повідомлення про помилку Python. Це робить інтерфейс дружнім до користувача та надійним у роботі.</p>
    </div>
</div>

<!-- SECTION 09: CUSTOM POPOVER NAVIGATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Навігація через Popovers</h2></div>
    <div class="glass-card flow-step">
        <p>Для збереження чистоти робочого простору, всі другорядні налаштування (вибір масштабу, фільтри) винесені у спливаючі панелі (Popovers). Це дозволяє графікам займати 100% ширини контентної області, що особливо важливо в новому широкоформатному режимі ATLAS, який ми впровадили для покращення читабельності.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM SCROLLING COMFORT (UX FIX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Комфорт скролінгу (UX Fix)</h2></div>
    <div class="glass-card flow-step">
        <p>У нижній частині модуля додано спеціальний технічний відступ (Spacer) висотою 300 пікселів. Це дрібна, але важлива деталь дизайну, яка дозволяє користувачеві проскролити графіки так, щоб вони не перекривалися елементами браузера або футером, забезпечуючи комфортний візуальний аналіз нижніх частин діаграм.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Clustering Engine</h4>
                <p>Низькорівневий виконавець K-Means аналізу.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📈</div>
            <div class="role-content">
                <h4>Trend Engine</h4>
                <p>Ядро математичної декомпозиції часових рядів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>Streamlit Layout</h4>
                <p>Інфраструктура для фрагментації та навігації.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (3D CLUSTERS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (3D Clusters)</h2></div>
    <div class="glass-card flow-step">
        <p>Наступним етапом є впровадження **3D-візуалізації кластерів** через PCA-проекцію. Це дозволить аналітику буквально "політати" навколо груп підстанцій у багатовимірному просторі ознак. Також планується інтеграція автоматичних текстових інсайтів (AI Insights), які будуть підсвічувати головні причини аномалій у трендах.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Поглиблений Аналіз</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чи можна експортувати результати декомпозиції?</b> — Так, графіки можна зберігати як PNG, а розраховані компоненти тренду доступні для копіювання через контекстне меню.</p>
        <p><b>Як часто оновлюються кластери?</b> — При кожній зміні глобального набору даних (Data Ingestion).</p>
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
