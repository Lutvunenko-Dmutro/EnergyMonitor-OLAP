# Технічна специфікація модуля: backtest.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">HISTORICAL BACKTESTING ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📉</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">ML Validation Hub: backtest</h1>
            <p class="mega-subtitle">Механізм верифікації моделей машинного навчання. Забезпечує оцінку точності прогнозів (1-Step-Ahead) на історичних даних за допомогою векторизованих обчислень.</p>
            <div class="status-tags"><span class="tag tag-online">ONNX INFERENCE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">QUALITY ASSURANCE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Evaluation</span><span class="metric-value">1-Step-Ahead</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Execution</span><span class="metric-value">Vectorized Batch</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Metrics</span><span class="metric-value">RMSE, MAE, R²</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Safety</span><span class="metric-value">@robust_ml_handler</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>backtest.py</b> є ядром перевірки якості нейромереж. Його завдання — відповісти на запитання "А наскільки точно ця модель передбачила б навантаження, якби ми запустили її вчора?".</p>
        <p style="margin-top: 12px;">Він бере історичні дані, "заморожує" їх на певному моменті часу, робить прогноз (Inference) через завантажену ONNX модель, і порівнює цей прогноз з <i>реальним</i> фактом, який ми вже знаємо. Завдяки векторизації NumPy (передача в модель відразу цілого батчу вікон), цей процес відбувається миттєво, що дозволяє тестувати декілька архітектур одночасно прямо в UI без зависань.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@robust_ml_handler<br>def get_fast_backtest(substation_name: str, version: str) → Optional[Tuple]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Основний метод. Завантажує модель та скейлер (<code>load_resources</code>), отримує вікно даних (<code>get_latest_window</code>), і формує 3D тензор <code>X_batch</code>. Проганяє весь батч через ONNX Runtime за 1 виклик. Повертає кортеж результатів (rmse, mae, mape, r2, error, DataFrame).</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@robust_ml_handler<br>def evaluate_last_24h(substation_name: str, version: str) → Optional[Dict[str, float]]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Полегшена версія бектесту, призначена для швидкого аудиту виключно останніх 24 годин. Розраховує метрики точності за допомогою <code>sklearn.metrics</code> та повертає їх у вигляді словника. Зручно для швидкого моніторингу статусу (health-check) моделі.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@robust_ml_handler<br>def run_backtest_step(version: str, shared_values: np.ndarray, current_idx: int) → List[float]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Ітеративний метод для симуляції процесу "в реальному часі". Запускає інференс невеликими порціями (батчами по 24 години). Використовувався у старіших версіях UI з прогрес-баром.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Векторизований процес оцінки</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI("UI Request") --> CALL("get_fast_backtest()")
    
    CALL --> LOAD("load_resources(v)\nLoad ONNX & Scaler")
    LOAD --> DATA("get_latest_window()\nFetch History (Test_Size + Window)")
    
    DATA --> FEAT("select_features_v2()\nExtract [Load, Temp, etc.]")
    FEAT --> SCALE("_get_scaling_factor()\nScale Matrix")
    
    SCALE --> BATCH("np.array(List Comprehension)\nBuild 3D Tensor: [Batch, Window, Features]")
    
    BATCH --> ORT("model.run(X_batch)\nONNX Vectorized Inference")
    
    ORT --> INVERSE("scaler.inverse_transform()")
    INVERSE --> METRICS("finalize_backtest_metrics()\nRMSE, MAE, R²")
    
    METRICS --> UI_RES("Return: Metrics Tuple")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>numpy</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sklearn.metrics</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.predict_v2</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.vectorizer</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.metrics_engine</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.error_handlers (@robust_ml_handler)</span>
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
