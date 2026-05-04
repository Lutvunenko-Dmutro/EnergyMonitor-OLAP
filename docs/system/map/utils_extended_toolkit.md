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
        <p>Пакет <code>src/utils/</code> є "Швейцарським ножем" проекту ATLAS. Хоча ці модулі не містять прямої бізнес-логіки енергомоніторингу, вони забезпечують <b>Технічну Спроможність</b> всієї системи. Тут зосереджені інструменти, які роблять ATLAS швидким, стабільним та легким у налагодженні. Ми розглядаємо утиліти як "клей", що з'єднує складні аналітичні модулі в єдиний, надійно працюючий організм. Кожен інструмент спроектований з акцентом на продуктивність та мінімальне споживання ресурсів.</p>
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
                    <th>Вплив</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>cache_manager.py</code></td><td>Оптимізація доступу</td><td>TTL Validation / Clean</td><td>Швидкий старт системи</td></tr>
                <tr><td><code>memory_helper.py</code></td><td>Контроль ресурсів</td><td>auto_gc() / monitor</td><td>Захист від OOM Crash</td></tr>
                <tr><td><code>logging_config.py</code></td><td>Трасування подій</td><td>setup_structured_logs</td><td>Повна аудит-готовність</td></tr>
                <tr><td><code>error_handlers.py</code></td><td>Стійкість до збоїв</td><td>safe_execution_wrapper</td><td>Безперервна робота UI</td></tr>
                <tr><td><code>ui_helpers.py</code></td><td>UX Покращення</td><td>Plotly Theme Injector</td><td>Плавна візуалізація</td></tr>
                <tr><td><code>validators.py</code></td><td>Контроль типів</td><td>Deep Object Validation</td><td>Цілісність даних</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: SMART CACHE MANAGEMENT STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Розумного Управління Кешем</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>cache_manager.py</code> реалізовано алгоритм <b>Pre-emptive Cleanup</b>. Система не просто накопичує тимчасові файли, вона аналізує їх вік та актуальність. При кожному запуску ATLAS перевіряє TTL (Time-To-Live) кешованих даних. Це гарантує, що користувач завжди бачить свіжу аналітику, а дисковий простір сервера використовується максимально раціонально. Алгоритм також враховує пріоритетність даних: критичні метадані зберігаються довше, ніж результати проміжних розрахунків.</p>
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

<!-- SECTION 05: SEQUENCE: CACHE CLEANUP PROCESS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Sequence: Процес очищення кешу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
sequenceDiagram
    participant Sys as ATLAS Core
    participant Ca as CacheManager
    participant FS as File System
    
    Sys->>Ca: Trigger Maintenance
    Ca->>FS: Scan Cache Directory
    FS-->>Ca: List of Files (Timestamped)
    Ca->>Ca: Filter Expired (TTL > 24h)
    Ca->>FS: Delete Expired Files
    Ca-->>Sys: Cleanup Summary (MB Freed)
    </div></div>
</div>

<!-- SECTION 06: MEMORY SENTINEL & GARBAGE COLLECTION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Вартовий Пам'яті та Збір Сміття</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>memory_helper.py</code> містить систему **Watchdog Sentinel**. Вона постійно моніторить споживання RAM процесом. При наближенні до критичної межі (напр. 450 МБ), утиліта примусово ініціює глибокий збір сміття (Garbage Collection) через <code>gc.collect()</code>. Це дозволяє ATLAS працювати тижнями без перезавантаження, що є критичним для систем ситуаційного моніторингу в промислових умовах.</p>
    </div>
</div>

<!-- SECTION 07: STRUCTURED LOGGING & AUDIT TRAIL -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Структуроване Логування та Аудит</h2></div>
    <div class="glass-card flow-step">
        <p>За допомогою <code>logging_config.py</code> ми створюємо детальний <b>Audit Trail</b> всіх подій у системі. Логи розбиті за рівнями критичності (INFO, WARNING, ERROR) та збагачені контекстом. Це робить процес пошуку та усунення помилок (Troubleshooting) максимально швидким та прозорим. Кожен запис містить мітку часу з мікросекундною точністю для синхронізації з подіями в енергомережі.</p>
    </div>
</div>

<!-- SECTION 08: GRACEFUL ERROR HANDLING LAYER -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Шар М'якої Обробки Помилок</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>error_handlers.py</code> забезпечує принцип <b>Fail-Safe Rendering</b>. Якщо один аналітичний віджет виходить з ладу через некоректні дані, він не "обвалює" весь інтерфейс. Утиліта перехоплює виключення, логує його та відображає користувачеві безпечне повідомлення або пустий стан, зберігаючи працездатність решти системи. Це критично для забезпечення неперервності спостереження за мережею.</p>
    </div>
</div>

<!-- SECTION 09: TECHNICAL FAQ: UTILS TOOLKIT -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Технічний FAQ Утиліт</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Як змінити поріг спрацювання Watchdog пам'яті?</b><br>
        A: Параметр <code>MEMORY_THRESHOLD_MB</code> у <code>config.py</code> регулює межу активації GC.</p>
        <p><b>Q: Чи можна відключити автоматичне очищення кешу?</b><br>
        A: Так, встановіть <code>ENABLE_CACHE_MAINTENANCE = False</code>, але це призведе до поступового заповнення диска.</p>
        <p><b>Q: Який формат логів використовується?</b><br>
        A: За замовчуванням це JSON-формат, оптимізований для парсингу системами типу ELK або Grafana Loki.</p>
    </div>
</div>

<!-- SECTION 10: UTILS GLOSSARY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Глосарій Системних Утиліт</h2></div>
    <div class="glass-card flow-step">
        <ul>
            <li><b>TTL (Time To Live):</b> Час життя об'єкта в кеші до його видалення.</li>
            <li><b>GC (Garbage Collection):</b> Автоматичне звільнення пам'яті від об'єктів, що більше не використовуються.</li>
            <li><b>OOM (Out Of Memory):</b> Критична ситуація нестачі оперативної пам'яті.</li>
            <li><b>Sentinel:</b> Автономний процес-наглядач за здоров'ям системи.</li>
        </ul>
    </div>
</div>

<!-- SECTION 11: PROFESSIONAL USAGE GUIDELINES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Професійні настанови з використання</h2></div>
    <div class="glass-card flow-step">
        <p>При роботі з інструментарієм ATLAS дотримуйтесь наступних правил:</p>
        <ul>
            <li><b>Clean Code:</b> Не додавайте специфічну бізнес-логіку в <code>helpers.py</code>, тримайте утиліти універсальними.</li>
            <li><b>Logging Verbosity:</b> На продуктивному середовищі використовуйте рівень логування <code>WARNING</code> або <code>ERROR</code>.</li>
            <li><b>Validation:</b> Завжди використовуйте <code>validators.py</code> для перевірки складних вкладених об'єктів.</li>
            <li><b>Resources:</b> При виявленні витоків пам'яті першим ділом ініціюйте аудит через <code>memory_helper.py</code>.</li>
        </ul>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (PREDICTIVE UTILS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Predictive Utils)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Предиктивного Управління Ресурсами**, яке буде аналізувати патерни використання RAM та заздалегідь готувати кеш для найпопулярніших запитів. Також буде додано модуль <i>Health Dashboard</i> для самих утиліт та впроваджено автоматичну відправку критичних логів у Telegram-бот адміністратора через інтегровані вебхуки.</p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="./atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
</div>

<!-- ACADEMIC AUDIT HISTORY -->
<div class="audit-history" style="margin-top: 50px; padding: 20px; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.8rem;">
    <p><b>Audit ID:</b> ATH-2026-V4-UTILS</p>
    <p><b>Review Date:</b> 2026-05-04</p>
    <p><b>Status:</b> VERIFIED | DEFENSE-READY</p>
    <p><b>Note:</b> Інструментарій утиліт відповідає стандартам надійності та відмовостійкості систем критичної інфраструктури.</p>
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
