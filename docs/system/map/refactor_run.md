# Технічний Паспорт Компонента: scripts/system/refactor_run.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">⚡ AUTOMATED REFACTORING ORCHESTRATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛠️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">refactor_run.py</h1>
            <p class="mega-subtitle">Автоматизований оркестратор масового структурного рефакторингу та модульної деструктуризації кодової бази</p>
            <div class="status-tags">
                <span class="tag tag-online">REFACTORING ENGINE</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">ARCHITECTURE SANITIZER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🔄</div>
        <div class="metric-info">
            <span class="metric-label">Decoupling Target</span>
            <span class="metric-value">forecast.py / backtest.py</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📈</div>
        <div class="metric-info">
            <span class="metric-label">Target Component</span>
            <span class="metric-value">charts.py Integration</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-info">
            <span class="metric-label">Methodology</span>
            <span class="metric-value">Line Index Parsing</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Safety Level</span>
            <span class="metric-value">Destructive Read/Write</span>
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
            Модуль <code>scripts/system/refactor_run.py</code> виконує роль <strong>виділеного інструменту автоматизації рефакторингу</strong> архітектури платформи <i>Energy Monitor Ultimate</i>. Він призначений для вирішення проблеми накопичення "технічного боргу" та розмиття архітектурних шарів, автоматично розділяючи бізнес-логіку (ML-моделі та розрахунки) від візуального представлення (побудова графіків Plotly).
        </p>
        <p style="margin-top: 10px;">
            Основні задачі, які вирішує оркестратор рефакторингу:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Logic Extraction (Вилучення логіки):</strong> Автоматичне знаходження та виділення функцій малювання графіків (наприклад, <code>_generate_mega_hybrid_figure</code> та <code>_generate_forecast_figure</code>) з громіздкого інтерфейсного файлу <code>ui/views/forecast.py</code>.</li>
            <li><strong>Module Decoupling (Розв'язка модулів):</strong> Очищення файлу бектексту <code>ml/backtest.py</code> від академічних графічних методів (<code>generate_academic_plots</code>) та перенесення їх до спеціалізованого сховища графіків <code>ui/components/charts.py</code>.</li>
            <li><strong>Code Clean-up (Очищення імпортів):</strong> Видалення старих імпортів та впровадження нових посилань для збереження цілісності збірки проєкту.</li>
            <li><strong>Batch Synchronization (Пакетна синхронізація):</strong> Одночасна перезапис трьох ключових файлів системи в один прохід для гарантування працездатності.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр рефакторингу (Refactoring Operations Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Діаграма ілюструє точну черговість читання, парсингу, вирізання та вставки фрагментів коду під час роботи скрипта:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск refactor_run.py") --> READ_FC("1. Читання ui/views/forecast.py")
                READ_FC --> INDEX_FC("2. Визначення індексів функцій за назвами методів")
                
                INDEX_FC --> EXT_FC("3. Вирізання блоків коду: mega_hybrid_figure & forecast_figure")
                EXT_FC --> WRITE_FC("4. Перезапис ui/views/forecast.py (з новими імпортами)")
                
                WRITE_FC --> READ_BT("5. Читання ml/backtest.py")
                READ_BT --> INDEX_BT("6. Пошук індексу generate_academic_plots")
                
                INDEX_BT --> EXT_BT("7. Вирізання блоку коду: academic_plots")
                EXT_BT --> WRITE_BT("8. Перезапис ml/backtest.py (вилучено малювання)")
                
                WRITE_BT --> APP_CHARTS("9. Дописування вирізаного коду в ui/components/charts.py")
                APP_CHARTS --> IMP_CHARTS("10. Імпорт scipy, numpy, r2_score до charts.py")
                
                IMP_CHARTS --> END("Успішне завершення рефакторингу")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математика індексного зміщення та безпечного виділення рядків</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Визначення меж функції за індексами рядків</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Оскільки структура файлу є відомою, виділення блоку коду функції $F$ з масиву рядків $L$ виконується шляхом пошуку точного індексу початку сигнатури $I_{\text{start}}$ та початку наступного логічного методу $I_{\text{end}}$. Зріз рядків описується як:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ F = \bigcup_{i = I_{\text{start}}}^{I_{\text{end}} - 1} L_i $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Оптимальне зшивання інтерфейсного файлу</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Новий файл будується як об'єднання початкової секції імпортів (до першої вилученої функції $I_{\text{cache}}$), блоку нових модульних імпортів $I_{\text{new\_imports}}$ та збережених фрагментів бізнес-логіки:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ L_{\text{new}} = \{ L_0 \dots L_{I_{\text{cache}}-1} \} \cup I_{\text{new\_imports}} \cup \{ L_{I_{\text{comp}}} \dots L_{I_{\text{fig}}-1} \} \cup \{ L_{I_{\text{render}}} \dots L_{N-1} \} $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму деструктуризації</h2>
    </div>
    <div class="glass-card">
        <p>
            Спрощена схема зчитування, пошуку індексів та розподілу коду:
        </p>
        <pre><code class="language-python">
# Псевдокод алгоритму рефакторингу
def execute_system_refactoring():
    # 1. Читаємо вихідні дані
    forecast_lines = read_lines("ui/views/forecast.py")
    
    # 2. Знаходимо індекси меж методів
    idx_mega = forecast_lines.index("def _generate_mega_hybrid_figure")
    idx_comp = forecast_lines.index("def _render_comparative_audit")
    idx_fig  = forecast_lines.index("def _generate_forecast_figure")
    idx_rend = forecast_lines.index("def render")
    
    # 3. Вирізаємо код для перенесення
    mega_code_block = forecast_lines[idx_mega : idx_comp]
    fig_code_block  = forecast_lines[idx_fig  : idx_rend]
    
    # 4. Формуємо новий файл з підключенням модульного імпорту
    new_forecast = forecast_lines[0 : idx_mega]
    new_forecast.append("from src.ui.components.charts import _generate_mega_hybrid_figure, _generate_forecast_figure\n")
    new_forecast.extend(forecast_lines[idx_comp : idx_fig])
    new_forecast.extend(forecast_lines[idx_rend : ])
    
    write_file("ui/views/forecast.py", new_forecast)
    
    # 5. Додаємо вилучений код у спільну бібліотеку графіків
    append_to_file("ui/components/charts.py", mega_code_block + fig_code_block)
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому використовується метод пошуку за точними індексами рядків?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Пошук за назвою сигнатури є швидким та детермінованим способом для цього конкретного рефакторингу. Оскільки структура `forecast.py` та `backtest.py` є добре задокументованою, цей підхід гарантує повне вилучення методів від першого символу до початку наступного блоку без ризику пропустити внутрішні декоратори.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чи безпечно запускати цей скрипт декілька разів підряд?</h4>
        <p style="color: var(--text-warning); margin-bottom: 15px;">
            ⚠️ <strong>УВАГА:</strong> Цей скрипт є <u>деструктивним</u> при повторному виконанні. Оскільки він очікує знайти сигнатури функцій у вихідних файлах для визначення індексів, після першого успішного виконання ці функції зникнуть з `forecast.py`, і повторний запуск викличе помилку `ValueError: list.index(x): x not in list`. Запускати скрипт слід лише один раз під час модернізації архітектури.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Яку користь приніс цей рефакторинг для системи?</h4>
        <p style="color: var(--text-dim);">
            A: Ми повністю розв'язали модулі за стандартом Clean Architecture. Файли `ui/views/forecast.py` та `ml/backtest.py` тепер містять виключно координаційну логіку та математичні обчислення, не замислюючись про те, як малювати графіки. Уся графічна логіка зосереджена у `charts.py`, що дозволяє легко змінювати стиль графіків у майбутньому без ризику зламати розрахунки прогнозу.
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
