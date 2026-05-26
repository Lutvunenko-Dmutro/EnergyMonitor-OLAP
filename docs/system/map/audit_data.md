# Технічний Паспорт Компонента: scripts/ml/audit_data.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">📊 ML TRAINING DATA QUALITY ASSURANCE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📈</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">audit_data.py</h1>
            <p class="mega-subtitle">Спеціалізований аудитор цілісності навчальних вибірок, розподілу ознак та кореляційного аналізу</p>
            <div class="status-tags">
                <span class="tag tag-online">DATA SENTRY</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">QUALITY GATE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">Target Model</span>
            <span class="metric-value">V3 (9 Features)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🚫</div>
        <div class="metric-info">
            <span class="metric-label">Null Scan</span>
            <span class="metric-value">df.isnull().sum()</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔗</div>
        <div class="metric-info">
            <span class="metric-label">Correlation</span>
            <span class="metric-value">Pearson (r_xy)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Statistics</span>
            <span class="metric-value">Descriptive</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Системний аудит та підготовка даних ШІ</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/ml/audit_data.py</code> є виділеним інструментом забезпечення якості даних (Data Quality Assurance Gate) у конвеєрі машинного навчання платформи <b>Energy Monitor Ultimate</b>. Він аналізує якість та інформативність накопиченої в базі даних телеметрії перед запуском процедури навчання або калібрування рекурентних нейромереж LSTM.
        </p>
        <p style="margin-top: 10px;">
            Ключові напрями аналізу даних:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Описова статистика (Descriptive Stats):</strong> Розрахунок середнього, медіани, стандартного відхилення та квартилів для розуміння форми розподілу ознак.</li>
            <li><strong>Патрулювання порожніх значень (Null Detection):</strong> Виявлення пропусків (NaN) та некоректних записів, які можуть призвести до падіння навчання через нескінченні градієнти (Exploding Gradients).</li>
            <li><strong>Частка нульових значень (Zero Density):</strong> Контроль розрідженості даних. Великий відсоток нулів у телеметрії (наприклад, тиску або вологості повітря) може вказувати на технічну несправність датчиків.</li>
            <li><strong>Кореляційний аудит Пірсона:</strong> Виявлення лінійного зв'язку між факторами впливу та цільовим споживанням електроенергії для оптимізації відбору фіч (Feature Selection).</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: DATAFLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр статичного аудиту даних (Data Sentry Workflow)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема ілюструє послідовність кроків аналізу тренувальної вибірки:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск: audit_data.py") --> LOAD_DB("1. load_data_from_db(version='v3')")
                LOAD_DB --> CHECK_EMPTY{"2. Data empty?"}
                
                CHECK_EMPTY -- "Empty (True)" --> REJECT("Print 'Дані порожні!' -> Exit")
                CHECK_EMPTY -- "Valid (False)" --> PRINT_ROWS("3. Print total rows count")
                
                PRINT_ROWS --> STATS("4. Run df.describe(): Mean, STD, Quartiles")
                STATS --> NULLS("5. Run df.isnull().sum(): NaN detection")
                NULLS --> ZEROS("6. Loop columns: Calculate % of zeros")
                ZEROS --> CORR("7. Run Pearson Correlation with load_mw")
                
                CORR --> PRINT_REPORT("8. Output consolidated console report")
                PRINT_REPORT --> END("End of audit")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичний апарат аудиту ознак</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Кореляція Пірсона (Pearson Correlation Coefficient)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Вимірює силу та напрямок лінійного зв'язку між ознакою $x$ та цільовим навантаженням $y$ (load_mw). Сортування результатів за спаданням дозволяє відкинути малоінформативні фактори:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ r_{xy} = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^n (x_i - \bar{x})^2 \sum_{i=1}^n (y_i - \bar{y})^2}} $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Щільність нульових значень (Zero Density Metric)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Якщо фізичний показник (температура, вологість, КВВП) дорівнює строго `0.0` протягом тривалого періоду, це може бути результатом системної помилки датчиків. Аудитор розраховує частку нулів $Z_c$ для кожної колонки $c$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    Z_c = \frac{1}{N} \sum_{i=1}^N [x_{i,c} == 0] \times 100\%
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Контракт моделі V3 (descriptive stats)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Модель версії V3 оперує багатофакторним набором ознак. Для успішного навчання середнє значення (mean) та стандартне відхилення (std) мають знаходитися в межах нормального фізичного діапазону.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму аудиту даних</h2>
    </div>
    <div class="glass-card">
        <p>
            Псевдокод головної процедури аудиту вибірок навчальних даних:
        </p>
        <pre><code class="language-python">
# Псевдокод статичного аудиту ознак
def run_data_audit(model_version="v3"):
    # 1. Отримання даних з PostgreSQL
    df = db.query_ml_dataset(version=model_version)
    
    if df.is_empty():
        log.error("Набір даних порожній!")
        return
        
    # 2. Розрахунок описових характеристик
    descriptive_report = df.compute_summary_statistics()
    
    # 3. Виявлення NaN пропусків
    missing_counts = df.count_null_values()
    
    # 4. Аналіз розрідженості (Zero Ratios)
    zero_ratios = {}
    for col in df.columns:
        zero_ratios[col] = (df[col] == 0).sum() / len(df) * 100.0
        
    # 5. Розрахунок коефіцієнтів кореляції
    correlation_matrix = df.compute_pearson_correlations(target="load_mw")
    
    return descriptive_report, missing_counts, zero_ratios, correlation_matrix
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому кореляція Пірсона розраховується саме для load_mw?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Наша LSTM-нейромережа має головне завдання — прогнозувати активне навантаження енергосистеми на наступну добу. Показник <code>load_mw</code> є нашою цільовою змінною (Target Variable). Аналізуючи кореляцію інших ознак (температура, вологість, день тижня) з <code>load_mw</code>, ми можемо переконатися, що модель отримує дійсно інформативні вхідні фактори.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому наявність пропусків (NaN) у тренувальній вибірці є критичною?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Алгоритми зворотного поширення помилки (Backpropagation) у нейромережах Keras/TensorFlow виконують обчислення матриць ваг. Наявність хоча б одного значення <code>NaN</code> призводить до того, що під час множення матриць усі ваги шару перетворюються на <code>NaN</code> (ефект лавини), що унеможливлює подальше навчання.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як запустити аудит вручну?</h4>
        <p style="color: var(--text-dim);">
            A: Для запуску аудитора навчальної вибірки виконайте команду: <code>python scripts/ml/audit_data.py</code>
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
