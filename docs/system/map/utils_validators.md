# Технічна специфікація: Шар Безпеки та Валідації (SECURITY & VALIDATION LAYER)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CYBER SECURITY | INPUT SHIELD</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛡️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Валідатор Системи</h1>
            <p class="mega-subtitle">Шар кіберзахисту проекту ATLAS: багатошарова верифікація користувацького вводу, двигун запобігання SQL-ін'єкціям (Anti-Injection) та суворий контроль меж фізичних показників енергосистеми</p>
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

<!-- SECTION 01: SECURITY VALIDATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Безпеки та Валідації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>validators.py</code> є "Імунною системою" та "Прикордонним контролем" проекту ATLAS. В системах критичної інфраструктури будь-яка помилка у вхідних даних або навмисна маніпуляція (ін'єкція) може призвести до невірних аналітичних висновків або збою системи. Наша філософія базується на <b>Нульовій Довірі (Zero Trust)</b>: кожен біт інформації, що надходить від користувача або зовнішніх сервісів, проходить через суворий шар перевірок. Ми використовуємо білі списки (Whitelists), семантичний аналіз SQL-патернів та фізичні обмеження реального світу, щоб гарантувати, що ядро Атласу оперує виключно безпечними та валідними даними.</p>
    </div>
</div>

<!-- SECTION 02: VALIDATION PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема конвеєра безпеки (Validation Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    INPUT("User Input (Region, Substation, SQL Key)") --> SCAN("Anti-Injection Engine")
    
    subgraph SECURITY_LAYERS["Multi-layer Shield"]
        SCAN -- "Check Keywords" --> KW("DANGEROUS_KEYWORDS (drop, union, etc.)")
        KW -- "Check Syntax" --> SYNTAX("Pattern Detection (' or, ' =)")
        SYNTAX -- "Whitelist Check" --> WHITE("BUILTIN_NAMES / VALID_STEP_KEYS")
    end
    
    WHITE -- "Fail" --> REJECT("ValidationError & Security Audit")
    WHITE -- "Pass" --> BOUNDS("Bounds Checking (Numeric/Date)")
    
    BOUNDS -- "Out of Range" --> WARNING("Log Warning & Filter")
    BOUNDS -- "OK" --> SANITIZE("Final Sanitization")
    
    SANITIZE --> READY("SAFE_INPUT for Core Engines")
    </div></div>
</div>

<!-- SECTION 03: THE ANTI-INJECTION ENGINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Двигун запобігання ін'єкціям (Anti-Injection)</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>_has_dangerous_patterns</code> реалізує інтелектуальний аналіз тексту. Ми не просто шукаємо заборонені слова (напр. <code>drop</code>, <code>truncate</code>), ми аналізуємо семантичні конструкції, характерні для атак. Виявлення паттернів на кшталт <code>' or </code> або <code>' = </code> дозволяє заблокувати спроби обходу авторизації або несанкціонованої вибірки даних ще до того, як запит потрапить до бази даних Neon Cloud.</p>
    </div>
</div>

<!-- SECTION 04: VALIDATION WHITELIST MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця білих списків (Whitelists)</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Тип реєстру</th>
                    <th>Константа</th>
                    <th>Кількість елементів</th>
                    <th>Призначення</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Системні імена</td><td>BUILTIN_NAMES</td><td>5 (Усі, All, etc.)</td><td>Абстракція глобального вибору</td></tr>
                <tr><td>Ключі завантаження</td><td>VALID_STEP_KEYS</td><td>6 (sql_load, sql_fin...)</td><td>Захист оркестратора даних</td></tr>
                <tr><td>Джерела даних</td><td>VALID_DATA_SOURCES</td><td>4 (PG, Kaggle, Cache...)</td><td>Валідація ETL-потоків</td></tr>
                <tr><td>Заборонені слова</td><td>DANGEROUS_KEYWORDS</td><td>20+ SQL-токенів</td><td>Anti-Injection Shield</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: PHYSICAL BOUNDS & RANGE CHECKING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Фізичні межі та контроль діапазонів</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>validate_numeric_input</code> реалізує логіку <b>Engineering Sanity</b>. В енергетиці існують межі можливого: навантаження не може бути від'ємним, а температура трансформатора не може перевищувати певні критичні значення (напр. 150°C). Валідатор забезпечує суворий контроль <code>min_val</code> та <code>max_val</code>, відсікаючи аномальні показники датчиків або помилки вводу оператора, що гарантує фізичну коректність всієї аналітичної моделі Атласу.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (VALIDATION PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Валідатора (Shield Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION validate_substation_name(name):
    1. IF name IS None: RETURN True
    2. IF name IS string:
           IF name IN BUILTIN_NAMES: RETURN True
           IF has_dangerous_patterns(name):
               RAISE ValidationError("SQL Injection Detected!")
           RETURN True
    3. IF name IS list:
           FOR item IN name: validate_substation_name(item)
    4. ELSE: RAISE TypeError
END FUNCTION

FUNCTION sanitize_column_name(name):
    1. CHECK Length < 100 chars
    2. CHECK allowed_chars (a-z, 0-9, _)
    3. IF mismatch: RAISE ValidationError
    4. RETURN name
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: SQL IDENTIFIER SANITIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Санітизація SQL-ідентифікаторів</h2></div>
    <div class="glass-card flow-step">
        <p>Для динамічних запитів, де назви колонок можуть обиратися користувачем, використовується функція <code>sanitize_column_name</code>. Вона реалізує суворий режим <b>Alphabetical Purity</b>: дозволені лише латинські літери, цифри та символ підкреслення. Будь-який інший символ (пробіл, лапки, крапка) призводить до негайного відхилення запиту. Це унеможливлює техніку атаки через маніпуляцію іменами колонок у складних SQL-командах.</p>
    </div>
</div>

<!-- SECTION 08: TEMPORAL LOGIC VALIDATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Валідація часової логіки</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>validate_date_range</code> перевіряє не тільки типи (date objects), а й логічну послідовність (Start <= End). Також впроваджено <b>Large Range Warning</b>: якщо користувач намагається завантажити дані за період понад 5 років, система видає попередження в логах. Це захищає сервер від Out-of-Memory збоїв при спробі обробити надто великі масиви даних за один раз.</p>
    </div>
</div>

<!-- SECTION 09: MULTI-LEVEL LOGGING & AUDIT -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Багаторівневе логування та аудит</h2></div>
    <div class="glass-card flow-step">
        <p>Будь-яка невдала спроба валідації супроводжується записом у <code>system.log</code> з рівнем <code>WARNING</code> або <code>ERROR</code>. Лог містить деталі: який саме паттерн було виявлено або які межі було порушено. Це перетворює <code>validators.py</code> на систему виявлення вторгнень (IDS), дозволяючи адміністраторам ATLAS відстежувати підозрілу активність або технічні проблеми у вхідних потоках даних.</p>
    </div>
</div>

<!-- SECTION 10: ARCHITECTURAL DECOUPLING (DRY SECURITY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Архітектурна розв'язка (DRY Security)</h2></div>
    <div class="glass-card flow-step">
        <p>Централізація перевірок у <code>validators.py</code> реалізує принцип <b>Single Responsibility</b>. Якщо в майбутньому з'являться нові типи атак або зміняться вимоги до безпеки, розробнику достатньо оновити <code>DANGEROUS_KEYWORDS</code> в одному файлі. Всі інші 60+ модулів Атласу автоматично отримають оновлений захист, що гарантує цілісність безпекового контуру всієї платформи.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Core Analytics</h4>
                <p>Головний споживач валідаторів для фільтрації вхідних DataFrames.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🗄️</div>
            <div class="role-content">
                <h4>Core Database</h4>
                <p>Використовує санітизатори для безпечної побудови динамічних запитів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📡</div>
            <div class="role-content">
                <h4>System Logger</h4>
                <p>Канал реєстрації порушень безпеки та аномалій вхідних даних.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (ML-BASED ANOMALY DETECTION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (ML Anomaly Detection)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Адаптивної валідації**. Замість жорстких білих списків система буде використовувати <b>Isolation Forest</b> для виявлення аномальних вхідних значень на основі історичного контексту. Також буде додано підтримку <b>Deep SQL Parsing</b> (через <code>sqlparse</code>), що дозволить проводити гранулярний аналіз структури запитів для виявлення ще більш витончених векторів атак.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Валідатор Системи</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому я отримую ValidationError при пошуку?</b> — Ймовірно, ваш запит містить спецсимволи або ключові слова SQL, які система вважає небезпечними.</p>
        <p><b>Чи можна вимкнути Bounds Check?</b> — Ні, це вбудований захист для запобігання математичним помилкам у фізичному ядрі Атласу.</p>
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
