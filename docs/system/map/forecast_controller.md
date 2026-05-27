# Технічна специфікація модуля: forecast_controller.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AI ORCHESTRATOR & CACHE MANAGER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚦</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">AI Controller: forecast_controller</h1>
            <p class="mega-subtitle">Диспетчер між UI-шаром та ML-моделями. Забезпечує агресивне кешування (st.cache_data) результатів інференсу, бектестів та історичних даних для миттєвого відгуку дашборду.</p>
            <div class="status-tags"><span class="tag tag-online">CACHED CONTROLLER</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">ML ORCHESTRATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">Inference Cache</span><span class="metric-value">TTL 3600s</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Backtest Cache</span><span class="metric-value">TTL 3600s</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⏱️</div><div class="metric-info"><span class="metric-label">History Cache</span><span class="metric-value">TTL 600s</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛠️</div><div class="metric-info"><span class="metric-label">Cache Storage</span><span class="metric-value">RAM (Serialized)</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>forecast_controller.py</b> — це єдиний шлюз для всіх важких обчислень машинного навчання в системі. Замість того, щоб UI напряму викликав повільні ML-функції (що призвело б до зависання інтерфейсу при кожному кліку), він звертається до цього контролера.</p>
        <p style="margin-top: 12px;">Головне завдання контролера: обгорнути всі ML-виклики декораторами <code>@st.cache_data</code>. Це означає, що якщо користувач запитує прогноз (або бектест) з однаковими параметрами двічі (наприклад, просто перемикається між вкладками), результат повертається з пам'яті за 0.001с замість повторного прогону нейромережі.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def cached_ai_forecast(hours_ahead: int, substation_name: str, source_type: str, version: str, scenario: dict) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Кешована обгортка навколо <code>predict_v2.get_ai_forecast</code>. Транслює словник <code>scenario</code> (температура, health_score) у числові відхилення та константи. Кеш живе 1 годину. Показує спіннер "🧠 Neural Inference" під час першого обчислення.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def cached_fast_backtest(substation_name: str, version: str, source_type: str) → dict</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Кешована обгортка для повного історичного бектестингу моделі (порівняння передбачень з фактом на великому періоді). Запобігає надмірному навантаженню на БД. Кеш: 1 година.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_cached_history(sub: str, src: str) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Завантажує історичний таймсеріас або з бази, або з CSV (через <code>aggregator</code>). Кешується на 10 хвилин (оскільки живі дані можуть оновлюватись частіше).</p>
            </div>

            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def calculate_instant_metrics(df_hist: pd.DataFrame, version: str, sub_name: str, src_type: str) → Tuple[Optional[dict], float]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Викликає <code>evaluate_last_24h</code> для миттєвої оцінки точності на вчорашньому дні. Витягує <code>sigma</code> (стандартне відхилення помилки) для побудови довірчих інтервалів на графіку (повернутий fallback sigma = 0.05).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема кешованого інференсу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI("UI (forecast_view)") --> REQ("Call cached_ai_forecast(params)")
    REQ --> CACHE{st.cache_data\nHit?}
    
    CACHE -->|Yes| FAST("Return instantly from RAM")
    
    CACHE -->|No| EXTRACT("Parse scenario dict\n(temp_shift, health_score)")
    EXTRACT --> CALL_ML("Call get_ai_forecast()")
    
    CALL_ML --> ML_CORE[/"src.ml.predict_v2"/]
    ML_CORE --> RES("Return df_forecast")
    
    RES --> STORE("Store in Streamlit Cache\n(TTL = 3600s)")
    STORE --> OUT("Return to UI")
    FAST --> OUT
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.predict_v2.get_ai_forecast</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ml.backtest.get_fast_backtest</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.analytics.aggregator</span>
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
