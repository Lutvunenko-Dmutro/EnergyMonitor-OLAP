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
        <p>Модулі пакета <code>src/app/</code> (<code>config.py</code>, <code>types.py</code>) виконують роль "Конституції" системи. Вони визначають правила гри для всіх інших шарів: від бази даних до інтерфейсу користувача. Замість використання "магічних рядків" по всьому коду, ми впроваджуємо строгу типізацію та іменовані константи. Це дозволяє уникнути помилок, пов'язаних з людським фактором, та значно спрощує рефакторинг та розширення системи у майбутньому.</p>
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
                    <th>Ключові Елементи</th>
                    <th>Вплив на Систему</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>config.py</code></td><td>Глобальні константи</td><td>DataKeys, UI_THEME, DB_PARAMS</td><td>Управління поведінкою системи</td></tr>
                <tr><td><code>types.py</code></td><td>Строга типізація</td><td>SubstationData, GenerationRecord</td><td>Гарантія цілісності даних</td></tr>
                <tr><td><code>__init__.py</code></td><td>Експорт інтерфейсів</td><td>Singleton Accessors</td><td>Спрощення імпортів у сервісах</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: TYPE ENFORCEMENT STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Забезпечення Типів</h2></div>
    <div class="glass-card flow-step">
        <p>Ми використовуємо поєднання <b>Python Type Hints</b> та кастомних класів даних для створення "Безпечного Рукостискання" (Safe Handshake) між ML-моделями та UI-компонентами. Це гарантує, що якщо модель прогнозування очікує масив певної форми, вона його отримає, а інтерфейс правильно інтерпретує результати. Такий підхід мінімізує <i>Runtime Errors</i> та робить систему передбачуваною.</p>
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

<!-- SECTION 05: CENTRALIZED CONFIGURATION MANAGEMENT -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Централізоване Управління Конфігурацією</h2></div>
    <div class="glass-card flow-step">
        <p>Конфігурація у <code>config.py</code> побудована за принципом <b>Single Source of Truth</b>. Всі ліміти навантаження, кольорові коди станів та ключі кешування зберігаються в одному місці. Це дозволяє змінити поведінку всього додатку (наприклад, змінити поріг критичного навантаження) шляхом редагування одного рядка коду, що є критичним для гнучкості оперативного управління енергосистемою.</p>
    </div>
</div>

<!-- SECTION 06: DATA MODELS & SCHEMA REGISTRY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Реєстр Моделей та Схем Даних</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>types.py</code> ми визначаємо <i>Digital Twin Schemas</i>. Ці структури описують фізичні параметри підстанцій: напругу, струм, склад газів у маслі. Використання спільних схем дозволяє аналітичному ядру та візуалізатору "говорити однією мовою", незалежно від того, чи дані надходять з реальних датчиків, чи з генератора симуляції.</p>
    </div>
</div>

<!-- SECTION 07: ERROR MITIGATION THROUGH ENUMS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Запобігання помилкам через Enums</h2></div>
    <div class="glass-card flow-step">
        <p>Для всіх категоріальних даних (типи генераторів, статуси аварій, регіони) використовуються <b>Enums</b>. Це унеможливлює ситуації, коли в одному місці коду регіон записаний як "Kyiv", а в іншому як "Київ". Всі порівняння та фільтрації відбуваються через посилання на константи, що забезпечує 100% точність аналітичних вибірок.</p>
    </div>
</div>

<!-- SECTION 08: CONFIGURATION AGNOSTICISM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Конфігураційний Агностицизм</h2></div>
    <div class="glass-card flow-step">
        <p>Ядро розроблено так, щоб бути незалежним від середовища виконання. За допомогою змінних оточення (Environment Variables) конфігурація може адаптуватися до локальної розробки, CI/CD тестів або продакшн-розгортання в хмарі, не вимагаючи внесення змін до вихідного коду модулів конфігурації.</p>
    </div>
</div>

<!-- SECTION 09: MAINTENANCE & SCALABILITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Супровід та Масштабованість</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки чіткому розділенню типів та налаштувань, додавання нового типу енергооб'єкта або нового аналітичного параметра займає мінімум часу. Програміст просто додає поле в існуючий тип у <code>types.py</code>, і IDE автоматично підказує всі місця в проекті, де цей параметр потрібно обробити, що значно знижує технічний борг.</p>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v3.0 (DYNAMIC CONFIG) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v3.0 (Dynamic Core)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступних версіях планується впровадження **Динамічної Конфігурації**, яка дозволить змінювати параметри системи без перезапуску інтерфейсу. Також буде додано автоматичну генерацію API-схем на основі <code>types.py</code> для інтеграції з зовнішніми сервісами та розширено підтримку складних вкладених типів для більш детального моделювання мікромереж (Microgrids).</p>
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
