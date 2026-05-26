# Технічна специфікація: Двигун Системної Діагностики та Валідації (DIAGNOSTICS ENGINE HUB)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM INTEGRITY | QUALITY ASSURANCE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛡️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Центр Діагностики</h1>
            <p class="mega-subtitle">Шар інтелектуального контролю якості ATLAS: автоматичний пошук патернів помилок, моніторинг цілісності ML-моделей та формування комплексних звітів про стан здоров'я системи</p>
            <div class="status-tags"><span class="tag tag-online">SCANNER ACTIVE</span><span class="tag tag-version">v3.0.0</span><span class="tag tag-role">QUALITY GATE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Scanning</span><span class="metric-value">Deep Metadata Audit</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Patterns</span><span class="metric-value">Error Signature Mapping</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Reporting</span><span class="metric-value">Automated Health Score</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">ML Audit</span><span class="metric-value">Drift & Integrity Scan</span></div></div>
</div>

<!-- SECTION 01: THE MISSION OF DIAGNOSTICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Місія Системної Діагностики</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/core/diagnostics/</code> виконує роль "Імунної системи" проекту ATLAS. В складних аналітичних комплексах помилка в даних або в параметрах моделі може призвести до хибних прогнозів, що мають серйозні економічні наслідки. Наш двигун діагностики забезпечує превентивне виявлення таких проблем, аналізуючи метадані, структуру часових рядів та внутрішні стани нейронних мереж ще до того, як результати потраплять до оператора. Система гарантує, що кожен біт інформації відповідає стандартам наукової достовірності.</p>
    </div>
</div>

<!-- SECTION 02: DIAGNOSTICS MODULES MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Матриця Модулів Діагностики</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль</th>
                    <th>Функціональна Роль</th>
                    <th>Методологія</th>
                    <th>Рівень Аналізу</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>scanner.py</code></td><td>Глибоке сканування</td><td>AST / Regex Parsing</td><td>Структура коду/даних</td></tr>
                <tr><td><code>patterns.py</code></td><td>Аналіз сигнатур</td><td>ML Classifier / Rules</td><td>Семантика помилок</td></tr>
                <tr><td><code>models.py</code></td><td>Аудит ML-моделей</td><td>Graph Integrity Scan</td><td>Ядро інтелекту</td></tr>
                <tr><td><code>reporter.py</code></td><td>Генератор звітів</td><td>Templating Engine</td><td>Executive Summary</td></tr>
                <tr><td><code>compliance.py</code></td><td>Контроль стандартів</td><td>Policy Enforcement</td><td>Compliance & Audit</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: DEEP METADATA SCANNING STRATEGY -->
<div class="section-container" id="scanner">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Глибокого Сканування Метаданих</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>scanner.py</code> ми реалізуємо алгоритм <b>Multi-level Inspection</b>. Система використовує регулярні вирази та аналіз абстрактного синтаксичного дерева (AST) для перевірки відповідності встановленим стандартам ATLAS.</p>
        <p>Перевірці підлягають:</p>
        <ul>
            <li><b>Passport Integrity:</b> Наявність та коректність тегів <code># ATLAS_PASSPORT</code> та їх структурованих полів.</li>
            <li><b>API Consistency:</b> Перевірка сигнатур функцій на відповідність технічному завданню.</li>
            <li><b>Docstring Coverage:</b> Автоматичний підрахунок покриття коду коментарями.</li>
        </ul>
        <p>Будь-які відхилення автоматично потрапляють у список завдань на виправлення (Audit Backlog).</p>
    </div>
</div>

<!-- SECTION 04: DIAGNOSTIC PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема Діагностичного Конвеєра</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    CODE_BASE("ATLAS Codebase & Data") --> SCANNER("scanner.py: Deep Inspection")
    SCANNER -- Metadata --> PATTERNS("patterns.py: Signature Match")
    SCANNER -- AI Models --> ML_AUDIT("models.py: Integrity Check")
    
    PATTERNS --> REP_GEN("reporter.py: Orchestrator")
    ML_AUDIT --> REP_GEN
    
    REP_GEN --> PDF("Technical Health Report")
    REP_GEN --> UI_DASH("Admin Dashboard")
</div></div>
</div>

<!-- SECTION 05: AUDIT & COMPLIANCE STANDARDS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Стандарти Аудиту та Відповідності</h2></div>
    <div class="glass-card flow-step">
        <p>Проект ATLAS розроблявся з урахуванням високих вимог до академічної та промислової документації. Модуль діагностики розраховує підсумковий індекс здоров'я системи за наступною формулою:</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 14px; color: #fff; margin: 15px 0; border: 1px solid var(--border); text-align: center;">
            $$ \text{HealthScore} = \max\left(0, 100 - \left( 15.0 \cdot N_{\text{crit}} + 5.0 \cdot N_{\text{major}} + 1.0 \cdot N_{\text{minor}} \right)\right) $$
        </div>
        <p>Де $N_{\text{crit}}$, $N_{\text{major}}$, $N_{\text{minor}}$ — кількість виявлених критичних помилок, серйозних невідповідностей та дрібних попереджень відповідно.</p>
    </div>
</div>

<!-- SECTION 06: ERROR SIGNATURE & PATTERN MAPPING -->
<div class="section-container" id="patterns">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Мапування Сигнатур та Паттернів Помилок</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>patterns.py</code> дозволяє системі ATLAS "вчитися на помилках". Ми створюємо бібліотеку сигнатур відомих проблем. Алгоритм порівнює поточний стан системи з базою сигнатур, використовуючи відстань Левенштейна та тематичне моделювання. Це дозволяє не просто констатувати факт помилки, а вказувати на її першопричину (Root Cause Analysis), що значно прискорює технічне обслуговування системи та підвищує її MTTR (Mean Time To Repair).</p>
    </div>
</div>

<!-- SECTION 07: DIAGNOSTIC SEQUENCE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Sequence: Процес діагностичного циклу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
sequenceDiagram
    participant Sys as ATLAS System
    participant Sc as Scanner.py
    participant Pa as Patterns.py
    participant Re as Reporter.py
    
    Sys->>Sc: Trigger Full Audit
    Sc->>Sc: Scan Metadata & AST
    Sc->>Pa: Analyze Found Anomalies
    Pa-->>Sc: Return Error Signatures
    Sc->>Re: Compile Audit Findings
    Re->>Re: Calculate Health Score
    Re-->>Sys: Final Health Report (PDF/MD)
</div></div>
</div>

<!-- SECTION 08: AST STATIC CODE ANALYSIS DEEP DIVE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Статичний аналіз через AST (Abstract Syntax Tree)</h2></div>
    <div class="glass-card flow-step">
        <p>Для перевірки безпеки коду та виявлення прихованих дефектів (наприклад, незакритих з'єднань з базою або неоптимальних циклів) застосовується синтаксичний аналізатор на базі бібліотеки AST.</p>
        
        <h4 style="color: var(--accent); margin-top: 15px; font-family: 'Orbitron', sans-serif;">Реалізація AST-сканера для пошуку незахищених SQL запитів</h4>
        <pre><code class="language-python">
import ast

class SQLInjectionSafetyScanner(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def visit_Call(self, node):
        # 1. Пошук викликів функцій виконання запитів (execute, run_query)
        if isinstance(node.func, ast.Name) and node.func.id in ['execute', 'run_query']:
            if len(node.args) > 0:
                first_arg = node.args[0]
                # 2. Перевірка чи використовується конкатенація рядків / f-рядки замість параметризації
                if isinstance(first_arg, (ast.BinOp, ast.JoinedStr)):
                    self.violations.append({
                        "line": node.lineno,
                        "col": node.col_offset,
                        "type": "CRITICAL_SQL_INJECTION_RISK",
                        "message": "Raw string concatenation detected in query parameters. Use dict/tuple binds instead."
                    })
        self.generic_visit(node)

def analyze_file_safety(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    
    try:
        tree = ast.parse(source)
        scanner = SQLInjectionSafetyScanner()
        scanner.visit(tree)
        return scanner.violations
    except SyntaxError as se:
        return [{"line": se.lineno, "type": "SYNTAX_ERROR", "message": str(se)}]
        </code></pre>
    </div>
</div>

<!-- SECTION 09: ML MODEL INTEGRITY AUDIT -->
<div class="section-container" id="models">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Аудит Цілісності ML-Моделей</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>models.py</code> фокусується на безпеці ШІ. Він аналізує графіки обчислень ONNX-моделей на наявність некоректних шарів або неоптимальних шляхів виконання. Також проводиться перевірка вхідних та вихідних тензорів на відповідність фізичним обмеженням енергосистеми. Якщо ШІ видає "неможливе" значення (наприклад, навантаження вище потужності генератора), діагностичний двигун блокує цей прогноз та ініціює Fallback-процедуру.</p>
    </div>
</div>

<!-- SECTION 10: AUTOMATED REPORTING & DOCUMENTATION -->
<div class="section-container" id="reporter">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Автоматизована Звітність та Документація</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки <code>reporter.py</code> результати діагностики перетворюються на структуровані документи. Система автоматично генерує <i>System Health Score</i> — єдину метрику, що відображає загальний стан проекту. Ці звіти є критично важливими для проходження технічних аудитів та захисту наукових робіт, забезпечуючи доказову базу стабільності ATLAS. Кожен звіт містить перелік критичних правок (Critical Fixes) та рекомендації щодо оптимізації архітектури.</p>
    </div>
</div>

<!-- SECTION 11: ROADMAP TO v4.0 (SELF-HEALING ARCHITECTURE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Дорожня карта v4.0 (Self-healing)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 4.0 планується перехід до <b>Архітектури Самозцілення</b>. Система діагностики зможе не лише виявляти проблеми, а й автоматично застосовувати "патчі" (наприклад, перемикання на резервну БД або завантаження попередньої стабільної версії моделі). Також буде додано підтримку <i>Predictive Maintenance</i> для самого коду, виявляючи потенційні місця виникнення помилок на основі аналізу історії коммітів та складності коду за метрикою Маккейба.</p>
    </div>
</div>

<!-- SECTION 12: DIAGNOSTICS TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Технічний FAQ Діагностики</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Як додати нову сигнатуру помилки в базу?</b><br>
        A: Потрібно додати опис регулярного виразу та метадані проблеми у файл конфігурації модуля <code>patterns.py</code>.</p>
        <p><b>Q: Чи впливає робота сканера на продуктивність основної системи?</b><br>
        A: Ні, сканер працює в окремому асинхронному потоці або як фонове завдання, використовуючи лише вільні ресурси CPU.</p>
        <p><b>Q: Як інтерпретувати Health Score?</b><br>
        A: 100 — ідеальний стан; нижче 70 — рекомендується перевірка логів; нижче 40 — критичні структурні збої, що потребують негайного втручання.</p>
    </div>
</div>

<!-- SECTION 13: DIAGNOSTICS ENGINE GLOSSARY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">Глосарій Двигуна Діагностики</h2></div>
    <div class="glass-card flow-step">
        <ul>
            <li><b>AST (Abstract Syntax Tree):</b> Деревоподібне представлення структури вихідного коду для глибокого аналізу.</li>
            <li><b>Error Signature:</b> Унікальний відбиток (паттерн) певної технічної проблеми.</li>
            <li><b>Health Score:</b> Агрегований показник надійності та цілісності системи.</li>
            <li><b>Root Cause Analysis (RCA):</b> Метод виявлення першопричини виникнення дефекту.</li>
        </ul>
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
