# Технічна специфікація: Система Дизайну та Візуальної Ідентичності (DESIGN SYSTEM ENGINE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AESTHETIC CORE | CYBER-HUD DESIGN SYSTEM</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Дизайн-Система</h1>
            <p class="mega-subtitle">Ядро візуальної ідентичності проєкту ATLAS: глибока кастомізація Streamlit через CSS-ін'єкції, неонова стилізація віджетів, приховування системних елементів та глобальна синхронізація кольорів</p>
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
        <p>Модуль <code>styles.py</code> є "Душею" проєкту ATLAS. В світі аналітичного ПЗ дизайн часто приноситься в жертву функціональності. Наша філософія базується на <b>Естетичному Професіоналізмі</b>: ми перетворили стандартний інтерфейс Streamlit на футуристичний Cyber-HUD. Використання темних градієнтів, напівпрозорих елементів (Glassmorphism) та неонових акцентів не лише створює premium-вигляд, а й знижує втому очей оператора при тривалому моніторингу (24/7), фокусуючи увагу на критично важливих метриках через правильну ієрархію кольорів та контрастність.</p>
    </div>
</div>

<!-- SECTION 02: STYLE INJECTION PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр ін'єкції стилів (CSS Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    INIT("init_page_config()") --> P_CONF("Set Title, Icon, Wide Layout, Expanded Sidebar")
    P_CONF --> PLOTLY("Sync Plotly Theme (plotly_dark globally)")
    
    CSS("apply_custom_css()") --> INJECT("st.html(style_tag)")
    
    INJECT --> MASK("Mask System UI (data-testid='stHeader', data-testid='stDecoration')")
    INJECT --> SIDE("Style Sidebar (Gradients #0d1117 -> #161b22, custom headers)")
    INJECT --> NAV("Style Radio Navigation (Hide radio bubbles, apply custom tabs)")
    INJECT --> WIDGETS("Style Inputs (Selectbox, DateInput, custom borders)")
    INJECT --> SPINNER("Hide default Streamlit Spinner [data-testid='stSpinner']")
    
    MASK --> RENDER("Final Premium Aesthetic Cyber-HUD UI")
    SIDE --> RENDER
    NAV --> RENDER
    WIDGETS --> RENDER
    SPINNER --> RENDER
    </div></div>
</div>

<!-- SECTION 03: CYBER-HUD COMPONENTS STYLING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стилізація компонентів Cyber-HUD</h2></div>
    <div class="glass-card flow-step">
        <p>Для досягнення унікального вигляду ми радикально переробили стандартні елементи Streamlit:</p>
        <ul>
            <li><b>Top Navigation (Tabs UI):</b> Радіо-групи Streamlit перетворені на сучасний таб-бар. Ми повністю приховали стандартні кружечки вибору за допомогою <code>div[role="radiogroup"] label > div:first-child { display: none !important; }</code> та додали ефекти <code>transform: translateY(-2px)</code> та градієнтного світіння <code>box-shadow</code> при активності та наведенні.</li>
            <li><b>Glass Sidebar:</b> Сайдбар отримав глибоку градієнтну заливку <code>#0d1117 -> #161b22</code> з ледь помітною правою межею завдяки <code>border-right: 1px solid rgba(255, 255, 255, 0.05)</code>, що запобігає зливанню областей.</li>
            <li><b>Neon Primary Buttons:</b> Кнопка "Оновити дані" (Refresh) у сайдбарі використовує градієнт <code>linear-gradient(135deg, #1f6feb 0%, #114e9e 100%)</code> з ефектом <code>box-shadow: 0 4px 12px rgba(31, 111, 235, 0.25)</code> для неонового світіння та плавної анімації при ховері.</li>
            <li><b>Custom Inputs:</b> Селектори та вибір дат отримали мікро-рамки <code>rgba(255, 255, 255, 0.1)</code> та плавне підсвічування блакитним кольором <code>#58a6ff</code> при взаємодії.</li>
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
                    <th>Дизайн-токен (CSS)</th>
                    <th>Колір (HEX / RGBA)</th>
                    <th>Роль у системі дизайну</th>
                    <th>Елементи застосування</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Background Core</td><td>#05070a</td><td>Глибокий чорний космічний тон</td><td>Основний фон сторінки</td></tr>
                <tr><td>Sidebar Dark</td><td>#0d1117 -> #161b22</td><td>Темний градієнт для навігаційного блоку</td><td>Панель фільтрів st.sidebar</td></tr>
                <tr><td>Accent Primary</td><td>#1f6feb</td><td>Брендовий синій колір високої яскравості</td><td>Активні кнопки, активні вкладки навігації</td></tr>
                <tr><td>Accent Secondary</td><td>#58a6ff</td><td>Світло-блакитний для приємних підсвічувань</td><td>Селектори при ховері, заголовки сайдбару</td></tr>
                <tr><td>Neon Success</td><td>#22c55e (0.2 alpha)</td><td>Зелений індикатор безпеки та норми</td><td>Безпечні зони навантаження Gauge-спідометрів</td></tr>
                <tr><td>Neon Warning</td><td>#f59e0b (0.2 alpha)</td><td>Помаранчевий індикатор перед-аварійного стану</td><td>Попереджувальні зони, середні навантаження</td></tr>
                <tr><td>Neon Danger</td><td>#ef4444 (0.2 alpha)</td><td>Червоний індикатор критичного стану</td><td>Аварійні сигнали, зони критичного перевантаження</td></tr>
                <tr><td>Border Low-alpha</td><td>rgba(255,255,255,0.08)</td><td>Легкі скляні кордони для ефекту Glassmorphism</td><td>Вкладки, картки KPI, рамки віджетів</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: SYSTEM UI MASKING (GHOST-FREE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Маскування системного UI (Ghost-free)</h2></div>
    <div class="glass-card flow-step">
        <p>Одним із найважливіших завдань <code>styles.py</code> є перетворення Streamlit-скрипта на повноцінний автономний додаток. Для цього застосовуються спеціальні селектори маскування:</p>
        <pre><code class="language-css">/* Приховування смужки збирання та налаштувань Streamlit */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    background: transparent !important;
}
div[data-testid="stDecoration"] {
    display: none !important;
}
/* Приховування стандартного футера */
footer {
    visibility: hidden;
}
/* Приховування стандартного спінера */
[data-testid="stSpinner"] {
    display: none !important;
}</code></pre>
        <p>Це усуває візуальний шум, приховує технічні деталі платформи та створює ефект повністю кастомного ПЗ для операційного центру.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE & AST DETAILS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Стилів (UI Engine Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code class="language-python"># Ініціалізація та кастомізація стилів (styles.py)
FUNCTION init_page_config():
    1. INVOKE Streamlit page config setting:
           st.set_page_config(
               page_title="Energy Monitor ULTIMATE",
               layout="wide",
               page_icon="⚡",
               initial_sidebar_state="expanded"
           )
    2. SET Plotly dark theme globally:
           plotly.io.templates.default = "plotly_dark"
END FUNCTION

FUNCTION apply_custom_css():
    1. PREPARE CSS block containing style overrides:
           - Reduce top padding: .block-container { padding-top: 1.5rem; }
           - Increase metric values size to 1.8rem
           - Hide footer, spinner, and stDecoration decoration strip
           - Inject Sidebar linear gradient and custom typography styles (Inter font)
           - Transform st.radio group into fully functional Tab-Bar
           - Format selectboxes and dates borders (all transitions 0.2s-0.25s)
    2. INJECT CSS code into streamlit:
           st.html("<style> ... </style>")
END FUNCTION

FUNCTION setup_streamlit_page():
    1. CALL init_page_config()
    2. CALL apply_custom_css()
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: PLOTLY SYNCHRONIZATION ALGORITHMS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Алгоритми синхронізації Plotly (Visual Sync)</h2></div>
    <div class="glass-card flow-step">
        <p>Для того, щоб аналітичні графіки виглядали як рідна частина Cyber-HUD інтерфейсу, модуль <code>styles.py</code> виконує глобальне налаштування <code>plotly.io.templates.default = "plotly_dark"</code>. Це автоматично змінює колір фону графіків, осей та сітки на темний.</p>
        <p>Крім того, в аналітичних модулях (таких як <code>cards.py</code> та <code>forecast_plots.py</code>) Plotly-фігури додатково налаштовуються з параметром <code>paper_bgcolor="rgba(0,0,0,0)"</code> (прозорий фон), що унеможливлює виникнення сірих прямокутників і плавно інтегрує чарти у скляні картки.</p>
    </div>
</div>

<!-- SECTION 08: GLASSMORPHISM & DEPTH EFFECTS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Ефекти Glassmorphism та Глибини</h2></div>
    <div class="glass-card flow-step">
        <p>Ми активно використовуємо властивості <code>rgba</code> з низьким рівнем непрозорості для створення ефекту матового скла:</p>
        <ul>
            <li>Контейнери віджетів та селекторів мають <code>background-color: rgba(255, 255, 255, 0.02)</code>.</li>
            <li>Це дозволяє градієнтам фону ледь помітно просочуватися крізь елементи управління, додаючи інтерфейсу глибини, характерної для Sci-Fi приладових панелей.</li>
            <li>Вирівнювання кордонів товщиною <code>1px</code> з м'якими кутами <code>border-radius: 8px / 10px</code> завершує вигляд скляних панелей.</li>
        </ul>
    </div>
</div>

<!-- SECTION 09: TYPOGRAPHY & BRANDING IDENTITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Типографіка та Шрифтова Ієрархія</h2></div>
    <div class="glass-card flow-step">
        <p>Особливу увагу приділено шрифтам. Системний сайдбар та заголовки стилізовані з використанням сучасного гротеску <b>Inter</b>:</p>
        <ul>
            <li>Заголовки сайдбару переведені в режим <code>text-transform: uppercase</code>, мають насиченість <code>font-weight: 700</code> та збільшений міжлітерний інтервал <code>letter-spacing: 0.05rem</code>.</li>
            <li>Для акцентних заголовків та метрик застосовується спеціальний розмір <code>1.8rem</code> для забезпечення читабельності на відстані 2-3 метрів (актуально для моніторів диспетчерських пунктів).</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: USER COGNITIVE LOAD REDUCTION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Зниження когнітивного навантаження</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки приховуванню стандартних кружечків вибору у радіо-кнопках, ми перетворили вибір вкладок на повноцінний "Таб-бар". Колірний акцент на активній вкладці з неоновим ефектом <code>box-shadow: 0 5px 20px rgba(31, 111, 235, 0.4)</code> чітко вказує оператору на поточний контекст аналітики, мінімізуючи час на орієнтацію в інтерфейсі.</p>
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
                <p>Низькорівневий двигун глобальної стилізації аналітичних графіків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>Streamlit Core</h4>
                <p>Базове середовище для ін'єкції кастомних HTML/CSS блоків через st.html.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖋️</div>
            <div class="role-content">
                <h4>Google Fonts</h4>
                <p>Зовнішня шрифтова бібліотека для забезпечення преміальної типографіки (Inter / Orbitron).</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (DYNAMIC ACCENT COLORS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Dynamic Accents)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Динамічних акцентних тем</b>:</p>
        <ul>
            <li>Інтерфейс буде автоматично змінювати свій основний акцентний колір (Accent) залежно від загального стану здоров'я енергомережі:
                <ul>
                    <li><span style="color: #1f6feb;"><b>Blue (Safe):</b></span> Навантаження в нормі, аварії відсутні.</li>
                    <li><span style="color: #f59e0b;"><b>Yellow (Alert):</b></span> Навантаження > 90% на окремих вузлах.</li>
                    <li><span style="color: #ef4444;"><b>Red (Critical):</b></span> Зафіксовано активні аварії чи знеструмлення.</li>
                </ul>
            </li>
            <li>Реалізація перемикача стилів (Custom Themes Manager) з темами "Deep Space", "Neon Night" та "Monochrome Lab".</li>
        </ul>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Дизайн та Стилі</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому я не бачу стандартне меню Streamlit зверху справа?</b><br>— Ми повністю приховали його та верхню декоративну смужку, щоб надати ATLAS вигляду преміального автономного програмного продукту.</p>
        
        <p><b>Чому графіки Plotly іноді мають сірий фон?</b><br>— Перевірте, чи встановлено параметр <code>paper_bgcolor="rgba(0,0,0,0)"</code> у налаштуваннях макета вашої Plotly-фігури. Це обов'язкова умова для ефекту прозорості.</p>
        
        <p><b>Чи можу я змінити брендовий синій колір?</b><br>— У поточній версії 2.1 колір зафіксований в CSS-коді <code>styles.py</code> для збереження фірмового стилю. Можливість кастомізації з'явиться у версії 3.0.</p>
        
        <p><b>Чому приховується st.spinner?</b><br>— Стандартний спінер Streamlit створює непотрібне мерехтіння на екрані та зміщує елементи інтерфейсу при швидких оновленнях фрагментів. Замість нього використовуються тихі фонові фрагменти.</p>
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
