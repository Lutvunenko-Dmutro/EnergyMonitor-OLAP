# Технічна специфікація модуля: ui/components/charts/ (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">VISUALIZATION ENGINE & ANALYTICS CHARTS FRAMEWORK</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📊</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Графічний Фреймворк ATLAS</h1>
            <p class="mega-subtitle">Уніфікована система візуалізації часових рядів: академічні графіки, Dual-Axis кореляції, ритми споживання та ШІ-прогнозні полотна</p>
            <div class="status-tags"><span class="tag tag-online">CHART ENGINE ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">VISUAL ARCHITECT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📉</div><div class="metric-info"><span class="metric-label">Logic</span><span class="metric-value">Dual-Axis Sync</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔮</div><div class="metric-info"><span class="metric-label">Forecast</span><span class="metric-value">Uncertainty Bands</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⏳</div><div class="metric-info"><span class="metric-label">Pulse</span><span class="metric-value">Rhythm Analysis</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎭</div><div class="metric-info"><span class="metric-label">Style</span><span class="metric-value">Academic Dark</span></div></div>
</div>

<!-- SECTION 01: VISUALIZATION ENGINE PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Графічного Фреймворку</h2></div>
    <div class="glass-card flow-step">
        <p>Директорія <code>ui/components/charts/</code> є "Художником" проекту ATLAS. В енергетиці графіки — це не просто ілюстрації, а інструменти прецизійного аналізу. Наш фреймворк забезпечує математичну точність відображення при збереженні високої естетики Cyber-HUD. Ми розділили візуалізацію на три спеціалізовані шари: <b>Base</b> (фундамент), <b>Academic</b> (глибока кореляція) та <b>Forecast</b> (візуалізація майбутнього), що дозволяє створювати складні багатовимірні полотна з нульовим дублюванням коду.</p>
    </div>
</div>

<!-- SECTION 02: CHART ORCHESTRATION ARCHITECTURE -->
<div class="section-container">
    <div class="section-header":"02</span><h2 class="section-title">Архітектура оркестрації графіків</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("DataFrame: Raw Metrics") --> BASE("base.py: Уніфікована стилізація")
    BASE --> ACAD("academic.py: Dual-Axis & Correlation")
    BASE --> FC("forecast_plots.py: AI Results")
    ACAD --> RHYTHM("Rhythm Analysis (Pulse)")
    FC --> BANDS("Confidence Bands (Uncertainty)")
    RHYTHM & BANDS --> UI("Final Analytic Canvas")
    </div></div>
</div>

<!-- SECTION 03: DUAL-AXIS CORRELATION ENGINE (ACADEMIC) -->
<div class="section-container">
    <div class="section-header":"03</span><h2 class="section-title">Двигун крос-параметричної кореляції (Academic)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>academic.py</code> реалізує професійний <b>Dual-Axis Engine</b> для виявлення прихованих залежностей:</p>
        <ul>
            <li><b>Синхронізація осей:</b> Можливість накладати Load (MW) та Temperature (°C) на одне часове поле з незалежним масштабуванням.</li>
            <li><b>Колірна диференціація:</b> Жорстка прив'язка кольорів (наприклад, помаранчевий для навантаження, блакитний для погоди) по всій системі.</li>
            <li><b>Interactive Hover:</b> Об'єднаний тултіп (Unified Hover) показує значення обох параметрів у точці часу, полегшуючи візуальний аудит.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: FORECAST VISUALIZATION & UNCERTAINTY BANDS -->
<div class="section-container">
    <div class="section-header":"04</span><h2 class="section-title">Візуалізація прогнозів та зон невизначеності</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>forecast_plots.py</code> перетворює ШІ-висновки на зрозумілі полотна:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Елемент</th>
                    <th>Метод рендерингу</th>
                    <th>Аналітичне значення</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>History Line</td><td>Solid Line (Grey/White)</td><td>Еталонний контекст минулого</td></tr>
                <tr><td>AI Prediction</td><td>Dashed/Solid Accent Line</td><td>Траєкторія ймовірного майбутнього</td></tr>
                <tr><td>Confidence Bands</td><td>Shaded Area (Toself fill)</td><td>Межі допустимої похибки (Risk Map)</td></tr>
                <tr><td>Multi-Model Overlay</td><td>Multi-color comparison</td><td>Порівняння V1/V2/V3 архітектур</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: RHYTHM ANALYSIS & ENERGY PULSE (⏳) -->
<div class="section-container">
    <div class="section-header":"05</span><h2 class="section-title">Аналіз енергетичних ритмів та пульсу</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>render_rhythm_chart</code> візуалізує "Серцебиття мережі". Вона використовує спеціальний метод агрегації DOW (Day of Week), розділяючи профілі на будні та вихідні. Це дозволяє оператору миттєво перевірити адекватність роботи моделей прогнозування сезонності та виявити аномальні відхилення від тижневого ритму.</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (CHART FACTORY LOGIC) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод логіки графічної фабрики</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_dual_axis(df, y1_col, y1_label, y2_col, y2_label):
    1. INITIALIZE go.Figure()
    2. ADD Trace_1 (Scatter): yaxis='y1', mode='lines', color=color1
    3. ADD Trace_2 (Scatter): yaxis='y2', mode='lines', color=color2
    4. CONFIGURE Layout:
           yaxis1: side='left', title=y1_label
           yaxis2: side='right', overlaying='y', title=y2_label
    5. APPLY Global_Atlas_Theme (Dark, Grid, Hover)
    6. RETURN figure
    
FUNCTION render_forecast_bands(df_hist, df_fc, bands_array):
    1. PLOT Historical Data
    2. PLOT Prediction Line
    3. FOR EACH band IN bands_array:
           ADD Shaded Area (toself) around Prediction
    4. RETURN unified_figure</code></pre>
    </div>
</div>

<!-- SECTION 07: GLOBAL ACADEMIC STYLING (THEME SYSTEM) -->
<div class="section-container">
    <div class="section-header":"07</span><h2 class="section-title">Система глобальної академічної стилізації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>base.py</code> містить "ДНК" дизайну ATLAS. Він автоматично ін'єктує налаштування <code>plotly_dark</code>, сітку (gridlines) з низькою яскравістю та кастомні шрифти у кожну фігуру. Це гарантує, що будь-який графік, створений у будь-якому модулі системи, буде виглядати як частина єдиного наукового звіту, готового до публікації.</p>
    </div>
</div>

<!-- SECTION 08: HIGH-PERFORMANCE SVG/WEBGL RENDERING -->
<div class="section-container">
    <div class="section-header":"08</span><h2 class="section-title">Високопродуктивний рендеринг (SVG vs WebGL)</h2></div>
    <div class="glass-card flow-step">
        <p>Фреймворк інтелектуально вибирає метод рендерингу. Для звичайних аналітичних графіків використовується прецизійний <b>SVG</b> (для максимальної чіткості ліній), а при роботі з великими масивами історичних даних (Archive Audit) система може перемикатися на <b>WebGL</b> (через <code>render_mode</code>), забезпечуючи плавність взаємодії навіть при десятках тисяч точок.</p>
    </div>
</div>

<!-- SECTION 09: INTERACTIVE RANGE SLIDERS & ZOOMING -->
<div class="section-container">
    <div class="section-header":"09</span><h2 class="section-title">Інтерактивні слайдери та керування зумом</h2></div>
    <div class="glass-card flow-step">
        <p>Всі аналітичні графіки підтримують <b>Range Sliders</b> на осі часу. Це дозволяє оператору бачити загальну картину за місяць, але одним рухом миші зумуватися на конкретну годину аварії. Стан зуму зберігається при зміні фільтрів, що критично для послідовного дослідження інцидентів.</p>
    </div>
</div>

<!-- SECTION 10: FAIL-SAFE DATA VALIDATION IN CHARTS -->
<div class="section-container">
    <div class="section-header":"10</span><h2 class="section-title">Відмовостійка валідація даних у графіках</h2></div>
    <div class="glass-card flow-step">
        <p>Перед рендерингом фреймворк перевіряє вхідні DataFrame на наявність <code>NaN</code> та <code>Infinity</code>. Замість "зламу" інтерфейсу, система автоматично фільтрує пошкоджені записи та додає інформаційну анотацію, що гарантує безперервність моніторингу навіть при збоях окремих датчиків.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Graph Objects</h4>
                <p>Низькорівневий двигун для побудови складних багатоосьових композицій.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Base Stylizer</h4>
                <p>Модуль <code>base.py</code>, що забезпечує візуальну цілісність бренду ATLAS.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛡️</div>
            <div class="role-content">
                <h4>UI Helpers</h4>
                <p>Забезпечує безпечний рендер через <code>safe_plotly_render</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (REAL-TIME STREAMING) -->
<div class="section-container">
    <div class="section-header":"12</span><h2 class="section-title">Дорожня карта v3.0 (Real-time Streaming & 3D Charts)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Real-time Data Streaming</b> (візуалізація без перезавантаження компонента), підтримка <b>3D-поверхневих графіків</b> для аналізу регіонального споживання та інтеграція <b>інструментів анотування</b> графіків безпосередньо оператором у UI.</p>
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
