# Технічна специфікація: Базові Графічні Примітиви ATLAS (BASE CHARTS GIGA-PASSPORT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">GRAPHICAL FOUNDATION | BASE PLOTTING UTILS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Базовий Графічний Двигун</h1>
            <p class="mega-subtitle">Фундамент візуальної аналітики: уніфіковані стилі Plotly, кастомні лейаути для Cyber-HUD, оптимізовані палітри кольорів та стандартизація рендерингу для всіх UI-модулів</p>
            <div class="status-tags"><span class="tag tag-online">BASE PLOTTING ACTIVE</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">UI ARCHITECT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📐</div><div class="metric-info"><span class="metric-label">Framework</span><span class="metric-value">Plotly Graph Objects</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌌</div><div class="metric-info"><span class="metric-label">Theming</span><span class="metric-value">Dark HUD Pattern</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Standard</span><span class="metric-value">Unified Layouts</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Resilience</span><span class="metric-value">Type-Safe Plots</span></div></div>
</div>

<!-- SECTION 01: GRAPHICAL FOUNDATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Графічного Фундаменту</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>base.py</code> є "Канвою" проекту ATLAS. В системі з десятками аналітичних вкладок неприпустимо створювати графіки "з нуля" у кожному модулі. Базовий графічний двигун забезпечує **Візуальну Монолітність**: всі діаграми мають однакову товщину ліній, шрифти, кольори осей та поведінку при наведенні. Це ядро, яке інкапсулює складність налаштування Plotly, надаючи іншим модулям чистий та надійний інтерфейс для візуалізації енергетичних процесів.</p>
    </div>
</div>

<!-- SECTION 02: UNIFIED CHART RENDERING ARCHITECTURE -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Архітектура уніфікованого рендерингу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI_DATA("Raw Data Feed") --> LAYOUT("Base Layout Factory")
    LAYOUT --> THEME("Applying Cyber-HUD Tokens")
    THEME --> PLOT("Specific Plot Type (Bar, Line, Area)")
    PLOT --> RENDER("Final Plotly Object")
    RENDER --> UI_HELPER("UI Safe Dispatcher")
    </div></div>
</div>

<!-- SECTION 03: CYBER-HUD DESIGN TOKENS (🌌) -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Дизайн-токени Cyber-HUD у графіках</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль реалізує перенесення CSS-ідентичності в об'єкти Plotly:</p>
        <ul>
            <li><b>Background:</b> Примусове встановлення <code>paper_bgcolor</code> та <code>plot_bgcolor</code> у прозорий або глибокий чорний колір для інтеграції з HUD-контейнерами.</li>
            <li><b>Grid Styling:</b> Тонкі, напівпрозорі лінії сітки (rgba(255,255,255,0.05)), які не відволікають від даних, але допомагають у зчитуванні значень.</li>
            <li><b>Typography Sync:</b> Використання шрифтів без засічок (Inter/Roboto) з кастомними розмірами для легенд та підписів осей.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: UNIFIED AXIS & MARGIN LOGIC -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Уніфікована логіка осей та полів</h2></div>
    <div class="glass-card flow-step">
        <p>Всі графіки ATLAS підкоряються єдиному стандарту розривів та відступів:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Параметр</th>
                    <th>Значення</th>
                    <th>Мета</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Margins</td><td>t:40, l:10, r:10, b:40</td><td>Максимальне використання екранної площі</td></tr>
                <tr><td>Spikes</td><td>showspikes: True</td><td>Наочне проектування точки на осі при наведенні</td></tr>
                <tr><td>Axis Color</td><td>var(--accent-dim)</td><td>Стилізація під прилади ситуаційного центру</td></tr>
                <tr><td>Zero Line</td><td>Visible</td><td>Чітка база для відліку потужності МВт</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: TYPE-SAFE PLOTTING UTILS -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Типобезпечні утиліти побудови</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль надає методи-обгортки, які перевіряють вхідні дані перед рендерингом. Якщо замість ряду чисел прийшов порожній список, база видасть не помилку "Plotly Empty Trace", а красиво оформлений плейсхолдер з повідомленням "Дані відсутні". Це гарантує **Стійкість UI** (UI Resilience) та запобігає появі "білих плям" на дашбордах при затримках у надходженні телеметрії.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (BASE CHART ENGINE CORE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод ядра базового графічного двигуна</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION get_base_layout(title, height=400):
    1. INIT layout = {
           template: "plotly_dark",
           paper_bgcolor: "transparent",
           plot_bgcolor: "rgba(0,0,0,0)",
           font: { family: "Inter", color: "#e6edf3" },
           margin: { t: 50, l: 50, r: 20, b: 50 },
           xaxis: { showgrid: true, gridcolor: "rgba(255,255,255,0.05)" },
           yaxis: { showgrid: true, gridcolor: "rgba(255,255,255,0.05)" }
       }
    2. ADD Hovermode: "x unified" (для всіх ліній одночасно)
    3. RETURN layout

FUNCTION create_standard_trace(x, y, name, color):
    1. RETURN go.Scatter(x=x, y=y, name=name, line=dict(color=color, width=2.5))
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: INTERACTIVE TOOLTIP TEMPLATES -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Шаблони інтерактивних підказок (Tooltips)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль стандартизує вигляд <b>Hover Labels</b>. Всі підказки мають темний фон, білий текст та чітке розділення значень через HTML-теги. Це забезпечує читабельність складних метрик (наприклад, напруга + навантаження + температура) в одному спливаючому вікні, не перекриваючи сам графік.</p>
    </div>
</div>

<!-- SECTION 08: COLOR PALETTE MANAGEMENT -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Управління палітрою кольорів</h2></div>
    <div class="glass-card flow-step">
        <p>Двигун містить внутрішній реєстр кольорів (Neon Green, Alert Red, Warning Gold, Deep Blue). Використання цих констант у всіх графіках гарантує, що "Червоний" на графіку фінансів означає те саме, що "Червоний" на графіку прогнозів, підтримуючи єдину когнітивну модель сприйняття ризиків користувачем.</p>
    </div>
</div>

<!-- SECTION 09: GLOBAL PLOTLY CONFIGURATION SYNC -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Глобальна синхронізація конфігурації Plotly</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль виступає джерелом <b>Default Templates</b>. Це дозволяє при необхідності змінити візуальну стилістику всього проекту ATLAS (наприклад, переключитися з "Cyber-HUD" на "Print-Friendly") шляхом модифікації лише декількох рядків у <code>base.py</code>, що є прикладом високої архітектурної гнучкості.</p>
    </div>
</div>

<!-- SECTION 10: PERFORMANCE-OPTIMIZED DRAWING -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Оптимізоване малювання (Performance)</h2></div>
    <div class="glass-card flow-step">
        <p>Для графіків з великою кількістю точок (наприклад, секундні тіки за тиждень), двигун автоматично застосовує <code>Scattergl</code> (рендеринг через WebGL) замість стандартного SVG. Це дозволяє браузеру плавно відображати сотні тисяч точок, зберігаючи інтерактивність та високу частоту кадрів (FPS) інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Graph Objects</h4>
                <p>Низькорівневий двигун векторної та растрової візуалізації.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>Styles System</h4>
                <p>Джерело CSS-токенів та кольорових констант проекту.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4>Higher-level Charts</h4>
                <p>Академічні та прогнозні графіки будуються на базі цих примітивів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (LOTTIE & SHADERS) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v2.0 (Custom Shaders & Lottie)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується впровадження <b>Custom WebGL Shaders</b> для ефектів "дихаючих" ліній, підтримка <b>Lottie-анімацій</b> для іконок на графіках та перехід на <b>Plotly Resampler</b> для динамічного оновлення мега-датасетів без втрати швидкодії.</p>
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
