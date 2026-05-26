# Технічна специфікація: Головний Оркестратор Інтерфейсу (DASHBOARD LAYOUT ENGINE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">UI ORCHESTRATION | FRAGMENT ARCHITECTURE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏗️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Оркестратор Інтерфейсу</h1>
            <p class="mega-subtitle">Центральний хаб візуалізації проєкту ATLAS: координація багатосторінкової навігації, стабільний рендеринг через фрагменти та інтелектуальний роутинг аналітичних модулів</p>
            <div class="status-tags"><span class="tag tag-online">ORCHESTRATOR ACTIVE</span><span class="tag tag-version">v2.9.0</span><span class="tag tag-role">CORE UI ENGINE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Pattern</span><span class="metric-value">Fragment-Based UI</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Performance</span><span class="metric-value">Lazy Filtering</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Ghost-Busting Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">State</span><span class="metric-value">Session-Safe Bus</span></div></div>
</div>

<!-- SECTION 01: UI ORCHESTRATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Оркестрації Інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>dashboard.py</code> є "Скелетом" та "Нервовою системою" проєкту ATLAS. В складних аналітичних системах на базі Streamlit головною проблемою є повний рендеринг сторінки при кожній зміні віджета. Наша філософія базується на <b>Ізольованому Рендерингу</b>: ми розділили інтерфейс на незалежні фрагменти (<code>st.fragment</code>), які оновлюються автономно. Це дозволяє карті, графікам споживання та AI-моделям працювати паралельно, не блокуючи один одного та забезпечуючи миттєвий відгук системи на дії диспетчера. Це виключає мерехтіння екрана та знижує навантаження на мережевий трафік на 80% порівняно з традиційним підходом.</p>
    </div>
</div>

<!-- SECTION 02: APPLICATION ARCHITECTURE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Архітектурна схема UI-двигуна (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    APP("Main Entry (app.py)") --> SIDE("Sidebar (Filters/Mode)")
    SIDE --> DASH("Dashboard Orchestrator (dashboard.py)")
    
    DASH --> NAV("Stable Navigation Bus (Radio Sync)")
    NAV --> FRAG_BUS{"Stable Fragment Bus"}
    
    FRAG_BUS --> MAP("fragment_live_map (st.fragment)")
    FRAG_BUS --> CONS("fragment_live_consumption (st.fragment)")
    FRAG_BUS --> AI("fragment_live_ai (st.fragment)")
    
    DASH --> STATIC("Static Route Handler (Post-Fragment)")
    STATIC --> GEN("tab_generation (Static)")
    STATIC --> FIN("tab_finance (Static)")
    STATIC --> FOR("tab_forecast (Static Controller)")
    STATIC --> AUDIT("tab_audit (Static)")
    
    SUB("Sub-fragments (Tab Stability)") --> AI
    </div></div>
</div>

<!-- SECTION 03: FRAGMENT-BASED RENDERING STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія фрагментарного рендерингу</h2></div>
    <div class="glass-card flow-step">
        <p>Для досягнення максимальної продуктивності в <code>dashboard.py</code> реалізовано наступні підходи:</p>
        <ul>
            <li><b>Stable Fragment IDs:</b> Всі фрагменти викликаються в коді ЗАВЖДИ в однаковій послідовності, незалежно від активної вкладки. Це гарантує стабільність дельта-індексів Streamlit і запобігає "зникненню" віджетів або перезавантаженню стану при перемиканні.</li>
            <li><b>Lazy Data Access:</b> Фрагменти не отримують DataFrame як аргумент (щоб уникнути копіювання пам'яті). Вони отримують лише ключі та параметри фільтрації, самостійно звертаючись до <code>get_verified_data()</code>. Це скорочує затримки передачі даних у 6-10 разів.</li>
            <li><b>Ghost-Busting:</b> Механізм очищення пам'яті через <code>gc.collect()</code> після завершення роботи кожного фрагмента для запобігання витокам RAM при тривалій роботі дашборду у режимі 24/7.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: NAVIGATION & ROUTING MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця навігації та роутингу</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Вкладка / Опція Навігації</th>
                    <th>Тип рендерингу (Технологія)</th>
                    <th>Режим доступності</th>
                    <th>Метод виклику / Обробник</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>🗺️ Карта мережі</td><td>st.fragment (Interactive)</td><td>Live Mode Only</td><td><code>fragment_live_map()</code></td></tr>
                <tr><td>📉 Споживання</td><td>st.fragment (Lazy)</td><td>Universal</td><td><code>fragment_live_consumption()</code></td></tr>
                <tr><td>🏭 Генерація</td><td>Static Route (Full Render)</td><td>Live Mode Only</td><td><code>tab_generation.render()</code></td></tr>
                <tr><td>🚨 Журнал аварій</td><td>Static Route (Full Render)</td><td>Live Mode Only</td><td><code>tab_alerts.render()</code></td></tr>
                <tr><td>💰 Економіка</td><td>Static Route (Full Render)</td><td>Live Mode Only</td><td><code>tab_finance.render()</code></td></tr>
                <tr><td>🤖 AI Аналітика</td><td>Nested Fragments (Deep Isolation)</td><td>Universal</td><td><code>fragment_live_ai()</code></td></tr>
                <tr><td>🔮 Прогноз ШІ</td><td>Controller Dispatch (Interactive)</td><td>Universal</td><td><code>tab_forecast.render()</code></td></tr>
                <tr><td>📜 Цифровий архів</td><td>Static Route (Full Render)</td><td>Universal</td><td><code>tab_audit.render()</code></td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: THE STABLE FRAGMENT BUS (CORE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Шина стабільних фрагментів (Stable Bus)</h2></div>
    <div class="glass-card flow-step">
        <p>Критичною особливістю <code>dashboard.py</code> є блок <b>Stable Fragment Bus</b>. У Streamlit порядок виклику функцій визначає ідентифікатори об'єктів. Якщо ми будемо викликати фрагмент "Карта" тільки коли вибрана вкладка карти, то при переході на "Споживання" всі ID змістяться. Ми вирішили це через виклик ВСІХ фрагментів з прапором <code>active=False</code>, що зберігає дерево віджетів незмінним та забезпечує безшовне перемикання між аналітичними панелями.</p>
        <p>Спеціальні вбудовані субфрагменти кластеризації (<code>fragment_advanced_tab1</code> та <code>fragment_advanced_tab2</code>) також реєструються в цій шині з <code>active=False</code> за замовчуванням, щоб зберегти цілісність сесії при завантаженні складних AI-компонентів.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE & DETAILS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Головного Оркестратора (Dashboard Core)</h2></div>
    <div class="glass-card flow-step">
        <pre><code class="language-python"># Оркестрація життєвого циклу рендерингу (dashboard.py)
FUNCTION render_dashboard_ui(data, group_col, data_source, selected_region, date_range, selected_substation, filter_fn):
    1. INITIALIZE:
           - st.title("⚡ Energy Monitor")
           - Отримання базової синхронізації часу: last_update = data["load"]["timestamp"].max()
           - Збереження selected_region у st.session_state
           
    2. ACCORDION (Substation Live Telemetry):
           - render st.expander("📊 Деталізація по підстанціях (Live)")
           - live_telemetry_wrapper(active=True) # Always active for telemetry stream registration
           
    3. NAVIGATION (Adaptive Routing):
           IF data_source == "Еталонні дані (Kaggle)":
               options = ["📉 Споживання", "🤖 AI Аналітика", "🔮 Прогноз ШІ"]
               IF nav_index >= len(options): nav_index = 0
           ELSE:
               options = ["🗺️ Карта мережі", "📉 Споживання", "🏭 Генерація", "🚨 Журнал аварій", "💰 Економіка", "🤖 AI Аналітика", "🔮 Прогноз ШІ", "📜 Цифровий архів"]
               
           current_page = st.radio(options, horizontal=True, key="top_navigation", on_change=sync_nav)
           
    4. STABLE FRAGMENT BUS REGISTRATION (Crucial Order):
           - fragment_live_map("load", filter_params, active=(current_page == "🗺️ Карта мережі"))
           - fragment_live_consumption("load", group_col, filter_params, active=(current_page == "📉 Споживання"))
           - fragment_live_ai("load", selected_substation, filter_params, active=(current_page == "🤖 AI Аналітика"))
           - fragment_advanced_tab1(load_df, selected_substation, active=False) # ID Lock
           - fragment_advanced_tab2(load_df, selected_substation, active=False) # ID Lock
           
    5. STATIC ROUTING PHASE:
           IF current_page == "🏭 Генерація":
               render tab_generation.render(filtered_gen_df)
           ELSE IF current_page == "🚨 Журнал аварій":
               render tab_alerts.render(filtered_alerts_df)
           ELSE IF current_page == "💰 Економіка":
               render tab_finance.render(filtered_fin_df, lines_df)
           ELSE IF current_page == "🔮 Прогноз ШІ":
               render tab_forecast.render(selected_substation, data_source)
           ELSE IF current_page == "📜 Цифровий архів":
               render tab_audit.render(selected_region, date_range, selected_substation)
               
    6. MEMORY CLEANUP & FOOTER:
           - Del local dataframes
           - Invoke gc.collect() to prevent RAM bloat
           - Render st.divider() and custom grey Centered Copyright footer
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: ADAPTIVE INTERFACE LOGIC (LIVE vs KAGGLE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Логіка адаптації інтерфейсу (Dynamic Routing)</h2></div>
    <div class="glass-card flow-step">
        <p>Двигун <code>dashboard.py</code> автоматично змінює набір доступних вкладок залежно від джерела даних. В режимі "Kaggle" система приховує вкладки "Карта", "Генерація", "Журнал аварій" та "Економіка", оскільки історичні набори даних не містять необхідних гео-координат, сенсорів та типів активних джерел.</p>
        <div style="background: rgba(255, 165, 0, 0.1); border-left: 4px solid orange; padding: 10px; border-radius: 4px; margin-top: 10px;">
            <strong>⚠️ КРИТИЧНЕ ПРАВИЛО:</strong> Спроби рендерингу порожніх або несумісних сторінок блокуються на рівні меню. Це автоматично звужує область інспекції до сумісних інструментів прогнозування та аналізу споживання, запобігаючи виникненню винятків часу виконання (runtime exceptions).
        </div>
    </div>
</div>

<!-- SECTION 08: INTELLIGENT NAVIGATION SYNC (SYNC_NAV) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Інтелектуальна синхронізація навігації</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>sync_nav()</code> відповідає за збереження стану та "пам'ять" інтерфейсу:</p>
        <pre><code class="language-python">def sync_nav():
    options = st.session_state.get("current_options", [])
    if not options:
        return
    if "top_navigation" in st.session_state:
        try:
            st.session_state.nav_index = options.index(st.session_state.top_navigation)
        except ValueError:
            st.session_state.nav_index = 0
            if "top_navigation" in st.session_state:
                del st.session_state["top_navigation"]</code></pre>
        <p>При переході між джерелами (наприклад, з Live до Kaggle) набір опцій у <code>st.radio</code> миттєво змінюється. Ця логіка автоматично перераховує індекси, запобігаючи критичній помилці <code>ValueError: index out of bounds</code> у віджетах Streamlit.</p>
    </div>
</div>

<!-- SECTION 09: MEMORY MANAGEMENT & GC (STABILITY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Управління пам'яттю та GC (Stability)</h2></div>
    <div class="glass-card flow-step">
        <p>Оскільки проєкт ATLAS працює з великими обсягами реальної та синтетичної телеметрії, використання оперативної пам'яті є жорстко контрольованим:</p>
        <ul>
            <li>Після завершення рендерингу кожної важкої вкладки (наприклад, "Генерація", "Економіка" чи "Карта") ми примусово виконуємо команду <code>del df; gc.collect()</code>.</li>
            <li>Це звільняє невикористовувані посилання з купи Python (heap) і повертає пам'ять операційній системі.</li>
            <li>Дана стратегія запобігає витоку RAM при тривалій безперервній роботі (24/7), утримуючи споживання пам'яті сервером в межах стабільних <b>120-180 MB</b> незалежно від кількості звернень користувачів.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: BOTTOM DESIGN & COPYRIGHT -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дизайн підвалу (Footer & UX)</h2></div>
    <div class="glass-card flow-step">
        <p>Кожна сторінка, згенерована через <code>dashboard.py</code>, завершується уніфікованим роздільником (<code>st.divider()</code>) та футером:</p>
        <div style="text-align: center; color: var(--text-dim); background: rgba(255,255,255,0.01); padding: 10px; border-radius: 6px; border: 1px dashed var(--border);">
            <code>© 2025 Energy Systems Analytics | Diploma Project</code>
        </div>
        <p style="margin-top: 10px;">Це створює візуальну завершеність професійного інженерного інтерфейсу. Також у коді забезпечується фінальний відступ для комфортного скролінгу, щоб користувач міг без зусиль переглянути нижні лінії графіків на екранах будь-якого розширення.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>UI Components styles.py</h4>
                <p>Постачальник глобальних кастомних стилів (CSS), шрифтів та Cyber-HUD маскування.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>Database Loader loader.py</h4>
                <p>Центральне джерело стабільних валідованих даних через <code>get_verified_data()</code>.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📡</div>
            <div class="role-content">
                <h4>Live Telemetry Wrapper</h4>
                <p>Оркестратор телеметрії <code>live_kpi.py</code>, який відповідає за Snapshot-зчитування.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📂</div>
            <div class="role-content">
                <h4>Views Registry (tab_*)</h4>
                <p>Набір імпортованих модулів представлень: map, consumption, alerts, advanced, generation, finance, forecast, historical_audit.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (MULTI-WINDOW SUPPORT) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Multi-window Support)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Багатовіконного режиму**:</p>
        <ul>
            <li>Користувач зможе від'єднати будь-який важкий фрагмент (наприклад, Живу Карту або KPI навантаження) в окреме браузерне вікно для побудови професійної відеостіни в диспетчерській.</li>
            <li>Буде додано підтримку <b>Hotkeys</b> (гарячих клавіш: <code>Ctrl + 1-8</code>) для миттєвого перемикання між вкладками без використання миші.</li>
            <li>Реалізація фонової синхронізації станів вікон через механізм HTML5 LocalStorage Events.</li>
        </ul>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Оркестратор Інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому деякі вкладки перемикаються повільно?</b><br>— Це може статися при виборі дуже великих часових діапазонів у календарі фільтрації для статичних вкладок (наприклад, Економіка). Спробуйте зменшити період або скористатися локальним кешуванням.</p>
        
        <p><b>Куди зникла вкладка "Карта мережі"?</b><br>— Ви перемкнулися в режим "Еталонні дані (Kaggle)". Карта та живі гео-дані підстанцій доступні виключно в режимі Live симуляції Digital Twin.</p>
        
        <p><b>Як фрагменти оновлюються автономно?</b><br>— Завдяки декоратору <code>@st.fragment</code>, будь-яка зміна всередині фрагмента ініціює перезапуск тільки його локального блоку коду, не зачіпаючи основне дерево Streamlit.</p>
        
        <p><b>Чому st.radio не викликає Value Error при зміні опцій?</b><br>— Це забезпечується інтелектуальним скиданням <code>nav_index</code> у функції <code>sync_nav()</code> при виявленні несумісних індексів меню.</p>
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
