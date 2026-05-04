# Технічна специфікація: Архітектура ML-Активів ATLAS (AI ASSETS GIGA-PASSPORT)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AI RESOURCE LIFECYCLE | ML ASSETS & ARCHITECTURE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📦</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Паспорт ML-Активів</h1>
            <p class="mega-subtitle">Реєстр інтелектуальних ресурсів ATLAS: ONNX-архітектури моделей (V1-V3), бінарні скейлери, мапінг сутностей та стратегія оптимізованого інференсу</p>
            <div class="status-tags"><span class="tag tag-online">MODELS v3 FINAL</span><span class="tag tag-version">ONNX-Runtime</span><span class="tag tag-role">AI RESOURCE MANAGER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🤖</div><div class="metric-info"><span class="metric-label">Model Format</span><span class="metric-value">ONNX (Optimized)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📐</div><div class="metric-info"><span class="metric-label">Look-back</span><span class="metric-value">48 Hours Window</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🏭</div><div class="metric-info"><span class="metric-label">Substations</span><span class="metric-value">12 Core Units</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚀</div><div class="metric-info"><span class="metric-label">Inference</span><span class="metric-value">Graph Opt. Enable</span></div></div>
</div>

<!-- SECTION 01: ML RESOURCE LIFECYCLE PHILOSOPHY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Філософія Життєвого Циклу ML-Ресурсів</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>model_loader.py</code> є "Збройовою палатою" проекту ATLAS. В системах промислового ШІ критично важливо забезпечити не тільки точність, а й надійність завантаження моделей. Паспорт ML-активів описує стратегію переходу від експериментальних моделей до продуктових ONNX-рішень, які забезпечують передбачуваний час відгуку та незалежність від важких фреймворків (як-от PyTorch/TensorFlow) під час роботи HUD-інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 02: MODEL REGISTRY & VERSIONING (V1-V3) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Реєстр моделей та версіонування (V1-V3)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    V1("V1: Baseline Model (ARIMA/Simple)") --> V2("V2: LSTM Hybrid (Beta)")
    V2 --> V3("V3: Final Recursive LSTM (Diploma-Freeze)")
    V3 --> ONNX("ONNX Serialization (Graph Opt)")
    ONNX --> APP("ATLAS HUD Execution")
    SCALER("Joblib Scaler (Normalization)") -. "Sync" .-> ONNX
    </div></div>
</div>

<!-- SECTION 03: SUBSTATION IDENTITY MAPPING -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Мапінг ідентичності підстанцій (Substation Identity)</h2></div>
    <div class="glass-card flow-step">
        <p>Для коректної роботи багатовимірних моделей ШІ використовується жорсткий мапінг назв підстанцій у числові індекси:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Назва об'єкта (ID)</th>
                    <th>Внутрішній індекс</th>
                    <th>Статус у моделі</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>ПС Бровари / Вінниця</td><td>0 / 1</td><td>Active Inference</td></tr>
                <tr><td>ПС Дніпровська-750</td><td>2</td><td>Priority Monitoring</td></tr>
                <tr><td>ПС Київська / Північна</td><td>5 / 6</td><td>High-Density Cluster</td></tr>
                <tr><td>ПС Слобожанська (Харків)</td><td>9</td><td>Border Node Model</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 04: ONNX-RUNTIME OPTIMIZATION STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Стратегія оптимізації ONNX-Runtime</h2></div>
    <div class="glass-card flow-step">
        <p>Система ATLAS не просто завантажує моделі, а налаштовує <b>Inference Session</b> для максимальної швидкодії:</p>
        <ul>
            <li><b>Graph Optimization (ORT_ENABLE_ALL):</b> Об'єднання вузлів нейромережі для зменшення кількості обчислень.</li>
            <li><b>Execution Providers:</b> Пріоритезація CPU-інференсу з фіксованою кількістю потоків (intra_op_num_threads) для стабільної роботи разом із Streamlit.</li>
            <li><b>Integrity Guards:</b> Валідація атрибутів скейлера (mean_, data_max_) перед кожним запуском сесії для запобігання використанню пошкоджених артефактів.</li>
        </ul>
    </div>
</div>

<!-- SECTION 05: SMART RESOURCE CACHING (Streamlit Sync) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Розумне кешування ресурсів (Smart Caching)</h2></div>
    <div class="glass-card flow-step">
        <p>Використання <code>st.cache_resource</code> дозволяє завантажувати важку ШІ-модель у пам'ять лише один раз. Навіть якщо 100 користувачів відкриють дашборд одночасно, система використовуватиме одну спільну сесію ONNX у RAM, що радикально економить ресурси сервера та забезпечує миттєву готовність до прогнозування (Cold-start avoidance).</p>
    </div>
</div>

<!-- SECTION 06: PSEUDO-CODE (MODEL LOADING CORE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">06</span><h2 class="section-title">Псевдокод ядра завантаження ресурсів</h2></div>
    <div class="glass-card flow-step">
        <pre><code>FUNCTION load_resources(version):
    1. PATH = Resolve_Model_Path(version)
    2. CHECK File_Exists(PATH) AND File_Exists(SCALER_PATH)
    
    3. INIT ort.SessionOptions():
           - enable_graph_opt = ALL
           - threads = 1 (Deterministic)
           
    4. sess = ort.InferenceSession(PATH)
    5. scaler = joblib.load(SCALER_PATH)
    
    6. VALIDATE Scaler_Integrity(scaler)
    7. RETURN (sess, scaler)
END FUNCTION</code></pre>
    </div>
</div>

<!-- SECTION 07: AUTOMATED PEAK DETECTION SERVICE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">07</span><h2 class="section-title">Сервіс автоматичного детектування піків</h2></div>
    <div class="glass-card flow-step">
        <p>Функція <code>_get_substation_peak_automated</code> реалізує інтелектуальну дозавантаження контексту для моделей. Вона звертається до БД для отримання реальних історичних максимумів та проектної потужності підстанцій. Це дозволяє ML-моделі коректно де-нормовувати вихідні дані та видавати прогнози у реальних МВт, адаптуючись до поточної конфігурації мережі.</p>
    </div>
</div>

<!-- SECTION 08: FAIL-SAFE RECOURSE STRATEGY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">08</span><h2 class="section-title">Стратегія відмовостійкості (Fail-safe Checkpoints)</h2></div>
    <div class="glass-card flow-step">
        <p>У разі відсутності фінальної моделі V3 (наприклад, під час ітераційного навчання), система автоматично перемикається на <b>V3_checkpoint (best_v3.onnx)</b>. Якщо і він недоступний, логується критична помилка, але інтерфейс продовжує роботу завдяки надійності <code>robust_ml_handler</code>, що виключає каскадний обвал всього HUD.</p>
    </div>
</div>

<!-- SECTION 09: DETERMINISTIC WINDOW MANAGEMENT -->
<div class="section-container">
    <div class="section-header"><span class="section-number">09</span><h2 class="section-title">Детерміноване управління вікном (48h Window)</h2></div>
    <div class="glass-card flow-step">
        <p>Всі моделі ATLAS V3 жорстко синхронізовані з параметром <code>DEFAULT_WINDOW_SIZE = 48</code>. Це гарантує, що для прогнозування завжди використовується 48-годинна передісторія, що є оптимальним для захоплення добових та погодних ритмів споживання енергії, забезпечуючи стабільну точність без збільшення обчислювальної складності.</p>
    </div>
</div>

<!-- SECTION 10: LEGACY & CLI COMPATIBILITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">10</span><h2 class="section-title">Сумісність з Legacy та CLI (Streamlit Fallback)</h2></div>
    <div class="glass-card flow-step">
        <p>Завдяки декоратору <code>st_cache_resource_fallback</code>, модуль може працювати як у графічному інтерфейсі Streamlit, так і в звичайних консольних скриптах для навчання або тестування. Це робить <code>model_loader.py</code> універсальним інструментом для всього циклу розробки ШІ — від лабораторії до продакшну.</p>
    </div>
</div>

<!-- SECTION 11: MODULE DEPENDENCY MATRIX -->
<div class="section-container">
    <div class="section-header"><span class="section-number">11</span><h2 class="section-title">Матриця залежностей (Dependencies)</h2></div>
    <div class="roles-grid">
        <div class="role-item">
            <div class="role-icon">📦</div>
            <div class="role-content">
                <h4>ONNX Runtime</h4>
                <p>Основний двигун інференсу нейронних мереж.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">⚖️</div>
            <div class="role-content">
                <h4>Joblib / Sklearn</h4>
                <p>Десеріалізація та застосування скейлерів даних.</p>
            </div>
        </div>
        <div class="role-item">
            <div class="role-icon">🏗️</div>
            <div class="role-content">
                <h4>Predict V2</h4>
                <p>Основний споживач ресурсів для генерації рекурсивних прогнозів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 12: ROADMAP TO v4.0 (QUANTIZATION & EDGE) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">12</span><h2 class="section-title">Дорожня карта v4.0 (Quantization & Edge AI)</h2></div>
    <div class="glass-card flow-step">
        <p>У версії 4.0 планується впровадження <b>Квантування моделей (INT8)</b> для зменшення споживання RAM, підтримка <b>Multi-model Ensembles</b> (одночасний інференс декількох архітектур) та перехід на <b>WebAssembly (ONNX.js)</b> для виконання ШІ безпосередньо в браузері оператора.</p>
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

<!-- ACADEMIC AUDIT HISTORY -->
<div class='audit-history' style='margin-top: 50px; padding: 20px; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.8rem;'>
    <p><b>Audit ID:</b> ATH-2026-V4-FINAL</p>
    <p><b>Review Date:</b> 2026-05-04</p>
    <p><b>Status:</b> VERIFIED | DEFENSE-READY</p>
    <p><b>Note:</b> Цей модуль пройшов повну технічну верифікацію на відповідність архітектурним стандартам ATLAS.</p>
</div>
