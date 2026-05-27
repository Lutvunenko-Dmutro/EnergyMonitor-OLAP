# Технічна специфікація модуля: cards.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">UI INDICATORS LIBRARY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📟</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">UI Components: cards</h1>
            <p class="mega-subtitle">Бібліотека інтерактивних карток та індикаторів. Реалізує компактні візуальні елементи (Gauge Charts, Health Bars) для швидкої оцінки стану об'єктів мережі в дашбордах.</p>
            <div class="status-tags"><span class="tag tag-online">PLOTLY UI</span><span class="tag tag-version">v1.0.0</span><span class="tag tag-role">VISUAL COMPONENTS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🚥</div><div class="metric-info"><span class="metric-label">Gauge</span><span class="metric-value">Plotly Indicator (0-100%)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Health</span><span class="metric-value">Emoji Progress Bar</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔴</div><div class="metric-info"><span class="metric-label">Zoning</span><span class="metric-value">Green / Amber / Red</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Rendering</span><span class="metric-value">safe_plotly_render</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>cards.py</b> містить перевикористовувані (reusable) UI-компоненти для відображення ключових метрик підстанцій у "плитковому" (card) форматі.</p>
        <p style="margin-top: 12px;">Замість того, щоб дублювати код малювання "спідометрів" (Gauge) або індикаторів "здоров'я обладнання" (Health) в різних вкладках, всі вони винесені сюди. Модуль активно використовує <code>plotly.graph_objects.Indicator</code> для спідометрів та кастомну генерацію текстових емодзі для Health Score, що забезпечує дуже швидкий рендеринг без втрати інформативності.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def make_health_bar(h: float | pd.NA) → str</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Генерує текстовий прогрес-бар для "здоров'я" (Health Score, 0-100). Використовує символ 🟩 для заповненої частини та ⬜ для порожньої. Додає кольорове емодзі стану на початку (🟢 >= 85, 🟡 >= 60, 🔴 < 60). Повертає відформатований рядок.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render_gauge(value: float) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Рендерить Plotly Gauge (Спідометр). Налаштований на діапазон 0-100% з трьома кольоровими зонами ("steps"): Зелена (0-70), Помаранчева (70-90), та Червона (90-100). Має прозорий фон (<code>paper_bgcolor="rgba(0,0,0,0)"</code>) та рендериться через <code>safe_plotly_render</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема візуалізації</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI("Streamlit Column\n(Container)") --> CALL_G("render_gauge(85.5)")
    UI --> CALL_H("make_health_bar(92.0)")
    
    CALL_G --> PLOTLY("go.Figure(go.Indicator)\n+ Zones (Green, Amber, Red)")
    PLOTLY --> SAFE_RENDER("safe_plotly_render()")
    SAFE_RENDER --> VIEW_G("[Plotly Interactive Widget]")
    
    CALL_H --> MATH("round(92.0 / 10) = 9")
    MATH --> STR("9x🟩 + 1x⬜\n+ 🟢 Emoji")
    STR --> VIEW_H("String: '🟢 🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ 92.0%'")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>plotly.graph_objects</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.ui_helpers (safe_plotly_render)</span>
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
