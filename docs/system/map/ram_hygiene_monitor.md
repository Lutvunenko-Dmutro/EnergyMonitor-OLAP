# Технічна специфікація: Монітор Гігієни RAM ATLAS (RAM HYGIENE GIGA-PASSPORT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">MEMORY MANAGEMENT & WATCHDOG | RAM HYGIENE MONITOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🩺</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Монітор Гігієни RAM</h1>
            <p class="mega-subtitle">Система захисту ресурсів: відстеження споживання пам'яті (RSS/VMS), превентивне очищення сміття (GC), Watchdog-контроль витоків та автоматична стабілізація сесій оператора</p>
            <div class="status-tags"><span class="tag tag-online">WATCHDOG ACTIVE</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">RESOURCES MANAGER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Tracking</span><span class="metric-value">Real-time RSS</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Action</span><span class="metric-value">Force GC Collection</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚨</div><div class="metric-info"><span class="metric-label">Alert</span><span class="metric-value">Critical Threshold</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Memory Watchdog</span></div></div>
</div>

<!-- SECTION 01: MEMORY HYGIENE PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Гігієни Пам'яті</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>memory_helper.py</code> є "Санітаром" проекту ATLAS. В Streamlit-додатках, які працюють з великими ML-моделями та SQL-вибірками, пам'ять є найкритичнішим ресурсом. Філософія монітора базується на **Превентивному Управлінні**: замість очікування падіння системи через OOM (Out of Memory), Watchdog постійно аналізує профіль споживання і вживає заходів щодо очищення RAM до того, як ситуація стане критичною. Це гарантує аптайм системи 24/7 у диспетчерських центрах.</p>
    </div>
</div>

<!-- SECTION 02: MEMORY PROTECTION PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр захисту пам'яті</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    MONITOR("RSS Tracking (psutil)") --> EVAL{"Threshold Check"}
    EVAL -- "Memory Safe" --> SLEEP("Wait for next Tick")
    EVAL -- "Warning Level" --> GC_COLLECT("Manual Garbage Collection")
    EVAL -- "Critical Level" --> PURGE("Purge System Cache")
    PURGE --> LOG("Critical Log & Alert")
    GC_COLLECT --> SLEEP
    SLEEP --> MONITOR
    </div></div>
</div>

<!-- SECTION 03: RSS & VMS TRACKING STRATEGY (📊) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія відстеження RSS та VMS</h2></div>
    <div class="glass-card flow-step">
        <p>Монітор використовує бібліотеку <code>psutil</code> для отримання точного профілю процесу:</p>
        <ul>
            <li><b>RSS (Resident Set Size):</b> Реальна фізична пам'ять, яку займає ATLAS у RAM. Головний показник для аляртів.</li>
            <li><b>VMS (Virtual Memory Size):</b> Загальний обсяг віртуальної пам'яті. Використовується для детекції аномального резервування ресурсів ОС.</li>
            <li><b>Memory Percent:</b> Частка RAM від загального обсягу пам'яті сервера, що дозволяє системі бути "ввічливою" до інших процесів.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: AUTOMATED GARBAGE COLLECTION (GC) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Автоматичне збирання сміття (GC)</h2></div>
    <div class="glass-card flow-step">
        <p>Python має вбудований GC, але для ATLAS реалізовано примусове керування:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Тип події</th>
                    <th>Дія Watchdog</th>
                    <th>Результат</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Tab Switch</td><td>gc.collect() call</td><td>Звільнення пам'яті від попередньої візуалізації</td></tr>
                <tr><td>Model Reload</td><td>Object deletion + GC</td><td>Уникнення дублювання ваг нейромережі в RAM</td></tr>
                <tr><td>Periodic Tick</td><td>Incremental cleanup</td><td>Підтримка стабільного "плато" споживання</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: MEMORY LEAK DETECTION LOGIC -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Логіка детекції витоків пам'яті</h2></div>
    <div class="glass-card flow-step">
        <p>Монітор аналізує <b>тренд споживання</b>. Якщо після кожного оновлення даних обсяг RAM не повертається до базового рівня (Base Line), система фіксує потенційний витік (Memory Leak). Watchdog логує імена об'єктів-кандидатів на витік, що дозволяє розробникам швидко ідентифікувати некоректно закриті з'єднання БД або незнищені об'єкти Plotly-фігур.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (RAM MONITOR CORE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод ядра монітора пам'яті</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION monitor_ram_hygiene():
    1. CURRENT_RSS = psutil.Process().memory_info().rss / 1024^2
    2. LOG_DEBUG(f"Current Memory Usage: {CURRENT_RSS} MB")
    
    3. IF CURRENT_RSS > CONFIG.MEM_WARNING_MB:
           FORCE_GC_COLLECTION()
           CLEAR_TEMP_UI_CACHE()
           
    4. IF CURRENT_RSS > CONFIG.MEM_CRITICAL_MB:
           LOG_CRITICAL("OOM RISK! Emergency Cache Purge...")
           App.CacheManager.clear_all()
           NOTIFY_OPERATOR("System slowing down due to memory pressure")
           
    5. RETURN Health_Status
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: FRAGMENT-BASED MEMORY RELEASE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Фрагментоване вивільнення пам'яті</h2></div>
    <div class="glass-card flow-step">
        <p>Утиліти реалізують метод <b>"Memory Pinning"</b> для критичних структур. Ми примусово тримаємо в пам'яті лише активний аналітичний контекст. Дані підстанцій, які не відображаються у поточному фрагменті Streamlit (через <code>@st.fragment</code>), активно вимиваються з пам'яті, що дозволяє працювати з мега-датасетами навіть на офісних ноутбуках з 8GB RAM.</p>
    </div>
</div>

<!-- SECTION 08: INTEGRATION WITH SYSTEM STATUS HUD -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Інтеграція з системним HUD-статусом</h2></div>
    <div class="glass-card flow-step">
        <p>Дані монітора RAM транслюються безпосередньо в UI-заголовок ATLAS у вигляді мікро-індикатора (🩸/🟢). Оператор завжди бачить "навантаження на мозок" системи. Якщо індикатор стає червоним, це сигнал не відкривати занадто багато важких звітів одночасно, що підвищує культуру експлуатації складного ПЗ.</p>
    </div>
</div>

<!-- SECTION 09: CACHE-DEPENDENT CLEANUP STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Стратегія очищення залежного кешу</h2></div>
    <div class="glass-card flow-step">
        <p>Монітор тісно інтегрований з <code>cache_manager.py</code>. При критичному навантаженні Watchdog не просто просить GC зібрати сміття, а примусово інвалідує найстаріші записи в кеші (LRU - Least Recently Used). Це звільняє пам'ять від даних, до яких оператор не звертався останні 30 хвилин, забезпечуючи пріоритет для поточних розрахунків.</p>
    </div>
</div>

<!-- SECTION 10: AUTOMATED SESSION STABILIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Автоматична стабілізація сесій</h2></div>
    <div class="glass-card flow-step">
        <p>У разі виявлення критичного розростання пам'яті в конкретній сесії браузера (через накопичення станів), монітор може ініціювати <b>Soft Reload</b> для цієї сесії. Це скидає внутрішні буфери Streamlit, повертаючи споживання RAM до початкового рівня без втрати користувачем поточного контексту роботи.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">⚙️</div>
            <div class="role-content">
                <h4>Psutil Engine</h4>
                <p>Низькорівневий інтерфейс взаємодії з системними ресурсами ОС.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🗑️</div>
            <div class="role-content">
                <h4>Garbage Collector</h4>
                <p>Стандартний механізм Python для управління життєвим циклом об'єктів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>Cache Manager</h4>
                <p>Споживач команд Watchdog на примусове очищення RAM.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (RAM-AWARE ML INFERENCE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v2.0 (RAM-Aware ML Inference)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується впровадження <b>RAM-Aware Inference</b> (автоматичне зниження точності/глибини прогнозу при дефіциті пам'яті), підтримка <b>Memory Swap Alerts</b> та інтеграція з <b>Docker Resource Quotas</b> для автоматичного масштабування контейнерів.</p>
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
