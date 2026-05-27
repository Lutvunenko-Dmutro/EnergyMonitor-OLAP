# Технічна специфікація модуля: scanner.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DEEP CODE INSPECTOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔍</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">System Audit Scanner: scanner</h1>
            <p class="mega-subtitle">Рекурсивний аудит кодової бази за допомогою Python AST. Виявляє відсутні імпорти, надто довгі функції, небезпечні конструкції та security-вразливості.</p>
            <div class="status-tags"><span class="tag tag-online">PYTHON AST</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">CODE QUALITY</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🏗️</div><div class="metric-info"><span class="metric-label">AST</span><span class="metric-value">Syntax + Import Walk</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚚</div><div class="metric-info"><span class="metric-label">Imports</span><span class="metric-value">Missing Module Detect</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📏</div><div class="metric-info"><span class="metric-label">Heuristic</span><span class="metric-value">UI=200L vs Core=100L</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Security</span><span class="metric-value">Regex Pattern Scan</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>scanner.py</b> — це "CI/CD пайплайн" в мінімалістичному Python-форматі. Він обходить всю кодову базу та знаходить проблеми, не запускаючи жодного рядка коду (через AST-парсинг).</p>
        <p style="margin-top: 12px;">Особлива фішка — <b>Context-Aware Thresholds</b>: якщо файл знаходиться в папці <code>ui/</code>, то допустима довжина функції — 200 рядків (бо UI-функції за природою довгі через рендеринг). Для всіх інших модулів порог — 100 рядків. При аналізі імпортів, сканер будує динамічний список доступних модулів через рекурсивний обхід директорій, щоб не помилково позначати внутрішні модулі як "missing".</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>class ProjectScanner(root: Path)</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Конструктор. Зберігає <code>root</code>. Будує <code>_available_modules</code> через <code>_build_module_set()</code>: рекурсивно знаходить всі .py файли в <code>SCAN_DIRS</code> і конструює всі можливі варіанти їх імен (пакет + модуль).</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def scan_all() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Збирає всі .py файли з <code>SCAN_DIRS</code> (ігноруючи <code>EXCLUDE_DIRS</code>). Для кожного файлу викликає <code>_analyze_file(fpath)</code> та накопичує результати у <code>self.results</code>.</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _analyze_file(fpath: Path) → FileDiag</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Ядро аудиту. Читає файл (<code>errors='replace'</code> для бінарних символів). Парсить через <code>ast.parse()</code>. Послідовно викликає: <code>_check_imports()</code>, <code>_check_functions()</code>, <code>_check_file_patterns()</code>, <code>_check_security()</code>. Ловить <code>SyntaxError</code> і зберігає місце помилки.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Аналізу Файлу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("scan_all()") --> COLLECT("Glob SCAN_DIRS\nFilter EXCLUDE_DIRS")
    COLLECT --> LOOP("For each .py file:")
    LOOP --> READ("fpath.read_text(errors='replace')")
    READ --> AST_PARSE("ast.parse(source)")
    AST_PARSE --> CHK_IMP("_check_imports()\nFind missing 3rd-party")
    CHK_IMP --> CHK_FN("_check_functions()\nLong fn > 100/200 lines")
    CHK_FN --> CHK_PAT("_check_file_patterns()\nFind print() calls")
    CHK_PAT --> CHK_SEC("_check_security()\nRegex SECURITY_PATTERNS")
    CHK_SEC --> DIAG("Return FileDiag()")
    DIAG --> LOOP
    LOOP -->|Done| RESULTS("self.results ready\nfor HtmlReporter")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>ast</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>re</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>importlib.util</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pathlib.Path</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.diagnostics.models (FileDiag, FunctionDiag, DiagIssue)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.diagnostics.patterns (SCAN_DIRS, SECURITY_PATTERNS, thresholds...)</span>
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
