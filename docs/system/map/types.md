# Технічна специфікація модуля: types.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">TYPE DEFINITION REGISTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">💎</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Data Contracts: types</h1>
            <p class="mega-subtitle">Реєстр типізованих аліасів для статичного аналізу системи. Визначає контракти між ML, Core та UI компонентами через TypeAlias та Dataclasses.</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON TYPING</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">DATA CONTRACTS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🗄️</div><div class="metric-info"><span class="metric-label">DataDict</span><span class="metric-value">Dict[str, DataFrame]</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🤖</div><div class="metric-info"><span class="metric-label">PredictionResult</span><span class="metric-value">forecast + rmse + meta</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">FilterParams</span><span class="metric-value">region + dates + sub</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💚</div><div class="metric-info"><span class="metric-label">HealthStatus</span><span class="metric-value">cpu + memory + db_ok</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>types.py</b> — це "Словник мови" системи. В Python типізація не є обов'язковою, але без неї великий проєкт перетворюється на хаос: IDE не може підказати, які поля є у словнику, PyRight/mypy не можуть знайти помилки.</p>
        <p style="margin-top: 12px;">Цей модуль вирішує проблему, надаючи іменовані TypeAlias для кожного "конверта даних" в системі. Наприклад, замість того щоб писати <code>Dict[str, Union[pd.DataFrame, str, int]]</code> скрізь, ви пишете просто <code>BootData</code>. IDE (і читач) відразу розуміє що це — дані з boot sequence. Це "живий документ": кожен аліас супроводжується docstring з описом полів.</p>
    </div>
</div>

<!-- SECTION 02: TYPE CATALOG -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Каталог Типів (TypeAlias)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>DataDict = Dict[str, pd.DataFrame]</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Словник завантажених даних {load, gen, alerts, lines, fin}</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>DateRange = Tuple[date, date]</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— (start_date, end_date) з DatePicker</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>SubstationSelection = Union[str, List[str]]</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Одна або список підстанцій</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>PredictionResult = Dict[str, Union[DataFrame, float, dict]]</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— {forecast: df, rmse: float, metadata: dict}</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>MetricsDict = Dict[str, float]</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— {accuracy: 0.95, mse: 0.001, mae: 0.01}</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>AlertData = Dict[str, Union[str, float, bool]]</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— {substation, level, severity, timestamp}</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>FilterParams = Dict[str, Union[str, DateRange, List[str], None]]</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Параметри фільтрації сайдбару</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>BootData = Dict[str, Union[DataFrame, str, int]]</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— Повернений результат splash.py</span></div>
            <div style='padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent);'><code style='color: var(--accent); font-size: 13px;'>HealthStatus = Dict[str, Union[float, str, bool]]</code><span style='font-size: 12px; color: var(--text-dim); margin-left: 10px;'>— {cpu: 0.45, memory: 0.65, db_healthy: True}</span></div>
        </div>
    </div>
</div>

<!-- SECTION 03: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing (Dict, List, Tuple, Optional, Union)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>dataclasses (dataclass)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime (date, datetime)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
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
