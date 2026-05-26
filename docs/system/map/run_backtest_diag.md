# Технічний Паспорт Компонента: scripts/ml/run_backtest_diag.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">📊 BACKTEST QUICK DIAGNOSTIC SENTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🩺</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">run_backtest_diag.py</h1>
            <p class="mega-subtitle">Утиліта експрес-діагностики бектестів, версійного порівняння точності MAPE та логування збоїв обчислень</p>
            <div class="status-tags">
                <span class="tag tag-online">DIAGNOSTIC RUNNER</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">RAPID AUDITOR</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🔍</div>
        <div class="metric-info">
            <span class="metric-label">Target Substation</span>
            <span class="metric-value">ПС Бровари</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔄</div>
        <div class="metric-info">
            <span class="metric-label">Model Versions</span>
            <span class="metric-value">V1, V2, V3</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">Key Metric</span>
            <span class="metric-value">MAPE (%)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Logger System</span>
            <span class="metric-value">setup_logger</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль експрес-діагностики</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/ml/run_backtest_diag.py</code> є швидким **верифікаційним сенсором** (Backtest Quick Diagnostic) в архітектурі машинного навчання платформи <b>Energy Monitor Ultimate</b>. Він надає розробникам та операторам інструмент миттєвого аудиту працездатності ШІ-моделей для конкретного об'єкта енергомережі без необхідності запускати повний аналітичний інтерфейс користувача.
        </p>
        <p style="margin-top: 10px;">
            Основні діагностичні цілі утиліти:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Версійний бенчмаркінг (Version Benchmarking):</strong> Послідовний розрахунок точності за метрикою MAPE для всього еволюційного стеку моделей (V1 - legacy, V2 - multi-features, V3 - deep multi-step).</li>
            <li><strong>Аудит конкретної підстанції (Target Node Validation):</strong> Фокусована перевірка точності на прикладі реального регіонального вузла <i>"ПС Бровари"</i>.</li>
            <li><strong>Детектор збоїв конвеєра (Pipeline Fault Detection):</strong> Перехоплення та безпечне логування помилок (наприклад, відсутність ваг моделей, проблеми підключення до БД чи невідповідність форм ознак) без аварійного завершення процесу.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: PROCESS SEQUENCE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр швидкої перевірки моделей (Express Diagnostic Workflow)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема відображає послідовність кроків обчислення похибок бектестів:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            sequenceDiagram
                autonumber
                participant Sentry as run_backtest_diag.py
                participant Engine as src.ml.backtest
                participant Loader as DB Loader
                participant Model as LSTM Model H5
                
                Sentry->>Sentry: Ініціалізація логера та завдання substation = "ПС Бровари"
                Note over Sentry: Початок циклу за версіями: v1, v2, v3
                Sentry->>Engine: get_backtest_metrics(version, substation_name)
                Engine->>Loader: Зчитування історичного вікна телеметрії
                Loader->>Engine: Повернення матриць ознак
                Engine->>Model: Завантаження ваг та запуск інференсу
                Model->>Engine: Розрахунок прогнозу навантаження
                Engine->>Engine: Розрахунок похибки MAPE (%)
                Engine->>Sentry: Повернення кортежу (mape, error)
                
                alt Помилка (error is not None)
                    Sentry->>Sentry: Вивід у консоль: "Error {v}: {err}"
                else Успішно (error is None)
                    Sentry->>Sentry: Вивід у консоль: "mape: {mape}%"
                end
                Note over Sentry: Перехід до наступної версії моделі
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Метрика MAPE та діагностичне логування</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Середня абсолютна відсоткова похибка (MAPE - Mean Absolute Percentage Error)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Метрика MAPE є головним індикатором якості в експрес-діагностиці, оскільки вона виражає помилку у відсотках відносно реального навантаження, що дозволяє порівнювати точність на підстанціях різної потужності:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{MAPE} = \frac{100\%}{n} \sum_{i=1}^n \left| \frac{y_i - \hat{y}_i}{y_i} \right| $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Система централізованого логування (setup_logger)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Утиліта використовує внутрішній системний логер <code>setup_logger(__name__)</code>. Це гарантує, що всі проміжні попередження від TensorFlow або SQLAlchemy записуються в загальний обертовий лог-файл проєкту для подальшого аналізу адміністраторами.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод циклу діагностики бектестів</h2>
    </div>
    <div class="glass-card">
        <p>
            Спрощений псевдокод внутрішньої логіки швидкого тестування моделей:
        </p>
        <pre><code class="language-python">
# Псевдокод швидкого аудиту моделей
def execute_rapid_backtest_diagnostics(target_substation="ПС Бровари"):
    model_versions = ["v1", "v2", "v3"]
    logger.info(f"Запуск діагностики бектестів для {target_substation}...")
    
    for version in model_versions:
        # Безпечний виклик ядра розрахунку бектесту
        mape_score, error_msg = backtest.calculate_metrics(
            model_version=version, 
            substation_name=target_substation
        )
        
        if error_msg is not None:
            logger.error(f"Помилка розрахунку версії {version}: {error_msg}")
        else:
            print(f"Версія: {version.upper()} | MAPE: {mape_score:.2f}% | Стан: OK")
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Часті питання (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому для діагностики за замовчуванням обрано підстанцію "ПС Бровари"?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: ПС Бровари є типовим представником регіональних підстанцій з комерційним типом профілю навантаження. Проведення діагностики саме на цьому об'єкті дозволяє перевірити стійкість моделей до динамічних коливань споживання промислової зони передмістя.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Які помилки (errors) найчастіше перехоплює цей скрипт?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Найчастіше скрипт виявляє відсутність скомпілованого H5-файлу моделі для конкретної версії у папці <code>models/</code>, або недостатню кількість накопичених телеметричних рядів у таблиці <code>LoadMeasurements</code> бази даних для цієї підстанції.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як запустити цей скрипт вручну?</h4>
        <p style="color: var(--text-dim);">
            A: Виконайте у терміналі наступну команду: <code>python scripts/ml/run_backtest_diag.py</code>
        </p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn">
        <span class="btn-icon">🔙</span>
        <span class="btn-text">Повернутися до Атласу</span>
    </a>
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
