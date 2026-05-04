# Технічна специфікація: Ядро Системних Операцій та Фізики (CORE KERNEL HUB)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM CORE | PHYSICS & DATA ACCESS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Ядро Системи</h1>
            <p class="mega-subtitle">Фундаментальний шар ATLAS: математичне моделювання фізичних процесів енергомережі, оркестрація низькорівневих SQL-запитів та інтелектуальне завантаження зовнішніх архівів Kaggle</p>
            <div class="status-tags"><span class="tag tag-online">KERNEL ACTIVE</span><span class="tag tag-version">v2.9.0</span><span class="tag tag-role">BASE INFRASTRUCTURE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⚛️</div><div class="metric-info"><span class="metric-label">Physics</span><span class="metric-value">Ohm & Joule Models</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Queries</span><span class="metric-value">Optimized SQL Bus</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Kaggle</span><span class="metric-value">Lazy CSV Loader</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Integrity</span><span class="metric-value">Atomic Data Access</span></div></div>
</div>

<!-- SECTION 01: ARCHITECTURAL FOUNDATION -->
<div class="section-container" id="main">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Архітектурний Фундамент Ядра</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/core/</code> є найнижчим та найбільш критичним шаром проекту ATLAS. Це "Двигун", на якому базується вся вища логіка. Тут визначаються закони фізики, за якими працює наша модель енергосистеми, та правила взаємодії з джерелами даних. Без цього шару ні ML-моделі, ні UI-компоненти не мали б твердого ґрунту для розрахунків та відображення інформації.</p>
    </div>
</div>

<!-- SECTION 02: KERNEL COMPONENTS MATRIX -->
<div class="section-container" id="config">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Матриця Компонентів Ядра</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль</th>
                    <th>Функціональна Роль</th>
                    <th>Ключова Технологія</th>
                    <th>Вплив</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>physics.py</code></td><td>Фізичне моделювання</td><td>Математичні формули</td><td>Точність симуляції</td></tr>
                <tr><td><code>queries.py</code></td><td>Доступ до даних</td><td>SQL / Raw Logic</td><td>Продуктивність БД</td></tr>
                <tr><td><code>kaggle_loader.py</code></td><td>Зовнішні дані</td><td>Pandas / Lazy Loading</td><td>Гнучкість аналізу</td></tr>
                <tr><td><code>logger.py</code></td><td>Системний аудит</td><td>Logging Stream</td><td>Трасування</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: PHYSICS-DRIVEN MODELING STRATEGY -->
<div class="section-container" id="physics">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Фізично-орієнтованого Моделювання</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>physics.py</code> ми імплементуємо базові закони електротехніки. Ми моделюємо втрати енергії в лініях (Закон Джоуля-Ленца) та падіння напруги залежно від навантаження. Це робить систему ATLAS не просто візуалізатором таблиць, а **Справжнім Енергетичним Симулятором**, який розуміє фізичну природу процесів, що відбуваються в мережі.</p>
    </div>
</div>

<!-- SECTION 04: CORE DATA INTERACTION DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема Взаємодії Ядра з Даними</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI_REQ("UI / Service Request") --> QUERY_BUS("queries.py: Query Orchestrator")
    QUERY_BUS --> DB_LOCAL[("Local PostgreSQL")]
    QUERY_BUS --> DB_CLOUD[("Cloud Neon DB")]
    
    KAG_REQ("Archive Request") --> KAG_LOAD("kaggle_loader: Lazy CSV")
    KAG_LOAD --> CSV_STORAGE[("Kaggle Dataset Storage")]
    
    PHYS_ENG("physics.py: Engine") -- Rules --> SENSORS("Simulation Sensors")
    SENSORS -- Data --> DB_LOCAL
    </div></div>
</div>

<!-- SECTION 05: OPTIMIZED QUERY ORCHESTRATION -->
<div class="section-container" id="queries">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Оптимізована Оркестрація Запитів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>queries.py</code> містить бібліотеку пре-компільованих SQL-запитів. Ми уникаємо динамічного формування SQL-рядків у коді, що не лише підвищує продуктивність, а й захищає систему від SQL-ін'єкцій. Кожен запит оптимізовано для роботи з великими масивами часових рядів, забезпечуючи миттєву агрегацію мільйонів записів.</p>
    </div>
</div>

<!-- SECTION 06: INTELLIGENT KAGGLE DATA HANDLING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Інтелектуальна Обробка Даних Kaggle</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>kaggle_loader.py</code> реалізує паттерн **Lazy Loading**. Оскільки архіви Kaggle можуть займати сотні мегабайт, ми не завантажуємо їх у пам'ять повністю. Замість цього система зчитує лише необхідні часові фрагменти та колонки, що дозволяє проводити глибокий аналіз історичних даних навіть на пристроях з обмеженим обсягом RAM.</p>
    </div>
</div>

<!-- SECTION 07: SYSTEM-WIDE LOGGING & DIAGNOSTICS -->
<div class="section-container" id="logger">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Системне Логування та Діагностика</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки <code>logger.py</code> ядро забезпечує повну прозорість операцій. Будь-яка помилка фізичного розрахунку або збій при доступі до даних фіксується з максимальною деталізацією. Це дозволяє команді підтримки ATLAS швидко виявляти вузькі місця в продуктивності та гарантувати надійність системи 24/7.</p>
    </div>
</div>

<!-- SECTION 08: PHYSICS OF POWER FLOWS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Фізика Потокорозподілу</h2></div>
    <div class="glass-card flow-step">
        <p>Ми використовуємо спрощені алгоритми розрахунку потокорозподілу для візуалізації балансу між генерацією та споживанням. Ядро автоматично розраховує надлишкову потужність або її дефіцит, що є базою для роботи модулів прогнозування ШІ та систем сповіщення про критичні стани мережі.</p>
    </div>
</div>

<!-- SECTION 09: CORE INTEGRITY & ATOMICITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Цілісність та Атомарність Ядра</h2></div>
    <div class="glass-card flow-step">
        <p>Всі операції ядра побудовані на принципі атомарності. Ми гарантуємо, що кожна фізична симуляція або запит до даних завершується повністю або не змінює стан системи взагалі. Це критично для підтримки високої наукової достовірності аналітичних звітів та надійності роботи ML-конвеєрів.</p>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v3.0 (DISTRIBUTED KERNEL) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v3.0 (Distributed Kernel)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується перехід на **Розподілене Ядро**, де фізичні розрахунки будуть паралелізуватися між декількома обчислювальними вузлами. Також буде додано підтримку <i>Complex Power Algebra</i> для більш точного моделювання реактивної потужності та впроваджено модуль автоматичної інтеграції з API реальних операторів систем передачі (TSO).</p>
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
