# Технічний Паспорт Компонента: scripts/thesis/converter/formulas.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">⚛️ LATEX-TO-WORD MATH ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚛️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">formulas.py</h1>
            <p class="mega-subtitle">Двигун математичної трансформації, OLE/COM-інтегратор з MS Word, генератор MathML та менеджер буфера обміну</p>
            <div class="status-tags">
                <span class="tag tag-online">MATH ENGINE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">COM INTEGRATOR</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📑</div>
        <div class="metric-info">
            <span class="metric-label">Input Format</span>
            <span class="metric-value">LaTeX Notation ($ / $$)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧬</div>
        <div class="metrics-info">
            <span class="metric-label">Output Format</span>
            <span class="metric-value">Word Native OMML</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">win32com Patch</span>
            <span class="metric-value">Late Binding CDispatch</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-info">
            <span class="metric-label">Execution Strategy</span>
            <span class="metric-value">Single Pass COM execution</span>
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
            Модуль <code>scripts/thesis/converter/formulas.py</code> є <strong>високотехнологічним математичним транслятором (LaTeX-to-Word Math Engine)</strong> платформи <i>Energy Monitor Ultimate</i>. Він вирішує одну з найскладніших інженерних проблем при конвертації Markdown у формати Microsoft Office: перетворення академічного LaTeX-коду математичних формул у нативні редаговані об'єкти формул Word (OMML - Office Math Markup Language).
        </p>
        <p style="margin-top: 10px;">
            Основні задачі, які вирішує математичний двигун:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Трансформація LaTeX у MathML (LaTeX to MathML):</strong> Переклад синтаксису LaTeX в XML-представлення стандарту W3C MathML за допомогою вбудованих бібліотек.</li>
            <li><strong>Керування буфером Windows (Clipboard Bridge):</strong> Автоматизоване копіювання MathML XML-коду в системний буфер обміну з обробкою затримок та блокувань пам'яті Windows.</li>
            <li><strong>Нативна вставка об'єктів (COM Automation):</strong> Запуск прихованого процесу MS Word, пошук маркерів формул у тексті, вставка коду MathML з буфера (MS Word автоматично перетворює MathML на нативні формули) та встановлення правильної ДСТУ нумерації формул.</li>
            <li><strong>Monkey-patching OLE-кешу (Resilience Layer):</strong> Автоматичне виявлення та очищення бітих файлів згенерованого OLE-кешу (`gen_py`) та примусове ввімкнення пізнього динамічного зв'язування (Late Binding), що робить COM-з'єднання з Word абсолютно стійким до збоїв.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр обробки формул (COM Math Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Наступна схема демонструє детальний потік даних від вихідного коду LaTeX до нативного математичного блоку в Word:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск finalize_thesis_document()") --> FIX_CACHE("1. _fix_word_com_cache(): Очищення gen_py")
                FIX_CACHE --> MONKEY_PATCH("2. Monkey-patch gencache: GetClassForCLSID = None")
                
                MONKEY_PATCH --> LAUNCH_WORD("3. win32_dynamic.Dispatch('Word.Application')")
                LAUNCH_WORD --> OPEN_DOC("4. word.Documents.Open(abs_path)")
                
                OPEN_DOC --> SEARCH_MARKER("5. Пошук у тексті маркера '⇲'")
                SEARCH_MARKER -- "Не знайдено" --> UPDATE_FIELDS("10. doc_word.Fields.Update() (Оновлення Змісту)")
                SEARCH_MARKER -- "Знайдено" --> GET_LATEX("6. Вилучення тексту формули між ⇲ та ⇱")
                
                GET_LATEX --> CONV_XML("7. latex_to_mathml(formula)")
                CONV_XML --> CLIPBOARD("8. paste_mathml(): Копіювання XML у CF_UNICODETEXT")
                
                CLIPBOARD --> PASTE_WORD("9. rng.Paste() (Вставка у Word & Конвертація в OMML)")
                PASTE_WORD --> SEARCH_MARKER
                
                UPDATE_FIELDS --> SAVE_DOC("11. Збереження & Закриття Word")
                SAVE_DOC --> END("✅ Документ повністю оптимізовано")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математика вирівнювання та OLE-автоматизація</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Концепція двопозиційної табуляції (Dual Tab Alignment)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Згідно з ДСТУ, математична формула має бути розташована суворо по центру сторінки, а її порядковий номер — вирівняний по правому краю. Для забезпечення цього без створення громіздких невидимих таблиць, двигун впроваджує до абзацу формули дві точки табуляції на позиціях $T_1 = 8.5$ см (вирівнювання за центром) та $T_2 = 17.0$ см (вирівнювання за правим краєм):
                </p>
                <pre style="margin-bottom: 8px;"><code class="language-python">TabStops = {(8.5cm, Center), (17.0cm, Right)}  =>  Format = "\t Formula \t (Chapter.Number)"</code></pre>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Стійке динамічне зв'язування (Late Binding Resilience)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Раннє зв'язування (Early Binding) у бібліотеці `win32com` кешує схеми об'єктів у папці `gen_py`. Якщо це кешування пошкоджується, будь-який запуск Word падає з критичною помилкою. Двигун вирішує це, динамічно підміняючи функцію `GetClassForCLSID` на лямбда-вираз, що завжди повертає `None`, блокуючи звернення до кешу:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{gencache.GetClassForCLSID} = \lambda \text{ clsid}: \text{None} \quad \implies \quad \text{Force Late Binding (CDispatch)} $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод двигуна математичної оптимізації</h2>
    </div>
    <div class="glass-card">
        <p>
            Алгоритм вилучення, трансляції в MathML та вставки формул:
        </p>
        <pre><code class="language-python">
# Псевдокод математичного OLE-двигуна
import re
import time
import win32com.client as win32
import win32clipboard
from latex2mathml.converter import convert as latex_to_mathml

def process_formulas_in_word_document(docx_file_path):
    # 1. Захист від збоїв кешу win32com
    disable_early_binding_cache()
    
    # 2. Ініціалізація OLE сервера Word
    word_app = win32.Dispatch("Word.Application")
    word_app.Visible = False
    
    document = word_app.Documents.Open(docx_file_path)
    word_selection = word_app.Selection
    
    # Повертаємо курсор на початок
    word_selection.HomeKey(Unit=6) 
    search_engine = word_selection.Find
    
    while True:
        # Шукаємо відкриваючий маркер інлайнової формули
        search_engine.Text = "⇲"
        if not search_engine.Execute():
            break # Формули закінчилися
            
        start_position = word_selection.Start
        word_selection.Collapse(Direction=0) # Скидаємо виділення
        
        # Шукаємо закриваючий маркер
        search_engine.Text = "⇱"
        if not search_engine.Execute():
            break
            
        end_position = word_selection.End
        range_object = document.Range(start_position, end_position)
        
        # Вилучаємо чистий LaTeX-код
        latex_code = range_object.Text.replace("⇲", "").replace("⇱", "").strip()
        
        # 3. Конвертація в MathML XML
        mathml_xml = latex_to_mathml(latex_code)
        
        # 4. Вставка через системний буфер обміну Windows
        copy_text_to_clipboard(mathml_xml)
        time.sleep(0.05) # Мікрозатримка для синхронізації пам'яті
        
        # Word автоматично парсить MathML у нативну формулу при Paste
        range_object.Paste()
        word_selection.Collapse(Direction=0)
        
    # 5. Фіналізація: оновлюємо нативні поля Word (Зміст)
    document.Fields.Update()
    document.Save()
    document.Close()
    word_app.Quit()
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому для вставки формул використовується буфер обміну Windows (Clipboard)?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Microsoft Word має унікальну недокументовану особливість: він не має прямих API-методів для створення об'єктів формул з тексту (наприклад, через звичайні властивості тексту Range). Проте, якщо скопіювати в буфер обміну валідний XML-код стандарту W3C MathML та виконати команду `Range.Paste()`, внутрішній парсер Word автоматично розпізнає XML-структуру та "на льоту" трансформує її у чудовий нативний об'єкт математичного конструктора.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Що за помилка `CLSIDToPackageMap` виникає у win32com та як її долає скрипт?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Це відомий баг бібліотеки `pywin32`. Коли Word оновлюється або аварійно завершує роботу, кеш-папка `gen_py` (де зберігаються оптимізовані статичні класи зв'язку) пошкоджується. Будь-які наступні виклики `win32.Dispatch` викликають збій `AttributeError` або `TypeError`. Скрипт застосовує революційне вирішення: функція `_fix_word_com_cache` автоматично виявляє та видаляє пошкоджену директорію кешу Word на диску, а динамічний Dispatch з лямбда-патчем повністю вимикає використання статичного кешу, змушуючи систему працювати через стійке пізнє зв'язування.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Навіщо потрібна мікрозатримка `time.sleep(0.05)` перед вставкою?</h4>
        <p style="color: var(--text-dim);">
            A: Системний буфер обміну Windows (Clipboard) є спільним ресурсом операційної системи. Коли Python записує туди великий блок MathML-тексту, операційній системі потрібні лічені мілісекунди для виділення глобальної пам'яті (`GlobalAlloc`) та підтвердження транзакції буфера. Якщо спробувати вставити текст негайно, Word може виконати команду `Paste` до того, як буфер обновиться, що призведе до вставки попереднього скопійованого користувачем тексту. Затримка у 50 мс робить процес абсолютно надійним.
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
