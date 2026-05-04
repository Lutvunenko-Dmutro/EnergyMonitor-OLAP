# Технічна специфікація модуля: ui/segments/splash.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ACTIVE BOOT SEQUENCE & UI IMMERSION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚀</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Система Запуску ATLAS</h1>
            <p class="mega-subtitle">Інтерактивна заставка та ініціалізація: Cyber-HUD естетика, CRT-ефекти, вибір джерела даних та динамічна візуалізація завантаження</p>
            <div class="status-tags"><span class="tag tag-online">BOOTLOADER ACTIVE</span><span class="tag tag-version">v2.8.5</span><span class="tag tag-role">UI IMMERSION</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Style</span><span class="metric-value">Cyber-HUD</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Boot</span><span class="metric-value">Active Sequence</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Source</span><span class="metric-value">Local vs Cloud</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📽️</div><div class="metric-info"><span class="metric-label">VFX</span><span class="metric-value">CRT Scanlines</span></div></div>
</div>

<!-- SECTION 01: UI IMMERSION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія UI-Імерсивності</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>splash.py</code> відповідає за "перше враження" від проекту ATLAS. В системах Defense Edition інтерфейс має не лише бути функціональним, а й транслювати відчуття високотехнологічного, захищеного комплексу. Сплеш-екран виконує роль імерсивного бутлоадера, який маскує складні процеси ініціалізації БД та ML-моделей за анімованим процесом "запуску енергоядра", що радикально підвищує якість сприйняття системи на захисті.</p>
    </div>
</div>

<!-- SECTION 02: ACTIVE BOOTSTRAPPING ARCHITECTURE -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Архітектура активного бутстрапінгу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("Старт Додатка") --> AUTH("Stage: Selection (Local/Cloud)")
    AUTH --> GEN("Generator Handshake")
    GEN --> LOGS("Stream: Real-time Logs")
    LOGS --> BAR("Stream: Progress Bar (%)")
    BAR --> DONE{"Завантаження завершено?"}
    DONE -- "Так" --> UI("Main Dashboard Render")
    DONE -- "Ні" --> GEN
    </div></div>
</div>

<!-- SECTION 03: CYBER-HUD AESTHETICS & CRT EFFECTS -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Cyber-HUD естетика та CRT-ефекти</h2></div>
    <div class="glass-card flow-step">
        <p>Для досягнення premium-ефекту система використовує спеціалізовані CSS-ін'єкції:</p>
        <ul>
            <li><b>CRT Scanlines:</b> Накладання напівпрозорих горизонтальних ліній та градієнтів, що імітують старі термінали управління.</li>
            <li><b>Typography:</b> Використання шрифтів <code>Orbitron</code> (для заголовків) та <code>Roboto Mono</code> (для логів завантаження).</li>
            <li><b>Glow Effects:</b> Використання <code>text-shadow</code> та <code>box-shadow</code> з неоновим відтінком <code>#00ff88</code> для створення ефекту світіння екрана.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: MULTI-SOURCE SELECTION STAGE -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Етап вибору джерела (Selection Stage)</h2></div>
    <div class="glass-card flow-step">
        <p>Першим етапом роботи модуля є вибір вузла даних (Local Node vs Cloud Neon). Це реалізовано через стилізовані картки <code>select-card</code>, які блокують подальше виконання програми до моменту прийняття рішення користувачем. Це гарантує, що ініціалізація почнеться саме з потрібним драйвером БД.</p>
    </div>
</div>

<!-- SECTION 05: DYNAMIC LOG STREAMING LOGIC -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Логіка динамічного стрімінгу логів</h2></div>
    <div class="glass-card flow-step">
        <p>Замість статичного зображення, <code>splash.py</code> відображає реальні етапи завантаження системи. Функція отримує дані з генератора <code>get_active_boot_data_generator()</code>, який повертає:</p>
        <ul>
            <li><b>Messages:</b> Текстові статуси (наприклад, "Connecting to PostgreSQL...", "Loading V3 ONNX Model...").</li>
            <li><b>Progress:</b> Відсоткове значення (0-100%).</li>
            <li><b>Data State:</b> Поточний стан завантажених об'єктів.</li>
        </ul>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (BOOT GENERATOR LOOP) -->
<div class="section-container">
    <div class="section-header":"06</span><h2 class="section-title">Псевдокод циклу бутлоадера</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION show_boot_sequence():
    1. IF "db_mode" NOT IN session:
           RENDER selection_ui (HTML/CSS)
           STOP until button_click
           
    2. INITIALIZE placeholder = st.empty()
    3. FOR msg, progress, data IN boot_generator():
           HTML = TEMPLATE.replace("LOGS", msg)
                          .replace("PROGRESS", progress)
           placeholder.markdown(HTML, unsafe_allow_html=True)
           final_data = data
           SLEEP(0.1) # Visual smoothness
           
    4. CLEAR placeholder
    5. RETURN final_data
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: CRT SCANLINE CSS SPECIFICATION -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Специфікація CRT Scanline CSS</h2></div>
    <div class="glass-card flow-step">
        <p>Ефект сканування реалізований через псевдоелемент <code>::before</code> з лінійним градієнтом:</p>
        <div class="formula-box">
            background: linear-gradient(rgba(18,16,16,0) 50%, rgba(0,0,0,0.25) 50%)
        </div>
        <p class="section-desc">Це створює ритмічне чергування темних та світлих смуг, що разом з 3px сіткою додає інтерфейсу автентичного вигляду індустріального монітора.</p>
    </div>
</div>

<!-- SECTION 08: PROGRESS BAR SYNCHRONIZATION -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Синхронізація прогрес-бару</h2></div>
    <div class="glass-card flow-step">
        <p>Прогрес-бар заставки (<code>progress-bar</code>) напряму пов'язаний з реальними етапами підготовки системи. Кожен успішно завантажений модуль (наприклад, <code>predict_v2</code>) додає фіксовану кількість відсотків до шкали, забезпечуючи чесну візуалізацію часу очікування для користувача.</p>
    </div>
</div>

<!-- SECTION 09: IMMERSIVE LOG ANIMATION -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Анімація імерсивних логів</h2></div>
    <div class="glass-card flow-step">
        <p>Кожен рядок логу завантаження з'являється з невеликою затримкою та анімацією <code>fadeIn</code>. Використання префікса <code>></code> та шрифту фіксованої ширини створює ефект роботи термінала реального часу, що підсилює технологічний образ ATLAS.</p>
    </div>
</div>

<!-- SECTION 10: MEMORY HYGIENE AFTER BOOT -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Гігієна пам'яті після запуску</h2></div>
    <div class="glass-card flow-step">
        <p>Після завершення послідовності завантаження, блок <code>placeholder.empty()</code> повністю видаляє HTML та CSS заставки з DOM-дерева сторінки. Це звільняє ресурси браузера для відображення основних графіків та карт на дашборді.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🗄️</div>
            <div class="role-content">
                <h4>DB Loader</h4>
                <p>Джерело даних та статусів для генератора завантаження.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>Google Fonts</h4>
                <p>Забезпечує шрифти Orbitron та Roboto Mono.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Streamlit Empty</h4>
                <p>Контейнер для динамічного оновлення HTML-коду.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (CUSTOM SPLASH) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v3.0 (Custom Splash)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується підтримка <b>звукових ефектів запуску</b> (Audio Boot), можливість <b>кастомізації логотипу</b> для різних замовників та впровадження <b>фонового прогріву кешу</b> (warm-up) безпосередньо під час відображення заставки.</p>
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

<!-- ACADEMIC AUDIT HISTORY -->
<div class='audit-history' style='margin-top: 50px; padding: 20px; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.8rem;'>
    <p><b>Audit ID:</b> ATH-2026-V4-FINAL</p>
    <p><b>Review Date:</b> 2026-05-04</p>
    <p><b>Status:</b> VERIFIED | DEFENSE-READY</p>
    <p><b>Note:</b> Цей модуль пройшов повну технічну верифікацію на відповідність архітектурним стандартам ATLAS.</p>
</div>
