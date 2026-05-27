# Технічна специфікація модуля: models.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DIAGNOSTICS DATA MODELS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🏗️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Quality Assurance Schema: models</h1>
            <p class="mega-subtitle">Визначає базові структури даних (Dataclasses) для системи автоматичного аудиту проєкту. Фіксує проблеми (Issues) на рівнях функцій та файлів.</p>
            <div class="status-tags"><span class="tag tag-online">DATACLASSES</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">DATA SCHEMAS</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🐛</div><div class="metric-info"><span class="metric-label">DiagIssue</span><span class="metric-value">Severity, Code, Line</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">FunctionDiag</span><span class="metric-value">AST Function Stats</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📄</div><div class="metric-info"><span class="metric-label">FileDiag</span><span class="metric-value">Syntax & Imports Status</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Aggregates</span><span class="metric-value">Dynamic Status Properties</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>models.py</b> (у папці diagnostics) відіграє роль "Конституції" для сканера коду. Сканер не може просто повертати текст про помилки — йому потрібні строгі структури даних, які потім можна передати у генератор звітів (напр. markdown чи JSON).</p>
        <p style="margin-top: 12px;">Модуль використовує модуль <code>@dataclass</code> з Python для створення легковагових контейнерів. Основна фішка — розумні <code>@property</code>. Наприклад, замість того щоб вручну рахувати загальний статус файлу (OK/WARNING/ERROR), клас <code>FileDiag</code> автоматично сканує всі прикріплені до нього функції (<code>FunctionDiag</code>) і всі <code>DiagIssue</code>, та динамічно визначає свій загальний <code>status</code> і кількість знайдених проблем (<code>total_issues</code>).</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Схема Даних (Dataclasses)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@dataclass class DiagIssue</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Базовий блок проблеми. Містить: <code>severity</code> ("ERROR"|"WARNING"|"INFO"), <code>code</code> (ідентифікатор), <code>message</code> (опис), опціональну <code>line</code> (номер рядка), та <code>category</code>.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@dataclass class FunctionDiag</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Контейнер аналізу однієї функції. Містить: <code>name</code>, <code>lineno</code>, <code>lines</code>, та масив <code>issues: List[DiagIssue]</code>. Має <code>@property status</code>, що повертає ERROR якщо є хоч один ERROR-issue, інакше WARNING або OK.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>@dataclass class FileDiag</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Контейнер цілого файлу. Зберігає шлях (<code>path</code>, <code>rel_path</code>), <code>syntax_ok</code>, списки <code>imports</code> та <code>missing_imports</code>, масив <code>functions</code> та глобальні <code>file_issues</code> і <code>security_issues</code>. Включає складні <code>@property</code> агрегатори: <code>status</code> (глобальна оцінка), <code>total_issues</code> (сума всіх проблем файлу + функцій), <code>security_status</code> (безпека).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Ієрархія Моделей Аудиту</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
classDiagram
    class DiagIssue {
        +String severity
        +String code
        +String message
        +int line
        +String category
    }

    class FunctionDiag {
        +String name
        +int lineno
        +int lines
        +List~DiagIssue~ issues
        +status() String
    }

    class FileDiag {
        +Path path
        +bool syntax_ok
        +List~String~ imports
        +List~String~ missing_imports
        +List~FunctionDiag~ functions
        +List~DiagIssue~ file_issues
        +List~DiagIssue~ security_issues
        +status() String
        +total_issues() int
        +security_status() String
    }

    FileDiag "1" *-- "many" FunctionDiag : contains
    FileDiag "1" *-- "many" DiagIssue : file/security issues
    FunctionDiag "1" *-- "many" DiagIssue : logic issues
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>dataclasses (dataclass, field)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing (Optional, List)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pathlib (Path)</span>
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
