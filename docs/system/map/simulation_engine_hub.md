# Технічна специфікація: Двигун Симуляції Сенсорів та Телеметрії (SIMULATION ENGINE HUB)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SENSORS SIMULATION | DIGITAL TWIN DATA</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🤖</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Двигун Симуляції</h1>
            <p class="mega-subtitle">Ядро генерації живих даних ATLAS: імітація поведінки сенсорів підстанцій, розрахунок фізичних параметрів та забезпечення Real-time стріму телеметрії для ситуаційного центру</p>
            <div class="status-tags"><span class="tag tag-online">SIMULATOR ACTIVE</span><span class="tag tag-version">v4.1.0</span><span class="tag tag-role">VIRTUAL SENSORS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📡</div><div class="metric-info"><span class="metric-label">Telemetry</span><span class="metric-value">Real-time JSON Stream</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💓</div><div class="metric-info"><span class="metric-label">Frequency</span><span class="metric-value">Dynamic Grid Response</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌡️</div><div class="metric-info"><span class="metric-label">Physics</span><span class="metric-value">Transformer Heat Models</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Multiprocess Lock Control</span></div></div>
</div>

<!-- SECTION 01: MISSION OF VIRTUAL SENSORS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Місія Віртуальних Сенсорів</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/services/simulation/</code> відповідає за створення "живої" атмосфери в системі ATLAS. Оскільки реальні датчики енергосистеми не завжди доступні для розробки, ми створили <b>High-Fidelity Simulator</b>. Він моделює складну взаємодію фізичних величин: як навантаження впливає на температуру масла в трансформаторі, як частота мережі реагує на баланс генерації та споживання, і як накопичуються розчинені гази (H2) при тривалих перевантаженнях. Це дозволяє системі ATLAS функціонувати як повноцінний цифровий двійник енергосистеми.</p>
    </div>
</div>

<!-- SECTION 02: SIMULATION COMPONENTS MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Матриця Компонентів Симуляції</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль</th>
                    <th>Роль у системі</th>
                    <th>Метод генерації</th>
                    <th>Частота оновлення</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>data_generator.py</code></td><td>Генератор профілів</td><td>Probabilistic Modeling</td><td>Статична (Pre-run)</td></tr>
                <tr><td><code>sensors.py</code></td><td>Логіка датчиків</td><td>Differential Equations</td><td>1 Гц (Real-time)</td></tr>
                <tr><td><code>sensors_db.py</code></td><td>Оркестратор стріму</td><td>Multiprocessing Loop</td><td>1 Гц (Real-time)</td></tr>
                <tr><td><code>generator_constants.py</code></td><td>Фізичні ліміти</td><td>Standard Norms</td><td>Static Metadata</td></tr>
                <tr><td><code>live_state_handler.py</code></td><td>Буферизація JSON</td><td>Memory Mapped Access</td><td>Миттєво</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: DIGITAL TWIN PHYSICS FORMULAS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Фізичні формули Цифрового Двійника</h2></div>
    <div class="glass-card flow-step">
        <p>Симуляція базується на наступних математичних моделях:
        <ul>
            <li><b>Температурна інерція:</b> T_next = T_curr + (Load_factor² * k_heat - (T_curr - T_env) * k_cool) * dt.</li>
            <li><b>Генерація H2 (Газоутворення):</b> Rate_H2 = base_rate * exp(alpha * T_oil).</li>
            <li><b>Дрейф частоти:</b> df/dt = (Power_Gen - Power_Load) / Inertia_Constant.</li>
            <li><b>Health Score Decay:</b> dH/dt = -beta * (T_oil > T_limit) * (T_oil - T_limit).</li>
        </ul>
        Ці формули забезпечують реалістичну динаміку станів, що є критичним для тестування систем раннього попередження (Alerting System).</p>
    </div>
</div>

<!-- SECTION 04: REAL-TIME TELEMETRY STREAMING -->
<div class="section-container" id="generator">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Стрімінг Телеметрії в Реальному Часі</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення миттєвої реакції інтерфейсу, симулятор використовує механізм <b>Zero-Latency JSON Buffering</b>. Дані про стан системи записуються в пам'ять кожну секунду. Це реалізовано через атомарні операції запису у <code>live_state.json</code>, що дозволяє UI-фрагментам підхоплювати цей стан без необхідності важких запитів до реляційної бази даних PostgreSQL. Це створює ідеальну чуйність інтерфейсу Situational Awareness.</p>
    </div>
</div>

<!-- SECTION 05: SIMULATION DATA FLOW -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Схема Потоку Даних Симуляції</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    CONST("Constants & Physics Rules") --> SENSOR_LOGIC("sensors.py: Agent Logic")
    SENSOR_LOGIC --> ORCHESTRATOR("sensors_db.py: Main Loop")
    
    subgraph OUTPUT_STREAM["Multi-channel Output"]
        ORCHESTRATOR -- High Frequency --> JSON("live_state.json (HUD)")
        ORCHESTRATOR -- Low Frequency --> DB[("PostgreSQL Archive")]
    end
    
    JSON --> UI("Situational Dashboard")
    DB --> ANALYTICS("Historical Audit")
    </div></div>
</div>

<!-- SECTION 06: SENSOR STATE TRANSITIONS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Діаграма станів: Життєвий цикл сенсора</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
stateDiagram-v2
    [*] --> Off: Initialization
    Off --> Nominal: Start Engine
    Nominal --> Overload: Load > 100%
    Overload --> Nominal: Load Reduction
    Overload --> Critical: T > T_critical
    Critical --> Failure: Sudden Breakdown
    Failure --> Off: Maintenance Reset
    Nominal --> Off: Stop Engine
    </div></div>
</div>

<!-- SECTION 07: PHYSICAL MODELING OF ASSETS -->
<div class="section-container" id="sensors">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Фізичне Моделювання Активів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>sensors.py</code> реалізує цифрові двійники обладнання. Кожна підстанція має свій набір віртуальних датчиків: навантаження, температура масла, концентрація H2, рівень вібрації. Показник <i>Health Score</i> динамічно деградує при роботі в зонах перевантаження, що дозволяє тестувати системи предиктивного обслуговування (Predictive Maintenance). Алгоритми імітують стохастичну природу вимірювань, додаючи невелику похибку до кожного значення.</p>
    </div>
</div>

<!-- SECTION 08: MULTIPROCESS ORCHESTRATION & LOCKS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Багатопроцесорна Оркестрація та Блокування</h2></div>
    <div class="glass-card flow-step">
        <p>Для стабільної роботи симулятор запускається як окремий фоновий процес. Модуль <code>sensors_db.py</code> використовує механізм **Lock-файлів** (через модуль <code>portalocker</code> або системні виклики), щоб запобігти одночасному запуску декількох інстансів генератора. Це гарантує, що лише один процес має право на запис у <code>live_state.json</code>, запобігаючи пошкодженню даних. Система також підтримує "м'яку зупинку" через перехоплення сигналів <code>SIGTERM</code>.</p>
    </div>
</div>

<!-- SECTION 09: FAIL-SAFE OPERATION & RESOURCE MONITORING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Відмовостійкість та Моніторинг Ресурсів</h2></div>
    <div class="glass-card flow-step">
        <p>Симулятор обладнаний системою самодіагностики. Якщо запис у базу даних стає неможливим, двигун продовжує транслювати живий стан у JSON-буфер. Це дозволяє ситуаційному центру бачити поточну картину мережі навіть за умови розриву зв'язку з хмарним сховищем. Після відновлення зв'язку система автоматично синхронізує накопичені в пам'яті дані з архівом.</p>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v5.0 (DISTRIBUTED MULTI-AGENT SIM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v5.0 (Multi-Agent Sim)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 5.0 планується перехід на **Розподілену Мультиагентну Симуляцію**, де кожна підстанція буде окремим автономним агентом з власною логікою поведінки. Також буде додано підтримку <i>Monte Carlo Simulations</i> для розрахунку ймовірностей аварійних відключень та впроваджено модуль імітації кібер-атак на протоколи передачі телеметрії (наприклад, імітація спуфінгу значень напруги) для навчання систем кіберзахисту енергосистеми.</p>
    </div>
</div>

<!-- SECTION 11: SIMULATION TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Технічний FAQ Симуляції</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Як змінити швидкість симуляції?</b><br>
        A: Швидкість регулюється через параметр <code>dt</code> у <code>sensors_db.py</code>. За замовчуванням це 1 секунда реального часу.</p>
        <p><b>Q: Чи можна симулювати аварійне відключення підстанції?</b><br>
        A: Так, для цього достатньо надіслати сигнал через API або змінити статус у <code>live_state.json</code> на <i>Failure</i>.</p>
        <p><b>Q: Як забезпечується реалістичність шумів сенсорів?</b><br>
        A: Ми використовуємо генератори псевдовипадкових чисел з нормальним розподілом, параметри якого налаштовані на основі аналізу реальних приладів обліку.</p>
    </div>
</div>

<!-- SECTION 12: SIMULATION ENGINE GLOSSARY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Глосарій Двигуна Симуляції</h2></div>
    <div class="glass-card flow-step">
        <ul>
            <li><b>Digital Twin:</b> Віртуальна копія фізичного об'єкта, яка імітує його поведінку в реальному часі.</li>
            <li><b>Telemetry Stream:</b> Потік даних від сенсорів, що відображає стан системи в кожний момент часу.</li>
            <li><b>Multiprocessing Lock:</b> Механізм запобігання конфліктам при одночасному доступі декількох процесів до одного ресурсу.</li>
            <li><b>Stochastic Modeling:</b> Метод моделювання, що враховує випадкові фактори та імовірнісні процеси.</li>
        </ul>
    </div>
</div>

<!-- SECTION 14: PROFESSIONAL USAGE GUIDELINES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">14</span><h2 class="section-title">Професійні настанови з використання</h2></div>
    <div class="glass-card flow-step">
        <p>Для максимально ефективної роботи з Симулятором ATLAS рекомендується дотримуватися наступних правил:</p>
        <ul>
            <li><b>Стабільність стріму:</b> Запускайте симулятор на виділеному ядрі CPU для уникнення мікро-затримок у генерації телеметрії.</li>
            <li><b>Масштабування:</b> При додаванні понад 1000 віртуальних сенсорів перемикайте <code>sensors_db.py</code> в режим <i>Async Batching</i>.</li>
            <li><b>Моніторинг:</b> Регулярно перевіряйте розмір файлу <code>live_state.json</code> — він не повинен перевищувати 5МБ для збереження миттєвої реакції UI.</li>
            <li><b>Архівація:</b> Налаштуйте автоматичну очистку застарілих симуляційних логів раз на тиждень.</li>
        </ul>
    </div>
</div>

<!-- SECTION 14: PROFESSIONAL USAGE GUIDELINES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">14</span><h2 class="section-title">Професійні настанови з використання</h2></div>
    <div class="glass-card flow-step">
        <p>Для максимально ефективної роботи з Симулятором ATLAS рекомендується дотримуватися наступних правил:</p>
        <ul>
            <li><b>Стабільність стріму:</b> Запускайте симулятор на виділеному ядрі CPU для уникнення мікро-затримок у генерації телеметрії.</li>
            <li><b>Масштабування:</b> При додаванні понад 1000 віртуальних сенсорів перемикайте <code>sensors_db.py</code> в режим <i>Async Batching</i>.</li>
            <li><b>Моніторинг:</b> Регулярно перевіряйте розмір файлу <code>live_state.json</code> — він не повинен перевищувати 5МБ для збереження миттєвої реакції UI.</li>
            <li><b>Архівація:</b> Налаштуйте автоматичну очистку застарілих симуляційних логів раз на тиждень.</li>
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
