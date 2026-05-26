# Технічна специфікація: Бібліотека UI-Компонентів (SHARED UI COMPONENTS HUB)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">COMPONENTS HUB | ATOMIC DESIGN</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧩</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Хаб UI-Компонентів</h1>
            <p class="mega-subtitle">Центральний вузол багаторазових візуальних елементів проєкту ATLAS: координація бібліотек графіків, карток KPI та дизайн-системи для забезпечення візуальної цілісності HUD-інтерфейсів</p>
            <div class="status-tags"><span class="tag tag-online">COMPONENTS HUB ACTIVE</span><span class="tag tag-version">v2.2.0</span><span class="tag tag-role">DESIGN SYSTEM LEAD</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Design</span><span class="metric-value">Atomic UI System</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Library</span><span class="metric-value">Charts & Indicators</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Integrity</span><span class="metric-value">Global Style Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Reuse</span><span class="metric-value">Cross-View Sharing</span></div></div>
</div>

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Спільних Компонентів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>components/__init__.py</code> є "Складським центром" (Hub) для всіх візуальних будівельних блоків проєкту ATLAS. Наша філософія базується на <b>Атомарному Дизайні</b>: ми розробляємо компоненти як незалежні, самодостатні одиниці, які можна легко комбінувати для створення нових аналітичних екранів. Такий підхід гарантує, що кожна карта KPI або графік тренду виглядає і працює однаково у будь-якій частині системи, що критично важливо для професійного сприйняття інженерного програмного забезпечення та зниження витрат на розробку нових функцій.</p>
    </div>
</div>

<!-- SECTION 02: ATOMIC DESIGN MATHEMATICAL FORMALIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математична формалізація атомарного інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <p>Атомарна побудова інтерфейсу описується як функціональна суперпозиція компонентів різного рівня абстракції:</p>
        
        <h4>1. Рівняння композиції інтерфейсу ($\mathbf{View}$)</h4>
        <p>Кожне повносторінкове представлення ($\mathbf{View}$) будується шляхом композиції молекулярних ($\mathbf{M}$) та атомарних ($\mathbf{A}$) компонентів, об'єднаних функцією макетування $\mathcal{C}$:</p>
        $$\mathbf{View} = \mathcal{C}\left(\sum_{j=1}^{K} \mathbf{M}_j + \sum_{i=1}^{N} \mathbf{A}_i\right)$$
        <p>де:</p>
        <ul>
            <li>$\mathbf{A}_i$ — атомарні елементи (типові кольорові токени, CSS-шрифти Orbitron, іконки).</li>
            <li>$\mathbf{M}_j$ — молекулярні блоки (віджети <code>make_health_bar</code>, спідометр <code>render_gauge</code>, графік Dual-Axis).</li>
            <li>$\mathcal{C}$ — оркестратор розміщення (контейнери Streamlit columns, popovers, tabs).</li>
        </ul>

        <h4>2. Вектор глобальної колірної схеми ($\mathbf{Theme}$)</h4>
        <p>Для збереження 100% когнітивної цілісності, кожен компонент споживає єдиний вектор параметрів теми, імпортований з <code>styles.py</code>:</p>
        $$\mathbf{Theme} = \langle \text{Primary}, \text{Secondary}, \text{Background}, \text{Text}, \text{Glow} \rangle$$
        <p>Це гарантує, що неонові відтінки та Glassmorphism ефекти синхронізовані по всій екосистемі ATLAS.</p>
    </div>
</div>

<!-- SECTION 03: COMPONENTS ARCHITECTURE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Архітектурна схема хаба (Architecture Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    VIEWS("UI Views (forecast, map, consumption)") --> HUB("Components Hub (components/__init__.py)")
    
    HUB --> CARDS("cards.py: KPI Cards, Gauges, Health Bars")
    HUB --> CHARTS("charts/ sub-package: Line, Boxplot, Scatter, Sankey")
    HUB --> STYLES("styles.py: CSS Theming, CRT Scanlines, Google Fonts")
    
    CARDS --> ATOMIC("Atomic Visual Units")
    CHARTS --> ATOMIC
    STYLES --> ATOMIC
    
    ATOMIC --> UI("Unified Cyber-HUD Interface")
    </div></div>
</div>

<!-- SECTION 04: COMPONENT DISPATCHER MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця диспетчеризації компонентів</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль коду</th>
                    <th>Експортовані функції</th>
                    <th>Роль у системі Cyber-HUD</th>
                    <th>Ключова залежність</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>cards.py</code></td><td><code>make_health_bar</code>, <code>render_gauge</code></td><td>Візуальний контроль технічного стану підстанцій, спідометр сумарного навантаження</td><td>Streamlit, HTML Injection</td></tr>
                <tr><td><code>charts/</code></td><td><code>render_dual_axis_chart</code>, <code>render_rhythm_chart</code>, <code>px.line</code>, <code>go.Sankey</code></td><td>Візуалізація ШІ-прогнозів, регресії, теплових карт та потоків потужності</td><td>Plotly Express & GO</td></tr>
                <tr><td><code>styles.py</code></td><td><code>inject_custom_css</code>, <code>set_page_configuration</code></td><td>Застосування CRT-ефекту ліній сканування, підключення Google Fonts, неонових градієнтів</td><td>Streamlit Markdown (Unsafe HTML)</td></tr>
                <tr><td><code>__init__.py</code></td><td>Центральний простір імен (Namespace)</td><td>Зручний ре-експорт та єдиний імпорт для всіх представлень сторінок</td><td>Python Package Registry</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: GLOBAL STYLE CONSISTENCY (UI UNIFORM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Глобальна цілісність стилів (UI Uniform)</h2></div>
    <div class="glass-card flow-step">
        <p>Хаб компонентів є "Охоронцем" візуальної ідентичності ATLAS. Через <code>__init__.py</code> ми гарантуємо, що будь-який новий компонент, доданий у систему, наслідує глобальні стилі з <code>styles.py</code>. Це стосується колірних палітр, шрифтів <b>Orbitron</b> та <b>Roboto Mono</b>, а також специфічних для Cyber-HUD ефектів Glassmorphism та CRT scanlines. Така стандартизація робить інтерфейс ATLAS цілісним та професійним, усуваючи "візуальний хаос", характерний для неструктурованих проєктів.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Хаба (Components Hub & Styling Engine)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>PACKAGE src.ui.components:
    1. // [INIT & EXPOSE PUBLIC API]
       IMPORT make_health_bar, render_gauge FROM src.ui.components.cards
       IMPORT inject_custom_css, get_font_families FROM src.ui.components.styles
       
    2. // [ATOMIC THEME INJECTOR]
       FUNCTION initialize_design_system():
           // Fetch fonts from Google API
           inject_google_web_fonts("Orbitron", "Roboto Mono", "Inter")
           // Apply CRT CRT monitor glow & scanlines mask
           inject_css_variables({
               "--bg-color": "#0d1117",
               "--accent": "#3b82f6",
               "--glow": "0 0 10px rgba(59, 130, 246, 0.5)",
               "--border": "1px solid rgba(255,255,255,0.08)"
           })
           
    3. // [MOLECULAR PROGRESS BAR GENERATOR]
       FUNCTION create_health_indicator(score):
           IF score &gt; 85:
               RETURN f"&lt;span style='color:green;'&gt;🟢 Excellent ({score}%)&lt;/span&gt;"
           ELSE IF score &gt; 60:
               RETURN f"&lt;span style='color:orange;'&gt;🟡 Warning ({score}%)&lt;/span&gt;"
           ELSE:
               RETURN f"&lt;span style='color:red;'&gt;🔴 Critical ({score}%)&lt;/span&gt;"
END PACKAGE</code></pre>
    </div>
</div>

<!-- SECTION 07: USER-CENTRIC DESIGN COHESION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Користувацька цілісність дизайну</h2></div>
    <div class="glass-card flow-step">
        <p>З точки зору чергового оператора, хаб компонентів забезпечує <b>Передбачуваність</b>. Якщо він бачить червоний колір на картці KPI, він знає, що цей самий відтінок червоного буде використаний на графіку помилок і на карті підстанцій. Така когнітивна консистентність є критичною для систем моніторингу реального часу, оскільки вона дозволяє мозку оператора швидше розпізнавати патерни небезпеки та приймати вірні рішення без додаткових зусиль на дешифрування інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 08: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4><a href="ui_design_system.md">styles.py</a></h4>
                <p>Дизайн-система Cyber-HUD, яка забезпечує шрифти, CSS-змінні та ефекти освітлення для всіх компонентів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4><a href="ui_views_registry.md">Views Registry</a></h4>
                <p>Головний клієнт хаба, який використовує спільні картки та графіки для побудови аналітичних сторінок.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Engine</h4>
                <p>Низькорівневий рендеринг графічних примітивів, що споживає кольорові HSL токени дизайн-системи.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 09: ROADMAP TO v3.0 (DYNAMIC THEME SWITCHER) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Дорожня карта v3.0 (Dynamic Theme Switcher)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 заплановано:</p>
        <ul>
            <li><b>Dynamic Theming:</b> Можливість гарячого перемикання тем інтерфейсу (наприклад, "Cyber-HUD Neon" на "Classic Paper Light") без перевантаження сервера Streamlit.</li>
            <li><b>Components Playground:</b> Сторінка в Атласі для ізольованого тестування та калібрування нових віджетів на синтетичних даних.</li>
            <li><b>Custom CSS Exporter:</b> Експорт CSS-стилів дизайн-системи для інтеграції з іншими супутніми сервісами енергохолдингу.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">FAQ: Технічні особливості Хаба</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Чому не рекомендується писати окремі стилі inline CSS у представленнях?</b><br>
        A: Inline CSS порушує принцип атомарності та ускладнює підтримку коду. Якщо в майбутньому колірний код проєкту ATLAS зміниться, розробнику доведеться шукати inline-стилі по десятках файлів, тоді як при роботі через Хаб та <code>styles.py</code> зміна вноситься в одному рядку.</p>
        <p><b>Q: Як працює ре-експорт у __init__.py?</b><br>
        A: Замість того, щоб у повносторінковому View писати довгі імпорти:
        <code>from src.ui.components.cards import make_health_bar</code>
        можна написати компактний імпорт:
        <code>from src.ui.components import make_health_bar</code>,
        це спрощує читання та захищає від зсувів шляхів під час рефакторингу.</p>
        <p><b>Q: Які шрифти використовуються і як вони підключаються?</b><br>
        A: Шрифти Orbitron (для заголовків та цифр у стилі електронного табло) та Inter (для читабельного тексту) підключаються через Google Web Fonts API шляхом динамічного впровадження <code>st.markdown(&lt;style&gt; @import url(...) &lt;/style&gt;, unsafe_allow_html=True)</code>.</p>
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
