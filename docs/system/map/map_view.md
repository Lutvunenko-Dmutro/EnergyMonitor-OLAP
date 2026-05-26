# Технічна специфікація: Система Геопросторового Моніторингу (MAP VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">GEOSPATIAL GRID INTELLIGENCE | GRID MONITOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📍</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Географічний Моніторинг</h1>
            <p class="mega-subtitle">Високопродуктивна інтерактивна система візуалізації об'єктів енергосистеми на карті: оперативний контроль завантаження вузлів, просторовий аналіз та картографічний аудит</p>
            <div class="status-tags"><span class="tag tag-online">MAP ENGINE ACTIVE</span><span class="tag tag-version">v2.3.0</span><span class="tag tag-role">GRID OPERATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🗺️</div><div class="metric-info"><span class="metric-label">Provider</span><span class="metric-value">Mapbox / Carto Dark</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Refresh</span><span class="metric-value">Real-time Latency</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Visuals</span><span class="metric-value">High-contrast Dark</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Interaction</span><span class="metric-value">Scatter / Density Map</span></div></div>
</div>

<!-- SECTION 01: SYSTEM PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Геопросторового Моніторингу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>map.py</code> є "Очима" проєкту ATLAS. В енергетиці просторовий контекст є критичним: аварія в одному вузлі може каскадно вплинути на сусідні регіони через перевантаження ЛЕП. Наша філософія базується на <b>Ситуаційній Обізнаності (Situational Awareness)</b>: карта повинна миттєво підсвічувати "гарячі точки" мережі через колірні та розмірні індикатори. Ми використовуємо сучасні висококонтрастні темні карти (Carto Darkmatter) для мінімізації навантаження на зір оператора та забезпечення фокусу на критичних метриках завантаження підстанцій.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL SPATIAL FORMULAS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичне картографічне моделювання</h2></div>
    <div class="glass-card flow-step">
        <p>Геопросторовий моніторинг спирається на розрахунок динамічних параметрів маркерів та щільності:</p>
        
        <h4>1. Динамічне завантаження підстанцій ($L_{\text{pct}}$)</h4>
        <p>Відносна позиція кольору маркера на шкалі залежить від відношення фактичного навантаження до встановленої паспортної потужності:</p>
        $$L_{\text{pct}} = \frac{L_{\text{actual}, i}}{C_{\text{mw}, i}} \times 100\%$$
        <p>де $L_{\text{actual}, i}$ — поточна потужність підстанції $i$ (МВт), а $C_{\text{mw}, i}$ — максимальна встановлена пропускна здатність підстанції (МВт).</p>

        <h4>2. Ядерна оцінка щільності споживання (Mapbox Density Kernel)</h4>
        <p>Теплова карта (Density Map) використовує двовимірну радіальну гаусову функцію для розрахунку інтенсивності навантаження $I(p)$ у географічній точці $p$, зваженого за фактичним споживанням підстанцій:</p>
        $$I(p) = \sum_{i=1}^{M} L_{\text{actual}, i} \times K\left(\frac{d(p, x_i)}{r}\right)$$
        <p>де $K(d)$ — функція ядра (яка спадає зі збільшенням відстані), $d(p, x_i)$ — велике коло відстані між точкою $p$ та підстанцією $x_i$, а $r$ — фіксований радіус пошуку (радіус розмиття встановлено в <code>radius=40</code>).</p>
    </div>
</div>

<!-- SECTION 03: GEOSPATIAL PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Конвеєр Геопросторової Обробки (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Input Historical Load Data") --> IS_EMPTY{"Is Empty?"}
    IS_EMPTY -- "Yes" --> INFO("Display Ingestion Note")
    IS_EMPTY -- "No" --> GROUP_RESOLVE("Resolve Grouping Column (substation/region)")
    
    GROUP_RESOLVE --> TAIL_EXTRACT("tail(1) per group (Latest metrics)")
    TAIL_EXTRACT --> GEO_CHECK{"latitude & longitude exist?"}
    
    GEO_CHECK -- "No" --> WARN("Display Missing Geo-coordinates warning")
    GEO_CHECK -- "Yes" --> PARAM_RESOLVE("Determine size_col & color_col via capacity")
    
    PARAM_RESOLVE --> SELECT_MODE{"Radio Select: Map Mode"}
    
    SELECT_MODE -- "Маркери (Статус)" --> SCATTER("px.scatter_mapbox (Size=Capacity, Color=Load %)")
    SELECT_MODE -- "Heatmap" --> DENSITY("px.density_mapbox (z=actual_load_mw, radius=40)")
    
    SCATTER --> STYLING("Style Layout: 'carto-darkmatter' + Center Ukraine")
    DENSITY --> STYLING
    STYLING --> RENDER("safe_plotly_render")
    </div></div>
</div>

<!-- SECTION 04: COLOR CODING & SEMANTIC RULES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Колірне кодування та семантика статусів</h2></div>
    <div class="glass-card flow-step">
        <p>Для швидкого візуального аналізу завантаженості ЛЕП та підстанцій використовується трирівнева колірна шкала:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Діапазон завантаження</th>
                    <th>Візуальний маркер (Color)</th>
                    <th>Семантичний статус енерговузла</th>
                    <th>Рекомендовані дії диспетчера</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>0% - 60%</b></td><td><span style="color:#22c55e; font-weight:bold">🟢 Green (#22c55e)</span></td><td>Нормальний (Номінальний) режим</td><td>Втручання не потрібне, планове спостереження</td></tr>
                <tr><td><b>60% - 85%</b></td><td><span style="color:#f59e0b; font-weight:bold">🟡 Amber (#f59e0b)</span></td><td>Підвищена увага (Warning)</td><td>Контроль температурних трендів трансформаторного масла</td></tr>
                <tr><td><b>85% - 100%+</b></td><td><span style="color:#ef4444; font-weight:bold">🔴 Red (#ef4444)</span></td><td>Критичне перевантаження (Alarm)</td><td>Запуск аварійного балансування, ручне розвантаження ліній</td></tr>
                <tr><td><b>No Data</b></td><td><span style="color:#6b7280; font-weight:bold">⚫ Gray (#6b7280)</span></td><td>Втрата зв'язку з телеметрією</td><td>Діагностика мережевого з'єднання з датчиком (SCADA)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: INTERACTIVE HOVER CARDS (HUD) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Інтерактивні картки Heads-Up Display (HUD)</h2></div>
    <div class="glass-card flow-step">
        <p>При наведенні курсору на маркер підстанції активується <b>HUD-картка</b>, яка динамічно виводить повний фізико-технічний профіль об'єкта, не перевантажуючи при цьому загальний вигляд карти:</p>
        <ul>
            <li>Назва підстанції та її точні географічні координати.</li>
            <li>Фактичне навантаження в МВт та відносний відсоток завантаження від номіналу.</li>
            <li>Клас робочої напруги (Voltage kV).</li>
            <li>Поточна температура масла трансформатора (°C) та рівень водню (DGA).</li>
            <li>AI-індекс технічного стану здоров'я об'єкта (Health Score %).</li>
        </ul>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Картографічного Ядра (Map Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_geospatial_monitor(df_load):
    1. // [CHECK DATA AVAILABILITY]
       IF df_load is Empty:
           show_data_missing_info()
           RETURN
           
    2. // [RESOLVE GROUPING COLUMN BY PRIORITY]
       IF "substation_name" IN df_load:
           group_col = "substation_name"
       ELSE IF "substation_id" IN df_load:
           group_col = "substation_id"
       ELSE IF "region_name" IN df_load:
           group_col = "region_name"
       ELSE:
           group_col = None
           
    3. // [EXTRACT LATEST METRICS FOR EACH NODE]
       IF group_col is not None:
           latest = df_load.sort_values("timestamp").groupby(group_col).tail(1).copy()
       ELSE:
           latest = df_load.sort_values("timestamp").tail(1).copy()
           
    4. // [GEO-COORDINATES SAFETY SHIELD]
       IF "latitude" NOT IN latest OR "longitude" NOT IN latest:
           show_missing_geo_warning()
           RETURN
           
    5. // [CALCULATE VISUAL SCALING PARAMETERS]
       hover_params = {"actual_load_mw": True, "latitude": False, "longitude": False}
       IF "capacity_mw" IN latest.columns:
           latest["load_pct"] = (latest.actual_load_mw / latest.capacity_mw) * 100
           size_col = "capacity_mw"
           color_col = "load_pct"
           size_max_val = 25
           hover_params["capacity_mw"] = True
           hover_params["load_pct"] = ":.1f"
       ELSE:
           latest["marker_size"] = 10
           size_col = "marker_size"
           color_col = "actual_load_mw"
           size_max_val = 15
           
       FOR col IN ["temperature_c", "health_score", "voltage_kv"]:
           IF col IN latest.columns:
               hover_params[col] = True
               
    6. // [RENDER GRAPHICAL LAYERS VIA PLOTLY MAPBOX]
       IF map_mode == "Маркери (Статус)":
           fig = px.scatter_mapbox(
               latest, lat="latitude", lon="longitude", zoom=5.5,
               center={"lat": 49.0, "lon": 31.0}, mapbox_style="carto-darkmatter",
               color=color_col, color_continuous_scale=["#22c55e", "#f59e0b", "#ef4444"],
               size=size_col, size_max=size_max_val, hover_name=resolve_hover_name(latest),
               hover_data=hover_params, labels=labels_ua
           )
       ELSE:
           fig = px.density_mapbox(
               latest, lat="latitude", lon="longitude", z="actual_load_mw",
               radius=40, zoom=5.5, center={"lat": 49.0, "lon": 31.0},
               mapbox_style="carto-darkmatter", color_continuous_scale="Viridis",
               labels=labels_ua
           )
           
    7. fig.update_layout(height=600, margin={"r":0, "t":0, "l":0, "b":0})
    8. safe_plotly_render(fig)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🌐</div>
            <div class="role-content">
                <h4>Mapbox WebGL Rendering</h4>
                <p>Зовнішній сервіс Carto Darkmatter, що забезпечує швидкий рендеринг векторних карт без навантаження на CPU.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Express Mapbox Engine</h4>
                <p>Низькорівневий двигун генерації точкових маркерів та теплових карт на базі координат.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🛠️</div>
            <div class="role-content">
                <h4><a href="utils_extended_toolkit.md">ui_helpers.py</a></h4>
                <p>Забезпечення безпечного виведення карт без збоїв рендерингу (<code>safe_plotly_render</code>).</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 08: ROADMAP TO v3.0 (ANIMATED TRANSMISSION LINES) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Дорожня карта v3.0 (Animated Transmission Lines)</h2></div>
    <div class="glass-card flow-step">
        <p>У наступних версіях заплановано:</p>
        <ul>
            <li><b>Animated Flow Lines:</b> Візуалізація ліній електропередач (ЛЕП) у вигляді анімованих векторних стрілок, швидкість руху яких пропорційна потужності перетоку (МВт) в реальному часі.</li>
            <li><b>3D Substation Buildings:</b> Рендеринг тривимірних об'єктів підстанцій при високому рівні масштабування карти (Zoom 16+).</li>
            <li><b>Weather Radar Layer:</b> Накладання шару грозового фронту або опадів у реальному часі для оцінки ризику аварій від природних факторів.</li>
        </ul>
    </div>
</div>

<!-- SECTION 09: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">FAQ: Технічні особливості роботи з картою</h2></div>
    <div class="glass-card flow-step">
        <p><b>Q: Чому карта не малюється при виборі деяких Kaggle-файлів?</b><br>
        A: Базові Kaggle-файли містять лише часові позначки та навантаження. Модуль автоматично перевіряє наявність стовпців <code>latitude</code> та <code>longitude</code>. Якщо вони відсутні, система активовує запобіжний щит (Safe Shield) та виводить попередження "Географічні дані недоступні", запобігаючи генерації технічної помилки.</p>
        <p><b>Q: Як розраховується розмір маркерів підстанцій?</b><br>
        A: Якщо доступна колонка номінальної встановленої потужності (<code>capacity_mw</code>), розмір точки масштабується пропорційно (більші підстанції мають більший радіус, максимум 25 пікселів). Це дозволяє оператору з першого погляду зрозуміти системну ієрархію об'єктів.</p>
        <p><b>Q: Чому WebGL є критичним для цього модуля?</b><br>
        A: WebGL передає розрахунки координат та кольорів маркерів безпосередньо графічному прискорювачу (GPU) комп'ютера оператора. Завдяки цьому зум, рух карти та спливаючі HUD-підказки працюють плавно при 60 FPS навіть при виведенні великої кількості енерговузлів.</p>
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
