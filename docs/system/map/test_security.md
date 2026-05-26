# Технічний Паспорт Компонента: tests/test_security.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🛡️ CYBER-SECURITY & INPUT PROTECTION SHIELD</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔒</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">test_security.py</h1>
            <p class="mega-subtitle">Система аудиту безпеки: захист від SQL-ін'єкцій, сканування витоків паролів Neon та валідація вхідних даних</p>
            <div class="status-tags">
                <span class="tag tag-online">SECURITY GATE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">VULNERABILITY SCANNER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Vulnerability Focus</span>
            <span class="metric-value">SQL Injection</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔑</div>
        <div class="metric-info">
            <span class="metric-label">Secret Leak Patrol</span>
            <span class="metric-value">Neon Key Regex</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔍</div>
        <div class="metric-info">
            <span class="metric-label">Validation Style</span>
            <span class="metric-value">Strict Whitelists</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🩹</div>
        <div class="metric-info">
            <span class="metric-label">Error Recovery</span>
            <span class="metric-value">Context-aware</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Системна безпека та цілісність кодової бази</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>tests/test_security.py</code> виконує роль головного кибер-щита проєкту <b>Energy Monitor Ultimate</b>. Його основна мета — гарантувати, що аналітична платформа надійно захищена від зовнішніх векторів атак, таких як впровадження шкідливого SQL-коду (SQL Injection), передавання аномальних вхідних значень, витік конфіденційних паролів підключення до Neon PostgreSQL та дестабілізація інтерфейсу через необроблені критичні помилки.
        </p>
        <p style="margin-top: 10px;">
            Ключові напрями кібер-аудиту:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>SQL Injection Shield (Превентивний аналіз):</strong> Валідація евристичних алгоритмів розпізнавання шкідливих сигнатур (наприклад, <code>UNION SELECT</code>, <code>DROP TABLE</code> або тавтології <code>'1'='1</code>).</li>
            <li><strong>Input Whitelisting (Суворі білі списки):</strong> Контроль за тим, щоб назви підстанцій, регіонів, числові параметри та часові діапазони відповідали суворим шаблонам типів та бізнес-обмежень.</li>
            <li><strong>Neon DB Key Patrol (Автоматичне сканування паролів):</strong> Вбудований у тести динамічний сканер кодової бази, який використовує регулярні вирази для пошуку випадково залишених хардкоджених токенів доступу до бази даних у хмарі.</li>
            <li><strong>Рендеринг та санітизація колонок:</strong> Запобігання атакам через кастомні SQL-запити до метаданих таблиць шляхом суворої фільтрації символів у назвах полів.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: SECURITY FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Алгоритм перевірки та фільтрації (Vulnerability Mitigation Flow)</h2>
    </div>
    <div class="glass-card">
        <p>
            На діаграмі показано, як вхідні дані проходять через захисні бар'єри перед виконанням:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                INPUT("Вхідний параметр (Рядок)") --> CHECKS_PATTERN{"1. Dangerous Patterns?"}
                
                CHECKS_PATTERN -- "Знайдено (DROP, UNION, etc.)" --> REJECT("Reject: ValidationError")
                CHECKS_PATTERN -- "Не знайдено" --> CHECKS_WHITELIST{"2. Whitelist Check?"}
                
                CHECKS_WHITELIST -- "Немає в списку" --> REJECT
                CHECKS_WHITELIST -- "Є в списку" --> SANITIZE{"3. Sanitize Column Names"}
                
                SANITIZE -- "Символи: . - ` або довжина > 100" --> REJECT
                SANITIZE -- "Валідно" --> EXECUTE("Безпечне виконання SQL / Рендеринг UI")
                
                style REJECT fill:#7f1d1d,stroke:#b91c1c,stroke-width:2px;
                style EXECUTE fill:#14532d,stroke:#15803d,stroke-width:2px;
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Детальний опис тест-класів та механік захисту</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Виявлення SQL-ін'єкцій (TestSQLInjectionPrevention)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Перевіряє роботу функції <code>_has_dangerous_patterns</code>. Тестується список із 6 класичних хакерських корисних навантажень (payloads), включаючи коментарі SQL <code>--</code> та об'єднання таблиць <code>UNION SELECT</code>. При виявленні ін'єкції у функціях валідації назв підстанцій чи регіонів має збуджуватися виключення <code>ValidationError</code>.
                </p>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Очищення назв колонок (TestColumnSanitization)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Назви колонок у Pandas та SQL-запитах мають містити лише безпечні літерно-цифрові символи та підкреслення. Будь-які спроби передати крапки, дефіси, зворотні апострофи (backticks) або рядки довжиною більше 100 символів блокуються збудженням <code>ValidationError</code>.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Патрулювання витоків Neon DB (test_no_hardcoded_passwords)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Вбудований статичний аналізатор коду (AST/Regex). Автоматично обходить дерево каталогу проєкту за допомогою <code>os.walk</code>, ігноруючи віртуальні папки (<code>.venv</code>, <code>.git</code> тощо), та шукає регулярним виразом випадково залишені паролі Neon DB:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    \text{Pattern} = \text{re.compile(r'npg\_[a-zA-Z0-9]\{12,\}')}
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Якщо сканер знаходить хоча б один витік у файлах `.py` чи `.md`, тест негайно падає з виведенням списку вразливих файлів.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">4. Валідація числових меж та відновлення (TestNumericValidation & TestRecovery)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Контролює діапазони числових значень (наприклад, температура, КВВП). Також перевіряє менеджер контексту помилок <code>ErrorContext</code>, який гарантує стійкість системи: навіть при виникненні виключення в межах операції, контекст записує помилку в лог і дозволяє решті системи продовжувати роботу.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод регулярного виразу детектора Neon DB</h2>
    </div>
    <div class="glass-card">
        <p>
            Логіка перевірки витоків токенів Neon, яка верифікується тестом, реалізована наступним чином:
        </p>
        <pre><code class="language-python">
# Псевдокод сканування витоків паролів
def scan_project_for_leaks():
    import re, os
    # Токени Neon PostgreSQL завжди починаються з 'npg_'
    neon_pattern = re.compile(r"npg_[a-zA-Z0-9]{12,}")
    leaks = []
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and file != 'test_security.py':
                with open(os.path.join(root, file), 'r') as f:
                    if neon_pattern.search(f.read()):
                        leaks.append(file)
                        
    return leaks # Має бути порожнім!
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому файл test_security.py виключений з переліку файлів для сканування витоків?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Усередині самого файлу <code>test_security.py</code> ми маємо описати регулярні вирази та тестові рядки для перевірки сканера. Якби ми не виключили сам файл тесту зі списку сканування, тест виявив би вразливість у самому собі (Self-Reference False Positive).
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Що таке npg_ у регулярному виразі?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Хмарний сервіс PostgreSQL <b>Neon</b> генерує паролі для підключення до БД, які завжди починаються з префікса <code>npg_</code>. Це унікальний сигнатурний ідентифікатор, який дозволяє виявляти витоки з ймовірністю 100% без помилкових спрацьовувань на випадкових рядках.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як зреагує система на спробу ввести завеликий інтервал дат?</h4>
        <p style="color: var(--text-dim);">
            A: Згідно з тестом <code>test_large_date_range_warning</code>, система не буде блокувати запит збудженням помилки, оскільки аналітика великих періодів є легітимною. Замість цього система просто запише попередження (Warning) в лог для аудиту навантаження на БД.
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
