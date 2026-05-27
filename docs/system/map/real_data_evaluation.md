# Технічний Паспорт Компонента: scripts/ml/real_data_evaluation.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">📈 REAL-WORLD TELEMETRY MODEL EVALUATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧠</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">real_data_evaluation.py</h1>
            <p class="mega-subtitle">Емпіричний валідатор ШІ-моделей на реальних історичних архівах, порівняння з Persistence Baseline та генератор наукових фігур</p>
            <div class="status-tags">
                <span class="tag tag-online">EVALUATOR ENGINE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">SCIENTIFIC PROVER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-info">
            <span class="metric-label">Baseline Type</span>
            <span class="metric-value">Persistence Naive</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Stitch Horizon</span>
            <span class="metric-value">14 Days (336 hours)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">Output Figures</span>
            <span class="metric-value">Fig 5 & Fig 7 (300 DPI)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🩺</div>
        <div class="metric-info">
            <span class="metric-label">Loss Function</span>
            <span class="metric-value">MSE / MAE (Float32)</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль та наукова гіпотеза</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/ml/real_data_evaluation.py</code> є виділеним **емпіричним валідатором** (Real-World Model Evaluator) платформи <b>Energy Monitor Ultimate</b>. Він вирішує критично важливе наукове завдання — доводить ефективність розробленої архітектури LSTM нейромережі на реальних історичних архівах енергосистеми шляхом порівняння точності прогнозів з класичною "наївною" моделлю (Naive Persistence Baseline).
        </p>
        <p style="margin-top: 10px;">
            Основний функціонал валідатора:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Зчитування реальної телеметрії (Fetch Real Data):</strong> Запит до таблиці <code>LoadMeasurements</code> бази даних PostgreSQL для отримання часових рядів навантаження по підстанції ID=10 (ПС Київська-Центральна).</li>
            <li><strong>Порівняльний аналіз з Persistence Baseline:</strong> Розрахунок точності "наївного" прогнозу (прогноз на завтра = фактичне навантаження сьогодні) як нижнього порогу ефективності.</li>
            <li><strong>Зшивання безперервного прогнозу (Stitched Continuous Forecast):</strong> Алгоритм об'єднання 14 послідовних добових прогнозів у суцільний 336-годинний ряд для побудови Figure 5.</li>
            <li><strong>Статистичний розподіл похибок (Gaussian normal fit):</strong> Розрахунок математичного сподівання $\mu$ та стандартного відхилення $\sigma$ похибок прогнозу для наочної демонстрації переваги LSTM (Figure 7).</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: WORKFLOW & STITCHING ALGORITHM -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр емпіричної валідації (Evaluation & Stitching Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Діаграма ілюструє процес навчання, розрахунку прогнозів та зшивання результатів у суцільні 14-денні ряди:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск: real_data_evaluation.py") --> FETCH("1. Зчитування LoadMeasurements (ПС ID 10)")
                FETCH --> SPLIT("2. Розділення Train/Test за часовим індексом (80/20)")
                
                SPLIT --> SCALE("3. MinMaxScaler: Нормалізація в [0, 1]")
                SCALE --> WIN_GEN("4. Створення ковзних вікон: look_back=24 -> horizon=24")
                
                WIN_GEN --> TRAIN("5. Навчання LSTM в пісочниці: 50 епох, Adam(lr=0.001)")
                TRAIN --> PRED("6. Розрахунок прогнозів LSTM та Naive Baseline")
                
                PRED --> INVERSE("7. inverse_transform: Зворотне масштабування в реальні МВт")
                INVERSE --> STITCH("8. Алгоритм зшивання прогнозів (Stitching): крок = 24 години")
                
                STITCH --> GRAPH_5("9. Figure 5: Stitched 14-day Continuous plot (300 DPI)")
                STITCH --> GRAPH_7("10. Figure 7: Comparative Gaussian Error Distribution (300 DPI)")
                
                GRAPH_5 & GRAPH_7 --> END("Збереження результатів та вихід")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичне обґрунтування Persistence Baseline та зшивання</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Наївна модель перенесення (Naive Persistence Baseline)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Наївне прогнозування базується на припущенні, що завтрашній день $y(t + 24)$ буде ідентичним сьогоднішньому дню $x(t)$. Для нормалізованого вікна $X_{\text{test}} \in \mathbb{R}^{S \times 24 \times 1}$ наївний прогноз отримується спрощеною зміною розмірності (reshape):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \hat{y}_{\text{naive}}(t + i) = x(t - 24 + i) \quad (\forall i \in [0, 23]) $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Алгоритм зшивання прогнозів (Stitched Continuous Array)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Оскільки кожне ковзне вікно дає прогноз на 24 години, просте накладання призведе до наявності 24 дублюючих значень для кожної години. Для побудови безперервної лінії 14 днів (336 годин) застосовується кроковий пробіг з інтервалом $\Delta = 24$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \mathbf{A}_{\text{stitched}} = \bigcup_{k=0}^{K} \hat{\mathbf{y}}[k \cdot 24] \quad (\text{де } K = 14) $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Це створює суцільну часову шкалу без розривів та усереднень.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Гаусові щільності похибок (Figure 7 Normal fit)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для LSTM та Baseline розраховуються параметри розподілу Гауса $\mathcal{N}(\mu, \sigma^2)$. Тест доводить наукову гіпотезу: розмах похибок LSTM $\sigma_{\text{lstm}}$ є суттєво меншим за $\sigma_{\text{naive}}$, а медіана $\mu_{\text{lstm}}$ лежить ближче до 0.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму зшивання рядів</h2>
    </div>
    <div class="glass-card">
        <p>
            Алгоритм зшивання добових прогнозів у суцільний часовий ряд 14 днів:
        </p>
        <pre><code class="language-python">
# Псевдокод зшивання часових рядів (Stitching Engine)
def stitch_forecast_horizons(y_real_matrix, preds_matrix, days=14):
    total_hours = days * 24
    stitched_actual = []
    stitched_forecast = []
    
    # Робимо крок рівно у 24 години
    for i in range(0, min(total_hours, len(y_real_matrix)), 24):
        # Додаємо повний добовий масив (24 значення)
        stitched_actual.extend(y_real_matrix[i])
        stitched_forecast.extend(preds_matrix[i])
        
    return stitched_actual, stitched_forecast
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому як бейзлайн обрано саме Persistence Naive модель, а не класичну ARIMA?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Модель Persistence (наполегливості) є найпростішим і водночас найсуворішим базовим порогом для добових прогнозів в енергосистемах. Оскільки енергоспоживання має виражений добовий ритм, прогноз "завтра буде як сьогодні" є досить точним. Будь-яка складна ШІ-модель має обов'язково довести, що вона суттєво перевершує цей наївний поріг за показниками RMSE/MAE, інакше її впровадження є недоцільним.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому зшивання відбувається кроками по 24 години?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Наша модель прогнозує вектор на 24 години вперед. При ковзному вікні з кроком 1 година ми отримуємо 24 перекриваються прогнози на кожну фізичну годину. Якщо зшивати їх з кроком 1, ми отримаємо суміш прогнозів різної глибини. Зшивання кроком 24 години відображає реальний добовий сценарій диспетчеризації: раз на добу о 00:00 розраховується план навантаження на наступні 24 години.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Які вихідні графіки генерує скрипт?</h4>
        <p style="color: var(--text-dim);">
            A: Скрипт зберігає два файли у високій роздільній здатності 300 DPI для наукових публікацій: <code>figure_5_continuous.png</code> (порівняння ліній навантаження) та <code>figure_7_comparison.png</code> (порівняння розподілів похибок Гауса).
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
