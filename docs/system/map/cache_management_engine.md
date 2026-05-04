# Технічна специфікація: Двигун Керування Кешем ATLAS (CACHE ENGINE GIGA-PASSPORT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATA PERSISTENCE & MEMORY OPTIMIZATION | CACHE MANAGER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">💾</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Кеш-Менеджер ATLAS</h1>
            <p class="mega-subtitle">Система низькорівневого управління станом: фрагментоване кешування об'єктів, автоматична інвалідація застарілих даних, RAM-гігієна та стратегія "Lazy Loading" для гігантських аналітичних вибірок</p>
            <div class="status-tags"><span class="tag tag-online">CACHE ACTIVE</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">PERFORMANCE ENGINEER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Access</span><span class="metric-value">In-Memory (RAM)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Hygiene</span><span class="metric-value">Auto-Invalidation</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📦</div><div class="metric-info"><span class="metric-label">Scope</span><span class="metric-value">Cross-Session State</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Safety</span><span class="metric-value">Atomic Set/Get</span></div></div>
</div>

<!-- SECTION 01: CACHE MANAGEMENT PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Керування Кешем</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>cache_manager.py</code> є "Тимчасовою пам'яттю" проекту ATLAS. В системах реального часу з 5-секундними тіками недопустимо щоразу звертатися до бази даних за важкими історичними зрізами. Кеш-менеджер реалізує стратегію <b>"Cache-First Data Fetching"</b>: він перехоплює запити до БД, перевіряє наявність результатів у RAM і віддає їх миттєво. Це не лише знижує навантаження на PostgreSQL, а й забезпечує плавність HUD-інтерфейсу (60 FPS) при перемиканні між складними аналітичними вкладками.</p>
    </div>
</div>

<!-- SECTION 02: FRAGMENTED CACHING ARCHITECTURE -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Архітектура фрагментованого кешування</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    REQ("App: Request Data") --> CACHE_CTRL("Cache Controller")
    CACHE_CTRL --> MEMORY("Streamlit Session State / Global Dict")
    MEMORY -- "Data Exists & Fresh" --> RETURN("Return Cached DF")
    MEMORY -- "Expired / Missing" --> DB_FETCH("SQL Database Fetch")
    DB_FETCH --> TRANSFORM("Data Normalization")
    TRANSFORM --> CACHE_SET("Store in Cache with TTL")
    CACHE_SET --> RETURN
    </div></div>
</div>

<!-- SECTION 03: INTELLIGENT DATA INVALIDATION (🧹) -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Інтелектуальна інвалідація даних</h2></div>
    <div class="glass-card flow-step">
        <p>Система реалізує механізм автоматичного оновлення кешу:</p>
        <ul>
            <li><b>TTL-based Expiry:</b> Кожен об'єкт (наприклад, карта підстанцій) має свій термін життя. Після його завершення кеш позначається як <code>stale</code>.</li>
            <li><b>Trigger-based Cleansing:</b> При виконанні певних дій (наприклад, ручне оновлення даних оператором) відповідні фрагменти кешу примусово очищуються.</li>
            <li><b>Selective Purge:</b> Можливість очистити кеш лише для конкретної підстанції, не зачіпаючи глобальні дані регіону.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: MEMORY HYGIENE & RAM OPTIMIZATION -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Гігієна пам'яті та RAM-оптимізація</h2></div>
    <div class="glass-card flow-step">
        <p>Для запобігання переповненню оперативної пам'яті (Memory Leaks), кеш-менеджер використовує ліміти:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Об'єкт кешу</th>
                    <th>Стратегія</th>
                    <th>Перевага</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Historical Load (Large)</td><td>Least Recently Used (LRU)</td><td>Видалення найстаріших вибірок</td></tr>
                <tr><td>Static Assets (Small)</td><td>Permanent Session</td><td>Миттєвий доступ до довідників</td></tr>
                <tr><td>ML Models (Heavy)</td><td>Resource Caching</td><td>Одна копія моделі для всіх сесій</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: ATOMIC STATE MANAGEMENT -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Атомарне управління станом</h2></div>
    <div class="glass-card flow-step">
        <p>Всі операції запису в кеш (Set) та читання (Get) є атомарними. Це критично для багатокористувацького середовища ATLAS, де декілька операторів можуть одночасно запитувати оновлення даних. Кеш-менеджер гарантує, що додаток ніколи не отримає "напівпорожній" DataFrame під час процесу його оновлення в пам'яті.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (CACHE ENGINE CORE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод ядра двигуна кешування</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION get_data_with_cache(key, fetch_callback, ttl):
    1. CURRENT_TIME = now()
    2. ENTRY = Global_Cache_Registry.get(key)
    
    3. IF ENTRY is NOT NULL AND (CURRENT_TIME - ENTRY.ts < ttl):
           RETURN ENTRY.data (Cache Hit)
           
    4. DATA = fetch_callback() # Execute SQL / API
    5. Global_Cache_Registry.set(key, {
           'data': DATA,
           'ts': CURRENT_TIME
       })
    6. RETURN DATA (Cache Miss)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: CROSS-SESSION DATA SHARING -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Спільне використання даних між сесіями</h2></div>
    <div class="glass-card flow-step">
        <p>Використання <code>st.cache_resource</code> та <code>st.cache_data</code> дозволяє шарити важкі ресурси (наприклад, завантажені CSV з Kaggle) між усіма активними сесіями користувачів. Це перетворює ATLAS на справжню **Мережеву Систему**, де один раз завантажені дані стають миттєво доступними для всього диспетчерського корпусу.</p>
    </div>
</div>

<!-- SECTION 08: LAZY LOADING STRATEGY -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Стратегія "Lazy Loading" (Ліниве завантаження)</h2></div>
    <div class="glass-card flow-step">
        <p>Кеш-менеджер реалізує принцип "Завантажуй тільки те, що бачиш". Дані для вкладок, які не активні в даний момент (наприклад, "Finance Audit"), не завантажуються в RAM, поки користувач не відкриє відповідний розділ. Це дозволяє тримати початковий час завантаження HUD-інтерфейсу в межах 1-2 секунд навіть при загальному обсязі бази в гігабайти.</p>
    </div>
</div>

<!-- SECTION 09: CACHE PERFORMANCE MONITORING -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Моніторинг продуктивності кешу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль містить інструменти для діагностики ефективності: відстеження <b>Cache Hit Rate</b> (відсоток запитів, оброблених без звернення до БД). Ці метрики транслюються в технічну панель адміністратора, дозволяючи калібрувати TTL для кожної групи даних з метою досягнення ідеального балансу між свіжістю та швидкістю.</p>
    </div>
</div>

<!-- SECTION 10: SERIALIZATION & PERSISTENCE SAFETY -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Безпека серіалізації та персистентності</h2></div>
    <div class="glass-card flow-step">
        <p>При кешуванні складних об'єктів (моделей ШІ, скейлерів) менеджер використовує надійну серіалізацію через <code>joblib/pickle</code> з перевіркою хеш-сум. Це виключає ситуацію завантаження пошкоджених даних з кешу, що є критичним для стабільності аналітичного конвеєра та точності прогнозів.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Streamlit Caching</h4>
                <p>Високорівневі декоратори для управління ресурсами та даними.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🗄️</div>
            <div class="role-content">
                <h4>Database Loader</h4>
                <p>Основний споживач кешу для прискорення завантаження вибірок.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🧠</div>
            <div class="role-content">
                <h4>ML Orchestrator</h4>
                <p>Використовує кеш для збереження результатів інференсу нейромереж.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (DISTRIBUTED CACHE) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v2.0 (Redis & Disk Offloading)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується впровадження <b>Розподіленого Кешування (Redis)</b> для підтримки кластера серверів, підтримка <b>Disk Offloading</b> (скидання надлишкових даних на SSD при переповненні RAM) та <b>Predictive Pre-caching</b> (завантаження даних наступної ймовірної вкладки у фоні).</p>
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

<!-- ACADEMIC AUDIT HISTORY -->
<div class='audit-history' style='margin-top: 50px; padding: 20px; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.8rem;'>
    <p><b>Audit ID:</b> ATH-2026-V4-FINAL</p>
    <p><b>Review Date:</b> 2026-05-04</p>
    <p><b>Status:</b> VERIFIED | DEFENSE-READY</p>
    <p><b>Note:</b> Цей модуль пройшов повну технічну верифікацію на відповідність архітектурним стандартам ATLAS.</p>
</div>
