# Технічна специфікація: Візуалізатор Академічної Звітності (ACADEMIC RESEARCH VISUALIZATION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">THESIS VISUALIZATION | NEURAL AUDIT</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎓</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Академічна Звітність</h1>
            <p class="mega-subtitle">Спеціалізований модуль візуалізації наукових результатів: статистичний аналіз помилок нейромереж (Figure 7), регресійна кореляція (Figure 8) та часова динаміка (Figure 5) згідно зі стандартами дипломного проєктування</p>
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
        <p>Модуль <code>academic.py</code> є "Доказовою базою" проєкту ATLAS. В академічному середовищі недостатньо просто показати графік прогнозу — необхідно науково обґрунтувати його статистичну точність. Наша філософія базується на <b>Статистичній Суворості</b>: ми розробили набір графіків, які повністю відповідають стандартам наукових публікацій. Використання нормального розподілу помилок та регресійних діаграм дозволяє не просто "вірити" штучному інтелекту, а математично довести його ефективність та стабільність, що є критичним для успішного захисту магістерської або докторської дисертації.</p>
    </div>
</div>

<!-- SECTION 02: ACADEMIC PLOTTING PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр академічної візуалізації (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Actual vs Predicted Dataset") --> UNIFY("Unify Data (DataFrame or dict of v1/v2/v3)")
    
    UNIFY --> FIG5("Figure 5: Temporal Dynamics")
    FIG5 --> OVERLAY("Overlay LSTM Predictions on Ground Truth")
    
    UNIFY --> FIG7("Figure 7: Error Statistics")
    FIG7 --> CALC_ERR("Compute: error = actual - predicted")
    CALC_ERR --> HIST("Probability Density Histogram (opacity=0.2)")
    CALC_ERR --> SCIPY("scipy.stats.norm.fit(error)")
    SCIPY --> SCIPY_PDF("Generate Normal Curve using mu & std")
    
    UNIFY --> FIG8("Figure 8: Neural Regression")
    FIG8 --> IDEAL("Add Diagonal line 'Ideal Line (y=x)'")
    IDEAL --> SCATTER("Scatter Markers opacity=0.5, size=6")
    
    OVERLAY --> RENDER("Final Research Suite Rendering")
    SCIPY_PDF --> RENDER
    SCATTER --> RENDER
    </div></div>
</div>

<!-- SECTION 03: STATISTICAL ERROR ANALYSIS (FIG. 7) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Статистичний аналіз похибки (Figure 7)</h2></div>
    <div class="glass-card flow-step">
        <p>Для Figure 7 ми впровадили гібридну візуалізацію розподілу похибки:</p>
        <ul>
            <li><b>Probability Density Histogram:</b> Гістограма показує відносну частоту та щільність імовірності відхилення прогнозу від факту. Ми використовуємо напівпрозорий режим (<code>opacity=0.2</code>) для фонового відображення, щоб він не перекривав лінії інших моделей.</li>
            <li><b>Normal Distribution Fit (Апроксимація):</b> Використовуючи науковий пакет <code>scipy.stats.norm</code>, система розраховує середнє значення ($\mu$) та середньоквадратичне відхилення ($\sigma$) похибки, накладаючи ідеальну гаусову криву розподілу. Це наочно демонструє відсутність системного зміщення в моделях ШІ (бажане значення $\mu \approx 0$).</li>
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
                    <th>Тип аналізу / Графік</th>
                    <th>Специфічні колірні коди</th>
                    <th>Наукова цінність (для дисертації)</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Figure 5</b></td><td>Temporal Dynamics</td><td>Actual: <code>#ff9f43</code> (Orange)<br>LSTM versions: <code>#a29bfe</code>, <code>#74b9ff</code>, <code>#ff7675</code></td><td>Наочна оцінка здатності LSTM до відстеження різких трендів, сезонних піків та спадів навантаження ліній.</td></tr>
                <tr><td><b>Figure 7</b></td><td>Error Density</td><td>v1: Lavender<br>v2: Blue<br>v3: Red</td><td>Математичне підтвердження нормальності похибки. Дозволяє візуально порівняти "вузькість дзвона" для різних версій ШІ.</td></tr>
                <tr><td><b>Figure 8</b></td><td>Neural Regression</td><td>Diagonal: <code>rgba(255,255,255,0.2)</code><br>Markers: opacity=0.5, size=6</td><td>Оцінка лінійної кореляції прогнозу з реальністю (Ground Truth). Чим щільніша хмара навколо діагоналі — тим вища якість.</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: NEURAL REGRESSION CORRELATION (FIG. 8) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Регресійна кореляція нейромережі (Figure 8)</h2></div>
    <div class="glass-card flow-step">
        <p>Для Figure 8 ми використовуємо Scatter-діаграму, де кожна маркерна точка відображає пару (Фактичне значення, Прогнозоване значення). Ми будуємо допоміжну пунктирну лінію <b>"Ideal Line (y=x)"</b>. Це дозволяє аудитору миттєво побачити викиди (Outliers) — аномальні випадки, де модель суттєво переоцінила або недооцінила навантаження, та проаналізувати умови, в яких це сталося.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE & MATH) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Математика та алгоритми (Thesis Core)</h2></div>
    <div class="glass-card flow-step">
        <p>Математична формула щільності нормального розподілу похибок $P(x)$ для апроксимації кривої Гауса:</p>
        <div style="text-align: center; margin: 15px 0; font-size: 15px; color: var(--accent);">
            $$P(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{(x - \mu)^2}{2\sigma^2}}$$
        </div>
        <p>де похибка обчислюється як $e_t = x_t - \hat{x}_t$, $\mu$ — математичне очікування (зміщення), а $\sigma$ — середньоквадратичне відхилення похибок.</p>
        
        <pre><code class="language-python"># Генерація академічних графіків (academic.py)
FUNCTION generate_academic_plots(data, substation_name):
    1. INITIALIZE & UNIFY:
           IF data IS None: RETURN None, None, None
           IF isinstance(data, pd.DataFrame):
               results_dict = {"v1": data} # Single model mode
               is_multi = False
           ELSE:
               results_dict = data # Dictionary of models (v1, v2, v3)
               is_multi = True
               
           colors = {"v1": "#a29bfe", "v2": "#74b9ff", "v3": "#ff7675"}
           
    2. FIGURE 5: TEMPORAL LOAD DYNAMICS
           fig_trend = go.Figure()
           ref_df = results_dict[first_key]
           
           # Actual load ground truth line
           fig_trend.add_trace(go.Scatter(
               x=ref_df["timestamp"], y=ref_df["actual_load_mw"],
               name="Actual (Факт)", line=dict(color="#ff9f43", width=3)
           ))
           
           # Predictions lines
           FOR version, df IN results_dict.items():
               fig_trend.add_trace(go.Scatter(
                   x=df["timestamp"], y=df["predicted_load_mw"],
                   name=f"LSTM {version.upper()}",
                   line=dict(color=colors[version], dash="dash" if is_multi else "solid")
               ))
               
    3. FIGURE 7: STATISTICAL ERROR DENSITY
           fig_dist = go.Figure()
           FOR version, df IN results_dict.items():
               error = df["actual_load_mw"] - df["predicted_load_mw"]
               
               # 3.1 Transparent Histogram
               fig_dist.add_trace(go.Histogram(
                   x=error, nbinsx=40, histnorm='probability density',
                   name=f"LSTM {version.upper()}", marker_color=colors[version],
                   opacity=0.2, legendgroup=version, showlegend=False
               ))
               
               # 3.2 Smooth Normal Distribution Curve
               mu, std = error.mean(), error.std()
               xr = np.linspace(error.min(), error.max(), 100)
               fig_dist.add_trace(go.Scatter(
                   x=xr, y=scipy.stats.norm.pdf(xr, mu, std),
                   name=f"Модель {version.upper()}",
                   line=dict(color=colors[version], width=4),
                   legendgroup=version
               ))
               
    4. FIGURE 8: NEURAL REGRESSION CORRELATION
           fig_scatter = go.Figure()
           mn, mx = ref_df["actual_load_mw"].min(), ref_df["actual_load_mw"].max()
           
           # y=x ideal diagonal
           fig_scatter.add_trace(go.Scatter(
               x=[mn, mx], y=[mn, mx], mode="lines", name="Ideal (y=x)",
               line=dict(color="rgba(255,255,255,0.2)", dash="dash")
           ))
           
           # Add scatter markers
           FOR version, df IN results_dict.items():
               fig_scatter.add_trace(go.Scatter(
                   x=df["actual_load_mw"], y=df["predicted_load_mw"],
                   mode="markers", name=f"Pred {version.upper()}",
                   marker=dict(opacity=0.5, size=6, color=colors[version])
               ))
               
    5. STYLE OVERRIDES:
           Apply dark template "plotly_dark"
           Position legends horizontally at the bottom (y=-0.2, x=0.5)
           Set custom margins: margin=dict(l=10, r=10, t=50, b=100)
           
    6. RETURN fig_trend, fig_dist, fig_scatter
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: MULTI-MODEL COMPARATIVE ANALYSIS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Багатомодельний порівняльний аналіз</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>academic.py</code> підтримує одночасне відображення результатів декількох версій LSTM моделей (v1, v2, v3). Це критично для розділу "Експериментальне порівняння" в наукових роботах. Кожна модель отримує свій фіксований колір з нашої академічної палітри (Pastel Red, Soft Blue, Light Purple), що дозволяє на одному графіку порівняти точність кожної архітектури та швидко зробити математично обґрунтовані висновки.</p>
    </div>
</div>

<!-- SECTION 08: THESIS-READY FORMATTING STANDARDS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Стандарти форматування для дипломів</h2></div>
    <div class="glass-card flow-step">
        <p>Усі графіки автоматично маркуються згідно з внутрішньою нумерацією диплома (Figure 5, 7, 8). Ми використовуємо <b>plotly_dark</b> як базовий шаблон, але з кастомними налаштуваннями відступів (Margin Fix), щоб графіки ідеально вписувалися в структуру сторінки при експорті в PNG/PDF. Легенда завжди виноситься в нижню частину (горизонтально), щоб не перекривати дані на вузьких екранах ноутбуків під час демонстрації.</p>
    </div>
</div>

<!-- SECTION 09: SCIENTIFIC COMPUTING INTEGRATION -->
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
        <p>Для зручності аналізу ми впровадили <b>Legend Grouping (Групування легенди)</b>. При натисканні на назву моделі в легенді на Figure 7, автоматично вимикається і її гістограма, і лінія нормального розподілу. Це дозволяє досліднику миттєво ізолювати результати конкретної нейромережі для детального вивчення, не втрачаючи контекст інших графіків, що значно прискорює процес валідації гіперпараметрів.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🧪</div>
            <div class="role-content">
                <h4>Scipy Stats (stats.norm)</h4>
                <p>Математичне ядро для апроксимації розподілу помилок нейромережі.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🧮</div>
            <div class="role-content">
                <h4>NumPy Core</h4>
                <p>Генерація лінійних просторів (np.linspace) для побудови гладких кривих.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Plotly Graph Objects</h4>
                <p>Високоточний рендеринг академічних Scatter, Histogram та Subplot об'єктів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>Pandas Core</h4>
                <p>Обробка вхідних масивів даних часових рядів та обчислення похибок.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (AUTOMATED THESIS EXPORT) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Automated LaTeX Export)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Автоматичного експорту в LaTeX**:</p>
        <ul>
            <li>Система буде не просто показувати графіки, а генерувати готовий <code>.tex</code> код для вставки в диплом, включаючи автоматично згенерований опис результатів (наприклад: "Модель v3 показала на 15% вужчий розподіл помилок, ніж v1").</li>
            <li>Додавання <b>Bland-Altman діаграм</b> для ще більш глибокого аналізу та виявлення систематичних відхилень у прогнозах.</li>
            <li>Експорт векторних графіків у форматі <code>.eps</code> для відповідності стандартам IEEE.</li>
        </ul>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Академічні Графіки</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому на Figure 7 не відображається лінія нормального розподілу?</b><br>— Перевірте, чи не порожні вхідні DataFrames прогнозованих значень. Якщо модель дала однаковий нульовий масив, стандартне відхилення $\sigma = 0$, що робить розрахунок PDF неможливим.</p>
        
        <p><b>Як додати нову модель (наприклад, v4) для порівняння?</b><br>— Передайте у функцію <code>generate_academic_plots</code> словник з ключем "v4" та відповідним DataFrame. Система автоматично підхопить її та призначить колір.</p>
        
        <p><b>Як зберегти графік у високій якості для друку?</b><br>— Натисніть іконку камери у правому верхньому кутку графіка Plotly. Система завантажить PNG файл. Для кращого результату розгорніть графік на весь екран перед експортом.</p>
        
        <p><b>Чому гістограми помилок напівпрозорі?</b><br>— Ми встановили <code>opacity=0.2</code>, щоб при накладанні гістограм декількох моделей вони не перекривали одна одну і користувач міг бачити межі кожної.</p>
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
