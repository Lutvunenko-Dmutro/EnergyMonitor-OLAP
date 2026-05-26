# Технічна специфікація: Система Візуалізації Структури Генерації (GENERATION MIX MONITOR)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ENERGY MIX ANALYSIS | POWER FLOW VISUALIZATION</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🌊</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Структура Генерації</h1>
            <p class="mega-subtitle">Багатовимірний монітор джерел енергії та балансування потужності: візуалізація потоків через діаграми Sankey, аналіз балансу Energy Mix та динаміка генерації</p>
            <div class="status-tags"><span class="tag tag-online">GENERATION ACTIVE</span><span class="tag tag-version">v2.5.0</span><span class="tag tag-role">BALANCING AUTHORITY</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Flows</span><span class="metric-value">Source -> Region</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚛️</div><div class="metric-info"><span class="metric-label">Categories</span><span class="metric-value">Nuclear / Thermal / RES</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Chart Type</span><span class="metric-value">Sankey / Stacked Area</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Colors</span><span class="metric-value">Master Sync Palette</span></div></div>
</div>

<!-- SECTION 01: GENERATION MIX PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Моніторингу Генерації</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>generation.py</code> є "Серцем" енергобалансу проєкту ATLAS. В сучасній енергетичній системі критично важливо розуміти не лише обсяги споживання, а й походження потужності. Наша філософія базується на <b>Прозорості Потоків</b>: ми візуалізуємо повний шлях електроенергії від типу генерації (АЕС, ТЕС, ГЕС, СЕС, ВЕС) до кінцевого регіону споживання. Використання діаграм Sankey дозволяє диспетчеру миттєво оцінити топологічну структуру балансу, а кругові діаграми Energy Mix підсвічують частку екологічно чистої енергії в системі.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL BALANCING FORMULAS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математична формалізація енергетичного балансу</h2></div>
    <div class="glass-card flow-step">
        <p>Моніторинг генерації спирається на закони збереження енергії та балансові рівняння:</p>
        
        <h4>1. Рівняння вузлового балансу потужності (Sankey Flow conservation)</h4>
        <p>Для будь-якого віртуального транзитного вузла $j$ сума вхідних потоків генерації дорівнює сумі вихідних потоків розподіленого споживання (закон Кірхгофа для потоків):</p>
        $$\sum_{i \in \text{Sources}} F_{\text{gen}, i \to j} = \sum_{k \in \text{Regions}} F_{\text{cons}, j \to k}$$
        <p>де $F_{\text{gen}, i \to j}$ — потужність, що надходить від генератора типу $i$ до вузла розподілу, а $F_{\text{cons}, j \to k}$ — розподілена потужність до регіону $k$.</p>

        <h4>2. Частка екологічно чистої енергії (RES Share)</h4>
        <p>Частка відновлюваних джерел енергії (ВДЕ) у загальному балансі генерації розраховується як відношення екологічних джерел до сумарного вироблення:</p>
        $$\text{RES}_{\text{share}} = \frac{P_{\text{solar}} + P_{\text{wind}} + P_{\text{hydro}}}{\sum_{m \in \text{All}} P_{m}} \times 100\%$$
        <p>де $P_{m}$ — миттєва потужність вироблення джерела типу $m$ в МВт.</p>
    </div>
</div>

<!-- SECTION 03: GENERATION VISUALIZATION PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Конвеєр Візуалізації Генерації (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Input Generation Data (per Source/Region)") --> AGGR_FLOW("Group by generator_type & region_name")
    AGGR_FLOW --> SANKEY_MAP("Map Strings to Indices (Sources + Targets)")
    
    SANKEY_MAP --> HEX_RGBA("Convert Hex colors to RGBA (Alpha=0.5)")
    HEX_RGBA --> REND_SANKEY("go.Sankey (Flow Links)")
    
    DATA --> AGGR_MIX("Group by generator_type (Sum)")
    AGGR_MIX --> REND_PIE("px.pie (Donut 50% hole + Inside Labels)")
    
    DATA --> AGGR_TIME("Group by timestamp & generator_type (Sum)")
    AGGR_TIME --> REND_AREA("go.Scatter (stackgroup='one' + Line Color Sync)")
    </div></div>
</div>

<!-- SECTION 04: GENERATION TYPE COLOR MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця колірної синхронізації (Master Colors)</h2></div>
    <div class="glass-card flow-step">
        <p>Для покращення когнітивного сприйняття системи ми впровадили <b>Master Colors</b>. Кожен тип джерела має фіксований колір, який єдиний для всіх графіків (Sankey, Pie, Area) на дашборді:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Тип джерела</th>
                    <th>Фіксований колір</th>
                    <th>Hex-код</th>
                    <th>Роль у маневруванні та енергомережі</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Nuclear (АЕС)</b></td><td>Amber (Жовтий)</td><td><code>#fbbf24</code></td><td>Базова генерація системи (мінімальна швидкість маневрування)</td></tr>
                <tr><td><b>Thermal (ТЕС/ТЕЦ)</b></td><td>Purple (Фіолетовий)</td><td><code>#a855f7</code></td><td>Середньоманеврене покриття напівпікових навантажень</td></tr>
                <tr><td><b>Hydro (ГЕС/ГАЕС)</b></td><td>Blue (Синій)</td><td><code>#3b82f6</code></td><td>Високоманеврене регулювання ранкових та вечірніх піків споживання</td></tr>
                <tr><td><b>Solar (СЕС)</b></td><td>Orange (Помаранчевий)</td><td><code>#f97316</code></td><td>Відновлювана генерація (залежить від інсоляції)</td></tr>
                <tr><td><b>Wind (ВЕС)</b></td><td>Teal (Бірюзовий)</td><td><code>#2dd4bf</code></td><td>Відновлювана генерація (залежить від вітрового тиску)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: DYNAMIC STACKED AREA ANALYSIS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Аналіз динаміки генерації (Stacked Area)</h2></div>
    <div class="glass-card flow-step">
        <p>Для детального аналізу добових циклів вироблення ми використовуємо <b>Stacked Area Chart</b>, побудований на базі <code>go.Scatter</code> з параметром <code>stackgroup="one"</code>. На відміну від звичайних лінійних графіків, цей чарт показує сумарну потужність системи як суму всіх шарів. Це дозволяє наочно побачити "сонячний горб" вдень або роботу ГЕС під час вечірніх піків. Використання напівпрозорих заливок (RGBA) зберігає легкість сприйняття навіть при накладанні 5 різних типів генерації.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ядра Генерації (Mix Engine Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_generation_mix(df_gen):
    1. // [VALIDITY CHECK]
       IF df_gen is Empty:
           show_live_simulation_warning()
           RETURN
           
    2. // [SANKEY DATA PROCESSING]
       df_s = df_gen.groupby(["generator_type", "region_name"])["actual_generation_mw"].sum().reset_index()
       src_labels = sorted(df_s.generator_type.unique())
       tgt_labels = sorted(df_s.region_name.unique())
       all_nodes = src_labels + tgt_labels
       
       node_indices = create_index_mapping(all_nodes)
       source_idx = [node_indices[s] for s in df_s.generator_type]
       target_idx = [node_indices[t] for t in df_s.region_name]
       values = df_s.actual_generation_mw.tolist()
       
    3. // [DYNAMIC COLORING WITH RGBA HEX TRANSLATION]
       node_colors = [MASTER_COLORS.get(node.lower(), "#64748b") for node in all_nodes]
       link_colors = [hex_to_rgba(MASTER_COLORS.get(src.lower(), "#888888"), alpha=0.5) for src in df_s.generator_type]
       
    4. // [RENDER SANKEY GRAPH]
       fig_sankey = go.Figure(go.Sankey(
           node=dict(label=all_nodes, color=node_colors, pad=20, thickness=15),
           link=dict(source=source_idx, target=target_idx, value=values, color=link_colors)
       ))
       safe_plotly_render(fig_sankey)
       
    5. // [LOWER ROW: DONUT & STACKED AREA]
       c1, c2 = st.columns([1, 2])
       with c1:
           mix_map = {gen: MASTER_COLORS.get(gen.lower(), "#888888") for gen in df_gen.generator_type.unique()}
           fig_pie = px.pie(df_gen, values="actual_generation_mw", names="generator_type", hole=0.5, color_discrete_map=mix_map)
           safe_plotly_render(fig_pie)
           
       with c2:
           df_area = df_gen.groupby(["timestamp", "generator_type"])["actual_generation_mw"].sum().reset_index()
           fig_area = go.Figure()
           FOR gen_type in df_area.generator_type.unique():
               df_sub = df_area[df_area.generator_type == gen_type]
               line_color = MASTER_COLORS.get(gen_type.lower(), "#888888")
               fig_area.add_trace(go.Scatter(
                   x=df_sub.timestamp, y=df_sub.actual_generation_mw,
                   name=gen_type, stackgroup="one",
                   line=dict(width=2, color=line_color),
                   fillcolor=hex_to_rgba(line_color, 0.3)
               ))
           safe_plotly_render(fig_area)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: COLOR TRANSFORMATION ALGORITHMS (HEX-TO-RGBA) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Алгоритми динамічної трансформації кольорів (Hex-to-RGBA)</h2></div>
    <div class="glass-card flow-step">
        <p>Для досягнення ефекту "скляного" інтерфейсу та згладжування ліній зв'язків у діаграмі Sankey, модуль містить алгоритм парсингу Hex-строк:</p>
        <pre><code class="language-python">def hex_to_rgba(h, alpha=0.5):
    h = h.lstrip("#")
    rgb = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"</code></pre>
        <p>Цей інструмент динамічно розраховує трибайтний масив RGB та додає четвертий канал прозорості (Alpha), запобігаючи візуальному накладанню ліній та перекриттю тексту підписів вузлів.</p>
    </div>
</div>

<!-- SECTION 08: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4><a href="simulation_engine_hub.md">data_generator.py</a></h4>
                <p>Постачальник динамічних даних генерації АЕС/ТЕС/ВДЕ у режимі Live-симуляції енергосистеми.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Graph Objects</h4>
                <p>Низькорівневий двигун рендерингу складних вузлів та зв'язків для діаграм Sankey (<code>go.Sankey</code>).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4><a href="utils_extended_toolkit.md">ui_helpers.py</a></h4>
                <p>Гарант безпечної інтеграції Plotly-об'єктів у фреймворк Streamlit за допомогою <code>safe_plotly_render</code>.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 09: ROADMAP TO v3.0 (CARBON AUDIT) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Дорожня карта v3.0 (Carbon Footprint Audit)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступній версії заплановано:</p>
        <ul>
            <li><b>Real-time Carbon Counter:</b> Розрахунок викидів CO₂ на основі типу генерації та спалюваного палива (вугілля, газ) в реальному часі.</li>
            <li><b>AI Curtailment Prediction:</b> Прогнозування обсягів обмеження відновлюваної енергетики (RES Curtailment) при виникненні профіциту в енергосистемі.</li>
            <li><b>Interactive Substation Nodes:</b> Можливість розгорнути вузол регіону на діаграмі Sankey для перегляду розподілу струмів на кожній підстанції.</li>
        </ul>
    </div>
</div>

<!-- SECTION 10: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">FAQ: Технічні особливості роботи</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Чому при виборі Kaggle-джерела пише "Дані про генерацію відсутні"?</b><br>
        A: Kaggle-датасети містять лише сумарні показники споживання регіону без інформації про структуру генерації (яка електростанція скільки виробляла). Ці дані є унікальною фічею нашого імітаційного двигуна (Digital Twin) у реальному часі. Перемкніть джерело на "Симулятор" у боковій панелі.</p>
        <p><b>Q: Як працює сортування вузлів у Sankey-діаграмі?</b><br>
        A: Система сортує джерела та регіони за алфавітом (<code>sorted()</code>), що забезпечує стабільність вузлів при перезавантаженні сторінки та запобігає перемішуванню зв'язків.</p>
        <p><b>Q: Які переваги дає Stacked Area Go.Scatter перед px.area?</b><br>
        A: Використання <code>go.Scatter(stackgroup='one')</code> дає 100% контроль над кольором контуру кожної зони, лінією згладжування та налаштуваннями напівпрозорої заливки, що неможливо зробити базовими методами Plotly Express.</p>
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
