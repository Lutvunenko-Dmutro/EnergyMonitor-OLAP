# Технічна специфікація модуля: validators.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SECURITY & VALIDATION LAYER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛡️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Input Shield: validators</h1>
            <p class="mega-subtitle">Багатошаровий захист від SQL-ін'єкцій, перевірка параметрів за білими списками, санітизація колонок та bounds-checking числових значень.</p>
            <div class="status-tags"><span class="tag tag-online">ANTI-INJECTION</span><span class="tag tag-version">v2.2.0</span><span class="tag tag-role">SECURITY GUARD</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🚫</div><div class="metric-info"><span class="metric-label">SQL Keywords</span><span class="metric-value">15 Dangerous Patterns</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">✅</div><div class="metric-info"><span class="metric-label">Whitelists</span><span class="metric-value">BUILTIN_NAMES + STEP_KEYS</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📏</div><div class="metric-info"><span class="metric-label">Bounds</span><span class="metric-value">date range + numeric limits</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Sanitize</span><span class="metric-value">SQL Identifier chars only</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>validators.py</b> — це "Вхідні двері" системи. Оскільки назви підстанцій і регіонів потрапляють у SQL-запити, зловмисник теоретично міг би передати <code>'; DROP TABLE --</code> замість назви.</p>
        <p style="margin-top: 12px;">Захист двошаровий: 1) <b>Keyword blocklist</b> — перевірка на 15 небезпечних SQL-ключових слів через <code>_has_dangerous_patterns()</code>. 2) <b>Whitelist validation</b> — для step_key та data_source перевірка по frozenset; якщо значення не в списку — виключення <code>ValidationError(ValueError)</code>. Окремо є <code>sanitize_column_name()</code> — лише <code>[a-zA-Z0-9_]</code> символи допустимі для динамічних SQL-ідентифікаторів. Усі функції ретельно задокументовані у форматі Google Docstring.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px;'>class ValidationError(ValueError)</code>
                <span style='font-size: 12px; color: var(--text-dim); margin-left: 8px;'>— Базовий клас помилки валідації</span>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px;'>def validate_substation_name(name, valid_names) → bool</code>
                <span style='font-size: 12px; color: var(--text-dim); margin-left: 8px;'>— None / str / list підтримка. BUILTIN_NAMES allowlist. SQL injection check.</span>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px;'>def validate_region_name(region) → bool</code>
                <span style='font-size: 12px; color: var(--text-dim); margin-left: 8px;'>— SQL-scan + max length 100 chars.</span>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px;'>def validate_date_range(start, end) → bool</code>
                <span style='font-size: 12px; color: var(--text-dim); margin-left: 8px;'>— start &lt;= end. Попередження при > 5 років.</span>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px;'>def validate_data_source(source) → bool</code>
                <span style='font-size: 12px; color: var(--text-dim); margin-left: 8px;'>— Whitelist: PostgreSQL / Kaggle / Cache / Historical.</span>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px;'>def sanitize_column_name(name, max_length=100) → str</code>
                <span style='font-size: 12px; color: var(--text-dim); margin-left: 8px;'>— Лише [a-zA-Z0-9_]. Для безпечних динамічних SQL ORDER BY.</span>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 13px;'>def validate_numeric_input(value, min_val, max_val) → bool</code>
                <span style='font-size: 12px; color: var(--text-dim); margin-left: 8px;'>— Перевірка типу та меж для числових параметрів.</span>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Валідації Вводу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("User Input\n(substation_name)") --> CHK_BUILTIN{"In BUILTIN_NAMES?\n'Усі підстанції'..."}
    CHK_BUILTIN -->|Yes| PASS("✅ Pass")
    CHK_BUILTIN -->|No| DANGEROUS("_has_dangerous_patterns()\n15 SQL keywords check")
    DANGEROUS -->|Found| RAISE("❌ raise ValidationError\n'Invalid characters'")
    DANGEROUS -->|Clean| WHITELIST{"valid_names\nprovided?"}
    WHITELIST -->|No| PASS
    WHITELIST -->|Yes, not in list| WARN("⚠️ logger.warning\n(soft fail, new station?)")
    WHITELIST -->|Yes, in list| PASS
    WARN --> PASS
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing (Optional, Union, List, Set)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime.date</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
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
