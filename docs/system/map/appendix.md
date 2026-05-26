# Технічний Паспорт Компонента: scripts/thesis/converter/appendix.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">📜 TECHNICAL APPENDIX GENERATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📄</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">appendix.py</h1>
            <p class="mega-subtitle">Генератор технічних додатків, автоматизований збирач лістингів коду та інтегратор структурованої верстки за стандартами ДСТУ</p>
            <div class="status-tags">
                <span class="tag tag-online">APPENDIX ENGINE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">CODE CRAWLER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📂</div>
        <div class="metric-info">
            <span class="metric-label">Scanning Scope</span>
            <span class="metric-value">src/ Root Crawler</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📑</div>
        <div class="metric-info">
            <span class="metric-label">File Whitelist</span>
            <span class="metric-value">Opt-in (config.py)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-info">
            <span class="metric-label">Formatting Handlers</span>
            <span class="metric-value">add_h1 / add_h2 / add_code</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Encoding</span>
            <span class="metric-value">UTF-8 strict read</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль та академічні вимоги</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/thesis/converter/appendix.py</code> виконує роль <strong>автоматизованого компілятора технічних додатків (Source Code Appendix Generator)</strong> платформи <i>Energy Monitor Ultimate</i>. Згідно з академічними вимогами до дипломних робіт інженерних спеціальностей, пояснювальна записка обов'язково повинна містити повний лістинг розробленого програмного забезпечення (Додаток Л). Даний модуль автоматизує цей рутинний процес, збираючи вихідний код з репозиторію та оформлюючи його у вигляді структурованих моноширинних блоків безпосередньо у вихідному Word-файлі.
        </p>
        <p style="margin-top: 10px;">
            Основний функціонал генератора додатків:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Recursive Harvesting (Рекурсивне збирання):</strong> Автоматичний обхід файлової системи директорії <code>src/</code> за допомогою <code>os.walk</code> з ігноруванням службових папок (наприклад, <code>__pycache__</code>).</li>
            <li><strong>Реєстр білого списку (Whitelist Filtering):</strong> Імпорт списку файлів з <code>config.py</code>. Конвертуються виключно схвалені модулі ядра (наприклад, <code>predict_v2.py</code>, <code>physics.py</code>), що дозволяє чітко керувати підсумковим обсягом сторінок.</li>
            <li><strong>Path Normalization (Нормалізація шляхів):</strong> Формування відносних шляхів до файлів відносно кореневої робочої директорії для виведення в заголовках додатків (наприклад, <i>"Файл: src/ml/predict_v2.py"</i>).</li>
            <li><strong>Структурований запис:</strong> Виклик спеціалізованих методів `add_h1`, `add_h2` та `add_code` для правильного відображення коду з дрібним моноширинним шрифтом (8pt) та сірою рамкою.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр генерації додатків (Appendix Construction Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Діаграма демонструє послідовність кроків рекурсивного сканування та запису вихідного коду у Word-документ:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск add_source_code_appendix(doc, src_dir)") --> CHK_DIR{"1. Чи існує src_dir?"}
                
                CHK_DIR -- "Ні" --> END("Швидкий вихід")
                CHK_DIR -- "Так" --> WRITE_H1("2. add_h1: Запис заголовка ДОДАТОК Л")
                
                WRITE_H1 --> CRAWL_DIR("3. os.walk(src_dir)")
                CRAWL_DIR --> FILT_CACHE("4. Ігнорування __pycache__ сегментів")
                
                FILT_CACHE --> LOOP_FILES("5. Цикл по виявлених файлах")
                LOOP_FILES --> CHK_WHITE{"6. Чи є файл у WHITELIST_FILES?"}
                
                CHK_WHITE -- "Ні" --> SKIP_FILE("6a. Пропуск файлу")
                CHK_WHITE -- "Так" --> CALC_REL("6b. os.path.relpath(): Розрахунок відносного шляху")
                
                CALC_REL --> WRITE_H2("7. add_h2: Запис назви файлу у документ")
                WRITE_H2 --> READ_CODE("8. Читання коду: open(file, encoding='utf-8')")
                
                READ_CODE -- "Помилка читання" --> WARN_ERR("8a. Вивід WARN в консоль")
                READ_CODE -- "Успішно" --> SPLIT_LINES("8b. Розбиття коду на рядки (.splitlines)")
                
                SPLIT_LINES --> WRITE_CODE("9. add_code: Вставка коду дрібним моноширинним шрифтом")
                WRITE_CODE & WARN_ERR & SKIP_FILE --> LOOP_NEXT("10. Перехід до наступного файлу")
                
                LOOP_NEXT -- "Є ще файли" --> LOOP_FILES
                LOOP_NEXT -- "Обхід завершено" --> END
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математика нормалізації шляхів та ліміти обсягу</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Розрахунок релятивного шляху (Relative Path mapping)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для виведення гарного заголовка файлу, абсолютний шлях до файлу $P_{\text{abs}}$ перетворюється на релятивний шлях $P_{\text{rel}}$ відносно поточної робочої директорії $W$ шляхом відсікання спільного префікса:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ P_{\text{rel}} = \text{os.path.relpath}(P_{\text{abs}}, W) = P_{\text{abs}} \setminus \text{CommonPrefix}(P_{\text{abs}}, W) $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Управління лімітом сторінок додатків</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Оскільки лістинг великих Python-файлів може займати сотні сторінок, а загальний обсяг додатків регламентується ВАК/ДСТУ (не більше 20-30% від основного обсягу записки), кількість сторінок додатків контролюється через кардинальне число білого списку $N_{\text{whitelist}}$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ |F_{\text{included}}| \le N_{\text{whitelist}} \quad (\text{де } N_{\text{whitelist}} = 9) $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму збору лістингів</h2>
    </div>
    <div class="glass-card">
        <p>
            Рекурсивний обхід та запис коду з контролем кодування:
        </p>
        <pre><code class="language-python">
# Псевдокод генератора додатків коду
import os

def generate_source_appendix(word_document, source_folder, approved_list):
    if not os.path.exists(source_folder):
        return
        
    # Записуємо головний заголовок додатку
    add_heading_h1(word_document, "ДОДАТОК Л. ПОВНИЙ ЛІСТИНГ КЛЮЧОВИХ МОДУЛІВ ПРОЄКТУ")
    
    for root, subfolders, files in os.walk(source_folder):
        # Ігноруємо системні папки кешу
        if "__pycache__" in subfolders:
            subfolders.remove("__pycache__")
            
        for file in files:
            if file in approved_list:
                # Отримуємо красивий шлях
                absolute_path = os.path.join(root, file)
                relative_path = os.path.relpath(absolute_path, os.getcwd())
                
                # Записуємо заголовок файлу
                add_heading_h2(word_document, f"Файл: {relative_path}")
                
                try:
                    with open(absolute_path, 'r', encoding='utf-8') as code_file:
                        lines = code_file.read().splitlines()
                        # Записуємо рядки коду
                        add_code_block_to_doc(word_document, lines)
                except Exception as error:
                    print(f"Error reading file {file}: {error}")
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому не можна просто скопіювати весь вихідний код у додатки?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Повний об'єм кодової бази проєкту Energy Monitor Ultimate перевищує 15 000 рядків. Якщо включити весь код без розбору, додаток роздується до 300+ сторінок, що зробить дипломну роботу перевантаженою та викличе зауваження нормоконтролю. Білий список `WHITELIST_FILES` спеціально відбирає лише 9 найважливіших файлів ядра (фізичні моделі, ШІ-пайплайни, аналітичні в'ю), щоб загальний обсяг диплома з додатками становив оптимальні 80-90 сторінок.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому `os.walk` модифікує список `dirs` на місці (`dirs.remove("__pycache__")`)?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Це стандартна та найбільш ефективна практика оптимізації `os.walk` у Python. Якщо видалити назву папки зі списку `dirs` безпосередньо під час ітерації, генератор `os.walk` <u>не буде</u> спускатися в цю папку рекурсивно. Це значно прискорює сканування та запобігає витраті ресурсів на читання тисяч тимчасових `.pyc` файлів кешу.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Які стилі застосовуються до тексту коду в Word?</h4>
        <p style="color: var(--text-dim);">
            A: До коду застосовується кастомний хендлер `add_code`. Він використовує моноширинний шрифт Consolas або Courier New, зменшує розмір тексту до 8.5pt (щоб довгі інженерні рядки не переносилися на наступний рядок візуально), встановлює мінімальний міжрядковий інтервал (1.0) та додає тонкі рамки з лівого боку для красивого Cyber-HUD вигляду лістингу.
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
