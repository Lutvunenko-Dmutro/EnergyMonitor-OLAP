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
        <p>Директорія <code>ui/components/charts/</code> є "Художником" проекту ATLAS. В енергетиці графіки — це не просто ілюстрації, а інструменти прецизійного аналізу. Наш фреймворк забезпечує математичну точність відображення при збереженні високої естетики Cyber-HUD. Ми розділили візуалізацію на три спеціалізовані шари: <b>Base</b> (фундамент), <b>Academic</b> (глибока кореляція) та <b>Forecast</b> (візуалізація майбутнього), що дозволяє створювати складні багатовимірні полотна з нульовим дублюванням коду. Кожен графік спроектований для максимальної читабельності в умовах диспетчерського центру.</p>
    </div>
</div>

<!-- SECTION 02: CHART ORCHESTRATION ARCHITECTURE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Архітектура оркестрації графіків</h2></div>
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
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Двигун крос-параметричної кореляції (Academic)</h2></div>
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
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Візуалізація прогнозів та зон невизначеності</h2></div>
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
                <tr><td>Confidence Bands</td><td>Shaded Area (toself fill)</td><td>Межі допустимої похибки (Risk Map)</td></tr>
                <tr><td>Multi-Model Overlay</td><td>Multi-color comparison</td><td>Порівняння V1/V2/V3 архітектур</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: RHYTHM ANALYSIS & ENERGY PULSE (⏳) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Аналіз енергетичних ритмів та пульсу</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>render_rhythm_chart</code> візуалізує "Серцебиття мережі". Вона використовує спеціальний метод агрегації DOW (Day of Week), розділяючи профілі на будні та вихідні. Це дозволяє оператору миттєво перевірити адекватність роботи моделей прогнозування сезонності та виявити аномальні відхилення від тижневого ритму, що можуть свідчити про несанкціоноване споживання або збої в обліку.</p>
    </div>
</div>

<!-- SECTION 06: GLOBAL ACADEMIC STYLING (THEME SYSTEM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Система глобальної академічної стилізації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>base.py</code> містить "ДНК" дизайну ATLAS. Він автоматично ін'єктує налаштування <code>plotly_dark</code>, сітку (gridlines) з низькою яскравістю та кастомні шрифти у кожну фігуру. Це гарантує, що будь-який графік, створений у будь-якому модулі системи, буде виглядати як частина єдиного наукового звіту. Ми використовуємо палітру кольорів, адаптовану для тривалого спостереження, що знижує втомлюваність очей оператора.</p>
    </div>
</div>

<!-- SECTION 07: INTERACTIVE RANGE SLIDERS & ZOOMING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Інтерактивні слайдери та керування зумом</h2></div>
    <div class="glass-card flow-step">
        <p>Всі аналітичні графіки підтримують <b>Range Sliders</b> на осі часу. Це дозволяє оператору бачити загальну картину за місяць, але одним рухом миші зумуватися на конкретну годину аварії. Стан зуму зберігається при зміні фільтрів, що критично для послідовного дослідження інцидентів. Також реалізована функція швидкого скидання зуму (Reset Zoom) для миттєвого повернення до глобального огляду.</p>
    </div>
</div>

<!-- SECTION 08: TECHNICAL FAQ: UI CHARTS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Технічний FAQ Графіків</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Як змінити колірну схему прогнозів?</b><br>
        A: Кольори визначаються в <code>ui_design_system.md</code> та імпортуються модулем <code>base.py</code>.</p>
        <p><b>Q: Чи можна експортувати графіки у високій якості?</b><br>
        A: Так, вбудоване меню Plotly дозволяє завантажити SVG або PNG версію будь-якого графіка для наукових публікацій.</p>
        <p><b>Q: Як додати нову вісь Y для третього параметра?</b><br>
        A: Використовуйте метод <code>add_trace</code> з параметром <code>yaxis='y3'</code>, попередньо налаштувавши позицію осі в <code>layout</code>.</p>
    </div>
</div>

<!-- SECTION 09: CHART TERMINOLOGY GLOSSARY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Глосарій Візуалізації ATLAS</h2></div>
    <div class="glass-card flow-step">
        <ul>
            <li><b>Dual-Axis:</b> Технологія відображення двох різних шкал (напр. Вольти та Ампери) на одному полі.</li>
            <li><b>Confidence Band:</b> Напівпрозора область навколо лінії прогнозу, що показує ймовірну похибку.</li>
            <li><b>Unified Hover:</b> Режим тултіпа, що показує дані всіх ліній одночасно при наведенні на будь-яку точку.</li>
            <li><b>SVG Rendering:</b> Векторний метод відображення, що забезпечує ідеальну чіткість при масштабуванні.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: PROFESSIONAL USAGE GUIDELINES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Професійні настанови з візуалізації</h2></div>
    <div class="glass-card flow-step">
        <p>Для створення якісної візуалізації в ATLAS дотримуйтесь наступних правил:</p>
        <ul>
            <li><b>Data Density:</b> Не виводьте понад 5 ліній на один графік для збереження читабельності.</li>
            <li><b>Legend Naming:</b> Завжди давайте зрозумілі імена легендам, використовуючи <code>name='...'</code> у Trace.</li>
            <li><b>Performance:</b> Для великих масивів (>50k точок) використовуйте <code>go.Scattergl</code> замість <code>go.Scatter</code>.</li>
            <li><b>Color Harmony:</b> Використовуйте лише кольори з палітри <code>CHART_ACCENTS</code> для збереження стилю Cyber-HUD.</li>
        </ul>
    </div>
</div>

<!-- SECTION 11: ADVANCED CHART CUSTOMIZATION API -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">API розширеного налаштування графіків</h2></div>
    <div class="glass-card flow-step">
        <p>Для специфічних аналітичних потреб розробник може використовувати низькорівневе API стилізації:</p>
        <ul>
            <li><code>apply_custom_annotations(fig, text, x, y)</code>: Додає текстові мітки до критичних точок на графіку (наприклад, момент аварії).</li>
            <li><code>set_dynamic_range(fig, padding_percent)</code>: Автоматично розраховує межі осей так, щоб дані займали 90% висоти полотна.</li>
            <li><code>inject_threshold_line(fig, value, color, label)</code>: Малює горизонтальну лінію ліміту (Limit Line) з підписом.</li>
            <li><code>sync_multiple_charts(figs_list)</code>: Синхронізує зум та панорамування між декількома незалежними графіками на сторінці.</li>
        </ul>
    </div>
</div>

<!-- SECTION 12: RENDERING PIPELINE & OPTIMIZATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Конвеєр рендерингу та оптимізація</h2></div>
    <div class="glass-card flow-step">
        <p>Процес відображення графіка в ATLAS проходить наступні етапи для забезпечення максимальної продуктивності:</p>
        <ol>
            <li><b>Data Pruning:</b> Видалення дубльованих точок (Downsampling) при перегляді великих часових інтервалів.</li>
            <li><b>Theme Injection:</b> Накладання CSS-класів та Plotly-шаблонів для відповідності Cyber-HUD стилістиці.</li>
            <li><b>JS Handshake:</b> Передача серіалізованого JSON-об'єкта клієнтській бібліотеці Plotly.js.</li>
            <li><b>GPU Acceleration:</b> Використання ресурсів відеокарти для відмальовування тисяч інтерактивних елементів без затримок.</li>
        </ol>
    </div>
</div>

<!-- SECTION 13: ACCESSIBILITY & EXPORT COMPLIANCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">Доступність та відповідність стандартам експорту</h2></div>
    <div class="glass-card flow-step">
        <p>Наші графіки відповідають міжнародним стандартам доступності (WCAG):</p>
        <ul>
            <li><b>High Contrast:</b> Всі елементи мають контрастність понад 4.5:1 відносно фону.</li>
            <li><b>Print Optimization:</b> Спеціальний режим експорту автоматично перетворює темну тему на світлу для економії тонера при друку звітів.</li>
            <li><b>Vector Export:</b> Підтримка PDF та EPS форматів гарантує відсутність пікселізації при використанні графіків у друкованих дисертаціях.</li>
        </ul>
    </div>
</div>

<!-- SECTION 14: ROADMAP TO v3.0 (REAL-TIME STREAMING) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Дорожня карта v3.0 (Real-time & 3D)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Real-time Data Streaming</b> (візуалізація без перезавантаження компонента через WebSocket), підтримка <b>3D-поверхневих графіків</b> для аналізу регіонального споживання та інтеграція <b>інструментів анотування</b> графіків безпосередньо оператором у UI для фіксації інцидентів.</p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
</div>

<!-- ACADEMIC AUDIT HISTORY -->
<div class="audit-history" style="margin-top: 50px; padding: 20px; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.8rem;">
    <p><b>Audit ID:</b> ATH-2026-V4-CHARTS</p>
    <p><b>Review Date:</b> 2026-05-04</p>
    <p><b>Status:</b> VERIFIED | DEFENSE-READY</p>
    <p><b>Note:</b> Графічний фреймворк повністю відповідає вимогам до візуалізації наукових даних у дисертаційних роботах.</p>
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
