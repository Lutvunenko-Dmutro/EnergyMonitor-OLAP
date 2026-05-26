# Технічна специфікація: Бібліотека Інтерактивних Карток та Індикаторів (UI INDICATORS LIBRARY)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">UI COMPONENTS | MICRO-INDICATORS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎛️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Бібліотека Індикаторів</h1>
            <p class="mega-subtitle">Набір компактних візуальних елементів для швидкої оцінки стану об'єктів енергомережі: кругові діаграми завантаження (Gauges), текстові прогрес-бари здоров'я (Health Bars) та легковагові UI-компоненти</p>
            <div class="status-tags"><span class="tag tag-online">LIBRARY ACTIVE</span><span class="tag tag-version">v2.2.0</span><span class="tag tag-role">VISUAL ANALYTICS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🟢</div><div class="metric-info"><span class="metric-label">Pattern</span><span class="metric-value">Emoji-based Bars</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⏲️</div><div class="metric-info"><span class="metric-label">Indicator</span><span class="metric-value">Plotly Gauge Engine</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Performance</span><span class="metric-value">Zero-latency Render</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Style</span><span class="metric-value">Adaptive Thresholds</span></div></div>
</div>

<!-- SECTION 01: CARDS LIBRARY PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Бібліотеки Індикаторів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>cards.py</code> є "Атомарним" рівнем інтерфейсу проєкту ATLAS. В умовах щільних інформаційних дашбордів кожен піксель має значення. Наша філософія базується на <b>Інформаційній Щільності</b>: ми створюємо індикатори, які передають стан системи через колір та прості символи (емодзі), не вимагаючи від користувача читання довгих цифр. Це дозволяє оператору миттєво сканувати таблиці з десятками підстанцій та за мілісекунди ідентифікувати проблемні ділянки мережі, що значно прискорює реакцію на аварії.</p>
    </div>
</div>

<!-- SECTION 02: INDICATOR GENERATION PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр генерації індикаторів (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Raw Numeric Value (MW, %, C, H2)") --> TYPE_SELECT{"Select Indicator Type"}
    
    TYPE_SELECT -- "Health Score" --> BAR_LOGIC("make_health_bar(h)")
    BAR_LOGIC --> NAN_CHECK{"Is Value NaN?"}
    NAN_CHECK -- "Yes" --> RETURN_NA("Return ⚪ N/A")
    NAN_CHECK -- "No" --> ROUND("Calculate: filled = clamp(0, 10, round(h / 10))")
    ROUND --> SYMBOLS("Generate progress bar string (🟩/⬜)")
    SYMBOLS --> COLOR_MAP("Map status color (🟢/🟡/🔴)")
    COLOR_MAP --> STRING("Return Rich Text Status String")
    
    TYPE_SELECT -- "System Load" --> GAUGE_LOGIC("render_gauge(value)")
    GAUGE_LOGIC --> THEME("Apply Transparent Layout & White Font")
    THEME --> STEPS("Define Color Zones (Green/Orange/Red steps)")
    STEPS --> PLOTLY("Build go.Indicator Gauge Chart")
    PLOTLY --> WRAPPER("safe_plotly_render() check")
    
    STRING --> UI("Embed inside DataFrame Table or KPI Widget")
    WRAPPER --> UI
    </div></div>
</div>

<!-- SECTION 03: ASSET HEALTH BAR (SYMBOLIC PROGRESS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Прогрес-бар здоров'я (Asset Health Bar)</h2></div>
    <div class="glass-card flow-step">
        <p>Для візуалізації стану обладнання в таблицях ми розробили унікальний символьний прогрес-бар:</p>
        <ul>
            <li><b>Visual Density:</b> Використання Unicode-символів <code>🟩</code> та <code>⬜</code> дозволяє створювати наочний графік прямо всередині текстового поля таблиці без використання важких графічних бібліотек (canvas, SVG, JS).</li>
            <li><b>Semantic Emoji:</b> Кожен бар починається з кольорового кола (🟢/🟡/🔴), що дає швидкий когнітивний відгук про категорію стану (Норма / Увага / Критично) без вчитування в цифри.</li>
            <li><b>Safe Handling:</b> Функція <code>make_health_bar</code> має вбудований захист від порожніх значень (NaN) і некоректних типів даних, повертаючи нейтральний статус <code>⚪ N/A</code>.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: INDICATOR THRESHOLD MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця порогових значень індикаторів</h2></div>
    <div class="glass-card flow-step">
        <p>Математичне мапування стану та порогові значення Health Score базуються на наступній логіці:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Категорія Стану</th>
                    <th>Діапазон Health Score (%)</th>
                    <th>Колір (Hex / Emoji)</th>
                    <th>Візуальне відображення (Символи)</th>
                    <th>Оперативний регламент</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Safe Operational</b></td><td>85.0% - 100.0%</td><td>🟢 / #22c55e</td><td><code>🟢 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩</code> (>=85)</td><td>Стандартний моніторинг за графіком</td></tr>
                <tr><td><b>Warning Zone</b></td><td>60.0% - 84.9%</td><td>🟡 / #f59e0b</td><td><code>🟡 🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜</code> (>=60)</td><td>Збільшити частоту опитування сенсорів</td></tr>
                <tr><td><b>Critical Alert</b></td><td>0.0% - 59.9%</td><td>🔴 / #ef4444</td><td><code>🔴 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜</code> (&lt;60)</td><td>Негайний виїзд ремонтної бригади</td></tr>
                <tr><td><b>Offline / Error</b></td><td>NaN / Null</td><td>⚪ / Gray</td><td><code>⚪ N/A</code></td><td>Перевірити зв'язок та живлення датчиків</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: THE PLOTLY GAUGE ENGINE (VISUAL BUDGETING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Спідометр навантаження (Plotly Gauge)</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>render_gauge(value)</code> створює круговий індикатор навантаження. Ми використовуємо <b>Зоноване забарвлення шкали (Steps)</b>:</p>
        <ul>
            <li><b>Зелена зона (0-70%):</b> Безпечний режим роботи підстанції.</li>
            <li><b>Помаранчева зона (70-90%):</b> Режим підвищеного навантаження, резервні лінії готові до підключення.</li>
            <li><b>Червона зона (90-100%):</b> Критичне перевантаження, загроза автоматичного вимкнення через тепловий пробій ліній.</li>
        </ul>
        <p>Завдяки використанню низького альфа-каналу (<code>rgba(..., 0.2)</code>) для зон, шкала не засліплює очі та ідеально вписується у загальний Cyber-HUD інтерфейс.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE & FORMULAS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Математика та алгоритми (Cards Logic)</h2></div>
    <div class="glass-card flow-step">
        <p>Математична формула для обчислення кількості заповнених одиниць прогрес-бару ($filled$) при значенні здоров'я $h$:</p>
        <div style="text-align: center; margin: 15px 0; font-size: 15px; color: var(--accent);">
            $$filled = \max\left(0, \min\left(10, \text{round}\left(\frac{h}{10}\right)\right)\right)$$
        </div>
        <p>Це гарантує, що значення завжди утримується у межах від 0 до 10 одиниць, навіть якщо вхідний показник $h$ виходить за межі [0, 100]%.</p>
        
        <pre><code class="language-python"># Реалізація алгоритмів бібліотеки індикаторів (cards.py)
FUNCTION make_health_bar(h):
    1. CHECK FOR NaN:
           IF h IS NULL OR pd.isna(h):
               RETURN "⚪ N/A"
               
    2. CAST & CLAMP:
           h_val = float(h)
           filled = int(max(0, min(10, round(h_val / 10))))
           
    3. BUILD STRINGS:
           bar_string = ("🟩" * filled) + ("⬜" * (10 - filled))
           
    4. DETERMINE SEMANTIC EMOJI:
           IF h_val >= 85.0:
               emoji = "🟢"
           ELSE IF h_val >= 60.0:
               emoji = "🟡"
           ELSE:
               emoji = "🔴"
               
    5. RETURN f"{emoji} {bar_string} {h_val:.1f}%"
END FUNCTION

FUNCTION render_gauge(value):
    1. INITIALIZE Plotly Go.Figure:
           fig = go.Figure(go.Indicator(
               mode = "gauge+number",
               value = value,
               number = {"suffix": "%", "font": {"size": 18}},
               gauge = {
                   "axis": {"range": [0, 100]},
                   "bar": {"color": "#3b82f6"}, # Classic blue needle
                   "steps": [
                       {"range": [0, 70], "color": "rgba(34, 197, 94, 0.2)"},
                       {"range": [70, 90], "color": "rgba(245, 158, 11, 0.2)"},
                       {"range": [90, 100], "color": "rgba(239, 68, 68, 0.2)"}
                   ]
               }
           ))
    2. APPLY STYLES & TRANSPARENCY:
           fig.update_layout(
               height=120,
               margin=dict(t=25, b=5, l=10, r=10),
               paper_bgcolor="rgba(0,0,0,0)",
               font={"color": "white"}
           )
    3. FAIL-SAFE RENDER CHECK:
           TRY:
               FROM src.utils.ui_helpers IMPORT safe_plotly_render
           EXCEPT ImportError:
               safe_plotly_render = st.plotly_chart
               
           safe_plotly_render(fig)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: LIGHTWEIGHT UI OPTIMIZATION (STABILITY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Оптимізація легкого інтерфейсу (Stability)</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення високої продуктивності при рендерингу десятків індикаторів одночасно, ми використовуємо <b>прозорий фон</b> (<code>paper_bgcolor="rgba(0,0,0,0)"</code>) в об'єктах Plotly. Це дозволяє уникнути конфліктів з нашим кастомним CSS-фоном та зменшує навантаження на графічний процесор браузера (GPU), оскільки системі не потрібно прораховувати накладання важких фонових шарів.</p>
    </div>
</div>

<!-- SECTION 08: FAIL-SAFE WRAPPER INTEGRATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Інтеграція захисної обгортки (Fail-safe)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>cards.py</code> тісно інтегрований з <code>ui_helpers</code>. Перед рендерингом кожного Gauge-індикатора система намагається імпортувати <code>safe_plotly_render</code>. Якщо утиліта недоступна (наприклад, при тестуванні ізольованого компонента в консольному середовищі або при першому запуску), модуль автоматично перемикається на стандартний <code>st.plotly_chart</code>, забезпечуючи відмовостійкість інтерфейсу навіть при тимчасових збоях у структурі проєкту.</p>
    </div>
</div>

<!-- SECTION 09: EMOJI-DRIVEN SEMANTIC UI -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Семантичний UI на основі емодзі</h2></div>
    <div class="glass-card flow-step">
        <p>Використання стандартних Unicode-символів (Emoji) для прогрес-барів — це стратегічне рішення. Вони мають фіксовану ширину в більшості моноширинних та системних шрифтів, що гарантує ідеальне вирівнювання барів у таблицях без використання складних CSS Grid або Flexbox. Це робить наш інтерфейс "легким" для парсингу Streamlit та миттєвим у відображенні на мобільних пристроях.</p>
    </div>
</div>

<!-- SECTION 10: USER-CENTRIC DESIGN (VISUAL HIERARCHY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Користувацький дизайн (Візуальна ієрархія)</h2></div>
    <div class="glass-card flow-step">
        <p>Всі індикатори розроблені з урахуванням <b>Центральної композиції</b>. У Gauge-чарті числове значення розташоване в самому центрі дуги, а суфікс "%" має менший розмір шрифту (<code>size: 18</code>). Це фокусує увагу оператора на самій цифрі, залишаючи одиниці виміру як контекстну інформацію. Такий підхід мінімізує час зчитування даних диспетчером у кризових ситуаціях.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Graph Objects</h4>
                <p>Низькорівневий двигун для рендерингу кругових індикаторів (go.Indicator).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4>UI Helpers safe_plotly_render</h4>
                <p>Утиліта для запобігання дублювання подій рендерингу у фрагментах Streamlit.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">⚙️</div>
            <div class="role-content">
                <h4>Pandas Core pd.isna</h4>
                <p>Обробка NaN, перевірка числових типів та валідація даних сенсорів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (ANIMATED SVG CARDS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Animated SVG Cards)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Анімованих SVG-карток</b>:</p>
        <ul>
            <li>Замість емодзі будуть використовуватися власні векторні SVG-іконки з плавними переходами (CSS transitions).</li>
            <li>Картки підстанцій отримають мікро-пульсацію червоним світлом при виникненні перевантаження або аварії.</li>
            <li>Інтеграція <b>Sparklines</b> — мікро-трендів за останні 5-10 хвилин, вбудованих безпосередньо у клітинки таблиці підстанцій для швидкої оцінки динаміки навантаження.</li>
        </ul>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Бібліотека Карток</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому мій прогрес-бар здоров'я став сірим з написом N/A?</b><br>— Це означає, що від датчиків даної підстанції прийшло порожнє значення (Null / NaN). Перевірте статус підключення сенсорів або перезапустіть симуляцію.</p>
        
        <p><b>Чи можу я змінити кольори зон на круговому спідометрі (Gauge)?</b><br>— Так, межі та кольори зафіксовані у списку <code>steps</code> методу <code>render_gauge(value)</code>. Ви можете відкоригувати параметри <code>range</code> та <code>color</code> відповідно до інженерних лімітів вашої мережі.</p>
        
        <p><b>Чому спідометр займає так мало місця (height=120)?</b><br>— Ми свідомо оптимізували висоту віджета, щоб він міг лаконічно відображатися на картках підстанцій без необхідності вертикального скролінгу.</p>
        
        <p><b>Як Unicode прогрес-бар впливає на швидкість завантаження?</b><br>— Оскільки це чистий текст, швидкість його рендерингу є миттєвою (0 мілісекунд), що робить його в сотні разів продуктивнішим за будь-які JS-рендери прогрес-барів.</p>
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
