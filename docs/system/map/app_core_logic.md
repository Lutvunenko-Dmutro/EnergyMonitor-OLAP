# Технічна специфікація: Ядро Конфігурації та Типізації Додатка (APP CORE LOGIC)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">APPLICATION CORE | TYPES & CONFIG</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Ядро Додатка</h1>
            <p class="mega-subtitle">Централізоване управління конфігурацією, типами даних та глобальними константами системи ATLAS, що забезпечує цілісність бізнес-логіки та стабільність обміну даними між шарами</p>
            <div class="status-tags"><span class="tag tag-online">CORE ACTIVE</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">BASE LOGIC</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🆔</div><div class="metric-info"><span class="metric-label">Identity</span><span class="metric-value">Strict Enum Mapping</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔑</div><div class="metric-info"><span class="metric-label">Config</span><span class="metric-value">Environment Agnostic</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Data</span><span class="metric-value">Pydantic/Typed Handshake</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Zero-Null Tolerance</span></div></div>
</div>

<!-- SECTION 01: ARCHITECTURAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Архітектурна Роль Ядра</h2></div>
    <div class="glass-card flow-step">
        <p>Модулі пакета <code>src/app/</code> (<code>config.py</code>, <code>types.py</code>) виконують роль "Конституції" системи. Вони визначають правила гри для всіх інших шарів: від бази даних до інтерфейсу користувача. Замість використання "магічних рядків" по всьому коду, ми впроваджуємо строгу типізацію та іменовані константи. Це дозволяє уникнути помилок, пов'язаних з людським фактором, та значно спрощує рефакторинг та розширення системи у майбутньому. Ядро забезпечує те, що кожна компонента ATLAS розуміє очікувані формати даних та межі своїх повноважень.</p>
    </div>
</div>

<!-- SECTION 02: CORE COMPONENTS MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Матриця Компонентів Ядра</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль</th>
                    <th>Роль</th>
                    <th>Методологія</th>
                    <th>Ключовий Елемент</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>config.py</code></td><td>Глобальні константи</td><td>Static Registry Pattern</td><td>SystemSettings Class</td></tr>
                <tr><td><code>types.py</code></td><td>Строга типізація</td><td>Pydantic / TypedDict</td><td>DataModels Registry</td></tr>
                <tr><td><code>__init__.py</code></td><td>Експорт інтерфейсів</td><td>Singleton Accessors</td><td>Interface Re-exports</td></tr>
                <tr><td><code>paths.py</code></td><td>Управління шляхами</td><td>Pathlib Integration</td><td>Project FS Registry</td></tr>
                <tr><td><code>exceptions.py</code></td><td>Доменні помилки</td><td>Custom Exception Tree</td><td>AtlasBaseException</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: TYPE ENFORCEMENT STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Забезпечення Типів</h2></div>
    <div class="glass-card flow-step">
        <p>Ми використовуємо поєднання <b>Python Type Hints</b> та кастомних класів даних (на базі Pydantic або dataclasses) для створення "Безпечного Рукостискання" (Safe Handshake) між ML-моделями та UI-компонентами. 
        Це гарантує:
        <ul>
            <li><b>Validation at Boundary:</b> Перевірка даних на вході в сервіс.</li>
            <li><b>Schema Enforcement:</b> Неможливість передачі некоректних полів у UI.</li>
            <li><b>IDE Support:</b> Повне автодоповнення та статична перевірка коду (Mypy).</li>
        </ul>
        Такий підхід мінімізує <i>Runtime Errors</i> та робить систему передбачуваною.</p>
    </div>
</div>

<!-- SECTION 04: DATA FLOW DIAGRAM (CORE ORIENTED) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема потоку даних (Ядро)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph LR
    CONFIG("config.py: Constants") --> SERVICE("Services Logic")
    TYPES("types.py: Schemas") --> SERVICE
    SERVICE --> UI("UI Views")
    DB("Database") -- Raw Data --> SERVICE
    SERVICE -- Typed Objects --> UI
    </div></div>
</div>

<!-- SECTION 05: THE CORE SINGLETON PATTERN -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Патерн Singleton у конфігурації</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення глобального доступу до налаштувань без створення дублікатів у пам'яті, об'єкт конфігурації реалізовано через патерн **Singleton**. Це гарантує, що будь-яка зміна в налаштуваннях під час виконання (runtime) буде миттєво доступна всім модулям системи. Такий підхід забезпечує синхронізовану поведінку всіх компонентів ATLAS, від стрімінгу телеметрії до генерації звітів.</p>
    </div>
</div>

<!-- SECTION 06: CENTRALIZED CONFIGURATION MANAGEMENT -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Централізоване Управління Конфігурацією</h2></div>
    <div class="glass-card flow-step">
        <p>Конфігурація у <code>config.py</code> побудована за принципом <b>Single Source of Truth</b>. Всі ліміти навантаження, кольорові коди станів та ключі кешування зберігаються в одному місці. Це дозволяє змінити поведінку всього додатку (наприклад, змінити поріг критичного навантаження або URL бази даних) шляхом редагування одного рядка коду. Це критично для гнучкості оперативного управління та швидкого розгортання системи в різних інфраструктурних умовах.</p>
    </div>
</div>

<!-- SECTION 07: SEQUENCE: APPLICATION HANDSHAKE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Sequence: Процес ініціалізації Ядра</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
sequenceDiagram
    participant App as ATLAS Main
    participant Co as Config.py
    participant Ty as Types.py
    participant DB as DB Service
    
    App->>Co: Load System Constants
    Co-->>App: Constants Loaded
    App->>Ty: Register Data Schemas
    Ty-->>App: Schemas Active
    App->>DB: Handshake with Typed Config
    DB-->>App: Connection Verified (ACID)
    App->>App: Core Logic Ready
    </div></div>
</div>

<!-- SECTION 08: DATA MODELS & SCHEMA REGISTRY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Реєстр Моделей та Схем Даних</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>types.py</code> ми визначаємо <i>Digital Twin Schemas</i>. Ці структури описують фізичні параметри підстанцій: напругу, струм, склад газів у маслі. Використання спільних схем дозволяє аналітичному ядру та візуалізатору "говорити однією мовою", незалежно від того, чи дані надходять з реальних датчиків, чи з генератора симуляції. Це забезпечує високу модульність: ми можемо замінити джерело даних, не змінюючи логіку обробки.</p>
    </div>
</div>

<!-- SECTION 09: ERROR MITIGATION THROUGH ENUMS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Запобігання помилкам через Enums</h2></div>
    <div class="glass-card flow-step">
        <p>Для всіх категоріальних даних використовуються <b>Enums</b>. Це унеможливлює ситуації з друкарськими помилками в ключах або назвах регіонів. Всі порівняння та фільтрації відбуваються через посилання на об'єкти констант, що забезпечує 100% точність аналітичних вибірок. Це також спрощує локалізацію інтерфейсу: ми змінюємо відображення імені в одному місці Enum, і воно оновлюється всюди.</p>
    </div>
</div>

<!-- SECTION 10: MAINTENANCE & SCALABILITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Супровід та Масштабованість</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки чіткому розділенню типів та налаштувань, додавання нового типу енергооб'єкта (наприклад, сонячної станції) займає мінімум часу. Програміст просто додає поле в існуючий тип у <code>types.py</code>, і інструменти статичного аналізу автоматично підказують всі місця в проекті, де цей параметр потрібно обробити. Це значно знижує технічний борг та робить проект ATLAS готовим до довгострокового супроводу в промислових масштабах.</p>
    </div>
</div>

<!-- SECTION 11: ROADMAP TO v3.0 (DYNAMIC CONFIG) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Дорожня карта v3.0 (Dynamic Core)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступних версіях планується впровадження **Динамічної Конфігурації**, яка дозволить змінювати параметри системи (наприклад, інтервал опитування датчиків) без перезапуску інтерфейсу через механізм <i>Hot Reload</i>. Також буде додано автоматичну генерацію документації OpenAPI на основі <code>types.py</code> та розширено підтримку складних вкладених типів для більш детального моделювання Smart-Grid мереж наступного покоління.</p>
    </div>
</div>

<!-- SECTION 12: APP CORE TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Технічний FAQ Ядра Додатка</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Як додати нову глобальну константу?</b><br>
        A: Необхідно додати її в клас <code>SystemSettings</code> у файлі <code>config.py</code>. Це забезпечить її доступність через Singleton-екземпляр.</p>
        <p><b>Q: Що робити, якщо Pydantic модель видає ValidationError?</b><br>
        A: Перевірте відповідність вхідних даних схемі в <code>types.py</code>. Найчастіше це свідчить про зміну формату даних у БД без оновлення моделей ядра.</p>
        <p><b>Q: Чи можна використовувати змінні оточення (.env)?</b><br>
        A: Так, ядро автоматично завантажує параметри з файлу <code>.env</code>, якщо вони там визначені, надаючи їм пріоритет над дефолтними значеннями.</p>
    </div>
</div>

<!-- SECTION 13: APP CORE GLOSSARY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">Глосарій Ядра Додатка</h2></div>
    <div class="glass-card flow-step">
        <ul>
            <li><b>Singleton:</b> Патерн проектування, який гарантує наявність лише одного екземпляра класу в системі.</li>
            <li><b>Strict Typing:</b> Механізм контролю відповідності типів даних під час розробки та виконання коду.</li>
            <li><b>Environment Agnostic:</b> Здатність системи працювати в різних оточеннях без зміни вихідного коду.</li>
            <li><b>Schema Handshake:</b> Процес верифікації структури даних при передачі між різними шарами архітектури.</li>
        </ul>
    </div>
</div>

<!-- SECTION 14: PROFESSIONAL USAGE GUIDELINES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">14</span><h2 class="section-title">Професійні настанови з використання Ядра</h2></div>
    <div class="glass-card flow-step">
        <p>При розширенні логіки ядра ATLAS враховуйте наступні архітектурні принципи:</p>
        <ul>
            <li><b>Type Safety:</b> Завжди оновлюйте <code>types.py</code> перед внесенням змін у логіку сервісів.</li>
            <li><b>Config Isolation:</b> Не хардкодьте шляхи до файлів, використовуйте <code>ProjectPaths</code> з <code>config.py</code>.</li>
            <li><b>Singleton Integrity:</b> Уникайте створення декількох екземплярів <code>SystemSettings</code>, використовуйте лише метод <code>get_instance()</code>.</li>
            <li><b>Documentation:</b> Кожен новий тип даних повинен мати відповідний опис у технічному паспорті хаба.</li>
        </ul>
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
