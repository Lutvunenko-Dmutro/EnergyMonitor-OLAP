# Технічна специфікація модуля: layouts.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">FORECAST & BACKTEST LAYOUTS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📐</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">UI Layouts Orchestrator: layouts</h1>
            <p class="mega-subtitle">Оркестратор представлення. Керує складними інтерфейсними компоновками: Mega-Hybrid графіки, ітераційні цикли бектестування (Progress Bars) та академічні звіти (Scatter/Dist).</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT COMPONENTS</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">LAYOUT ENGINE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🎓</div><div class="metric-info"><span class="metric-label">Academic</span><span class="metric-value">Distribution & Scatter</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Backtest</span><span class="metric-value">Interactive Progress Loop</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Hybrid</span><span class="metric-value">History + Forecast Plot</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎯</div><div class="metric-info"><span class="metric-label">Metrics</span><span class="metric-value">RMSE, MAE, R2</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>layouts.py</b> розвантажує основний контролер <code>forecast.py</code>, забираючи на себе всю складність відмальовки специфічних "вікон". Його головне завдання — красиво і професійно скомпонувати дані, які ШІ-модель уже порахувала.</p>
        <p style="margin-top: 12px;">Тут реалізовано <b>Backtest Loop Orchestration</b>: коли користувач запускає бектест, цей модуль малює прогрес-бар, кнопки управління (Пауза/Продовжити/Зупинити), та ітеративно оновлює екран, поки не будуть оброблені всі 168 кроків (тиждень). Після завершення розрахунків модуль перемикається в режим <b>Academic Reporting</b>, де розвертає розширені KPI (RMSE, MAE, R²) та будує розподіли помилок (Histogram) і графіки кореляції (Scatter Plot) для глибокого аналізу ШІ.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_single_forecast_results(...) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Візуалізатор прогнозу однієї станції. Розраховує миттєві метрики (<code>calculate_instant_metrics</code>), викликає <code>get_fast_backtest</code> для фонової перевірки і накладає інтервали довіри (±1.96 * sigma) на DataFrame. Потім малює Mega-Hybrid графік (<code>_generate_mega_hybrid_figure</code>) та KPI панель. Опціонально розгортає Expander "Академічна аналітика" з графіками розподілу.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_backtest_execution_loop(sub_name, version, src_type) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Керує 3 фазами: 1. Фоновий ітеративний цикл: читає <code>bt_status</code>, малює прогрес-бар <code>curr_idx/168</code> та кнопки. Викликає <code>run_backtest_step(batch_size=24)</code>, поповнює масив та робить <code>st.rerun()</code>. 2. Фаза фіналізації: викликає <code>finalize_backtest_metrics</code> та розраховує фінальні RMSE/R². 3. Фаза звіту: якщо статус "finished" (або "multi_finished"), рендерить повний академічний звіт (Tabs: Часові ряди, Розподіл, Кореляція).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Backtest Execution Loop Пайплайн</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    LOOP("render_backtest_execution_loop()") --> CHK_STATE{"st.session_state\n[bt_status]"}
    
    CHK_STATE -->|'running'| BATCH("run_backtest_step(batch_size=24)")
    BATCH --> UPDATE("bt_idx += 24\nExtend bt_preds")
    UPDATE --> RERUN_RUN("st.rerun()")
    
    CHK_STATE -->|'finalizing'| FINALIZE("finalize_backtest_metrics()")
    FINALIZE --> METRICS("Save RMSE, MAE, R²\nSet status='finished'")
    METRICS --> RERUN_FIN("st.rerun()")
    
    CHK_STATE -->|'finished'| REPORT("Render Academic Report\nst.tabs & st.metric")
    REPORT --> PLOTS("generate_academic_plots()\n(Trend, Dist, Scatter)")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.ui_helpers (safe_plotly_render)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.components.charts (_generate_mega_hybrid_figure, generate_academic_plots)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.forecast_controller (calculate_instant_metrics)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.backtest (get_fast_backtest, run_backtest_step, finalize_backtest_metrics)</span>
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
