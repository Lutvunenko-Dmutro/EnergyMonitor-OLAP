# Технічна специфікація: Фінансовий Аудит та Аналіз Мережевих Втрат (FINANCIAL & GRID VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ECONOMIC AUDIT | GRID LOSS MODELING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">💰</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Фінансова Аналітика</h1>
            <p class="mega-subtitle">Система моніторингу економічної ефективності енергосистеми: аналіз добової вартості генерації, волатильності цін та фізико-економічного моделювання технічних втрат у мережах</p>
            <div class="status-tags"><span class="tag tag-online">FINANCE ACTIVE</span><span class="tag tag-version">v2.2.0</span><span class="tag tag-role">ECONOMIST-DISPATCHER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Audit</span><span class="metric-value">Daily Generation Cost</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔥</div><div class="metric-info"><span class="metric-label">Volatility</span><span class="metric-value">Pricing Heatmap</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Safety</span><span class="metric-value">Loss Curve Analysis</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Grid</span><span class="metric-value">HVDC / AC Loading</span></div></div>
</div>

<!-- SECTION 01: FINANCIAL VIEW PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Фінансового Аудиту</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>finance.py</code> є економічним "сканером" проекту ATLAS. В умовах ринку електроенергії кожен диспетчерський крок має свою ціну. Наша філософія базується на <b>Фізико-Економічному Синтезі</b>: ми не просто рахуємо гроші, а пов'язуємо їх з фізичним станом ліній електропередач. Розрахунок втрат потужності в реальному часі та їх вартісна оцінка дозволяють приймати рішення, які є не лише технічно надійними, а й економічно оптимальними.</p>
    </div>
</div>

<!-- SECTION 02: FINANCIAL PROCESSING PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр Фінансової Обробки (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    LOAD("Historical Load Data") --> COST("Apply Dynamic Pricing")
    COST --> AGGR_DAILY("Aggregate Daily Cost by Region")
    AGGR_DAILY --> VIS_BAR("Daily Generation Cost (Stacked)")
    
    LOAD --> LOSS("Physics Engine: Loss Calc")
    LOSS --> LINE_TYPE("AC vs HVDC Classification")
    LINE_TYPE --> VIS_LINE("Average Line Loading Trends")
    VIS_LINE --> ALERT("Risk Zone Shading (80-95%)")
    
    COST --> HEAT("Pivot Data (Day vs Hour)")
    HEAT --> VIS_HEAT("Pricing Volatility Heatmap")
    
    LOSS --> VIS_SCAT("Loss Curve (Load vs MW Loss)")
    </div></div>
</div>

<!-- SECTION 03: GRID STABILITY MONITORING (AC/HVDC) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Моніторинг стабільності мереж (AC/HVDC)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль візуалізує навантаження ліній електропередач різних типів:</p>
        <ul>
            <li><b>AC Lines:</b> Стандартні мережі змінного струму. Система відстежує їх завантаження відносно номіналу.</li>
            <li><b>HVDC Segments:</b> Магістральні лінії постійної напруги (High Voltage DC). Візуалізуються окремим фіолетовим кольором через їхню стратегічну важливість.</li>
            <li><b>Risk Zones:</b> Автоматичне затінення областей 80-95% (Warning) та 95-100% (Critical) на графіках дозволяє диспетчеру побачити наближення до межі стійкості ще до спрацювання автоматики.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: ANALYTICAL TOOLS MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця фінансових інструментів</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Інструмент</th>
                    <th>Механізм</th>
                    <th>Аналітичний висновок</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Daily Cost Bar</td><td>Stacked Aggregation</td><td>Економічна вага кожного регіону</td></tr>
                <tr><td>Pricing Heatmap</td><td>Day-Hour Matrix</td><td>Виявлення годин пікових цін</td></tr>
                <tr><td>Loss Scatter</td><td>Physics correlation</td><td>Ефективність передачі потужності</td></tr>
                <tr><td>Loading Splines</td><td>Smooth trends</td><td>Прогнозування перевантажень ЛЕП</td></tr>
                <tr><td>Alert Annotations</td><td>Threshold Triggers</td><td>Миттєве попередження про критичні зони</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: PRICING VOLATILITY HEATMAPS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Теплові карти волатильності цін</h2></div>
    <div class="glass-card flow-step">
        <p>Для аналізу динаміки цін ми використовуємо формат <b>Heatmap</b> (візуалізація через палітру Inferno). Вісь X показує години доби (0-23), а вісь Y — календарні дні. Це дозволяє миттєво ідентифікувати "цінові сплески" (Price Spikes) в пікові години та оцінити стабільність тарифного меню. Такий аналіз допомагає в плануванні режимів роботи гідроакумулюючих станцій (ГАЕС) для максимізації прибутку.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Фінансового Ядра (Finance Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_financial_view(df_fin, df_lines):
    1. PHYSICS: df_lines = physics.calculate_losses(df_lines)
    
    2. TOP_ROW:
           render_cost_bars(df_fin, color_by='region')
           render_loading_lines(df_lines, colors={'AC': blue, 'HVDC': purple})
           
    3. ADD_OVERLAYS: 
           draw_warning_rect(80, 95, color='orange')
           draw_critical_rect(95, 100, color='red')
           
    4. BOTTOM_ROW:
           heat_matrix = df_fin.pivot(day, hour, price)
           render_heatmap(heat_matrix, scale='Inferno')
           render_loss_scatter(df_lines, x='load', y='losses')
           
    5. SPACER: Extra 300px for scroll comfort
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: PHYSICS-BASED LOSS CHARACTERISTICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Фізичні характеристики втрат (Loss Curve)</h2></div>
    <div class="glass-card flow-step">
        <p>За допомогою діаграми розсіювання (Scatter Plot) ми візуалізуємо нелінійну залежність втрат від рівня завантаження. Оскільки втрати пропорційні квадрату струму ($P_{loss} \propto I^2 R$), графік наочно демонструє, чому завантаження ліній понад 80% є вкрай неефективним з економічної точки зору. Це дозволяє диспетчеру обґрунтовано перерозподіляти потоки через менш завантажені гілки мережі.</p>
    </div>
</div>

<!-- SECTION 08: HANDLING DATA CONTINUITY (SAMPLE FILTER) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Забезпечення неперервності даних (Filtering)</h2></div>
    <div class="glass-card flow-step">
        <p>Для уникнення візуальних артефактів на графіках трендів, <code>finance.py</code> реалізує фільтр <b>Sample Count</b>. Якщо для певного дня доступно менше 20 годин телеметрії (що вказує на серйозний збій у зборі даних), цей день виключається з розрахунку середнього значення. Це запобігає появі неправдивих "провалів" навантаження на графіках, які могли б дезінформувати оператора.</p>
    </div>
</div>

<!-- SECTION 09: SMART LEGEND & INTERACTION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Розумна легенда та взаємодія</h2></div>
    <div class="glass-card flow-step">
        <p>Легенди всіх фінансових графіків інтегровані з функціями <b>Item Toggle</b>. Оператор може одним кліком приховати всі AC-лінії, щоб зосередитися тільки на HVDC-магістралях, або відключити певний регіон у стовпчиковій діаграмі вартості. Це забезпечує гнучкість аналізу "від загального до конкретного" без необхідності перевантаження сторінки.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM SPACER & SCROLLING (UX FIX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Комфорт скролінгу (UX Fix)</h2></div>
    <div class="glass-card flow-step">
        <p>У нижній частині фінансової вкладки додано технічний відступ (Spacer) висотою 300 пікселів. Це гарантує, що при перегляді нижніх діаграм (Характеристика втрат та Теплова карта цін), користувач може прокрутити їх до центру екрана для зручного аналізу осей та легенд, уникаючи перекриття інтерфейсом операційної системи.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">⚙️</div>
            <div class="role-content">
                <h4>Physics Engine</h4>
                <p>Розрахунок технічних втрат та класифікація ліній.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Objects</h4>
                <p>Низькорівневий рендеринг теплових карт та бар-чартів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4>UI Helpers</h4>
                <p>Безпечна візуалізація та обробка помилок рендерингу.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (REAL-TIME LOSS PREDICTION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Real-time Loss Prediction)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступній версії планується впровадження <b>Прогнозного аналізу втрат</b>. Система буде використовувати ШІ для передбачення втрат на наступні 24 години на основі прогнозів споживання. Також буде додано підтримку <b>Multi-currency</b> (USD/EUR) та автоматичну інтеграцію з даними енергетичних бірж (Market APIs) для актуалізації тарифів у реальному часі.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Фінанси та Мережі</h2></div>
    <div class="glass-card flow-step">
        <p><b>Як розраховується вартість втрат?</b> — Множенням фізичних втрат (МВт) на актуальну ціну за МВт·год для даного регіону та години.</p>
        <p><b>Чому лінія завантаження іноді вище 100%?</b> — Це свідчить про короткочасні перевантаження, які фіксуються системою як аварійні режими.</p>
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
