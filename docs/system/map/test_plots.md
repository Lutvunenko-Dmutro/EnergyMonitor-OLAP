# Технічний Паспорт Компонента: scripts/ml/test_plots.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🖼️ VISUAL ANALYTICS & RENDERING VALIDATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">test_plots.py</h1>
            <p class="mega-subtitle">Утиліта автономного калібрування графіків, тестування кольорових палітр та контролю роздільної здатності наукових ілюстрацій</p>
            <div class="status-tags">
                <span class="tag tag-online">VISUAL SENTRY</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">RENDERING SHIELD</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-info">
            <span class="metric-label">Plot Target 1</span>
            <span class="metric-value">Errors Distribution</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📉</div>
        <div class="metric-info">
            <span class="metric-label">Plot Target 2</span>
            <span class="metric-value">Forecast Comparison</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">Export Quality</span>
            <span class="metric-value">300 DPI (High-Res)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧠</div>
        <div class="metric-info">
            <span class="metric-label">Data Source</span>
            <span class="metric-value">Statistical Mocks</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль візуального тестування</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/ml/test_plots.py</code> є виділеним **валідатором графічних компонентів** (Visual Analytics Validator) в архітектурі платформи <b>Energy Monitor Ultimate</b>. Він надає розробникам інструмент автономного тестування та високоточного калібрування дизайну графіків Matplotlib перед їх безпосередньою інтеграцією в інтерфейс користувача Streamlit або у звіт дипломної роботи (Thesis).
        </p>
        <p style="margin-top: 10px;">
            Основні інженерні напрями модуля:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Trend Comparison Sandbox (Пісочниця порівняння):</strong> Тестування суміщення трьох незалежних часових рядів на одному полотні — фактичного споживання (Real), прогнозу ARIMA та прогнозу LSTM з розрахунком RMSE.</li>
            <li><strong>Academic Plot Verification:</strong> Перевірка побудови гістограм похибок з накладанням теоретичних кривих щільності ймовірності Гауса та чорною обвідкою стовпчиків (edgecolor='black') для відповідності ДСТУ стандартам друку.</li>
            <li><strong>Rendering Quality Control (Контроль рендерингу):</strong> Тестування вивантаження графіків у стиснутому та безвтратному форматі PNG з високою щільністю пікселів (300 DPI).</li>
            <li><strong>Statistical Mocking:</strong> Генерація штучних гармонічних рядів та похибок для швидкої відладки дизайну без звернення до бази даних.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: WORKFLOW & RENDERING ENGINE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр графічної валідації (Rendering & Export Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема показує процес генерації та збереження тестових графіків:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск: test_plots.py") --> GENERATE_MOCKS("1. Statistical Mocking: ерація шумів та синусоїд")
                GENERATE_MOCKS --> DIS_COMP("2. plot_error_distribution()")
                
                DIS_COMP --> MATPLOT_1("3. Matplotlib subplots: figsize=(9, 6)")
                MATPLOT_1 --> GAUSS_CURVES("4. scipy.stats.norm.pdf() curves")
                GAUSS_CURVES --> EXPORT_1("5. Save: lstm_error_dist_v1_test.png (300 DPI)")
                
                EXPORT_1 --> FORECAST_COMP("6. plot_forecast_comparison()")
                FORECAST_COMP --> MATPLOT_2("7. Matplotlib subplots: figsize=(11, 6)")
                MATPLOT_2 --> PLOT_LINES("8. Draw lines: Real, ARIMA, LSTM")
                PLOT_LINES --> EXPORT_2("9. Save: forecast_comparison_v1_test.png (300 DPI)")
                
                EXPORT_2 --> END("Консольне повідомлення: Графіки згенеровані!")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичне моделювання тестових кривих</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Теоретична щільність Гауса (scipy.stats.norm.pdf)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для побудови плавних ліній розподілу похибок тестовий модуль розраховує ординати нормального розподілу для кожної координати $x$ на основі медіани $\mu$ та відхилення $\sigma$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ p(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2} \left(\frac{x - \mu}{\sigma}\right)^2} $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Генератор гармонічного навантаження (Statistical Mocking Sinusoid)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для відлагодження графіків порівняння трендів використовується 1-тижневий фрагмент (168 годин) синтетичного сигналу навантаження $L(t)$ з випадковим шумом:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ L(t) = 500 + 100 \sin\left(\frac{2\pi \cdot t}{24}\right) + \epsilon(t), \quad \text{де } \epsilon(t) \sim \mathcal{N}(0, 20^2) $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод циклу рендерингу</h2>
    </div>
    <div class="glass-card">
        <p>
            Алгоритм побудови суміщених трендів порівняння прогнозів:
        </p>
        <pre><code class="language-python">
# Псевдокод рендерингу суміщених графіків
def render_forecast_trends_test(time, actual, lstm, arima):
    # 1. Створення полотна з білим фоном (facecolor='white')
    figure, axis = plt.subplots(figsize=(11, 6), facecolor="white")
    axis.set_facecolor("white")
    
    # 2. Малювання ліній
    axis.plot(time, actual, color="#404040", linewidth=1.2, label="Actual")
    axis.plot(time, arima, color="orange", linestyle="--", label="ARIMA")
    axis.plot(time, lstm, color="blue", label="LSTM")
    
    # 3. Додавання легкої сітки та легенди з рамкою
    axis.grid(True, linestyle="-", alpha=0.3, color="gray")
    axis.legend(facecolor="white", edgecolor="lightgray")
    
    # 4. Експорт у високій роздільній здатності
    plt.tight_layout()
    plt.savefig("forecast_comparison_test.png", dpi=300, bbox_inches="tight")
    plt.close()
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому для графіків примусово задається білий фон facecolor='white'?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Деякі операційні системи або налаштування Matplotlib за замовчуванням рендерять прозорий фон (transparent background) для збережених зображень. При вставці такого графіка у темну тему сайту або у друковану версію диплома з білими аркушами чорний текст осей зливається з прозорим фоном, роблячи графік нечитабельним. Примусове встановлення білого фону гарантує однаково чітке відображення ілюстрацій на будь-яких носіях.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому на гістограмах Figure 7 додано edgecolor='black'?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: При друку наукових робіт або перегляді на екранах з низькою контрастністю напівпрозорі стовпчики гістограми без меж зливаються між собою, перетворюючись на однорідну колірну пляму. Чорна тонка обводка кожного стовпчика дозволяє чітко розрізняти межі окремих інтервалів (bins) розподілу.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як запустити калібрування графіків?</h4>
        <p style="color: var(--text-dim);">
            A: Виконайте команду: <code>python scripts/ml/test_plots.py</code>, після чого у робочій папці з'являться два тестові файли: <code>lstm_error_dist_v1_test.png</code> та <code>forecast_comparison_v1_test.png</code>.
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
