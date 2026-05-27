# Технічна специфікація модуля: baseline_arima.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">STATISTICAL BASELINE ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📉</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">ARIMA/SARIMA Benchmarking: baseline_arima</h1>
            <p class="mega-subtitle">Наукова база для обґрунтування переваг методів глибокого навчання (LSTM) над класичною статистикою. Реалізує SARIMA з Grid Search оптимізацією.</p>
            <div class="status-tags"><span class="tag tag-online">STATSMODELS ENGINE</span><span class="tag tag-version">v1.0.0</span><span class="tag tag-role">BENCHMARKING</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Optimization</span><span class="metric-value">Grid Search (p, d, q)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📅</div><div class="metric-info"><span class="metric-label">Seasonality</span><span class="metric-value">SARIMA(24)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Forecasting</span><span class="metric-value">Rolling Window</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚖️</div><div class="metric-info"><span class="metric-label">Purpose</span><span class="metric-value">LSTM Comparison</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>baseline_arima.py</b> потрібен для формування "еталонного мінімуму" (Baseline). Щоб довести, що складна нейромережа LSTM має сенс, її результати порівнюються з класичною статистичною моделлю <code>SARIMA</code> (Seasonal Autoregressive Integrated Moving Average).</p>
        <p style="margin-top: 12px;">Модуль автоматично підбирає оптимальні гіперпараметри через Grid Search (<code>itertools.product</code>) та використовує жорстко задану добову сезонність (24 години). Прогноз виконується за методом "ковзаючого вікна" (Rolling One-Step-Ahead) для максимальної точності порівняння з LSTM.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def find_best_arima(train_data, test_data) → tuple</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Автоматизований підбір (Grid Search). Перебирає комбінації <code>p=[0,1,2]</code>, <code>d=[1]</code>, <code>q=[0,1]</code>. Для швидкості навчає модель і тестує її тільки на перших 72 кроках (3 дні) <code>test_data</code>. Знаходить комбінацію з мінімальним RMSE.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def rolling_arima_forecast(train_data, test_data, order, seasonal_order) → np.ndarray</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Rolling Window Forecast. Навчає <code>SARIMAX</code> на історії. Для кожного кроку в <code>test_data</code> робить прогноз на 1 годину вперед (One-Step), після чого додає реальний факт з тесту в модель без повного перенавчання (через <code>model_fit.append([obs], refit=False)</code>). Повертає масив прогнозів.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def run_arima_baseline(version, train_data, test_data, do_grid_search=False) → tuple</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний оркестратор. Якщо <code>do_grid_search</code>, викликає <code>find_best_arima</code>, інакше бере (1, 1, 1). Встановлює сезонність (1, 1, 1, 24). Викликає <code>rolling_arima_forecast</code> та розраховує кінцеві метрики MAPE та RMSE. Повертає (predictions, mape, rmse).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Rolling Window Forecast Логіка</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    INIT("SARIMAX.fit(train_data)") --> FORECAST_1("forecast(steps=1)")
    
    FORECAST_1 --> APPEND_1("append(test_data[0], refit=False)")
    
    APPEND_1 --> FORECAST_2("forecast(steps=1)")
    
    FORECAST_2 --> APPEND_2("append(test_data[1], refit=False)")
    
    APPEND_2 -.-> LOOP("... repeat for len(test_data) ...")
    
    LOOP --> EVAL("Calculate Metrics\n(RMSE, MAPE)")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>statsmodels.tsa.arima.model.ARIMA</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>statsmodels.tsa.statespace.sarimax.SARIMAX</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sklearn.metrics (mean_squared_error, mean_absolute_percentage_error)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>numpy</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>itertools (product)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>matplotlib.pyplot</span>
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
