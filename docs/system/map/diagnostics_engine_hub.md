# Технічна специфікація: Двигун Системної Діагностики та Валідації (DIAGNOSTICS ENGINE HUB)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">SYSTEM INTEGRITY | QUALITY ASSURANCE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛡️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Центр Діагностики</h1>
            <p class="mega-subtitle">Шар інтелектуального контролю якості ATLAS: автоматичний пошук патернів помилок, моніторинг цілісності ML-моделей та формування комплексних звітів про стан здоров'я системи</p>
            <div class="status-tags"><span class="tag tag-online">SCANNER ACTIVE</span><span class="tag tag-version">v3.0.0</span><span class="tag tag-role">QUALITY GATE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Scanning</span><span class="metric-value">Deep Metadata Audit</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧩</div><div class="metric-info"><span class="metric-label">Patterns</span><span class="metric-value">Error Signature Mapping</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Reporting</span><span class="metric-value">Automated Health Score</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">ML Audit</span><span class="metric-value">Drift & Integrity Scan</span></div></div>
</div>

<!-- SECTION 01: THE MISSION OF DIAGNOSTICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Місія Системної Діагностики</h2></div>
    <div class="glass-card flow-step">
        <p>Пакет <code>src/core/diagnostics/</code> виконує роль "Імунної системи" проекту ATLAS. В складних аналітичних комплексах помилка в даних або в параметрах моделі може призвести до хибних прогнозів, що мають серйозні економічні наслідки. Наш двигун діагностики забезпечує превентивне виявлення таких проблем, аналізуючи метадані, структуру часових рядів та внутрішні стани нейронних мереж ще до того, як результати потраплять до оператора.</p>
    </div>
</div>

<!-- SECTION 02: DIAGNOSTICS MODULES MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Матриця Модулів Діагностики</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Модуль</th>
                    <th>Функціональна Роль</th>
                    <th>Методологія</th>
                    <th>Ціль</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>scanner.py</code></td><td>Глибоке сканування</td><td>Regex & Metadata Audit</td><td>Виявлення структурних збоїв</td></tr>
                <tr><td><code>patterns.py</code></td><td>Аналіз сигнатур</td><td>Pattern Recognition</td><td>Класифікація типів помилок</td></tr>
                <tr><td><code>models.py</code></td><td>Аудит ML-моделей</td><td>ONNX Graph Analysis</td><td>Гарантія цілісності AI</td></tr>
                <tr><td><code>reporter.py</code></td><td>Генератор звітів</td><td>Markdown & PDF Export</td><td>Візуалізація стану системи</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: DEEP METADATA SCANNING STRATEGY -->
<div class="section-container" id="scanner">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Стратегія Глибокого Сканування Метаданих</h2></div>
    <div class="glass-card flow-step">
        <p>У <code>scanner.py</code> ми реалізуємо алгоритм <b>Multi-level Inspection</b>. Система перевіряє не лише наявність файлів, а й відповідність їхнього внутрішнього змісту встановленим стандартам ATLAS (наприклад, наявність тегів # ATLAS_PASSPORT). Це гарантує, що документація та код завжди синхронізовані, а будь-які відхилення автоматично потрапляють у список завдань на виправлення.</p>
    </div>
</div>

<!-- SECTION 04: DIAGNOSTIC PIPELINE DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема Діагностичного Конвеєра</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    CODE_BASE("ATLAS Codebase & Data") --> SCANNER("scanner.py: Deep Inspection")
    SCANNER -- Metadata --> PATTERNS("patterns.py: Signature Match")
    SCANNER -- AI Models --> ML_AUDIT("models.py: Integrity Check")
    
    PATTERNS --> REP_GEN("reporter.py: Orchestrator")
    ML_AUDIT --> REP_GEN
    
    REP_GEN --> PDF("Technical Health Report")
    REP_GEN --> UI_DASH("Admin Dashboard")
    </div></div>
</div>

<!-- SECTION 05: ERROR SIGNATURE & PATTERN MAPPING -->
<div class="section-container" id="patterns">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Мапування Сигнатур та Паттернів Помилок</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>patterns.py</code> дозволяє системі ATLAS "вчитися на помилках". Ми створюємо бібліотеку сигнатур відомих проблем: від втрати пакетів телеметрії до дрейфу ваг моделей. Коли сканер виявляє аномалію, цей модуль ідентифікує її тип та пропонує готові сценарії вирішення, що значно прискорює технічне обслуговування системи.</p>
    </div>
</div>

<!-- SECTION 06: ML MODEL INTEGRITY AUDIT -->
<div class="section-container" id="models">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Аудит Цілісності ML-Моделей</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>models.py</code> фокусується на безпеці ШІ. Він аналізує графіки обчислень ONNX-моделей на наявність некоректних шарів або неоптимальних шляхів виконання. Також проводиться перевірка вхідних та вихідних тензорів на відповідність фізичним обмеженням енергосистеми, запобігаючи "галюцинаціям" ШІ.</p>
    </div>
</div>

<!-- SECTION 07: AUTOMATED REPORTING & DOCUMENTATION -->
<div class="section-container" id="reporter">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Автоматизована Звітність та Документація</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки <code>reporter.py</code> результати діагностики перетворюються на структуровані документи. Система автоматично генерує <i>System Health Score</i> — єдину метрику, що відображає загальний стан проекту. Ці звіти є критично важливими для проходження технічних аудитів та захисту наукових робіт, забезпечуючи доказову базу стабільності ATLAS.</p>
    </div>
</div>

<!-- SECTION 08: METADATA DRIVEN DEVELOPMENT (MDD) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Розвиток через Метадані (MDD)</h2></div>
    <div class="glass-card flow-step">
        <p>Ми впроваджуємо підхід, де метадані (паспорти) є не просто описом, а активною частиною системи. Діагностичний двигун використовує інформацію з паспортів для автоматичного налаштування глибини перевірки кожного модуля, створюючи саморегульовану екосистему контролю якості.</p>
    </div>
</div>

<!-- SECTION 09: GRACEFUL DEGRADATION ANALYSIS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Аналіз М'якої Деградації</h2></div>
    <div class="glass-card flow-step">
        <p>Система діагностики здатна оцінювати, як вихід з ладу одного модуля вплине на загальну точність прогнозів. Це дозволяє впроваджувати стратегії <b>Graceful Degradation</b>: якщо складний ML-алгоритм недоступний, система автоматично перемикається на спрощену статистичну модель, зберігаючи базову функціональність моніторингу.</p>
    </div>
</div>

<!-- SECTION 10: ROADMAP TO v4.0 (SELF-HEALING ARCHITECTURE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Дорожня карта v4.0 (Self-healing)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 4.0 планується перехід до **Архітектури Самозцілення**. Система діагностики зможе не лише виявляти проблеми, а й автоматично застосовувати "патчі" або перевантажувати мікросервіси при виявленні критичних патернів. Також буде додано підтримку <i>Predictive Maintenance</i> для самого коду, виявляючи потенційні місця виникнення помилок на основі аналізу історії коммітів.</p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="./atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
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
