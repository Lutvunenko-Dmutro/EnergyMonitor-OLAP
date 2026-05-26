# Технічний Паспорт Компонента: tests/test_utils.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🔧 TOOLKIT & STABILITY RESILIENCE SENTINEL</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛠️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">test_utils.py</h1>
            <p class="mega-subtitle">Система верифікації допоміжних утиліт, безпечної алокації колонок та валідації часових меж</p>
            <div class="status-tags">
                <span class="tag tag-online">UTILITIES AUDITOR</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">STABILITY SHIELD</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🧹</div>
        <div class="metric-info">
            <span class="metric-label">Key Target</span>
            <span class="metric-value">helpers.py</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Defense Goal</span>
            <span class="metric-value">Prevent KeyError</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📅</div>
        <div class="metric-info">
            <span class="metric-label">Date Validation</span>
            <span class="metric-value">Bound Checks</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔄</div>
        <div class="metric-info">
            <span class="metric-label">Normalization</span>
            <span class="metric-value">Selection Normalizer</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Системний аудит та стабільність утиліт</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>tests/test_utils.py</code> є виділеним сенсором стабільності інфраструктурного шару утиліт проєкту <b>Energy Monitor Ultimate</b>. Він фокусується на тестуванні критично важливих функцій загального призначення з файлу <code>src.utils.helpers</code>, які використовуються у всіх частинах системи — від завантаження бази даних до рендерингу UI-елементів у Streamlit.
        </p>
        <p style="margin-top: 10px;">
            Він гарантує безперебійну роботу в наступних сценаріях:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Запобігання аварійним KeyError (Column Safety):</strong> Перевірка того, що при спробі побудувати графік за відсутніми або частково знятими з обліку колонками, система не падає, а граційно відкидає відсутні поля.</li>
            <li><strong>Нормалізація вибору користувача (Selection Sanitizer):</strong> Забезпечення стійкості до варіативності вводу підстанцій (окремий рядок, список з одним чи багатьма об'єктами, порожній вибір або None).</li>
            <li><strong>Цілісність часових інтервалів (Temporal Invariants):</strong> Контроль математичної правильності вибору часових меж (наприклад, неможливість встановити дату початку аналізу пізніше за дату завершення).</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: GRAPHICAL UTILITIES WORKFLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр обробки та стабілізації (Stability & Normalization Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема демонструє, як утиліти системи нормалізують та очищують дані для запобігання критичним помилкам:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                INPUT_SEL("Вхідний вибір підстанцій") --> NORM_SEL("1. normalize_substation_selection()")
                
                NORM_SEL -- "Рядок: 'Київ ТЕС'" --> OUT_STR("Повертає рядок 'Київ ТЕС'")
                NORM_SEL -- "Список: ['Київ ТЕС', 'Харків ТЕС']" --> OUT_FIRST("Повертає перший 'Київ ТЕС'")
                NORM_SEL -- "Порожній список: []" --> OUT_ALL("Повертає 'Усі підстанції'")
                NORM_SEL -- "None" --> OUT_NONE("Повертає None")
                
                INPUT_COLS("Очікувані колонки: ['A', 'B', 'C', 'D']") --> SAFE_COLS("2. get_safe_column_list()")
                SAFE_COLS -- "DataFrame має лише ['A', 'B']" --> OUT_SAFE("Повертає ['A', 'B'] (Безпечно без KeyError)")
                
                INPUT_DATES("Часовий діапазон: [T_start, T_end]") --> NORM_DATES("3. is_valid_date_range()")
                NORM_DATES -- "T_start <= T_end" --> OUT_TRUE("Valid (True)")
                NORM_DATES -- "T_start > T_end або None" --> OUT_FALSE("Invalid (False)")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Розбір тест-кейсів та математичної логіки</h2>
    </div>
    <div class="glass-card">
        <p style="margin-bottom: 15px;">
            Тестовий модуль охоплює три класи утиліт:
        </p>
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Нормалізація вибору (TestNormalizeSubstationSelection)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    У багатокористувацькому інтерфейсі Streamlit користувач може обирати як одну підстанцію, так і декілька. Утиліта <code>normalize_substation_selection</code> приводить будь-який формат вводу до єдиного рядка:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    S_{\text{norm}} = \begin{cases} s, & s \in \text{String} \\ s[0], & s \in \text{List} \land |s| \ge 1 \\ \text{"Усі підстанції"}, & s = [] \\ \text{None}, & s = \text{None} \end{cases}
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Валідація часових інтервалів (TestIsValidDateRange)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Перевіряє коректність вибору часового діапазону. Запобігає логічним збоям у SQL-запитах до бази даних. Функція <code>is_valid_date_range(D_s, D_e)</code> повертає <code>True</code> тільки тоді, коли обидві дати не дорівнюють `None` та виконується математична умова:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ D_{\text{start}} \le D_{\text{end}} $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Безпечна алокація колонок (TestGetSafeColumnList)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Якщо аналітичний модуль намагається звернутися до колонки DataFrame, якої немає у фізичній схемі файлу, pandas викидає помилку <code>KeyError</code>, яка ламає весь інтерфейс користувача. Функція <code>get_safe_column_list</code> динамічно перетинає очікувані колонки з реально існуючими в об'єкті, гарантуючи 100% захист від збоїв, зберігаючи вихідний порядок проходження колонок:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ C_{\text{safe}} = C_{\text{expected}} \cap C_{\text{actual}} $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму виділення безпечних колонок</h2>
    </div>
    <div class="glass-card">
        <p>
            Алгоритм безпечного вилучення колонок, який захищає систему від KeyError та верифікується тестами:
        </p>
        <pre><code class="language-python">
# Псевдокод захисту від KeyError у Pandas
def get_safe_column_list(dataframe, expected_columns):
    if dataframe.empty:
        return []
        
    actual_columns = set(dataframe.columns)
    safe_list = []
    
    # Зберігаємо порядок колонок згідно з очікуваним шаблоном
    for col in expected_columns:
        if col in actual_columns:
            safe_list.append(col)
            
    return safe_list
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому порожній список підстанцій [] перетворюється на "Усі підстанції"?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: В інтерфейсі користувача Streamlit при очищенні вибору віджет мульти-селектора повертає порожній список <code>[]</code>. З точки зору бізнес-логіки, якщо користувач нічого не обрав, це означає, що він бажає бачити сумарну аналітику по всій енергомережі, тому утиліта автоматично нормалізує цей вхід до дефолтного значення <code>"Усі підстанції"</code>.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чи підтримує валідатор дат переходи через кінець року?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Так, це спеціально перевіряється тестом <code>test_date_range_across_years</code>. Валідація базується на порівнянні об'єктів <code>datetime.date</code>, тому перехід з грудня на січень наступного року опрацьовується математично коректно.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Чи зберігає get_safe_column_list дублікати?</h4>
        <p style="color: var(--text-dim);">
            A: Так, згідно з тестом <code>test_get_safe_columns_with_duplicates</code>, якщо очікуваний список колонок містить дублікати (наприклад, через складну логіку групування), функція збереже їх у вихідному результаті, оскільки це може бути необхідно для побудови специфічних мульти-індексів.
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
