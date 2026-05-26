# Технічний Паспорт Компонента: tests/test_ml_model.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🧠 INTELLIGENT FORECAST & TENSOR SENTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🤖</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">test_ml_model.py</h1>
            <p class="mega-subtitle">Система верифікації LSTM нейромереж, топології тензорів та аналітичних метрик похибки</p>
            <div class="status-tags">
                <span class="tag tag-online">NEURAL AUDITOR</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">QUALITY GATE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">LSTM Input Shape</span>
            <span class="metric-value">(batch, 24, 9)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-info">
            <span class="metric-label">Output Horizon</span>
            <span class="metric-value">24 Hours (1 feat)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Quality Metrics</span>
            <span class="metric-value">RMSE, MAE, MAPE</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔄</div>
        <div class="metric-info">
            <span class="metric-label">Time Encoding</span>
            <span class="metric-value">Sin / Cos Cyclical</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль та ШШ-аудит</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>tests/test_ml_model.py</code> виконує роль головного валідатора для всіх когнітивних та предиктивних ШІ-компонентів платформи <b>Energy Monitor Ultimate</b>. Він фокусується на тестуванні математичної коректності глибокої нейронної мережі LSTM, методів обробки даних (feature engineering) та математичних функцій розрахунку точності прогнозів.
        </p>
        <p style="margin-top: 10px;">
            Ключові сфери верифікації:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Топологія тензорів Keras (Tensor Dimension Consistency):</strong> Перевірка того, що вхідні дані кодуються у правильні тривимірні об'єкти, придатні для шарів рекурентної мережі (LSTM Layers).</li>
            <li><strong>Математика похибок (Error Metrics Precision):</strong> Тестування формул розрахунку якості прогнозів, які визначають успішність бектестів та автоматичне перенавчання моделей.</li>
            <li><strong>Циклічний енкодінг часу (Temporal Geometry):</strong> Перевірка тригонометричного перетворення часових міток для кращого сприйняття нейромережею добової сезонності.</li>
            <li><strong>Препроцесинг даних (Normalization Shield):</strong> Валідація масштабування ознак у герметичному діапазоні $[0, 1]$ за допомогою алгоритму MinMaxScaler.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: NEURAL PIPELINE FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Життєвий цикл нейронного прогнозування (ML Inference Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема відображає послідовність етапів обробки даних, які верифікує цей тестовий модуль:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                RAW_DATA("Raw Time-Series Data (1D)") --> SLIDING_WINDOW("1. Sliding Window (window_size=24)")
                SLIDING_WINDOW --> NORMALIZATION("2. Normalization (MinMaxScaler -> [0, 1])")
                NORMALIZATION --> CYCLICAL_ENC("3. Cyclical Encoding (Hour -> Sin/Cos)")
                
                CYCLICAL_ENC --> BATCH_REPLACE("4. Reshape to (Batch_size, 24, 9)")
                BATCH_REPLACE --> INFERENCE("5. LSTM Neural Inference")
                INFERENCE --> OUTPUT_SHAPE{"6. Output Shape Validation?"}
                
                OUTPUT_SHAPE -- "Correct (Batch, 24, 1)" --> CHECK_RANGE("7. Range check (no NaN/Inf, >-500, <1000)")
                OUTPUT_SHAPE -- "Incorrect" --> FAIL_TEST("AssertionError: Shape Mismatch")
                
                CHECK_RANGE -- "Valid Values" --> METRICS("8. Calculate Accuracy Metrics: RMSE, MAE, MAPE")
                METRICS --> PASS("ML Component: VERIFIED")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: MATHEMATICAL SPECIFICATIONS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичний апарат аналізу та метрик</h2>
    </div>
    <div class="glass-card">
        <p style="margin-bottom: 15px;">
            Тестовий модуль перевіряє три класичні математичні функції оцінки похибки моделей машинного навчання:
        </p>
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Середньоквадратична помилка (RMSE - Root Mean Squared Error)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Вимірює стандартне відхилення залишків прогнозування. Штрафує великі похибки сильніше через піднесення до квадрата:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2} $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Середня абсолютна помилка (MAE - Mean Absolute Error)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Характеризує середній модуль розбіжності між фактичним значенням споживання та ШІ-прогнозом:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i| $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Середня абсолютна відсоткова помилка (MAPE - Mean Absolute Percentage Error)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Показує відносну відсоткову похибку моделі, що є зручним для презентації бізнес-користувачам:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{MAPE} = \frac{100\%}{n} \sum_{i=1}^n \left| \frac{y_i - \hat{y}_i}{y_i} \right| $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">4. Циклічне кодування міток часу (Sin/Cos Time Encoding)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Щоб уникнути штучного розриву між 23:59 та 00:00 годинами, значення кодуються на колі радіусом 1:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ X_{sin} = \sin\left(\frac{2\pi \cdot t}{24}\right), &nbsp;&nbsp;&nbsp; X_{cos} = \cos\left(\frac{2\pi \cdot t}{24}\right) $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Це створює безперервну топологічну репрезентацію часу для рекурентних шарів.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE / DATA PROCESSING -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму розрахунку циклічного часу</h2>
    </div>
    <div class="glass-card">
        <p>
            Для розуміння алгоритму кодування часу, який перевіряється в <code>test_cyclical_encoding</code>, наведено псевдокод:
        </p>
        <pre><code class="language-python">
# Псевдокод тригонометричного відображення часу
def encode_hour_cyclical(hour_value):
    import math
    # Період для добового циклу дорівнює 24 годинам
    period = 24.0
    
    # Розрахунок координат на одиничному колі
    sin_component = math.sin(2 * math.pi * hour_value / period)
    cos_component = math.cos(2 * math.pi * hour_value / period)
    
    return sin_component, cos_component
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ & ADVANCED TUNING -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Часті питання (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому для LSTM вхідна форма тензора має бути 3D-об'єктом?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Шари LSTM фреймворку Keras/TensorFlow очікують тривимірний вхід виду <code>(Batch Size, Time Steps, Features)</code>. Тест <code>test_forecast_output_shape</code> спеціально перевіряє, що наш конвеєр даних правильно виконує операцію <code>reshape(1, 24, 9)</code> перед передачею в нейромережу.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому тести пропускаються (skip) у випадку відсутності Keras?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Це стандартна практика написання стійких тестів (Resilient Testing). Якщо на сервері інтеграції (CI/CD) відсутня важка бібліотека штучного інтелекту, тести не мають падати з критичним помилками імпорту. Замість цього вони граційно переходять у статус <code>Skipped</code>, дозволяючи решті тестів успішно виконатися.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Які значення похибки вважаються нормальними для енергомережі?</h4>
        <p style="color: var(--text-dim);">
            A: Для MAPE хорошим результатом вважається похибка < 5% (перевіряється в <code>test_mape_calculation</code>), для складніших об'єктів — до 10%. Будь-який прогноз із MAPE > 20% вказує на критичний збій моделі або появу аномальних даних у мережі.
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
