# Технічний Паспорт Модуля: scripts/thesis/converter/handlers.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">⚡ MARKDOWN-TO-WORD TRANSFORMATION ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">handlers.py</h1>
            <p class="mega-subtitle">Бібліотека обробників структурних елементів та інтелектуальний транслятор Markdown-компонентів у об'єкти DOCX за стандартами ДСТУ</p>
            <div class="status-tags">
                <span class="tag tag-online">TRANSFORMER ACTIVE</span>
                <span class="tag tag-version">v3.2.0</span>
                <span class="tag tag-role">LAYOUT GENERATOR</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📑</div>
        <div class="metric-info">
            <span class="metric-label">Heading Logic</span>
            <span class="metric-value">H1-H4 Hierarchical Control</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🖼️</div>
        <div class="metric-info">
            <span class="metric-label">Image Scaling</span>
            <span class="metric-value">Proportional (Aspect Ratio)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Tables & Lists</span>
            <span class="metric-value">Borderless & Grid Layouts</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">💻</div>
        <div class="metric-info">
            <span class="metric-label">Code Syntax</span>
            <span class="metric-value">Multi-token Highlight</span>
        </div>
    </div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення та архітектурна роль</h2></div>
    <div class="glass-card flow-step">
        <p>
            Модуль <code>handlers.py</code> є виконавчим механізмом низькорівневої трансляції текстової розмітки Markdown у об'єктно-орієнтовану структуру документа Microsoft Word (формат <code>.docx</code>). Він забезпечує точне дотримання суворих вимог ДСТУ до оформлення пояснювальних записок академічних робіт, автоматично керуючи відступами, шрифтами, інтервалами, а також візуальними табличними сітками та кодовими лістингами.
        </p>
        <p style="margin-top: 10px;">
            Основний спектр відповідальності модуля включає:
        </p>
        <ul>
            <li><strong>Dynamic Heading Processing:</strong> Контроль ієрархії заголовків (від H1 до H4) з інтелектуальним фільтруванням службової інформації для виключення її потрапляння до автоматичного Змісту (TOC).</li>
            <li><strong>Smart Image Scaling:</strong> Пропорційне масштабування растрових зображень з урахуванням орієнтації сторінки (книжкова, квадратна, альбомна) та підтримка кастомних параметрів ширини.</li>
            <li><strong>List & Table Orchestration:</strong> Формування нумерованих та маркованих списків (з використанням тире <code>–</code> за ДСТУ), а також складних таблиць (зокрема, безрамкових бланків завдань та щоденників переддипломної практики).</li>
            <li><strong>Code Syntax Highlight:</strong> Оформлення лістингів програмного коду моноширинним шрифтом Courier New з багатоколірним розпізнаванням ключових слів Python, рядків, операторів, числових констант та коментарів.</li>
        </ul>
    </div>
</div>

<!-- SECTION 02: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичні основи масштабування та верстки</h2></div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Алгоритм пропорційного масштабування зображень</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Якщо користувачем не вказано кастомну ширину зображення (параметр <code>?w=W_user</code>), то фінальний розмір $W_{\text{final}}$ на сторінці визначається на основі коефіцієнта пропорцій (Aspect Ratio) растрового файлу $A = H / W$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ W_{\text{final}} = \begin{cases} 
                    8.0 \text{ см}, & \text{якщо } A > 1.2 \quad (\text{виражена книжкова орієнтація}) \\
                    11.0 \text{ см}, & \text{якщо } 0.8 < A \le 1.2 \quad (\text{квадратна орієнтація}) \\
                    15.5 \text{ см}, & \text{якщо } A \le 0.8 \quad (\text{виражена альбомна орієнтація})
                    \end{cases} $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Оптимальний розподіл колонок таблиць</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для таблиць на всю корисну ширину сторінки ($W_{\text{total}} = 16.5$ см) за відсутності жорстко прописаних ширин колонок застосовується пропорційний розподіл на основі максимальної довжини символів у кожному стовпці:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ L_j = \max_{i} (\text{len}(C_{i, j})) \quad \implies \quad W_j = \frac{L_j}{\sum_{k=1}^{N_c} L_k} \times W_{\text{total}} $$
                </div>
                <p style="margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);">
                    При цьому кожна колонка обмежується мінімальним порогом $W_{\text{min}} = 2.0$ см для запобігання надмірному вертикальному стисненню тексту.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: INTERACTION PIPELINE (DIAGRAM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Життєвий цикл трансформації елементів</h2></div>
    <div class="glass-card">
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                MD_IN("Вхідний рядок Markdown") --> TYPE_DET{"Визначення типу елемента"}
                
                TYPE_DET -- "Заголовок (#, ##, ...)" --> Heading_Handler["should_be_in_toc() / clean_heading_dots()"]
                Heading_Handler --> H_STYLE["Додавання Heading Paragraph з keep_with_next=True"]
                
                TYPE_DET -- "Зображення (![...])" --> Image_Handler["PIL: Зчитування Aspect Ratio"]
                Image_Handler --> Img_Scale["Розрахунок ширини за формулою Aspect Ratio"]
                Img_Scale --> Img_Insert["Вставка картинки та підпису Джерела за ДСТУ"]
                
                TYPE_DET -- "Програмний код (```)" --> Code_Handler["add_code(): Рядковий токенізатор"]
                Code_Handler --> Token_High["Підсвітка ключових слів (Blue), рядків (Red), коментарів (Green)"]
                Token_High --> Mono_Para["Courier New 11pt, Shift+Enter переноси"]
                
                TYPE_DET -- "Таблиця (|...|)" --> Table_Handler["add_table(): Парсер рядків таблиці"]
                Table_Handler --> T_Border{"Безрамкова (Титулка/Завдання)?"}
                T_Border -- "Так" --> T_Borderless["col_widths = [7.5, 4.0, 5.0] (без сітки)"]
                T_Border -- "Ні" --> T_Grid["Table Grid, cantSplit для рядків"]
                
                H_STYLE & Img_Insert & Mono_Para & T_Borderless & T_Grid --> DOCX_OUT("Вихідний об'єкт python-docx")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 04: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Алгоритм токенізації та підсвітки синтаксису коду</h2></div>
    <div class="glass-card">
        <p>
            Псевдокод описує логіку роботи методу <code>add_code()</code> для побудови багатоколірних лістингів у форматі Word OpenXML:
        </p>
        <pre><code class="language-python">
def add_code(doc, code_lines):
    # Створюємо єдиний параграф для блоку коду
    paragraph = doc.add_paragraph()
    pf = paragraph.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.line_spacing = Pt(16) # Щільний міжрядковий інтервал
    
    python_keywords = {'def', 'class', 'import', 'return', 'if', 'else', 'for', 'try', 'except', 'self'}
    python_builtins = {'print', 'len', 'int', 'str', 'list', 'dict', 'range', 'Exception'}
    
    for line in code_lines:
        # Виділяємо коментар, якщо він є
        if '#' in line:
            main_part, comment_part = line.split('#', 1)
            comment_part = '#' + comment_part
        else:
            main_part, comment_part = line, ""
            
        # Токенізуємо рядок за допомогою regex
        tokens = re.split(r'(\s+|[(),\[\]{}:.=#@]|".*?"|\'.*?\')', main_part)
        for token in tokens:
            if not token: continue
            run = paragraph.add_run(token)
            set_font_courier_new(run, size=11)
            
            stripped = token.strip()
            if stripped in python_keywords:
                run.font.color.rgb = RGBColor(0, 0, 255) # Blue keywords
                run.font.bold = True
            elif stripped in python_builtins:
                run.font.color.rgb = RGBColor(0, 128, 128) # Teal builtins
            elif token.startswith('"') or token.startswith("'"):
                run.font.color.rgb = RGBColor(163, 21, 21) # Red strings
                
        # Додаємо коментар зеленим кольором
        if comment_part:
            run_comment = paragraph.add_run(comment_part)
            set_font_courier_new(run_comment, size=11)
            run_comment.font.color.rgb = RGBColor(0, 128, 0) # Green comments
            
        # Для переносів використовуємо Shift+Enter (символ '\n') замість створення нових параграфів
        if line != code_lines[-1]:
            paragraph.add_run('\n')
        </code></pre>
    </div>
</div>

<!-- SECTION 05: TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Технічний FAQ модуля</h2></div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому деякі заголовки H1 починаються з нової сторінки, а деякі — ні?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Модуль аналізує заголовок на наявність ключових слів великих розділів (<i>РОЗДІЛ, ВСТУП, ВИСНОВКИ, ЛІТЕРАТУРА, ДОДАТКИ</i>). Для таких заголовків автоматично встановлюється властивість <code>p.paragraph_format.page_break_before = True</code>. Інші заголовки H1 (наприклад, текстові блоки титульної сторінки) виводяться без розриву сторінки, щоб уникнути хаотичних порожніх проміжків.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Яким чином вилучаються "сміттєві" заголовки зі Змісту (TOC)?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Функція <code>should_be_in_toc()</code> виконує глибоку фільтрацію тексту за списком стоп-слів (наприклад, <i>"НА ТЕМУ", "СТУДЕНТУ", "КИЇВ", "РЕЦЕНЗІЯ", "КАЛЕНДАРНИЙ ПЛАН"</i>). Якщо рядок містить ці слова, параграф створюється як звичайний текст без стилю "Heading", що повністю блокує його потрапляння до автоматично генерованого Змісту в Word.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як забезпечується цілісність табличних даних при переносі сторінок?</h4>
        <p style="color: var(--text-dim);">
            A: Для кожного створеного рядка таблиці викликається OpenXML-маніпуляція через об'єкт <code>trPr = row._tr.get_or_add_trPr()</code>, куди записується маркер <code>cantSplit</code>. Це повідомляє текстовому процесору Microsoft Word, що рядок таблиці не може бути розірваний навпіл між сторінками, а повинен цілком переноситися на наступну сторінку.
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
