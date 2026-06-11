# Технічна специфікація: Центр Керування Аваріями (ALERTS & INCIDENT VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">INCIDENT LIFECYCLE | EMERGENCY DISPATCH</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Керування Аваріями</h1>
            <p class="mega-subtitle">Централізований високопродуктивний інтерфейс обробки критичних подій: автоматична реєстрація інцидентів, моніторинг життєвого циклу аварій та інтерактивне управління статусами реагування</p>
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

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Управління Інцидентами</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>alerts.py</code> є "Тривожною кнопкою" проєкту ATLAS. В енергетиці швидкість реакції на інцидент (від фізичного перевантаження лінії до цілеспрямованої кібер-атаки на SCADA-систему) визначає цілісність всієї енергомережі. Наша філософія базується на <b>Безперервності та Прозорості</b>: кожен інцидент повинен бути негайно зафіксованій у базі даних, призначений відповідальному диспетчеру та доведений до повного вирішення із записом таймстемпу. Інтерактивні таблиці Streamlit дозволяють диспетчеру безпечно виконувати адміністрування бази даних аварій безпосередньо з інтерфейсу Cyber-HUD.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL STATE FORMALIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математична формалізація переходів статусів</h2></div>
    <div class="glass-card flow-step">
        <p>Для запобігання неможливим станам життєвого циклу інциденту, перехід станів описується орієнтованим графом та детермінованим кінцевим автоматом (FSM):</p>
        <p>Нехай множина станів $S \in \{S_0: \text{"NEW"}, S_1: \text{"IN PROGRESS"}, S_2: \text{"RESOLVED"}\}$, а дії оператора — $A \in \{A_{ack}: \text{"Прийняти в роботу"}, A_{res}: \text{"Вирішити"}\}$.</p>
        <p>Функція переходів $\delta(S, A)$ задається наступним чином:</p>
        $$\delta(S_0, A_{ack}) = S_1$$
        $$\delta(S_1, A_{res}) = S_2$$
        $$\delta(S_2, A_{ack}) = S_1 \quad \text{(повторне відкриття за потреби)}$$
        <p>Всі зміни записуються в базу даних за допомогою SQL транзакції, що гарантує ACID-консистентність.</p>
    </div>
</div>

<!-- SECTION 03: INCIDENT LIFECYCLE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Життєвий цикл інциденту (Lifecycle)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    INIT["Automatic Anomaly Ingestion"] --> TRIGGER("Create New Alert (Status: NEW)")
    MANUAL["Manual Entry (Operator Input)"] --> TRIGGER
    TRIGGER --> TABLE["Render in st.data_editor (🔴 NEW)"]
    TABLE --> DISP["Dispatcher Click: Acknowledge (🟡 IN PROGRESS)"]
    DISP --> ACTION["Field Response / Line Re-routing / Mitigation"]
    ACTION --> RESOLVE["Mark as RESOLVED (🟢 RESOLVED)"]
    RESOLVE --> ARCHIVE["Optional Database Cleanup (Keep last N)"]
    </div></div>
</div>

<!-- SECTION 04: INCIDENT SEVERITY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця рівнів небезпеки та кодування</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Тип події</th>
                    <th>Візуальний код (Emoji)</th>
                    <th>Пріоритет</th>
                    <th>Рекомендована дія диспетчера</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Перевантаження</b></td><td>🟠 Перевантаження</td><td><span style="color:#f59e0b">MEDIUM</span></td><td>Перевірка графіків ШІ-прогнозу, перерозподіл генерації</td></tr>
                <tr><td><b>Аварія</b></td><td>🔴 Аварія</td><td><span style="color:#ef4444">HIGH</span></td><td>Негайний виїзд ремонтної бригади на підстанцію</td></tr>
                <tr><td><b>Кібер-атака</b></td><td>☠️ Кібер-атака</td><td><span style="color:#ef4444; font-weight:bold">CRITICAL</span></td><td>Ізоляція мережевого сегмента, перехід на ручне керування</td></tr>
                <tr><td><b>Пожежа</b></td><td>🔥 Пожежа</td><td><span style="color:#ef4444; font-weight:bold">CRITICAL</span></td><td>Виклик служби порятунку (ДСНС), відключення ліній живлення</td></tr>
                <tr><td><b>Information</b></td><td>🔵 INFO</td><td><span style="color:#3b82f6">LOW</span></td><td>Плановий аналіз та пасивне спостереження за параметрами</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: SMART STATUS EDITING (ST.DATA_EDITOR) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Розумне редагування статусів (In-place)</h2></div>
    <div class="glass-card flow-step">
        <p>Для мінімізації затримок оператора ми використовуємо компонент <code>st.data_editor</code> з повним мапуванням колонок. Оператор може редагувати статус інциденту в один клік без перезавантаження всієї сторінки. Оновлення синхронізуються з базою даних через колбек-функцію <code>save_changes</code>. При цьому система автоматично очищує емодзі перед записом у БД, зберігаючи "чистий" формат даних (<code>NEW</code>, <code>ACKNOWLEDGED</code>, <code>RESOLVED</code>) для подальшої машинної обробки та ШІ-навчання.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Центру Керування (Alerts Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_incident_center(df_alerts):
    1. // [SAFE FEEDBACK LOOP]
       IF "alerts_feedback" in session_state:
           show_toast_or_error(session_state.alerts_feedback)
           delete session_state.alerts_feedback
       
    2. // [ISOLATED MANUAL ENTRY FORM]
       with container(border=True):
           substation = selectbox("Оберіть підстанцію", list_substations())
           alert_type = selectbox("Тип інциденту", ["Перевантаження", "Аварія", "Кібер-атака", "Пожежа"])
           description = text_input("Короткий опис")
           IF button_clicked("📢 Зареєструвати аварію"):
               success, msg = db_services.create_custom_alert(substation, alert_type, description)
               IF success:
                   st.toast("✅ Додано!")
                   clear_streamlit_cache()
                   trigger_rerun()
                   
    3. // [SAFE INDEX RESET & EMOJI MAPPING]
       df_display = df_alerts.reset_index(drop=True)
       df_display["alert_type"] = df_display["alert_type"].map(type_emoji_dict)
       df_display["status"] = df_display["status"].map(status_emoji_dict)
       
    4. // [INTERACTIVE GRID WITH CALLBACK]
       st.data_editor(
           df_display,
           column_config={
               "status": SelectboxColumn(options=["🔴 NEW", "🟡 IN PROGRESS", "🟢 RESOLVED"])
           },
           disabled=["alert_id", "timestamp", "substation_name", "alert_type", "description"],
           on_change=lambda: save_changes(st.session_state.edited_rows, df_alerts)
       )
       
    5. // [DATABASE HYGIENE]
       IF button_clicked("🧹 Очистка (TOP-10)"):
           db_services.cleanup_old_alerts(keep_last=10)
           clear_streamlit_cache()
           trigger_rerun()
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: AUTOMATED DATABASE HYGIENE & TRANSACTION SAFETY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Автоматична гігієна та безпека транзакцій</h2></div>
    <div class="glass-card flow-step">
        <p>Велика кількість історичних аварій може сповільнювати завантаження дашборду. Модуль містить механізм <b>Auto-Cleanup</b>. За допомогою кнопки очищення диспетчер може видалити всі застарілі вирішені інциденти, залишивши лише 10 останніх записів у SQLite БД. Процес виконується через безпечний SQL-запит:</p>
        <pre><code class="language-sql">DELETE FROM LoadAlerts 
WHERE alert_id NOT IN (
    SELECT alert_id FROM LoadAlerts 
    ORDER BY timestamp DESC LIMIT 10
);</code></pre>
        <p>Після видалення здійснюється автоматичне очищення кешу Streamlit (<code>st.cache_data.clear()</code>), що забезпечує миттєве оновлення інтерфейсу у всіх користувачів.</p>
    </div>
</div>

<!-- SECTION 08: SESSION-BASED FEEDBACK LOOPS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Механізм асинхронного зворотного зв'язку</h2></div>
    <div class="glass-card flow-step">
        <p>Оскільки редагування статусів у <code>st.data_editor</code> використовує відтерміновані колбеки, прямий виклик UI-елементів всередині функції зміни даних може призвести до збою потоку рендерингу Streamlit. Для вирішення цього ми реалізували систему <code>alerts_feedback</code> через сесію. Стан зберігає кортеж <code>(message, icon, type)</code>, який безпечно відмальовується у вигляді Toast при наступному циклі рендерингу (Boot Sequence).</p>
    </div>
</div>

<!-- SECTION 09: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4><a href="../db_services.md">db_services.py</a></h4>
                <p>Низькорівневе ядро бізнес-логіки бази даних: створення, оновлення та очистка інцидентів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4><a href="core_kernel_hub.md">src.core.database</a></h4>
                <p>Провайдер SQL-транзакцій до SQLite (база даних <code>energy.db</code>).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥</div>
            <div class="role-content">
                <h4>Streamlit Framework</h4>
                <p>Рендеринг віджетів <code>st.data_editor</code>, <code>st.toast</code> та управління станом сесії.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v3.0 (PUSH NOTIFICATIONS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v3.0 (Push Notifications)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступній версії заплановано:</p>
        <ul>
            <li><b>Real-time WebSockets:</b> Миттєве оновлення статусу без перемальовування всієї сторінки.</li>
            <li><b>Email & Push Notifications:</b> Автоматична розсилка сповіщень черговим інженерам про критичні інциденти.</li>
            <li><b>Digital Signature (ЕЦП):</b> Верифікація особи диспетчера при переведенні аварій у статус <code>RESOLVED</code>.</li>
        </ul>
    </div>
</div>

<!-- SECTION 11: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">FAQ: Технічні особливості роботи</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Чому при оновленні статусу таблиця іноді "стрибає"?</b><br>
        A: Це пов'язано з очищенням кешу Streamlit після збереження. Система оновлює дані в базі та скидає кешовані датафрейми, що вимагає одного швидкого перерендерингу для відображення актуальної інформації.</p>
        <p><b>Q: Як додати новий тип інциденту до випадаючого списку?</b><br>
        A: Списки типів жорстко закодовані в <code>src/ui/views/alerts.py</code> для відповідності базі даних. Для додавання нових типів (наприклад, "Аварія трансформатора струму") необхідно додати запис у словники <code>type_emoji</code> та валідатор форми.</p>
        <p><b>Q: Чому після зміни статусу в таблиці в БД пишеться простий текст, а не емодзі?</b><br>
        A: Це зроблено навмисно. Перед збереженням функція <code>save_changes</code> мапує візуальний статус з емодзі (наприклад, "🟢 RESOLVED") у чистий текстовий код ("RESOLVED"). Це запобігає появі нечитабельних символів у SQL-запитах та забезпечує сумісність з іншими аналітичними модулями системи.</p>
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
