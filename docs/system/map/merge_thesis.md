# Технічний Паспорт Компонента: scripts/thesis/merge_thesis.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🧬 ACADEMIC DOCUMENT MERGER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔗</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">merge_thesis.py</h1>
            <p class="mega-subtitle">Утиліта адитивної конкатенації, злиття структурованих розділів дисертації та автоматичного впровадження розривів сторінок Pandoc</p>
            <div class="status-tags">
                <span class="tag tag-online">ASSEMBLER</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">TEXT CONSOLIDATOR</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📑</div>
        <div class="metric-info">
            <span class="metric-label">Input Files</span>
            <span class="metric-value">10 Core Chapters</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">💾</div>
        <div class="metric-info">
            <span class="metric-label">Encoding</span>
            <span class="metric-value">UTF-8 strict</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-info">
            <span class="metric-label">Output File</span>
            <span class="metric-value">THESIS_FULL_FINAL_UTF8.md</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🩹</div>
        <div class="metric-info">
            <span class="metric-label">Format Break</span>
            <span class="metric-value">&lt;pagebreak&gt; injection</span>
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
            Модуль <code>scripts/thesis/merge_thesis.py</code> є <strong>головним асемблером (складальником тексту)</strong> дипломної роботи платформи <i>Energy Monitor Ultimate</i>. Він вирішує важливе структурне завдання: послідовно об'єднує окремі Markdown-файли розділів у єдиний монолітний документ. Це дозволяє підтримувати розробку розділів ізольовано, не створюючи гігантських нечитабельних файлів, та автоматично генерувати фінальну версію для транслятора Pandoc.
        </p>
        <p style="margin-top: 10px;">
            Ключові обов'язки складальника тексту:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Секвенційне злиття (Sequential Merging):</strong> Строго регламентований порядок злиття 10 файлів — починаючи від титульного листа <code>OFFICIAL_TITLE_PAGE.md</code>, анотації, вступу, трьох основних розділів теорії та архітектури, і закінчуючи висновками, бібліографією та додатками.</li>
            <li><strong>Розмітка сторінок (Page Break Management):</strong> Автоматичне вставлення спеціального маркерного коментаря <code>&lt;pagebreak&gt;</code> перед початком кожного нового розділу (крім першого) для забезпечення роздільності глав при генерації у формат Word.</li>
            <li><strong>Збереження кодування:</strong> strict UTF-8 збірка для запобігання втрати специфічних символів українського алфавіту (букви <i>ґ, є, і, ї</i>) та математичних знаків.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Життєвий цикл збирання тексту (Document Assembly Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Наступна схема демонструє процес послідовного зчитування, модифікації структури та збереження результату:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск merge_thesis.py") --> INIT_LIST("1. Завантаження масиву FILES_TO_MERGE (10 файлів)")
                INIT_LIST --> OPEN_OUT("2. Відкриття вихідного файлу на запис (UTF-8)")
                
                OPEN_OUT --> LOOP_START("3. Цикл по файлах зі списку")
                LOOP_START --> CHK_EXIST{"4. Чи існує файл на диску?"}
                
                CHK_EXIST -- "Ні" --> PRINT_WARN("4a. Вивід попередження в консоль & Пропуск")
                CHK_EXIST -- "Так" --> READ_IN("4b. Читання вмісту вхідного файлу")
                
                READ_IN --> CHK_FIRST{"5. Чи є файл першим у списку (Title Page)?"}
                CHK_FIRST -- "Так" --> WRITE_BODY("6a. Запис тіла документа")
                CHK_FIRST -- "Ні" --> WRITE_BREAK("6b. Запис маркерного розриву &lt;pagebreak&gt; у потік")
                
                WRITE_BREAK --> WRITE_BODY
                WRITE_BODY --> WRITE_SPACE("7. Запис додаткових відступів \n\n")
                
                WRITE_SPACE --> LOOP_NEXT("8. Перехід до наступного файлу")
                PRINT_WARN --> LOOP_NEXT
                
                LOOP_NEXT -- "Є ще файли" --> LOOP_START
                LOOP_NEXT -- "Всі файли оброблено" --> CLOSE_OUT("9. Закриття вихідного потоку")
                
                CLOSE_OUT --> END("Успішне завершення збірки моноліту")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичне представлення адитивної збірки</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Рівняння адитивної конкатенації з розривами сторінок</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Нехай $C_i$ — текстовий вміст $i$-го файлу з масиву розділів, а $B$ — рядок маркерного розриву сторінки <code>\n&lt;pagebreak&gt;\n</code>. Фінальний згенерований монолітний документ $M_{\text{merged}}$ описується як послідовне зшивання рядків:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ M_{\text{merged}} = C_1 \oplus \bigoplus_{i=2}^{N} \left( B \oplus C_i \oplus \text{"} \backslash \text{n} \backslash \text{n"} \right) $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Логіка вприску розривів (Pagebreak conditional injection)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Розрив сторінки вставляється виключно за умови, що індекс поточного оброблюваного файлу $i$ задовольняє нерівність:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{InjectPB}(i) = \begin{cases} 
                      \text{True}, & i > 0 \\
                      \text{False}, & i = 0
                   \end{cases} $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Це гарантує відсутність порожнього білого листа на самому початку згенерованого документа.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму злиття тексту</h2>
    </div>
    <div class="glass-card">
        <p>
            Повний алгоритм конкатенації та санітації переносів рядків:
        </p>
        <pre><code class="language-python">
# Псевдокод адитивної збірки диплома
def assemble_thesis_documents():
    output_path = "docs/thesis/THESIS_FULL_FINAL_UTF8.md"
    base_folder = "docs/thesis"
    
    files_sequence = [
        "OFFICIAL_TITLE_PAGE.md",
        "THESIS_0_ABSTRACT.md",
        "ABBREVIATIONS.md",
        "THESIS_0_INTRODUCTION.md",
        "THESIS_1_THEORY.md",
        "THESIS_2_REQUIREMENTS.md",
        "THESIS_3_DESIGN_AND_IMPLEMENTATION.md",
        "THESIS_FINAL_CONCLUSIONS.md",
        "BIBLIOGRAPHY.md",
        "THESIS_APPENDICES.md"
    ]
    
    # Відкриваємо вихідний потік
    with open(output_path, "w", encoding="utf-8") as out_file:
        for index, file_name in enumerate(files_sequence):
            full_path = os.path.join(base_folder, file_name)
            
            if not os.path.exists(full_path):
                log_warning(f"File not found: {file_name}")
                continue
                
            # Читаємо розділ
            with open(full_path, "r", encoding="utf-8") as in_file:
                content = in_file.read()
                
                # Вприскуємо розрив сторінки між розділами
                if index > 0:
                    out_file.write("\n<pagebreak>\n")
                    
                out_file.write(content)
                out_file.write("\n\n") # Додаткова гігієнічна лінія
                
    log_success("Consolidated thesis ready.")
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Навіщо потрібен маркер `<pagebreak>`? Як його розуміє Pandoc чи Word?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Маркер `<pagebreak>` є кастомним прапорцем для нашої системи конвертації. Під час подальшого пробігу двигуна рендерингу (на базі Pandoc), цей тег розпізнається та замінюється на низькорівневий XML-код розриву сторінки OpenXML (а саме `<w:p><w:r><w:br w:type="page"/></w:r></w:p>`), який змушує MS Word перенести наступний текст на нову сторінку.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому порядок злиття файлів є таким жорстким?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Порядок файлів у списку `FILES_TO_MERGE` строго регламентується методичними вказівками кафедри та вимогами ДСТУ до структури випускних робіт. Порушення черговості (наприклад, розміщення списку скорочень перед анотацією чи додатків перед висновками) є грубою помилкою нормоконтролю та призведе до недопуску роботи до захисту.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Чому використовується кодування UTF-8 без BOM?</h4>
        <p style="color: var(--text-dim);">
            A: Стандарт UTF-8 без позначки порядку байтів (BOM) є загальноприйнятим для Unix-систем та веб-інструментів. Додавання BOM-маркера (трьох байтів `EF BB BF` на початку файлу) може викликати некоректну роботу консольних утиліт Pandoc, відображаючи зайві невидимі або "биті" символи (так звані кракозябри) на початку першої сторінки генерованого Word-документа.
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
