# Технічна специфікація модуля: train_v1.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">BASELINE NEURAL TRAINING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧠</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">LSTM Baseline: train_v1</h1>
            <p class="mega-subtitle">Тренувальний скрипт для базової моделі LSTM (V1). Використовує спрощену архітектуру (univariate) виключно для порівняльного аналізу (Baseline) з класичними методами (ARIMA).</p>
            <div class="status-tags"><span class="tag tag-online">LEGACY TRAINING</span><span class="tag tag-version">v1.0.0</span><span class="tag tag-role">ML EXPERIMENT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Input Shape</span><span class="metric-value">Univariate (Load Only)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛠️</div><div class="metric-info"><span class="metric-label">Architecture</span><span class="metric-value">LSTM (64->64->32->1)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚖️</div><div class="metric-info"><span class="metric-label">Evaluation</span><span class="metric-value">Vs. ARIMA (14 Days)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🗄️</div><div class="metric-info"><span class="metric-label">Export</span><span class="metric-value">.h5 & .pkl</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>train_v1.py</b> є початковою точкою еволюції ML-ядра системи. Він реалізує найпростіший підхід до прогнозування: аналіз одновимірного часового ряду (лише історія навантаження, без температури чи іншої телеметрії). </p>
        <p style="margin-top: 12px;">Основна задача цього скрипта — не створити продакшен-модель, а згенерувати Baseline (базовий рівень). У кінці свого виконання скрипт автоматично проганяє навчену LSTM-мережу та класичну статистичну модель ARIMA на тих самих даних (14 днів) і генерує графіки порівняння, щоб обґрунтувати доцільність використання складніших нейромереж (V2, V3).</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def load_v1_data() → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Агрегує дані з таблиці <code>LoadMeasurements</code>. На відміну від V2/V3, ігнорує <code>substation_id</code>, підсумовуючи навантаження по всіх підстанціях (<code>SUM(avg_load)</code>) для отримання загального профілю системи. Виконує ресемплінг по годинах та лінійну інтерполяцію пропусків.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def create_sequences(data: np.ndarray, seq_length: int) → Tuple[np.ndarray, np.ndarray]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Трансформує плоский масив часового ряду у 3D-тензор для Keras. Кожен X — це вікно розміром <code>seq_length</code> (за замовчуванням 24 години), а Y — наступне значення навантаження (t+1).</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def train_and_evaluate() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний пайплайн: спліт даних 80/20 (без витоку даних), навчання MinMaxScaler, компіляція LSTM (64-64-32 нейрони, Dropout 0.2, Adam), тренування 20 епох. Після тренування запускає <code>run_arima_baseline()</code> на тестових 336 годинах і зберігає порівняльні PDF-звіти (MSE, MAE, R2).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн навчання та порівняння</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("python train_v1.py") --> LOAD("load_v1_data()\nAggregate Total Load")
    LOAD --> SCALE("MinMaxScaler(0,1)\nFit on 80% Train")
    SCALE --> SEQ("create_sequences()\nWindow=24h")
    
    SEQ --> SPLIT("Train (80%) / Test (20%)")
    SPLIT --> COMPILE("Compile LSTM Model\nLoss=MSE, Opt=Adam")
    
    COMPILE --> TRAIN("model.fit()\nEpochs=20, Batch=32")
    TRAIN --> SAVE("Save .h5 & .pkl")
    
    SAVE --> EVAL_LSTM("LSTM Predict (Test)\n14 Days (336h)")
    SAVE --> EVAL_ARIMA("ARIMA Predict (Test)\nrun_arima_baseline()")
    
    EVAL_LSTM --> METRICS("Calculate MSE, MAE, R2\nCompare LSTM vs ARIMA")
    EVAL_ARIMA --> METRICS
    
    METRICS --> PLOT("Generate Validation Plots\nSave to /results")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>tensorflow.keras</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sklearn.preprocessing</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.baseline_arima</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.utils.plots</span>
        </div>
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
