# Технічна специфікація модуля: services/simulation/sensors.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">VIRTUAL HARDWARE INSTRUMENTATION | PHYSICS-BASED SENSING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📡</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Сервіс Віртуальних Сенсорів</h1>
            <p class="mega-subtitle">Імітація фізичних датчиків високовольтного обладнання: закони Ома та Джоуля-Ленца, теплова інерція трансформаторів та хімічна деградація масла</p>
            <div class="status-tags"><span class="tag tag-online">SENSORS ACTIVE</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">HARDWARE SIMULATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📐</div><div class="metric-info"><span class="metric-label">Logic</span><span class="metric-value">Physical Laws</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌡️</div><div class="metric-info"><span class="metric-label">Thermal</span><span class="metric-value">Inertia Modeling</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚛️</div><div class="metric-info"><span class="metric-label">Chemical</span><span class="metric-value">H2 Dissolution</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚦</div><div class="metric-info"><span class="metric-label">State</span><span class="metric-value">Operational Logic</span></div></div>
</div>

<!-- SECTION 01: VIRTUAL HARDWARE INSTRUMENTATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Віртуального Приладобудування</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>sensors.py</code> є "Нервовими закінченнями" проекту ATLAS. Для створення повноцінного Цифрового Двійника недостатньо просто генерувати навантаження — потрібно імітувати відгук фізичного заліза. Сервіс реалізує програмні датчики, які поводяться як реальні пристрої SCADA: напруга падає під навантаженням, трансформатор повільно гріється (інерція) і так само повільно остигає, а критичний перегрів запускає незворотні хімічні процеси виділення газів. Це забезпечує глибину симуляції, необхідну для предиктивної аналітики.</p>
    </div>
</div>

<!-- SECTION 02: SENSOR READING ARCHITECTURE (DATACLASS) -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Архітектура структури даних сенсора</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    RAW("Raw Physics Calc") --> STRUCT("SensorReading Dataclass")
    STRUCT --> VOLT("Voltage (kV)")
    STRUCT --> FREQ("Frequency (Hz)")
    STRUCT --> POW("Active Power (MW)")
    STRUCT --> TEMP("Oil Temp (°C)")
    STRUCT --> HEALTH("Health Score (%)")
    STRUCT --> STATUS("Status (OK/WARN/CRIT)")
    </div></div>
</div>

<!-- SECTION 03: PHYSICAL LAW SIMULATION (OHM'S LAW) -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Симуляція фізичних законів (Voltage & Load)</h2></div>
    <div class="glass-card flow-step">
        <p>Датчик не просто повертає константи, він обчислює взаємозалежні параметри:</p>
        <ul>
            <li><b>Voltage Drop:</b> Напруга розраховується з урахуванням падіння під навантаженням (<code>nominal - load_pct * 3.5</code>), що імітує реальну поведінку ліній електропередач.</li>
            <li><b>Frequency Wobble:</b> Частота імітується як нормальний розподіл навколо 50 Гц (<code>normalvariate(0, 0.015)</code>), відображаючи постійну динамічну рівновагу генерації та споживання.</li>
            <li><b>Current Calculation:</b> Струм (А) виводиться математично з повної потужності та напруги з урахуванням коефіцієнта потужності (cos φ = 0.9).</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: THERMAL INERTIA & CHEMICAL DEGRADATION -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Теплова інерція та хімічна деградація</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль реалізує "Пам'ять заліза" через стан об'єкта <code>VirtualHighVoltageSensor</code>:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Феномен</th>
                    <th>Математична модель</th>
                    <th>Ефект у симуляції</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Теплова інерція</td><td>+= 0.15 (heat) / -= 0.05 (cool)</td><td>Трансформатор остигає в 3 рази повільніше, ніж гріється</td></tr>
                <tr><td>H2 Level</td><td>Cumulative + random(0.1, 0.5) if Temp > 80</td><td>Незворотне накопичення газів при перегріві</td></tr>
                <tr><td>Health Decay</td><td>Threshold-based subtraction</td><td>Зниження надійності при виході за межі 75°C</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: OPERATIONAL STATUS LOGIC -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Логіка операційних статусів</h2></div>
    <div class="glass-card flow-step">
        <p>На основі зібраних фізичних параметрів датчик автоматично визначає свій стан (Fuzzy Logic):</p>
        <ul>
            <li><b>OK:</b> Здоров'я > 85% та температура в межах норми.</li>
            <li><b>WARNING:</b> Здоров'я 60-85%. Потребує планового огляду.</li>
            <li><b>CRITICAL:</b> Здоров'я < 60% або температура > 95°C. Ризик термічного пробою та пожежі.</li>
        </ul>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (VIRTUAL SENSOR CORE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод ядра віртуального сенсора</h2></div>
    <div class="glass-card flow-step">
        <pre><code>CLASS VirtualHighVoltageSensor:
    1. INIT: SET nominal_mw, nominal_voltage (330/110kV)
    
    FUNCTION read_telemetry():
        # A. Update base physics
        frequency = 50.0 + normal_noise
        load_pct = current_load + noise
        
        # B. Calculate voltage drop
        voltage = nominal - (load_pct * loss_factor)
        
        # C. Process Thermal Inertia
        target_t = 20 + (load_pct * 65)
        IF current_temp < target_t: current_temp += 0.15 # Heating
        ELSE: current_temp -= 0.05 # Cooling
        
        # D. Chemical degradation
        IF current_temp > 80: h2_level += accumulation_rate
        
        # E. Asset Health scoring
        health = 100 - temp_penalty - h2_penalty
        
        RETURN SensorReading(all_calculated_values, status)
END CLASS</code></pre>
    </div>
</div>

<!-- SECTION 07: NOMINAL CAPACITY STANDARDS (UKRENERGO) -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Стандарти номінальної потужності (Укренерго)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль використовує реальні галузеві стандарти для ініціалізації об'єктів. Для <b>330 кВ</b> підстанцій вибираються потужності 200/250/400/500 МВт, а для <b>110 кВ</b> — 40/63/125 МВт. Це робить вихідні дані сенсорів валідними для професійної експертизи енергетиками.</p>
    </div>
</div>

<!-- SECTION 08: HIGH-PRECISION FLOATING POINT EXPOSURE -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Експозиція високоточних даних</h2></div>
    <div class="glass-card flow-step">
        <p>Всі вихідні дані округлюються до специфічних для галузі значень: частота до 3 знаків (0.001 Гц), напруга та потужність до 2 знаків, температура до 1 знака. Це імітує розрядність АЦП реальних мікропроцесорних пристроїв захисту та автоматики.</p>
    </div>
</div>

<!-- SECTION 09: MULTI-REGION TEMPERATURE MAP SYNC -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Синхронізація регіональної температури</h2></div>
    <div class="glass-card flow-step">
        <p>Датчик не працює у вакуумі — він враховує "температуру навколишнього середовища" як базу для розрахунку перегріву трансформатора. Це дозволяє симулювати сезонні ефекти: літню спеку, яка ускладнює охолодження, та зимові морози, які дозволяють тримати вищі навантаження без ризику деградації.</p>
    </div>
</div>

<!-- SECTION 10: PERSISTENT SENSOR STATE (STATEFUL) -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Станний сенсор: Збереження пам'яті</h2></div>
    <div class="glass-card flow-step">
        <p>Об'єкт сенсора зберігає свій стан (<code>_current_temp</code>, <code>_h2_level</code>) протягом всього часу роботи процесу симуляції. Це дозволяє будувати безперервні графіки, де фізичні параметри плавно еволюціонують, а не стрибають хаотично, що є критично важливим для навчання нейромереж прогнозуванню відмов.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Data Classes</h4>
                <p>Стандартний контейнер для передачі структурованих телеметричних вимірювань.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🎲</div>
            <div class="role-content">
                <h4>Random NormalVariate</h4>
                <p>Імітація стохастичних шумів фізичного світу та вимірювальних систем.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🕰️</div>
            <div class="role-content">
                <h4>DateTime</h4>
                <p>Маркування кожного заміру точним часовим штампом для аналітики.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (ELECTROMAGNETIC HARMONICS) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v2.0 (Harmonics & Weather Impact)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується впровадження <b>Гармонійного аналізу</b> (симуляція нелінійних спотворень струму), врахування <b>швидкості вітру</b> для розрахунку конвекційного охолодження трансформаторів та підтримка <b>симуляції коротких замикань</b> з імітацією спрацювання захисної автоматики.</p>
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
