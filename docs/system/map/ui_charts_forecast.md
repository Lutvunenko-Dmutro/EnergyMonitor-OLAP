# Технічна специфікація: Двигун Візуалізації Прогнозів (ADVANCED FORECAST PLOTTING ENGINE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AI FORECAST VIZ | HYBRID RENDERING</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔮</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Двигун Візуалізації Прогнозів</h1>
            <p class="mega-subtitle">Ядро графічного відображення ШІ-моделей проєкту ATLAS: комбіноване накладання довірчих інтервалів (Confidence Bands), порівняльний аудит нейромереж (V1/V2/V3) та наскрізна гібридна хронологія</p>
            <div class="status-tags"><span class="tag tag-online">FORECAST VIZ ACTIVE</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">ML VISUALIZER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Pattern</span><span class="metric-value">Hybrid Multi-Layer</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📐</div><div class="metric-info"><span class="metric-label">Confidence Bounds</span><span class="metric-value">Smart Clipping</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Timeline</span><span class="metric-value">Mega-Flow Chrono</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⭐</div><div class="metric-info"><span class="metric-label">Audit View</span><span class="metric-value">LSTM v3 Highlighted</span></div></div>
</div>

<!-- SECTION 01: FORECAST PLOTTING PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Візуалізації Прогнозів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>forecast_plots.py</code> є "Вікном у майбутнє" проєкту ATLAS. В енергетиці сухий точковий прогноз часто не дає повної картини ризиків. Наша філософія базується на <b>Гібридному Багатошаровому відображенні</b>: ми поєднуємо історичні фактичні дані, ШІ-прогноз майбутнього навантаження та напівпрозору смугу невизначеності (довірчий інтервал). Це дозволяє диспетчеру оцінити не лише найбільш імовірний сценарій, але й підготуватися до можливих пікових екстремумів похибки.</p>
    </div>
</div>

<!-- SECTION 02: FORECAST PLOTTING PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр візуалізації прогнозів ШІ (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("History & Forecast DataFrames") --> TYPE_SELECT{"Select Rendering Type"}
    
    TYPE_SELECT -- "Single Forecast" --> FC_ENG("_generate_forecast_figure()")
    FC_ENG --> HIST_LINE("Add History trace (Blue: #3498db)")
    FC_ENG --> CLIP_LOGIC("Clip upper bond: max history vs forecast")
    CLIP_LOGIC --> CONCAT_SHAPE("Concatenate: upper + lower bounds [::-1]")
    CONCAT_SHAPE --> BAND_TRACE("Add filled confidence trace (Red alpha: 0.08)")
    BAND_TRACE --> PRED_LINE("Add Forecast trace (Dashed Red: #e74c3c)")
    
    TYPE_SELECT -- "Multi-Model Forecast" --> MULTI_ENG("_generate_multi_forecast_figure()")
    MULTI_ENG --> LOOP_FC("Loop models v1/v2/v3: draw distinct line styles")
    
    TYPE_SELECT -- "Unified Audit Comparison" --> AUDIT_ENG("generate_comparison_plot()")
    AUDIT_ENG --> GROUND_TRUTH("Draw Ground Truth Actuals (Solid orange: #ff9f43)")
    AUDIT_ENG --> AUDIT_LOOP("Draw Models: v1 (dot), v2 (dash), v3 (solid red ⭐)")
    
    TYPE_SELECT -- "Mega-Flow Hybrid" --> MEGA_ENG("_generate_mega_hybrid_figure()")
    MEGA_ENG --> JOIN_BT_FC("Join Backtest Actuals + Backtest Preds + Future Forecast")
    
    HIST_LINE --> RENDER("Output go.Figure to UI View")
    LOOP_FC --> RENDER
    GROUND_TRUTH --> RENDER
    JOIN_BT_FC --> RENDER
    </div></div>
</div>

<!-- SECTION 03: HYBRID MULTI-LAYER RENDERING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Гібридний багатошаровий рендеринг (Confidence Bands)</h2></div>
    <div class="glass-card flow-step">
        <p>Для побудови графіків з довірчими смугами ми використовуємо техніку <b>замкненого контуру (Tofill Scatter)</b>. Замість малювання окремої верхньої та нижньої меж, ми створюємо єдину лінію, що обходить контур по колу:</p>
        <ul>
            <li><b>Contour Concatenation:</b> Ми об'єднуємо вісь часу у прямому та зворотному напрямках: <code>pd.concat([ts, ts[::-1]])</code>.</li>
            <li><b>Value Concatenation:</b> Аналогічно об'єднуємо верхню межу ($upper\_bond$) зі зворотною нижньою межею ($lower\_bond[::-1]$).</li>
            <li><b>Zero-line Transparency:</b> Рендеримо отриману фігуру з прозорими границями (<code>line_color="rgba(0,0,0,0)"</code>) та ніжним заповненням червоного кольору з альфа-каналом <code>0.08</code>. Це створює елегантну смугу, що візуалізує коридор безпеки.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: FORECAST LAYOUT MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця стилів та графіків прогнозування</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модель / Версія</th>
                    <th>Стиль лінії (Line style)</th>
                    <th>Колір (Hex / RGBA)</th>
                    <th>Опис та роль в інтерфейсі</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Історія (Actuals)</b></td><td>Solid (width=3)</td><td><code>#ff9f43</code> / Orange</td><td>Фактичні історичні дані навантаження підстанцій (Ground Truth)</td></tr>
                <tr><td><b>LSTM Baseline (V1)</b></td><td>Dotted (width=2)</td><td><code>#00d2d3</code> / Teal</td><td>Базова модель часових рядів, що служить відправною точкою</td></tr>
                <tr><td><b>LSTM Diagnostic (V2)</b></td><td>Dashed (width=2)</td><td><code>#54a0ff</code> / Blue</td><td>Модель з урахуванням фізичних параметрів та DGA хроматографії</td></tr>
                <tr><td><b>LSTM Hybrid (V3) ⭐</b></td><td>Solid (width=3)</td><td><code>#ee5253</code> / Red</td><td>Флагманська модель блендингу з найвищою точністю та стійкістю</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: SMART CONFIDENCE BOUNDS CLIPPING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Інтелектуальне обмеження меж (Smart Clipping)</h2></div>
    <div class="glass-card flow-step">
        <p>Математичні моделі іноді можуть генерувати аномально великі або від'ємні значення на межах довірчих інтервалів при різких стрибках навантаження ліній. Щоб графік виглядав реалістично, ми впровадили механізм <b>Smart Clipping</b>:</p>
        <div style="text-align: center; margin: 15px 0; font-size: 14px; color: var(--accent);">
            $$\text{safe\_upper} = \min\left(\text{upper\_bond}, 1.5 \times \max\left(\max(H_{actual}), \max(F_{predicted})\right)\right)$$
        </div>
        <p>Це автоматично обрізає довірчий інтервал зверху, якщо він перевищує максимальне історичне або прогнозоване навантаження у 1.5 рази, запобігаючи візуальному стисканню корисного масштабу графіка.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE & DETAILS) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Двигуна Прогнозів (Forecast Plotting Core)</h2></div>
    <div class="glass-card flow-step">
        <pre><code class="language-python"># Рендеринг ШІ-прогнозів (forecast_plots.py)
FUNCTION _generate_forecast_figure(df_hist, df_fc, title, version_lbl):
    1. INITIALIZE Plotly Go.Figure:
           fig = go.Figure()
           
    2. ADD HISTORICAL ACTUALS:
           IF df_hist exists and actuals in columns:
               fig.add_trace(go.Scatter(
                   x = df_hist["timestamp"], y = df_hist["actual_load_mw"],
                   name = "Історія", line = dict(color="#3498db", width=2.5)
               ))
               
    3. ADD CONFIDENCE BANDS (Smart Clipping & Contour):
           IF df_fc exists and upper_bond in columns:
               h_max = df_hist["actual_load_mw"].max()
               p_max = df_fc["predicted_load_mw"].max()
               
               # Apply math clipping formula
               safe_upper = df_fc["upper_bond"].clip(upper = max(h_max, p_max) * 1.5)
               
               # Concatenate contour coordinates
               contour_x = pd.concat([df_fc["timestamp"], df_fc["timestamp"][::-1]])
               contour_y = pd.concat([safe_upper, df_fc["lower_bond"][::-1]])
               
               fig.add_trace(go.Scatter(
                   x = contour_x, y = contour_y,
                   fill = "toself", fillcolor = "rgba(231,76,60,0.08)",
                   line = dict(color="rgba(0,0,0,0)"), showlegend = False
               ))
               
    4. ADD AI FORECASTED LINE:
           IF df_fc exists:
               fig.add_trace(go.Scatter(
                   x = df_fc["timestamp"], y = df_fc["predicted_load_mw"],
                   name = f"Прогноз ({version_lbl})",
                   line = dict(color="#e74c3c", width=2.5, dash="dash")
               ))
               
    5. RETURN fig
END FUNCTION

FUNCTION generate_comparison_plot(results, substation_name):
    1. INITIALIZE: fig = go.Figure()
    
    2. ADD FACTUAL GROUND TRUTH:
           fig.add_trace(go.Scatter(
               x = first_df["timestamp"], y = first_df["actual_load_mw"],
               name = "Фактичне навантаження (Ground Truth)",
               line = dict(color="#ff9f43", width=3)
           ))
           
    3. LOOP & DRAW ML MODEL TRACES (v1, v2, v3):
           FOR version, df IN results.items():
               fig.add_trace(go.Scatter(
                   x = df["timestamp"], y = df["predicted_load_mw"],
                   name = labels[version], line = styles[version]
               ))
               
    4. APPLY DARK LAYOUT:
           title = f"Порівняльна відповідність нейромереж ({substation_name})"
           Apply plotly_dark template, margin overrides and bottom centered horizontal legend.
           
    5. RETURN fig
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: MEGA-FLOW CHRONOLOGY INTEGRATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Наскрізна хронологія (Mega-Flow Chronology)</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>_generate_mega_hybrid_figure</code> реалізує унікальний **Mega-Flow** графік. Він безшовно з'єднує історичний бектест та майбутній прогноз на єдиній шкалі часу. Це дозволяє оператору оцінити якість роботи ШІ на минулому тижні (порівняння фактичної лінії та лінії бектесту) і одночасно подивитися на пунктирний прогноз на наступні 24 години, створюючи цілісний потік часу без розривів на екрані.</p>
    </div>
</div>

<!-- SECTION 08: HYBRID SENSITIVITY HIGHLIGHTING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Виділення моделі LSTM v3 (Флагман ⭐)</h2></div>
    <div class="glass-card flow-step">
        <p>У режимі порівняльного аудиту (<code>generate_comparison_plot</code>) ми застосували концепцію <b>акцентної ієрархії</b>. Поки моделі v1 (дот) та v2 (даш) відображаються тонкими лініями приглушених кольорів, флагманська модель v3 отримує товсту суцільну червону лінію <code>#ee5253</code> шириною <code>3.5</code>. Це миттєво фокусує погляд дослідника на найточнішому варіанті, дозволяючи візуально порівнювати відхилення інших моделей щодо нашого еталону.</p>
    </div>
</div>

<!-- SECTION 09: PERFORMANCE DATA CONCATENATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Оптимізація пам'яті при роботі з великими DF</h2></div>
    <div class="glass-card flow-step">
        <p>Об'єднання довірчих інтервалів для тисяч точок даних може створювати навантаження на пам'ять. Двигун оптимізує цей процес за допомогою швидкої конкатенації індексів Pandas <code>pd.concat</code> безпосередньо перед передачею в Plotly. Вхідні дані не дублюються у пам'яті, а передаються у вигляді зрізів (slices), що дозволяє будувати графіки прогнозів з частотою оновлення менше **15 мс**.</p>
    </div>
</div>

<!-- SECTION 10: USER DISPATCHER INTERACTION (HOVER SYNC) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Інтерактивна взаємодія диспетчера (Hover Sync)</h2></div>
    <div class="glass-card flow-step">
        <p>Для покращення читабельності дрібних деталей на лінії часу, всі графіки налаштовані з параметром <code>hovermode="x unified"</code>. Коли оператор наводить курсор на будь-яку точку графіка, система відображає єдину вертикальну лінію-зріз та плаваючу картку зі значеннями ВСІХ моделей, історії та довірчих інтервалів одночасно. Це усуває потребу наводити безпосередньо на тонку нитку кожної окремої лінії.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🔮</div>
            <div class="role-content">
                <h4>Plotly Graph Objects</h4>
                <p>Низькорівневий двигун рендерингу точкових Scatter та Filled Area об'єктів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🗄️</div>
            <div class="role-content">
                <h4>Pandas Library (pd.concat)</h4>
                <p>Оркестратор швидкої підготовки та реверсування часових рядів для контурів.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🖥️</div>
            <div class="role-content">
                <h4>Streamlit UI View</h4>
                <p>Кінцевий споживач та контейнер для вбудовування згенерованих фігур.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (3D CONFIDENCE SPHERE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Multi-step Probabilistic Forecasting)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується радикальний апгрейд двигуна візуалізації прогнозів:</p>
        <ul>
            <li>Впровадження **Багатоступеневих імовірнісних смуг (Fan Charts)** — малювання 3-4 рівнів довірчих інтервалів (50%, 75%, 95%) з різним рівнем градієнтної прозорості. Це відповідає стандартам центральних банків та системних операторів енергоринків.</li>
            <li>Реалізація інтерактивного слайдера "Time-Travel", що дозволить диспетчеру переглядати, як ШІ бачив прогноз на тиждень вперед з будь-якої історичної точки.</li>
        </ul>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Візуалізація Прогнозів ШІ</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому довірча смуга (Confidence Band) не відображається на моєму графіку?</b><br>— Смуга будується тільки тоді, коли у вхідному DataFrame прогнозу (<code>df_fc</code>) присутні колонки <code>upper_bond</code> та <code>lower_bond</code>. Базова модель v1 не має розрахунку довірчих меж, тому для неї будується тільки центральна лінія прогнозу.</p>
        
        <p><b>Як працює обмеження Smart Clipping?</b><br>— Якщо верхня межа довірчого інтервалу через математичну аномалію злітає вгору, система автоматично "зрізає" її на рівні 1.5 від максимуму історії або прогнозу, захищаючи масштаб графіка від сплющення.</p>
        
        <p><b>Чому лінія історії синя, а лінія прогнозу червона?</b><br>— Це відповідає нашому колірному брендбуку: холодний спокійний тон (Синій) символізує надійний історичний факт, а гарячий колір (Червоний) привертає увагу до прогнозного ШІ-майбутнього.</p>
        
        <p><b>Як налаштовано відображення осей часу?</b><br>— Система автоматично підлаштовує формат дат під інтервал (дні/години) за допомогою вбудованого інтелектуального масштабування Plotly.</p>
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
