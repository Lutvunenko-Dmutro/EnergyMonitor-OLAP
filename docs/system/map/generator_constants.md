# Технічна специфікація модуля: generator_constants.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SUBSTATION REGISTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏭</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Capacity Constants: generator_constants</h1>
            <p class="mega-subtitle">Технічний паспорт об'єктів енергосистеми. Містить нормативні показники встановлених потужностей (МВт) для забезпечення реалізму фізичної симуляції.</p>
            <div class="status-tags"><span class="tag tag-online">METADATA</span><span class="tag tag-version">v1.0.0</span><span class="tag tag-role">STATIC REGISTRY</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🗺️</div><div class="metric-info"><span class="metric-label">Mapping</span><span class="metric-value">Name to Capacity (MW)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚓</div><div class="metric-info"><span class="metric-label">Role</span><span class="metric-value">Simulation Anchoring</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎯</div><div class="metric-info"><span class="metric-label">Precision</span><span class="metric-value">Real-world Scales</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Type</span><span class="metric-value">Static Dictionary</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>generator_constants.py</b> слугує фізичним якорем (Anchor) для "цифрового двійника". Щоб симуляція виглядала правдоподібно, навантаження різних підстанцій має відрізнятися в рази.</p>
        <p style="margin-top: 12px;">Цей файл містить єдиний словник <code>BASE_CAPACITY_MAP</code>, що зіставляє назви українських енерговузлів з їх реальною (або наближеною) максимальною пропускною здатністю. Ці константи читаються модулями <code>db_seeder</code> та <code>data_generator</code> перед розрахунком відсоткового навантаження, перетворюючи абстрактні відсотки на конкретні Мегавати.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Структура даних</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>BASE_CAPACITY_MAP</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Python Dictionary. Ключі — точні назви підстанцій (String, наприклад "ПС Запорізька"), значення — базова потужність у МВт (Float, наприклад 3200.0). Якщо підстанції немає в словнику, генератори використовують fallback-логіку або 100.0 МВт за замовчуванням.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <p style="color: var(--text-dim); margin-bottom: 0;"><i>Цей модуль не має зовнішніх залежностей.</i></p>
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
