# Технічна специфікація: Система Інтерактивної Заставки та Ініціалізації (ACTIVE BOOT SEQUENCE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ACTIVE BOOTLOADER | CYBER-HUD IMMERSION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎬</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Заставка та Ініціалізація</h1>
            <p class="mega-subtitle">Система візуального завантаження проекту у стилі "Cyber-HUD": інтерактивний вибір джерела даних, анімований процес ініціалізації з CRT-ефектами та покрокове логування завантаження ML-ресурсів</p>
            <div class="status-tags"><span class="tag tag-online">BOOTLOADER ACTIVE</span><span class="tag tag-version">v2.8.5</span><span class="tag tag-role">SYSTEM GATEKEEPER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🎥</div><div class="metric-info"><span class="metric-label">Visuals</span><span class="metric-value">CRT / Scanline FX</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📂</div><div class="metric-info"><span class="metric-label">Selection</span><span class="metric-value">Local / Cloud Neon</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">Bootstrapping</span><span class="metric-value">Data-driven Progress</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Design</span><span class="metric-value">Orbitron / Roboto Mono</span></div></div>
</div>

<!-- SECTION 01: SPLASH SCREEN PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Інтерактивної Заставки</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>splash.py</code> є "Обличчям" та "Входом" до проекту ATLAS. В професійних системах очікування завантаження важких даних та ML-моделей може бути нудним. Наша філософія базується на <b>Цифровому Зануренні (Immersion)</b>: ми перетворили технічний процес ініціалізації на візуальне шоу у стилі кіберпанку. Це не лише маскує час очікування, а й створює premium-атмосферу високотехнологічного центру керування енергосистемою, підвищуючи довіру користувача до системи ще до появи перших графіків.</p>
    </div>
</div>

<!-- SECTION 02: BOOT SEQUENCE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема процесу ініціалізації (Boot Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("Application Entry") --> SELECT("Database Protocol Selection (UI Card)")
    SELECT -- "🏠 Local" --> BOOT("Initialize Bootloader")
    SELECT -- "🌐 Cloud" --> BOOT
    
    BOOT --> CSS("Inject Cyber-HUD CSS & CRT Effects")
    CSS --> STREAM("Get Boot Data Generator")
    
    STREAM --> LOGS("Animate Real-time Logs (> Initialising...)")
    LOGS --> BAR("Update Progress Bar (0 -> 100%)")
    BAR --> DATA("Verify Data Segments (Load, Gen, Fin...)")
    
    DATA --> FINISH("Clear Placeholder & Transition to Dashboard")
    </div></div>
</div>

<!-- SECTION 03: INTERACTIVE SELECTION INTERFACE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Інтерфейс інтерактивного вибору</h2></div>
    <div class="glass-card flow-step">
        <p>Першим етапом завантаження є вибір протоколу бази даних. Ми розробили спеціальну картку <b>Energy Core Selection</b>:</p>
        <ul>
            <li><b>LOCAL NODE:</b> Швидкий доступ до локальної бази SQLite (ідеально для офлайн-роботи).</li>
            <li><b>CLOUD NEON:</b> Підключення до масштабованої хмарної інфраструктури PostgreSQL Neon.</li>
            <li><b>Visual Feedback:</b> При виборі кнопки підсвічуються неоновим сяйвом, а дані про вибір миттєво зберігаються у <code>session_state</code> для ініціалізації відповідного драйвера.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: BOOTLOADER STYLING MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця стилізації заставки (Cyber-HUD)</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Елемент</th>
                    <th>Стиль / Технологія</th>
                    <th>Ефект для користувача</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Scanlines</td><td>CSS Linear Gradients</td><td>Ефект старого CRT-монітора</td></tr>
                <tr><td>Log Stream</td><td>Fading Keyframe Animation</td><td>Відчуття живої роботи системи</td></tr>
                <tr><td>Typography</td><td>Orbitron / Roboto Mono</td><td>Футуристичний технічний вигляд</td></tr>
                <tr><td>Color Palette</td><td>Neon Green (#00ff88) / Dark Blue</td><td>Високий контраст та "преміальність"</td></tr>
                <tr><td>Handshake</td><td>SQL Connection Metadata</td><td>Підтвердження автентичності вузла</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: DATA-DRIVEN PROGRESS TRACKING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Відстеження прогресу на основі даних</h2></div>
    <div class="glass-card flow-step">
        <p>Заставка в <code>splash.py</code> не є статичною анімацією. Вона працює через <b>Generator Pattern</b>. Функція ітерує через реальний процес завантаження даних (<code>get_active_boot_data_generator</code>). Кожна завершена операція (зчитування таблиці підстанцій, підготовка ваг моделей) генерує новий лог-запис та збільшує відсоток прогрес-бару. Це гарантує, що 100% на екрані відповідають 100% готовності даних у пам'яті.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Заставки (Splash Core)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION show_boot_sequence():
    1. STAGE_1 (Selection):
           IF 'db_mode' not in session:
               RENDER_SELECTION_CARD() # Local vs Cloud
               STOP_EXECUTION()
               
    2. STAGE_2 (Bootloader):
           placeholder = st.empty()
           logs_accumulator = ""
           FOR msg, progress, data IN boot_generator():
               logs_accumulator += "<div class='line'>" + msg + "</div>"
               html = TEMPLATE.replace(PLACEHOLDERS, logs, progress)
               placeholder.markdown(html, unsafe_allow_html=True)
               SLEEP(0.1) # Smoothness
               
    3. STAGE_3 (Transition):
           placeholder.empty()
           RETURN final_data
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: CRT SCANLINE & GLITCH EFFECTS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Ефекти CRT-монітора та сканування</h2></div>
    <div class="glass-card flow-step">
        <p>Для посилення візуального ефекту ми використовуємо складні CSS-маски. Псевдоелемент <code>::before</code> над контейнером заставки створює сітку скануючих ліній, що рухаються. Поєднання градієнтів RGB-субпікселів та затемнення кожного другого рядка пікселів створює автентичне відчуття роботи з терміналом 80-х років, інтегрованим у сучасний інтерфейс. Це додає проекту ATLAS унікальної візуальної ідентичності.</p>
    </div>
</div>

<!-- SECTION 08: BOOT METADATA & HANDSHAKE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Метадані завантаження та "Рукостискання"</h2></div>
    <div class="glass-card flow-step">
        <p>У нижній частині заставки (Footer) відображаються технічні метадані: <code>Auth Token</code>, <code>Cluster ID</code> та версія системи. Це не просто декоративні елементи — вони динамічно змінюються залежно від обраного режиму (Local vs Cloud). Це "візуальне рукостискання" (Handshake) підтверджує користувачеві, що він підключився до правильного вузла енергетичного кластера, і система готова до безпечної обробки телеметрії.</p>
    </div>
</div>

<!-- SECTION 09: USER EXPERIENCE IMMERSION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Користувацьке занурення та UX</h2></div>
    <div class="glass-card flow-step">
        <p>Використання шрифтів <b>Orbitron</b> (для заголовків) та <b>Roboto Mono</b> (для логів) вибрано не випадково. Orbitron асоціюється з науковою фантастикою та технологіями майбутнього, а Roboto Mono — з кодом та точними розрахунками. Такий типографічний контраст у поєднанні з плавною появою рядків логів створює відчуття "пробудження" складного штучного інтелекту, що є ключовим емоційним моментом при запуску Атласу.</p>
    </div>
</div>

<!-- SECTION 10: AUTOMATIC TRANSITION (PHASE-OUT) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Автоматичний перехід та вихід (Phase-out)</h2></div>
    <div class="glass-card flow-step">
        <p>Після досягнення 100% завантаження, <code>splash.py</code> виконує невелику паузу (0.5с) для фіксації результату користувачем, а потім примусово очищує <code>st.empty()</code> контейнер. Це забезпечує різкий та чистий перехід до головного дашборду без залишкових візуальних артефактів. Вся логіка заставки інкапсульована і не впливає на подальшу роботу основного інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>DB Loader</h4>
                <p>Провайдер ітератора процесу завантаження даних.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>Google Fonts</h4>
                <p>Зовнішнє джерело футуристичної типографіки (Orbitron).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>Streamlit Empty</h4>
                <p>Контейнер для динамічної підміни HTML-вмісту заставки.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (VOICE GREETING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Voice Greeting)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Голосового привітання</b>. При успішній ініціалізації система буде вітати користувача синтезованим голосом, підтверджуючи готовність до роботи. Також буде додано підтримку <b>Біометричної ініціалізації</b> (Face ID / Touch ID) безпосередньо у заставці для професійних розгортань у захищених енергоцентрах.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Заставка та Запуск</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому завантаження зупинилося на 50%?</b> — Це може означати проблему з підключенням до хмарної бази даних Neon. Перевірте статус з'єднання.</p>
        <p><b>Чи можна пропустити заставку?</b> — Заставка є частиною критичного процесу ініціалізації пам'яті; вона зникає автоматично, як тільки дані готові.</p>
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
