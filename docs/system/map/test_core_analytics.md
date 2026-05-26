# Технічний Паспорт Компонента: tests/test_core_analytics.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">📊 MATHEMATICAL & OLAP ANALYSIS VALIDATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">test_core_analytics.py</h1>
            <p class="mega-subtitle">Система верифікації математичної точності багатовимірної фільтрації та OLAP-зрізів</p>
            <div class="status-tags">
                <span class="tag tag-online">ANALYTICS SENTRY</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">LOGIC GATE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🔍</div>
        <div class="metric-info">
            <span class="metric-label">Target Function</span>
            <span class="metric-value">filter_dataframe</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Memory Defense</span>
            <span class="metric-value">Copy vs View</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">Edge Cases Checked</span>
            <span class="metric-value">Missing Columns</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧱</div>
        <div class="metric-info">
            <span class="metric-label">Slicing Dimensions</span>
            <span class="metric-value">Region, Date, Substation</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Математична верифікація та цілісність</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>tests/test_core_analytics.py</code> фокусується на тестуванні критично важливої функції аналітичного ядра — <code>filter_dataframe</code> з модуля <code>src.core.analytics.filter</code>. Ця функція є основою для всіх звітів, графіків та дашбордів системи, забезпечуючи динамічну "нарізку" та фільтрацію телеметричних даних у реальному часі.
        </p>
        <p style="margin-top: 10px;">
            Головне завдання тестування — підтвердити, що:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Типова безпека (Type Safety):</strong> Функція жорстко реагує на некоректні типи даних, запобігаючи непередбачуваним збоям під час обчислень.</li>
            <li><strong>Багатовимірна фільтрація (Multi-dimensional Filtering):</strong> Зрізи за географічним регіоном, часовим вікном та конкретним енергетичним вузлом (підстанцією) виконуються строго за логічними правилами.</li>
            <li><strong>Безпека пам'яті (Memory Safety / Copy vs View):</strong> Результат фільтрації завжди є незалежною копією даних (Deep Copy), що запобігає модифікації оригінального масиву через посилання.</li>
            <li><strong>Стійкість до аномалій (Graceful Degradation):</strong> Відсутність окремих аналітичних колонок не ламає систему, а граційно обробляється з поверненням максимально доступного обсягу інформації.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: GRAPHICAL TEST WORKFLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Схема валідаційних сценаріїв (Validation Pathways)</h2>
    </div>
    <div class="glass-card">
        <p>
            Діаграма відображає розгалуження перевірок, що проходять через тестовий клас:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                INPUT("Вхідні дані (DataFrame)") --> CHECK_TYPE{"Перевірка типу?"}
                
                CHECK_TYPE -- "Не pd.DataFrame" --> RAISE_ERR("TypeError: Expected pd.DataFrame")
                CHECK_TYPE -- "pd.DataFrame" --> DIMS{"Розподіл за вимірами"}
                
                DIMS --> REGION("Фільтр Регіону")
                DIMS --> DATE("Фільтр Дати")
                DIMS --> SUBSTATION("Фільтр Підстанцій")
                DIMS --> MEMORY("Фільтр Копіювання")
                
                REGION --> REG_ALL("ALL_REGIONS: зберегти довжину")
                REGION --> REG_SPEC("Київ: довжина = 12")
                REGION --> REG_NONE("Неіснуючий: порожній DF")
                
                DATE --> DATE_IN("Тільки в межах [T_start, T_end]")
                
                SUBSTATION --> SUB_SINGLE("Одна підстанція: Київ ТЕС")
                SUBSTATION --> SUB_MULT("Список підстанцій: Київ ТЕС + Харків ТЕС")
                SUBSTATION --> SUB_EMPTY("Порожній список: Усі підстанції")
                
                MEMORY --> MEM_COPY("Зміна результату не змінює оригінал (L[0]=999)")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: DETAILED TEST CASES ANALYSIS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Розбір тестових кейсів та математичної логіки</h2>
    </div>
    <div class="glass-card">
        <p style="margin-bottom: 15px;">
            Тестове покриття реалізовано двома тестовими класами: <code>TestFilterDataframe</code> та <code>TestFilterEdgeCases</code>.
        </p>
        
        <table class="passport-table" style="width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 13.5px;">
            <thead>
                <tr style="border-bottom: 2px solid var(--border); text-align: left;">
                    <th style="padding: 10px; color: var(--accent);">Тестовий метод</th>
                    <th style="padding: 10px; color: var(--accent);">Що перевіряє</th>
                    <th style="padding: 10px; color: var(--accent);">Математичний інваріант / Очікуваний результат</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_dataframe_empty_input</td>
                    <td style="padding: 10px;">Поведінка на порожньому вході</td>
                    <td style="padding: 10px; color: var(--text-dim);"><code>df.empty is True</code>, тип результату — <code>pd.DataFrame</code></td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_dataframe_invalid_type</td>
                    <td style="padding: 10px;">Валідація типу вхідного параметра</td>
                    <td style="padding: 10px; color: var(--text-dim);">Виклик з рядком викидає <code>TypeError</code></td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_by_region</td>
                    <td style="padding: 10px;">Фільтрація по регіону</td>
                    <td style="padding: 10px; color: var(--text-dim);">Всі записи належать регіону, N_rows зменшується пропорційно (24 -> 12)</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_by_all_regions</td>
                    <td style="padding: 10px;">Вибір глобального ключа</td>
                    <td style="padding: 10px; color: var(--text-dim);"><code>ALL_REGIONS</code> зберігає початковий розмір набору даних</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_by_date_range</td>
                    <td style="padding: 10px;">Зріз за часовим вікном</td>
                    <td style="padding: 10px; color: var(--text-dim);"><code>∀ t ∈ result: T_start ≤ t.date ≤ T_end</code></td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_by_single_substation</td>
                    <td style="padding: 10px;">Вузол сітки (Single Node)</td>
                    <td style="padding: 10px; color: var(--text-dim);">Всі рядки мають <code>substation_name == "Київ ТЕС"</code></td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_by_multiple_substations</td>
                    <td style="padding: 10px;">Вузли сітки (Multi-node selection)</td>
                    <td style="padding: 10px; color: var(--text-dim);">Результат містить об'єднання множин підстанцій</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_returns_copy_not_view</td>
                    <td style="padding: 10px;">Герметичність пам'яті</td>
                    <td style="padding: 10px; color: var(--text-dim);"><code>result.loc[0, 'load'] = 999</code> не змінює оригінальний DataFrame</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_missing_columns</td>
                    <td style="padding: 10px;">Відсутність колонок фільтрації</td>
                    <td style="padding: 10px; color: var(--text-dim);">Відсутність <code>region_name</code> граційно ігнорується, повертаючи весь DF</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_nonexistent_region</td>
                    <td style="padding: 10px;">Неіснуючий регіональний вузол</td>
                    <td style="padding: 10px; color: var(--text-dim);">Повертає порожній DataFrame довжиною 0</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px; font-family: monospace;">test_filter_empty_substation_list</td>
                    <td style="padding: 10px;">Порожній список утиліт</td>
                    <td style="padding: 10px; color: var(--text-dim);">Передавання порожнього списку <code>[]</code> трактується як "Усі підстанції"</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE / FILTER CORE LOGIC -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод ядра аналітичного фільтра (Logical Filter Core)</h2>
    </div>
    <div class="glass-card">
        <p>
            Для кращого розуміння бізнес-логіки функції <code>filter_dataframe</code>, яку ми тестуємо, наведено псевдокод її внутрішньої структури:
        </p>
        <pre><code class="language-python">
def filter_dataframe(df, region, dates, dataset_name, substation=None):
    # 1. Валідація типів
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected pd.DataFrame, got ...")
        
    if df.empty:
        return df.copy()
        
    # Створюємо поверхневу копію для уникнення Side Effects
    result = df.copy()
    
    # 2. Фільтрація по регіону
    if region != "Усі регіони" and "region_name" in result.columns:
        result = result[result["region_name"] == region]
        
    # 3. Фільтрація по часовому діапазону [T_start, T_end]
    if dates is not None and "timestamp" in result.columns:
        start_date, end_date = dates
        result = result[
            (result["timestamp"].dt.date >= start_date) & 
            (result["timestamp"].dt.date <= end_date)
        ]
        
    # 4. Фільтрація по підстанціям
    if substation is not None and substation != [] and "substation_name" in result.columns:
        if isinstance(substation, list):
            result = result[result["substation_name"].isin(substation)]
        else:
            result = result[result["substation_name"] == substation]
            
    return result
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Питання та відповіді (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому перевірка копіювання DataFrame (Copy vs View) є настільки критичною?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: В аналітичних дашбордах pandas часто виконує "chained assignment" або повертає <code>SettingWithCopyWarning</code>. Якщо повернути звичайний View (посилання на пам'ять), будь-яка подальша зміна даних (наприклад, нормування чи коригування генерації) змінить глобальний кеш даних, що призведе до катастрофічного спотворення показників на інших екранах.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Що відбувається, якщо у вхідному файлі відсутня колонка регіону?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Згідно з логікою тесту <code>test_filter_missing_columns</code>, функція граційно ігнорує фільтр регіону і не ламається (не викидає KeyError). Вона просто повертає решту масиву, оскільки система має працювати навіть з частково деградованими джерелами даних.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як запустити тільки цей набір тестів?</h4>
        <p style="color: var(--text-dim);">
            A: Для запуску саме цього аналітичного сенсора виконайте команду: <code>pytest tests/test_core_analytics.py -v</code>
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
