# Технічна специфікація модуля: metrics_engine.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SCIENTIFIC ACCURACY AUDIT</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📐</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Analytical Metrics Engine: metrics_engine</h1>
            <p class="mega-subtitle">Реалізує комплексний апарат математичного та статистичного аналізу (RMSE, MAE, MAD, Shapiro-Wilk) для верифікації точності ШІ прогнозів.</p>
            <div class="status-tags"><span class="tag tag-online">SCIPY / SKLEARN</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">MATH VALIDATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Stats</span><span class="metric-value">Shapiro-Wilk (Normality)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Filter</span><span class="metric-value">3-Sigma MAD Threshold</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚖️</div><div class="metric-info"><span class="metric-label">Scale</span><span class="metric-value">Dynamic Scaling Factors</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎯</div><div class="metric-info"><span class="metric-label">Accuracy</span><span class="metric-value">RMSE, MAE, R², MAPE</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>metrics_engine.py</b> відповідає на одне критичне запитання: <i>"Наскільки сильно помилився ШІ?"</i>. Оскільки дані з сенсорів часто містять шуми (наприклад, станція різко вимкнулась на 1 хвилину), звичайні формули помилок дадуть хибні результати.</p>
        <p style="margin-top: 12px;">Цей модуль розв'язує проблему завдяки <b>Robust 3-Sigma MAD (Median Absolute Deviation)</b>. Він автоматично відкидає 100%-аномальні стрибки перед тим, як рахувати фінальні RMSE чи R². Також він проводить академічний статистичний аудит залишків (чи нормально розподілені помилки через критерій Шапіро-Уілка), та автоматично синхронізує прогнози ШІ з реальними даними з Бази Даних (Ground Truth Sync).</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def perform_statistical_audit(errors: np.ndarray) → Dict[str, Any]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Рахує математичну статистику для графіка розподілу (Histogram). Повертає: mu (середнє), sigma (станд. відх.), p_value (тест Шапіро), is_normal (p > 0.05), skew (асиметрія), kurt (ексцес).</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _get_outlier_mask(actual: np.ndarray, preds: np.ndarray) → np.ndarray</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Повертає булеву маску для фільтрації аномалій. Рахує <code>mad = np.median(np.abs(err - median))</code>. Обчислює поріг <code>3.5 * 1.4826 * mad</code> (із кліпінгом 100-5000) та відсікає помилки, що перевищують цей ліміт.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def finalize_backtest_metrics(...) → Optional[Tuple]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Огорнута в <code>@robust_ml_handler</code> функція фіналізації бектесту. Робить <code>inverse_transform</code> для зняття скейлінгу ШІ. Викликає <code>_get_ground_truth()</code> (запит до БД або Kaggle CSV). Робить внутрішній merge (Join по <code>timestamp</code>/<code>ts</code>). Застосовує <code>_get_outlier_mask</code>. Обчислює sklearn метрики: <code>mean_squared_error</code>, <code>mean_absolute_error</code>, <code>r2_score</code>, та MAPE. Повертає <code>(rmse, mae, mape, r2, None, merged_df)</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Валідації Точності</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("finalize_backtest_metrics()") --> UNNORM("scaler.inverse_transform(preds)")
    
    UNNORM --> TIME("Generate pd.DatetimeIndex\n(floor to hour)")
    
    TIME --> GT("_get_ground_truth()\nSQL JOIN LoadMeasurements & Substations")
    
    GT --> MERGE("pd.merge(preds_df, actual_df,\nby='timestamp')")
    
    MERGE --> MASK("_get_outlier_mask()\nMAD robust filtering")
    
    MASK --> CLEAN("Apply True/False mask to arrays")
    
    CLEAN --> METRICS("sklearn.metrics:\nRMSE, MAE, MAPE, R²")
    
    METRICS --> AUDIT("perform_statistical_audit(errors)\nShapiro-Wilk Test")
    
    AUDIT --> DONE("Return final scores to UI")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>numpy</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>scipy.stats (shapiro, skew, kurtosis)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sklearn.metrics (mean_squared_error, mean_absolute_error, r2_score)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database (run_query)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.predict_v2 (load_resources, _get_substation_peak_automated)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.kaggle_loader (load_kaggle_data)</span>
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
