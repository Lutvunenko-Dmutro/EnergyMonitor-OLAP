# Технічний Паспорт Компонента: scripts/thesis/collect_stats.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🎓 ACADEMIC VOLUME ANALYZER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📖</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">collect_stats.py</h1>
            <p class="mega-subtitle">Аналізатор фізичного обсягу дипломної роботи, COM-інтегратор з MS Word API та автоматизований реєстратор метрик ДСТУ</p>
            <div class="status-tags">
                <span class="tag tag-online">METRICS ENGINE</span>
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
            <span class="metric-label">Target Format</span>
            <span class="metric-value">MS Word (.docx)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🌐</div>
        <div class="metric-info">
            <span class="metric-label">API Interface</span>
            <span class="metric-value">Windows win32com COM</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Metric Method</span>
            <span class="metric-value">ComputeStatistics(2)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">DSTU Standard</span>
            <span class="metric-value">Pages Verification</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль та науково-академічне призначення</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/thesis/collect_stats.py</code> — це **виділена утиліта академічного контролю та верстки** дипломного проєкту. Вона вирішує важливе практичне завдання: автоматично підраховує точну кількість фізичних сторінок у DOCX-файлах розділів диплома. Це дозволяє автору миттєво оцінювати загальний обсяг роботи перед фінальним злиттям, контролювати вимоги ДСТУ щодо рекомендованої кількості сторінок (наприклад, 80-120 сторінок без додатків) та уникати ручної рутинної перевірки.
        </p>
        <p style="margin-top: 10px;">
            Ключові технічні обов'язки аналізатора:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Automated Volume Analytics (Посторінковий аналіз):</strong> Послідовне сканування папки <code>docs/thesis/check_pages/</code> та виявлення всіх DOCX-модулів.</li>
            <li><strong>COM Integration (Зв'язок з MS Word):</strong> Ініціалізація та керування прихованим процесом MS Word (через Component Object Model) для динамічного прорахунку макета документа.</li>
            <li><strong>DSTU Audit (Аудит обсягів):</strong> Розрахунок загальної суми сторінок та виведення структурованої таблиці результатів в CLI інтерфейс.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Життєвий цикл роботи аналізатора (COM Audit Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Наступна схема демонструє процес запуску COM-сервера, послідовного опитування файлів та безпечного виходу:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск collect_stats.py") --> INIT_COM("1. win32com.client.Dispatch('Word.Application')")
                INIT_COM --> SET_VIS("2. word.Visible = False (Прихований запуск)")
                
                SET_VIS --> LIST_FILES("3. Сканування папки docs/thesis/check_pages/")
                LIST_FILES --> SORT_FILES("4. Сортування файлів за алфавітом")
                
                SORT_FILES --> LOOP_START("5. Цикл по файлах docx")
                LOOP_START --> OPEN_DOC("6. word.Documents.Open(path)")
                
                OPEN_DOC -- "Успішно відкрито" --> STATS("7. doc.ComputeStatistics(2) -> Pages Count")
                OPEN_DOC -- "Помилка (файл зайнятий / пошкоджений)" --> ERR("7a. Вивід помилки в консоль")
                
                STATS --> PRINT_LINE("8. Форматований вивід: Назва файлу | X стор.")
                PRINT_LINE --> CLOSE_DOC("9. doc.Close(False) (Без збереження змін)")
                
                CLOSE_DOC & ERR --> LOOP_NEXT("10. Перехід до наступного файлу")
                LOOP_NEXT -- "Маємо ще файли" --> LOOP_START
                LOOP_NEXT -- "Всі файли оброблено" --> SUM_ALL("11. Підрахунок загальної суми сторінок")
                
                SUM_ALL --> QUIT_WORD("12. word.Quit() (Закриття процесу WINWORD)")
                QUIT_WORD --> END("Виведення фінального звіту та завершення")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Технологія COM та математика динамічної розмітки</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Динамічний прорахунок сторінок (Dynamic Pagination)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    На відміну від PDF або текстових файлів, файли формату OpenXML (DOCX) не містять у своїй внутрішній структурі збережених маркерів сторінок. Кількість сторінок є динамічною функцією $P$, що залежить від параметрів рендерингу (розміри полів $M$, стилі шрифтів $F$, висота рядка $L$ та конфігурація принтера $D$):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ P_{\text{pages}} = f(M, F, L, D) $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Саме тому використання COM-сервера MS Word є єдиним способом отримати 100% точний результат, аналогічний тому, що побачить користувач при друці.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Константа wdStatisticPages</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Метод <code>ComputeStatistics(2)</code> використовує константу з переліку <code>WdStatistic</code>. Передача значення <code>2</code> відповідає запиту кількості сторінок:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{wdStatisticWords} = 0, \quad \text{wdStatisticLines} = 1, \quad \text{wdStatisticPages} = 2 $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Адитивне підрахування обсягу</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Фінальний обсяг роботи розраховується як проста адитивна сума сторінок усіх $N$ файлів розділів:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ P_{\text{total}} = \sum_{k=1}^{N} P_k $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод COM-інтеграції з MS Word</h2>
    </div>
    <div class="glass-card">
        <p>
            Логіка взаємодії з OLE Automation Server для аналізу сторінок:
        </p>
        <pre><code class="language-python">
# Псевдокод зчитування сторінок через MS Word COM
def get_thesis_pages_statistics(folder_path):
    # Ініціалізуємо OLE-зв'язок
    word_app = dispatch_ole_object("Word.Application")
    word_app.Visible = False
    
    total_pages = 0
    files_list = get_sorted_files_with_extension(folder_path, ".docx")
    
    for docx_file in files_list:
        try:
            # Відкриваємо документ у режимі "лише читання"
            document = word_app.Documents.Open(docx_file, ReadOnly=True)
            
            # 2 = wdStatisticPages
            pages_count = document.ComputeStatistics(2) 
            print(f"File: {docx_file} -> {pages_count} pages")
            
            total_pages += pages_count
            document.Close(SaveChanges=False)
        except Exception as error:
            print(f"Failed to parse {docx_file}: {error}")
            
    # Завжди закриваємо процес, щоб уникнути витоку пам'яті
    word_app.Quit()
    return total_pages
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому не можна дізнатися кількість сторінок простішим способом (наприклад, читанням метаданих OpenXML)?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Файли `.docx` дійсно містять метадані у файлі `docProps/app.xml` (тег `<Pages>`), проте ці дані записуються туди <u>лише в момент останнього ручного збереження</u> файлу користувачем у MS Word. Якщо документ генерується програмно (наприклад, через Pandoc або python-docx), ці метадані часто залишаються пустими або вказують застаріле значення. Тільки запуск двигуна рендерингу Word через COM-інтерфейс гарантує правильний прорахунок.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Що станеться, якщо скрипт впаде через помилку всередині циклу?</h4>
        <p style="color: var(--text-warning); margin-bottom: 15px;">
            ⚠️ <strong>ВАЖЛИВО:</strong> Якщо скрипт перерве роботу до виклику `word.Quit()`, процес `WINWORD.EXE` залишиться висіти в оперативній пам'яті Windows у фоновому режимі. Це може призвести до блокування файлів та споживання ресурсів. У разі аварійного завершення рекомендується запустити команду `taskkill /F /IM WINWORD.EXE` для очищення процесів.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Чи працює цей скрипт на ОС Linux / macOS?</h4>
        <p style="color: var(--text-dim);">
            A: Ні, бібліотека `win32com` є специфічною для ОС Windows, оскільки вона спирається на системний реєстр Windows та COM-двигун Microsoft Office. Для запуску на Linux/macOS потрібні інші інструменти (наприклад, LibreOffice в headless режимі), проте точність pagination там може відрізнятися від оригінального MS Word.
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
