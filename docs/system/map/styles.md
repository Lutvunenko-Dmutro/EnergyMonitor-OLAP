# Технічна специфікація модуля: ui/components/styles.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DESIGN SYSTEM & CYBER-HUD IDENTITY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Дизайн-Система Cyber-HUD</h1>
            <p class="mega-subtitle">Візуальний двигун проекту: глибока CSS-ін'єкція, неонова стилізація та преміальна Glassmorphism естетика</p>
            <div class="status-tags"><span class="tag tag-online">AESTHETIC PLUS</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">UI IDENTITY</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">💉</div><div class="metric-info"><span class="metric-label">Method</span><span class="metric-value">CSS Injection</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌌</div><div class="metric-info"><span class="metric-label">Theme</span><span class="metric-value">Neon Deep Dark</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">UI Guard</span><span class="metric-value">System Stealth</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Sync</span><span class="metric-value">Plotly Dark</span></div></div>
</div>

<!-- SECTION 01: VISUAL PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Cyber-HUD дизайну</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>styles.py</code> не просто "фарбує" кнопки. Він створює імерсивне середовище, в якому оператор енергосистеми відчуває себе за пультом футуристичного командного центру. Філософія Cyber-HUD базується на поєднанні глибокого чорного фону (для зниження втоми очей) з яскравими акцентними градієнтами, які виділяють критично важливу інформацію.</p>
    </div>
</div>

<!-- SECTION 02: CSS INJECTION ENGINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Двигун CSS-ін'єкції</h2></div>
    <div class="glass-card flow-step">
        <p>Для подолання стандартних обмежень лейауту Streamlit, ми використовуємо метод прямої ін'єкції стилів через <code>st.html</code>. Це дозволяє нам маніпулювати DOM-деревом на рівні селекторів <code>data-testid</code>, змінюючи поведінку та вигляд нативних віджетів.</p>
        <ul>
            <li><b>DOM Targeting:</b> Використання специфічних аттрибутів Streamlit для точкової стилізації.</li>
            <li><b>Shadow DOM Overrides:</b> Перевизначення глобальних змінних теми (Primary Color, Background).</li>
            <li><b>Layout Resilience:</b> Адаптивне налаштування відступів (padding) для максимального використання екранного простору.</li>
        </ul>
    </div>
</div>

<!-- SECTION 03: VISUAL COMPONENTS SPECIFICATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Специфікація візуальних компонентів</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    SIDEBAR("Sidebar (Deep #0D1117)") --> NAV("Navigation Labels (Neon Blue)")
    NAV --> BTN("Primary Buttons (Linear Gradient)")
    DASH("Dashboard") --> CARDS("Metric Cards (Glassmorphism)")
    CARDS --> PLOTLY("Plotly Charts (Sync Dark)")
    </div></div>
</div>

<!-- SECTION 04: GLOBAL COLOR PALETTE (PALETTE MATRIX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця кольорової палітри</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Елемент</th>
                    <th>Код кольору / Градієнт</th>
                    <th>Ефект</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Background</td><td>#0d1117</td><td>Глибокий космос (Base)</td></tr>
                <tr><td>Accent (Blue)</td><td>#58a6ff</td><td>Неонова підсвітка іконок</td></tr>
                <tr><td>Primary Button</td><td>linear-gradient(135deg, #1f6feb, #114e9e)</td><td>Ефект глибини та натискання</td></tr>
                <tr><td>Sidebar</td><td>linear-gradient(180deg, #0d1117, #161b22)</td><td>Вертикальний градієнт фокусу</td></tr>
                <tr><td>Success</td><td>#2ea043</td><td>Позитивні тренди (Eco Green)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: GLASSMORPHISM & SHADOWS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Естетика Glassmorphism</h2></div>
    <div class="glass-card flow-step">
        <p>Для створення ефекту накладених панелей використовуються напівпрозорі межі (border) та м'які тіні з розмиттям:</p>
        <div class="formula-box">
            box-shadow: 0 4px 15px rgba(88, 166, 255, 0.15);<br>
            border: 1px solid rgba(255, 255, 255, 0.08);
        </div>
        <p class="section-desc">Це дозволяє "відірвати" аналітичні віджети від фону, створюючи тривимірний простір інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 06: UI RESILIENCE & STEALTH MODE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">UI Resilience: Режим "Стелс"</h2></div>
    <div class="glass-card flow-step">
        <p>Для перетворення веб-сторінки на професійний софт, система приховує всі зайві системні елементи:</p>
        <ul>
            <li><b>Header Stealth:</b> Приховування верхньої смужки Streamlit та меню.</li>
            <li><b>Footer Hidden:</b> Видалення копірайтів для чистоти дизайну.</li>
            <li><b>Spinner Block:</b> Приховування стандартних спінерів для використання кастомних Splash-екранів.</li>
            <li><b>Decoration Hide:</b> Видалення кольорових акцентів над хедером.</li>
        </ul>
    </div>
</div>

<!-- SECTION 07: PSEUDO-CODE (CSS INJECTOR) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Псевдокод CSS-ін'єктора</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION apply_custom_css():
    DEFINE CSS_BLOCK:
        .block-container -> set padding
        [data-testid="stSidebar"] -> apply linear-gradient
        button[kind="primary"] -> set neon-shadow & transition
        div[role="radiogroup"] -> transform to custom navigation tabs
        header -> set visibility: hidden
    END DEFINE
    
    INJECT CSS_BLOCK into current HTML session
    LOG design_system_applied("Aesthetic Plus")
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 08: PLOTLY DARK SYNC STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Стратегія синхронізації Plotly Dark</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>styles.py</code> примусово встановлює глобальний шаблон <code>plotly_dark</code>. Це гарантує, що всі графіки, створені в будь-якому модулі системи, автоматично отримають темний фон, відповідні кольори осей та шрифтів без необхідності налаштування кожного окремого графіка.</p>
    </div>
</div>

<!-- SECTION 09: NAVIGATION TABS CUSTOMIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Кастомізація навігаційних табів</h2></div>
    <div class="glass-card flow-step">
        <p>Стандартні радіо-кнопки Streamlit перетворюються на сучасні навігаційні панелі через:</p>
        <ul>
            <li>Приховування круглих чекбоксів (display: none).</li>
            <li>Перетворення лейблів на кнопки з відступами та рамками.</li>
            <li>Додавання <code>hover</code> ефектів з легким зміщенням вгору (translateY).</li>
            <li>Використання акцентного градієнту для активного стану.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: RESPONSIVE DESIGN CONSIDERATIONS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Особливості адаптивного дизайну</h2></div>
    <div class="glass-card flow-step">
        <p>Стилі оптимізовані для широкоформатних моніторів диспетчерських центрів (Ultra-Wide). Використання відносних одиниць <code>rem</code> для шрифтів та <code>vh/vw</code> для деяких елементів гарантує, що HUD буде виглядати масштабованим та читабельним на екранах будь-якої роздільної здатності.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🚀</div>
            <div class="role-content">
                <h4>Main Orchestrator</h4>
                <p>Викликає ініціалізацію стилів на самому початку життєвого циклу сесії.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Dashboard UI</h4>
                <p>Базується на CSS-класах, визначених у стилях, для побудови карток метрик.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (DYNAMIC THEMING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Dynamic Theming)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>динамічної зміни тем</b> (наприклад, "Alarm Mode" з червоним пульсуючим фоном при критичних аваріях) та повна підтримка <b>SVG-іконок</b> для кожного типу підстанції.</p>
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
