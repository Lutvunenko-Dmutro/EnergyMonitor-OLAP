# Технічна специфікація модуля: data_generator.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CONTINUOUS DIGITAL TWIN</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Simulation Engine: data_generator</h1>
            <p class="mega-subtitle">Ядро системи для імітації роботи енергомережі в режимі реального часу. Підтримує безперервну генерацію телеметрії з симуляцією зносу активів (H2, Temperature).</p>
            <div class="status-tags"><span class="tag tag-online">REAL-TIME DAEMON</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">STATEFUL SIMULATION</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Loop</span><span class="metric-value">Infinite While (time.sleep)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌡️</div><div class="metric-info"><span class="metric-label">Physics</span><span class="metric-value">Stress Modeling</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">State</span><span class="metric-value">In-Memory Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📡</div><div class="metric-info"><span class="metric-label">Data</span><span class="metric-value">SQL Streaming</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>На відміну від <code>db_seeder</code> (який генерує минуле масивами), <b>data_generator.py</b> живе в теперішньому часі (Live Mode). Це "серцебиття" додатку.</p>
        <p style="margin-top: 12px;">Він тримає в пам'яті стан кожної підстанції (скільки було навантаження секунду тому, який був рівень здоров'я). Кожні 5 секунд він обчислює нові значення навантаження, зносу (H2 ppm, Temp), та записує їх у базу, імітуючи надходження реальних IoT-метрик. Дані, згенеровані цим модулем, відразу ж з'являються на графіках у Live-вкладках.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def run_realtime_sensors(sub_profiles: dict, current_temps: dict) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Точка входу в нескінченний цикл симуляції. Спочатку викликає <code>_init_sensor_state</code> для відновлення контексту (передається з seeder-а). Потім крутиться у <code>while True:</code>. Якщо змінилася година — перераховує погоду (<code>calculate_weather</code>). Потім викликає <code>_process_sensor_tick</code> та засинає на 5 секунд.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _process_sensor_tick(substations, sub_profiles, previous_factors, current_health, weather_map, now, is_weekend) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Ітерація симуляції для всіх підстанцій. Обчислює базове навантаження через фізичні модулі. Штучно додає шум (Random) до показників температури масла (<code>temperature_c</code>) та розчиненого газу (<code>h2_ppm</code>). Знижує <code>health_score</code>, якщо параметри виходять за норму. Виконує серію одиничних <code>INSERT INTO LoadMeasurements</code> з поточним <code>now()</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Життєвий цикл Digital Twin</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("run_realtime_sensors()") --> INIT("_init_sensor_state()\nLoad memory dicts")
    
    INIT --> LOOP_WHILE("while True:")
    
    LOOP_WHILE --> TIME{"Hour Changed?"}
    TIME -->|Yes| WX("calculate_weather()")
    TIME -->|No| TICK("_process_sensor_tick()")
    WX --> TICK
    
    TICK --> CALC("Physics: Add random noise\nto H2 & Temp. Decrease Health")
    CALC --> DB("cursor.execute(INSERT)\nLive SQL stream")
    
    DB --> SLEEP("time.sleep(5)")
    SLEEP --> LOOP_WHILE
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>time</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>random</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database (get_db_cursor)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.physics (calculate_substation_load, calculate_weather)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.services.data.db_seeder (generate_professional_data - for standalone start)</span>
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
