# Технічний Паспорт Компонента: diagnose.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🛡️ SYSTEM DIAGNOSTICS & QUALITY GATE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🩺</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">diagnose.py</h1>
            <p class="mega-subtitle">Оркестратор автоматизованого аудиту кодової бази та генератор інтерактивних звітів якості</p>
            <div class="status-tags">
                <span class="tag tag-online">DIAGNOSTIC CORE</span>
                <span class="tag tag-version">v5.0.0</span>
                <span class="tag tag-role">QUALITY ASSURANCE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🔍</div>
        <div class="metric-info">
            <span class="metric-label">Audit Scope</span>
            <span class="metric-value">Whole Project</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📄</div>
        <div class="metric-info">
            <span class="metric-label">Report Format</span>
            <span class="metric-value">HTML Interactive</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-info">
            <span class="metric-label">Scanner Engine</span>
            <span class="metric-value">ProjectScanner</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚖️</div>
        <div class="metric-info">
            <span class="metric-label">Metric Type</span>
            <span class="metric-value">Health Score</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль діагностики проєкту</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>diagnose.py</code> є головним інструментом забезпечення якості (Quality Gate) та технічного аудиту проєкту <b>Energy Monitor Ultimate</b>. Він координує процеси статичного аналізу кодової бази, виявлення накопиченого технічного боргу, перевірки колізій імпортів та генерації наочних звітів для розробників.
        </p>
        <p style="margin-top: 10px;">
            Основний функціонал діагностики:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Статичне сканування структури (Project Scanner):</strong> Глибокий аналіз розташування файлів, наявності необхідних конфігурацій та перевірка коректності імпортів модулів.</li>
            <li><strong>Виявлення технічного боргу (Code Smell Detection):</strong> Сканування файлів на наявність неоптимальних конструкцій, легасі-коду та критичних помилок.</li>
            <li><strong>Розрахунок індексу стабільності (Health Score Matrix):</strong> Агрегація статистики виявлених дефектів та розрахунок загального рейтингу "здоров'я" системи.</li>
            <li><strong>Генерація інтерактивного звіту (HTML Reporting):</strong> Створення красивого адаптивного дашборду <code>diagnostics_report.html</code> з детальною таблицею знайдених проблем та рекомендаціями щодо їх усунення.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: GRAPHICAL DIAGNOSTICS WORKFLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр системного аудиту (Diagnostics Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема відображає послідовність етапів статичного аналізу та формування звіту:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск: diagnose.py") --> ROOT_DIR("Визначення кореня проєкту Path(__file__).parent")
                ROOT_DIR --> SCANNER_INIT("Ініціалізація ProjectScanner(ROOT)")
                
                SCANNER_INIT --> SCAN_ALL("scanner.scan_all()")
                
                subgraph "Етап 1: Статичний аналіз"
                    SCAN_ALL --> SCAN_IMPORTS("Аналіз імпортів")
                    SCAN_ALL --> SCAN_DEBT("Пошук технічного боргу")
                    SCAN_ALL --> SCAN_STRUCTURE("Аналіз структури файлів")
                end
                
                SCAN_IMPORTS & SCAN_DEBT & SCAN_STRUCTURE --> SCAN_RESULTS("Збір масиву scanner.results")
                
                SCAN_RESULTS --> REPORTER_INIT("Ініціалізація HtmlReporter()")
                REPORTER_INIT --> GEN_REPORT("reporter.generate(results, REPORT_PATH)")
                
                subgraph "Етап 2: Генерація звіту"
                    GEN_REPORT --> WRITE_HTML("Запис diagnostics_report.html")
                end
                
                WRITE_HTML --> CALCULATE_STATS("Розрахунок статистики помилок (total, err)")
                CALCULATE_STATS --> PRINT_STATS("Вивід підсумків у консоль")
                PRINT_STATS --> END("Завершення")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Архітектурні компоненти та метрики якості</h2>
    </div>
    <div class="glass-card">
        <p style="margin-bottom: 15px;">
            Система діагностики координує роботу двох центральних сервісних шарів:
        </p>
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Сканер структури (ProjectScanner)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Обходить дерево каталогів, ігноруючи приховані ресурси. У кожному `.py` файлі аналізує AST-дерево для виявлення застарілих або відсутніх імпортів, невикористовуваних змінних, а також небезпечних викликів (наприклад, <code>eval</code> чи хардкоджених секретів).
                </p>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Генератор звітів (HtmlReporter)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Перетворює плоский масив об'єктів результатів у сучасний HTML-дашборд. Звіт містить інтерактивні фільтри за категоріями помилок, семантичне кодування рівнів небезпеки (ERROR, WARNING, INFO) та покрокові інструкції з рефакторингу виявлених дефектів.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Матриця розрахунку Health Score</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Загальний індекс здоров'я розраховується на основі вагових коефіцієнтів критичності виявлених проблем:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{Health Score} = 100 - \frac{10 \times N_{\text{errors}} + 3 \times N_{\text{warnings}} + 1 \times N_{\text{info}}}{N_{\text{total\_files}}} $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Це дозволяє отримати об'єктивну відсоткову оцінку якості коду проєкту перед проходженням фінального захисту чи деплоєм на сервер.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод циклу діагностики</h2>
    </div>
    <div class="glass-card">
        <p>
            Псевдокод демонструє спрощений event loop роботи скрипта <code>diagnose.py</code>:
        </p>
        <pre><code class="language-python">
# Псевдокод головного циклу технічного аудиту
def run_diagnostics():
    project_root = get_current_directory()
    report_output = project_root + "/diagnostics_report.html"
    
    # 1. Запуск аналізу
    scanner = ProjectScanner(project_root)
    scanner.execute_deep_scan()
    
    # 2. Рендеринг звіту
    reporter = HtmlReporter()
    reporter.generate_dashboard(scanner.findings, report_output)
    
    # 3. Калькуляція статистики
    total_scanned = len(scanner.findings)
    error_count = count_severity(scanner.findings, level="ERROR")
    
    print(f"📊 Оброблені файли: {total_scanned}")
    print(f"❌ Критичні дефекти: {error_count}")
    print(f"📄 HTML-звіт згенеровано: {report_output}")
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Де зберігається diagnostics_report.html і як його переглянути?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Звіт зберігається безпосередньо у кореневій директорії проєкту. Ви можете відкрити його у будь-якому сучасному веб-браузері (Chrome, Firefox, Safari, Edge) подвійним кліком на файл. Він є повністю автономним (self-contained) і не вимагає інтернет-з'єднання.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чи можу я налаштувати правила сканування або додати нові перевірки?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Так. Усі правила статичного аналізу описані в класі <code>ProjectScanner</code> у файлі <code>src/core/diagnostics/scanner.py</code>. Ви можете легко додати нові регулярні вирази або логічні блоки для виявлення специфічного технічного боргу.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як часто рекомендується запускати діагностику?</h4>
        <p style="color: var(--text-dim);">
            A: Рекомендується запускати діагностику перед кожним комітом у репозиторій або деплоєм нової версії (Quality Gate). Для запуску виконайте команду: <code>python diagnose.py</code>
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
