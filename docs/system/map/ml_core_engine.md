# Технічна специфікація: Ядро Машинного Навчання та Прогнозування (ML CORE ENGINE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AI ANALYTICS | DEEP LEARNING & FORECASTING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧠</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Ядро Інтелекту</h1>
            <p class="mega-subtitle">Високотехнологічний комплекс ML-алгоритмів ATLAS: від предиктивних LSTM-мереж та ONNX-інференсу до статистичних ARIMA-бенчмарків та систем автоматичного аудиту точності</p>
            <div class="status-tags"><span class="tag tag-online">INFERENCE ACTIVE</span><span class="tag tag-version">v5.2.0</span><span class="tag tag-role">AI ORCHESTRATION</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Inference</span><span class="metric-value">ONNX Runtime Optimized</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📉</div><div class="metric-info"><span class="metric-label">Accuracy</span><span class="metric-value">RMSE-based Validation</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Training</span><span class="metric-value">Automated LSTM Pipeline</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Auditing</span><span class="metric-value">Backtest Verification</span></div></div>
</div>

<!-- SECTION 01: ARCHITECTURAL MISSION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Архітектурна Місія ML-Ядра</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/ml/</code> є інтелектуальним центром системи ATLAS. Його місія — перетворення історичних даних та живих потоків телеметрії на точні прогнози майбутнього стану мережі. Ми використовуємо гібридний підхід, поєднуючи класичні статистичні моделі (ARIMA) для стабільного фону та сучасні нейронні мережі (LSTM) для вловлювання складних нелінійних залежностей. Це забезпечує надійність прогнозів навіть у періоди високої волатильності енергоспоживання. Ядро спроектоване для роботи в умовах невизначеності, де кожна помилка може коштувати стабільності енергосистеми.</p>
    </div>
</div>

<!-- SECTION 02: ML MODULES MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Матриця Модулів Машинного Навчання</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль</th>
                    <th>Роль</th>
                    <th>Ключова Технологія</th>
                    <th>Математичний апарат</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>predict_v2.py</code></td><td>Основний інференс</td><td>ONNX Runtime</td><td>Recurrent Inference (Many-to-Many)</td></tr>
                <tr><td><code>train_lstm.py</code></td><td>Навчання нейромереж</td><td>PyTorch / LSTM</td><td>Adam Optimizer / MSE Loss</td></tr>
                <tr><td><code>baseline_arima.py</code></td><td>Статистичний фон</td><td>SARIMA</td><td>Auto-Regressive Integrated Moving Average</td></tr>
                <tr><td><code>forecast_controller.py</code></td><td>Оркестратор ШІ</td><td>LRU Caching</td><td>Dynamic Model Dispatcher</td></tr>
                <tr><td><code>backtest.py</code></td><td>Аудит точності</td><td>Time-series Split</td><td>Walk-forward Validation</td></tr>
                <tr><td><code>vectorizer.py</code></td><td>Feature Engineering</td><td>Scikit-learn / Numpy</td><td>Cyclic Temporal Encoding</td></tr>
                <tr><td><code>metrics_engine.py</code></td><td>Аудит точності</td><td>RMSE / MAE / sMAPE</td><td>Statistical Error Analysis</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: HYBRID FORECASTING STRATEGY -->
<div class="section-container" id="predict-v2">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Гібридного Прогнозування</h2></div>
    <div class="glass-card flow-step">
        <p>Наша стратегія базується на принципі <b>Multi-model Consensus</b>. Замість того, щоб покладатися на одну модель, ATLAS порівнює результати глибокого навчання (LSTM) з класичними методами. Це дозволяє виявляти аномалії в самих прогнозах: якщо результати моделей розходяться занадто сильно, система сигналізує про високу невизначеність, що є критично важливим для безпечного оперативного управління. Гібридизація також включає "сезонне змішування" (Seasons Blending), де історичні профілі навантаження використовуються як базовий шар для нейромережевої корекції.</p>
    </div>
</div>

<!-- SECTION 04: ML PIPELINE ARCHITECTURE -->
<div class="section-container" id="backtest">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Архітектура ML-Конвеєра (Pipeline)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA_CLEAN("Vectorizer: Feature Engineering") --> MODEL_LOAD("Model Loader: Registry")
    MODEL_LOAD --> INF_ENGINE("ONNX Inference Engine")
    INF_ENGINE --> FORECAST("Forecast Controller")
    
    subgraph AUDIT_LAYER["Integrity & Accuracy Audit"]
        BACKTEST("Backtest Engine")
        METRICS("Metrics Engine: RMSE/MAE")
    end
    
    FORECAST --> AUDIT_LAYER
    AUDIT_LAYER --> UI_OUTPUT("Dashboard Visualization")
    
    subgraph TRAINING_LAB["Off-line Training Lab"]
        TRAIN_LSTM("train_lstm.py")
        TRAIN_V1("train_v1.py")
    end
    
    TRAINING_LAB -- Artifacts --> MODEL_LOAD
</div></div>
</div>

<!-- SECTION 05: DEEP LEARNING ARCHITECTURE (LSTM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Архітектура Глибокого Навчання (LSTM)</h2></div>
    <div class="glass-card flow-step">
        <p>Для прогнозування ATLAS використовує багатошарову рекурентну архітектуру <b>LSTM (Long Short-Term Memory)</b>. Вона здатна утримувати в пам'яті як короткострокові коливання (наприклад, включення потужного споживача), так і довгострокові цикли (тижневі ритми роботи промисловості). LSTM-елемент містить фільтри для регулювання потоку інформації:</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #fff; margin: 15px 0; border: 1px solid var(--border);">
            $$ f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) \quad \text{(Forget Gate)} $$
            $$ i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) \quad \text{(Input Gate)} $$
            $$ \tilde{C}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c) $$
            $$ C_t = f_t * C_{t-1} + i_t * \tilde{C}_t \quad \text{(Cell State Update)} $$
            $$ o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) \quad \text{(Output Gate)} $$
            $$ h_t = o_t * \tanh(C_t) \quad \text{(Hidden State Output)} $$
        </div>
        <p>Вхідний вектор включає:</p>
        <ul>
            <li><code>L_t-1...L_t-n</code>: Історія навантаження (вікно 48 годин).</li>
            <li><code>T_ext</code>: Прогноз температури повітря.</li>
            <li><code>C_sin/C_cos</code>: Гармоніки часу доби та дня тижня.</li>
            <li><code>S_state</code>: Поточний стан обладнання (Binary health flags).</li>
        </ul>
        <p>На виході модель видає вектор прогнозних значень на наступні 24-72 години.</p>
    </div>
</div>

<!-- SECTION 06: ONNX-BASED INFERENCE OPTIMIZATION -->
<div class="section-container" id="model-loader">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Оптимізація Інференсу через ONNX</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення високої продуктивності в браузерному середовищі, всі навчені моделі конвертуються у формат <b>ONNX (Open Neural Network Exchange)</b>. Це дозволяє проводити розрахунки з мінімальними затримками, не вимагаючи наявності важких фреймворків (як-от PyTorch) у середовищі виконання інтерфейсу. Модуль <code>predict_v2.py</code> реалізує цю логіку, забезпечуючи ідеальну швидкість відгуку системи. Крім того, ONNX-інференс дозволяє системі ATLAS бути платформо-незалежною, легко розгортаючись як на серверних GPU, так і на легких Edge-пристроях.</p>
    </div>
</div>

<!-- SECTION 07: FEATURE ENGINEERING & VECTORIZATION -->
<div class="section-container" id="vectorizer">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Feature Engineering та Векторизація</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>vectorizer.py</code> відповідає за перетворення "сирих" позначок часу та значень навантаження у тензори, зрозумілі для ШІ. Ми використовуємо <b>Cyclical Encoding</b> для часу (Sin/Cos перетворення годин та місяців), що дозволяє моделі розуміти безперервність циклів споживання. Також проводиться динамічне масштабування (Scaling) для вирівнювання діапазонів різних підстанцій. Процес векторизації включає інтелектуальну обробку пропусків (Imputation) на основі середньозважених значень сусідніх періодів, що робить ШІ-ядро стійким до втрати пакетів телеметрії.</p>
    </div>
</div>

<!-- SECTION 08: AUTOMATED BACKTESTING & TIMEFRAME VALIDATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Протокол крос-валідації часових рядів (Walk-Forward)</h2></div>
    <div class="glass-card flow-step">
        <p>Для запобігання витоку інформації з майбутнього (data leakage) при оцінці якості моделей, у модулі <code>backtest.py</code> впроваджено Walk-Forward Time-Series Split.</p>
        
        <h4 style="color: var(--accent); margin-top: 15px; font-family: 'Orbitron', sans-serif;">Алгоритм бектестингу на ковзному вікні</h4>
        <pre><code class="language-python">
# Псевдокод реалізації Walk-Forward валідації
def run_walk_forward_backtest(model, data, initial_train_hours=8760, forecast_horizon=24, step_hours=168):
    total_hours = len(data)
    results = []
    
    current_train_end = initial_train_hours
    
    while current_train_end + forecast_horizon <= total_hours:
        # 1. Розділення на тренувальну та тестову вибірки
        train_set = data.iloc[0:current_train_end]
        test_set = data.iloc[current_train_end:current_train_end + forecast_horizon]
        
        # 2. Навчання або донавчання моделі на історичному вікні
        model.fit(train_set)
        
        # 3. Виконання багатокрокового прогнозу
        features = extract_features(test_set)
        predictions = model.predict(features)
        
        # 4. Збереження метрик якості
        actuals = test_set['actual_load'].values
        rmse = calculate_rmse(actuals, predictions)
        mae = calculate_mae(actuals, predictions)
        
        results.append({
            "test_timestamp": test_set.index[0],
            "predictions": predictions,
            "actuals": actuals,
            "rmse": rmse,
            "mae": mae
        })
        
        # 5. Просування навчального вікна вперед
        current_train_end += step_hours
        
    return results
        </code></pre>
    </div>
</div>

<!-- SECTION 09: ML TERMINOLOGY & EVALUATION METRICS -->
<div class="section-container" id="metrics">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Математика оцінки якості (Evaluation Metrics)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>metrics_engine.py</code> розраховує наступні фундаментальні метрики оцінки точності:</p>
        <ul>
            <li><b>RMSE (Root Mean Squared Error):</b> Дуже чутлива до великих похибок метрика, критична для енергомереж.
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; text-align: center; margin: 10px 0; border: 1px solid var(--border);">
                    $$ \text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2} $$
                </div>
            </li>
            <li><b>MAE (Mean Absolute Error):</b> Середня абсолютна похибка, що показує реальне відхилення в мегаватах.
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; text-align: center; margin: 10px 0; border: 1px solid var(--border);">
                    $$ \text{MAE} = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i| $$
                </div>
            </li>
            <li><b>sMAPE (Symmetric Mean Absolute Percentage Error):</b> Симетрична відносна похибка в межах $[0\%, 200\%]$.
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; text-align: center; margin: 10px 0; border: 1px solid var(--border);">
                    $$ \text{sMAPE} = \frac{100\%}{N} \sum_{i=1}^{N} \frac{|y_i - \hat{y}_i|}{(|y_i| + |\hat{y}_i|)/2} $$
                </div>
            </li>
        </ul>
    </div>
</div>

<!-- SECTION 10: THE MODEL REGISTRY & LIFECYCLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Реєстр Моделей та Життєвий Цикл</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>model_loader.py</code> виконує роль <b>Model Registry</b>. Він автоматично знаходить найкращі версії ваг моделей у директорії <code>cache/models/</code>, перевіряє їх цілісність за контрольними сумами та завантажує в пам'ять. Це забезпечує безшовне оновлення інтелекту ATLAS: розробник може просто підкласти новий файл моделі, і система почне використовувати його без перезапуску. Життєвий цикл моделі включає стадії: <i>Training -> Validation -> Candidate -> Production -> Archive</i>.</p>
    </div>
</div>

<!-- SECTION 11: DATA FLOW SEQUENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Sequence Diagram: Процес Прогнозування</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
sequenceDiagram
    participant UI as Dashboard UI
    participant FC as Forecast Controller
    participant VEC as Vectorizer
    participant INF as ONNX Engine
    participant DB as Historical DB
    
    UI->HFC: Request Forecast (sub_id, horizon)
    FC->>DB: Fetch last window (48h)
    DB-->>FC: Raw data
    FC->>VEC: Vectorize(data)
    VEC-->>FC: Tensors (Sin/Cos/Norm)
    FC->>INF: Run Inference
    INF-->>FC: Raw AI Output
    FC->>FC: Apply Bias Correction
    FC-->>UI: Structured JSON Forecast
</div></div>
</div>

<!-- SECTION 12: ROADMAP TO v6.0 (REINFORCEMENT LEARNING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v6.0 (RL-Grid Control)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 6.0 планується впровадження <b>Reinforcement Learning (RL)</b> для автономного управління балансуванням мережі. Система не просто прогнозуватиме дефіцит, а пропонуватиме оптимальні керуючі дії (вимикання/вмикання ліній) для мінімізації втрат та ризиків. Також буде додано підтримку <i>Explainable AI (XAI)</i> через алгоритми SHAP/LIME, щоб диспетчер міг бачити, які саме фактори (наприклад, різке падіння температури або вихідні дні) найбільше вплинули на формування конкретного прогнозу.</p>
    </div>
</div>

<!-- SECTION 13: TECHNICAL FAQ & TROUBLESHOOTING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">Технічний FAQ та Усунення Несправностей</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Яка мінімальна довжина вікна для точного прогнозу?</b><br>
        A: Для моделей V3 оптимальним є вікно 48 годин. Менші вікна призводять до втрати добової сезонності.</p>
        <p><b>Q: Як система реагує на різку зміну погоди?</b><br>
        A: Модуль <code>predict_v2.py</code> включає температурний градієнт у вхідний вектор, що дозволяє ШІ миттєво коригувати прогноз при отриманні нових метеоданих.</p>
        <p><b>Q: Що робити при високому RMSE?</b><br>
        A: Перевірте якість векторизації у <code>vectorizer.py</code> та переконайтеся, що вхідні дані не містять аномальних викидів, які не були відфільтровані.</p>
    </div>
</div>

<!-- SECTION 14: ML TERMINOLOGY GLOSSARY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">14</span><h2 class="section-title">Глосарій ML-термінів ATLAS</h2></div>
    <div class="glass-card flow-step">
        <ul>
            <li><b>Inference:</b> Процес отримання прогнозу від уже навченої моделі.</li>
            <li><b>Backtesting:</b> Перевірка моделі на історичних даних для оцінки її реальної точності.</li>
            <li><b>ONNX:</b> Універсальний формат обміну моделями, що забезпечує високу швидкість обчислень.</li>
            <li><b>LSTM:</b> Тип рекурентної нейронної мережі, спеціалізований на роботі з часовими рядами.</li>
        </ul>
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
