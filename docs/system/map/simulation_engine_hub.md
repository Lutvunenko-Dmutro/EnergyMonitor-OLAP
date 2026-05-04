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
        <p>Пакет <code>src/services/simulation/</code> відповідає за створення "живої" атмосфери в системі ATLAS. Оскільки реальні датчики енергосистеми не завжди доступні для розробки, ми створили <b>High-Fidelity Simulator</b>. Він моделює не просто випадкові числа, а складну взаємодію фізичних величин: як навантаження впливає на температуру масла в трансформаторі, як частота мережі реагує на баланс генерації та споживання, і як накопичуються розчинені гази (H2) при тривалих перевантаженнях.</p>
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
                    <th>Вихідний формат</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>data_generator.py</code></td><td>Генератор профілів</td><td>Статистичні моделі</td><td>DataFrame / CSV</td></tr>
                <tr><td><code>sensors.py</code></td><td>Логіка датчиків</td><td>Фізичні формули</td><td>State Objects</td></tr>
                <tr><td><code>sensors_db.py</code></td><td>Оркестратор стріму</td><td>Multiprocessing</td><td>JSON / SQL</td></tr>
                <tr><td><code>generator_constants.py</code></td><td>Фізичні ліміти</td><td>Domain Constants</td><td>Hyperparameters</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: REAL-TIME TELEMETRY STREAMING -->
<div class="section-container" id="generator">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стрімінг Телеметрії в Реальному Часі</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення миттєвої реакції інтерфейсу, симулятор використовує механізм <b>Zero-Latency JSON Buffering</b>. Дані про стан системи записуються в пам'ять (або швидкий файл <code>live_state.json</code>) кожну секунду, а UI-фрагменти підхоплюють цей стан без необхідності важких запитів до реляційної бази даних. Це створює ілюзію прямого підключення до пульта управління справжньою підстанцією.</p>
    </div>
</div>

<!-- SECTION 04: SIMULATION DATA FLOW -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема Потоку Даних Симуляції</h2></div>
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

<!-- SECTION 05: PHYSICAL MODELING OF ASSETS -->
<div class="section-container" id="sensors">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Фізичне Моделювання Активів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>sensors.py</code> реалізує цифрові двійники (Digital Twins) обладнання. Температура масла розраховується за спрощеною термодинамічною моделлю, де нагрів пропорційний квадрату струму, а охолодження залежить від температури навколишнього середовища. Показник <i>Health Score</i> динамічно деградує при роботі в зонах перевантаження, що дозволяє тестувати системи предиктивного обслуговування.</p>
    </div>
</div>

<!-- SECTION 06: GRID FREQUENCY DYNAMICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Динаміка Частоти Енергомережі</h2></div>
    <div class="glass-card flow-step">
        <p>Симулятор ATLAS моделює глобальну частоту системи (номінал 50.0 Гц). При виникненні дефіциту генерації частота починає падати, що активує алгоритми автоматичного розвантаження. Це дозволяє оператору відпрацьовувати сценарії кризового управління та спостерігати за реакцією автоматики на аномальні режими роботи мережі.</p>
    </div>
</div>

<!-- SECTION 07: MULTIPROCESS ORCHESTRATION & LOCKS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Багатопроцесорна Оркестрація та Блокування</h2></div>
    <div class="glass-card flow-step">
        <p>Для стабільної роботи симулятор запускається як окремий фоновий процес. Модуль <code>sensors_db.py</code> використовує механізм **Lock-файлів**, щоб запобігти одночасному запуску декількох інстансів генератора, що могло б призвести до пошкодження даних у БД. Система також підтримує "м'яку зупинку" (Graceful Shutdown) через обробку системних сигналів.</p>
    </div>
</div>

<!-- SECTION 08: SYNTHETIC LOAD PROFILES (PATTERN ENGINE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Генератор Профілів Навантаження</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>data_generator.py</code> створює еталонні добові графіки. Він враховує "ранковий пік", "денне плато" та "вечірній пік" споживання. Для кожної підстанції додається індивідуальний шумовий компонент, що робить симуляцію статистично достовірною та придатною для навчання AI-моделей розпізнавання образів.</p>
    </div>
</div>

<!-- SECTION 09: FAIL-SAFE OPERATION & RESOURCE MONITORING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Відмовостійкість та Моніторинг Ресурсів</h2></div>
    <div class="glass-card flow-step">
        <p>Симулятор обладнаний системою самодіагностики. Якщо запис у базу даних стає неможливим (наприклад, через втрату зв'язку з хмарою Neon), двигун продовжує транслювати живий стан у JSON-буфер, забезпечуючи роботу HUD-інтерфейсу в режимі "ReadOnly Telemetry", поки зв'язок з архівом не буде відновлено.</p>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v5.0 (DISTRIBUTED MULTI-AGENT SIM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v5.0 (Multi-Agent Sim)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 5.0 планується перехід на **Розподілену Мультиагентну Симуляцію**, де кожна підстанція буде окремим автономним агентом. Також буде додано підтримку <i>Monte Carlo Simulations</i> для розрахунку ймовірностей аварійних відключень та впроваджено модуль імітації кібер-атак на протоколи передачі телеметрії для навчання систем захисту.</p>
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
