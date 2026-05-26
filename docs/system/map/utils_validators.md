# Технічна специфікація: Шар Безпеки та Валідації (SECURITY & VALIDATION LAYER)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CYBER SECURITY | INPUT SHIELD</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛡️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Валідатор Системи</h1>
            <p class="mega-subtitle">Шар кіберзахисту та цілісності даних проєкту ATLAS: багатошарова верифікація користувацького вводу, двигун запобігання SQL-ін'єкціям та суворий контроль фізичних меж енергосистеми</p>
            <div class="status-tags"><span class="tag tag-online">SAFEGUARD ACTIVE</span><span class="tag tag-version">v2.2.0</span><span class="tag tag-role">SECURITY GUARDIAN</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🚫</div><div class="metric-info"><span class="metric-label">Engine</span><span class="metric-value">Anti-SQL Injection</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚪</div><div class="metric-info"><span class="metric-label">Method</span><span class="metric-value">Whitelist Verification</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📏</div><div class="metric-info"><span class="metric-label">Bounds</span><span class="metric-value">Physical Range Check</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Sanitization</span><span class="metric-value">SQL Identifier Clean</span></div></div>
</div>

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Безпеки та Валідації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>validators.py</code> є "Імунною системою" та "Прикордонним контролем" проєкту ATLAS. В системах критичної інфраструктури будь-яка помилка у вхідних даних або навмисна маніпуляція (ін'єкція) може призвести до невірних аналітичних висновків або збою системи. Наша філософія базується на <b>Нульовій Довірі (Zero Trust)</b>: кожен біт інформації, що надходить від користувача або зовнішніх сервісів, проходить через суворий шар перевірок. Ми використовуємо білі списки (Whitelists), семантичний аналіз SQL-патернів та фізичні обмеження реального світу, щоб гарантувати, що ядро Атласу оперує виключно безпечними та валідними даними.</p>
    </div>
</div>

<!-- SECTION 02: FORMAL SECURITY MODELS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математична формалізація захисного контуру</h2></div>
    <div class="glass-card flow-step">
        <p>Валідація вхідних даних спирається на теорію формальних граматик та логічні константи:</p>
        
        <h4>1. Функція верифікації білого списку ($f_{\text{valid}}$)</h4>
        <p>Вхідний рядок $x$ вважається безпечним тоді й лише тоді, коли він належить допустимому білому списку $\mathbf{W}$ та відповідає регулярному виразу дозволених символів $\mathbf{P}_{\text{safe}}$:</p>
        $$f_{\text{valid}}(x) = \begin{cases} 
           1, & \text{якщо } x \in \mathbf{W} \text{ та } \text{RegexMatch}(x, \mathbf{P}_{\text{safe}}) \\ 
           0, & \text{в іншому випадку} 
        \end{cases}$$
        <p>де $\mathbf{P}_{\text{safe}} = \text{"^[a-zA-Z0-9\_]+$"}$ (запобігає використанню лапок, крапок з комою та пробілів у SQL-ідентифікаторах).</p>

        <h4>2. Фізичні обмеження (Numeric Range Constraint)</h4>
        <p>Будь-який числовий показник датчика $V_{\text{input}}$ (наприклад, температура масла) валідується на відповідність фізичним межам реального світу:</p>
        $$\text{Constraint}(V_{\text{input}}) \implies V_{\text{input}} \in [V_{\text{min}}, V_{\text{max}}]$$
        <p>Порушення інтервалу виключає запис з обробки та ініціює системне попередження <code>ValidationError</code>.</p>
    </div>
</div>

<!-- SECTION 03: VALIDATION PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема Конвеєра Безпеки (Validation Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    INPUT("User Input (Region, Substation, SQL Key)") --> SCAN("Anti-Injection Engine")
    
    subgraph SECURITY_LAYERS["Multi-layer Shield"]
        SCAN -- "Check Keywords" --> KW("DANGEROUS_KEYWORDS (drop, union, insert)")
        KW -- "Check Syntax" --> SYNTAX("Pattern Detection (' or, ' =)")
        SYNTAX -- "Whitelist Check" --> WHITE("BUILTIN_NAMES / VALID_STEP_KEYS")
    end
    
    WHITE -- "Fail" --> REJECT("ValidationError & Security Audit log")
    WHITE -- "Pass" --> BOUNDS("Bounds Checking (Numeric/Date Range)")
    
    BOUNDS -- "Out of Range" --> WARNING("Log Warning & Exception")
    BOUNDS -- "OK" --> SANITIZE("Final Sanitization")
    
    SANITIZE --> READY("SAFE_INPUT for Core Engines")
    </div></div>
</div>

<!-- SECTION 04: VALIDATION WHITELIST MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця білих списків (Whitelists)</h2></div>
    <div class="glass-card flow-step">
        <p>Для мінімізації гнучкості зловмисника, модуль спирається на жорстко визначені константні контури перевірок:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Тип білого списку</th>
                    <th>Цільова константа</th>
                    <th>Об'єкт захисту</th>
                    <th>Діагностичне значення</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Системні імена</b></td><td><code>BUILTIN_NAMES</code></td><td>Абстракції глобального вибору (Всі, All, Global)</td><td>Запобігання підміни глобальних фільтрів вибірки</td></tr>
                <tr><td><b>Ключі завантаження</b></td><td><code>VALID_STEP_KEYS</code></td><td>Ідентифікатори етапів (sql_load, sql_fin...)</td><td>Захист оркестратора від виконання недозволених запитів</td></tr>
                <tr><td><b>Джерела даних</b></td><td><code>VALID_DATA_SOURCES</code></td><td>Провайдери (PostgreSQL, Kaggle, Cache, Live)</td><td>Захист ETL конвеєра від підключення фейкових баз</td></tr>
                <tr><td><b>Заборонені слова</b></td><td><code>DANGEROUS_KEYWORDS</code></td><td>Blacklist SQL-токенів (drop, union, truncate, or)</td><td>Анти-ін'єкційний щит (Anti-SQL Injection Shield)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: PHYSICAL BOUNDS & RANGE CHECKING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Фізичні межі та контроль діапазонів</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>validate_numeric_input</code> реалізує логіку <b>Engineering Sanity</b>. В енергетиці існують межі можливого: навантаження не може бути від'ємним, а температура трансформатора не може перевищувати певні критичні значення (наприклад, 150°C). Валідатор забезпечує суворий контроль <code>min_val</code> та <code>max_val</code>, відсікаючи аномальні показники датчиків або помилки вводу оператора, що гарантує фізичну коректність всієї аналітичної моделі Атласу.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Валідатора (Shield Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>MODULE src.utils.validators:
    1. // [ANTI-SQL INJECTION REGEX PATTERN MATCH]
       FUNCTION has_dangerous_patterns(input_str):
           FOR keyword IN DANGEROUS_KEYWORDS:
               IF keyword in input_str.lower():
                   RETURN True
           FOR pattern IN DANGEROUS_SYNTAX_PATTERNS: // "or 1=1", "' ="
               IF regex_match(pattern, input_str):
                   RETURN True
           RETURN False
           
    2. // [SUITE FOR MULTIPLE/SINGLE SUBSTATION ENTRIES]
       FUNCTION validate_substation_name(name):
           IF name is None: 
               RETURN True
           IF type(name) is list:
               FOR item IN name:
                   validate_substation_name(item)
               RETURN True
           IF type(name) is string:
               IF name IN BUILTIN_NAMES: 
                   RETURN True
               IF has_dangerous_patterns(name):
                   RAISE ValidationError("🚨 SQL Injection Attempt Blocked!")
               RETURN True
           RAISE TypeError("Некоректний тип імені об'єкта")
           
    3. // [ALPHABETICAL PURITY COLUMN SANITIZER]
       FUNCTION sanitize_column_name(name):
           IF len(name) &gt; 100:
               RAISE ValidationError("Задовге ім'я колонки")
           IF NOT regex_match("^[a-zA-Z0-9_]+$", name):
               RAISE ValidationError("Недозволені символи в назві колонки")
           RETURN name
END MODULE</code></pre>
    </div>
</div>

<!-- SECTION 07: SQL IDENTIFIER SANITIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Санітизація SQL-ідентифікаторів</h2></div>
    <div class="glass-card flow-step">
        <p>Для динамічних запитів, де назви колонок можуть обиратися користувачем, використовується функція <code>sanitize_column_name</code>. Вона реалізує суворий режим <b>Alphabetical Purity</b>: дозволені лише латинські літери, цифри та символ підкреслення. Будь-який інший символ (пробіл, лапки, крапка) призводить до негайного відхилення запиту. Це унеможливлює техніку атаки через маніпуляцію іменами колонок у складних SQL-командах.</p>
    </div>
</div>

<!-- SECTION 08: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🗄️</div>
            <div class="role-content">
                <h4><a href="core_kernel_hub.md">src.core.database</a></h4>
                <p>Низькорівневий SQL-двигун, що використовує валідатори перед виконанням динамічних запитів до SQLite та Neon Cloud.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4><a href="analysis_services_hub.md">aggregator.py</a></h4>
                <p>Фільтрує вхідні DataFrames на основі валідованих списків підстанцій.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4><a href="utils_extended_toolkit.md">error_handlers.py</a></h4>
                <p>Перехоплює винятки <code>ValidationError</code> та безпечно відображає їх оператору як попередження.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 09: ROADMAP TO v3.0 (ML ANOMALY PATTERN SCANNING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Дорожня карта v3.0 (ML Anomaly Pattern Scanning)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 заплановано:</p>
        <ul>
            <li><b>AI Anomaly Guard:</b> Використання навченої моделі Isolation Forest для динамічного виявлення аномальних вхідних значень датчиків на основі поведінкового контексту.</li>
            <li><b>Deep SQL AST Parsing:</b> Застосування повноцінного синтаксичного аналізатора SQL (через бібліотеку <code>sqlparse</code>) для глибокої верифікації структури складних запитів.</li>
            <li><b>Real-time IP Block:</b> Інтеграція з фаєрволом Neon Cloud для автоматичного блокування IP-адрес користувачів, які здійснили більше 3 спроб SQL-ін'єкцій.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">FAQ: Технічні відповіді про Валідатор</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Чому після спроби ввести деякі текстові описи інцидентів виникає помилка безпеки?</b><br>
        A: Валідатор сканує текстові поля на наявність небезпечних патернів. Якщо ваш опис містить слова на кшталт "select object for union" (наприклад, при описі дій ремонтної бригади), Anti-Injection Shield розпізнає це як потенційну SQL-ін'єкцію (keyword <code>union</code>) та відхилить запит з міркувань безпеки. Змініть формулювання.</p>
        <p><b>Q: Як працює валідація часових діапазонів?</b><br>
        A: Функція <code>validate_date_range</code> перевіряє, чи є об'єкти датами, чи дата початку менша або дорівнює даті кінця (Start &le; End), а також чи період не перевищує 5 років. Це захищає сервер Neon Cloud від переповнення пам'яті (OOM) при масовому завантаженні гігабайтної історії.</p>
        <p><b>Q: Чому назви підстанцій перевіряються через списки?</b><br>
        A: Оскільки користувач може обрати декілька підстанцій одночасно, валідатор <code>validate_substation_name</code> реалізує рекурсивну перевірку: якщо на вхід надходить список (List), функція викликає сама себе для кожного елемента списку, забезпечуючи 100% захист кожного об'єкта.</p>
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
