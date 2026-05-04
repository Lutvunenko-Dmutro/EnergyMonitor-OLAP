# Технічна специфікація: Візуалізатор Академічної Звітності (ACADEMIC CHARTS GIGA-PASSPORT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ACADEMIC RESEARCH VISUALIZATION | THESIS-READY GRAPHICS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🎓</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Академічний Візуалізатор</h1>
            <p class="mega-subtitle">Система наукового обґрунтування результатів: статистичний аналіз похибок (Fig. 7), кореляційна регресія (Fig. 8) та багатомодельний трекінг динаміки (Fig. 5)</p>
            <div class="status-tags"><span class="tag tag-online">ACADEMIC MODE ACTIVE</span><span class="tag tag-version">v1.2.0</span><span class="tag tag-role">SCIENTIFIC VISUALIZER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📉</div><div class="metric-info"><span class="metric-label">Tracking</span><span class="metric-value">Temporal Load Dynamics</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Audit</span><span class="metric-value">Statistical Error PDF</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔵</div><div class="metric-info"><span class="metric-label">Regression</span><span class="metric-value">Scatter Correlation</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📑</div><div class="metric-info"><span class="metric-label">Thesis</span><span class="metric-value">Ready for Defense</span></div></div>
</div>

<!-- SECTION 01: ACADEMIC VISUALIZATION PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Академічної Візуалізації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>academic.py</code> є "Доказовою базою" проекту ATLAS. В академічному середовищі критично важливо не просто показати результат, а довести його статистичну достовірність. Візуалізатор реалізує суворий науковий стандарт відображення даних, орієнтований на публікацію в технічних журналах та захист магістерських/кандидатських дисертацій. Кожен графік (Figure 5, 7, 8) відповідає конкретним етапам доведення ефективності запропонованих методів глибокого навчання.</p>
    </div>
</div>

<!-- SECTION 02: RESEARCH VISUALIZATION PIPELINE -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Конвеєр наукової візуалізації</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("ML Evaluation Results (V1, V2, V3)") --> TREND("Fig 5: Temporal Dynamics & Tracking")
    DATA --> DIST("Fig 7: Statistical Error Analysis (PDF)")
    DATA --> SCATTER("Fig 8: Neural Regression Correlation")
    
    TREND --> THESIS("Academic Dissertation / Report")
    DIST --> THESIS
    SCATTER --> THESIS
    </div></div>
</div>

<!-- SECTION 03: FIGURE 5 - TEMPORAL LOAD DYNAMICS -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Figure 5: Темпоральна динаміка навантаження</h2></div>
    <div class="glass-card flow-step">
        <p>Цей графік демонструє здатність ШІ відстежувати реальні фізичні процеси у часі:</p>
        <ul>
            <li><b>Ground Truth (Orange):</b> Базовий рівень реального навантаження (товста лінія).</li>
            <li><b>Multi-Model Tracking:</b> Пунктирні лінії для різних ітерацій LSTM (V1, V2, V3).</li>
            <li><b>Visual Evidence:</b> Наочне доведення того, як кожна наступна версія моделі краще захоплює пікові навантаження та добову сезонність.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: FIGURE 7 - STATISTICAL ERROR ANALYSIS (📊) -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Figure 7: Статистичний аналіз похибок (PDF)</h2></div>
    <div class="glass-card flow-step">
        <p>Глибокий аудит розподілу помилок прогнозування:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Компонент</th>
                    <th>Реалізація</th>
                    <th>Наукове значення</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Histogram Overlay</td><td>Probability Density</td><td>Частотний аналіз промахів прогнозу</td></tr>
                <tr><td>Normal PDF Curve</td><td>Scipy Stats (Mu, Std)</td><td>Доведення нормальності розподілу помилок</td></tr>
                <tr><td>Multi-Model Comparison</td><td>Layered Density</td><td>Кількісне доведення стабільності ШІ</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: FIGURE 8 - NEURAL REGRESSION CORRELATION (🎯) -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Figure 8: Кореляційна діаграма регресії</h2></div>
    <div class="glass-card flow-step">
        <p>Діаграма розсіювання, що візуалізує якість регресійної моделі. Візуалізатор будує лінію ідеального прогнозу <code>y=x</code> та накладає фактичні "хмари" прогнозів. Концентрація точок навколо діагоналі є прямим візуальним доказом високого коефіцієнта детермінації (R2) та точності калібрування нейронної мережі на всьому діапазоні потужностей.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (ACADEMIC PLOT CORE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод ядра академічного візуалізатора</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION generate_academic_plots(data):
    1. CONVERT data to standardized dictionary (v1, v2, v3)
    
    2. CREATE Fig_5 (Trends):
           ADD Scatter(actual, color=Orange, width=3)
           FOR EACH model in results: ADD Scatter(predicted, style=Dash)
           SET title="Figure 5: Temporal Load Dynamics"
           
    3. CREATE Fig_7 (Distribution):
           FOR EACH model:
               err = actual - predicted
               ADD Histogram(opacity=0.2)
               ADD PDF_Curve(scipy.stats.norm.pdf(mu, std), width=4)
           SET title="Figure 7: Comparative Statistical Error Analysis"
           
    4. CREATE Fig_8 (Scatter):
           ADD Line(y=x, style=Dash, opacity=0.2)
           ADD Scatter(actual vs predicted, mode=markers, opacity=0.5)
           SET title="Figure 8: Neural Regression Correlation"
           
    5. RETURN (Fig_5, Fig_7, Fig_8)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: THESIS-READY FORMATTING STANDARDS -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Стандарти форматування для диплома</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль примусово встановлює заголовки згідно з нумерацією фігур у пояснювальній записці (наприклад, "Figure 7: ..."). Це дозволяє оператору просто зробити скріншот або експортувати графік, і він буде готовий до вставки в текстовий редактор без додаткового редагування підписів та легенд.</p>
    </div>
</div>

<!-- SECTION 08: COLOR PSYCHOLOGY & ACCESSIBILITY -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Колірна психологія та доступність</h2></div>
    <div class="glass-card flow-step">
        <p>Для різних версій моделей обрано контрастні кольори (v1: Purple, v2: Blue, v3: Red). Це дозволяє чітко розрізняти лінії навіть при чорно-білому друці за рахунок різної інтенсивності каналів та використання різних типів ліній (суцільна/пунктирна), що є стандартом для наукових публікацій.</p>
    </div>
</div>

<!-- SECTION 09: STATISTICAL KERNEL DENSITY ESTIMATION (KDE) -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Статистична оцінка щільності ядра (KDE)</h2></div>
    <div class="glass-card flow-step">
        <p>Замість простої гістограми, візуалізатор будує апроксимацію розподілу через <b>Нормальну PDF</b>. Це дозволяє науково оцінити стабільність моделі: чим "вужчий" та "вищий" пік розподілу навколо нуля, тим менша дисперсія помилки і тим надійніша модель з точки зору математичної статистики.</p>
    </div>
</div>

<!-- SECTION 10: AUTOMATED LEGEND & MARGIN TUNING -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Автоматичне управління легендами та полями</h2></div>
    <div class="glass-card flow-step">
        <p>Використання <code>legendgroup</code> гарантує синхронізацію легенд між гістограмою та лінією розподілу (Fig 7). Поля (margins) налаштовані так, щоб графік займав максимум корисного простору, що важливо при двоколонковій верстці академічних статей або слайдів презентацій.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Objects</h4>
                <p>Низькорівневий API для побудови складних наукових діаграм.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🧬</div>
            <div class="role-content">
                <h4>Scipy Stats</h4>
                <p>Математичне ядро для розрахунку параметрів нормального розподілу.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🐼</div>
            <div class="role-content">
                <h4>Pandas Core</h4>
                <p>Обробка та підготовка агрегованих результатів ML-моделей.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v2.0 (PDF AUTO-GENERATOR) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v2.0 (PDF Auto-Generator)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 2.0 планується впровадження <b>автоматичного експорту в LaTeX</b>, підтримка <b>Violin Plots</b> для аналізу сезонних помилок та інтеграція з <b>Statsmodels</b> для автоматичного виведення таблиць статистичної значущості (p-values) безпосередньо під графіками.</p>
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
