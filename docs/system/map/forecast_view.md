# Технічна специфікація: Центр Прогнозування та Аудиту ШІ (AI FORECAST & AUDIT VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AI INFERENCE CENTER | PREDICTIVE AUDIT</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚡</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Центр Прогнозування</h1>
            <p class="mega-subtitle">Головний інтерфейс взаємодії з ШІ-моделями: реактивна генерація прогнозів навантаження, покроковий аудит точності та порівняльний аналіз архітектур нейромереж</p>
            <div class="status-tags"><span class="tag tag-online">FORECASTER ACTIVE</span><span class="tag tag-version">v2.8.0</span><span class="tag tag-role">CHIEF DISPATCHER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">Engine</span><span class="metric-value">Reactive Multi-Inference</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Audit</span><span class="metric-value">Cross-Architectural</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Safety</span><span class="metric-value">Interruption Monitor</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Context</span><span class="metric-value">Live / Simulation</span></div></div>
</div>

<!-- SECTION 01: FORECAST CENTER PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Центру Прогнозування</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>forecast.py</code> є "Командним містком" проекту ATLAS. Тут зосереджена вся потужність ШІ-аналітики. Наша філософія базується на <b>Реактивності та Прозорості</b>: користувач повинен не просто отримувати прогноз, а розуміти, яка модель (V1, V2 чи V3) є найбільш адекватною для поточної ситуації. Система дозволяє "на льоту" змінювати сценарії (What-if) та миттєво бачити результат на інтерактивних графіках Plotly, забезпечуючи найвищий рівень підтримки прийняття рішень.</p>
    </div>
</div>

<!-- SECTION 02: FORECAST & AUDIT WORKFLOW -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Робочий процес прогнозування (Workflow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    USER("User Selection (Substation/Model)") --> HEAD("Forecast Header (Config)")
    HEAD --> ACTION{Action Selected?}
    
    ACTION -- "⚡ Forecast" --> ENGINE("Reactive Inference Engine")
    ENGINE --> CACHE("Orchestrator Cache Check")
    CACHE --> VIS("Plotly Result Rendering")
    
    ACTION -- "📊 Audit" --> BACK("Backtest Execution Loop")
    BACK --> COMP("Comparative Metrics Matrix")
    COMP --> REPORT("Academic Accuracy Report")
    
    VIS --> STATE("Session State Sync")
    REPORT --> STATE
    </div></div>
</div>

<!-- SECTION 03: REACTIVE INFERENCE ENGINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Реактивний інференс-двигун</h2></div>
    <div class="glass-card flow-step">
        <p>Серцем модуля є функція <code>run_reactive_forecast_engine</code>, яка забезпечує:</p>
        <ul>
            <li><b>Asynchronous State Monitoring:</b> Відстеження переривань з боку користувача (Interruption Monitor) для економії ресурсів сервера.</li>
            <li><b>Multi-Model Dispatching:</b> Одночасний запуск декількох версій ШІ для порівняння їхньої поведінки в ідентичних умовах.</li>
            <li><b>Dynamic Simulation Injection:</b> Застосування користувацьких сценаріїв (зміна температури, стану здоров'я обладнання) безпосередньо перед розрахунком.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: COMPARATIVE AUDIT MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця порівняльного аудиту</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Режим аудиту</th>
                    <th>Опис</th>
                    <th>Користь для диспетчера</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Single Model</td><td>Детальний аналіз однієї обраної версії ШІ</td><td>Глибоке вивчення конкретного прогнозу</td></tr>
                <tr><td>Cross-Architecture</td><td>Порівняння V1, V2 та V3 на одному графіку</td><td>Вибір найбільш стабільної моделі зараз</td></tr>
                <tr><td>Global Audit</td><td>Масовий бектест всієї мережі підстанцій</td><td>Оцінка загального стану системи за добу</td></tr>
                <tr><td>Historical Deep-Dive</td><td>Покрокова звірка з фактом за минулий тиждень</td><td>Верифікація точності перед звітуванням</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: INTERRUPT-SAFE EXECUTION (STABILITY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Стабільність через Interruption Monitor</h2></div>
    <div class="glass-card flow-step">
        <p>Для запобігання конфліктам при швидкому перемиканні користувачем налаштувань, модуль реалізує <b>Interruption Monitor</b>. Якщо користувач натискає іншу кнопку під час виконання важкого розрахунку, система детектує це через <code>session_state</code>, коректно зупиняє попередній потік і видає інформативне повідомлення (Toast), зберігаючи цілісність даних та пам'яті.</p>
    </div>
</div>

<!-- SECTION 06: CORE VIEW LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Логіки Відображення (View Core)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_forecast_tab(substation, source):
    1. INIT_HEADER: (ver, scen, multi, src) = render_header(substation)
    
    2. HANDLE_ACTIONS:
       IF btn_forecast_clicked:
           st.session_state.mode = "forecast"
           CLEAR_OLD_RESULTS()
           
       IF btn_backtest_clicked:
           st.session_state.mode = "audit"
           
    3. DISPATCH_ENGINE:
       IF mode == "forecast":
           results = run_reactive_engine(substation, ver, scen)
           render_charts(results)
           
       IF mode == "audit":
           IF multi_model:
               _render_comparative_audit(substation)
           ELSE:
               render_backtest_loop(substation, ver)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: GLOBAL NETWORK AUDIT MODE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Глобальний аудит мережі (Global Audit)</h2></div>
    <div class="glass-card flow-step">
        <p>При виборі опції "Усі підстанції", модуль переходить у режим **Масового аудиту**. Система автоматично ітерує через усі доступні об'єкти, запускаючи для кожного швидкий бектест (Fast Backtest). Результати агрегуються у вигляді інтерактивної таблиці з кольоровим кодуванням: підстанції з високою похибкою підсвічуються червоним, що дозволяє диспетчеру миттєво виявити проблемні ділянки мережі.</p>
    </div>
</div>

<!-- SECTION 08: INTERACTIVE PLOTLY RENDERING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Інтерактивний рендеринг Plotly</h2></div>
    <div class="glass-card flow-step">
        <p>Всі графіки прогнозів базуються на <b>Plotly JSON</b>. Це забезпечує повноцінну інтерактивність: можливість зумування окремих годин, динамічне приховування ліній моделей через легенду та перегляд точних значень при наведенні курсору. Завдяки хелперу <code>safe_plotly_render</code>, графіки коректно відображаються навіть при нестабільному з'єднанні з сервером.</p>
    </div>
</div>

<!-- SECTION 09: SESSION STATE SYNC & PERSISTENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Синхронізація та збереження стану</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>forecast.py</code> активно використовує <code>st.session_state</code> для збереження результатів розрахунків. Це дозволяє користувачеві перемикатися між іншими вкладками (наприклад, "Monitoring" або "Map") і повертатися назад, не втрачаючи вже згенерований прогноз або результати аудиту. Це критично для багатозадачної роботи аналітика.</p>
    </div>
</div>

<!-- SECTION 10: ACADEMIC BACKTEST REPORTING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Академічна звітність бектестів</h2></div>
    <div class="glass-card flow-step">
        <p>У режимі аудиту система генерує детальний звіт по кожній моделі. Окрім візуальних ліній, користувач отримує таблицю з MAE, RMSE та R² Score. Ці дані автоматично готуються для експорту в академічні звіти, дозволяючи миттєво отримати верифіковану статистику точності ШІ для наукових публікацій або тезису.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🧠</div>
            <div class="role-content">
                <h4>Forecast Controller</h4>
                <p>Головний диспетчер ML-інференсу та кешування.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>UI Components</h4>
                <p>Набір віджетів для побудови сіток та графіків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>Historical Data</h4>
                <p>Джерело еталонних значень для верифікації (Ground Truth).</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (AUTONOMOUS AUDIT) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Autonomous Audit)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступній версії планується впровадження <b>Автономного аудиту</b>. Система буде самостійно проводити фоновий бектест всіх нових моделей після навчання і автоматично підсвічувати найкращу архітектуру для кожної підстанції. Також буде додано підтримку <b>PDF-експорту</b> повних технічних паспортів прогнозів.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Робота Центру Прогнозування</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому кнопка "Прогноз" іноді не активна?</b> — Це може статися під час активної синхронізації бази даних. Зачекайте кілька секунд.</p>
        <p><b>Як порівняти V2 та V3?</b> — Увімкніть опцію "Порівняльний аудит архітектур" у заголовку вкладки.</p>
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
