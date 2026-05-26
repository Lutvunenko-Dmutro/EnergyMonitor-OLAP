# ⚛️ Технічна специфікація модуля: physics.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SCIENTIFIC CORE | PHYSICS & DIGITAL TWIN SIMULATION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚛️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Математичний Двійник</h1>
            <p class="mega-subtitle">Ядро фізико-математичного моделювання процесів енергосистеми: розрахунок втрат ЛЕП, стабільності балансу, предиктивної діагностики трансформаторів та динамічного ціноутворення НКРЕКП</p>
            <div class="status-tags"><span class="tag tag-online">DIGITAL TWIN ACTIVE</span><span class="tag tag-version">v3.1.0</span><span class="tag tag-role">PHYSICS ENGINE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Grid Losses</span><span class="metric-value">AC & HVDC Models</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚖️</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Real-time GSI Index</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💰</div><div class="metric-info"><span class="metric-label">Tariffs</span><span class="metric-value">НКРЕКП № 949</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Asset Health</span><span class="metric-value">Oil Temp + H2 (DGA)</span></div></div>
</div>

<!-- SECTION 01: ARCHITECTURAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальна Роль та Місія</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>physics.py</code> є науково-теоретичним базисом проєкту <b>ATLAS</b>. Він виконує роль <b>Цифрового Двійника (Digital Twin)</b> фізичної енергосистеми. У той час як ШІ фокусується на трендах споживання, це ядро прораховує фундаментальні закони електрофізики та теплообміну: розраховує активні втрати потужності в провідниках, оцінює ризики перевантаження підстанцій на основі поточної температури навколишнього середовища, проводить віртуальну хроматографію трансформаторного масла (DGA) та виконує економічний розрахунок вартості електроенергії згідно з українським законодавством.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL MODELING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичне Моделювання Фізичних Процесів</h2></div>
    <div class="glass-card flow-step">
        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-bottom: 10px;">1. Розрахунок Активних Втрат Потужності (Закон Джоуля-Ленца)</h3>
        <p>Для AC (змінного струму) ліній теплові втрати в ЛЕП моделюються з урахуванням реактивної складової (косинусу фі):</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fff; margin: 15px 0; border: 1px solid var(--border);">
            P_losses = I^2 * R = ( P_load / (U_grid * cos(φ)) )^2 * R
        </div>
        <p>Де:</p>
        <ul>
            <li><code>P_load</code> — активне навантаження підстанції (МВт).</li>
            <li><code>U_grid</code> — номінальна напруга лінії (кВ).</li>
            <li><code>cos(φ)</code> — коефіцієнт потужності (прийнятий за <code>0.85</code>).</li>
            <li><code>R</code> — активний опір ЛЕП (Ом).</li>
        </ul>

        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-top: 20px; margin-bottom: 10px;">2. Індекс Стабільності Мережі (Grid Stability Index)</h3>
        <p>Індекс стабільності балансу генерації та споживання (GSI) розраховується як відносне відхилення частоти:</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fff; margin: 15px 0; border: 1px solid var(--border);">
            GSI = 1.0 - |P_gen - P_cons| / (P_gen + P_cons)
        </div>
        <p>Якщо <code>GSI < 0.85</code>, система автоматично реєструє аварійний стан загрози віялових відключень.</p>

        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-top: 20px; margin-bottom: 10px;">3. Предиктивне Здоров'я Трансформатора (DGA)</h3>
        <p>Діагностика стану трансформаторів базується на інерційному тепловому балансі та концентрації розчиненого водню в маслі (H2 ppm):</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fff; margin: 15px 0; border: 1px solid var(--border);">
            Health_Index = ω1 * (1 - T_oil / T_max) + ω2 * (1 - C_H2 / C_max)
        </div>
        <p>Коефіцієнти <code>ω1, ω2</code> визначають вагомість термічного старіння та газоутворення.</p>
    </div>
</div>

<!-- SECTION 03: KEY METHODS & API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Сигнатури та Логіка Функцій API</h2></div>
    <div class="glass-card flow-step">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def calculate_line_losses(load_mw, line_type='AC') -> float</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);">Розраховує теплові втрати в ЛЕП. Для ліній AC враховується реактивний опір, для ліній HVDC (постійний струм високої напруги) опір моделюється виключно як активний, що зменшує втрати на 30%.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def estimate_grid_stability(generation, consumption) -> dict</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);">Розрахунок GSI та формування висновку для системи автоматики захисту (Blackout risk level, balance delta).</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def calculate_energy_price(consumption_kwh, price_mode) -> float</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);"><b>Економічний симулятор.</b> Виконує розрахунок вартості за двозонними та тризонними тарифами з урахуванням постанови НКРЕКП № 949 (години пікових коефіцієнтів).</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def calculate_transformer_health(load, ext_temp) -> dict</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);">Моделює внутрішню температуру обмоток трансформатора за диференційним рівнянням теплопередачі в залежності від навантаження та температури повітря.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 04: DIGITAL TWIN PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Конвеєр Обчислень Цифрового Двійника</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA_INPUT("Вхідні дані (Телеметрія / Прогноз ШІ)") --> TEMP_MODEL("Модель погоди (calculate_weather())")
    
    subgraph ENGINE["Physics Engine Simulation"]
        TEMP_MODEL --> LOSSES("Розрахунок втрат ЛЕП")
        TEMP_MODEL --> TRANS_HEALTH("Розрахунок здоров'я трансформаторів")
        TEMP_MODEL --> STABILITY("Оцінка стабільності частоти GSI")
    end
    
    subgraph ECON["Market Layer"]
        STABILITY --> PRICE("Тарифікація НКРЕКП № 949")
    end
    
    PRICE --> OUTPUT("Вихідні метрики Цифрового Двійника")
    TRANS_HEALTH --> OUTPUT
    LOSSES --> OUTPUT
    </div></div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../system/atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
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
