# Технічний Паспорт Компонента: scripts/thesis/convert_thesis.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🎓 ACADEMIC THESIS CONVERSION ORCHESTRATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚀</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">convert_thesis.py</h1>
            <p class="mega-subtitle">Головний оркестратор автоматизованої збірки, трансляції Markdown-to-Docx та верифікації дипломного проєкту</p>
            <div class="status-tags">
                <span class="tag tag-online">ORCHESTRATOR</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">ACADEMIC BUILDER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🛠️</div>
        <div class="metric-info">
            <span class="metric-label">Pipeline Pass</span>
            <span class="metric-value">Pandoc & COM Merge</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📑</div>
        <div class="metric-info">
            <span class="metric-label">Total Modules</span>
            <span class="metric-value">13 Thesis Chapters</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-info">
            <span class="metric-label">Pre-check Command</span>
            <span class="metric-value">taskkill WINWORD</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Strict Rule</span>
            <span class="metric-value">No AI-smell wording</span>
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
            Модуль <code>scripts/thesis/convert_thesis.py</code> є <strong>головним диспетчером та компілятором</strong> дипломного проєкту в екосистемі <i>Energy Monitor Ultimate</i>. Він автоматизує збірку дисертаційного матеріалу з десятків окремих Markdown-файлів (розділи теорії, вимог, архітектури, експериментів та додатків коду) у єдиний монолітний документ MS Word (DOCX) за суворим стандартом ДСТУ.
        </p>
        <p style="margin-top: 10px;">
            Критичні правила та вимоги конвеєра:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Угода про найменування (Naming Convention):</strong> Фінальний згенерований файл обов'язково зберігається у форматі <code>Литвиненко_YYYYMMDD.docx</code> для фіксації дати збірки.</li>
            <li><strong>Очищення процесів (Process Hygiene):</strong> Перед початком генерації скрипт обов'язково здійснює примусове закриття фонових процесів MS Word через <code>taskkill</code> для запобігання конфліктів блокування файлів (I/O File Lock).</li>
            <li><strong>Академічна цензура тексту (Anti-AI check):</strong> Контроль відсутності специфічних "AI-smell" слів-маркерів (наприклад, <i>парадигма, трансформація, екосистема</i>), що можуть сигналізувати про неякісну генерацію тексту сторонніми ШІ-моделями.</li>
            <li><strong>Інтеграція метрик обсягу:</strong> Після успішної збірки оркестратор автоматично викликає модуль <code>collect_stats.py</code> для вимірювання фінального обсягу сторінок.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Схема конвеєра збірки (Thesis Build & Merge Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Діаграма відображає послідовні фази від санітації робочого середовища до посторінкової конвертації, злиття розділів та запуску аудиту:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск convert_thesis.py --all") --> CLEAN_PROC("1. taskkill /F /IM WINWORD.EXE")
                CLEAN_PROC --> LIST_CHAPS("2. Завантаження списку з 13 розділів (THESIS_MODULES)")
                
                LIST_CHAPS --> LOOP_START("3. Цикл по кожному розділу")
                LOOP_START --> CONV_INDIV("4. run_conversion(): Конвертація окремого MD в check_pages/*.docx")
                
                CONV_INDIV --> LOOP_NEXT("5. Перехід до наступного розділу")
                LOOP_NEXT -- "Маємо ще файли" --> LOOP_START
                LOOP_NEXT -- "Всі розділи сконвертовано" --> MERGE_CORE("6. Виклик merge_thesis.main(): Злиття MD в єдиний UTF-8")
                
                MERGE_CORE --> GEN_FINAL("7. run_conversion(): Створення Литвиненко_YYYYMMDD.docx")
                GEN_FINAL --> STATS("8. Виклик get_stats(): Фінальний замір сторінок")
                
                STATS --> END("✅ Збірка успішно завершена")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математична модель зшивання та конфігурація збірки</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Алгоритм пакетної конкатенації (Markdown Stitching)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Перед фінальним рендерингом у формат DOCX, всі глави диплома $C_i$ конкатенуються у єдиний монолітний UTF-8 файл $M_{\text{final}}$. Процес зшивання враховує необхідність вставки символів примусового розриву сторінки (Page Break, $\text{PB}$) між розділами для дотримання академічної верстки:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ M_{\text{final}} = \bigoplus_{i=1}^{K} \left( C_i \oplus \text{PB} \right) \quad (\text{де } K = 13) $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Хронологічне кодування імені файлу</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для уникнення плутанини між версіями збірок під час спільної роботи з науковим керівником, фінальний артефакт підписується датою генерації:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ F_{\text{out}} = \text{"Литвиненко\_"} \oplus \text{FormatDateTime}(\text{"yyyyMMdd"}, \text{Now}()) \oplus \text{".docx"} $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод оркестрації збірки</h2>
    </div>
    <div class="glass-card">
        <p>
            Спрощена схема координації процесів та виклику конвертерів:
        </p>
        <pre><code class="language-python">
# Псевдокод головного академічного оркестратора
def compile_diploma_pipeline(modules_list):
    # 1. Захист від заблокованих файлів
    kill_process_by_name("WINWORD.EXE")
    
    # 2. Посторінкова проміжна конвертація
    for md_file in modules_list:
        output_name = md_file.replace(".md", ".docx")
        run_markdown_to_docx(
            source=f"docs/thesis/{md_file}",
            target=f"docs/thesis/check_pages/{output_name}",
            render_settings={"appendix": False}
        )
        
    # 3. Злиття розділів у єдиний монолітний файл знань
    import merge_thesis_script
    merge_thesis_script.merge_all_markdown_files()
    
    # 4. Рендеринг фінальної дисертації
    current_date = get_formatted_date("YYYYMMDD")
    final_docx_path = f"docs/thesis/Литвиненко_{current_date}.docx"
    
    run_markdown_to_docx(
        source="docs/thesis/THESIS_FULL_FINAL_UTF8.md",
        target=final_docx_path,
        render_settings={"appendix": True}
    )
    
    # 5. Автоматичний аудит сторінок
    total_pages = trigger_collect_stats_module()
    print(f"Compilation Successful. Total Page count: {total_pages}")
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому перед початком збірки обов'язково закривається MS Word?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: MS Word під час відкриття файлу DOCX накладає ексклюзивне блокування на запис (I/O File Lock) та створює прихований тимчасовий файл-двійник (починається з `~$`). Якщо в цей момент скрипт спробує перезаписати цей файл новою версією, операційна система Windows поверне критичну помилку `PermissionError: [Errno 13] Permission denied`. Попередній `taskkill` гарантує свободу запису.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Що таке "AI-smell" слова та чому вони під забороною?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Сучасні великі мовні моделі (наприклад, GPT або Claude) мають характерний стилістичний почерк, часто зловживаючи пафосними абстрактними термінами (<i>трансформація, парадигма, екосистема, синергія, рушійна сила, мінімізувати, інтегрувати</i>). Наукові керівники та рецензенти легко виявляють такі слова, що шкодить оцінці роботи. Ми дотримуємося строгого інженерного та сухого академічного стилю викладу.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як запустити повну збірку диплома?</h4>
        <p style="color: var(--text-dim);">
            A: Для запуску повної збірки та злиття всіх частин слід передати спеціальний прапорець командного рядка: <code>python scripts/thesis/convert_thesis.py --all</code>. Якщо прапорець відсутній, скрипт виконає поодиноку конвертацію одного файлу, вказаного в аргументах.
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
