# Технічний Паспорт Компонента: scripts/thesis/converter/config.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">⚙️ THESIS CONVERSION REGISTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎛️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">config.py</h1>
            <p class="mega-subtitle">Центральний реєстр параметрів конвертації, менеджер інтелектуального мапінгу Mermaid-діаграм та конфігуратор білого списку додатків</p>
            <div class="status-tags">
                <span class="tag tag-online">REGISTRY NODE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">CONVERTER CONFIG</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📂</div>
        <div class="metric-info">
            <span class="metric-label">Input Target</span>
            <span class="metric-value">THESIS_FULL_FINAL_UTF8.md</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">💾</div>
        <div class="metric-info">
            <span class="metric-label">Output Target</span>
            <span class="metric-value">THESIS_FINAL.docx</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔄</div>
        <div class="metric-info">
            <span class="metric-label">Mermaid Mappings</span>
            <span class="metric-value">8 Active Signatures</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Appendix Limit</span>
            <span class="metric-value">9 Whitelisted Files</span>
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
            Модуль <code>scripts/thesis/converter/config.py</code> є <strong>головним інформаційним ядром та конфігуратором</strong> системи трансляції Markdown-to-Docx платформи <i>Energy Monitor Ultimate</i>. Він виступає "єдиним джерелом істини" для налаштування процесу збірки дипломної роботи, регламентуючи шляхи файлів, правила автозаміни інтерактивних схем та перелік вхідних лістингів коду.
        </p>
        <p style="margin-top: 10px;">
            Основні обов'язки та налаштування реєстру:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Визначення глобальних шляхів:</strong> Встановлення точних шляхів для вхідного монолітного файлу <code>THESIS_FULL_FINAL_UTF8.md</code> та результуючого Word-файлу <code>THESIS_FINAL.docx</code>.</li>
            <li><strong>Mermaid-to-Image Mapping (Реєстр замін):</strong> Оскільки MS Word не вміє динамічно рендерити Mermaid-діаграми, модуль містить унікальний словник `MERMAID_MAP`. Він ставить у відповідність текстовим сигнатурам Mermaid-схем (наприклад, <i>"erDiagram"</i> або <i>"sequenceDiagram"</i>) назви статичних високоякісних PNG-зображень та їх офіційні академічні підписи за ДСТУ.</li>
            <li><strong>Реєстрація білого списку коду (Appendix Whitelist):</strong> Чіткий перелік з 9 файлів ядра системи (таких як <code>predict_v2.py</code>, <code>physics.py</code>, <code>data_generator.py</code> тощо), які автоматично витягуються та додаються в Додатки пояснювальної записки.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Схема взаємодії конфігуратора з конвертером (Configuration Flow)</h2>
    </div>
    <div class="glass-card">
        <p>
            Діаграма демонструє, як налаштування `config.py` зчитуються різними вузлами системи під час процесу збірки документації:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                CONFIG("scripts/thesis/converter/config.py") --> |1. Шляхи INPUT / OUTPUT| ENGINE("scripts/thesis/converter/engine.py")
                CONFIG --> |2. Словник MERMAID_MAP| ENGINE
                CONFIG --> |3. Список WHITELIST_FILES| APPENDIX("scripts/thesis/converter/appendix.py")
                
                ENGINE --> |4. Автозаміна Mermaid на зображення & Вставка підписів ДСТУ| DOCX("Формування об'єкта Document")
                APPENDIX --> |5. Сканування src/ & Збір лістингів коду| DOCX
                
                DOCX --> |6. Збереження| TARGET_FILE("THESIS_FINAL.docx")
                
                style CONFIG fill:#1e293b,stroke:#38bdf8,stroke-width:2px
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Технічні деталі та логіка інтелектуального мапінгу</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Логіка виявлення та заміна Mermaid сигнатур</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Під час лінійного парсингу Markdown-файлу, якщо рядок відповідає одній із сигнатур-ключів $K$ словника `MERMAID_MAP`, двигун автоматично припиняє читання текстового блоку та виконує заміну на відповідний кортеж $V = (\text{img\_name}, \text{caption})$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{If } \text{line}. \text{startswith}(K_i) \quad \implies \quad \text{InsertImage}(V_{i,0}) \oplus \text{InsertCaption}(V_{i,1}) $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Оптимізація обсягу Додатків коду</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Замість обходу всього репозиторію, який призвів би до перевантаження документа сторінками коду, список `WHITELIST_FILES` є обмеженим. Для кожного файлу $f$ на диску перевіряється умова входження до білого списку $W$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{IncludeFile}(f) = \begin{cases} 
                      \text{True}, & f \in W \\
                      \text{False}, & f \notin W 
                   \end{cases} $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод реєстру конфігурацій</h2>
    </div>
    <div class="glass-card">
        <p>
            Структура словника замін та білого списку:
        </p>
        <pre><code class="language-python">
# Псевдокод конфігуратора конвертера
# scripts/thesis/converter/config.py

# Головні шляхи збірки
INPUT_MARKDOWN_PATH = "docs/thesis/THESIS_FULL_FINAL_UTF8.md"
OUTPUT_WORD_PATH    = "docs/thesis/THESIS_FINAL.docx"

# Реєстр мапінгу схем Mermaid на статичні файли малюнків
MERMAID_DIAGRAMS_MAP = {
    "graph TB\n    subgraph UI": (
        "diag_architecture.png", 
        "Рис. 3.0. Архітектурна схема системи EnergyMonitor-OLAP"
    ),
    "erDiagram": (
        "diag_er_db.png", 
        "Рис. 3.4. Схема бази даних (ER-діаграма)"
    ),
    "graph TD\n    subgraph Local": (
        "diag_infra_cloud.png", 
        "Рис. 3.2. Схема розгортання та потоків даних системи"
    )
}

# Дозволені файли для імпорту в Додаток Л
CODE_LISTINGS_WHITELIST = [
    "physics.py", 
    "predict_v2.py", 
    "vectorizer.py", 
    "metrics_engine.py",
    "data_generator.py"
]
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Навіщо потрібна заміна схем Mermaid на картинки?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Схеми Mermaid є текстовим описом графа, який чудово рендериться у веб-середовищі (наприклад, на GitHub чи MkDocs-сервері) за допомогою бібліотеки `mermaid.js`. Проте Microsoft Word не підтримує виконання JavaScript та не вміє відображати текстовий код у вигляді красивих графів. Завдяки словнику `MERMAID_MAP`, двигун автоматично знаходить код схеми і вставляє замість нього заздалегідь підготовлене та протестоване PNG-зображення діаграми, зберігаючи ДСТУ підписи рисунків.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Як змінити підпис під малюнком у дипломі?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Для цього не потрібно шукати місце у великому коді конвертера. Достатньо просто відкрити файл `config.py` та змінити текстове значення у відповідному кортежі словника `MERMAID_MAP`. Наприклад, замінити `"Рис. 3.4. Схема бази даних (ER-діаграма)"` на `"Рис. 3.4. Логічна ER-діаграма схеми даних PostgreSQL"`. Під час наступної збірки підпис оновиться автоматично.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як додати новий файл коду в Додатки?</h4>
        <p style="color: var(--text-dim);">
            A: Потрібно відкрити `config.py`, знайти список `WHITELIST_FILES` та дописати туди точне ім'я файлу (наприклад, `"check_db_stats.py"`). Під час обходу репозиторію скрипт автоматично виявить цей файл у папці `scripts/system/`, прочитає його та додасть до кінця Додатка Л.
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
