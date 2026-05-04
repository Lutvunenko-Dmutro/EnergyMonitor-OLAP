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
        <p>Пакет <code>src/ml/</code> є інтелектуальним центром системи ATLAS. Його місія — перетворення історичних даних та живих потоків телеметрії на точні прогнози майбутнього стану мережі. Ми використовуємо гібридний підхід, поєднуючи класичні статистичні моделі (ARIMA) для стабільного фону та сучасні нейронні мережі (LSTM) для вловлювання складних нелінійних залежностей. Це забезпечує надійність прогнозів навіть у періоди високої волатильності енергоспоживання.</p>
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
                    <th>Технологія</th>
                    <th>Функція</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>predict_v2.py</code></td><td>Основний інференс</td><td>ONNX Runtime</td><td>Прогноз в реальному часі</td></tr>
                <tr><td><code>train_lstm.py</code></td><td>Навчання нейромереж</td><td>PyTorch / LSTM</td><td>Генерація ваг моделей</td></tr>
                <tr><td><code>baseline_arima.py</code></td><td>Статистичний фон</td><td>Statsmodels (SARIMA)</td><td>Benchmark аналіз</td></tr>
                <tr><td><code>forecast_controller.py</code></td><td>Оркестратор ШІ</td><td>LRU Caching</td><td>Керування запитами ШІ</td></tr>
                <tr><td><code>backtest.py</code></td><td>Аудит точності</td><td>Time-series Split</td><td>Валідація на архівах</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: HYBRID FORECASTING STRATEGY -->
<div class="section-container" id="predict-v2">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Гібридного Прогнозування</h2></div>
    <div class="glass-card flow-step">
        <p>Наша стратегія базується на принципі <b>Multi-model Consensus</b>. Замість того, щоб покладатися на одну модель, ATLAS порівнює результати глибокого навчання (LSTM) з класичними методами. Це дозволяє виявляти аномалії в самих прогнозах: якщо результати моделей розходяться занадто сильно, система сигналізує про високу невизначеність, що є критично важливим для безпечного оперативного управління.</p>
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

<!-- SECTION 05: ONNX-BASED INFERENCE OPTIMIZATION -->
<div class="section-container" id="model-loader">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Оптимізація Інференсу через ONNX</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення високої продуктивності в браузерному середовищі, всі навчені моделі конвертуються у формат <b>ONNX (Open Neural Network Exchange)</b>. Це дозволяє проводити розрахунки з мінімальними затримками, не вимагаючи наявності важких фреймворків (як-от PyTorch) у середовищі виконання інтерфейсу. Модуль <code>predict_v2.py</code> реалізує цю логіку, забезпечуючи ідеальну швидкість відгуку системи.</p>
    </div>
</div>

<!-- SECTION 06: FEATURE ENGINEERING & VECTORIZATION -->
<div class="section-container" id="vectorizer">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Feature Engineering та Векторизація</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>vectorizer.py</code> відповідає за перетворення "сирих" позначок часу та значень навантаження у тензори, зрозумілі для ШІ. Ми використовуємо <b>Cyclical Encoding</b> для часу (Sin/Cos перетворення годин та місяців), що дозволяє моделі розуміти безперервність циклів споживання. Також проводиться динамічне масштабування (Scaling) для вирівнювання діапазонів різних підстанцій.</p>
    </div>
</div>

<!-- SECTION 07: AUTOMATED BACKTESTING & ERROR AUDIT -->
<div class="section-container" id="metrics">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Автоматизований Бектестинг та Аудит</h2></div>
    <div class="glass-card flow-step">
        <p>Впевненість у прогнозі неможлива без перевірки на минулому. <code>backtest.py</code> автоматично імітує ситуації "що було б, якби ми прогнозували тиждень тому", порівнюючи результати ШІ з реальними даними, що вже стали історією. Це дозволяє розраховувати динамічний довірчий інтервал (Confidence Interval) та постійно моніторити дрейф точності моделей.</p>
    </div>
</div>

<!-- SECTION 08: THE MODEL REGISTRY & LIFECYCLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Реєстр Моделей та Життєвий Цикл</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>model_loader.py</code> виконує роль <b>Model Registry</b>. Він автоматично знаходить найкращі версії ваг моделей у директорії <code>cache/models/</code>, перевіряє їх цілісність та завантажує в пам'ять. Це забезпечує безшовне оновлення інтелекту ATLAS: розробник може просто підкласти новий файл моделі, і система почне використовувати його без перезапуску.</p>
    </div>
</div>

<!-- SECTION 09: ANALYTIC METRICS & PERFORMANCE ENGINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Аналітичні Метрики та Двигун Оцінки</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>metrics_engine.py</code> зосереджена математика оцінки якості. Ми використовуємо не лише стандартні RMSE та MAE, а й специфічні для енергетики метрики: <i>Peak Load Deviation</i> та <i>Trend Sign Consistency</i>. Це дозволяє оцінювати корисність прогнозу не просто з точки зору математики, а з точки зору практичної цінності для диспетчера мережі.</p>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v6.0 (REINFORCEMENT LEARNING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v6.0 (RL-Grid Control)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 6.0 планується впровадження **Reinforcement Learning (RL)** для автономного управління балансуванням мережі. Система не просто прогнозуватиме дефіцит, а пропонуватиме оптимальні керуючі дії (вимикання/вмикання ліній) для мінімізації втрат та ризиків. Також буде додано підтримку <i>Explainable AI (XAI)</i>, щоб диспетчер міг бачити, які саме фактори найбільше вплинули на формування конкретного прогнозу.</p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="./atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
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
