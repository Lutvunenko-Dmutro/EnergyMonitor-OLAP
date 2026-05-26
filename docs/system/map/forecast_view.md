# ⚡ Технічна специфікація: Центр Прогнозування та Аудиту ШІ (AI FORECAST & AUDIT VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">STREAMLIT PLATFORM | AI FORECASTING CONTROL PANEL</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚡</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Панель Управління ШІ</h1>
            <p class="mega-subtitle">Головний вебаналітичний інтерфейс ATLAS: реактивна генерація прогнозів навантаження, покроковий ретроспективний аудит та порівняльний аналіз нейромережевих архітектур</p>
            <div class="status-tags"><span class="tag tag-online">FORECASTER ACTIVE</span><span class="tag tag-version">v2.8.0</span><span class="tag tag-role">CHIEF DISPATCHER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">UI Engine</span><span class="metric-value">Streamlit Responsive</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Charts</span><span class="metric-value">Plotly JSON Interactive</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Threading</span><span class="metric-value">Interrupt Safe</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Validation</span><span class="metric-value">Comparative Backtest</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальна Роль та Філософія</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>forecast.py</code> є головним інтерфейсним «містком» оператора в системі <b>ATLAS</b>. Він об'єднує складні математичні розрахунки, ML-інференс та базу даних в один інтуїтивно зрозумілий реактивний HUD (Heads-Up Display). Головна філософія цього екрану — **«Довіра через прозорість»**: оператор бачить не просто одну лінію прогнозу, а отримує повний інструментарій для порівняння різних ШІ-моделей (LSTM V1, V2, V3) на одному графіку, симуляції погодних аномалій («What-if» сценарії) та миттєвого прорахунку похибок точності MAE/RMSE.</p>
    </div>
</div>

<!-- SECTION 02: ADVANCED INTERFACE MECHANISMS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Інженерні Особливості Веб-Інтерфейсу</h2></div>
    <div class="glass-card flow-step">
        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-bottom: 10px;">1. Захист від зависання сервера (Interruption Monitor)</h3>
        <p>У Streamlit швидка зміна налаштувань користувачем може призвести до паралельного запуску кількох важких потоків нейромережевого прогнозування, що викликає <b>CPU Thrashing</b> (перевантаження процесора). Для усунення цього ефекту реалізовано монітор стану сесії:</p>
        <ul>
            <li>Перед запуском розрахунку у <code>st.session_state</code> реєструється токен поточної операції.</li>
            <li>Якщо користувач робить новий клік до завершення старого, система виявляє невідповідність токенів, примусово зупиняє попередні обчислення та виконує швидкий скид пам'яті.</li>
            <li>Користувач отримує миттєвий відгук у вигляді спливаючого повідомлення (Toast), без зависання інтерфейсу додатка.</li>
        </ul>

        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-top: 20px; margin-bottom: 10px;">2. Графічна оптимізація Plotly (Cyber HUD Theme)</h3>
        <p>Візуалізація часових рядів здійснюється через динамічний рендеринг об'єктів Plotly. Ми повністю прибрали стандартні стилі та інтегрували індивідуальні налаштування сітки:</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--text-dim); border: 1px solid var(--border);">
            fig.update_layout(<br>
            &nbsp;&nbsp;&nbsp;&nbsp;plot_bgcolor="rgba(15, 23, 42, 0.4)",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;paper_bgcolor="rgba(0,0,0,0)",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;font=dict(color="#94a3b8", family="JetBrains Mono"),<br>
            &nbsp;&nbsp;&nbsp;&nbsp;xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),<br>
            &nbsp;&nbsp;&nbsp;&nbsp;yaxis=dict(gridcolor="rgba(255,255,255,0.05)")<br>
            )
        </div>
    </div>
</div>

<!-- SECTION 03: FORECAST VIEW WORKFLOW -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Робочий процес взаємодії (Workflow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    USER("Клік користувача (Прогноз / Бектест)") --> STATE_INIT("Ініціалізація токена сесії")
    STATE_INIT --> CHECK_INTERRUPT{"Виявлено переривання?"}
    
    CHECK_INTERRUPT -- Так --> STOP_PREV("Примусова зупинка потоку ШІ")
    STOP_PREV --> RUN_NEW("Запуск нового обчислення")
    
    CHECK_INTERRUPT -- Ні --> RUN_NEW
    
    RUN_NEW --> DISPATCH{"Вибір режиму роботи"}
    
    DISPATCH -- "⚡ AI Forecast" --> FORECAST_CONTROLLER("Запуск Forecast Controller")
    DISPATCH -- "📊 Backtest" --> BACKTEST_ENGINE("Запуск Backtest Engine (Аудит)")
    
    FORECAST_CONTROLLER --> PLOTLY("Рендеринг Plotly HUD")
    BACKTEST_ENGINE --> COMP_TABLE("Таблиця метрик точності (R2, RMSE)")
    
    PLOTLY --> DISPLAY("Відображення на екрані")
    COMP_TABLE --> DISPLAY
    </div></div>
</div>

<!-- SECTION 04: CORE VIEW LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Псевдокод Головного Рендерера Екрану</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_forecast_view(substation_id, db_source):
    1. READ user_inputs (substation, horizon, model_version)
    2. RENDER_HEADER with simulation parameters (Temperature shift, equipment health)
    3. IF btn_generate_forecast:
        st.session_state.forecast_token = generate_unique_token()
        RESULTS = execute_forecast(substation_id, horizon, model_version)
        IF forecast_token_changed:
            ABORT()
        RENDER_DYNAMIC_PLOTLY(RESULTS)
        RENDER_METRIC_CARDS(RESULTS)
    4. IF btn_run_backtest:
        RUN_COMPARATIVE_AUDIT(substation_id)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 05: ACADEMIC ACCURACY & AUDITING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Стенд Академічної Звітності Метрик</h2></div>
    <div class="glass-card flow-step">
        <p>У режимі порівняльного бектестування (Backtesting Mode) інтерфейс автоматично перетворюється на академічний аналітичний звіт. Система виконує ретроспективне тестування моделей на історичному вікні та будує порівняльну таблицю з розрахунком стандартних наукових коефіцієнтів:</p>
        <ul>
            <li><b>R² (Коефіцієнт детермінації):</b> показує відсоток відповідності моделі реальному тренду (ціль: >0.90).</li>
            <li><b>RMSE (Середньоквадратична помилка):</b> демонструє величину стандартного відхилення прогнозу від факту в МВт.</li>
            <li><b>MAE (Середня абсолютна помилка):</b> показує реальне середнє відхилення прогнозу в абсолютних одиницях.</li>
        </ul>
        <p>Ці дані готові до миттєвого експорту та впровадження у графічну частину дипломної роботи.</p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../system/atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
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
