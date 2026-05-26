# Технічна специфікація: Система Інтерактивної Заставки та Ініціалізації (ACTIVE BOOT SEQUENCE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ACTIVE BOOTLOADER | CYBER-HUD IMMERSION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎬</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Заставка та Ініціалізація</h1>
            <p class="mega-subtitle">Система візуального завантаження проєкту у стилі "Cyber-HUD": інтерактивний вибір джерела даних, анімований процес ініціалізації з CRT-ефектами та покрокове логування завантаження ML-ресурсів</p>
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
        <p>Модуль <code>splash.py</code> є "Обличчям" та "Входом" до проєкту ATLAS. В професійних системах очікування завантаження важких даних та ШІ-моделей (особливо при роботі з хмарними інстансами, що засинають) може бути тривалим. Наша філософія базується на <b>Цифровому Зануренні (Immersion)</b>: ми перетворили технічний процес ініціалізації на інтерактивне візуальне шоу у стилі кіберпанку. Це не лише маскує час очікування, а й створює premium-атмосферу високотехнологічного центру керування енергосистемою, підвищуючи довіру користувача до системи ще до появи перших графіків.</p>
    </div>
</div>

<!-- SECTION 02: BOOT SEQUENCE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема процесу ініціалізації (Boot Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("Application Entry (app.py)") --> STATE_CHECK{"Is db_mode in session?"}
    
    STATE_CHECK -- "No" --> RENDER_CARD("Render Energy Core Selection Card")
    RENDER_CARD --> PROTOCOL_CHOICE{"User Selection Button Click?"}
    
    PROTOCOL_CHOICE -- "🏠 LOCAL NODE" --> SET_LOCAL("st.session_state.db_mode = 'local'")
    PROTOCOL_CHOICE -- "🌐 CLOUD NEON" --> SET_CLOUD("st.session_state.db_mode = 'cloud'")
    
    SET_LOCAL --> RERUN_BOOT("Trigger st.rerun()")
    SET_CLOUD --> RERUN_BOOT
    
    STATE_CHECK -- "Yes" --> INJECT_HTML("Inject CSS overlays & Scanline mask template")
    RERUN_BOOT --> INJECT_HTML
    
    INJECT_HTML --> BOOT_GEN("Invoke get_active_boot_data_generator()")
    BOOT_GEN --> LOOP_GEN("Loop iterations: msg, progress_pct, current_data")
    
    LOOP_GEN --> LOGS_RENDER("Accumulate log messages into HTML lines")
    LOGS_RENDER --> WIDTH_UPDATE("Update Progress Bar CSS width (0% -> 100%)")
    WIDTH_UPDATE --> TIME_DELAY("Apply time.sleep(0.1) for smoothness")
    
    TIME_DELAY --> FINISH_CHECK{"Is progress 100%?"}
    FINISH_CHECK -- "No" --> LOOP_GEN
    FINISH_CHECK -- "Yes" --> SPACER_PAUSE("Sleep(0.5) to let user view success")
    
    SPACER_PAUSE --> CLEAR_CONTAINER("Call placeholder.empty() to clear splash")
    CLEAR_CONTAINER --> RET_DATA("Return final_data to Main Dashboard")
    </div></div>
</div>

<!-- SECTION 03: INTERACTIVE SELECTION INTERFACE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Інтерфейс інтерактивного вибору протоколу</h2></div>
    <div class="glass-card flow-step">
        <p>Першим етапом завантаження є вибір джерела бази даних. Ми розробили спеціальну картку <b>Energy Core Selection</b>, яка з'являється, якщо у поточній сесії відсутні налаштування з'єднання:</p>
        <ul>
            <li><b>LOCAL NODE:</b> Використовує локальну базу даних SQLite. Ідеально для швидкого старту та локального тестування ШІ.</li>
            <li><b>CLOUD NEON:</b> Підключення до масштабованої хмарної інфраструктури PostgreSQL Neon. Забезпечує доступ до загальних глобальних вимірювань.</li>
            <li><b>Visual Feedback:</b> При наведенні кнопки підсвічуються яскравим неоновим світінням (Blue/Green), а після натискання вибір записується у <code>session_state</code> і запускається перезбірка.</li>
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
                    <th>Компонент стилю</th>
                    <th>Специфічні властивості CSS</th>
                    <th>Естетичний вплив на користувача</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Scanlines & CRT</b></td><td><code>linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%)</code> з субпікселями RGB</td><td>Створює реалістичний ефект старого CRT-монітора (електронно-променевої трубки).</td></tr>
                <tr><td><b>Logo box</b></td><td><code>border: 1px solid #00ff88; border-left: 5px solid #00ff88</code>, неоновий box-shadow</td><td>Привертає увагу, підтверджує успішну ініціалізацію завантажувача (Bootloader).</td></tr>
                <tr><td><b>Logs stream</b></td><td>Анімація <code>fadeIn 0.2s forwards</code> з префіксом <code>&gt;</code> перед кожним рядком</td><td>Імітує живе логування комп'ютерного терміналу при читанні системного ядра.</td></tr>
                <tr><td><b>Progress Bar</b></td><td>Неонова смуга <code>height: 2px</code> з яскравим розмитим світінням (glow)</td><td>Наочна оцінка ступеня готовності системи до переходу в робочий режим.</td></tr>
                <tr><td><b>Typography</b></td><td>Шрифти Orbitron (для заголовків) та Roboto Mono (для логів)</td><td>Створює відчуття роботи з суворим військовим або промисловим терміналом.</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: DATA-DRIVEN PROGRESS TRACKING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Відстеження прогресу на основі даних</h2></div>
    <div class="glass-card flow-step">
        <p>Заставка в <code>splash.py</code> не є штучною анімацією. Вона тісно пов'язана з **патерном Генератора (Generator Pattern)**:</p>
        <ul>
            <li>Функція ітерує через реальний процес завантаження даних <code>get_active_boot_data_generator()</code>.</li>
            <li>Кожна завершена операція на сервері (зчитування таблиці підстанцій, зшивання профілів навантаження, ініціалізація ваг моделей LSTM) генерує реальний текстовий рядок-лог та збільшує відсоток прогресу.</li>
            <li>Це гарантує, що 100% на екрані відповідають 100% готовності об'єктів у пам'яті, виключаючи "фальшиві" таймери очікування.</li>
        </ul>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE & DETAILS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Заставки (Splash Core Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code class="language-python"># Ініціалізація та CRT-заставка (splash.py)
FUNCTION show_boot_sequence():
    1. STAGE 1: PROTOCOL PROTOCOL PROTOCOL SELECTION
           IF "db_mode" NOT in st.session_state:
               # Inject interactive CSS font & container definitions
               InjectSelectionCSS()
               
               # RENDER CARD
               st.markdown("<div class='select-card'>...</div>")
               
               c1, c2 = st.columns(2)
               IF c1.button("🏠 LOCAL NODE"):
                   st.session_state["db_mode"] = "local"
                   st.rerun()
               IF c2.button("🌐 CLOUD NEON"):
                   st.session_state["db_mode"] = "cloud"
                   st.rerun()
               st.stop() # Wait for interaction
               
    2. STAGE 2: CRT INITIALIZATION
           placeholder = st.empty() # Create dynamic overlay container
           log_accumulator = ""
           final_data = {}
           
           db_mode = st.session_state["db_mode"]
           cluster_label = "NEON-CLOUD-CENTRAL" IF db_mode == "cloud" ELSE "LOCAL-DEVELOPMENT-NODE"
           
    3. STAGE 3: DATA GENERATION ITERATION
           FOR msg, progress_pct, current_data IN get_active_boot_data_generator():
               # Add log message with CSS fade-in animation
               log_accumulator += f'<div class="log-line">{msg}</div>'
               
               # Substitute placeholders in HTML template
               html_frame = HTML_TEMPLATE.replace("LOGS_PLACEHOLDER", log_accumulator)
                                          .replace("PROGRESS_PLACEHOLDER", str(progress_pct))
                                          .replace("NEON-CLOUD-UKRAINE-01", cluster_label)
                                          
               # Render template inside placeholder container
               placeholder.markdown(html_frame, unsafe_allow_html=True)
               final_data = current_data
               
               # Small delay (0.1s) for smooth visual reading of logs
               time.sleep(0.1)
               
    4. STAGE 4: TRANSITION PHASE
           time.sleep(0.5) # Let user view "100% INITIALISED" status
           placeholder.empty() # Destroy splash container completely
           
    5. RETURN final_data to Main Controller
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: CRT SCANLINE & GLITCH EFFECTS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Ефекти CRT-монітора та сканування</h2></div>
    <div class="glass-card flow-step">
        <p>Для посилення візуального ефекту ми використовуємо складні CSS-маски. Псевдоелемент <code>::before</code> над контейнером заставки створює сітку скануючих ліній, що рухаються. Поєднання градієнтів RGB-субпікселів та затемнення кожного другого рядка пікселів створює автентичне відчуття роботи з терміналом 80-х років, інтегрованим у сучасний інтерфейс. Це додає проєкту ATLAS унікальної візуальної ідентичності.</p>
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
                <h4>database.loader</h4>
                <p>Провайдер ітератора процесу завантаження даних (get_active_boot_data_generator).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>Google Fonts API</h4>
                <p>Зовнішнє джерело футуристичної та термінальної типографіки (Orbitron / Roboto Mono).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>Streamlit Empty Container</h4>
                <p>Контейнер для динамічної повної підміни HTML-вмісту заставки без залишків.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (BIOMETRICS & VOICE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Voice & Glitch FX)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження нових іммерсивних фіч:</p>
        <ul>
            <li><b>Синтез привітання:</b> Голосовий синтезатор буде вимовляти: "ATLAS Core Initialised. Welcome back, commander" після успішного завантаження.</li>
            <li><b>Glitch-ефекти:</b> Додавання мікро-глітчів та перешкод при критичних попередженнях зв'язку з базою Neon.</li>
            <li><b>Користувацькі скіни:</b> Можливість вибору колірної палітри завантаження (Amber CRT, Green Phosphor, Cyber-Blue).</li>
        </ul>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Заставка та Ініціалізація</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому завантаження зупиняється на 50% і далі не рухається?</b><br>— Найчастіше це сигналізує про проблеми зв'язку з хмарною базою даних Neon ( PostgreSQL). Система очікує відповіді драйвера. Перевірте статус з'єднання.</p>
        
        <p><b>Як скинути вибір джерела бази даних (db_mode)?</b><br>— Очистіть кеш-кукі вашого браузера або перезапустіть Streamlit сесію. Вибір скинеться і ви знову побачите картку вибору Energy Core.</p>
        
        <p><b>Чи можу я пропустити заставку, щоб не чекати?</b><br>— Заставка не є декоративним елементом. Під час її відображення відбувається реальне завантаження даних у пам'ять RAM. Вона зникне автоматично, як тільки дані будуть готові.</p>
        
        <p><b>Чому на екрані вибору кнопок немає звичної шапки Streamlit?</b><br>— Ми повністю маскуємо стандартний інтерфейс на етапі ініціалізації для забезпечення повного візуального занурення в Cyber-HUD стиль.</p>
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
