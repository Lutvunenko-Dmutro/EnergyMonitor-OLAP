# Технічна специфікація модуля: atlas_steward.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AUTOMATION ENGINE & UTILITY NODE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Служба автоматизації: atlas_steward</h1>
            <p class="mega-subtitle">Автоматизований інструмент очищення, консолідації та актуалізації метаданих технічних паспортів в екосистемі ATLAS</p>
            <div class="status-tags"><span class="tag tag-online">STEWARD ACTIVE</span><span class="tag tag-version">v5.0.0</span><span class="tag tag-role">UTILITY ORCHESTRATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Runtime</span><span class="metric-value">Python 3.11+</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Execution</span><span class="metric-value">Automated Clean</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧬</div><div class="metric-info"><span class="metric-label">Priority</span><span class="metric-value">High Performance</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Interface</span><span class="metric-value">CLI / Auto-Run</span></div></div>
</div>

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Модуля Автоматизації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>atlas_steward.py</code> є "Двірником" та "Санітаром" проєкту ATLAS. У великих програмних комплексах із сотнями файлів ручна підтримка актуальності зв'язків між вихідним кодом Python та файлами документації (паспортами) є вкрай неефективною. Наша філософія базується на <b>Консистентності та Консолідації</b>: утиліта автоматично сканує директорію <code>src/</code>, знаходить технічні теги <code># ATLAS_PASSPORT</code>, об'єднує застарілі індивідуальні паспорти у великі централізовані хаби (Consolidated Hubs) та генерує фінальний індекс <code>atlas_metadata.json</code>.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL / LOGIC REGEX MODELS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Логіко-математична модель консолідації</h2></div>
    <div class="glass-card flow-step">
        <p>Служба автоматизації оперує регулярними виразами та дискретним мапуванням:</p>
        
        <h4>1. Оператор екстракції тегів ($T$)</h4>
        <p>Для кожного рядка коду $l$ функція шукає наявність спеціального коментаря за допомогою регулярного виразу $\mathbf{P}_{\text{tag}}$:</p>
        $$T(l) = \text{RegexSearch}(l, \mathbf{P}_{\text{tag}}) \implies \text{PassportName}$$
        <p>де $\mathbf{P}_{\text{tag}} = \text{"# ATLAS_PASSPORT: docs/system/map/(.+?\\.md)"}$.</p>

        <h4>2. Функція консолідаційного мапування ($M$)</h4>
        <p>Отримане ім'я паспорта перевіряється за словником консолідації $\mathbf{Map}$ для об'єднання у центральні технічні хаби:</p>
        $$M(p) = \begin{cases} 
           \mathbf{Map}(p), & \text{якщо } p \in \text{Domain}(\mathbf{Map}) \\ 
           p, & \text{в іншому випадку} 
        \end{cases}$$
        <p>Наприклад, <code>predict_v2.md</code> автоматично перенаправляється на великий хаб <code>ml_core_engine.md</code>, а duplicate-теги видаляються з файлу.</p>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Життєвий цикл виконання (Architecture Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("Launch atlas_steward.py") --> INIT("Read consolidation mapping dictionary")
    INIT --> SCAN("Traverse src/ via self.src_dir.rglob('*.py')")
    
    SCAN --> FILE_READ("Read file lines (UTF-8)")
    FILE_READ --> LINE_LOOP("Check each line via Regex TAG_PATTERN")
    
    LINE_LOOP -- "Tag Found & in Map" --> REPLACE("Replace name with consolidated Hub name")
    LINE_LOOP -- "Tag is Redundant Duplicate" --> DELETE("Remove line (Deduplication)")
    LINE_LOOP -- "Clean Line" --> KEEP("Keep Line intact")
    
    REPLACE --> WRITE("Write file back to disk (modified=True)")
    DELETE --> WRITE
    KEEP --> WRITE
    
    WRITE --> SUMMARY("Print Audit Stats (Scanned / Fixed / Duplicates)")
    SUMMARY --> JSON_GEN("regenerate_metadata() index call")
    JSON_GEN --> EXIT("Save docs/system/map/atlas_metadata.json & Exit")
    </div></div>
</div>

<!-- SECTION 04: API & AST REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Інтерфейси та сигнатури класу AtlasSteward</h2></div>
    <div class="glass-card flow-step">
        <p>Структура об'єктної моделі автоматизації, побудована відповідно до принципів OOP:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Член класу</th>
                    <th>Сигнатура API</th>
                    <th>Тип</th>
                    <th>Опис виконуваної задачі</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>__init__</code></td><td><code>def __init__(self, root_dir: str = ".")</code></td><td>Конструктор</td><td>Ініціалізація відносних шляхів до папок <code>src/</code> та <code>docs/system/map/</code></td></tr>
                <tr><td><code>run_cleanup</code></td><td><code>def run_cleanup(self)</code></td><td>Публічний метод</td><td>Запуск циклу рекурсивного сканування файлів, виведення аудиторської статистики</td></tr>
                <tr><td><code>regenerate_metadata</code></td><td><code>def regenerate_metadata(self)</code></td><td>Внутрішній метод</td><td>Створення та запис індексного файлу <code>atlas_metadata.json</code> із сортованим списком паспортів</td></tr>
                <tr><td><code>_process_file</code></td><td><code>def _process_file(self, file_path: Path, stats: dict)</code></td><td>Приватний метод</td><td>Читання, парсинг регулярними виразами, консолідація тегів та видалення дублікатів у файлі</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Псевдокод Автоматизатора (Steward Core Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>CLASS AtlasSteward:
    FUNCTION __init__(root_dir):
        self.root = Path(root_dir)
        self.src_dir = root / "src"
        self.docs_dir = root / "docs" / "system" / "map"
        
    FUNCTION run_cleanup():
        stats = {"fixed": 0, "duplicates_removed": 0, "total_files": 0}
        FOR py_file IN rglob(self.src_dir, "*.py"):
            stats["total_files"] += 1
            self._process_file(py_file, stats)
        self.regenerate_metadata()
        
    FUNCTION _process_file(file_path, stats):
        content = read_text(file_path, encoding="utf-8")
        lines = content.splitlines()
        new_lines = []
        found_tags = []
        modified = False
        
        FOR line IN lines:
            match = regex_search(TAG_PATTERN, line)
            IF match:
                passport_name = match.group(1)
                IF passport_name IN HUB_CONSOLIDATION_MAP:
                    new_passport = HUB_CONSOLIDATION_MAP[passport_name]
                    line = line.replace(passport_name, new_passport)
                    passport_name = new_passport
                    modified = True
                    stats["fixed"] += 1
                    
                IF passport_name IN found_tags:
                    modified = True
                    stats["duplicates_removed"] += 1
                    continue // Deduplicate (skip adding line)
                found_tags.append(passport_name)
            new_lines.append(line)
            
        IF modified:
            write_text(file_path, join(new_lines), encoding="utf-8")
            
    FUNCTION regenerate_metadata():
        md_files = list_files_in_dir(self.docs_dir, "*.md")
        metadata = {
            "project": "Project ATLAS",
            "total_passports": len(md_files),
            "last_sync": current_iso_time(),
            "passports": [{"name": f, "path": f"system/map/{f}"} for f in md_files]
        }
        write_json(self.docs_dir / "atlas_metadata.json", metadata)
END CLASS</code></pre>
    </div>
</div>

<!-- SECTION 06: DEDUPLICATION & CONSOLIDATION RULES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Правила консолідації та дедуплікації</h2></div>
    <div class="glass-card flow-step">
        <p>Мапування <code>HUB_CONSOLIDATION_MAP</code> визначає правила злиття файлів:</p>
        <ul>
            <li><b>ML Core Engine Hub:</b> Злиття 7 застарілих технічних паспортів (<code>predict_v2.md</code>, <code>train_lstm.md</code>, <code>vectorizer.md</code> тощо) в один великий суцільний опис ядра ШІ.</li>
            <li><b>Core Kernel Hub:</b> Об'єднання конфігурацій (<code>core_config.md</code>, <code>queries.md</code>) та завантажувача Kaggle в єдиний архітектурний опис ядра.</li>
            <li><b>Deduplication:</b> Якщо розробник випадково додав кілька однакових тегів <code># ATLAS_PASSPORT</code> у різні місця одного файлу, стюард автоматично видалить дублікати, залишаючи лише один перший тег для чистоти метаданих.</li>
        </ul>
    </div>
</div>

<!-- SECTION 07: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📂</div>
            <div class="role-content">
                <h4>Python Standard Library</h4>
                <p>Використання модулів <code>pathlib.Path</code> для кросплатформеної навігації шляхами, <code>re</code> для регулярних виразів та <code>json</code>.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Source Tree (*.py)</h4>
                <p>Об'єкт сканування: весь вихідний код проєкту в папці <code>src/</code>.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📖</div>
            <div class="role-content">
                <h4>Passports Directory (*.md)</h4>
                <p>Індексний каталог: генерація та аудит технічних файлів у <code>docs/system/map/</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 08: ROADMAP TO v3.0 (COMPILER INTEGRATION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Дорожня карта v3.0 (Pre-commit Git Integration)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 заплановано:</p>
        <ul>
            <li><b>Pre-commit Hook:</b> Автоматичний запуск стюарда при спробі зробити <code>git commit</code> для запобігання надсиланню неконсистентних тегів у репозиторій.</li>
            <li><b>Missing Passport Generator:</b> Автоматична генерація базового каркаса (Boilerplate) паспорта, якщо в коді знайдено новий тег, для якого ще немає файлу .md.</li>
            <li><b>HTML Interactive Graphs:</b> Генерація інтерактивного 3D-графу зв'язків між класами безпосередньо у звіті стюарда.</li>
        </ul>
    </div>
</div>

<!-- SECTION 09: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">FAQ: Технічні відповіді</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Як запустити стюарда вручну?</b><br>
        A: Запустіть скрипт безпосередньо з кореневої директорії проєкту:
        <code>python src/utils/atlas_steward.py</code>. Він самостійно виявить межі проєкту та проведе повне очищення.</p>
        <p><b>Q: Що станеться, якщо я перейменую файл паспорта в docs?</b><br>
        A: Якщо ви перейменували файл .md, вам необхідно оновити теги в коді Python та мапування <code>HUB_CONSOLIDATION_MAP</code> у файлі <code>atlas_steward.py</code>. Після запуску стюард автоматично виправить решту посилань та оновіть файл метаданих.</p>
        <p><b>Q: Чому використовується саме pathlib, а не os.path?</b><br>
        A: Об'єкти <code>Path</code> є значно безпечнішими та сучаснішими за прості текстові рядки шляхів. Вони автоматично вирішують проблеми з косими рисками (Slash/Backslash) на Windows (де запущено розробку) та Linux (де збирається MkDocs), запобігаючи технічним збоям шляхів.</p>
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
