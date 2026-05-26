# Технічна специфікація: Фінансовий Аудит та Аналіз Мережевих Втрат (FINANCIAL & GRID VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ECONOMIC AUDIT | GRID LOSS MODELING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">💰</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Фінансова Аналітика</h1>
            <p class="mega-subtitle">Економічний монітор та двигун фізико-економічного моделювання: аналіз вартості генерації, волатильності цін та розрахунок технічних втрат у мережах</p>
            <div class="status-tags"><span class="tag tag-online">FINANCE ACTIVE</span><span class="tag tag-version">v2.2.0</span><span class="tag tag-role">ECONOMIST-DISPATCHER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Audit</span><span class="metric-value">Daily Cost Stacked</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔥</div><div class="metric-info"><span class="metric-label">Volatility</span><span class="metric-value">Pricing Heatmap</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Safety</span><span class="metric-value">Loss Curve Model</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Grid</span><span class="metric-value">HVDC / AC Loading</span></div></div>
</div>

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Фінансового Аудиту</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>finance.py</code> є економічним "сканером" проєкту ATLAS. В умовах ринку електроенергії кожен диспетчерський крок має свою ціну. Наша філософія базується на <b>Фізико-Економічному Синтезі</b>: ми не просто рахуємо гроші, а пов'язуємо їх з фізичним станом ліній електропередач (ЛЕП). Розрахунок втрат потужності в реальному часі та їх вартісна оцінка дозволяють приймати рішення, які є не лише технічно надійними, а й економічно оптимальними.</p>
    </div>
</div>

<!-- SECTION 02: PHYSICAL & ECONOMIC FORMULAS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Фізико-математичні основи розрахунків</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль об'єднує економічний облік та фізичні закони передачі енергії:</p>
        
        <h4>1. Добова вартість генерації ($C_{\text{total}}$)</h4>
        <p>Розраховується шляхом інтегрування погодинного споживання та динамічного тарифу для кожного регіону:</p>
        $$C_{\text{total}} = \sum_{t \in D} P_{\text{load}, t} \times Price_{t} \times \Delta t$$
        <p>де $P_{\text{load}, t}$ — потужність навантаження (МВт) у годину $t$, $Price_{t}$ — ціна електроенергії (грн/МВт·год), а $\Delta t = 1 \text{ година}$.</p>

        <h4>2. Технічні втрати потужності в лініях ($P_{\text{loss}}$)</h4>
        <p>Фізичні втрати в провідниках пропорційні квадрату сили струму $I$, що протікає через лінію з активним опором $R$:</p>
        $$P_{\text{loss}} = I^2 R = \left(\frac{P_{\text{trans}}}{U \sqrt{3} \cos\phi}\right)^2 R \implies P_{\text{loss}} \propto P_{\text{trans}}^2$$
        <p>Оскільки втрати зростають квадратично від передаваної потужності $P_{\text{trans}}$, завантаження ліній понад 80% призводить до різкого падіння ККД системи. Модуль будує <b>Loss Curve</b> (криву втрат) для демонстрації цієї залежності.</p>
    </div>
</div>

<!-- SECTION 03: FINANCIAL PROCESSING PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Конвеєр Фінансової Обробки (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA_FIN("df_fin (Cost & Price)") --> STACK_COST("Group by day & region")
    STACK_COST --> BAR_CHART("px.bar (Stacked Cost)")
    
    DATA_LINES("df_lines (Grid Telemetry)") --> LOSS_ENGINE("physics.calculate_line_losses")
    LOSS_ENGINE --> CLASSIFY("AC vs HVDC Split")
    
    CLASSIFY --> AGGR_DAILY("Group by day (Mean load_pct)")
    AGGR_DAILY --> FILTER_DAYS("Filter: sample_count >= 20 hours")
    
    FILTER_DAYS --> RENDER_LINES("px.line (Spline mode + Warning zones)")
    RENDER_LINES --> HRECTS("Draw Orange (80-95%) & Red (95-100%) Overlays")
    
    DATA_FIN --> HEAT_GROUP("Group by day & hour")
    HEAT_GROUP --> PIVOT("Pivot Matrix (Day x Hour)")
    PIVOT --> HEATMAP("go.Heatmap (Colorscale: Inferno)")
    
    LOSS_ENGINE --> LOSS_SCATTER("px.scatter (load_pct vs losses_mw)")
    </div></div>
</div>

<!-- SECTION 04: ANALYTICAL TOOLS MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця фінансових інструментів</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Інструмент візуалізації</th>
                    <th>Метод реалізації</th>
                    <th>Технічний висновок для оператора</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Generation Cost Bar</b></td><td>Stacked Bar Chart (Plotly)</td><td>Аналіз сукупних витрат на генерацію та порівняння часток регіонів</td></tr>
                <tr><td><b>Grid Loading Splines</b></td><td>px.line з параметром <code>line_shape="spline"</code></td><td>Аналіз завантаженості ліній ЛЕП, прогнозування виходу в критичні зони</td></tr>
                <tr><td><b>Pricing Heatmap</b></td><td>Матричний go.Heatmap з палітрою <code>Inferno</code></td><td>Визначення годин пікових цін (Price Spikes) для оптимізації роботи ГАЕС</td></tr>
                <tr><td><b>Loss Scatter Model</b></td><td>px.scatter (Навантаження vs Фізичні втрати в МВт)</td><td>Валідація теплового стану ліній, оцінка ККД передачі потужності</td></tr>
                <tr><td><b>Safety Alert Zones</b></td><td>Накладання <code>add_hrect</code> (Warning/Critical)</td><td>Миттєве виявлення ризику аварійного відключення ЛЕП</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: GRID STABILITY & HVDC VISUALIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Моніторинг стабільності мереж (AC/HVDC)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль візуалізує навантаження ліній електропередач різних типів:</p>
        <ul>
            <li><b>AC Lines:</b> Стандартні мережі змінного струму. Система відстежує їх завантаження відносно номіналу.</li>
            <li><b>HVDC Segments:</b> Магістральні лінії постійної напруги (High Voltage DC). Візуалізуються окремим яскравим фіолетовим кольором через їхню стратегічну важливість.</li>
            <li><b>Risk Zones:</b> Автоматичне затінення областей 80-95% (Warning, помаранчевий колір) та 95-100% (Critical, червоний колір) на графіках дозволяє диспетчеру побачити наближення до межі стійкості ще до спрацювання систем релейного захисту.</li>
        </ul>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Фінансового Ядра (Finance Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_financial_view(df_fin, df_lines):
    1. // [PHYSICS ENGINE INTEGRATION FOR TECHNICAL LOSSES]
       df_lines = physics.calculate_line_losses(df_lines)
       
    2. // [TEMPORAL LABELS MAPPING]
       IF df_fin is not empty:
           df_fin["day"] = format_date(df_fin["timestamp"])
       IF df_lines is not empty:
           df_lines["day"] = format_date(df_lines["timestamp"])
           
    3. // [UPPER ROW: DAILY COST & SPLINE GRID LOADING]
       col1, col2 = st.columns(2)
       with col1:
           df_cost = df_fin.groupby(["day", "region_name"])["cost"].sum().reset_index()
           fig_fin = px.bar(df_cost, x="day", y="cost", color="region_name", barmode="stack")
           safe_plotly_render(fig_fin)
           
       with col2:
           df_daily = df_lines.groupby(["day", "line_type"]).agg(load_mean=("load_pct", "mean"), count=("load_pct", "count"))
           df_l_mean = df_daily[df_daily.count >= 20] // [SAFETY: FILTER INCOMPLETE DAYS]
           fig_lines = px.line(df_l_mean, x="day", y="load_mean", color="line_type", line_shape="spline")
           
           // [ADD SAFETY THRESHOLDS]
           fig_lines.add_hrect(y0=80, y1=95, fillcolor="orange", opacity=0.1, label="WARNING")
           fig_lines.add_hrect(y0=95, y1=100, fillcolor="red", opacity=0.15, label="CRITICAL")
           fig_lines.add_hline(y=100, line_dash="solid", line_color="red", label="LIMIT 100%")
           safe_plotly_render(fig_lines)
           
    4. // [LOWER ROW: HEATMAP & LOSS MODEL]
       col3, col4 = st.columns(2)
       with col3:
           heat_pivot = pivot_matrix(df_fin, index="day", columns="hour", values="price_per_mwh")
           fig_heat = go.Figure(go.Heatmap(z=heat_pivot.values, colorscale="Inferno"))
           safe_plotly_render(fig_heat)
           
       with col4:
           fig_scat = px.scatter(df_lines, x="load_pct", y="losses_mw", color="line_type")
           safe_plotly_render(fig_scat)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: PRICING VOLATILITY HEATMAPS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Теплові карти волатильності цін</h2></div>
    <div class="glass-card flow-step">
        <p>Для глибокого аналізу динаміки тарифів використовується <b>Heatmap</b> на базі <code>go.Heatmap</code> з кольоровою шкалою <code>Inferno</code>. Вісь X показує години доби (0-23), а вісь Y — календарні дні. Це дозволяє миттєво ідентифікувати "цінові сплески" (Price Spikes) в пікові години та оцінити стабільність тарифного меню системи, що є важливим для оптимізації маневреної генерації (ГЕС/ГАЕС).</p>
    </div>
</div>

<!-- SECTION 08: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">⚙️</div>
            <div class="role-content">
                <h4><a href="physics.md">physics.py</a></h4>
                <p>Фізичний двигун системи: розрахунок технічних втрат в ЛЕП та класифікація типів мереж.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Graph Objects & Express</h4>
                <p>Низькорівневий та високорівневий рендеринг графічних об'єктів (Heatmap, Stacked Bar, Scatter).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4><a href="utils_extended_toolkit.md">ui_helpers.py</a></h4>
                <p>Керування безпечним відмальовуванням графіків та ізоляція помилок через <code>safe_plotly_render</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 09: ROADMAP TO v3.0 (PREDICTIVE PRICING & CARBON EMISSIONS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Дорожня карта v3.0 (Predictive Pricing & Carbon Emissions)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 заплановано:</p>
        <ul>
            <li><b>AI Price Forecasting:</b> Використання ШІ для прогнозування цін на балансуючому ринку на 24 години вперед.</li>
            <li><b>Real-time Loss Optimization:</b> Автоматичний розрахунок оптимального розподілу навантаження між паралельними ЛЕП для мінімізації сумарних втрат ($P_{\text{loss}}$).</li>
            <li><b>Multi-currency Support:</b> Перемикання інтерфейсу між UAH, USD та EUR з підключенням живих курсів валют через API.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">FAQ: Технічні відповіді</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Як розраховуються технічні втрати для AC та HVDC ліній?</b><br>
        A: Фізичний калькулятор у <code>physics.py</code> враховує різні коефіцієнти втрат: для змінного струму (AC) втрати є вищими через вплив індуктивного опору та реактивної потужності. Для HVDC-ліній постійного струму втрати менші, оскільки відсутній реактивний опір провідників.</p>
        <p><b>Q: Чому на графіку завантаження ліній іноді зникає останній день?</b><br>
        A: Це реалізація фільтрації неповних днів (<code>df_daily["sample_count"] >= 20</code>). Якщо поточна доба ще триває і база містить, наприклад, лише 5 годин даних, графік не малює цей день, щоб запобігти помилковому різкому спаду лінії середньодобового завантаження.</p>
        <p><b>Q: Чому саме палітра Inferno для теплової карти цін?</b><br>
        A: Inferno є лінійною за яскравістю палітрою, що забезпечує чітке сприйняття градієнтів цін навіть для користувачів з вадами колірного зору, а також ідеально вписується в дизайн-систему Cyber-HUD.</p>
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
