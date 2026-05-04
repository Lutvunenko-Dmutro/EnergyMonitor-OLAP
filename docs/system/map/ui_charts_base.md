# Технічна специфікація: Ядро Базової Візуалізації (CORE VISUALIZATION ENGINE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CHARTING ENGINE | ANALYTICAL CORE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Ядро Візуалізації</h1>
            <p class="mega-subtitle">Фундаментальний двигун аналітичних графіків проекту ATLAS: підтримка подвійних осей (Dual-Axis), аналіз ритміки споживання та професійна стилізація з використанням Alpha-blending для прецизійного аудиту даних</p>
            <div class="status-tags"><span class="tag tag-online">VIS ENGINE ACTIVE</span><span class="tag tag-version">v2.3.0</span><span class="tag tag-role">CORE ANALYTICS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Mode</span><span class="metric-value">Dual-Axis Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⏳</div><div class="metric-info"><span class="metric-label">Analysis</span><span class="metric-value">Rhythm (Day Type)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Alpha</span><span class="metric-value">0.08 Blending</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Library</span><span class="metric-value">Plotly Graph Objects</span></div></div>
</div>

<!-- SECTION 01: CHARTING ENGINE PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Ядра Візуалізації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>base.py</code> є "Очима" аналітичної системи ATLAS. В складних енергетичних системах дані мають сенс лише у порівнянні. Наша філософія базується на <b>Кореляційній Прозорості</b>: ми розробили інструменти, які дозволяють бачити не просто цифри, а зв'язки між ними. Використання подвійних осей (Dual-Axis) та порівняння добових ритмів (Rhythm Analysis) дає диспетчеру можливість миттєво зрозуміти, як зміна одного параметра (наприклад, температури повітря) впливає на інший (навантаження мережі), перетворюючи сирі дані на усвідомлені технічні рішення.</p>
    </div>
</div>

<!-- SECTION 02: VISUALIZATION PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр побудови графіків (Vis Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Aggregated Dataframe") --> TYPE{"Identify Chart Type"}
    
    TYPE -- "Correlation" --> DUAL("render_dual_axis_chart")
    DUAL --> SUBPLOTS("make_subplots (secondary_y=True)")
    SUBPLOTS --> TRACES("Add Scatter Traces (Left/Right)")
    TRACES --> ALPHA("Apply RGBA Alpha Blending (0.08)")
    
    TYPE -- "Patterns" --> RHYTHM("render_rhythm_chart")
    RHYTHM --> GROUP("Group by DayType (Mon vs Sat)")
    GROUP --> OVERLAY("Overlay Profiles (Hour 0-23)")
    
    ALPHA --> LAYOUT("Update Layout (Dark Theme)")
    OVERLAY --> LAYOUT
    
    LAYOUT --> FIG("Return go.Figure Object")
    </div></div>
</div>

<!-- SECTION 03: DUAL-AXIS CORRELATION ENGINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Двигун кореляції з подвійною віссю (Dual-Axis)</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>render_dual_axis_chart</code> є ключовою для діагностичного аналізу:</p>
        <ul>
            <li><b>Independent Scaling:</b> Ліва та права осі Y масштабуються незалежно, що дозволяє порівнювати параметри з різними одиницями виміру (наприклад, МВт та °C).</li>
            <li><b>Visual Hierarchy:</b> Основний параметр (навантаження) підсвічується заливкою (Fill to zero) з альфа-каналом, тоді як допоміжний параметр відображається пунктирною лінією (Dot dash).</li>
            <li><b>Multi-Substation Overlay:</b> Модуль автоматично розпізнає наявність даних від декількох підстанцій та будує індивідуальні тренди для кожної, зберігаючи цілісність легенди.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: CHART STYLING & COLOR MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця стилізації та колірна палітра</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Параметр</th>
                    <th>Тип лінії</th>
                    <th>Колір (Hex)</th>
                    <th>Alpha-заливка</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Load (MW)</td><td>Solid (2px)</td><td>#f97316 (Orange)</td><td>0.08 (Subtle)</td></tr>
                <tr><td>Temperature</td><td>Dot (1.5px)</td><td>#38bdf8 (Blue)</td><td>None</td></tr>
                <tr><td>Oil Temp</td><td>Solid (1.5px)</td><td>#f43f5e (Rose)</td><td>None</td></tr>
                <tr><td>Health Index</td><td>Solid (2px)</td><td>#22c55e (Green)</td><td>None</td></tr>
                <tr><td>Gas (H2)</td><td>Dash (1.5px)</td><td>#a855f7 (Purple)</td><td>None</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: RHYTHM ANALYSIS (WORKDAY VS WEEKEND) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Аналіз енергетичних ритмів (Будні vs Вихідні)</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>render_rhythm_chart</code> візуалізує "Відбиток пальця" енергосистеми. Ми накладаємо середній профіль понеділка (робочий день) на профіль суботи (вихідний). Це дозволяє технічному персоналу перевірити правильність роботи ШІ-моделей: чи враховують вони падіння промислового споживання у вихідні та зміщення пікових годин вечірнього споживання населенням.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра (Vis Engine Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_dual_axis(df, left_col, right_col):
    1. INITIALIZE: fig = make_subplots(secondary_y=True)
    
    2. ITERATE_SUBSTATIONS:
           FOR sub IN df.substations.unique():
               # Left Axis Trace (Fillable)
               fig.add_trace(go.Scatter(y=sub.left, fill='tozeroy', alpha=0.08))
               
               # Right Axis Trace (Trendline)
               fig.add_trace(go.Scatter(y=sub.right, dash='dot'), secondary_y=True)
               
    3. STYLE:
           SET template = "plotly_dark"
           SET hovermode = "x unified"
           SET legend = "horizontal_bottom"
           
    4. RETURN fig
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: ALPHA-BLENDING & VISUAL LAYER SYNC -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Alpha-blending та синхронізація шарів</h2></div>
    <div class="glass-card flow-step">
        <p>Для запобігання візуального перекриття (Occlusion) при відображенні декількох графіків, ми використовуємо власну утиліту <code>_hex_to_rgb</code>. Вона динамічно перетворює HEX-кольори у RGBA з рівнем прозорості <b>0.08</b> для фонових заливок. Це створює ефект "легких тіней" під графіками, які допомагають оку відстежувати площу під кривою, але не заважають бачити сітку та інші лінії трендів.</p>
    </div>
</div>

<!-- SECTION 08: INTERACTIVE HOVER & LEGEND DESIGN -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Дизайн інтерактивного наведення та легенди</h2></div>
    <div class="glass-card flow-step">
        <p>Усі графіки використовують режим <b>hovermode="x unified"</b>. Це означає, що при наведенні курсору на будь-яку точку осі X, система автоматично підсвічує значення всіх параметрів на цей момент часу у єдиному тултипі. Легенда графіків винесена у нижню частину (horizontal layout), що звільняє місце для самої візуалізації та забезпечує кращу читабельність на мобільних пристроях.</p>
    </div>
</div>

<!-- SECTION 09: MEMORY OPTIMIZATION FOR HEAVY PLOTS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Оптимізація пам'яті для важких графіків</h2></div>
    <div class="glass-card flow-step">
        <p>При роботі з великими часовими діапазонами (наприклад, рік даних), модуль <code>base.py</code> автоматично підтримує роботу з агрегованими масивами. Ми мінімізуємо кількість точок у об'єктах <code>go.Scatter</code>, передаючи вже підготовлені в Pandas середні значення. Це гарантує швидкий відгук інтерфейсу (FPS > 30) навіть при активному масштабуванні (Zooming) складних кореляційних діаграм.</p>
    </div>
</div>

<!-- SECTION 10: USER-CENTRIC ANALYTICAL UX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Аналітичний UX (Користувацький досвід)</h2></div>
    <div class="glass-card flow-step">
        <p>Графіки в <code>base.py</code> розроблені як **Дослідницькі інструменти**. Оператор може вимкнути будь-яку лінію, просто натиснувши на її назву в легенді. Це дозволяє крок за кроком "очищати" візуалізацію від шуму, фокусуючись на конкретному аспекті аварії або аномалії, що значно прискорює процес розслідування технологічних інцидентів.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Subplots</h4>
                <p>Механізм створення багатоосьових композицій графіків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Plotly Graph Objects</h4>
                <p>Низькорівневий рендеринг векторних Scatter-трейсів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">⚙️</div>
            <div class="role-content">
                <h4>Pandas Core</h4>
                <p>Постачальник очищених та типізованих аналітичних масивів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (WEBGL RENDERING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (WebGL Rendering)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується перехід на **WebGL-рендеринг** (go.Scattergl). Це дозволить плавно відображати мільйони точок телеметрії без будь-якої агрегації. Також буде додано підтримку <b>Зумування за областю</b> (Range Selector), як у професійних фінансових терміналах, та вбудовані інструменти анотування для маркування аномалій прямо на графіку.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Ядро Візуалізації</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому на графіку Rhythm немає суботи?</b> — Перевірте, чи охоплює обраний часовий діапазон хоча б один вихідний день.</p>
        <p><b>Як скинути зум на графіку?</b> — Двічі клікніть на полотно графіка, і він повернеться до початкового масштабу.</p>
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
