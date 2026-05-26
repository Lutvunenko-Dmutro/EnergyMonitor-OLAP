# Технічна специфікація: Розширений Інструментарій Допоміжних Сервісів (EXTENDED UTILS TOOLKIT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM UTILITIES | HELPERS & HANDLERS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛠️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Інструментарій Системи</h1>
            <p class="mega-subtitle">Централізована бібліотека допоміжних сервісів проєкту ATLAS: від інтелектуального управління кешем та пам'яттю до прецизійного логування та обробки виняткових ситуацій</p>
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

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Роль Утиліт в Архітектурі Системи</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/utils/</code> є "Швейцарським ножем" проєкту ATLAS. Хоча ці модулі не містять безпосередньої бізнес-логіки енергомоніторингу, вони забезпечують <b>Технічну Спроможність</b> всієї платформи. Тут зосереджені інструменти, які роблять ATLAS швидким, стабільним та легким у налагодженні. Ми розглядаємо утиліти як "клей", що з'єднує складні аналітичні модулі в єдиний, надійно працюючий організм. Кожен інструмент спроєктований з акцентом на продуктивність та мінімальне споживання ресурсів.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL RESOURCE CONTROL MODELS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичні моделі управління ресурсами</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення стабільності та довготривалої безперервної роботи (24/7) утиліти реалізують такі логіко-математичні алгоритми:</p>
        
        <h4>1. Поріг спрацювання вартового пам'яті (Memory Sentinel)</h4>
        <p>Поточний об'єм оперативної пам'яті, що споживається процесом дашборду ($\text{RAM}_{\text{process}}$), безперервно відстежується. Якщо значення перевищує критичну межу, примусово викликається збирач сміття (Garbage Collector):</p>
        $$\text{Trigger}_{\text{GC}} = \begin{cases} 
           1, & \text{якщо } \text{RAM}_{\text{process}} \ge \text{Limit}_{\text{OOM}} \\ 
           0, & \text{в іншому випадку} 
        \end{cases}$$
        <p>де $\text{Limit}_{\text{OOM}} = 512 \text{ МБ}$ (регулюється параметром <code>MEMORY_THRESHOLD_MB</code>).</p>

        <h4>2. Період очищення дискового кешу (Cache TTL Expiry)</h4>
        <p>Файли кешу застарівають відповідно до часу створення. Кожен файл $f$ видаляється, якщо дельта часу перевищує встановлений ліміт TTL:</p>
        $$\text{Age}(f) = t_{\text{current}} - t_{\text{creation}}(f) \ge \text{TTL}_{\text{limit}} \implies \text{Delete}(f)$$
        <p>де $\text{TTL}_{\text{limit}} = 86400 \text{ секунд}$ (24 години).</p>
    </div>
</div>

<!-- SECTION 03: UTILS INTERACTION DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема Взаємодії Утиліт (Architecture Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    APP_START("Application Boot") --> CACHE("cache_manager: TTL Cache Audit")
    CACHE --> LOG("logging_config: Init Structured Logs")
    LOG --> MONITOR("memory_helper: Set Watchdog Poller")
    
    subgraph RUNTIME_SUPPORT["Runtime Execution Guard"]
        ERR("error_handlers: Catch & Render Safe Block")
        UI_H("ui_helpers: Plotly Theme Injector")
        HELP("helpers: Common Logic Shorthands")
    end
    
    MONITOR --> RUNTIME_SUPPORT
    RUNTIME_SUPPORT --> SYSTEM_EXIT("Safe Exit & Cache Cleanup")
    </div></div>
</div>

<!-- SECTION 04: UTILITIES MODULES MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця Модулів Утиліт</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль коду</th>
                    <th>Призначення</th>
                    <th>Реалізований алгоритм</th>
                    <th>Вплив на екосистему ATLAS</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>cache_manager.py</code></td><td>Оптимізація дисків</td><td>Pre-emptive TTL Validation & Clean</td><td>Захист дискового простору від гігабайтних зрізів бази даних</td></tr>
                <tr><td><code>memory_helper.py</code></td><td>Контроль оперативки</td><td>auto_gc() та монітор через psutil</td><td>Захист від аварійного OOM-відключення (Out Of Memory)</td></tr>
                <tr><td><code>logging_config.py</code></td><td>Трасування подій</td><td>setup_structured_logs (JSON/txt)</td><td>Повна аудит-готовність та швидке виявлення багів (Troubleshooting)</td></tr>
                <tr><td><code>error_handlers.py</code></td><td>Стійкість до збоїв</td><td>safe_execution_wrapper (Fail-safe)</td><td>Запобігання падінню всього UI при збої одного віджета</td></tr>
                <tr><td><code>ui_helpers.py</code></td><td>UX кастомізація</td><td>Plotly Theme & Margin Injector</td><td>Плавна інтерактивна візуалізація в стилі Cyber-HUD</td></tr>
                <tr><td><code>helpers.py</code></td><td>Спрощення коду</td><td>Форматувальні функції та обробники дат</td><td>Дотримання принципів DRY та покращення читабельності коду</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: SEQUENCE: CACHE CLEANUP PROCESS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Послідовність дій: Очищення кешу (Sequence)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
sequenceDiagram
    participant Sys as ATLAS Core
    participant Ca as CacheManager
    participant FS as File System
    
    Sys->>Ca: Trigger Maintenance Event
    Ca->>FS: Scan Cache Directory
    FS-->>Ca: List of Cache Files
    Ca->>Ca: Filter Expired Files (Age >= 24h)
    Ca->>FS: Delete Selected Expired Files
    Ca-->>Sys: Return Freed Memory Summary (MB)
    </div></div>
</div>

<!-- SECTION 06: MEMORY SENTINEL & GARBAGE COLLECTION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Вартовий Пам'яті та Збір Сміття</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>memory_helper.py</code> містить систему **Watchdog Sentinel**. Вона постійно моніторить споживання RAM процесом. При наближенні до критичної межі, утиліта примусово ініціює глибокий збір сміття (Garbage Collection) через <code>gc.collect()</code>. Це дозволяє ATLAS працювати тижнями без перезавантаження, що є критичним для систем ситуаційного моніторингу в промислових умовах.</p>
    </div>
</div>

<!-- SECTION 07: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Псевдокод Інструментарію (Extended Utils Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>MODULE src.utils:
    1. // [GC WATCHDOG SENTINEL FOR OOM PROTECTION]
       FUNCTION monitor_memory_consumption(threshold_mb=512):
           process = psutil.Process(os.getpid())
           ram_usage = process.memory_info().rss / (1024 * 1024)
           IF ram_usage &gt;= threshold_mb:
               log_warning(f"⚠️ Високе використання RAM: {ram_usage:.1f}MB. Викликаємо GC...")
               gc.collect()
               
    2. // [PRE-EMPTIVE CACHE LIFECYCLE CLEANUP]
       FUNCTION cleanup_expired_cache(cache_dir, max_age_hours=24):
           limit_seconds = max_age_hours * 3600
           FOR cache_file IN Path(cache_dir).glob("*"):
               file_age = time.time() - cache_file.stat().st_mtime
               IF file_age &gt;= limit_seconds:
                   delete_file(cache_file)
                   
    3. // [FAIL-SAFE EXECUTION WRAPPER FOR UI STABILITY]
       FUNCTION safe_execute_widget(widget_func, *args, **kwargs):
           TRY:
               widget_func(*args, **kwargs)
           EXCEPT Exception as e:
               st.error("⚠️ Віджет тимчасово недоступний")
               log_error_context_to_file(e)
END MODULE</code></pre>
    </div>
</div>

<!-- SECTION 08: GRACEFUL ERROR HANDLING LAYER -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Шар М'якої Обробки Помилок (Fail-Safe)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>error_handlers.py</code> забезпечує принцип <b>Fail-Safe Rendering</b>. Якщо один аналітичний віджет виходить з ладу через некоректні дані, він не "обвалює" весь інтерфейс. Утиліта перехоплює виключення, логує його та відображає користувачеві безпечне повідомлення або пустий стан, зберігаючи працездатність решти системи. Це критично для забезпечення безперервності спостереження за мережею.</p>
    </div>
</div>

<!-- SECTION 09: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4><a href="ui_dashboard_layout.md">dashboard.py</a></h4>
                <p>Основний споживач утиліт для оптимізації рендерингу та запуску вартового пам'яті.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4><a href="data_services_hub.md">db_services.py</a></h4>
                <p>Використовує менеджер кешу для перевірки термінів придатності збережених таблиць споживання.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛡️</div>
            <div class="role-content">
                <h4><a href="utils_validators.md">validators.py</a></h4>
                <p>Тісна інтеграція з утилітами для перевірки користувацьких типів даних та текстових фільтрів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v3.0 (PREDICTIVE RESOURCE BALANCING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v3.0 (Predictive Resource Balancing)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 заплановано:</p>
        <ul>
            <li><b>Предиктивне вивільнення кешу:</b> ШІ буде вивчати звички оператора та заздалегідь підвантажувати в кеш найпопулярніші регіони, автоматично очищуючи неактивні.</li>
            <li><b>Loki & ELK Export:</b> Прямий експорт логів через Fluentbit у хмарні системи моніторингу критичної інфраструктури холдингу.</li>
            <li><b>UI Health Dashboard:</b> Окрема вкладка розробника для моніторингу поточної швидкості збору сміття та об'єму кешу.</li>
        </ul>
    </div>
</div>

<!-- SECTION 11: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">FAQ: Технічні особливості роботи</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Як змінити поріг вартового пам'яті?</b><br>
        A: Поріг регулюється константою <code>MEMORY_THRESHOLD_MB</code> у конфігураційному файлі. Для промислових серверів рекомендується встановити поріг 1024 або 2048 МБ.</p>
        <p><b>Q: Чи може очищення кешу призвести до видалення важливих даних?</b><br>
        A: Ні. Менеджер кешу видаляє тільки тимчасові проміжні зрізи розрахунків, які система вміє автоматично відновлювати при першому ж зверненні. База даних <code>energy.db</code> ніколи не підлягає автоматичному очищенню.</p>
        <p><b>Q: Навіщо потрібні окремі ui_helpers?</b><br>
        A: Вони ізолюють Streamlit-специфічні функції (такі як впровадження користувацьких CSS-стилів Orbitron та обгортки Plotly-рендерингу). Це залишає базові аналітичні модулі чистими від Streamlit-коду для полегшення майбутнього портування на React чи Django.</p>
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
