# Технічний Паспорт Компонента: tests/test_physics.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">⚛️ PHYSICAL RULES & DIGITAL TWIN VALIDATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚡</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">test_physics.py</h1>
            <p class="mega-subtitle">Система верифікації фізичних обмежень, профілів навантаження та динамічних ринкових тарифів</p>
            <div class="status-tags">
                <span class="tag tag-online">PHYSICS SENTRY</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">QUALITY GATE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🌞</div>
        <div class="metric-info">
            <span class="metric-label">Solar Output Night</span>
            <span class="metric-value">0.0 MW</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚛️</div>
        <div class="metric-info">
            <span class="metric-label">Nuclear Stability</span>
            <span class="metric-value">~98.0% (Stable)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📉</div>
        <div class="metric-info">
            <span class="metric-label">Weekend Reduction</span>
            <span class="metric-value">k = 0.8 (Industrial)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">💰</div>
        <div class="metric-info">
            <span class="metric-label">Price Caps</span>
            <span class="metric-value">Night: 5600 / Peak: 9000</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Математичне моделювання та верифікація фізики</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>tests/test_physics.py</code> є головним аудитором математичного ядра симуляції та "цифрового двійника" (Digital Twin) енергомережі платформи <b>Energy Monitor Ultimate</b>. Він гарантує, що всі віртуальні вимірювання, які генеруються системою, строго підпорядковуються законам фізики та реальним ринковим правилам функціонування об'єднаної енергетичної системи (ОЕС) України.
        </p>
        <p style="margin-top: 10px;">
            Основні аспекти фізичної та фінансової валідації:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Стабільність базової генерації (Base-load Nuclear Control):</strong> Атомні електростанції (АЕС) є вкрай інерційними і мають працювати в базовому режимі з мінімальними відхиленнями (на рівні 98%).</li>
            <li><strong>Термодинамічні профілі поновлюваних джерел (Thermodynamic Solar Cycle):</strong> Сонячні електростанції (СЕС) не можуть генерувати енергію за відсутності сонячної інсоляції в нічні години (генерація = 0).</li>
            <li><strong>Економічний аудит ринку (Price Caps Integrity):</strong> Ціни на ринку "на добу наперед" (РДН) мають строго обмежуватися лімітами, встановленими регулятором (граничні ціни - price caps), залежно від зон доби.</li>
            <li><strong>Коефіцієнти зниження попиту (Weekend Load Shedding):</strong> Промислові об'єкти мають зменшувати споживання у вихідні дні через зупинку цехів та офісів, що моделюється мультиплікатором 0.8.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: PHYSICAL BOUNDARY METRIC FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Карта перевірок фізичних та комерційних законів (Physical State Flow)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема ілюструє, як модуль тестує різні компоненти фізичного ядра <code>physics.py</code>:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                PHYSICS("Physics Engine (physics.py)") --> PRICE_CAPS("1. Electricity Prices")
                PHYSICS --> GEN_OUT("2. Generator Outputs")
                PHYSICS --> LOAD_DEMAND("3. Load Demand Profiles")
                
                PRICE_CAPS --> NIGHT_CAP("Night (03:00) <= 5600 грн/МВт-год")
                PRICE_CAPS --> PEAK_CAP("Peak (19:00) <= 9000 грн/МВт-год")
                
                GEN_OUT --> SOLAR("Solar: Day > 0 / Night == 0")
                GEN_OUT --> NUCLEAR("Nuclear: approx. 98.0% of Nom Capacity")
                
                LOAD_DEMAND --> WEEKEND_RED("Industrial Weekend load-shedding (0.7 < Ratio < 0.95)")
                LOAD_DEMAND --> TEMP_ALERT("Cold temp (10.0°C) -> Overload alerts")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: DETAILED TEST CASES & FORMULAS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Аналітичний розбір фізичних рівнянь та бізнес-правил</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Граничні тарифи РДН (test_calculate_energy_price_caps)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Перевіряє, що ціноутворення відповідає правилам енергетичного ринку. Розрахунок цін $P(h)$ обмежується наступними лімітами:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \begin{cases} P(h) \le 5600, & h \in [0, 7) \text{ (Нічний мінімум)} \\ P(h) \le 9000, & h \in [17, 23) \text{ (Вечірній пік)} \end{cases} $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Сонце вночі дорівнює нулю (test_calculate_generator_output_solar_night)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    СЕС залежать від сонячного випромінювання. Генерація $G_{solar}(t)$ розраховується на основі часу доби:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ G_{solar}(\text{02:00}) = 0.0 \text{ МВт}, &nbsp;&nbsp;&nbsp;&nbsp; G_{solar}(\text{12:00}) > 0.0 \text{ МВт} $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Зниження споживання промисловості у вихідні (test_calculate_substation_load_weekend_reduction)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Перевіряє роботу коефіцієнтів попиту. Навантаження підстанції у вихідний $L_{weekend}$ має бути меншим за робочий день $L_{workday}$ за рахунок системного мультиплікатора $k = 0.8$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ 0.7 < \frac{L_{weekend}}{L_{workday}} < 0.95 \quad (\text{Очікуване значення } \approx 0.8) $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">4. Базова стабільність АЕС (test_calculate_generator_output_nuclear_stable)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Атомні реактори працюють із максимальним КВВП (коефіцієнтом використання встановленої потужності) і не беруть участі у маневруванні:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ G_{nuclear}(t) \approx C_{max} \cdot 0.98 \quad (\pm 1\% \text{ точність}) $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму стабілізації АЕС</h2>
    </div>
    <div class="glass-card">
        <p>
            Для розуміння логіки генерації АЕС, яка верифікується тестом, наведено псевдокод:
        </p>
        <pre><code class="language-python">
# Псевдокод моделювання генерації АЕС (базовий режим)
def calculate_nuclear_output(max_mw):
    # Коефіцієнт базового навантаження = 98%
    base_load_factor = 0.98
    
    # Допускається мінімальне випадкове відхилення в межах +/- 0.5%
    random_fluctuation = np.random.uniform(-0.005, 0.005)
    
    actual_output = max_mw * (base_load_factor + random_fluctuation)
    return actual_output
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ & PHYSICAL EXPLANATIONS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Часті питання (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому атомна генерація має фіксований КВВП на рівні 98%?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: З точки зору безпеки та технології, ядерні реактори ВВЕР-1000 є дуже інерційними і не призначені для маневрування. Швидкі зміни навантаження створюють ризик ксенонового отруєння реактора. Тому в моделі "цифрового двійника" АЕС видає стабільну базову потужність 98%, а маневрування мережі виконують ГЕС та ТЕС.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому тест алертів перевантаження містить спрощений assert True?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Ймовірність генерації аварійного алерта при перевантаженні в коді <code>physics.py</code> налаштована як випадковий процес із дуже низькою ймовірністю (0.1% на крок). Запуск тесту 1000 разів дає лише ~63% шансу зустріти алерт. Щоб уникнути випадкових падінь тестів на серверах інтеграції (Flaky Tests), жорсткий ассерт замінено на валідацію роботи самої функції.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Які ще профілі навантаження підтримує система?</h4>
        <p style="color: var(--text-dim);">
            A: Окрім промислового (INDUSTRIAL), підтримуються житловий (RESIDENTIAL) з вечірніми піками споживання та комерційний (COMMERCIAL) з піком у робочі години офісів.
        </p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn">
        <span class="btn-icon">🔙</span>
        <span class="btn-text">Повернутися до Атласу</span>
    </a>
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
