# Технічна специфікація модуля: filter.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATA FILTERING & CONDITIONING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔍</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Analytical Pre-processor: filter</h1>
            <p class="mega-subtitle">Забезпечення безпечної, валідованої та високопродуктивної "нарізки" даних (Slicing) для потреб UI-візуалізації. Централізований шар фільтрації DataFrame.</p>
            <div class="status-tags"><span class="tag tag-online">PANDAS ENGINE</span><span class="tag tag-version">v1.5.0</span><span class="tag tag-role">SECURITY LAYER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Validation</span><span class="metric-value">Strict Whitelisting</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📐</div><div class="metric-info"><span class="metric-label">Slicing</span><span class="metric-value">Multi-dimensional</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Performance</span><span class="metric-value">Vectorized Masking</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Adaptive</span><span class="metric-value">Dataset-aware Logic</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>filter.py</b> виконує роль "митника" (Pre-processor) між базою даних та графіками Streamlit. Його задача — взяти "сирий" великий датасет та швидко відрізати від нього тільки те, що просить користувач (за регіоном, підстанцією та часовим діапазоном).</p>
        <p style="margin-top: 12px;">Особливість модуля — <b>Безпека (Validation)</b>. Перш ніж застосувати фільтри до масиву <code>pandas</code>, він проганяє вхідні параметри через строгі валідатори (<code>validate_region_name</code>, <code>validate_substation_name</code>) для запобігання ін'єкціям чи маніпуляціям (наприклад, передача дуже великого масиву в <code>isin()</code>). Сама фільтрація працює через швидкі булеві маски (Vectorized Masking), що дозволяє обробляти мільйони рядків за долі секунди.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def filter_dataframe(df: pd.DataFrame, region: str, dates: tuple, dataset_name: str, substation: str|List) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний метод. Спочатку проводить перевірку типів та валідацію вводу. Потім послідовно накладає маски: 1) Регіон (якщо не дорівнює ALL_REGIONS), 2) Підстанція (підтримує як точний string матч, так і <code>isin()</code> для списків), 3) Дати (через булеве <code>dt.date >= start & dt.date <= end</code>). Має адаптивну логіку — наприклад, для датасету <code>alerts</code> часовий фільтр ігнорується, щоб показати всі існуючі інциденти.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн фільтрації</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("filter_dataframe(df, args)") --> VAL("Input Validation\n(Type Check & Security Whitelist)")
    
    VAL --> EMPTY{"Is df.empty?"}
    EMPTY -->|Yes| OUT_EARLY("Return Empty df")
    
    EMPTY -->|No| REGION{"Region Filter\n!= 'ALL'?"}
    REGION -->|Yes| APPLY_REG("df = df[df['region_name'] == region]")
    REGION -->|No| SUB{"Substation Filter\n!= 'ALL'?"}
    
    APPLY_REG --> SUB
    
    SUB -->|Yes| APPLY_SUB("df = df[df['substation_name'].isin(list)]")
    SUB -->|No| DATE{"Dataset != 'alerts'\n& Dates provided?"}
    
    APPLY_SUB --> DATE
    
    DATE -->|Yes| APPLY_DATE("Mask: dt.date >= start & <= end\ndf = df.loc[mask]")
    DATE -->|No| OUT_FINAL("Return Filtered df")
    
    APPLY_DATE --> OUT_FINAL
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime.date</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing (Union, List, Optional, Tuple)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.app.config.DataKeys</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.validators (validate_*, ValidationError)</span>
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
