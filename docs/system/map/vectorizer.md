# Технічна специфікація модуля: vectorizer.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ML FEATURE ENGINEERING ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔢</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">LSTM Data Vectorizer: vectorizer</h1>
            <p class="mega-subtitle">Трансформація часових рядів у тензори для LSTM. Циклічне кодування часу (Sine/Cosine), версійний відбір фіч (V1-V3), ковзне вікно 48 год.</p>
            <div class="status-tags"><span class="tag tag-online">NUMPY TENSORS</span><span class="tag tag-version">v3.0.0</span><span class="tag tag-role">FEATURE ENGINEERING</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🎡</div><div class="metric-info"><span class="metric-label">Temporal</span><span class="metric-value">Sin/Cos (hour + weekday)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🗃️</div><div class="metric-info"><span class="metric-label">Versions</span><span class="metric-value">V1: 1f / V2: 5f / V3: 9f</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🪟</div><div class="metric-info"><span class="metric-label">Window</span><span class="metric-value">DEFAULT = 48 годин</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩹</div><div class="metric-info"><span class="metric-label">Imputation</span><span class="metric-value">Linear + ffill/bfill</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>vectorizer.py</b> — це "Кухар" ML-пайплайну. Сирі дані БД або Kaggle CSV не можна прямо передати в нейромережу. Їх потрібно підготувати: вибрати правильні колонки, закодувати час, нормалізувати, сформувати вікна.</p>
        <p style="margin-top: 12px;">Найцікавіший прийом — <b>Циклічне кодування часу</b>: замість числа "23" для 23:00 (яке LSTM сприйме як "майже 24, дуже близько до 0"), використовуються <code>sin(2π * h / 24)</code> і <code>cos(2π * h / 24)</code>. Це дозволяє нейромережі "зрозуміти" кругову природу доби. Підтримка трьох версій (V1/V2/V3) дозволяє поступово розширювати набір фіч: V1 — тільки навантаження, V3 — повний набір з телеметрією та часовими ознаками.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def select_features_v2(data, version="v3") → np.ndarray</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Вибирає потрібні колонки залежно від версії. V1: <code>[actual_load_mw]</code>. V2: +temperature_c, h2_ppm, health_score, air_temp. V3: +hour_sin/cos, day_sin/cos. Якщо DataFrame — додає відсутні колонки як 0.0. Якщо ndarray — додає нульовий padding до правильного розміру.</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_latest_window(substation_name, source_type, version, offset_hours, window_size) → Tuple</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головна публічна функція. Визначає Is_All (чи це агрегований запит). Для <code>source_type="CSV"</code> — викликає <code>_fetch_window_csv()</code>. Для <code>"Live"</code> — будує SQL через <code>_build_live_sql()</code>, виконує <code>run_query()</code>. Сортує, інтерполює, викликає <code>_prepare_features()</code>. Повертає: <code>(values: np.ndarray, constants: dict, last_ts: Timestamp, feature_names: list)</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Feature Engineering</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("get_latest_window(\nsubstation, source, version)") --> SRC_CHK{"source_type"}
    
    SRC_CHK -->|CSV| CSV("_fetch_window_csv()\nload_kaggle_data()\ngroup + sort + slice")
    SRC_CHK -->|Live| SQL("_build_live_sql()\nrun_query(DB)")
    
    CSV --> INTERP("df.interpolate(linear)\nffill + bfill gaps")
    SQL --> INTERP
    
    INTERP --> TEMPORAL("_prepare_features():\nhour_sin = sin(2π * h / 24)\nhour_cos = cos(2π * h / 24)\nday_sin = sin(2π * d / 7)\nday_cos = cos(2π * d / 7)")
    
    TEMPORAL --> SELECT("select_features_v2(df, version)\nV1: 1f | V2: 5f | V3: 9f")
    
    SELECT --> RETURN("Return:\n(values, constants, last_ts, f_names)")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>numpy</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing (Tuple, Optional, Dict, List, Any)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database (run_query)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.kaggle_loader (load_kaggle_data) [lazy import]</span>
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
