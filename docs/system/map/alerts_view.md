# Технічна специфікація: Центр Керування Аваріями (ALERTS & INCIDENT VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">INCIDENT LIFECYCLE | EMERGENCY DISPATCH</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Керування Аваріями</h1>
            <p class="mega-subtitle">Централізований інтерфейс обробки критичних подій: реєстрація інцидентів, моніторинг життєвого циклу аварій та інтерактивне управління статусами реагування</p>
            <div class="status-tags"><span class="tag tag-online">ALERTS ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">SECURITY OFFICER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">States</span><span class="metric-value">New / Ack / Resolved</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🖱️</div><div class="metric-info"><span class="metric-label">Control</span><span class="metric-value">Data Editor Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Audit</span><span class="metric-value">SQLite Persistence</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Hygiene</span><span class="metric-value">Auto-Cleanup Support</span></div></div>
</div>

<!-- SECTION 01: INCIDENT MANAGEMENT PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Управління Інцидентами</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>alerts.py</code> є "Тривожною кнопкою" проекту ATLAS. В енергетиці швидкість реакції на інцидент (від перевантаження до кібер-атаки) визначає цілісність всієї енергосистеми. Наша філософія базується на <b>Безперервності та Прозорості</b>: кожен інцидент повинен бути зафіксований, призначений відповідальному та доведений до вирішення. Ми використовуємо інтерактивні таблиці Streamlit для забезпечення "адмін-доступу" до бази даних аварій безпосередньо з інтерфейсу дашборду.</p>
    </div>
</div>

<!-- SECTION 02: INCIDENT LIFECYCLE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Життєвий цикл інциденту (Lifecycle)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    INIT("Automatic Peak/Anomalies") --> TRIGGER("Create New Alert (RED)")
    MANUAL("Manual Entry (Cyber/Fire)") --> TRIGGER
    TRIGGER --> TABLE("Incident Log Table")
    TABLE --> DISP("Dispatcher Acknowledgment (YELLOW)")
    DISP --> ACTION("Field Repair / System Reset")
    ACTION --> RESOLVE("Mark as RESOLVED (GREEN)")
    RESOLVE --> ARCHIVE("Cleanup (Auto-Delete Old)")
    </div></div>
</div>

<!-- SECTION 03: INTERACTIVE INCIDENT REGISTRATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Інтерактивна реєстрація інцидентів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль надає можливість ручного введення подій, які не можуть бути задетектовані ШІ автоматично:</p>
        <ul>
            <li><b>Cyber-Attack Reporting:</b> Можливість негайно позначити підстанцію як скомпрометовану.</li>
            <li><b>Physical Hazards:</b> Реєстрація пожеж, пошкоджень ліній або стихійних лих.</li>
            <li><b>Custom Metadata:</b> Додавання текстових описів для уточнення деталей інциденту для команди технічної підтримки.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: INCIDENT SEVERITY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця рівнів небезпеки (Visual Coding)</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Тип події</th>
                    <th>Емодзі</th>
                    <th>Дія оператора</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Overload</td><td>🟠 Overload</td><td>Перевірка графіків ШІ-прогнозу</td></tr>
                <tr><td>Critical Failure</td><td>🔴 Аварія</td><td>Виїзд ремонтної бригади</td></tr>
                <tr><td>Cyber Security</td><td>☠️ Кібер-атака</td><td>Ізоляція мережевого сегмента</td></tr>
                <tr><td>Fire / Hazard</td><td>🔥 Пожежа</td><td>Виклик служби порятунку</td></tr>
                <tr><td>Information</td><td>🔵 INFO</td><td>Планове спостереження</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: SMART STATUS EDITING (ST.DATA_EDITOR) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Розумне редагування статусів (In-place)</h2></div>
    <div class="glass-card flow-step">
        <p>Для мінімізації зайвих кліків ми використовуємо <code>st.data_editor</code>. Це дозволяє оператору змінювати статус інциденту безпосередньо в таблиці. Зміни синхронізуються з базою даних через колбек-функцію <code>save_changes</code>. При цьому система автоматично очищує емодзі перед записом у БД, зберігаючи "чистий" формат даних для подальшої машинної обробки та звітності.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Центру Керування (Alerts Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_incident_center(df_alerts):
    1. FEEDBACK: Display status toasts from session_state
    
    2. ADMIN_PANEL:
           sub = selectbox("Target Object")
           type = selectbox("Incident Type")
           IF btn_register_clicked:
               db_services.create_alert(sub, type)
               TRIGGER_REFRESH()
               
    3. LOG_EDITOR:
           df_display = apply_emojis(df_alerts)
           st.data_editor(df_display, 
               on_change=save_changes_to_db,
               columns_config={status: SelectboxColumn})
               
    4. CLEANUP:
           IF btn_cleanup_clicked:
               db_services.delete_all_but_last(10)
               TRIGGER_REFRESH()
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: AUTOMATED DATABASE HYGIENE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Автоматична гігієна бази даних</h2></div>
    <div class="glass-card flow-step">
        <p>Велика кількість логів може сповільнювати систему. <code>alerts.py</code> містить інструмент <b>Auto-Cleanup</b>. За допомогою однієї кнопки оператор може видалити всі застарілі записи, залишивши тільки 10 (або іншу кількість) останніх інцидентів. Це гарантує, що база даних залишається компактною, а інтерфейс — швидким.</p>
    </div>
</div>

<!-- SECTION 08: SESSION-BASED FEEDBACK LOOPS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Механізми зворотного зв'язку (Feedback)</h2></div>
    <div class="glass-card flow-step">
        <p>Оскільки оновлення статусів відбувається асинхронно, ми реалізували систему <code>alerts_feedback</code> через стан сесії. Після успішного запису в БД, система створює тимчасовий об'єкт у пам'яті, який при наступному рендерингу перетворюється на Toast-сповіщення ("✅ Статус оновлено!"). Це забезпечує плавність UX без зайвих перезавантажень сторінки.</p>
    </div>
</div>

<!-- SECTION 09: ACCESS CONTROL & SECURITY (ADMIN MODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Контроль доступу та безпека</h2></div>
    <div class="glass-card flow-step">
        <p>Функціонал реєстрації та очистки інцидентів виділено в окремий контейнер з візуальною рамкою. Це допомагає оператору чітко розрізняти режим "Спостереження" та режим "Активної дії". В майбутніх версіях ці елементи керування можуть бути приховані за паролем адміністратора через інтеграцію з корпоративною системою аутентифікації.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM SPACER & SCROLLING (UX FIX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Комфорт скролінгу (UX Fix)</h2></div>
    <div class="glass-card flow-step">
        <p>У нижній частині журналу подій додано технічний відступ (Spacer) висотою 300 пікселів. Це дозволяє оператору комфортно прокручувати таблицю інцидентів так, щоб нижні рядки (найсвіжіші записи) не перекривалися межами браузера, забезпечуючи повноцінний візуальний контроль над стрічкою подій.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>DB Services</h4>
                <p>Низькорівневе ядро для запису статусів та очистки логів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Database Core</h4>
                <p>Функції виконання SQL-запитів до SQLite.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>Streamlit Widgets</h4>
                <p>Компоненти Data Editor та Selectbox для керування.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (PUSH NOTIFICATIONS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Push Notifications)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступній версії планується впровадження **Push-сповіщень** у браузер та інтеграція з Telegram-ботом. Це дозволить диспетчерам отримувати критичні сповіщення навіть якщо вкладка Атласу закрита. Також буде додано підтримку <b>Електронного підпису</b> для верифікації особи оператора, який змінив статус інциденту.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Інциденти та Аварії</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чи можна видалити окрему аварію?</b> — Наразі доступна лише масова очистка застарілих записів для підтримки швидкості БД.</p>
        <p><b>Як додати свій тип аварії?</b> — Ви можете надіслати запит AI-команді на оновлення списку категорій у <code>config.py</code>.</p>
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
