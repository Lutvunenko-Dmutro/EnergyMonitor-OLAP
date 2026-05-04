# Технічна специфікація: Система Відмовостійкості ATLAS (ERROR RESILIENCE GIGA-PASSPORT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">FAULT TOLERANCE & RESILIENCE | ERROR HANDLING SYSTEM</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛡️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Система Відмовостійкості</h1>
            <p class="mega-subtitle">Бронежилет програмного коду: багаторівнева обробка винятків (Robust Handlers), стратегія Graceful Degradation, захист інтерфейсу від каскадних збоїв та інтелектуальна діагностика стану</p>
            <div class="status-tags"><span class="tag tag-online">RESILIENCE ACTIVE</span><span class="tag tag-version">v1.5.0</span><span class="tag tag-role">STABILITY ENGINEER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🧱</div><div class="metric-info"><span class="metric-label">Strategy</span><span class="metric-value">Graceful Degradation</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📉</div><div class="metric-info"><span class="metric-label">Fallback</span><span class="metric-value">ML-Safe Defaults</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📢</div><div class="metric-info"><span class="metric-label">Reporting</span><span class="metric-value">Quiet Fail Mode</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⛓️</div><div class="metric-info"><span class="metric-label">Protection</span><span class="metric-value">Anti-cascade Logic</span></div></div>
</div>

<!-- SECTION 01: ERROR RESILIENCE PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Відмовостійкості</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>error_handlers.py</code> є "Системою Життєзабезпечення" проекту ATLAS. В складних аналітичних системах, де працюють нейронні мережі та зовнішні бази даних, помилки неминучі. Наша філософія базується на принципі <b>"Стійкості до відмов"</b>: замість того, щоб зупиняти весь додаток при збої одного ШІ-прогнозу, система локалізує проблему, логує її та надає користувачеві безпечне значення (Fallback), зберігаючи працездатність HUD-інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 02: RESILIENCE HIERARCHY & FLOW -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Ієрархія та потік відмовостійкості</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    EXEC("Function Execution") --> HANDLER{"Robust Handler?"}
    HANDLER -- "Normal" --> RESULT("Return Result")
    HANDLER -- "Error Detected" --> CATCH("Catch & Localize")
    CATCH --> LOG("Audit Logging & Sentry (Simulated)")
    LOG --> STRATEGY{"Recovery Strategy"}
    STRATEGY -- "Retry" --> EXEC
    STRATEGY -- "Fallback" --> DEFAULTS("Return Safe Defaults (Zeros/Mean)")
    DEFAULTS --> NOTIFY("Quiet UI Notification")
    NOTIFY --> RESULT
    </div></div>
</div>

<!-- SECTION 03: ML-SPECIFIC ROBUST HANDLERS (🧠) -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Спеціалізовані ML-обробники (Robust Handlers)</h2></div>
    <div class="glass-card flow-step">
        <p>Для ШІ-блоку реалізовано посилений захист через декоратор <code>@robust_ml_handler</code>:</p>
        <ul>
            <li><b>Input Sanitization:</b> Перевірка розмірності тензорів та типів даних перед передачею в ONNX-сесію.</li>
            <li><b>Resource Integrity:</b> Якщо файл моделі пошкоджено або не знайдено, обробник запобігає падінню системи, повертаючи об'єкт <code>NullModel</code>.</li>
            <li><b>Numerical Stability:</b> Автоматична заміна <code>NaN</code> та <code>Inf</code> значень на статистичні середні для запобігання "вибуху" градієнтів та некоректних графіків.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: GRACEFUL DEGRADATION LEVELS -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Рівні Graceful Degradation (Поступова деградація)</h2></div>
    <div class="glass-card flow-step">
        <p>Система ATLAS вміє працювати в умовах обмежених ресурсів:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Статус збою</th>
                    <th>Дія системи</th>
                    <th>Ефект для користувача</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>БД Недоступна</td><td>Перехід на локальний CSV-кеш</td><td>Дані застарілі, але інтерфейс активний</td></tr>
                <tr><td>ML Модель V3 Failure</td><td>Авто-перемикання на Baseline V1</td><td>Зниження точності без зупинки моніторингу</td></tr>
                <tr><td>RAM Overload</td><td>Очищення кешу та вимкнення анімацій</td><td>Стабілізація споживання ресурсів</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: QUIET FAIL MODE & UI FEEDBACK -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Режим "Quiet Fail" та зворотний зв'язок UI</h2></div>
    <div class="glass-card flow-step">
        <p>Ми уникаємо лякаючих системних помилок (Tracebacks). Замість них використовується <b>Quiet Fail</b>: помилка фіксується в логах, а в UI відображається делікатний статус-індикатор або плейсхолдер. Це критично для систем оперативного управління, де паніка оператора через незрозумілий текст помилки може призвести до хибних дій у реальній мережі.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (RESILIENCE CORE) -->
<div class="section-container">
    <div class="section-number">06</span><h2 class="section-title">Псевдокод ядра системи відмовостійкості</h2></div>
    <div class="glass-card flow-step">
        <pre><code>DECORATOR robust_ml_handler(func):
    FUNCTION wrapper(*args, **kwargs):
        TRY:
            VALIDATE_INPUTS(args)
            RETURN func(*args, **kwargs)
        EXCEPT FileNotFoundError:
            LOG_CRITICAL("AI Model File Missing!")
            RETURN Fallback_Model()
        EXCEPT NumericalError as e:
            LOG_WARNING(f"Math Instability: {e}")
            RETURN Sanitize_Outputs(Zero_Vector)
        EXCEPT Exception as e:
            REPORT_SENTRY(e)
            RETURN DEFAULT_SAFE_VALUE
    END FUNCTION
END DECORATOR</code></pre>
    </div>
</div>

<!-- SECTION 07: ANTI-CASCADE PROTECTION LOGIC -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Логіка анти-каскадного захисту</h2></div>
    <div class="glass-card flow-step">
        <p>Система ATLAS реалізує принцип <b>"Bulkhead Pattern"</b> (Відсіки корабля). Кожен великий компонент (ML, DB, UI) ізольований. Помилка в модулі розрахунку фінансових ризиків не може заблокувати потік даних у модулі моніторингу телеметрії. Це досягається за рахунок незалежних обробників у кожній аналітичній гілці конвеєра.</p>
    </div>
</div>

<!-- SECTION 08: INTELLIGENT RETRY STRATEGIES -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Інтелектуальні стратегії повторів (Retries)</h2></div>
    <div class="glass-card flow-step">
        <p>Для мережевих операцій застосовується <b>Exponential Backoff</b>. Якщо запит до PostgreSQL завершився таймаутом, система не "бомбардує" базу новими запитами, а робить повтори з інтервалами, що прогресивно збільшуються (1с, 2с, 4с). Це дає серверу час на відновлення та запобігає ефекту "громовиці" (Thundering Herd).</p>
    </div>
</div>

<!-- SECTION 09: SYSTEM HEALTH DIAGNOSTICS (🩸) -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Діагностика здоров'я системи</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль відстежує частоту виникнення помилок. Якщо кількість збоїв у певному вузлі перевищує критичний поріг (Error Threshold), система автоматично переходить у <b>Safe Mode</b>, відключаючи найбільш енергоємні та нестабільні функції до моменту втручання адміністратора або стабілізації параметрів мережі.</p>
    </div>
</div>

<!-- SECTION 10: AUDIT LOGGING & TRACEABILITY -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Аудит-логування та простежуваність</h2></div>
    <div class="glass-card flow-step">
        <p>Кожна перехоплена помилка супроводжується повним контекстом: <code>Substation_ID</code>, <code>Model_Version</code>, <code>Input_Params_Hash</code>. Це дозволяє розробникам відтворити умови збою в лабораторних умовах, що робить процес налагодження (Debugging) максимально швидким та прозорим.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Main Orchestrator</h4>
                <p>Використовує хандлери для глобального захисту життєвого циклу додатка.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🧠</div>
            <div class="role-content">
                <h4>ML Predictors</h4>
                <p>Основні споживачі "бронежилета" для захисту обчислень нейромереж.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Logging System</h4>
                <p>Приймає структуровані звіти про помилки для подальшого аналізу.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (AUTO-HEALING & AI-DEBUG) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v2.0 (Auto-Healing & AI-Debug)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується впровадження <b>Авто-відновлення (Auto-Healing)</b> — автоматичного рестарту окремих сервісів при збої, інтеграція з <b>LLM-діагностом</b> (який пояснює оператору причину помилки зрозумілою мовою) та підтримка <b>Circuit Breaker</b> на рівні окремих підстанцій.</p>
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
