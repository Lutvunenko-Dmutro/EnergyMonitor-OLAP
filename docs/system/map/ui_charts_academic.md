# Технічна специфікація: Візуалізатор Академічної Звітності (ACADEMIC RESEARCH VISUALIZATION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">THESIS VISUALIZATION | NEURAL AUDIT</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎓</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Академічна Звітність</h1>
            <p class="mega-subtitle">Спеціалізований модуль візуалізації наукових результатів: статистичний аналіз помилок нейромереж (Figure 7), регресійна кореляція (Figure 8) та часова динаміка (Figure 5) згідно зі стандартами дипломного проектування</p>
            <div class="status-tags"><span class="tag tag-online">ACADEMIC VIZ ACTIVE</span><span class="tag tag-version">v2.4.0</span><span class="tag tag-role">RESEARCH AUDITOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Figure 7</span><span class="metric-value">Statistical Error Distribution</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔵</div><div class="metric-info"><span class="metric-label">Figure 8</span><span class="metric-value">Regression Correlation (y=x)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📉</div><div class="metric-info"><span class="metric-label">Figure 5</span><span class="metric-value">Temporal Tracking</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔬</div><div class="metric-info"><span class="metric-label">Engine</span><span class="metric-value">Scipy / NumPy Integration</span></div></div>
</div>

<!-- SECTION 01: ACADEMIC VISUALIZATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Академічної Візуалізації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>academic.py</code> є "Доказовою базою" проекту ATLAS. В академічному середовищі недостатньо просто показати прогноз — необхідно науково обґрунтувати його точність. Наша філософія базується на <b>Статистичній Суворості</b>: ми розробили набір графіків, які відповідають стандартам наукових публікацій. Використання нормального розподілу помилок та регресійних діаграм дозволяє не просто "вірити" штучному інтелекту, а математично довести його ефективність та стабільність, що є критичним для успішного захисту магістерської дисертації.</p>
    </div>
</div>

<!-- SECTION 02: ACADEMIC PLOTTING PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр академічної візуалізації (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Actual vs Predicted Dataset") --> UNIFY("Unify Data (DataFrame or Multi-dict)")
    
    UNIFY --> FIG5("Figure 5: Temporal Dynamics")
    FIG5 --> OVERLAY("Overlay LSTM Predictions on Ground Truth")
    
    UNIFY --> FIG7("Figure 7: Error Statistics")
    FIG7 --> HIST("Probability Density Histogram")
    HIST --> SCIPY("Scipy Normal Distribution Fit (mu/std)")
    
    UNIFY --> FIG8("Figure 8: Regression Map")
    FIG8 --> IDEAL("Add 'Ideal Line' (y=x)")
    IDEAL --> SCATTER("Scatter Markers Analysis")
    
    OVERLAY --> RENDER("Final Research Suite")
    SCIPY --> RENDER
    SCATTER --> RENDER
    </div></div>
</div>

<!-- SECTION 03: STATISTICAL ERROR ANALYSIS (FIG. 7) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Статистичний аналіз помилок (Figure 7)</h2></div>
    <div class="glass-card flow-step">
        <p>Для Figure 7 ми впровадили гібридну візуалізацію розподілу похибки:</p>
        <ul>
            <li><b>Probability Density:</b> Гістограма показує щільність імовірності відхилення прогнозу від факту. Ми використовуємо напівпрозорий режим (opacity 0.2) для фонового відображення.</li>
            <li><b>Normal Distribution Fit:</b> Використовуючи <code>scipy.stats.norm</code>, система автоматично розраховує математичне очікування (mu) та середньоквадратичне відхилення (std) помилки, накладаючи ідеальну криву розподілу. Це наочно демонструє відсутність системного зміщення в моделях ШІ.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: ACADEMIC FIGURE MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця академічних графіків (Thesis Standards)</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Номер рисунка</th>
                    <th>Тип аналізу</th>
                    <th>Наукова цінність</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Figure 5</td><td>Temporal Dynamics</td><td>Візуалізація здатності LSTM до відстеження трендів</td></tr>
                <tr><td>Figure 7</td><td>Error Density</td><td>Математичне підтвердження нормальності похибки</td></tr>
                <tr><td>Figure 8</td><td>Neural Regression</td><td>Оцінка кореляції прогнозу з реальністю (Ground Truth)</td></tr>
                <tr><td>Multi-Model</td><td>Comparative Tracking</td><td>Обґрунтування вибору конкретної архітектури ШІ</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: NEURAL REGRESSION CORRELATION (FIG. 8) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Регресійна кореляція нейромережі (Figure 8)</h2></div>
    <div class="glass-card flow-step">
        <p>Для Figure 8 ми використовуємо Scatter-діаграму, де кожна точка — це пара (Actual, Predicted). Ми додаємо пунктирну лінію <b>"Ideal Line (y=x)"</b>. Чим ближче "хмара" точок до цієї лінії, тим вищою є якість моделі. Це дозволяє аудитору миттєво побачити викиди (Outliers) — випадки, де ШІ суттєво помилився, та проаналізувати умови, в яких це сталося.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Академічного Ядра (Thesis Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION generate_academic_plots(data_source):
    1. UNIFY: Ensure data is dictionary [v1, v2, v3]
    
    2. FIGURE_5 (Temporal):
           ADD_TRACE(actual_load, color=orange, width=3)
           FOR v IN models:
               ADD_TRACE(predicted_load[v], dash=dash)
               
    3. FIGURE_7 (Stats):
           FOR v IN models:
               err = actual - predicted
               mu, std = scipy.stats.norm.fit(err)
               ADD_HISTOGRAM(err, density=True)
               ADD_SCATTER(xr, normal_pdf(xr, mu, std))
               
    4. FIGURE_8 (Regression):
           ADD_IDEAL_LINE(y=x, opacity=0.2)
           FOR v IN models:
               ADD_SCATTER_MARKERS(actual, predicted, size=6)
               
    5. RETURN (fig5, fig7, fig8)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: MULTI-MODEL COMPARATIVE ANALYSIS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Багатомодельний порівняльний аналіз</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>academic.py</code> підтримує одночасне відображення результатів декількох версій LSTM моделей (v1, v2, v3). Це критично для розділу "Експериментальне порівняння" в дипломі. Кожна модель отримує свій унікальний колір з нашої академічної палітри (Pastel Red, Soft Blue, Light Purple), що дозволяє на одному графіку Figure 7 порівняти вузькість дзвона розподілу помилок для різних архітектур.</p>
    </div>
</div>

<!-- SECTION 08: THESIS-READY FORMATTING STANDARDS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Стандарти форматування для диплома</h2></div>
    <div class="glass-card flow-step">
        <p>Усі графіки автоматично отримують заголовки згідно з внутрішньою нумерацією диплома (Figure 5, 7, 8). Ми використовуємо <b>plotly_dark</b> як базовий шаблон, але з кастомними налаштуваннями відступів (Margin Fix), щоб графіки ідеально вписувалися в структуру сторінки при експорті в PNG/PDF. Легенда завжди виноситься в нижню частину (горизонтально), щоб не перекривати дані на вузьких екранах ноутбуків під час демонстрації.</p>
    </div>
</div>

<!-- SECTION 09: SCIENTIFIC COMPUTING INTEGRATION (SCIPY/NUMPY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Інтеграція з Scipy та Numpy (Наукове ядро)</h2></div>
    <div class="glass-card flow-step">
        <p>На відміну від звичайних UI-графіків, <code>academic.py</code> активно використовує <b>Numpy</b> для генерації діапазонів значень та <b>Scipy</b> для математичного моделювання. Це робить візуалізацію не просто картинкою, а результатом реальних наукових розрахунків. Кожен графік Figure 7 базується на апроксимації мільйонів точок даних, що гарантує високу доказову базу при відповідях на запитання екзаменаційної комісії.</p>
    </div>
</div>

<!-- SECTION 10: USER COGNITIVE LOAD & RESEARCH UX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Когнітивне навантаження та UX Дослідника</h2></div>
    <div class="glass-card flow-step">
        <p>Для зручності аналізу ми впровадили <b>Legend Grouping</b>. При натисканні на назву моделі в легенді на Figure 7, автоматично вимикається і її гістограма, і лінія нормального розподілу. Це дозволяє досліднику миттєво ізолювати результати конкретної нейромережі для детального вивчення, не втрачаючи контекст інших графіків, що значно прискорює процес валідації гіперпараметрів.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🧪</div>
            <div class="role-content">
                <h4>Scipy Stats</h4>
                <p>Математичне ядро для розрахунку нормального розподілу помилок.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🧮</div>
            <div class="role-content">
                <h4>NumPy Core</h4>
                <p>Векторні операції та генерація лінійних просторів для графіків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Plotly Graph Objects</h4>
                <p>Високоточний рендеринг академічних Scatter та Histogram об'єктів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (AUTOMATED THESIS EXPORT) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Automated Thesis Export)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Автоматичного експорту в LaTeX**. Система буде не просто показувати графіки, а генерувати готовий .tex код для вставки в диплом, включаючи автоматично згенерований опис результатів (наприклад: "Модель v2 показала на 15% вужчий розподіл помилок, ніж v1"). Також буде додано підтримку <b>Bland-Altman діаграм</b> для ще більш глибокого клінічного аналізу прогнозів.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Академічні Графіки</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому Figure 7 виглядає порожнім?</b> — Ймовірно, фактичні та прогнозовані дані ідентичні (помилка = 0). Перевірте вхідний датасет.</p>
        <p><b>Як змінити назву підстанції на графіку?</b> — Використовуйте параметр <code>substation_name</code> при виклику функції генерації у контролері.</p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
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
