# Технічний Паспорт Компонента: scripts/ml/benchmark_models.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🧬 SCIENTIFIC MODEL COMPARATOR & GRAPHICS CORE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📊</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">benchmark_models.py</h1>
            <p class="mega-subtitle">Двигун академічного бенчмаркінгу моделей, розрахунку коефіцієнтів детермінації R² та генерації наукових ілюстрацій</p>
            <div class="status-tags">
                <span class="tag tag-online">ACADEMIC ENGINE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">THESIS DISCOVERY</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📈</div>
        <div class="metric-info">
            <span class="metric-label">Target Substation</span>
            <span class="metric-value">ID 10 (Kyivska)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🎓</div>
        <div class="metric-info">
            <span class="metric-label">Baseline Model</span>
            <span class="metric-value">SARIMA Grid Search</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">Visual Figures</span>
            <span class="metric-value">Fig 5, Fig 7, Scatter</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚖️</div>
        <div class="metric-info">
            <span class="metric-label">Inference Mode</span>
            <span class="metric-value">One-Step-Ahead</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Академічна роль та науковий порівняльний аналіз</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/ml/benchmark_models.py</code> є виділеним **науковим компаратором** (Scientific Model Benchmarking Engine) в архітектурі платформи <b>Energy Monitor Ultimate</b>. Він розроблений для проведення кількісного та якісного порівняння інноваційного нейромережевого стеку моделей (LSTM V1, V2, V3) з класичними методами математичної статистики та прогнозування часових рядів (SARIMA).
        </p>
        <p style="margin-top: 10px;">
            Він формує доказову базу для дисертаційної роботи (Thesis) за трьома напрямами:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Генерація наукових ілюстрацій (Publication-ready Plots):</strong> Автоматичне вивантаження трьох ключових графіків у високій роздільній здатності (300 DPI) відповідно до вимог наукових видань (Comparison, Error Distribution, Scatter Plots).</li>
            <li><strong>Розрахунок коефіцієнтів детермінації $R^2$:</strong> Математична оцінка частки дисперсії залежної змінної, яка пояснюється нейромережею.</li>
            <li><strong>Параметризація похибок:</strong> Порівняльний аналіз статистичних розподілів похибок прогнозування для підтвердження переваги нелінійних рекурентних моделей над лінійними ARIMA.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: BENCHMARK WORKFLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр академічного порівняння (Scientific Benchmarking Workflow)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема відображає послідовність кроків порівняння моделей:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск: benchmark_models.py") --> INIT_SCENE("1. Створення папки results/")
                INIT_SCENE --> LOOP_VERSIONS("2. Цикл за версіями: v1, v2, v3")
                
                LOOP_VERSIONS --> LOAD_DATA("3. load_data_from_db() для ПС ID 10")
                LOAD_DATA --> SCALE_MINMAX("4. MinMaxScaler: розділення Train / Test (80/20)")
                SCALE_MINMAX --> LOAD_MODEL("5. Завантаження .h5 або .keras моделі")
                
                LOAD_MODEL --> PRED_ONE_STEP("6. Прогноз One-Step-Ahead (336 кроків)")
                PRED_ONE_STEP --> SARIMA_BASE("7. Оптимізація SARIMA (Grid Search)")
                SARIMA_BASE --> INVERSE_SCALE("8. Зворотне масштабування (inverse_transform)")
                
                INVERSE_SCALE --> CALC_METRICS("9. Метрики якості: RMSE, MAE, R²")
                CALCULATE_FIGS("10. Генерація графіків: Fig 5, Fig 7, Scatter (300 DPI)")
                
                CALC_METRICS --> CALCULATE_FIGS
                CALCULATE_FIGS --> CHECK_LAST{"11. Остання модель?"}
                CHECK_LAST -- "Ні" --> LOOP_VERSIONS
                CHECK_LAST -- "Так" --> END("Бенчмаркінг завершено успішно")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичний апарат порівняння та розподілу похибок</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Коефіцієнт детермінації ($R^2$ Score)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Вимірює частку поясненої дисперсії. Значення $R^2 = 1.0$ відповідає ідеальному прогнозу, тоді як $R^2 \le 0$ вказує на те, що прогноз моделі гірший за просте середнє:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ R^2 = 1 - \frac{\sum_{i=1}^N (y_i - \hat{y}_i)^2}{\sum_{i=1}^N (y_i - \bar{y})^2} $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Щільність нормального розподілу похибок (Normal Distribution Fit)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для Figure 7 (Error Distribution) розраховуються параметри нормального розподілу $\mathcal{N}(\mu, \sigma^2)$ для LSTM та ARIMA за допомогою методу максимальної правдоподібності:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ f(x | \mu, \sigma) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2} \left(\frac{x - \mu}{\sigma}\right)^2} $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Концентрованість похибок LSTM навколо нуля ($\mu \approx 0$) з мінімальним стандартним відхиленням $\sigma$ є науковим підтвердженням переваги нашої нейромережі.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Зворотне матричне масштабування (Inverse Scale Trick)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Моделі навчалися на багатофакторному наборі з $M$ колонок. Щоб де-нормалізувати окремий прогноз навантаження за допомогою <code>inverse_transform</code>, розроблено алгоритм алокації буфера-заглушки (dummy array):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    \mathbf{X}_{\text{dummy}} = \begin{bmatrix} \hat{\mathbf{y}}_{\text{scaled}} & \mathbf{0} & \dots & \mathbf{0} \end{bmatrix}_{N \times M} \quad \implies \quad \mathbf{y}_{\text{actual}} = \left(\text{Scaler}^{-1}(\mathbf{X}_{\text{dummy}})\right)[:, 0]
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму зворотної де-нормалізації</h2>
    </div>
    <div class="glass-card">
        <p>
            Алгоритм зворотної трансформації окремого одномірного вектора прогнозів:
        </p>
        <pre><code class="language-python">
# Псевдокод зворотної трансформації для багатовимірного скалера
def inverse_scale_single_column(scaled_predictions, scaler, total_features_count):
    import numpy as np
    length = len(scaled_predictions)
    
    # 1. Створення тимчасового буфера розмірністю (N x Features)
    dummy_matrix = np.zeros((length, total_features_count))
    
    # 2. Запис прогнозу у нульову колонку (load_mw)
    dummy_matrix[:, 0] = scaled_predictions
    
    # 3. Виклик зворотного перетворення
    unscaled_matrix = scaler.inverse_transform(dummy_matrix)
    
    # 4. Повернення розкодованого навантаження в реальних МВт
    return unscaled_matrix[:, 0]
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Що візуалізує "Figure 5: Comparison of forecasts"?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Графік порівнює фактичне навантаження енергомережі протягом 14 днів (336 годин) з прогнозами LSTM та класичної ARIMA. Це ключова ілюстрація для наукової доповіді, яка наочно показує, як нейромережа вловлює добову та тижневу сезонність споживання порівняно зі статистичним бейзлайном.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому для Figure 7 використовується крива нормального розподілу?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Розподіл похибок прогнозування в ідеальній моделі має наближатися до білого шуму з нормальним розподілом $\mathcal{N}(0, \sigma^2)$. Накладання теоретичної кривої Гауса поверх фактичних похибок LSTM та ARIMA дозволяє довести, що похибки нашої моделі є центрованими навколо нуля і мають значно меншу дисперсію.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Які файли моделей потрібні для роботи бенчмарку?</h4>
        <p style="color: var(--text-dim);">
            A: Скрипт очікує наявність скомпільованих файлів моделей <code>models/substation_model_v1.h5</code>, <code>substation_model_v2.h5</code> або <code>lstm_v3_multistep.keras</code> та відповідних pickle-файлів скалерів у директорії <code>models/</code>.
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
