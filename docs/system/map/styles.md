# Технічний Паспорт Модуля: scripts/thesis/converter/styles.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🎨 ACADEMIC STYLING & LAYOUT ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">styles.py</h1>
            <p class="mega-subtitle">Двигун академічного стилю та верстки, регулятор параметрів сторінки А4 та генератор нативної нумерації OpenXML за ДСТУ</p>
            <div class="status-tags">
                <span class="tag tag-online">STYLER ACTIVE</span>
                <span class="tag tag-version">v3.1.0</span>
                <span class="tag tag-role">LAYOUT MANAGER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">✒️</div>
        <div class="metric-info">
            <span class="metric-label">Core Font</span>
            <span class="metric-value">Times New Roman 14pt</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">↔️</div>
        <div class="metric-info">
            <span class="metric-label">Line Spacing</span>
            <span class="metric-value">1.5 / 21pt Justified</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📄</div>
        <div class="metric-info">
            <span class="metric-label">Page Format</span>
            <span class="metric-value">Standard A4 (21x29.7cm)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔢</div>
        <div class="metric-info">
            <span class="metric-label">Page Numbers</span>
            <span class="metric-value">Native w:instrText PAGE</span>
        </div>
    </div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення та архітектурна роль</h2></div>
    <div class="glass-card flow-step">
        <p>
            Модуль <code>styles.py</code> виступає центральним стандартизатором оформлення у процесі конвертації дипломних робіт. Він інкапсулює вимоги державних стандартів України (ДСТУ) до наукових праць та реалізує їх у вигляді програмних правил для OpenXML-розмітки текстового процесора MS Word.
        </p>
        <p style="margin-top: 10px;">
            Основний спектр відповідальності модуля включає:
        </p>
        <ul>
            <li><strong>Universal Font Management:</strong> Налаштування Times New Roman як глобального шрифту для основного тексту (14pt) та заголовків, а також використання Courier New (11pt) для лістингів коду.</li>
            <li><strong>Rich Text Parsing:</strong> Парсинг Markdown-розмітки inline-стилів (жирний <code>**</code>, курсив <code>*</code>, підкреслений <code>&lt;u&gt;</code> та виділення кольором <code>==</code>) та їх перетворення на нативні властивості Word Run (об'єкт <code>docx.shared.Pt</code>).</li>
            <li><strong>Standard Formatting:</strong> Забезпечення суворого вирівнювання тексту по ширині (Justified), міжрядкового інтервалу 1.5 та абзацного відступу (першого рядка) рівно 1.25 см.</li>
            <li><strong>Page Geometry & Pagination:</strong> Задання геометрії сторінки А4, конфігурація дзеркальних полів та вставка нативних полів автонумерації сторінок у верхньому чи нижньому правому кутку (з виключенням першої сторінки титульного листа).</li>
        </ul>
    </div>
</div>

<!-- SECTION 02: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математична формалізація стилю за ДСТУ</h2></div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Розрахунок інтервалів та зміщень</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Міжрядковий інтервал за вимогами ДСТУ складає 1.5 від розміру шрифту $H_{\text{font}} = 14$ pt, що в абсолютних одиницях виміру OpenXML дорівнює:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ S_{\text{line}} = 1.5 \times H_{\text{font}} = 21 \text{ pt} $$
                </div>
                <p style="margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);">
                    Абзацний відступ першого рядка (First Line Indent) фіксується на позначці:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ I_{\text{first}} = 1.25 \text{ см} = 0.492 \text{ in} $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Співвідношення геометрії сторінки А4</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Фізичні параметри друкованого аркуша визначаються наступними геометричними константами:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ W_{\text{page}} = 21.0 \text{ см}, \quad H_{\text{page}} = 29.7 \text{ см} $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: INTERACTION PIPELINE (DIAGRAM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Життєвий цикл стилізації тексту</h2></div>
    <div class="glass-card">
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                TEXT_IN("Вхідний текст з Markdown розміткою") --> REG_PARSE("clean_inline(): видалення залишків посилань та коду")
                REG_PARSE --> FORMAT_RUN["add_formatted_run(): парсер inline стилів"]
                
                FORMAT_RUN --> SPLIT{"Регулярний вираз: split(**, *, u, ==)"}
                SPLIT -- "**" --> BOLD_TOGGLE["Перемикання bold = NOT bold"]
                SPLIT -- "*" --> ITALIC_TOGGLE["Перемикання italic = NOT italic"]
                SPLIT -- "<u>" --> UNDER_TRUE["underline = True"]
                SPLIT -- "</u>" --> UNDER_FALSE["underline = False"]
                SPLIT -- "==" --> HIGH_TOGGLE["highlight_color = YELLOW"]
                
                BOLD_TOGGLE & ITALIC_TOGGLE & UNDER_TRUE & UNDER_FALSE & HIGH_TOGGLE --> RUN_GEN["paragraph.add_run(part)"]
                RUN_GEN --> FONT_ENG["set_run_font(): Призначення Times/Courier"]
                FONT_ENG --> PARA_ALIGN["para_std(): вирівнювання по ширині, інтервал 1.5, абзац 1.25см"]
                PARA_ALIGN --> PAGE_NUM["add_page_numbers(): Вставка нативного поля PAGE в колонтитул"]
                PAGE_NUM --> OUT_DOC("Стилізований ДСТУ-документ (.docx)")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 04: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Алгоритм генерації нативної нумерації сторінок</h2></div>
    <div class="glass-card">
        <p>
            Псевдокод демонструє низькорівневу вставку XML-полів MS Word для реалізації динамічної автонумерації сторінок у верхньому/нижньому правому куті:
        </p>
        <pre><code class="language-python">
def add_page_numbers(doc):
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    
    # Перша сторінка (титульна) має окремий колонтитул без номера
    section.different_first_page_header_footer = True
    
    # Отримуємо доступ до нижнього колонтитула для звичайних сторінок
    footer = section.footer
    p = footer.paragraphs[0]
    p.clear()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT # Номер сторінки справа
    
    # Створюємо Word Run для поля інструкцій (PAGE Field)
    run = p.add_run()
    
    # 1. Початок поля (Field Character Begin)
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._r.append(fldChar1)
    
    # 2. Текст інструкції (Instruction Text: PAGE)
    instr = OxmlElement('w:instrText')
    instr.text = 'PAGE'
    run._r.append(instr)
    
    # 3. Завершення поля (Field Character End)
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar2)
    
    # Призначаємо стандартний шрифт для номера сторінки
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
        </code></pre>
    </div>
</div>

<!-- SECTION 05: TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Часті питання (FAQ)</h2></div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому для нумерації сторінок використовується складний XML-код замість звичайного тексту?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Простий текст буде статично однаковим на всіх сторінках (наприклад, всюди виведеться цифра "2"). Використання нативного XML-тега <code>w:instrText</code> з інструкцією <code>PAGE</code> змушує текстовий процесор MS Word динамічно вираховувати номер сторінки в момент відкриття або друку документа на основі реальної геометрії верстки.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому у Word не встановлюється шрифт, хоча `run.font.name` змінено?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Це поширений баг бібліотеки <code>python-docx</code>. Зміна властивості <code>run.font.name</code> не завжди прописує шрифт у низькорівневих властивостях стилю Run. Для 100% надійності функція <code>set_run_font()</code> додатково створює OXML-елемент <code>w:rFonts</code> та явно прописує його атрибути <code>w:ascii</code> та <code>w:cs</code> (Complex Scripts).
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як реалізовано очищення тексту від Markdown-залишків?</h4>
        <p style="color: var(--text-dim);">
            A: Функція <code>clean_inline()</code> використовує каскад регулярних виразів для очищення тексту. Вона видаляє символи `**`, `*`, `\``, а також HTML-теги та посилання `[text](url)`, залишаючи чистий текст, але при цьому зберігає мітки формул типу `$$formula$$` у вигляді унікальних символів-розділювачів `⇲` та `⇱` для їх подальшої обробки математичним двигуном.
        </p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">Повернутися до Атласу</span></a>
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
