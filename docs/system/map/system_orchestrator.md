# Технічна специфікація: Стратегічний Оркестратор Системи (STRATEGIC ORCHESTRATOR)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM ENTRY POINT | COMMAND & CONTROL</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚀</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Головний Контролер</h1>
            <p class="mega-subtitle">Верховний оркестратор проекту ATLAS: управління життєвим циклом додатка, координація гібридних стратегій даних, моніторинг ресурсів (Watchdog) та запуск імерсивного HUD-інтерфейсу</p>
            <div class="status-tags"><span class="tag tag-online">ORCHESTRATOR ACTIVE</span><span class="tag tag-version">v5.0.0</span><span class="tag tag-role">SYSTEM COMMAND</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Security</span><span class="metric-value">Watchdog Sentinel Active</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Execution</span><span class="metric-value">Cloud-Safe Parallelism</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧬</div><div class="metric-info"><span class="metric-label">Strategy</span><span class="metric-value">Hybrid Data Ingestion</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Health</span><span class="metric-value">Auto-GC (380MB Threshold)</span></div></div>
</div>

<!-- SECTION 01: SYSTEM ORCHESTRATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Стратегічного Управління</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>main.py</code> є "Командним містком" та "Серцем" проекту ATLAS. В системах моніторингу реального часу критично важливо мати єдину точку входу, яка координує роботу всіх підсистем. Наша філософія базується на <b>Операційній Стійкості</b>: головний контролер не просто запускає інтерфейс, він готує обчислювальне середовище, обмежує апетити математичних бібліотек для хмарної стабільності та постійно слідкує за здоров'ям пам'яті. Це гарантує, що ATLAS залишається швидким та передбачуваним навіть при пікових навантаженнях, забезпечуючи безперервний доступ до критичної енергетичної аналітики.</p>
    </div>
</div>

<!-- SECTION 02: SYSTEM LIFECYCLE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема життєвого циклу (Startup Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("Entry: python main.py") --> ENV_BOOT("Environment Bootstrapping")
    
    subgraph PRE_FLIGHT["Pre-flight Diagnostics"]
        ENV_BOOT --> THREAD_LOCK("Thread-count Lockdown (Cloud-Safe)")
        THREAD_LOCK --> CACHE_CLEAN("Cache TTL Verification (24h)")
    end
    
    PRE_FLIGHT --> UI_INIT("init_page_config() & Custom CSS")
    UI_INIT --> WATCHDOG("Watchdog: auto_gc(380MB)")
    
    subgraph BOOT_SEQ["Active Boot Sequence"]
        WATCHDOG --> SPLASH("show_boot_sequence() / Splash")
        SPLASH --> DB_VERIFY("get_verified_data() / Handshake")
    end
    
    BOOT_SEQ --> DATA_STRAT("Hybrid Data Strategy Decision")
    DATA_STRAT --> SIDEBAR("Sidebar Render & User Filtering")
    SIDEBAR --> DASHBOARD("render_dashboard_ui() - Main Event Loop")
    </div></div>
</div>

<!-- SECTION 03: CLOUD-SAFE EXECUTION (THREAD LOCKDOWN) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Хмарно-орієнтована стабільність (Thread Lockdown)</h2></div>
    <div class="glass-card flow-step">
        <p>Для роботи в обмежених хмарних контейнерах (напр. Streamlit Community Cloud або Docker-інстанси), <code>main.py</code> примусово обмежує кількість потоків для бібліотек <b>OpenBLAS, MKL та OMP</b> до 1. Це запобігає ефекту "вибуху пам'яті" (Memory Spike), коли математичні операції намагаються захопити всі ресурси сервера, що часто призводить до аварійної зупинки додатку. Така конфігурація робить ATLAS надзвичайно стабільним та "доброзичливим" до ресурсів хостингу.</p>
    </div>
</div>

<!-- SECTION 04: STARTUP PHASE MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця фаз запуску системи</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Фаза</th>
                    <th>Функція / Дія</th>
                    <th>Мета</th>
                    <th>Критичність</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Environment</td><td>os.environ.update</td><td>Запобігання витокам RAM</td><td>Критична</td></tr>
                <tr><td>Diagnostics</td><td>system_startup()</td><td>Очищення кешу та TTL перевірка</td><td>Середня</td></tr>
                <tr><td>Watchdog</td><td>auto_gc(380MB)</td><td>Превентивне звільнення пам'яті</td><td>Висока</td></tr>
                <tr><td>Orchestration</td><td>Hybrid Data Strategy</td><td>Перемикання Live / Kaggle</td><td>Висока</td></tr>
                <tr><td>UI Loop</td><td>render_dashboard_ui</td><td>Рендеринг аналітичного простору</td><td>Максимальна</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: THE WATCHDOG SENTINEL (MEMORY PROTECTION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Вартовий пам'яті (Watchdog Sentinel)</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>main.py</code> інтегровано систему <b>Watchdog Sentinel</b> через функцію <code>auto_gc</code>. Система автоматично проводить збір сміття (Garbage Collection) при досягненні порогу 380 МБ споживання RAM. Це особливо важливо для довготривалих сесій роботи в браузері, де накопичення великих DataFrames та кешу Plotly може сповільнювати систему. Вартовий гарантує плавний UX без необхідності ручного перезавантаження сторінки користувачем.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (ORCHESTRATOR PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Оркестратора (Command Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION main():
    1. INITIALIZE: st.set_page_config(layout="wide")
    2. MONITOR: IF ram_usage > 380MB: RUN garbage_collector()
    3. STYLING: INJECT custom_css (HUD Theme)
    4. BOOTSTRAP:
           IF session_is_new:
               RUN show_boot_sequence() # Animation & Pre-fetch
           ELSE:
               GET data FROM cache_or_db()
    5. STRATEGY:
           IF user_selects_Kaggle:
               SWAP Live_Data WITH Kaggle_Archive (Lazy Load)
    6. FILTER: GET user_params FROM Sidebar
    7. EXECUTE: RUN dashboard_main_loop(data, params)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: HYBRID DATA INGESTION STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Гібридна стратегія завантаження даних</h2></div>
    <div class="glass-card flow-step">
        <p>Оркестратор реалізує унікальний механізм <b>Dynamic Source Swapping</b>. ATLAS може "на льоту" перемикатися між внутрішньою базою симуляції та зовнішніми еталонними архівами Kaggle. <code>main.py</code> координує цей перехід через паттерн <i>Lazy Loading</i>: важкі CSV-файли Kaggle завантажуються в пам'ять тільки тоді, коли користувач явно обирає їх у інтерфейсі, що економить ресурси при старті системи.</p>
    </div>
</div>

<!-- SECTION 08: THE BOOT SEQUENCE & USER EXPERIENCE (UX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Заставка та досвід користувача (Boot Experience)</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення відчуття "преміальності" системи, <code>main.py</code> оркеструє <b>Splash Screen</b> (Заставку) при першому вході. Заставка не тільки створює візуальний ефект, а й приховує за собою важкі процеси "холодного старту": первинне підключення до Neon DB та прогрів кешу. Використання <code>st.session_state["booted"]</code> гарантує, що анімація програється лише один раз за сесію, не дратуючи користувача при кожній зміні фільтрів.</p>
    </div>
</div>

<!-- SECTION 09: PROJECT DIAGNOSTICS & INTEGRITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Діагностика та цілісність проекту</h2></div>
    <div class="glass-card flow-step">
        <p>Перед запуском основного циклу, <code>main.py</code> викликає <code>system_startup()</code>. Це "передпольотна перевірка", яка верифікує стан кешу та оточення. Якщо кеш застарів (>24 години), він автоматично очищується. Такий підхід робить ATLAS <b>Самолікуючою системою (Self-healing)</b>, яка автоматично виправляє потенційні проблеми з тимчасовими файлами, що могли б призвести до відображення застарілих даних.</p>
    </div>
</div>

<!-- SECTION 10: ARCHITECTURAL ROLE AS THE SYSTEM'S "BRAIN" -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Роль як "Мозку" архітектури системи</h2></div>
    <div class="glass-card flow-step">
        <p>В архітектурі ATLAS <code>main.py</code> виконує роль <b>Top-Level Mediator</b>. Він не містить розрахункових формул або SQL-запитів, але він знає, які модулі (Core, Services, UI) повинні бути задіяні в кожен момент часу. Це забезпечує ідеальну розв'язку (Decoupling): ядро може працювати самостійно, але саме оркестратор перетворює набір модулів на цілісний додаток, що є вершиною інженерної думки у проекті Energy Monitor Ultimate.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>System Core</h4>
                <p>Базові механізми завантаження та фільтрації даних.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>UI Segments</h4>
                <p>Візуальні модулі (Sidebar, Dashboard, Splash), що складають обличчя системи.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📡</div>
            <div class="role-content">
                <h4>Utils Toolkit</h4>
                <p>Інструменти логування та критичного моніторингу RAM.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v6.0 (AUTONOMOUS AGENT ORCHESTRATION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v6.0 (Autonomous Orchestration)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 6.0 планується впровадження **Автономного Агента-Оркестратора**. Система зможе самостійно приймати рішення про вивантаження модулів з пам'яті залежно від активності користувача. Також буде додано <b>Multi-session Sync</b> для синхронізації стану між різними вкладками браузера та впроваджено <b>Real-time Health Dashboard</b> для самого оркестратора, щоб адміністратор міг бачити графік споживання ресурсів безпосередньо в HUD-інтерфейсі.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Головний Контролер</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому додаток іноді показує заставку повторно?</b> — Це стається при повному очищенні кешу браузера або перезавантаженні сторінки (F5), коли сесія скидається.</p>
        <p><b>Як змінити поріг очищення пам'яті?</b> — Змініть параметр <code>threshold_mb</code> у виклику <code>auto_gc</code> всередині функції <code>main()</code>.</p>
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
