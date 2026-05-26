# Технічна специфікація: Візуалізатор Оперативного Моніторингу та KPI (SITUATIONAL AWARENESS VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">OPERATIONAL MONITORING | DIGITAL TWIN KPI</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Оперативний Моніторинг</h1>
            <p class="mega-subtitle">Високотехнологічний центр контролю ключових показників ефективності (KPI) в реальному часі: оперативна оцінка цілісності мережі, стабільності частоти та предиктивна діагностика підстанцій</p>
            <div class="status-tags"><span class="tag tag-online">KPI ENGINE ACTIVE</span><span class="tag tag-version">v2.6.0</span><span class="tag tag-role">SYSTEM OPERATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🏥</div><div class="metric-info"><span class="metric-label">Health</span><span class="metric-value">Network Integrity %</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💓</div><div class="metric-info"><span class="metric-label">Stability</span><span class="metric-value">Frequency (Hz) Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Load</span><span class="metric-value">Total Power (MW)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛠️</div><div class="metric-info"><span class="metric-label">Method</span><span class="metric-value">Digital Twin Feed</span></div></div>
</div>

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Оперативного Моніторингу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>kpi.py</code> є "Пульсом" проєкту ATLAS. В енергетиці ситуаційна обізнаність (Situational Awareness) є критичною: оператор повинен за лічені секунди зрозуміти, чи знаходиться система в безпечному режимі. Наша філософія базується на <b>Когнітивній Швидкості</b>: ми використовуємо великі метрики (Big Numbers), колірну індикацію (Зелений/Жовтий/Червоний) та інтерактивні кругові спідометри (Gauges) для миттєвої передачі стану системи, мінімізуючи час на інтерпретацію цифр.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL FORMULAS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичні розрахунки оперативних метрик</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення ситуаційної обізнаності модуль в реальному часі виконує наступні математичні розрахунки:</p>
        
        <h4>1. Середньозважений індекс здоров'я мережі ($\overline{\text{Health}}$)</h4>
        <p>Комплексний показник працездатності розраховується як середнє арифметичне поточних AI-індексів здоров'я всіх активних підстанцій:</p>
        $$\overline{\text{Health}} = \frac{1}{M} \sum_{i=1}^{M} \text{Health}_{i}$$
        <p>де $\text{Health}_{i}$ — індекс здоров'я $i$-ї підстанції (%), розрахований на основі концентрації газів H2, температури масла та перевантажень.</p>

        <h4>2. Дельта відхилення частоти системи ($\Delta f$)</h4>
        <p>Стабільність частоти змінного струму є головним маркером балансу генерації та споживання. Відхилення розраховується відносно номінальних 50.00 Гц:</p>
        $$\Delta f = f_{\text{system}} - 50.00 \text{ Гц}$$
        <p>При $\Delta f > +0.2$ Гц система реєструє профіцит генерації, при $\Delta f < -0.2$ Гц — дефіцит потужності, що вимагає негайного автоматичного або ручного розвантаження мережі.</p>
    </div>
</div>

<!-- SECTION 03: KPI PROCESSING PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Конвеєр Обробки Метрик (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Input Latest DataFrame (df_latest)") --> IS_EMPTY{"Is Empty?"}
    IS_EMPTY -- "Yes" --> RENDER_WAIT("Display Ingestion Spinner")
    IS_EMPTY -- "No" --> CHECK_KAG{"Is Kaggle mode?"}
    
    CHECK_KAG -- "Yes (Missing health_score)" --> RENDER_SIMPLE("Display Simple Absolute MW metric")
    CHECK_KAG -- "No (Digital Twin mode)" --> CLEAN("pd.to_numeric with errors='coerce'")
    
    CLEAN --> AGGR("Calculate mean health, frequency_hz, sum load_mw")
    
    AGGR --> KPI_ROW("Render top columns: Health, Freq, Total Load")
    AGGR --> GAUGE("Render interactive Gauge relative to 40 GW capacity")
    
    CLEAN --> FILTER("Filter out AEP Region nodes")
    FILTER --> HEALTH_BARS("Apply make_health_bar to health_score")
    
    HEALTH_BARS --> DATAFRAME("st.dataframe (Custom format: MВт, кВ, °С, ppm)")
    </div></div>
</div>

<!-- SECTION 04: CORE METRICS DEFINITION MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця визначення ключових метрик</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Метрика</th>
                    <th>Метод розрахунку / Джерело</th>
                    <th>Норма</th>
                    <th>Діагностичне значення критичних меж</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>🏥 <b>Network Health</b></td><td>Агрегація AI-індексів здоров'я підстанцій</td><td>90 - 100%</td><td>&lt; 85% — прискорене старіння трансформаторів</td></tr>
                <tr><td>💓 <b>Frequency</b></td><td>Дані з віртуального осцилятора системи</td><td>50.00 Гц</td><td>&plusmn;0.2 Гц — запуск аварійної частотної розвантажувальної автоматики (АЧР)</td></tr>
                <tr><td>⚡ <b>Total Power</b></td><td>Сумація навантаження всіх активних споживачів</td><td>Залежно від піків</td><td>&gt; 95% від ліміту 40 ГВт — дефіцит резервів потужності</td></tr>
                <tr><td>🌡️ <b>Oil Temp</b></td><td>Датчики верхніх шарів трансформаторного масла</td><td>40 - 75°C</td><td>&gt; 85°C — критичний нагрів обмоток, ризик виникнення пожежі</td></tr>
                <tr><td>🛡️ <b>H2 Concentration</b></td><td>Хімічний хроматограф (DGA розчинених газів)</td><td>&lt; 50 ppm</td><td>&gt; 100 ppm — внутрішній тліючий розряд (дуга), деградація паперу</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: ADAPTIVE INTERFACE MODES (LIVE vs KAGGLE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Адаптивні режими інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль реалізує <b>Адаптивний Рендеринг</b>. При роботі з історичними файлами (Kaggle), де відсутні параметри здоров'я обладнання та концентрації газів, інтерфейс автоматично перемикається у спрощений режим. Замість "порожніх" віджетів з помилками, система виводить інформативне повідомлення про те, які метрики доступні тільки в режимі Digital Twin, зберігаючи фокус на фактичному навантаженні регіону.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Моніторингу (KPI Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_situational_awareness(df_latest, region_filter):
    1. // [CHECK VACANT DATA]
       IF df_latest is Empty:
           show_waiting_ingestion_message()
           RETURN
           
    2. // [ADAPT MODE DETECTION]
       IF "health_score" NOT IN df_latest.columns:
           show_kaggle_mode_info()
           total_load = df_latest["actual_load_mw"].sum()
           st.metric("⚡ Поточне навантаження регіону", format_mw(total_load))
           RETURN
           
    3. // [FAIL-SAFE DATATYPE COERCION]
       df_clean = df_latest.copy()
       numeric_cols = ["health_score", "frequency_hz", "actual_load_mw", "voltage_kv", "temperature_c", "h2_ppm"]
       FOR col IN numeric_cols:
           df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce").fillna(0.0)
           
    4. // [AGGR CALCULATIONS]
       avg_health = df_clean["health_score"].mean()
       system_freq = df_clean["frequency_hz"].iloc[0] IF df_clean["frequency_hz"].iloc[0] > 0 ELSE 50.0
       total_load = df_clean["actual_load_mw"].sum()
       
    5. // [KPI COLUMNS RENDER]
       m1, m2, m3, m4 = st.columns(4)
       m1.metric("🏥 Здоров'я мережі", f"{avg_health:.1f}%", color_by(avg_health > 85))
       m2.metric("💓 Частота", f"{system_freq:.2f} Гц", delta=(system_freq - 50.0))
       m3.metric("⚡ Повна потужність", format_mw(total_load))
       with m4:
           avg_load_pct = clip_value((total_load / 40000.0 * 100), 0, 100)
           render_gauge(avg_load_pct)
           
    6. // [DIGITAL TWINS DETAILED GRAPHICS TABLE]
       df_cards = df_clean.copy()
       IF "substation_name" IN df_cards.columns:
           df_cards = df_cards[df_cards.substation_name != "AEP Region"]
       IF region_filter IS VALID:
           df_cards = df_cards[df_cards.region_name == region_filter]
           
       df_table = df_cards[["substation_name", "actual_load_mw", "voltage_kv", "temperature_c", "h2_ppm", "health_score"]].copy()
       df_table["Стан (Здоров'я)"] = df_table["health_score"].apply(cards.make_health_bar)
       
       st.dataframe(df_table, column_config={
           "actual_load_mw": NumberColumn("Навантаження", format="%.1f МВт"),
           "voltage_kv": NumberColumn("Напруга", format="%.1f кВ"),
           "temperature_c": NumberColumn("Темп. Масла", format="%.1f °C"),
           "h2_ppm": NumberColumn("H2", format="%.1f ppm")
       }, hide_index=True)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: DIGITAL TWIN SUBSTATION TABLE (AI-INDEX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Таблиця підстанцій з AI-індексом</h2></div>
    <div class="glass-card flow-step">
        <p>Центральним елементом аналізу підстанцій є сучасна інтерактивна таблиця <code>st.dataframe</code>. Вона використовує спеціалізований прогрес-бар <code>make_health_bar</code> для відображення рівня працездатності: вузли в нормі отримують зелений індикатор, а підстанції з високою аварійністю або деградацією масла — червоний з текстовим маркером небезпеки. Це дозволяє оператору миттєво локалізувати найслабшу ланку системи.</p>
    </div>
</div>

<!-- SECTION 08: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4><a href="ui_cards_library.md">cards.py</a></h4>
                <p>Експортер графічних віджетів: функції рендерингу кругового спідометра <code>render_gauge</code> та генерації статус-барів <code>make_health_bar</code>.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4><a href="data_services_hub.md">aggregator.py</a></h4>
                <p>Аналітичний сервіс, що постачає останні актуальні зрізи станів датчиків підстанцій.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">⚙️</div>
            <div class="role-content">
                <h4>Pandas Core</h4>
                <p>Ядро для швидкої типізації, конвертації та обчислення середньозважених показників підстанцій.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 09: ROADMAP TO v3.0 (PREDICTIVE KPI & SOUND WARNINGS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Дорожня карта v3.0 (Predictive KPI & Sound Alerts)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступних версіях заплановано:</p>
        <ul>
            <li><b>AI Predictive Metrics:</b> Відображення прогнозованих ШІ-моделлю значень навантаження та температури на наступні 60 хвилин безпосередньо у вигляді тіньових маркерів на віджетах.</li>
            <li><b>Sound Warnings:</b> Голосова озвучка критичних зсувів частоти за межі номіналу (&Delta;f &gt; &plusmn;0.25 Гц) за допомогою Speech Synthesis API.</li>
            <li><b>Automated Load Shedding:</b> Кнопка екстреного відключення найменш критичних ліній споживання (Load Shedding) у разі перевантаження системи.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">FAQ: Технічні відповіді</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Чому показник здоров'я мережі показує "N/A" або 0.0%?</b><br>
        A: Це свідчить про те, що система підключена до Kaggle-датасету, який не містить AI-індексів здоров'я підстанцій, або симулятор датчиків ще не запустився. Перемкніть джерело даних на "Симулятор" у боковій панелі.</p>
        <p><b>Q: Як розраховується відсоток для кругового спідометра (Gauge)?</b><br>
        A: Ми порівнюємо поточне сумарне споживання системи (у МВт) з базовою системною константою пропускної спроможності мережі — 40 000 МВт (40 ГВт). Результат обрізається функцією <code>clip(0, 100)</code> для виключення виходу за межі шкали.</p>
        <p><b>Q: Як працює захист від TypeError при роботі з датчиками?</b><br>
        A: Оскільки симуляційні датчики передають дані асинхронно через SQLite, іноді при першому читанні можуть з'явитися текстові помилки або пропуски (None). Функція <code>pd.to_numeric(errors="coerce").fillna(0.0)</code> примусово переводить всі значення в дійсні числа, замінюючи помилки на нулі, що гарантує 100% захист від "падіння" рендерингу Streamlit.</p>
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
