# Технічна специфікація модуля: header.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">FORECAST CONTROL HEADER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎛️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">UI Configuration: header</h1>
            <p class="mega-subtitle">Інтерактивна панель налаштування прогнозів з вбудованим детектором змін станів. Забезпечує What-If симуляцію через повзунки (Сценарії).</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT STATE</span><span class="tag tag-version">v1.3.0</span><span class="tag tag-role">CONTROL BAR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Detector</span><span class="metric-value">Session State Observer</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">What-If</span><span class="metric-value">Temp / H2 / Health</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Safety</span><span class="metric-value">Wipe on Fundamental Change</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧪</div><div class="metric-info"><span class="metric-label">Mode</span><span class="metric-value">Multi-Model Toggle</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>header.py</b> — це "штурвал" системи прогнозування. Його головна фішка — розумний <i>детектор змін</i>. Оскільки Streamlit перемальовує весь екран при будь-якому кліку, ми не можемо просто кешувати графіки: якщо користувач змінив модель з V1 на V2, нам потрібно <b>очистити старі прогнози</b>.</p>
        <p style="margin-top: 12px;">Модуль зберігає попередні значення (<code>last_version</code>, <code>last_sub_selection</code>) і постійно порівнює їх з поточними. Якщо є зміна — викликається <code>Comprehensive wipe</code>, який чистить десятки ключів з <code>st.session_state</code> та змушує систему перезавантажитись (<code>st.rerun</code>). Також тут розміщено Expander з повзунками "Що-Якщо" (для V2/V3), які дозволяють штучно змінити погоду та знос перед прогнозом.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_forecast_header(sub_name: str, sub_label: str, data_source: str) → tuple</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Повертає кортеж конфігурації: <code>(version, scenario, is_multi_model, src_type)</code>. Логіка: 1) Ініціалізує <code>last_*</code> змінні в стейті. 2) Рендерить toggle порівняння та selectbox архітектури (блокує його, якщо toggle=True або CSV режим). 3) Перевіряє умову <code>changed = (last_sub != sub_name or ...)</code>. 4) Якщо changed == True, видаляє масив ключів (<code>tab_fc_df</code>, <code>tab_bt_df</code>, etc.) та викликає <code>st.rerun()</code>. 5) Рендерить Expander з 3 слайдерами (Температура, H2, Health) та повертає їх у словнику <code>scenario</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Життєвий Цикл Детектора Змін</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("render_forecast_header()") --> UI_RENDER("Render Controls\n(Toggle, Select, Sliders)")
    
    UI_RENDER --> GET_CUR("Get Current: version, multi_mode")
    
    GET_CUR --> COMPARE{"Current == Last State?"}
    
    COMPARE -->|Yes| OK("Return\n(version, scenario, multi, src)")
    
    COMPARE -->|No| RESET("Set tab_active_mode = 'idle'")
    RESET --> UPDATE("Update last_ variables in state")
    UPDATE --> WIPE("del st.session_state[key]\nfor 12+ cache keys")
    WIPE --> RERUN("st.rerun()\nTrigger hard refresh")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.ui.views.forecast_components.constants (MODEL_LABELS)</span>
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
