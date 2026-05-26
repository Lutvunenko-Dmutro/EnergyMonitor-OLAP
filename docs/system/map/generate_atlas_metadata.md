# Технічний Паспорт Компонента: scripts/system/generate_atlas_metadata.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🧬 AUTOMATED DOCUMENTATION ARCHITECT</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🕸️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">generate_atlas_metadata.py</h1>
            <p class="mega-subtitle">Інтелектуальний архітектор документації, семантичний парсер AST-дерев та генератор графа топології проєкту</p>
            <div class="status-tags">
                <span class="tag tag-online">METADATA ENGINE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">GRAPH BUILDER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📂</div>
        <div class="metric-info">
            <span class="metric-label">Target Structure</span>
            <span class="metric-value">Full Repo Scan</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🌳</div>
        <div class="metric-info">
            <span class="metric-label">Parsing Method</span>
            <span class="metric-value">Python AST (ast.parse)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Graph Artifacts</span>
            <span class="metric-value">JSON / JS Serialize</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛠️</div>
        <div class="metric-info">
            <span class="metric-label">Filters</span>
            <span class="metric-value">18+ Excluded Paths</span>
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
            Модуль <code>scripts/system/generate_atlas_metadata.py</code> — це **серце автоматизованої системи інвентаризації та документування** платформи <i>Energy Monitor Ultimate</i>. Він автоматично сканує репозиторій, виявляє файлову структуру, парсить семантичні описи з модулів і будує орієнтований граф залежностей (імпортів) між усіма компонентами системи.
        </p>
        <p style="margin-top: 10px;">
            Ключові можливості генератора метаданих:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Project Tree Crawler (Обхід репозиторію):</strong> Рекурсивний обхід файлової системи за допомогою <code>os.walk</code> з тонким налаштуванням фільтрації системних і тимчасових директорій.</li>
            <li><strong>Semantic Extraction (Семантичний парсинг):</strong> Читання файлів як абстрактних синтаксичних дерев (AST) через стандартний модуль Python <code>ast</code>, що гарантує 100% безпечне вилучення коментарів та докстрінгів без виконання самого коду.</li>
            <li><strong>Graph Topology (Логічні зв'язки):</strong> Виявлення внутрішніх імпортів (залежностей) між модулями за допомогою регулярних виразів для побудови карти зв'язків.</li>
            <li><strong>Knowledge Serialization (Серіалізація даних):</strong> Формування двох вихідних файлів знань — <code>atlas_data.json</code> (для динамічних запитів) та <code>atlas_data.js</code> (для автономного відображення графа в браузері).</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Життєвий цикл сканування (Scanning & Parsing Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Діаграма ілюструє процес рекурсивного збору інформації, парсингу AST та формування фінальної бази знань:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск generate_atlas_metadata.py") --> INIT("1. Ініціалізація списків Nodes та Edges")
                INIT --> CRAWL("2. Рекурсивний обхід os.walk(base_dir)")
                
                CRAWL --> FILTER{"3. Чи входить шлях в exclude_dirs?"}
                FILTER -- "Так" --> SKIP("3a. Пропустити директорію")
                FILTER -- "Ні" --> REG_DIR("3b. Реєстрація папки як Node(folder)")
                
                REG_DIR --> SCAN_FILE("4. Перебір файлів у папці")
                SCAN_FILE -- "Ні-Python (.csv, .db, .parquet)" --> STAT_DESC("5a. Генерація статичного опису")
                SCAN_FILE -- "Python (.py)" --> AST_PARSE("5b. ast.parse(): Читання докстрінга")
                
                AST_PARSE --> CLEAN_DESC("6. Регулярні вирази: Видалення ліній === та ---")
                STAT_DESC & CLEAN_DESC --> DET_LINK{"7. Чи є паспорт у docs/system/map/ або тег # ATLAS_PASSPORT?"}
                
                DET_LINK -- "Так" --> SET_LINK("8a. Прив'язка відносного посилання")
                DET_LINK -- "Ні" --> SET_NULL("8b. Link = None")
                
                SET_LINK & SET_NULL --> IMP_SCAN("9. Пошук локальних імпортів (src, scripts, tests)")
                IMP_SCAN --> ADD_EDGE("10. Додавання зв'язків у Edges")
                
                ADD_EDGE --> WRITE_JSON("11. Запис docs/javascripts/atlas_data.json")
                WRITE_JSON --> WRITE_JS("12. Запис docs/system/atlas_data.js (const ATLAS_DATA)")
                WRITE_JS --> END("Успішне завершення роботи")
                SKIP --> CRAWL
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичне представлення графа та парсинг AST</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Топологічна модель графа репозиторію</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Репозиторій представляється як орієнтований мультиграф $G = (V, E)$, де множина вершин $V = V_{\text{folder}} \cup V_{\text{file}}$ містить папки та файли як окремі вузли, а ребра $E = E_{\text{hierarchy}} \cup E_{\text{import}}$ відображають ієрархічну вкладеність та логічний імпорт коду:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ e = (u, v) \in E_{\text{import}} \quad \iff \quad u \text{ містить інструкцію import } v $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Семантична фільтрація докстрінгів</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для уникнення розривів слів та забезпечення бездоганного відображення в інтерпутаторі HTML, скрипт застосовує заміну звичайних пробілів перед дужками на нерозривні пробіли (Non-Breaking Space, <code>\u00A0</code>) та впроваджує символ об'єднання слів (Word Joiner, <code>\u2060</code>) після відкриття дужки:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ T(s) = \text{replace}(s, \text{" ("}, \text{"\u00A0(\u2060"}) $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Парсинг AST дерев (Python Syntax Tree)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Замість використання нестабільних регулярних виразів для пошуку коментарів, скрипт парсить вихідний код у вузли AST. Верхній докстрінг витягується безпосередньо з першого вузла модуля <code>ast.Module</code>:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{docstring}(M) = \text{ast.get\_docstring}(T_{\text{parsed}}) $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод семантичного парсера AST</h2>
    </div>
    <div class="glass-card">
        <p>
            Алгоритм безпечного вилучення першого докстрінга з Python файлу за допомогою AST-дерева:
        </p>
        <pre><code class="language-python">
# Псевдокод безпечного парсингу докстрінгів
import ast
import re

def extract_clean_docstring(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Парсимо файл у дерево без його виконання
            syntax_tree = ast.parse(f.read())
            doc = ast.get_docstring(syntax_tree)
            
            if doc:
                # Очищаємо від зайвих переносів рядків
                lines = [line.strip() for line in doc.strip().split("\n") if line.strip()]
                cleaned = "\n".join(lines)
                
                # Прибираємо декоративні розділювачі (===, ---)
                cleaned = re.sub(r'[-=]{3,}', '', cleaned)
                
                # Запобігаємо розриву дужок при переносі тексту
                cleaned = cleaned.replace(" (", "\u00A0(\u2060")
                return cleaned.strip()
    except Exception:
        pass
    return "Технічний модуль системи."
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому для вилучення описів використовується модуль `ast`, а не динамічний `import` та `__doc__`?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Динамічний імпорт модулів (через `importlib`) вимагає виконання файлу на етапі ініціалізації. Це може призвести до запуску небажаних фонових процесів, ініціалізації GUI-інтерфейсів або помилок підключення до БД. Статичний аналіз через AST (Abstract Syntax Tree) читає файл як звичайний структурований текст, гарантуючи 100% безпеку та швидкість роботи.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Які папки автоматично ігноруються під час сканування?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Скрипт містить жорсткий фільтр `exclude_dirs`, який ігнорує збірки сайту документації (`site`), кеші (`__pycache__`, `.pytest_cache`, `.streamlit`), віртуальні середовища (`venv`, `.venv`, `env`), внутрішні папки IDE (`.gemini`), результати експериментів (`results`), логи (`logs`) та тимчасові скрипти (`scratch`).
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як з'являється посилання на детальний паспорт модуля?</h4>
        <p style="color: var(--text-dim);">
            A: Скрипт спочатку шукає спеціальний маркерний коментар у самому коді файлу: `# ATLAS_PASSPORT: docs/system/map/<name>.md`. Якщо маркер відсутній, скрипт робить перевірку в папці `docs/system/map/` на наявність однойменного `.md` файлу. Якщо такий файл знайдено — створюється інтерактивний зв'язок для 3D-графа.
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
