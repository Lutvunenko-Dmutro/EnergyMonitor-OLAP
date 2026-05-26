# Технічний Паспорт Компонента: __init__.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">📦 CENTRAL PACKAGE NAMESPACE DISPATCHER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔌</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">__init__.py</h1>
            <p class="mega-subtitle">Універсальний диспетчер ініціалізації пакетів, менеджер просторів імен та ізолятор залежностей екосистеми ATLAS</p>
            <div class="status-tags">
                <span class="tag tag-online">INIT MODULE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">NAMESPACE EXPORTER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🧱</div>
        <div class="metric-info">
            <span class="metric-label">Execution Scope</span>
            <span class="metric-value">Package Load Time</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔄</div>
        <div class="metric-info">
            <span class="metric-label">Decoupling</span>
            <span class="metric-value">Circular Imports Shield</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-info">
            <span class="metric-label">Import Type</span>
            <span class="metric-value">Selective Export</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🩹</div>
        <div class="metric-info">
            <span class="metric-label">Performance</span>
            <span class="metric-value">No overhead (&lt;1ms)</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль та архітектурне призначення</h2>
    </div>
    <div class="glass-card">
        <p>
            У проєкті <i>Energy Monitor Ultimate</i> файли <code>__init__.py</code> є **основою модульної архітектури та просторів імен (Namespace Dispatchers)**. Згідно з методологією Clean Architecture, замість прямого зв'язування внутрішніх модулів із зовнішніми компонентами, кожен підпакет (наприклад, <code>scripts/thesis/converter/</code> або <code>src/core/analytics/</code>) реєструє свої головні інтерфейси у файлі <code>__init__.py</code>.
        </p>
        <p style="margin-top: 10px;">
            Основні задачі, які вирішують ініціалізаційні файли пакетів:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Експорт публічних інтерфейсів (Facade Pattern):</strong> Приховування детальної реалізації внутрішніх файлів та експорт лише стабільних функцій (наприклад, <code>run_conversion</code> з <code>.engine</code>) як єдиної точки входу для зовнішнього коду.</li>
            <li><strong>Запобігання круговим залежностям (Circular Imports Shield):</strong> Локалізація імпортів на рівні пакетів, що дозволяє уникнути циклічних зв'язків між класами та функціями.</li>
            <li><strong>Санітація просторів імен (Namespace Sanitation):</strong> Запобігання забрудненню глобального простору імен зайвими допоміжними змінними та внутрішніми функціями, які не мають використовуватися ззовні.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Схема диспетчеризації імпортів (Import Dispatching Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема ілюструє, як `__init__.py` виступає захисним шлюзом (фасадом), трансформуючи складні внутрішні шляхи модулів у чисті зовнішні виклики:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                CLIENT("Зовнішній клієнт: convert_thesis.py") --> IMPORT_CALL("1. Запит: from scripts.thesis.converter import run_conversion")
                
                IMPORT_CALL --> GATEWAY{"2. Звернення до scripts/thesis/converter/__init__.py"}
                
                GATEWAY --> REL_IMPORT("3. Локальний відносний імпорт: from .engine import run_conversion")
                REL_IMPORT --> SCAN_CORE("4. Читання конкретної реалізації в engine.py")
                
                SCAN_CORE --> RESOLVE("5. Повернення об'єкта функції клієнту")
                RESOLVE --> EXECUTE("6. Виконання run_conversion()")
                
                style GATEWAY fill:#1e293b,stroke:#38bdf8,stroke-width:2px
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математична модель ізоляції залежностей</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Концепція інтерфейсного фасаду (Facade mapping)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Нехай пакет $P$ складається з внутрішніх приватних підмодулів $M = \{m_1, m_2, \dots, m_k\}$, кожен з яких містить функції $f_{i,j}$. Простір імен `__init__.py` описується як виділена підмножина публічних експортованих інтерфейсів $I_{\text{public}} \subset \bigcup M$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ I_{\text{public}} = \{ \text{run\_conversion} \} \quad \implies \quad \forall f \in (M \setminus I_{\text{public}}): f \text{ є недоступним при import } P $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Формалізація кругової залежності (Circular dependency resolution)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    При прямому імпорті модулів $A \to B$ та $B \to A$, інтерпретатор Python генерує критичну помилку `ImportError` через незавершеність ініціалізації. Винесення точки зв'язку на рівень пакетного `__init__.py` перетворює граф залежностей $G$ з циклічного у спрямований ациклічний граф (DAG):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ G = (V, E) \quad \implies \quad E_{\text{new}} = \{ (A, P_B), (P_B, B_{\text{core}}) \} \quad (\text{де } P_B \text{ є ациклічним посередником}) $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод селективного експорту інтерфейсів</h2>
    </div>
    <div class="glass-card">
        <p>
            Структура `__init__.py` для чіткого керування доступними методами за допомогою списку `__all__`:
        </p>
        <pre><code class="language-python">
# Псевдокод ініціалізатора пакету (Facade Pattern)
# scripts/thesis/converter/__init__.py

# 1. Відносний імпорт внутрішніх реалізацій
from .engine import run_conversion as _run_conversion_core
from .config import INPUT, OUTPUT

# 2. Визначення публічного інтерфейсу пакету (Whitelist)
__all__ = [
    "run_conversion"
]

def run_conversion(input_path, output_path):
    """Публічний фасад для запуску конвертації."""
    return _run_conversion_core(input_path, output_path)
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Часті питання (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Навіщо потрібні порожні або мінімальні файли `__init__.py` у кожній директорії?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: У версіях Python 3.3+ концепція Namespace Packages дозволяє імпортувати файли з папок без `__init__.py`. Проте наявність цих файлів є суворим стандартом для великих архітектур. Вони явно маркують папку як логічний пакет коду, запобігають випадковим збігам шляхів імпорту та дозволяють прописати метадані ініціалізації для лінтерів та статичних аналізаторів коду (наприклад, MyPy).
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Що таке відносні імпорти (Relative Imports) та чому вони використовуються?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Відносні імпорти використовують крапку перед назвою модуля (наприклад, `from .engine import run_conversion`). Вони вказують Python шукати модуль у поточній папці поточного пакету, не перевіряючи глобальний системний шлях `sys.path`. Це гарантує повну портативність коду: якщо ми перейменуємо або перемістимо папку `converter/` в інше місце, всі внутрішні імпорти продовжать працювати без змін.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Що станеться, якщо спробувати імпортувати внутрішню функцію, яка не описана в `__init__.py`?</h4>
        <p style="color: var(--text-dim);">
            A: Якщо ми імпортуємо сам пакет (`import scripts.thesis.converter`), ми зможемо звернутися лише до тих функцій, які прописані в `__init__.py`. Внутрішні хендлери (наприклад, `add_formula` або `styles`) залишаться невидимими. Це запобігає випадковому виклику низькорівневих методів та гарантує, що клієнтський код використовує систему виключно через стабільний інтерфейс.
        </p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn">
        <span class="btn-icon">🔙</span>
        <span class="btn-text">Повернутися до Атласу</span>
    </a>
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
