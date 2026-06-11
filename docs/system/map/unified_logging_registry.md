# Технічна специфікація: Реєстр Логування та Аудиту ATLAS (LOGGING REGISTRY GIGA-PASSPORT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM TRACEABILITY & AUDIT | LOGGING REGISTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📜</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Реєстр Логування ATLAS</h1>
            <p class="mega-subtitle">Система тотальної простежуваності: конфігурація багаторівневого логування, ротація файлів, аудит ШІ-рішень та інтеграція з діагностичним центром для розслідування інцидентів</p>
            <div class="status-tags"><span class="tag tag-online">LOGGING ACTIVE</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">SECURITY AUDITOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📑</div><div class="metric-info"><span class="metric-label">Format</span><span class="metric-value">Structured Text / JSON</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Rotation</span><span class="metric-value">Size-based (10MB)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🕵️</div><div class="metric-info"><span class="metric-label">Audit</span><span class="metric-value">Full AI Traceability</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📢</div><div class="metric-info"><span class="metric-label">Output</span><span class="metric-value">Stream + File Sync</span></div></div>
</div>

<!-- SECTION 01: LOGGING PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Логування та Аудиту</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>logging_config.py</code> є "Пам'яттю та Свідком" проекту ATLAS. В системах критичної інфраструктури логування — це не просто запис помилок, а юридично значущий аудит дій та розрахунків. Наша система забезпечує **Повну Простежуваність (Full Traceability)**: від кожного SQL-запиту до кожного рішення нейронної мережі. Це дозволяє не лише швидко виправляти баги, а й проводити ретроспективний аналіз того, чому ШІ видав той чи інший прогноз у конкретній ситуації.</p>
    </div>
</div>

<!-- SECTION 02: LOGGING ARCHITECTURE & STREAMS -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Архітектура логування та потоки</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    APP("Atlas Application Core") --> LOG_MGR("Central Logging Registry")
    LOG_MGR --> STREAM("Console Stream (Colorized)")
    LOG_MGR --> FILE("Rotating File Handlers")
    
    FILE --> SYS_LOG("atlas_system.log (Global)")
    FILE --> AI_LOG("atlas_ai.log (Neural Audit)")
    FILE --> DB_LOG("atlas_db.log (SQL Trace)")
    
    STREAM --> OPERATOR("Real-time CLI Monitoring")
    </div></div>
</div>

<!-- SECTION 03: MULTI-LEVEL LOGGING STRATEGY (📜) -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Багаторівнева стратегія логування</h2></div>
    <div class="glass-card flow-step">
        <p>Ми використовуємо стандартні рівні з кастомними фільтрами для ATLAS:</p>
        <ul>
            <li><b>DEBUG:</b> Деталізація внутрішніх станів моделей та SQL-параметрів. Тільки для розробників.</li>
            <li><b>INFO:</b> Ключові події: старт системи, завантаження нової моделі, зміна підстанції.</li>
            <li><b>WARNING:</b> Відхилення від норми: дрейф моделі ШІ, таймаути БД, високе навантаження RAM.</li>
            <li><b>ERROR/CRITICAL:</b> Аварійні ситуації: втрата зв'язку з БД, відсутність бінарних файлів моделей.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: AUTOMATED LOG ROTATION & RETENTION -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Автоматична ротація та зберігання</h2></div>
    <div class="glass-card flow-step">
        <p>Система самостійно дбає про дисковий простір:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Параметр</th>
                    <th>Значення</th>
                    <th>Обґрунтування</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Max File Size</td><td>10 MB</td><td>Зручність перегляду в текстових редакторах</td></tr>
                <tr><td>Backup Count</td><td>5 Files</td><td>Зберігання історії за останні 48-72 години</td></tr>
                <tr><td>Encoding</td><td>UTF-8</td><td>Коректне відображення кирилиці (назви ПС)</td></tr>
                <tr><td>Propagation</td><td>False</td><td>Уникнення дублювання логів у консолі Streamlit</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: AI INFERENCE AUDIT LOGGING -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Аудит-логування ШІ-рішень</h2></div>
    <div class="glass-card flow-step">
        <p>Окремий потік логування фіксує метадані інференсу: <code>[AI_VERSION] [SUBSTATION] [INPUT_SIG] [RMSE]</code>. Це перетворює "чорну скриньку" нейромережі на прозору систему. У разі аномального прогнозу, аудитор може відкрити <code>atlas_ai.log</code> і побачити, які саме вхідні дані призвели до такого результату, що є критичним для сертифікації системи за стандартами Trustworthy AI.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (LOGGING REGISTRY CORE) -->
<div class="section-number">06</span><h2 class="section-title">Псевдокод ядра реєстру логування</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION setup_atlas_logging():
    1. INIT Formatter: "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    
    2. CREATE RotatingFileHandler("logs/atlas_system.log"):
           maxBytes = 10MB, backupCount = 5
           
    3. CREATE ConsoleHandler(sys.stdout):
           level = INFO, colorize = True
           
    4. REGISTER Loggers:
           'src.ml' -> File + Console
           'src.core.database' -> File (Level: WARNING)
           
    5. RETURN Central_Logger_Instance
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: ERROR TRACEBACK ENRICHMENT -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Збагачення Traceback-звітів</h2></div>
    <div class="glass-card flow-step">
        <p>При виникненні винятків (Exceptions), система логування автоматично збагачує звіт даними про стан середовища: обсяг вільної RAM, версію Python та ID активної сесії користувача. Це дозволяє команді підтримки ATLAS діагностувати проблеми "на льоту" без необхідності доступу до комп'ютера оператора.</p>
    </div>
</div>

<!-- SECTION 08: SECURITY & SENSITIVE DATA MASKING -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Безпека та маскування чутливих даних</h2></div>
    <div class="glass-card flow-step">
        <p>Система логування містить фільтри, які автоматично маскують чутливу інформацію: паролі від БД у Connection Strings та особисті дані користувачів (якщо вони присутні). Це гарантує відповідність проекту вимогам кібербезпеки та захисту персональних даних (GDPR/Закон про захист ПД).</p>
    </div>
</div>

<!-- SECTION 09: DIAGNOSTIC HUB INTEGRATION -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Інтеграція з діагностичним центром</h2></div>
    <div class="glass-card flow-step">
        <p>Логи ATLAS є основним джерелом даних для скрипта <code>diagnose.py</code>. Аналізатор логів сканує файли на наявність патернів критичних помилок та формує фінальний HTML-звіт про "Здоров'я Системи". Таким чином, пасивне логування перетворюється на активну систему попередження аварійних ситуацій.</p>
    </div>
</div>

<!-- SECTION 10: ASYNCHRONOUS LOGGING READINESS -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Готовність до асинхронного логування</h2></div>
    <div class="glass-card flow-step">
        <p>Архітектура реєстру підтримує <b>QueueHandler</b>, що дозволяє винести запис логів на диск в окремий потік. Це гарантує, що операції введення-виведення (I/O) ніколи не стануть "пляшковим горлечком" для основного циклу обчислень ШІ, забезпечуючи максимальну продуктивність додатку.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📜</div>
            <div class="role-content">
                <h4>Python Logging Core</h4>
                <p>Фундаментальна бібліотека обробки потоків подій.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛡️</div>
            <div class="role-content">
                <h4>Error Handlers</h4>
                <p>Головний постачальник структурованих звітів про збої.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🩺</div>
            <div class="role-content">
                <h4>Diagnose Tool</h4>
                <p>Споживач логів для генерації звітів про технічний стан.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (ELK STACK & REAL-TIME ALERTS) -->
<div class="section-container">
    <div class="section-header":"12"></span><h2 class="section-title">Дорожня карта v2.0 (ELK Stack & Real-time Alerts)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується інтеграція з <b>ELK Stack (Elasticsearch, Logstash, Kibana)</b> для централізованого аналізу логів, впровадження <b>Push/Email сповіщень</b> для миттєвих сповіщень адміністратора про Critical-події та підтримка <b>Binary Log Format</b> для екстремально швидкого запису телеметрії.</p>
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
