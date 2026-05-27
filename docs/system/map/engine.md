# Технічний Паспорт Компонента: scripts/thesis/converter/engine.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">⚙️ THESIS DOCUMENT LAYOUT ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">engine.py</h1>
            <p class="mega-subtitle">Ядро трансляції та верстки, інтелектуальний Markdown-парсер та двигун динамічної генерації нативного Змісту MS Word</p>
            <div class="status-tags">
                <span class="tag tag-online">LAYOUT ENGINE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">TRANSCRIPTION CORE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📑</div>
        <div class="metric-info">
            <span class="metric-label">Parser Strategy</span>
            <span class="metric-value">Intelligent Line Scan</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">Standards Applied</span>
            <span class="metric-value">DSTU Paragraph Styles</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Dynamic Elements</span>
            <span class="metric-value">Native TOC (fldChar)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🗃️</div>
        <div class="metric-info">
            <span class="metric-label">Post-Processing</span>
            <span class="metric-value">WinWord Single Pass</span>
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
            Модуль <code>scripts/thesis/converter/engine.py</code> є **трансляційним серцем (Layout Engine)** системи підготовки документації платформи <i>Energy Monitor Ultimate</i>. Він реалізує складну логіку перетворення плоского Markdown-файлу у професійно оформлений текстовий документ Microsoft Word (`.docx`). Двигун забезпечує не просто конвертацію тексту, а глибоку структурну трансформацію: створює стилі абзаців, налаштовує поля сторінок за ДСТУ, генерує нативний автоматично оновлюваний Зміст Word та динамічно обробляє наукові формули і таблиці.
        </p>
        <p style="margin-top: 10px;">
            Основний функціонал трансляційного двигуна:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Intelligent Markdown Parsing (Розумний парсинг):</strong> Порядковий скан вхідного файлу з розпізнаванням ієрархії заголовків (`#` до `####`), нумерованих та маркованих списків, посилань на зображення та таблиць.</li>
            <li><strong>Enforcement of DSTU styles (Санітація стилів):</strong> Створення глобальних стилів `Normal` (Times New Roman 14pt, інтервал 1.5, widow_control=True) та `Heading 1` з жорсткими налаштуваннями відступів та вирівнювання.</li>
            <li><strong>Dynamic TOC Generation (Генерація Змісту):</strong> Автоматичне вбудовування нативних полів Word (`TOC \o "1-3" \h \z \u`) безпосередньо в об'єктний XML-код документа перед розділом скорочень.</li>
            <li><strong>Mermaid & Navigation Sanitization (Фільтрація сміття):</strong> Очищення вихідного тексту від веб-навігації (посилання назад/вперед) та приховування Mermaid-блоків, призначених виключно для Git-версії.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Життєвий цикл конвертації (Conversion Engine Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Наступна схема демонструє фази роботи двигуна від первинного аналізу рядків до фіналізації Word-документа:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск run_conversion(input_md, output_docx)") --> READ_MD("1. Читання вхідного Markdown (UTF-8)")
                READ_MD --> CREATE_DOC("2. doc = Document() & Налаштування Margins за ДСТУ")
                
                CREATE_DOC --> CREATE_STYLES("3. Створення стилів Normal (14pt, 1.5) & Heading 1 (16pt bold)")
                CREATE_STYLES --> LOOP_LINES("4. Цикл по рядках Markdown файлу")
                
                LOOP_LINES --> FILTER_WEB("5. Фільтрація: Видалення навігаційних лінків & Mermaid схем")
                FILTER_WEB --> PARSE_STRUCT{"6. Визначення типу рядка за маркером"}
                
                PARSE_STRUCT -- "Код (code)" --> PROC_CODE("7a. add_code(): Збір лістингу вConsolas")
                PARSE_STRUCT -- "$$ (формули)" --> PROC_MATH("7b. add_formula(): Розмітка математичних маркерів ⇲")
                PARSE_STRUCT -- "| (таблиця)" --> PROC_TABLE("7c. add_table(): Парсинг сітки таблиці")
                PARSE_STRUCT -- "# (заголовок)" --> PROC_HEAD("7d. add_h1-h4(): Запис ієрархії розділів")
                PARSE_STRUCT -- "Текст" --> PROC_BODY("7e. add_body(): Запис абзацу за ДСТУ")
                
                PROC_HEAD --> CHK_TOC{"8. Чи є заголовок Скороченнями?"}
                CHK_TOC -- "Так" --> INSERT_TOC("8a. Вставка XML-поля TOC Word (Зміст)")
                CHK_TOC -- "Ні" --> LOOP_LINES
                
                PROC_CODE & PROC_MATH & PROC_TABLE & INSERT_TOC & PROC_BODY --> LOOP_NEXT("9. Перехід до наступного рядка")
                LOOP_NEXT -- "Є рядки" --> LOOP_LINES
                LOOP_NEXT -- "Кінець файлу" --> SAVE_DOC("10. Збереження проміжного docx файлу")
                
                SAVE_DOC --> FINALIZE("11. Виклик finalize_thesis_document(): COM-заміна формул & Зміст")
                FINALIZE --> END("✅ Готовий фінальний документ")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математика інлайнової математики та XML генерація Змісту</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Регулярний вираз виявлення інлайнових формул</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для запобігання втрати LaTeX нотації всередині речень, двигун застосовує регулярний вираз для пошуку інлайнових формул $\dots$ та замінює їх на маркерні дужки `⇲ ... ⇱` для подальшої обробки COM-сервером:
                </p>
                <pre style="margin-bottom: 8px;"><code class="language-python">T_processed = RegExSub(r'\$(.+?)\$', r'⇲\1⇱', T_raw)</code></pre>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. XML представлення поля TOC (Table of Contents)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Оскільки зміст Word є динамічним полем, двигун будує його за допомогою OXML-інструкції (Office XML). Створюється тег `w:instrText` зі спеціальними інструкціями збору рівнів (від 1 до 3), гіперпосилань (`\h`) та приховування номерів на екрані (`\z`):
                </p>
                <pre style="margin-bottom: 8px;"><code class="language-python">instrText = " TOC \o \"1-3\" \h \z \u "</code></pre>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод трансляційного двигуна</h2>
    </div>
    <div class="glass-card">
        <p>
            Спрощений алгоритм порядкового аналізу та генерації стилізованих об'єктів:
        </p>
        <pre><code class="language-python">
# Псевдокод ядра трансляції
import re

def convert_markdown_to_word_layout(input_md_path, output_docx_path):
    raw_lines = read_all_lines(input_md_path)
    document = create_empty_word_document()
    
    # 1. Налаштовуємо стилі ДСТУ
    setup_dstu_page_margins(document.sections[0])
    setup_normal_paragraph_style(document.styles['Normal'])
    
    in_code_block = False
    code_buffer = []
    
    for line in raw_lines:
        stripped = line.strip()
        
        # Ігноруємо веб-елементи (навігаційні стрілки, Mermaid)
        if is_web_navigation(stripped) or stripped.startswith("```mermaid"):
            continue
            
        # Блоки вихідного коду Consolas
        if stripped.startswith("```"):
            if in_code_block:
                add_monospace_code_block(document, code_buffer)
                code_buffer = []
                in_code_block = False
            else:
                in_code_block = True
            continue
            
        if in_code_block:
            code_buffer.append(line)
            continue
            
        # Заголовки першого рівня (Розділи)
        if stripped.startswith("# "):
            title = stripped.replace("# ", "")
            # Якщо це початок Скорочень - вприскуємо зміст
            if "СКОРОЧЕНЬ" in title.upper():
                insert_native_word_toc_field(document)
            add_heading_1_center(document, title)
            
        # Звичайний абзац тексту
        elif stripped:
            # Замінюємо інлайнові формули на маркери для COM-фіналізатора
            processed_text = replace_inline_formulas(stripped)
            add_paragraph_with_indent(document, processed_text)
            
    # Зберігаємо тимчасову версію та запускаємо MS Word для фіналізації
    document.save(output_docx_path)
    run_com_word_polishing(output_docx_path)
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому Зміст (TOC) відображається некоректно або пустим відразу після конвертації?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Зміст у Microsoft Word створюється як спеціальне поле динамічного оновлення (`Field`). Word розраховує його виключно під час відкриття документа на основі фактичного рендерингу сторінок. Для того, щоб Зміст з'явився та заповнився номерами сторінок автоматично, двигун на фінальному етапі викликає COM-метод `TablesOfContents.Update()`. Якщо відкрити документ у сторонньому редакторі (наприклад, LibreOffice або Google Docs), може знадобитися натиснути правою кнопкою миші на Зміст та обрати "Оновити поле".
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому вимкнено властивість `keep_with_next` для звичайних абзаців?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Властивість `keep_with_next` змушує Word тримати поточний абзац на одній сторінці з наступним. Якщо увімкнути її для звичайного тексту, Word намагатиметься перенести весь текст на одну сторінку, що призведе до хаосу в розмітці та гігантських порожніх пробілів внизу сторінок. Для звичайного тексту увімкнено виключно `widow_control=True` (заборона висячих рядків — перенесення одиночного першого чи останнього рядка абзацу на іншу сторінку).
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Що відбувається, якщо підпис рисунка є, а самого малюнка немає?</h4>
        <p style="color: var(--text-dim);">
            A: Двигун містить вбудований запобіжник (`last_was_image` прапорець). Якщо вхідний Markdown містить підпис рисунка (наприклад, `*Рис. 3.4. ER-діаграма*`), але перед ним не було посилання на зображення `![](...)`, двигун автоматично вставить яскраво-червоне попередження `[УВАГА: ВІДСУТНЄ ЗОБРАЖЕННЯ ДЛЯ ЦЬОГО ПІДПИСУ!]` у Word-файл. Це допомагає автору миттєво помітити помилку верстки перед здачею роботи.
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
