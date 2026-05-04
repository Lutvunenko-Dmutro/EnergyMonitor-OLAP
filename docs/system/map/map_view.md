# Технічна специфікація: Система Геопросторового Моніторингу (MAP VIEW)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">GEOSPATIAL GRID INTELLIGENCE | GRID MONITOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📍</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Географічний Моніторинг</h1>
            <p class="mega-subtitle">Інтерактивна візуалізація об'єктів енергосистеми на карті: оперативний контроль завантаження вузлів, аналіз щільності споживання та картографічний аудит техстану</p>
            <div class="status-tags"><span class="tag tag-online">MAP ENGINE ACTIVE</span><span class="tag tag-version">v2.3.0</span><span class="tag tag-role">GRID OPERATOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🗺️</div><div class="metric-info"><span class="metric-label">Provider</span><span class="metric-value">Mapbox / Carto</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Refresh</span><span class="metric-value">Real-time Latency</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Design</span><span class="metric-value">High-contrast Dark</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Interaction</span><span class="metric-value">Clustering / Heatmaps</span></div></div>
</div>

<!-- SECTION 01: MAP VIEW PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Геопросторового Моніторингу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>map.py</code> є "Очима" проекту ATLAS. В енергетиці просторовий контекст є критичним: аварія в одному вузлі може каскадно вплинути на сусідні регіони. Наша філософія базується на <b>Ситуаційній Обізнаності</b>: карта повинна миттєво підсвічувати "гарячі точки" мережі через колірні та розмірні індикатори. Ми використовуємо сучасні Dark-карти для мінімізації навантаження на зір оператора та забезпечення фокусу на критичних метриках завантаження підстанцій.</p>
    </div>
</div>

<!-- SECTION 02: GEOSPATIAL PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Конвеєр геопросторової обробки (Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DATA("Input Historical Load Data") --> FILTER("Extract Latest Timestamps")
    FILTER --> GEO("Resolve Latitude/Longitude")
    GEO --> MODE{Map Mode?}
    
    MODE -- "Status Markers" --> SIZE("Calculate Marker Sizes (Capacity)")
    SIZE --> COLOR("Assign Color (Load %)")
    COLOR --> SCATTER("px.scatter_mapbox")
    
    MODE -- "Heatmap" --> DENSITY("px.density_mapbox")
    DENSITY --> WEIGHT("Z-weight by Load MW")
    
    SCATTER --> THEME("Apply Carto-Darkmatter UI")
    WEIGHT --> THEME
    THEME --> RENDER("Safe Plotly Rendering")
    </div></div>
</div>

<!-- SECTION 03: DUAL MONITORING MODES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Подвійні режими моніторингу</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль підтримує два взаємодоповнюючих способи візуалізації енергосистеми:</p>
        <ul>
            <li><b>Статус-маркери (Scatter):</b> Кожна підстанція — це точка. Розмір точки відповідає її встановленій потужності (Capacity), а колір — відсотку поточного завантаження. Це ідеально для точкового контролю вузлів.</li>
            <li><b>Теплова карта (Heatmap):</b> Візуалізує щільність споживання на великих територіях. Дозволяє бачити "хвилі" споживання, що рухаються країною, та ідентифікувати перевантажені енергорайони.</li>
            <li><b>Mapbox Integration:</b> Використання векторних тайлів забезпечує плавний зум від рівня всієї України до конкретної вулиці в місті.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: COLOR CODING & SEMANTIC RULES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Колірне кодування та семантика</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Діапазон завантаження</th>
                    <th>Колір (HEX)</th>
                    <th>Статус системи</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>0% - 60%</td><td>#22c55e (Green)</td><td>Нормальний режим</td></tr>
                <tr><td>60% - 85%</td><td>#f59e0b (Amber)</td><td>Підвищена увага</td></tr>
                <tr><td>85% - 100%+</td><td>#ef4444 (Red)</td><td>Критичне перевантаження</td></tr>
                <tr><td>No Data</td><td>#6b7280 (Gray)</td><td>Втрата телеметрії</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: INTERACTIVE HOVER CARDS (HUD) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Інтерактивні картки (HUD)</h2></div>
    <div class="glass-card flow-step">
        <p>При наведенні курсору на об'єкт, система активує <b>Heads-Up Display (HUD)</b> картку. Вона містить розширений набір даних, який не перевантажує основну карту:</p>
        <ul>
            <li>Точне навантаження в МВт та %.</li>
            <li>Поточна температура повітря в районі об'єкта.</li>
            <li>Клас напруги (Voltage kV) та індекс технічного стану (Health Score).</li>
            <li>Географічні координати для швидкої звірки з диспетчерськими схемами.</li>
        </ul>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Картографічного Ядра (Map Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION render_geospatial_monitor(df_load):
    1. FILTER: latest_data = df_load.sort_by_time().groupby('node').last()
    2. VALIDATE: Ensure lat/lon columns exist in dataframe
    
    3. COMPUTE_VISUALS:
           IF capacity exists:
               marker_size = capacity * scale_factor
               marker_color = (actual / capacity) * 100
           ELSE:
               marker_size = constant(10)
               marker_color = actual_load
               
    4. RENDER_MODE:
           IF mode == "Markers":
               fig = px.scatter_mapbox(latest_data, lat, lon, size, color)
           ELSE:
               fig = px.density_mapbox(latest_data, lat, lon, z=load)
               
    5. STYLING: Apply 'carto-darkmatter' and center view on Ukraine
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: RESPONSIVE MAPBOX LAYOUT -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Адаптивний лейаут Mapbox</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль автоматично центрує карту на географічний центр України (49.0°N, 31.0°E) з оптимальним рівнем масштабування (Zoom 5.5). Завдяки інтеграції з новим широкоформатним дизайном Атласу, карта займає весь доступний простір по ширині, що дозволяє оператору бачити всю енергосистему країни як на великому дисплеї в диспетчерській, так і на ноутбуці.</p>
    </div>
</div>

<!-- SECTION 08: HANDLING MISSING GEO-COORDINATES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Обробка відсутності гео-координат</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення надійності, <code>map.py</code> виконує перевірку наявності стовпців <code>latitude</code> та <code>longitude</code>. Якщо дані надходять з джерела без гео-прив'язки (наприклад, деякі статичні файли Kaggle), система автоматично приховує карту та видає інформативне повідомлення, замість генерації пустого білого вікна або технічного збою.</p>
    </div>
</div>

<!-- SECTION 09: PERFORMANCE OPTIMIZATION (CLIENT-SIDE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Оптимізація продуктивності (WebGL)</h2></div>
    <div class="glass-card flow-step">
        <p>Візуалізація базується на технології WebGL через Plotly/Mapbox. Це дозволяє плавно відображати тисячі маркерів без навантаження на сервер. Всі маніпуляції з картою (зум, панорама) виконуються на стороні клієнта (в браузері), що робить інтерфейс Атласу миттєво відгукуваним та приємним у використанні.</p>
    </div>
</div>

<!-- SECTION 10: BOTTOM SCROLLING COMFORT (UX FIX) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Комфорт скролінгу (UX Fix)</h2></div>
    <div class="glass-card flow-step">
        <p>Як і в інших аналітичних вкладках, у нижній частині карти додано технічний Spacer (300px). Це дозволяє користувачеві прокрутити сторінку так, щоб нижні кнопки керування картою або легенда не перекривалися межами екрана, забезпечуючи повноцінний доступ до всіх інструментів гео-маніпуляції.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🌐</div>
            <div class="role-content">
                <h4>Mapbox GL</h4>
                <p>Зовнішній провайдер векторних тайлів карти.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Plotly Express</h4>
                <p>Двигун побудови картографічних шарів (Scatter/Density).</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">💾</div>
            <div class="role-content">
                <h4>Data Aggregator</h4>
                <p>Джерело останніх актуальних станів енергооб'єктів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (LIVE FLOW ANIMATION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Live Flow Animation)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження <b>Анімованих потоків потужності</b>. На карті з'являться лінії зв'язку (LEP) з рухомими індикаторами, що показуватимуть напрямок та інтенсивність перетоків електроенергії між регіонами. Також буде додано підтримку <b>3D-будівель</b> для міських підстанцій та інтеграцію з супутниковими знімками високої роздільної здатності.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Робота з картою</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому карта не завантажується?</b> — Перевірте наявність інтернет-з'єднання для доступу до тайлів Mapbox.</p>
        <p><b>Як перемикнутися в режим Heatmap?</b> — Скористайтеся перемикачем у верхньому правому куті карти.</p>
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
