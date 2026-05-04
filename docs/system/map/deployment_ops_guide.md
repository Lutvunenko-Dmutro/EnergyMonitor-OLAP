# Технічна специфікація: Операційне розгортання ATLAS (DEPLOYMENT GIGA-PASSPORT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">OPERATIONS & DEPLOYMENT | INFRASTRUCTURE GUIDE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚀</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Паспорт Розгортання</h1>
            <p class="mega-subtitle">Керівництво з операційної готовності: автоматизація запуску, управління залежностями, конфігурація оточення та стратегія "Health Check" для продуктових інсталяцій</p>
            <div class="status-tags"><span class="tag tag-online">OPS READY</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">DEVOPS ENGINEER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📦</div><div class="metric-info"><span class="metric-label">Packages</span><span class="metric-value">50+ Dependencies</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📜</div><div class="metric-info"><span class="metric-label">Scripts</span><span class="metric-value">PowerShell Autom.</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🐍</div><div class="metric-info"><span class="metric-label">Runtime</span><span class="metric-value">Python 3.10+</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🐘</div><div class="metric-info"><span class="metric-label">Backend</span><span class="metric-value">Neon/Postgres</span></div></div>
</div>

<!-- SECTION 01: DEPLOYMENT PHILOSOPHY (Infrastructure as Code) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Операційної Готовності</h2></div>
    <div class="glass-card flow-step">
        <p>Паспорт розгортання проекту ATLAS розроблений за принципом <b>"Zero-Configuration Start"</b>. Ми мінімізуємо час між клонуванням репозиторію та запуском першого ШІ-прогнозу. Операційна стратегія базується на автоматизації рутинних дій (створення venv, встановлення залежностей, міграції БД) через скрипти запуску. Це гарантує відтворюваність середовища на будь-якій машині — від локального ноутбука розробника до хмарного сервера в ситуаційному центрі.</p>
    </div>
</div>

<!-- SECTION 02: SYSTEM STARTUP FLOW (BOOT SEQUENCE) -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Послідовність завантаження системи</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    PS("START_ATLAS.ps1: Entry Point") --> VENV("VENV Check & Creation")
    VENV --> REQS("pip install -r requirements.txt")
    REQS --> ENV("Check .env & DB Connectivity")
    ENV --> DB_SYNC("Database Migrations (Optional)")
    DB_SYNC --> STREAMLIT("streamlit run main.py")
    STREAMLIT --> HUD("Final HUD Interface Ready")
    </div></div>
</div>

<!-- SECTION 03: DEPENDENCY MANAGEMENT (Requirements.txt) -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Управління залежностями (Requirements)</h2></div>
    <div class="glass-card flow-step">
        <p>Проект ATLAS використовує сучасний стек бібліотек, розділений на 4 ключові домени:</p>
        <ul>
            <li><b>Core Interface:</b> <code>streamlit</code>, <code>plotly</code> — ядро візуалізації та HUD.</li>
            <li><b>Data Engineering:</b> <code>pandas</code>, <code>numpy</code>, <code>sqlalchemy</code>, <code>psycopg2-binary</code> — обробка даних та зв'язок з Postgres.</li>
            <li><b>Machine Learning:</b> <code>scikit-learn</code>, <code>onnxruntime</code> — інференс моделей прогнозування та кластеризації.</li>
            <li><b>Utilities:</b> <code>python-dotenv</code>, <code>requests</code> — системна конфігурація та робота з API (Kaggle).</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: POWERSHELL AUTOMATION (START_ATLAS.ps1) -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Автоматизація PowerShell (START_ATLAS.ps1)</h2></div>
    <div class="glass-card flow-step">
        <p>Скрипт <code>START_ATLAS.ps1</code> виступає інтелектуальним оркестратором розгортання:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Функція</th>
                    <th>Метод</th>
                    <th>Бізнес-перевага</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Ізоляція</td><td>Test-Path .venv</td><td>Запобігання конфліктам системних бібліотек</td></tr>
                <tr><td>Свіжість коду</td><td>pip install --upgrade</td><td>Автоматичне оновлення до останніх патчів</td></tr>
                <tr><td>Оркестрація</td><td>streamlit run</td><td>Єдина точка входу для оператора</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: ENVIRONMENT CONFIGURATION (.env) -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Конфігурація середовища (.env)</h2></div>
    <div class="glass-card flow-step">
        <p>Для успішного запуску система вимагає наявності файлу <code>.env</code> з наступними параметрами:</p>
        <ul>
            <li><code>DATABASE_URL</code>: Повний рядок підключення до Neon/Postgres.</li>
            <li><code>KAGGLE_USERNAME / KEY</code>: Для автоматичного оновлення історичних даних.</li>
            <li><code>DEBUG</code>: Прапор активації розширеного логування для діагностики.</li>
            <li><code>ATLAS_SECRET</code>: Ключ для внутрішнього шифрування та сесій.</li>
        </ul>
    </div>
</div>

<!-- SECTION 06: INFRASTRUCTURE PREREQUISITES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Інфраструктурні передумови</h2></div>
    <div class="glass-card flow-step">
        <p>Мінімальні вимоги до хост-системи:</p>
        <ul>
            <li><b>OS:</b> Windows 10/11 (для .ps1) або Linux з bash-аналогом.</li>
            <li><b>Python:</b> Версія 3.10 або вище (вимагається для сумісності з onnxruntime).</li>
            <li><b>Network:</b> Відкритий порт 8501 (Streamlit) та 5432 (Postgres).</li>
            <li><b>RAM:</b> Мінімум 4GB для стабільної роботи симуляції та ML-моделей.</li>
        </ul>
    </div>
</div>

<!-- SECTION 07: HEALTH CHECK & DIAGNOSTICS STRATEGY -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Стратегія "Health Check" та діагностика</h2></div>
    <div class="glass-card flow-step">
        <p>Після запуску рекомендується виконати модуль <code>diagnose.py</code>. Він автоматично перевірить:</p>
        <ul>
            <li>Доступність бази даних та валідність схеми.</li>
            <li>Наявність усіх ML-артефактів у папці <code>models/</code>.</li>
            <li>Цілісність структури проектних папок та прав доступу.</li>
            <li>Версії ключових бібліотек на відповідність вимогам аудиту.</li>
        </ul>
    </div>
</div>

<!-- SECTION 08: CI/CD INTEGRATION READINESS -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Готовність до CI/CD інтеграції</h2></div>
    <div class="glass-card flow-step">
        <p>Архітектура розгортання повністю готова до автоматизації через <b>GitHub Actions</b> або <b>GitLab CI</b>. Завдяки використанню стандартного <code>requirements.txt</code> та чітких змінних оточення, ATLAS може бути розгорнутий у Docker-контейнері однією командою, що є стандартом для сучасних Enterprise-рішень.</p>
    </div>
</div>

<!-- SECTION 09: LOGGING & MONITORING DURING OPS -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Логування та моніторинг під час роботи</h2></div>
    <div class="glass-card flow-step">
        <p>Усі операції розгортання та запуску транслюються в консоль та дублюються в <code>atlas_ops.log</code>. Це дозволяє системним адміністраторам відстежувати час запуску, помилки підключення до БД та статус ініціалізації симуляції в режимі реального часу, забезпечуючи високий рівень **Observability**.</p>
    </div>
</div>

<!-- SECTION 10: ROLLBACK & RECOVERY PROCEDURES -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Процедури відкату (Rollback) та відновлення</h2></div>
    <div class="glass-card flow-step">
        <p>У разі невдалого оновлення скрипт передбачає механізми відновлення: можливість видалення пошкодженого <code>.venv</code> та його повного перестворення. Для бази даних рекомендується використовувати <b>Point-in-Time Recovery</b> засобами Neon/Postgres, що дозволяє повернути стан мережі на будь-яку секунду до виникнення збою.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📦</div>
            <div class="role-content">
                <h4>PyPI Ecosystem</h4>
                <p>Джерело всіх функціональних бібліотек проекту.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🐚</div>
            <div class="role-content">
                <h4>PowerShell / Bash</h4>
                <p>Інструменти автоматизації середовища виконання.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Neon DB Cloud</h4>
                <p>Основний провайдер керованої бази даних для Atlas.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (DOCKER & K8S) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v2.0 (Docker & Kubernetes)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується впровадження офіційного <b>Docker Image</b> для проекту, створення <b>Helm-чартів</b> для розгортання в Kubernetes та реалізація <b>Auto-scaling</b> аналітичних вузлів залежно від кількості активних сесій операторів.</p>
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
