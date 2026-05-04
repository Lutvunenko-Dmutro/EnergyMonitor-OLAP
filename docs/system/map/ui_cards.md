# Технічна специфікація модуля: ui/components/cards.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">UI INDICATORS LIBRARY & ASSET HEALTH VISUALIZER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏥</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Бібліотека KPI-Індикаторів ATLAS</h1>
            <p class="mega-subtitle">Система мікро-візуалізації стану мережі: кругові Gauge-діаграми навантаження, текстові прогрес-бари здоров'я активів та легковажні UI-компоненти</p>
            <div class="status-tags"><span class="tag tag-online">UI LIBRARY ACTIVE</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">VISUALIZATION EXPERT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⭕</div><div class="metric-info"><span class="metric-label">Engine</span><span class="metric-value">Plotly Indicator</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Bars</span><span class="metric-value">Emoji-Progress</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Logic</span><span class="metric-value">Color Zoning</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Weight</span><span class="metric-value">Zero-Latence UI</span></div></div>
</div>

<!-- SECTION 01: UI INDICATORS LIBRARY PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Бібліотеки KPI-Індикаторів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>cards.py</code> є "Органами Почуттів" інтерфейсу ATLAS. В критичних системах моніторингу швидкість зчитування інформації є вирішальною. Ми відмовилися від складних графіків там, де достатньо одного погляду. Бібліотека реалізує концепцію <b>Lightweight UI</b>: компактні, колірно-кодовані індикатори, що дозволяють оператору миттєво відрізнити "Зелену" (безпечну) зону від "Червоної" (аварійної), не відволікаючись на цифри.</p>
    </div>
</div>

<!-- SECTION 02: INDICATOR RENDERING ARCHITECTURE -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Архітектура рендерингу індикаторів</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    VAL("Вхідне значення (Load/Health)") --> NORM("Нормалізація (0-100)")
    NORM --> GAUGE("render_gauge: Plotly Indicator")
    NORM --> BAR("make_health_bar: Text Progress")
    GAUGE --> THEME("Dark Theme Injection")
    BAR --> EMOJI("Emoji Status Coding")
    THEME & EMOJI --> UI("Dashboard Widget")
    </div></div>
</div>

<!-- SECTION 03: ASSET HEALTH BARS & EMOJI LOGIC -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Прогрес-бари здоров'я та логіка емодзі</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>make_health_bar</code> реалізує унікальний підхід до текстової візуалізації для інтеграції в таблиці Digital Twin:</p>
        <ul>
            <li><b>Символьна графіка:</b> Використання <code>🟩</code> та <code>⬜</code> для створення бару з кроком 10%. Це дозволяє бачити стан об'єкта навіть у текстовому лозі або при відключених зображеннях.</li>
            <li><b>Колірна семантика:</b> 🟢 (Health > 85%), 🟡 (60-85%), 🔴 (< 60%).</li>
            <li><b>Robustness:</b> Автоматична обробка <code>NaN/None</code> значень (відображення ⚪ N/A), що гарантує стабільність таблиць.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: GAUGE INDICATORS & COLOR ZONING -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Gauge-індикатори та колірне зонування</h2></div>
    <div class="glass-card flow-step">
        <p>Для моніторингу загального завантаження мережі використовується <code>render_gauge</code>. Він реалізує сувору логіку безпечних зон:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Діапазон</th>
                    <th>Колір (RGBA)</th>
                    <th>Статус режиму</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>0 - 70%</td><td>rgba(34, 197, 94, 0.2)</td><td><b>SAFE:</b> Номінальна робота</td></tr>
                <tr><td>70 - 90%</td><td>rgba(245, 158, 11, 0.2)</td><td><b>WARN:</b> Зона підвищеної уваги</td></tr>
                <tr><td>90 - 100%</td><td>rgba(239, 68, 68, 0.2)</td><td><b>CRITICAL:</b> Ризик аварійного відключення</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: LIGHTWEIGHT UI OPTIMIZATION -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Оптимізація легковажного інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <p>Всі компоненти <code>cards.py</code> оптимізовані для <b>Zero-Latence</b> рендерингу. Gauge-діаграми мають фіксовану висоту (120px) та мінімальні відступи (margin), що дозволяє розміщувати їх у вузьких колонках KPI-панелей без спотворення лейауту. Використання <code>paper_bgcolor="rgba(0,0,0,0)"</code> забезпечує ідеальну прозорість та інтеграцію в скляний (Glassmorphism) дизайн ATLAS.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (KPI COMPONENTS CORE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод ядра KPI-компонентів</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION make_health_bar(h_value):
    1. IF h_value is MISSING: RETURN "⚪ N/A"
    2. filled_segments = ROUND(h_value / 10)
    3. bar_string = "🟩" * filled_segments + "⬜" * (10 - filled_segments)
    4. SELECT emoji based on thresholds (85, 60)
    5. RETURN formatted_string
    
FUNCTION render_gauge(load_val):
    1. CREATE go.Indicator(mode="gauge+number")
    2. SET axis range [0, 100]
    3. CONFIGURE steps: [Green(0-70), Amber(70-90), Red(90-100)]
    4. APPLY Dark_Theme_Layout
    5. CALL safe_plotly_render(fig)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: FAIL-SAFE RENDERER DISPATCHER -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Диспетчер відмовостійкого рендерингу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль містить механізм <b>Dynamic Import Fallback</b>: він намагається використовувати <code>safe_plotly_render</code> з утиліт проекту для забезпечення імерсивності, але у випадку помилки імпорту автоматично перемикається на стандартний <code>st.plotly_chart</code>. Це гарантує працездатність UI навіть під час часткового рефакторингу або збоїв залежностей.</p>
    </div>
</div>

<!-- SECTION 08: THEMATIC STYLING CONSISTENCY -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Уніфікація тематичного стилю</h2></div>
    <div class="glass-card flow-step">
        <p>Кольори індикаторів (<code>#3b82f6</code> для бару, білий шрифт для цифр) жорстко прив'язані до дизайн-системи ATLAS. Це забезпечує візуальну консистентність: індикатор у вкладці KPI виглядає точно так само, як індикатор у Sidebar, створюючи цілісний користувацький досвід.</p>
    </div>
</div>

<!-- SECTION 09: ASSET DIGITAL TWIN INTEGRATION -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Інтеграція з Цифровими Двійниками</h2></div>
    <div class="glass-card flow-step">
        <p>Компоненти <code>cards.py</code> розроблені спеціально для відображення стану <b>Digital Twins</b>. Кожен рядок таблиці підстанцій використовує <code>make_health_bar</code>, що перетворює сухі цифри напруги та температури масла в зрозумілу оцінку "життєздатності" активу.</p>
    </div>
</div>

<!-- SECTION 10: RESPONSIVE METRIC SCALING -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Адаптивне масштабування метрик</h2></div>
    <div class="glass-card flow-step">
        <p>Розмір шрифту в <code>render_gauge</code> (18px) підібраний таким чином, щоб цифри залишалися читабельними навіть на мобільних пристроях або при сильному стисненні вікна браузера, що критично для диспетчерів, які працюють з декількома моніторами одночасно.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📈</div>
            <div class="role-content">
                <h4>Plotly Graph Objects</h4>
                <p>Низькорівневий двигун для рендерингу Gauge-індикаторів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛡️</div>
            <div class="role-content">
                <h4>UI Helpers</h4>
                <p>Забезпечує безпечне відображення графіків (опційно).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🐼</div>
            <div class="role-content">
                <h4>Pandas</h4>
                <p>Використовується для валідації вхідних числових значень.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (INTERACTIVE GAUGES) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v2.0 (Animated & Interactive Gauges)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується впровадження <b>Анімованих переходів</b> між значеннями для плавності сприйняття, підтримка <b>Click-events</b> на індикаторах для швидкого переходу до детальної аналітики об'єкта та додавання <b>Sparklines</b> безпосередньо всередину картки KPI.</p>
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
