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
        <p>Модуль <code>cards.py</code> є "Атомарним" рівнем інтерфейсу проекту ATLAS. В умовах щільних інформаційних дашбордів кожен піксель має значення. Наша філософія базується на <b>Інформаційній Щільності</b>: ми створюємо індикатори, які передають стан системи через колір та прості символи (емодзі), не вимагаючи від користувача читання цифр. Це дозволяє оператору миттєво сканувати таблиці з сотнями підстанцій та за мілісекунди ідентифікувати проблемні ділянки мережі.</p>
    </div>
</div>

<!-- SECTION 02: INDICATOR GENERATION PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр генерації індикаторів (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Raw Numeric Value (MW, %, C)") --> TYPE_SELECT{"Select Indicator Type"}
    
    TYPE_SELECT -- "Health Score" --> BAR_LOGIC("make_health_bar(h)")
    BAR_LOGIC --> ROUND("Round to nearest 10%")
    ROUND --> SYMBOLS("Map to 🟩/⬜ and 🟢/🟡/🔴")
    SYMBOLS --> STRING("Return Rich Text Status")
    
    TYPE_SELECT -- "System Load" --> GAUGE_LOGIC("render_gauge(val)")
    GAUGE_LOGIC --> THEME("Apply Plotly Dark Theme")
    THEME --> STEPS("Define Color Zones (Safe/Warn/Crit)")
    STEPS --> PLOTLY("Render go.Indicator Object")
    
    STRING --> UI("Embed in Dataframe/KPI")
    PLOTLY --> UI
    </div></div>
</div>

<!-- SECTION 03: ASSET HEALTH BAR (SYMBOLIC PROGRESS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Прогрес-бар здоров'я (Asset Health Bar)</h2></div>
    <div class="glass-card flow-step">
        <p>Для візуалізації стану обладнання в таблицях ми розробили унікальний символьний прогрес-бар:</p>
        <ul>
            <li><b>Visual Density:</b> Використання <code>🟩</code> та <code>⬜</code> дозволяє створювати графік прямо всередині текстового поля таблиці без використання важких графічних бібліотек.</li>
            <li><b>Semantic Emoji:</b> Кожен бар починається з кольорового кола (🟢/🟡/🔴), що дає швидкий когнітивний відгук про категорію стану (Норма / Увага / Критично).</li>
            <li><b>Safe Handling:</b> Функція <code>make_health_bar</code> має вбудований захист від порожніх значень (NaN), повертаючи нейтральний статус <code>⚪ N/A</code>.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: INDICATOR THRESHOLD MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця порогових значень індикаторів</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Статус</th>
                    <th>Діапазон (%)</th>
                    <th>Колір (Hex/Emoji)</th>
                    <th>Рекомендована дія</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Safe Operational</td><td>85 - 100</td><td>🟢 / #22c55e</td><td>Моніторинг за планом</td></tr>
                <tr><td>Warning Zone</td><td>60 - 85</td><td>🟡 / #f59e0b</td><td>Збільшити частоту опитування</td></tr>
                <tr><td>Critical Alert</td><td>0 - 60</td><td>🔴 / #ef4444</td><td>Негайний виїзд бригади</td></tr>
                <tr><td>Offline / Error</td><td>NaN</td><td>⚪ / Gray</td><td>Перевірити зв'язок з датчиком</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: THE PLOTLY GAUGE ENGINE (VISUAL BUDGETING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Спідометр навантаження (Plotly Gauge)</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>render_gauge</code> створює високоякісний круговий індикатор. Ми використовуємо <b>Зоноване забарвлення</b> фону шкали (Steps): світло-зелений для безпечної зони (0-70%), оранжевий для перед-аварійної (70-90%) та червоний для критичної перевантаженості (90-100%). Це створює ефект аналогового приладу, який інтуїтивно зрозумілий навіть персоналу без глибокої технічної підготовки.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Бібліотеки (Cards Core Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION make_health_bar(h_value):
    1. VALIDATE: IF h_value IS NaN: RETURN "⚪ N/A"
    
    2. CALC_BAR:
           filled_units = round(h_value / 10)
           bar_string = ("🟩" * filled_units) + ("⬜" * (10 - filled_units))
           
    3. MAP_EMOJI:
           IF h_value >= 85: emoji = "🟢"
           ELIF h_value >= 60: emoji = "🟡"
           ELSE: emoji = "🔴"
           
    4. RETURN f"{emoji} {bar_string} {h_value}%"

FUNCTION render_gauge(load_val):
    1. DEFINE_COLORS: (Blue_Bar, Green_BG, Orange_BG, Red_BG)
    2. BUILD_FIGURE: go.Indicator(mode='gauge+number', value=load_val)
    3. SYNC_LAYOUT: background='transparent', font='white'
    4. RENDER: safe_plotly_render(fig)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: LIGHTWEIGHT UI OPTIMIZATION (STABILITY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Оптимізація легкого інтерфейсу (Stability)</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення високої продуктивності при рендерингу десятків індикаторів одночасно, ми використовуємо <b>Transparent Background</b> (<code>paper_bgcolor="rgba(0,0,0,0)"</code>) в об'єктах Plotly. Це дозволяє уникнути конфліктів з нашим кастомним CSS-фоном та зменшує навантаження на графічний процесор браузера, оскільки системі не потрібно прораховувати накладання фонових шарів.</p>
    </div>
</div>

<!-- SECTION 08: FAIL-SAFE WRAPPER INTEGRATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Інтеграція захисної обгортки (Fail-safe)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>cards.py</code> тісно інтегрований з <code>ui_helpers</code>. Перед рендерингом кожного Gauge-індикатора система намагається імпортувати <code>safe_plotly_render</code>. Якщо утиліта недоступна (наприклад, при тестуванні ізольованого компонента), модуль автоматично перемикається на стандартний <code>st.plotly_chart</code>, забезпечуючи відмовостійкість інтерфейсу навіть при часткових збоях у структурі проекту.</p>
    </div>
</div>

<!-- SECTION 09: EMOJI-DRIVEN SEMANTIC UI -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Семантичний UI на основі емодзі</h2></div>
    <div class="glass-card flow-step">
        <p>Використання стандартних Unicode-символів (Emoji) для прогрес-барів — це стратегічне рішення. Вони мають фіксовану ширину в більшості моноширинних шрифтів, що гарантує ідеальне вирівнювання барів у таблицях без використання складних CSS Grid або Flexbox. Це робить наш інтерфейс "легким" для парсингу Streamlit та миттєвим у відображенні на мобільних пристроях.</p>
    </div>
</div>

<!-- SECTION 10: USER-CENTRIC DESIGN (VISUAL HIERARCHY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Користувацький дизайн (Візуальна ієрархія)</h2></div>
    <div class="glass-card flow-step">
        <p>Всі індикатори розроблені з урахуванням <b>Центральної композиції</b>. У Gauge-чарті числове значення розташоване в центрі дуги, а суфікс "%" має менший розмір шрифту. Це фокусує увагу оператора на самій цифрі, залишаючи одиниці виміру як контекстну інформацію. Такий підхід мінімізує час зчитування даних, що є критичним під час ліквідації аварійних ситуацій.</p>
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
                <p>Низькорівневий двигун для рендерингу кругових індикаторів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4>UI Helpers</h4>
                <p>Забезпечує безпечний рендеринг без перезавантаження фрагментів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">⚙️</div>
            <div class="role-content">
                <h4>Pandas Core</h4>
                <p>Обробка NaN та підготовка числових типів для індикаторів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (ANIMATED SVG CARDS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Animated SVG Cards)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Анімованих SVG-карток</b>. Замість емодзі ми будемо використовувати власну бібліотеку векторних іконок, які будуть плавно змінювати свій стан (пульсація при критичних значеннях, плавне заповнення барів). Також буде додано підтримку <b>Sparklines</b> — мікро-графіків трендів за останні 5 хвилин, інтегрованих безпосередньо у картки підстанцій.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Бібліотека Карток</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому мій прогрес-бар сірий?</b> — Це означає, що дані від підстанції відсутні (N/A). Перевірте статус датчика.</p>
        <p><b>Чи можна змінити порогові значення?</b> — Так, вони зафіксовані в коді <code>cards.py</code> і можуть бути легко адаптовані під вимоги конкретного енерговузла.</p>
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
