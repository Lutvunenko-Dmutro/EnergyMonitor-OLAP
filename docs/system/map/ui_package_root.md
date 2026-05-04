# Технічна специфікація: Пакет Представлення та Візуалізації (UI & VISUALIZATION PACKAGE)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">UI ROOT | SYSTEM INTERFACE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🖥️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Пакет Візуалізації</h1>
            <p class="mega-subtitle">Корінь системи представлення проекту ATLAS: високорівневий Streamlit-інтерфейс, реалізація естетики Cyber-HUD та координація роботи представлень, сегментів та компонентів у єдиному ситуаційному центрі</p>
            <div class="status-tags"><span class="tag tag-online">UI ROOT ACTIVE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">SYSTEM GATEWAY</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🎨</div><div class="metric-info"><span class="metric-label">Design</span><span class="metric-value">Cyber-HUD Aesthetic</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Structure</span><span class="metric-value">View-Segment-Comp</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Engine</span><span class="metric-value">Streamlit 1.30+</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">State</span><span class="metric-value">Reactive Hub</span></div></div>
</div>

<!-- SECTION 01: UI PACKAGE PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Пакету Візуалізації</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/ui/</code> є "Вітриною" та головним органом взаємодії проекту ATLAS. В інженерних системах інтерфейс — це не просто декорація, а інструмент управління складністю. Наша філософія базується на <b>Когнітивній Ергономіці</b>: ми побудували ієрархію модулів так, щоб від оператора приховувалася технічна складність ML-моделей та SQL-запитів, надаючи натомість чистий, інтуїтивний та естетично бездоганний Cyber-HUD. Це перетворює ATLAS з набору скриптів на професійний ситуаційний центр, готовий до реальної експлуатації в енергосистемі.</p>
    </div>
</div>

<!-- SECTION 02: UI ARCHITECTURE HIERARCHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Ієрархія архітектури UI (Hierarchy Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    ROOT("UI Root (__init__.py)") --> VIEWS("Views/ (Analytics Pages)")
    ROOT --> SEGMENTS("Segments/ (Reactive Fragments)")
    ROOT --> COMPONENTS("Components/ (Reusable Blocks)")
    
    VIEWS --> V_LOGIC("Core Business Logic Vis")
    SEGMENTS --> S_LOGIC("Performance Polling & Layout")
    COMPONENTS --> C_LOGIC("Charts, Cards, Styles")
    
    V_LOGIC --> FINAL("ATLAS Unified Interface")
    S_LOGIC --> FINAL
    C_LOGIC --> FINAL
    </div></div>
</div>

<!-- SECTION 03: TRIAD STRUCTURE (VIEW-SEGMENT-COMPONENT) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Тріадна структура (View-Segment-Component)</h2></div>
    <div class="glass-card flow-step">
        <p>Для забезпечення масштабованості ми розділили UI на три рівні:</p>
        <ul>
            <li><b>Views:</b> Повносторінкові модулі (Прогноз, Аудит, Карта), що відповідають за конкретний бізнес-сценарій.</li>
            <li><b>Segments:</b> Частини сторінок (Sidebar, Dashboard Layout), що забезпечують структуру та динамічне оновлення через <code>st.fragment</code>.</li>
            <li><b>Components:</b> Атомарні блоки (Charts, KPI Cards, Styles), що використовуються повторно у різних частинах додатку.</li>
        </ul>
    </div>
</div>

<!-- SECTION 04: UI LAYER RESPONSIBILITY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Матриця відповідальності шарів UI</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Шар (Sub-package)</th>
                    <th>Головна функція</th>
                    <th>Рівень абстракції</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Views</td><td>Реалізація бізнес-логіки аналізу</td><td>Високий (User-facing)</td></tr>
                <tr><td>Segments</td><td>Оркестрація макетів та стейту</td><td>Середній (Orchestrator)</td></tr>
                <tr><td>Components</td><td>Рендеринг візуальних елементів</td><td>Низький (Atomic)</td></tr>
                <tr><td>Root</td><td>Ініціалізація та ідентичність</td><td>Глобальний (System)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 05: THE CYBER-HUD VISUAL IDENTITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Візуальна ідентичність Cyber-HUD</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/ui/</code> впроваджує єдиний дизайн-код ATLAS. Це не просто темна тема, а комплексна система, що включає: кастомні шрифти (Inter/Orbitron), напівпрозорі контейнери з ефектом скла (Glassmorphism), неонові індикатори стану та приховування всіх зайвих системних елементів Streamlit. Це створює "імерсивний" досвід, де користувач відчуває себе в кабіні пілота футуристичного енерговузла, що підвищує концентрацію на даних та знижує візуальну втому.</p>
    </div>
</div>

<!-- SECTION 06: CORE LOGIC (PSEUDO-CODE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод Ініціалізації Пакету (UI Root Logic)</h2></div>
    <div class="glass-card flow-step">
        <pre><code>MODULE src.ui:
    1. INITIALIZE_METADATA:
           SET package_name = "UI & Visualization"
           DEFINE subpackages = [Views, Components, Segments]
           
    2. COORDINATE_RESOURCES:
           LOAD Global_Styles from Components.Styles
           SYNC Layout from Segments.Dashboard
           
    3. EXPOSE_INTERFACE:
           Provide Gateway to Streamlit Entrypoint
           Ensure Cyber-HUD Aesthetic Compliance
END MODULE</code></pre>
    </div>
</div>

<!-- SECTION 07: PERFORMANCE & REACTIVITY STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Стратегія продуктивності та реактивності</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки чіткому розділенню на підпакети, ATLAS реалізує стратегію <b>Оптимізованого перерендерингу</b>. Використання фрагментів у <code>segments/</code> дозволяє оновлювати тільки телеметрію, не зачіпаючи важкі аналітичні графіки у <code>views/</code>. Це забезпечує високу швидкість відгуку інтерфейсу навіть при одночасній роботі з гігабайтами історичних даних та складними ML-прогнозами, роблячи роботу оператора максимально плавною.</p>
    </div>
</div>

<!-- SECTION 08: THE GATEWAY TO ATLAS DATA BUS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Шлюз до шини даних ATLAS (Data Bus)</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет UI служить головним споживачем внутрішньої шини даних (Session State). Через <code>__init__.py</code> проходять запити на синхронізацію стану між різними вкладками. Це гарантує, що якщо користувач змінив регіон на вкладці "Карта", ці зміни миттєво підхопляться вкладками "Прогноз" та "KPI", забезпечуючи цілісність аналітичного контексту у всьому додатку ATLAS.</p>
    </div>
</div>

<!-- SECTION 09: USER-CENTRIC DESIGN PRINCIPLES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Принципи орієнтованого на користувача дизайну</h2></div>
    <div class="glass-card flow-step">
        <p>Кожен піксель у пакеті <code>src/ui/</code> спроектований з урахуванням <b>Аналітичного UX</b>. Ми використовуємо принцип "Спершу головне": KPI та Карта розташовані на пріоритетних позиціях, а детальні таблиці та налаштування — у глибших шарах або сайдбарі. Використання звичних колірних кодів (Червоний для небезпеки, Зелений для норми) дозволяє оператору зчитувати стан системи на підсвідомому рівні, мінімізуючи час реакції на інциденти.</p>
    </div>
</div>

<!-- SECTION 10: STANDARDIZATION & SCALING (ACADEMIC VALUE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Стандартизація та масштабування (Академічна цінність)</h2></div>
    <div class="glass-card flow-step">
        <p>Для академічного захисту (тезису) структура пакета <code>src/ui/</code> є прикладом **Чистої архітектури** в Streamlit-додатках. Ми відійшли від "спагетті-коду" в одному файлі, впровадивши професійне пакетне розділення. Це демонструє високий рівень інженерної культури та здатність системи до масштабування: додавання нового функціоналу потребує лише створення нового модуля у відповідному підпакеті, що відповідає SOLID-принципам розробки ПЗ.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Streamlit Framework</h4>
                <p>Основне середовище виконання та рендерингу UI.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🎨</div>
            <div class="role-content">
                <h4>Custom CSS Engine</h4>
                <p>Система стилізації для забезпечення ідентичності Cyber-HUD.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">📊</div>
            <div class="role-content">
                <h4>Data Services</h4>
                <p>Бекенд-провайдери даних, що живлять інтерфейс через сесію.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v3.0 (MULTI-USER COLLABORATION) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v3.0 (Multi-user Collab)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 3.0 планується впровадження **Багатокористувацької колаборації**. Пакет UI буде підтримувати синхронне відображення стану системи для групи диспетчерів з можливістю "спільного перегляду" аномалій. Також буде додано підтримку <b>АР/VR представлень</b> для віртуальних ситуаційних центрів та розширено бібліотеку компонентів інтерактивними 3D-моделями енергооб'єктів.</p>
    </div>
</div>

<!-- SECTION 13: FAQ - ЧАСТІ ЗАПИТАННЯ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">13</span><h2 class="section-title">FAQ: Пакет Візуалізації</h2></div>
    <div class="glass-card flow-step">
        <p><b>Чому структура UI така складна?</b> — Це необхідно для підтримки високої продуктивності та легкості супроводу проекту при його зростанні.</p>
        <p><b>Де знайти налаштування теми?</b> — Всі глобальні стилі та кольорові токени інкапсульовані в <code>src/ui/components/styles.py</code>.</p>
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
