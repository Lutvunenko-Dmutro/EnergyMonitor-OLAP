# Технічна специфікація: Розширений Інструментарій Допоміжних Сервісів (EXTENDED UTILS TOOLKIT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM UTILITIES | HELPERS & HANDLERS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛠️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Інструментарій Системи</h1>
            <p class="mega-subtitle">Централізована бібліотека допоміжних сервісів ATLAS: від інтелектуального управління кешем та пам'яттю до прецизійного логування та обробки виняткових ситуацій</p>
            <div class="status-tags"><span class="tag tag-online">UTILS ACTIVE</span><span class="tag tag-version">v2.6.0</span><span class="tag tag-role">SUPPORT ENGINE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Cache</span><span class="metric-value">Smart TTL Cleanup</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Memory</span><span class="metric-value">Auto-GC Sentinel</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📝</div><div class="metric-info"><span class="metric-label">Logging</span><span class="metric-value">Structured Event Stream</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚑</div><div class="metric-info"><span class="metric-label">Errors</span><span class="metric-value">Graceful Failover Layer</span></div></div>
</div>

<!-- SECTION 01: THE ROLE OF UTILITIES IN SYSTEM ARCHITECTURE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Роль Утиліт в Архітектурі Системи</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/utils/</code> є "Швейцарським ножем" проекту ATLAS. Хоча ці модулі не містять прямої бізнес-логіки енергомоніторингу, вони забезпечують <b>Технічну Спроможність</b> всієї системи. Тут зосереджені інструменти, які роблять ATLAS швидким, стабільним та легким у налагодженні. Ми розглядаємо утиліти як "клей", що з'єднує складні аналітичні модулі в єдиний, надійно працюючий організм.</p>
    </div>
</div>

<!-- SECTION 02: UTILITIES MODULES MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Матриця Модулів Утиліт</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль</th>
                    <th>Призначення</th>
                    <th>Ключова Функція</th>
                    <th>Ефект</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>cache_manager.py</code></td><td>Оптимізація доступу</td><td>TTL Validation</td><td>Швидкий старт</td></tr>
                <tr><td><code>memory_helper.py</code></td><td>Контроль ресурсів</td><td>auto_gc()</td><td>Захист від OOM</td></tr>
                <tr><td><code>logging_config.py</code></td><td>Трасування подій</td><td>setup_logging()</td><td>Повна аудит-готовність</td></tr>
                <tr><td><code>error_handlers.py</code></td><td>Стійкість до збоїв</td><td>safe_execution</td><td>Безперервна робота</td></tr>
                <tr><td><code>ui_helpers.py</code></td><td>UX Покращення</td><td>Plotly Wrappers</td><td>Плавна візуалізація</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: SMART CACHE MANAGEMENT STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Розумного Управління Кешем</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>cache_manager.py</code> реалізовано алгоритм <b>Pre-emptive Cleanup</b>. Система не просто накопичує тимчасові файли, вона аналізує їх вік та актуальність. При кожному запуску ATLAS перевіряє TTL (Time-To-Live) кешованих даних. Це гарантує, що користувач завжди бачить свіжу аналітику, а дисковий простір сервера використовується максимально раціонально.</p>
    </div>
</div>

<!-- SECTION 04: UTILS INTERACTION DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема Взаємодії Утиліт</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    APP_START("Application Start") --> CACHE("cache_manager: TTL Audit")
    CACHE --> LOG("logging_config: Init Stream")
    LOG --> MONITOR("memory_helper: Set Watchdog")
    
    subgraph RUNTIME_SUPPORT["Runtime Execution Support"]
        ERR("error_handlers: Catch & Log")
        UI_H("ui_helpers: Optimize Render")
        HELP("helpers: Logic Shorthands")
    end
    
    MONITOR --> RUNTIME_SUPPORT
    RUNTIME_SUPPORT --> SYSTEM_EXIT("Safe Exit & Cleanup")
    </div></div>
</div>

<!-- SECTION 05: MEMORY SENTINEL & GARBAGE COLLECTION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Вартовий Пам'яті та Збір Сміття</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>memory_helper.py</code> містить систему **Watchdog Sentinel**. Вона постійно моніторить споживання RAM процесом Streamlit. При наближенні до критичної межі (напр. 380-450 МБ), утиліта примусово ініціює глибокий збір сміття (Garbage Collection). Це дозволяє ATLAS працювати тижнями без перезавантаження, що є критичним для систем ситуаційного моніторингу.</p>
    </div>
</div>

<!-- SECTION 06: STRUCTURED LOGGING & AUDIT TRAIL -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Структуроване Логування та Аудит</h2></div>
    <div class="glass-card flow-step">
        <p>За допомогою <code>logging_config.py</code> ми створюємо детальний <b>Audit Trail</b> всіх подій у системі. Логи розбиті за рівнями критичності (INFO, WARNING, ERROR) та збагачені контекстом (ID сесії, час виконання запиту). Це робить процес пошуку та усунення помилок (Troubleshooting) максимально швидким та прозорим для розробника.</p>
    </div>
</div>

<!-- SECTION 07: GRACEFUL ERROR HANDLING LAYER -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Шар М'якої Обробки Помилок</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>error_handlers.py</code> забезпечує принцип <b>Fail-Safe Rendering</b>. Якщо один аналітичний віджет виходить з ладу через некоректні дані, він не "обвалює" весь інтерфейс. Утиліта перехоплює виключення, логує його та відображає користувачеві безпечне повідомлення, зберігаючи працездатність решти системи.</p>
    </div>
</div>

<!-- SECTION 08: UI RENDER OPTIMIZATION HELPERS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Допоміжні Засоби Оптимізації UI</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>ui_helpers.py</code> зосереджені функції для прискорення рендерингу важких Plotly-графіків. Ми використовуємо паттерни багаторазового використання об'єктів та оптимізовані обгортки (Wrappers), які автоматично налаштовують темну тему та приховують зайві елементи керування, забезпечуючи "чистий" та імерсивний UX у стилі Cyber-HUD.</p>
    </div>
</div>

<!-- SECTION 09: CORE HELPERS & LOGIC SHORTHANDS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Базові Хелпери та Логічні Скорочення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>helpers.py</code> містить набір невеликих, але критичних функцій: форматування одиниць виміру (МВт, кВ), розрахунок часових зміщень та перетворення форматів даних. Централізація цих операцій запобігає дублюванню коду (DRY) та гарантує, що в усьому додатку дані відображаються в єдиному стандарті.</p>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v3.0 (PREDICTIVE UTILS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v3.0 (Predictive Utils)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Предиктивного Управління Ресурсами**, яке буде аналізувати патерни використання RAM та заздалегідь готувати кеш для найпопулярніших запитів користувачів. Також буде додано модуль <i>Health Dashboard</i> для самих утиліт та впроваджено автоматичну відправку критичних логів у Telegram-бот адміністратора через інтегровані вебхуки.</p>
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
