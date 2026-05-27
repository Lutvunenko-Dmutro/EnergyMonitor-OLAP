# Технічна специфікація модуля: sensors.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">VIRTUAL HARDWARE INSTRUMENTATION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔬</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Virtual Sensor Engine: sensors</h1>
            <p class="mega-subtitle">Програмна імітація фізичних датчиків高вольтного обладнання за законами фізики: Закон Ома, теплова інерція, хімічна деградація масла.</p>
            <div class="status-tags"><span class="tag tag-online">PHYSICS SIMULATION</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">DIGITAL TWIN</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Voltage</span><span class="metric-value">Ohm's Law Drop</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌡️</div><div class="metric-info"><span class="metric-label">Thermal</span><span class="metric-value">Inertia Modeling</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧪</div><div class="metric-info"><span class="metric-label">H2 ppm</span><span class="metric-value">Oil Degradation Model</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🏥</div><div class="metric-info"><span class="metric-label">Health</span><span class="metric-value">Composite Score</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>sensors.py</b> моделює поведінку реальних датчиків SCADA-систем без будь-якого зовнішнього обладнання. Його головна ідея — <b>Physical Realism</b>: кожен параметр розраховується не випадково, а за формулами.</p>
        <p style="margin-top: 12px;"><b>Теплова інерція:</b> трансформатор не може миттєво нагрітися — кожен цикл температура наближається до цільової зі швидкістю 0.15°C. <b>Закон Ома:</b> напруга падає пропорційно навантаженню. <b>Хімічна деградація:</b> якщо температура олії > 80°C, виділяється водень (H2). <b>Health Score:</b> комплексний індекс, що знижується при перегріві та надлишку H2, відображаючи реальний стан трансформатора.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@dataclass class SensorReading</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Контейнер даних одного знімку датчика: <code>sensor_id</code>, <code>timestamp</code>, <code>voltage_kv</code>, <code>frequency_hz</code>, <code>current_a</code>, <code>temperature_c</code>, <code>active_power_mw</code>, <code>load_pct</code>, <code>h2_ppm</code>, <code>health_score</code>, <code>status</code>.</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>class VirtualHighVoltageSensor(sensor_id, sub_type="330kV")</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Симулятор одного датчика. Ініціалізується з реалістичними параметрами Укренерго: <code>330kV → 200-500 МВт</code> або <code>110kV → 40-125 МВт</code>. Зберігає внутрішній стан між читаннями.</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def read_telemetry() → SensorReading</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Симулює один цикл знімку. 1. Оновлює частоту (±0.015 Hz normalvariate). 2. Дрейфує навантаження (±0.03). 3. Рахує напругу (Ом). 4. Оновлює температуру (теплова інерція 0.15). 5. Якщо temp > 80 → H2 +=. 6. Рахує <code>health</code> та <code>status</code>. Повертає <code>SensorReading</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Фізична Модель Датчика</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("read_telemetry()") --> FREQ("freq = 50 + normalvariate(0, 0.015)")
    FREQ --> LOAD("load_pct += normalvariate(0, 0.03)\nclip(0.1..1.3)")
    LOAD --> VOLT("voltage = V_nominal - load_pct * 3.5\nOhm's Law Drop")
    VOLT --> TEMP("target = 20 + load_pct * 65\nself.temp += 0.15 if below target")
    TEMP --> H2{"temp > 80?"}
    H2 -->|Yes| H2_ADD("h2_level += uniform(0.1, 0.5)\nChemical degradation")
    H2 -->|No| HEALTH("health = 100\n- (temp - 75) if temp > 75\n- h2/20 if h2 > 100")
    H2_ADD --> HEALTH
    HEALTH --> STATUS("status = OK/WARNING/CRITICAL\nbased on health & temp")
    STATUS --> RETURN("Return SensorReading()")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>random (normalvariate, uniform, choice)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>dataclasses (dataclass)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime</span>
        </div>
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
