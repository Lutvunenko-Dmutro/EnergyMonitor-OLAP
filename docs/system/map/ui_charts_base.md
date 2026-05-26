# Технічна специфікація: Ядро Базової Візуалізації (CORE VISUALIZATION ENGINE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CORE GRAPHICS | ANALYTICAL VISUALS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Ядро Базової Візуалізації</h1>
            <p class="mega-subtitle">Фундаментальний двигун графічної аналітики проєкту ATLAS: двовісні кореляційні графіки (Dual-Axis Charts), добові профілі ритмічності (Rhythm Analysis) та багатовузлові тренди</p>
            <div class="status-tags"><span class="tag tag-online">BASE VIZ ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">CORE VISUALIZER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Dual-Axis</span><span class="metric-value">Secondary Y-Axis Spec</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📅</div><div class="metric-info"><span class="metric-label">Rhythm</span><span class="metric-value">Monday vs Saturday</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Rendering</span><span class="metric-value">Zero-latency GPU</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧪</div><div class="metric-info"><span class="metric-label">Color blending</span><span class="metric-value">Hex-to-RGB Alpha</span></div></div>
</div>

<!-- SECTION 01: BASE VISUALIZATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Базової Візуалізації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>base.py</code> є "Зоровим апаратом" проєкту ATLAS. Нашою філософією є <b>Контекстна Прозорість</b>: графіки не повинні бути просто набором ліній. Вони мають виявляти приховані взаємозв'язки. Побудова кореляцій за двома осями Y (наприклад, суміщення температурного режиму з рівнем енергоспоживання) дозволяє диспетчеру миттєво побачити причину перевантаження, а ритмічні графіки допомагають виявити системні зрушення у тижневих циклах споживання міста.</p>
    </div>
</div>

<!-- SECTION 02: BASE CHART PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр базової візуалізації (Data Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Input DataFrame (load, temp, timestamp)") --> TYPE_SELECT{"Select Layout Engine"}
    
    TYPE_SELECT -- "Dual-Axis Trend" --> SUBPLOT("make_subplots(secondary_y=True)")
    SUBPLOT --> CHECK_MULTI{"Is Multi-Substation?"}
    
    CHECK_MULTI -- "Yes" --> ADD_TRACES_MULTI("Loop substations: add left & right lines")
    CHECK_MULTI -- "No" --> ADD_TRACES_SINGLE("Add single left & right lines")
    ADD_TRACES_SINGLE --> HEX_RGB("_hex_to_rgb(left_color)")
    HEX_RGB --> FILL("Apply Alpha-blended fill color (rgba, 0.08)")
    
    TYPE_SELECT -- "Rhythm Chart" --> RHYTHM_COPY("Copy & cast: dow, hour, avg_load to numeric")
    RHYTHM_COPY --> FILTER_DAYS("Filter: Monday (dow=1) & Saturday (dow=6)")
    FILTER_DAYS --> PLOT_RHYTHM("Render solid line (Monday) and dashed line (Saturday)")
    
    ADD_TRACES_MULTI --> STYLE_LAYOUT("Apply Template plotly_dark & Margin Fix")
    FILL --> STYLE_LAYOUT
    PLOT_RHYTHM --> STYLE_LAYOUT
    
    STYLE_LAYOUT --> RENDER("Output go.Figure to UI View")
    </div></div>
</div>

<!-- SECTION 03: DUAL-AXIS CORRELATION ARCHITECTURE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Архітектура двовісної кореляції (Dual-Axis)</h2></div>
    <div class="glass-card flow-step">
        <p>Для одночасного спостереження параметрів з різними шкалами (наприклад, потужність у МВт та температура у °C) ми використовуємо технологію <b>двовісного рендерингу (Secondary Y-Axis)</b>:</p>
        <ul>
            <li><b>Subplot Specs:</b> Ми ініціалізуємо об'єкт Plotly за допомогою <code>make_subplots(specs=[[{"secondary_y": True}]])</code>, що створює дві паралельні системи координат на одному полотні.</li>
            <li><b>Alpha-blending Area:</b> Для головного (лівого) тренду ми розраховуємо плавне заповнення до осі X. За допомогою функції <code>_hex_to_rgb</code> шістнадцятковий колір конвертується у формат RGBA з прозорістю <code>0.08</code>. Це створює відчуття глибини та покращує візуальний баланс графіка, не перекриваючи сітку.</li>
            <li><b>Grid Separation:</b> Ми вимикаємо сітку для правої осі (<code>showgrid=False</code>), щоб лінії правої осі не створювали візуального хаосу при перетині з основною сіткою.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: CORE VISUALIZATION MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця базових аналітичних графіків</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Тип графіка / Метод</th>
                    <th>Вхідні колонки</th>
                    <th>Особливості стилізації</th>
                    <th>Аналітична мета</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>render_dual_axis_chart()</code></td><td><code>ts</code>, <code>left_col</code>, <code>right_col</code>, <code>substation</code> (опціонально)</td><td>Дві осі Y, напівпрозоре заповнення лівого тренду (0.08 alpha), пунктирний правий тренд.</td><td>Аналіз впливу факторів (температура, вологість, водень) на загальне споживання.</td></tr>
                <tr><td><code>render_rhythm_chart()</code></td><td><code>dow</code> (Day of Week), <code>hour_of_day</code>, <code>avg_load</code></td><td>Суцільна лінія (Понеділок), штрихова лінія (Субота), колірний контраст Orange/SkyBlue.</td><td>Аналіз ритмічності: порівняння типового робочого дня з типовим вихідним для виявлення піків.</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: DAILY RHYTHM ANALYSIS (MON vs SAT) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Добові профілі ритмічності (Rhythm)</h2></div>
    <div class="glass-card flow-step">
        <p>Аналіз ритмічності в <code>render_rhythm_chart</code> фокусується на двох крайніх точках тижневого циклу споживання:</p>
        <ul>
            <li><b>Понеділок (dow=1):</b> Відображає максимальне робоче завантаження енергосистеми (активність заводів, офісів, транспорту). Позначається яскравою суцільною лінією <code>#f97316</code>.</li>
            <li><b>Субота (dow=6):</b> Показує типову картину вихідного дня (побутове споживання, відсутність промислового навантаження). Позначається штриховою лінією блакитного кольору <code>#38bdf8</code>.</li>
        </ul>
        <p>Цей графік дозволяє енергоаналітику миттєво визначити коефіцієнт нерівномірності споживання та скоригувати графіки генерації електростанцій.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE & AST DETAILS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Математичні перетворення та алгоритми (Base Logic)</h2></div>
    <div class="glass-card flow-step">
        <p>Математична формула для перетворення HEX-кольору у формат RGB (зсув по байтах):</p>
        <div style="text-align: center; margin: 15px 0; font-size: 15px; color: var(--accent);">
            $$\text{RGB}(H) = \left( \text{int}(H_{1:2}, 16), \text{int}(H_{3:4}, 16), \text{int}(H_{5:6}, 16) \right)$$
        </div>
        <p>Це перетворення виконується у допоміжній функції <code>_hex_to_rgb(hex_color)</code> для гнучкого додавання альфа-каналу прозорості.</p>
        
        <pre><code class="language-python"># Двигун базової візуалізації (base.py)
FUNCTION _hex_to_rgb(hex_color):
    1. Clean '#' symbol if present:
           h = hex_color.lstrip('#')
    2. Split hex into pairs and convert to decimal list:
           R = int(h[0:2], 16)
           G = int(h[2:4], 16)
           B = int(h[4:6], 16)
    3. Return string "R,G,B"
END FUNCTION

FUNCTION render_dual_axis_chart(df, left_col, left_label, left_color, right_col, right_label, right_color, fill_left):
    1. INITIALIZE subplots with secondary Y axis:
           fig = make_subplots(specs=[[{"secondary_y": True}]])
           
    2. CHECK FOR MULTI-SUBSTATION:
           IF "substation" in df.columns:
               unique_subs = df["substation"].unique()
           ELSE:
               unique_subs = [None]
           is_multi = len(unique_subs) > 1
           
    3. LOOP SUBSTATIONS AND ADD TRACES:
           FOR sub IN unique_subs:
               sub_df = df[df["substation"] == sub] IF sub IS NOT NULL ELSE df
               trace_name = str(sub) IF sub IS NOT NULL ELSE left_label
               
               # 3.1 Main left axis (usually Load)
               fig.add_trace(go.Scatter(
                   x = sub_df["ts"], y = sub_df[left_col],
                   name = f"{trace_name} ({left_label})" IF is_multi ELSE left_label,
                   line = dict(color=left_color IF NOT is_multi ELSE None, width=2),
                   fill = "tozeroy" IF fill_left and NOT is_multi ELSE "none",
                   fillcolor = f"rgba({_hex_to_rgb(left_color)},0.08)" IF fill_left and NOT is_multi ELSE None
               ), secondary_y=False)
               
               # 3.2 Secondary right axis (usually Temperature or H2)
               fig.add_trace(go.Scatter(
                   x = sub_df["ts"], y = sub_df[right_col],
                   name = f"{trace_name} ({right_label})" IF is_multi ELSE right_label,
                   line = dict(color=right_color IF NOT is_multi ELSE None, width=1.5, dash="dot" IF NOT is_multi ELSE "solid")
               ), secondary_y=True)
               
    4. Y-AXES STYLING:
           Set left Y axis title = left_label
           Set right Y axis title = right_label, disable secondary grid: showgrid=False
           
    5. LAYOUT OVERRIDES:
           height = 400
           hovermode = "x unified"
           Apply template "plotly_dark"
           Position legend horizontally at the bottom: y=-0.4
           
    6. RETURN fig
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: ZERO-LATENCY GPU RENDERING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Оптимізація рендерингу (Zero-latency)</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення миттєвого відображення графіків на слабких клієнтських комп'ютерах та смартфонах, ми використовуємо об'єкти <b>Plotly Scatter</b> з оптимізованими типами ліній. Всі розрахунки агрегації (наприклад, обчислення середнього добового ритму) виконуються на стороні сервера за допомогою швидких векторних операцій Pandas перед передачею даних у Plotly, що знижує навантаження на JS-двигун браузера до нуля.</p>
    </div>
</div>

<!-- SECTION 08: COGNITIVE RHYTHM MAPPING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Когнітивне мапування ритмів</h2></div>
    <div class="glass-card flow-step">
        <p>Вибір кольорів для Rhythm Chart базується на психофізіології кольору. Яскравий оранжевий (Понеділок) символізує енергію, активність та високу робочу динаміку, тоді як спокійний блакитний (Субота) асоціюється зі спокоєм, вихідними та низьким побутовим ритмом. Це дозволяє диспетчеру сприймати графік на рівні емоцій, навіть не дивлячись на підписи легенди.</p>
    </div>
</div>

<!-- SECTION 09: ROBUST NUMERIC CASTING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Стійка конвертація числових типів (Robust Casting)</h2></div>
    <div class="glass-card flow-step">
        <p>При побудові Rhythm Chart дані з бази можуть містити текстові артефакти або порожні значення. Щоб запобігти збоям рендерингу, у функції <code>render_rhythm_chart</code> застосовується примусове кастингування колонок до числових типів:</p>
        <pre><code class="language-python">for col in ["dow", "hour_of_day", "avg_load"]:
    df_r[col] = pd.to_numeric(df_r[col], errors="coerce")</code></pre>
        <p>Значення, які не вдалося перетворити на числа (наприклад, випадковий текст помилки датчика), м'яко замінюються на <code>NaN</code> і просто ігноруються при побудові ліній, що забезпечує стабільність UI.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM LEGEND UX FIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">UX-фікс розташування легенди</h2></div>
    <div class="glass-card flow-step">
        <p>Стандартна легенда Plotly зазвичай розташовується справа, що стискає корисну ширину графіка на 15-20%. У нашому ядрі легенду винесено **під графік (horizontally centered)** за допомогою параметрів <code>y=-0.4</code> та <code>x=0.5</code>. Це дає графіку дихати, збільшує корисну ширину шкали часу та робить аналіз дрібних деталей значно зручнішим.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Plotly Subplots</h4>
                <p>Інфраструктура для створення багатоосьових сіток графіків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🗄️</div>
            <div class="role-content">
                <h4>Pandas Library</h4>
                <p>Очищення даних, сортування та кастинг типів перед рендерингом.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>Plotly Express</h4>
                <p>Базовий набір для експрес-візуалізації швидких трендів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (HEATMAP GRID) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Heatmap Rhythm Grid)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується розширення ядра базової візуалізації:</p>
        <ul>
            <li>Впровадження <b>Heatmap Rhythm Grid</b> — теплової карти споживання, де кожна клітинка показує рівень навантаження на перетині "Година доби / День тижня". Це дозволить бачити повну картину тижня в одному компактному віджеті.</li>
            <li>Реалізація автоматичної підсвітки аномальних піків (Alarm Markers) на графіках трендів.</li>
            <li>Додавання підтримки експорту даних графіка безпосередньо у формат Excel з сайдбару.</li>
        </ul>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Базові Графіки</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому на Rhythm Chart не відображається Субота?</b><br>— Перевірте вхідний DataFrame. Якщо ваш часовий діапазон фільтрації охоплює лише будні дні (наприклад, середу та четвер), дані за суботу будуть відсутні, і відповідна лінія не побудується.</p>
        
        <p><b>Як працює злиття декількох підстанцій на одному графіку?</b><br>— Якщо в DataFrame є колонка <code>substation</code> і вона містить більше одного унікального об'єкта, система автоматично відключить градієнтну заливку (fill) та перейде в режим паралельного порівняння ліній для кожного об'єкта.</p>
        
        <p><b>Чому права вісь Y не має сітки?</b><br>— Ми вимкнули сітку правої осі (<code>showgrid=False</code>) навмисно, щоб горизонтальні лінії правої осі не перетиналися з лініями лівої осі, створюючи візуальний шум.</p>
        
        <p><b>Як функція _hex_to_rgb обробляє короткі HEX-коди (наприклад, #fff)?</b><br>— Функція очікує повний 6-значний HEX-код. Для стабільної роботи завжди передавайте кольори у форматі <code>#RRGGBB</code>.</p>
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
