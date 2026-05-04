# Технічна специфікація: Система Візуалізації Структури Генерації (GENERATION MIX MONITOR)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ENERGY MIX ANALYSIS | POWER FLOW VISUALIZATION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🌊</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Структура Генерації</h1>
            <p class="mega-subtitle">Багатовимірний монітор джерел енергії: візуалізація потоків потужності через діаграми Sankey, аналіз балансу Energy Mix та динаміка вироблення з розбивкою за категоріями</p>
            <div class="status-tags"><span class="tag tag-online">GENERATION ACTIVE</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">BALANCING AUTHORITY</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Flows</span><span class="metric-value">Source -> Region</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚛️</div><div class="metric-info"><span class="metric-label">Categories</span><span class="metric-value">Nuclear / RES / Thermal</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Chart Type</span><span class="metric-value">Sankey / Stacked Area</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Colors</span><span class="metric-value">Master Sync Palette</span></div></div>
</div>

<!-- SECTION 01: GENERATION MIX PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Моніторингу Генерації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>generation.py</code> є "Серцем" енергобалансу проекту ATLAS. В сучасному світі важливо не лише скільки енергії споживається, а й звідки вона береться. Наша філософія базується на <b>Прозорості Потоків</b>: ми візуалізуємо шлях електроенергії від типу генерації (АЕС, ТЕС, ВДЕ) до кінцевого регіону споживання. Використання діаграм Sankey дозволяє диспетчеру миттєво оцінити топологічну структуру балансу, а кругові діаграми Energy Mix підсвічують частку екологічно чистої енергії в системі.</p>
    </div>
</div>

<!-- SECTION 02: GENERATION VISUALIZATION PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр Візуалізації Генерації (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Input Generation Data (per Source/Region)") --> AGGR_FLOW("Aggregate by Type & Destination")
    AGGR_FLOW --> SANKEY("Generate Sankey Nodes & Links")
    SANKEY --> VIS_SANKEY("Power Flow Diagram (Interactive)")
    
    DATA --> AGGR_MIX("Sum by Generator Type")
    AGGR_MIX --> VIS_PIE("Pie Chart (Energy Mix %)")
    
    DATA --> AGGR_TIME("Time-series Grouping")
    AGGR_TIME --> VIS_AREA("Stacked Area Chart (Dynamics)")
    
    VIS_SANKEY --> SYNC("Master Color Synchronization")
    VIS_PIE --> SYNC
    VIS_AREA --> SYNC
    </div></div>
</div>

<!-- SECTION 03: POWER FLOW VISUALIZATION (SANKEY) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Візуалізація потоків (Sankey Diagram)</h2></div>
    <div class="glass-card flow-step">
        <p>Для відображення складних зв'язків між джерелами та споживачами ми впровадили діаграму <b>Sankey</b>:</p>
        <ul>
            <li><b>Topology Mapping:</b> Ліва частина діаграми — типи генерації (Джерела), права — регіони (Цілі).</li>
            <li><b>Weighted Links:</b> Товщина ліній між вузлами пропорційна обсягу переданої потужності в МВт.</li>
            <li><b>Interactive Tooltips:</b> При наведенні на потік система показує точне значення МВт*год, що передається від конкретного джерела до конкретного регіону.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: GENERATION TYPE COLOR MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця ідентифікації джерел (Master Colors)</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Тип джерела</th>
                    <th>Колір</th>
                    <th>HEX</th>
                    <th>Роль у системі</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Nuclear (АЕС)</td><td>Amber</td><td>#fbbf24</td><td>Базова генерація</td></tr>
                <tr><td>Thermal (ТЕС/ТЕЦ)</td><td>Purple</td><td>#a855f7</td><td>Маневрена потужність</td></tr>
                <tr><td>Hydro (ГЕС/ГАЕС)</td><td>Blue</td><td>#3b82f6</td><td>Пікове регулювання</td></tr>
                <tr><td>Solar (СЕС)</td><td>Orange</td><td>#f97316</td><td>Відновлювана енергія</td></tr>
                <tr><td>Wind (ВЕС)</td><td>Teal</td><td>#2dd4bf</td><td>Відновлювана енергія</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: DYNAMIC STACKED AREA ANALYSIS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Аналіз динаміки (Stacked Area)</h2></div>
    <div class="glass-card flow-step">
        <p>Для розуміння добових циклів вироблення ми використовуємо <b>Stacked Area Chart</b>. На відміну від звичайних ліній, цей графік показує сумарну потужність системи як суму всіх шарів. Це дозволяє наочно побачити "сонячний горб" вдень або роботу ГЕС під час ранкових та вечірніх піків споживання. Використання напівпрозорих заливок (RGBA) зберігає легкість сприйняття навіть при накладанні 5-6 різних типів генерації.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Генерації (Mix Engine Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_generation_mix(df_gen):
    1. VALIDATE: Ensure dataframe has [type, region, mw, ts]
    
    2. SANKEY_DATA_PREP:
           nodes = sources + regions
           links = map_to_indices(sources -> regions, values=mw)
           colors = [MASTER_COLORS.get(n) for n in nodes]
           RENDER_SANKEY(nodes, links, colors)
           
    3. PIE_CHART:
           mix = df_gen.groupby('type').sum()
           RENDER_PIE(mix, hole=0.5, color_map=MASTER_COLORS)
           
    4. AREA_CHART:
           timeline = df_gen.groupby(['ts', 'type']).sum()
           FOR type IN mix:
               ADD_STACKED_TRACE(timeline[type], fill='tonexty')
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: ENERGY MIX PERCENTAGE ANALYSIS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Аналіз відсоткової частки Energy Mix</h2></div>
    <div class="glass-card flow-step">
        <p>Центральним елементом нижнього ярусу є <b>Donut Chart</b>. Він фокусує увагу на структурі портфеля генерації. Спеціальний режим <code>textinfo="percent+label"</code> дозволяє диспетчеру миттєво відповісти на питання: "Яка частка АЕС у поточному балансі?". Синхронізація кольорів з діаграмою Sankey забезпечує когнітивну цілісність — користувач підсвідомо пов'язує жовтий колір з атомною енергією у всіх частинах дашборду.</p>
    </div>
</div>

<!-- SECTION 08: COLOR TRANSFORMATION ALGORITHMS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Алгоритми трансформації кольорів (Hex-to-RGBA)</h2></div>
    <div class="glass-card flow-step">
        <p>Для створення ефекту "скляного" інтерфейсу в <code>generation.py</code> реалізовано внутрішній конвертер <code>hex_to_rgba</code>. Він динамічно перетворює базові кольори з <code>MASTER_COLORS</code> у напівпрозорі версії для ліній зв'язку Sankey та заливки площ Area Chart. Це дозволяє уникнути візуального шуму та перекриття тексту, зберігаючи при цьому насиченість брендових кольорів Атласу.</p>
    </div>
</div>

<!-- SECTION 09: LIVE SIMULATION INTEGRATION -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Інтеграція з Live-симуляцією</h2></div>
    <div class="glass-card flow-step">
        <p>Дані про структуру генерації є найбільш динамічною частиною системи. Модуль тісно інтегрований з <code>data_generator.py</code>. У режимі симуляції користувач може спостерігати, як раптова зупинка енергоблока ТЕС (через інцидент у <code>alerts.py</code>) призводить до перерозподілу потоків на діаграмі Sankey та збільшення частки гідрогенерації для компенсації дефіциту в реальному часі.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM SPACER & SCROLLING (UX FIX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Комфорт скролінгу (UX Fix)</h2></div>
    <div class="glass-card flow-step">
        <p>У нижній частині вкладки генерації додано технічний Spacer (300px). Це критично для діаграм Sankey та Stacked Area, які зазвичай мають велику висоту. Відступ дозволяє користувачеві прокрутити графік так, щоб легенда та елементи керування Plotly знаходилися у верхній третині екрана, забезпечуючи зручний доступ до інтерактивних інструментів аналізу.</p>
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
                <p>Низькорівневий рендеринг складних Sankey-потоків.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Data Generator</h4>
                <p>Постачальник синтетичних даних про структуру джерел.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4>UI Helpers</h4>
                <p>Гарант безпечної візуалізації без технічних збоїв.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (CARBON FOOTPRINT) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Carbon Footprint)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Аудиту вуглецевого сліду</b>. Система буде розраховувати обсяг викидів CO2 у реальному часі на основі структури генерації. Також буде додано підтримку <b>Прогнозного балансування</b>: візуалізація необхідного Mix-у генерації для покриття ШІ-прогнозу навантаження на наступні 24 години.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Структура Генерації</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому Sankey діаграма іноді переплутана?</b> — Це може статися при великій кількості дрібних регіонів. Спробуйте змінити фільтр групування у боковій панелі.</p>
        <p><b>Як виділити тільки один тип джерела?</b> — Натисніть на відповідний колір у легенді графіка Area Chart.</p>
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
