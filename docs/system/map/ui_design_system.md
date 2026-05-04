# Технічна специфікація: Система Дизайну та Візуальної Ідентичності (DESIGN SYSTEM ENGINE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AESTHETIC CORE | CYBER-HUD DESIGN SYSTEM</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Дизайн-Система</h1>
            <p class="mega-subtitle">Ядро візуальної ідентичності проекту ATLAS: глибока кастомізація Streamlit через CSS-ін'єкції, неонова стилізація віджетів, приховування системних елементів та глобальна синхронізація кольорів</p>
            <div class="status-tags"><span class="tag tag-online">UI ENGINE ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">VISUAL ARCHITECT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">💉</div><div class="metric-info"><span class="metric-label">Method</span><span class="metric-value">Direct CSS Injection</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌌</div><div class="metric-info"><span class="metric-label">Theme</span><span class="metric-value">Cyber-HUD Dark</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Isolation</span><span class="metric-value">System UI Masking</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Sync</span><span class="metric-value">Plotly-to-CSS Link</span></div></div>
</div>

<!-- SECTION 01: DESIGN SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Дизайн-Системи</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>styles.py</code> є "Душею" проекту ATLAS. В світі аналітичного ПЗ дизайн часто приноситься в жертву функціональності. Наша філософія базується на <b>Естетичному Професіоналізмі</b>: ми перетворили стандартний інтерфейс Streamlit на футуристичний Cyber-HUD. Використання темних градієнтів, напівпрозорих елементів (Glassmorphism) та неонових акцентів не лише створює premium-вигляд, а й знижує втому очей оператора при тривалому моніторингу, фокусуючи увагу на критично важливих метриках через правильну ієрархію кольорів.</p>
    </div>
</div>

<!-- SECTION 02: STYLE INJECTION PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр ін'єкції стилів (CSS Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    INIT("init_page_config()") --> P_CONF("Set Page Title, Icon, Layout (Wide)")
    P_CONF --> PLOTLY("Sync Plotly Theme (plotly_dark)")
    
    CSS("apply_custom_css()") --> INJECT("st.html(style_tag)")
    
    INJECT --> MASK("Mask System UI (Header/Footer)")
    INJECT --> SIDE("Style Sidebar (Gradients/Fonts)")
    INJECT --> NAV("Style Radio Navigation (Tabs UI)")
    INJECT --> WIDGETS("Style Inputs (Select/Date/Button)")
    
    MASK --> RENDER("Final Aesthetic UI")
    SIDE --> RENDER
    NAV --> RENDER
    WIDGETS --> RENDER
    </div></div>
</div>

<!-- SECTION 03: CYBER-HUD COMPONENTS STYLING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стилізація компонентів Cyber-HUD</h2></div>
    <div class="glass-card flow-step">
        <p>Для досягнення унікального вигляду ми радикально переробили стандартні елементи:</p>
        <ul>
            <li><b>Top Navigation (Tabs):</b> Радіо-групи Streamlit перетворені на сучасні кнопки вкладок. Ми приховали стандартні кружечки вибору та додали ефекти <code>transform: translateY(-2px)</code> при наведенні, що створює відчуття глибини інтерфейсу.</li>
            <li><b>Glass Sidebar:</b> Сайдбар отримав градієнтну заливку <code>#0d1117 -> #161b22</code> з ледь помітною правою межею. Це створює ефект структурного розділення без візуального перевантаження.</li>
            <li><b>Neon Primary Buttons:</b> Кнопки "Refresh" та "Start Simulation" використовують яскраві градієнти (Blue/Green) з ефектом <code>box-shadow</code>, що імітує неонове світіння.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: CORE DESIGN TOKEN MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця дизайн-токенів (Colors & UI)</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Елемент</th>
                    <th>Значення / HEX</th>
                    <th>Роль у дизайні</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Background Core</td><td>#05070a</td><td>Глибокий чорний для контрасту</td></tr>
                <tr><td>Accent Primary</td><td>#1f6feb</td><td>Брендовий синій для активних станів</td></tr>
                <tr><td>Accent Secondary</td><td>#58a6ff</td><td>Світло-блакитний для ховерів</td></tr>
                <tr><td>Neon Success</td><td>#00ff88</td><td>Індикатор активності симуляції</td></tr>
                <tr><td>Border Low-alpha</td><td>rgba(255,255,255,0.08)</td><td>Легкі роздільники Glassmorphism</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: SYSTEM UI MASKING (GHOST-FREE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Маскування системного UI (Ghost-free)</h2></div>
    <div class="glass-card flow-step">
        <p>Одним із завдань <code>styles.py</code> є перетворення Streamlit-скрипта на повноцінний автономний додаток. Ми використовуємо CSS-селектори <code>data-testid="stHeader"</code> та <code>data-testid="stDecoration"</code> для приховування верхньої смужки Streamlit та меню. Також ми приховали стандартний футер та спінер завантаження (<code>st.spinner</code>), оскільки вони вносять візуальний шум у нашу кастомну заставку та преміальну навігацію.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Стилів (UI Engine Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION setup_design_system():
    1. INIT_PAGE_CONFIG:
           SET title = "Energy Monitor ULTIMATE"
           SET layout = "wide"
           SET plotly_theme = "plotly_dark"
           
    2. INJECT_GLOBAL_CSS:
           CSS_BLOCK = """
               .block-container { padding-top: 1.5rem; }
               footer { visibility: hidden; }
               .stSidebar { background: dark_gradient; }
               .radiogroup_labels { 
                   border-radius: 10px; 
                   hover: transform_up; 
                   active: blue_glow;
               }
           """
           st.html(CSS_BLOCK)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: PLOTLY SYNCHRONIZATION ALGORITHMS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Алгоритми синхронізації Plotly (Visual Sync)</h2></div>
    <div class="glass-card flow-step">
        <p>Для того, щоб аналітичні графіки виглядали як рідна частина інтерфейсу, модуль <code>styles.py</code> виконує глобальне налаштування <code>plotly.io.templates.default = "plotly_dark"</code>. Це автоматично змінює колір фону графіків, осей та сітки на темний. В поєднанні з нашими кастомними колірними палітрами в компонентах, це створює безшовний візуальний досвід, де дані та інтерфейс існують в єдиному світловому просторі.</p>
    </div>
</div>

<!-- SECTION 08: GLASSMORPHISM & DEPTH EFFECTS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Ефекти Glassmorphism та Глибини</h2></div>
    <div class="glass-card flow-step">
        <p>Ми активно використовуємо властивості <code>rgba</code> з низьким рівнем непрозорості для створення ефекту скла. Контейнери віджетів мають <code>background-color: rgba(255, 255, 255, 0.02)</code>. Це дозволяє ледь помітно відображати градієнти фону крізь елементи управління, що додає інтерфейсу ATLAS глибини та "дорожнечі", характерної для сучасних Apple-style або Sci-Fi інтерфейсів.</p>
    </div>
</div>

<!-- SECTION 09: RESPONSIVE PADDING & LAYOUT FIXES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Адаптивні відступи та фікси макета</h2></div>
    <div class="glass-card flow-step">
        <p>Стандартний Streamlit має досить великі відступи зверху (<code>padding-top: 6rem</code>). Модуль <code>styles.py</code> оптимізує використання екранного простору, зменшуючи цей відступ до <code>1.5rem</code>. Це дозволяє відображати більше корисної інформації на першому екрані, що особливо важливо для ситуаційних центрів, де оператор повинен бачити KPI та карту одночасно без зайвого скролінгу.</p>
    </div>
</div>

<!-- SECTION 10: USER COGNITIVE LOAD REDUCTION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Зниження когнітивного навантаження</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки приховуванню стандартних елементів управління радіо-кнопками (маленьких кружечків), ми перетворили вибір вкладок на роботу з повноцінним "Таб-баром". Це відповідає ментальній моделі користувача про сучасні веб-додатки. Колірний акцент на активній вкладці з ефектом <code>box-shadow: 0 5px 20px rgba(31, 111, 235, 0.4)</code> чітко вказує поточний контекст, не вимагаючи додаткового вчитування в текст.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>Plotly IO</h4>
                <p>Глобальний двигун стилізації для всіх аналітичних графіків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>Streamlit Core</h4>
                <p>Цільовий фреймворк для ін'єкції кастомних стилів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖋️</div>
            <div class="role-content">
                <h4>Google Fonts</h4>
                <p>Зовнішня бібліотека шрифтів (Inter) для професійної типографіки.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (DYNAMIC ACCENT COLORS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Dynamic Accents)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Динамічних акцентних кольорів</b>. Весь інтерфейс буде автоматично змінювати свій основний колір (Accent) залежно від загального стану мережі: Blue (Safe), Yellow (Alert), Red (Critical). Також буде додано підтримку <b>Custom Themes Manager</b>, що дозволить користувачам вибирати між різними варіантами Cyber-HUD (наприклад, "Deep Space", "Neon Night" або "Monochrome Lab").</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Дизайн та Стилі</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому я не бачу меню Streamlit?</b> — Ми приховали його для створення ефекту автономного софту. Всі налаштування доступні в сайдбарі.</p>
        <p><b>Як змінити основний колір інтерфейсу?</b> — Наразі колір зафіксований у <code>styles.py</code> для дотримання брендбуку ATLAS. Можливість зміни з'явиться у v3.0.</p>
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
