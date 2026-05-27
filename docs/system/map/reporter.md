# Технічна специфікація модуля: reporter.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DIAGNOSTICS REPORTING ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📊</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">HTML Health Auditor: reporter</h1>
            <p class="mega-subtitle">Трансформує результати технічного аудиту коду в автономний інтерактивний HTML-звіт з колірною індикацією критичності та підрахунком вразливостей.</p>
            <div class="status-tags"><span class="tag tag-online">HTML GENERATOR</span><span class="tag tag-version">v1.5.0</span><span class="tag tag-role">AUDIT RENDERER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Stats</span><span class="metric-value">OK / Warning / Error counts</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Style</span><span class="metric-value">Dark GitHub-Style HTML</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Security</span><span class="metric-value">Dedicated Issues Section</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📄</div><div class="metric-info"><span class="metric-label">Output</span><span class="metric-value">diagnostics_report.html</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>reporter.py</b> — це "Принтер" системи аудиту. Після того як <code>scanner.py</code> зробив всю важку роботу — обійшов файли, знайшов проблеми, склав список <code>FileDiag</code> — reporter перетворює цей Python-об'єкт на зручний HTML-документ.</p>
        <p style="margin-top: 12px;">Дизайн звіту навмисно копіює стиль GitHub: темний фон (<code>#0d1117</code>), колірні полоси зліва (<code>border-left: 4px solid #f85149</code> для помилок, <code>#d29922</code> для попереджень, <code>#3fb950</code> для OK). Звіт сортується автоматично: файли з <code>ERROR</code> завжди вгорі. Кожна картка файлу містить відповідні issues з їх рівнем та рядком коду.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>class HtmlReporter</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Клас без стану. Основний клас генерації звіту.</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def generate(results: list[FileDiag], output: Path) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головний метод. Рахує агрегати (total, ok, warn, err, sec_total). Сортує результати: спочатку ERROR-файли. Рендерить HTML через f-string. Записує файл (<code>output.write_text(html)</code>).</p>
            </div>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _file_row(r: FileDiag) → str</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Будує HTML-картку одного файлу. Використовує CSS клас <code>status-{r.status}</code> для кольору. Ітерується по <code>r.file_issues + r.security_issues</code> та рендерить кожну як <code>div.issue-item</code> з рядком коду.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Пайплайн Генерації Звіту</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("generate(results: list[FileDiag], output)") --> SORT("Sort results:\nERROR files first")
    SORT --> AGG("Count total, ok, warn, err\nCount security issues total")
    AGG --> ROWS("For each FileDiag:\n_file_row(r)")
    ROWS --> CSS("Apply status-{ERROR|WARNING|OK}\nborder-left color")
    CSS --> ISSUES("Render each DiagIssue:\nlevel + code + message (line)")
    ISSUES --> HTML("Assemble full HTML\nwith f-string template")
    HTML --> WRITE("output.write_text(html)\n→ diagnostics_report.html")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pathlib.Path</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.diagnostics.models (FileDiag)</span>
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
