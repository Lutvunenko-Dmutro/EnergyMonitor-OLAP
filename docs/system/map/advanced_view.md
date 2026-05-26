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
        <p>Модуль <code>advanced.py</code> є дослідницьким центром проєкту ATLAS. Його мета — надати диспетчеру та аналітику інструменти для відповіді на питання "Чому це відбувається?". Ми використовуємо методи навчання без учителя (Unsupervised Learning) для групування схожих об'єктів та складну математичну декомпозицію сигналу на тренди та сезонність. Наша філософія базується на <b>Ізоляції Обчислень</b>: кожна важка аналітична вкладка працює у власному фрагменті Streamlit, не заважаючи іншим частинам інтерфейсу та забезпечуючи плавний відгук інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 02: ANALYTICS DISPATCHER DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Диспетчеризація Аналітики (Architecture)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    MAIN("Main Dashboard UI") --> VIEW_DISP("render_advanced_analysis(df, selected_substation)")
    
    VIEW_DISP --> VALIDATION{"Validation: Are cols name, load, ts present?"}
    VALIDATION -- "No" --> ERR_BANNER("Show error: missing columns")
    VALIDATION -- "Yes" --> TAB_BUILD("Create st.tabs: Clustering & Trends")
    
    TAB_BUILD --> TAB_1("Tab 1: Clustering & Segmentation")
    TAB_BUILD --> TAB_2("Tab 2: Trend Analysis")
    
    TAB_1 --> FRAG_1("fragment_advanced_tab1(df, sub, active=True)")
    FRAG_1 --> POP_1("popover: settings")
    POP_1 --> TOGG_LOG("Toggle logarithmic scale: adv_use_log")
    TOGG_LOG --> CLUST_ENGINE("render_clustering_segment(df, use_log, sub)")
    CLUST_ENGINE --> VIS_1("K-Means profiles & dynamic centroids")
    
    TAB_2 --> FRAG_2("fragment_advanced_tab2(df, sub, active=True)")
    FRAG_2 --> POP_2("popover: settings")
    POP_2 --> TOGG_REL("Toggle relative load (%): adv_use_rel")
    TOGG_REL --> TREND_ENGINE("render_trend_decomposition(df, sub, use_rel)")
    TREND_ENGINE --> VIS_2("STL Decomposition (Trend, Seasonal, Residue plots)")
    
    VIS_1 --> SPACER("st.markdown(height=300px spacer)")
    VIS_2 --> SPACER
    </div></div>
</div>

<!-- SECTION 03: CLUSTERING & SEGMENTATION STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія кластеризації та сегментації</h2></div>
    <div class="glass-card flow-step">
        <p>Для розуміння структури споживання ми впровадили автоматичну сегментацію:</p>
        <ul>
            <li><b>K-Means Integration:</b> Виявлення типових профілів навантаження (промисловий, житловий, змішаний). Це дозволяє виділити підстанції з аналогічним стилем споживання.</li>
            <li><b>Dynamic Centroids:</b> Візуалізація "ідеальної середньої" поведінки для кожного кластера, що є еталоном для порівняння.</li>
            <li><b>Substation Mapping:</b> Прив'язка обраної підстанції до її кластерного оточення для порівняльного аналізу та прогнозування резервів потужності.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: ANALYTICAL TOOLS MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця аналітичних інструментів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль надає оператору наступні високоефективні математичні важелі:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Інструмент / Опція</th>
                    <th>Опис технології</th>
                    <th>Математична основа</th>
                    <th>Бізнес-цінність</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>🪵 Log Scale</td><td>Перехід до логарифмічного масштабу</td><td>$$x'_{t} = \log_{10}(x_{t} + 1)$$</td><td>Спільний аналіз об'єктів з різницею в масштабах споживання у 100+ разів</td></tr>
                <tr><td>📈 Relative View</td><td>Відображення у % від номіналу</td><td>$$x'_{t} = \frac{x_{t}}{P_{nominal}} \times 100$$</td><td>Порівняння профілів навантаження великих промислових вузлів та малих житлових ліній</td></tr>
                <tr><td>STL Decomposition</td><td>Розклад на Trend, Seasonality, Residue</td><td>$$Y(t) = T(t) + S(t) + E(t)$$</td><td>Відокремлення базового тренду споживання від добових коливань та випадкового шуму (аномалій)</td></tr>
                <tr><td>Fragment Cache</td><td>Ізольований рендеринг Streamlit</td><td><code>@st.fragment</code> state mapping</td><td>Збереження налаштувань та графіків при перемиканні вкладок без глобального перезавантаження сторінки</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: FRAGMENT-BASED STABILITY (UX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Стабільність через фрагменти (UX)</h2></div>
    <div class="glass-card flow-step">
        <p>Аналіз великих обсягів даних та проведення кластеризації K-Means "на льоту" може викликати затримки рендерингу. Завдяки декоратору <code>@st.fragment</code>, зміна будь-яких налаштувань (наприклад, перемикання на логарифмічну шкалу в поповері) оновлює виключно графік у межах поточної вкладки.</p>
        <p>Це запобігає повному перезавантаженню дашборду Streamlit та зчитуванню даних з бази, зберігаючи фокус аналітика та забезпечуючи <b>відгук інтерфейсу &lt; 100 мс</b>.</p>
    </div>
</div>

<!-- SECTION 06: CORE DISPATCHER LOGIC (PSEUDO-CODE & DETAILS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Диспетчера (Dispatcher Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code class="language-python"># Оркестрація та диспетчеризація AI-аналітики (advanced.py)
FUNCTION fragment_advanced_tab1(df, selected_substation, active):
    1. EXIT IF NOT ACTIVE:
           IF not active: RETURN
           
    2. RENDER SETTINGS POPOVER:
           col_space, col_tools = st.columns([4, 1])
           WITH col_tools.popover("⚙️ Налаштування"):
               use_log = st.toggle("🪵 Логарифмічна шкала", value=False, key="adv_use_log")
               
    3. CALL CLUSTERING COMPONENT:
           render_clustering_segment(df, use_log, selected_substation)
END FUNCTION

FUNCTION fragment_advanced_tab2(df, selected_substation, active):
    1. EXIT IF NOT ACTIVE:
           IF not active: RETURN
           
    2. RENDER SETTINGS POPOVER:
           col_space, col_tools = st.columns([4, 1])
           WITH col_tools.popover("⚙️ Налаштування"):
               use_rel = st.toggle("📈 Відносне навантаження (%)", value=False, key="adv_use_rel")
               
    3. CALL TREND DECOMPOSITION COMPONENT:
           render_trend_decomposition(df, selected_substation, use_rel)
END FUNCTION

FUNCTION render_advanced_analysis(df, selected_substation):
    1. TITLE & VALIDATIONS:
           st.title("🧩 Поглиблена аналітика (AI & Trends)")
           
           IF NOT columns ["substation_name", "actual_load_mw", "timestamp"] in df.columns:
               st.error("У даних відсутні необхідні колонки.")
               RETURN
               
           IF df.empty:
               st.warning("Недостатньо даних для аналізу.")
               RETURN
               
    2. RENDER TABS (Streamlit Native UI):
           tab1, tab2 = st.tabs(["📊 Кластеризація (Сегментація)", "📈 &Acy;наліз трендів"])
           
    3. TAB BINDINGS WITH EXPLICIT ACTIVE FLAGS (Perfect ID lock):
           WITH tab1:
               fragment_advanced_tab1(df, selected_substation, active=True)
           WITH tab2:
               fragment_advanced_tab2(df, selected_substation, active=True)
               
    4. SPACER UX FIX:
           st.markdown("<div style='height: 300px;'></div>")
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: MULTIDIMENSIONAL SCALING LOGIC -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Логіка багатовимірного масштабування</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль підтримує інтелектуальне масштабування. При порівнянні на одному графіку великої підстанції класу 330 кВ та малого розподільчого пункту 10 кВ звичайна лінійна шкала зробить менший об'єкт невидимою рівною лінією. Логарифмічний перемикач (Log Scale) в <code>advanced.py</code> вирівнює візуальну вагу об'єктів, дозволяючи аналітику бачити спільні добові патерни споживання незалежно від їхньої абсолютної потужності.</p>
    </div>
</div>

<!-- SECTION 08: INTELLIGENT ERROR HANDLING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Інтелектуальна обробка помилок</h2></div>
    <div class="glass-card flow-step">
        <p>Перед запуском важких математичних операцій, модуль проводить "швидку перевірку" цілісності даних:</p>
        <ul>
            <li>Перевіряється наявність усіх необхідних колонок (<code>substation_name</code>, <code>actual_load_mw</code>, <code>timestamp</code>) перед рендерингом.</li>
            <li>Якщо даних недостатньо для проведення STL-декомпозиції (наприклад, менше 24 точок для побудови повного добового профілю з погодинною дискретизацією), система виводить дружнє попередження, убезпечуючи сервер від аварійного виходу з винятком <code>ValueError</code>.</li>
        </ul>
    </div>
</div>

<!-- SECTION 09: CUSTOM POPOVER NAVIGATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Навігація через Popovers</h2></div>
    <div class="glass-card flow-step">
        <p>Для збереження чистоти робочого простору, всі другорядні налаштування (вибір масштабу, фільтри) винесені у спливаючі панелі (Popovers) <code>st.popover</code>. Це дозволяє аналітичним графікам Plotly займати 100% ширини контентної області, що особливо важливо в новому широкоформатному Cyber-HUD режимі ATLAS, який ми впровадили для покращення читабельності.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM SCROLLING COMFORT (UX FIX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Комфорт скролінгу (UX Spacer)</h2></div>
    <div class="glass-card flow-step">
        <p>У нижній частині модуля додано спеціальний технічний відступ (Spacer) висотою 300 пікселів:</p>
        <div style="background: rgba(255,255,255,0.01); border: 1px dashed var(--border); padding: 8px; border-radius: 4px; font-family: monospace; font-size: 12px; text-align: center; color: var(--text-dim);">
            &lt;div style="height: 300px;"&gt;&lt;/div&gt;
        </div>
        <p style="margin-top: 10px;">Це дрібна, але вкрай важлива деталь UX дизайну, яка дозволяє користувачеві проскролити графіки так, щоб вони не перекривалися елементами браузера або футером, забезпечуючи комфортний візуальний аналіз нижніх ліній трендів.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>clustering_view.py</h4>
                <p>Низькорівневий виконавець K-Means аналізу, розрахунку силуетних коефіцієнтів та рендерингу центроїдів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📈</div>
            <div class="role-content">
                <h4>trend_view.py</h4>
                <p>Ядро математичної декомпозиції часових рядів (STL) та візуалізатор сезонних трендів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>Streamlit Layout</h4>
                <p>Базовий інструментарій для організації native tabs (st.tabs) та popover меню.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (3D CLUSTERS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (3D Clusters)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **3D-візуалізації кластерів** через PCA-проекцію (Principal Component Analysis):</p>
        <ul>
            <li>Користувач зможе буквально "літати" навколо тривимірної хмари точок підстанцій у багатовимірному просторі ознак за допомогою Plotly 3D scatter plots.</li>
            <li>Автоматичне додавання текстових інсайтів (AI Insights), які будуть підсвічувати аномальні викиди у залишковій складовій STL-декомпозиції та автоматично пропонувати причини аномалії.</li>
        </ul>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Поглиблений Аналіз</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чи можна експортувати результати декомпозиції часових рядів?</b><br>— Так, будь-який сформований графік Plotly містить вбудовану панель інструментів (Camera icon) для миттєвого збереження у форматі PNG, а самі точки декомпозиції доступні для аналізу.</p>
        
        <p><b>Скільки точок даних потрібно для коректного аналізу трендів?</b><br>— Для STL-декомпозиції добового циклу з погодинною дискретизацією потрібно щонайменше 24 послідовні вимірювання (краще 48-72 години для точного визначення сезонності).</p>
        
        <p><b>Як часто перераховуються кластери K-Means?</b><br>— Кластеризація запускається автоматично при кожному тику оновлення глобального DataFrame, який передається з оркестратора, або при перемиканні логарифмічного масштабу.</p>
        
        <p><b>Чому налаштування винесені в st.popover, а не st.sidebar?</b><br>— Ми зробили це для збереження контексту роботи. Налаштування кластеризації мають стосуватися тільки цієї вкладки, не засмічуючи глобальний сайдбар з гео-фільтрами.</p>
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
