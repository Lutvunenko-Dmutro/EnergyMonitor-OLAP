# 🧠 Технічна специфікація модуля: predict_v2.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">AI ANALYTICS | NEURAL INFERENCE ENGINE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧠</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Нейромережевий Предиктор</h1>
            <p class="mega-subtitle">Високонадійний конвеєр предиктивної аналітики на базі оптимізованого ONNX-інференсу LSTM та автоматичної системи Fallback-захисту</p>
            <div class="status-tags"><span class="tag tag-online">INFERENCE ACTIVE</span><span class="tag tag-version">v3.5.0</span><span class="tag tag-role">NEURAL GUARD</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⚡</div><div class="metric-info"><span class="metric-label">Engine</span><span class="metric-value">ONNX Runtime</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧬</div><div class="metric-info"><span class="metric-label">Architecture</span><span class="metric-value">PyTorch LSTM Core</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚖️</div><div class="metric-info"><span class="metric-label">Resilience</span><span class="metric-value">Auto-Fallback</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Correction</span><span class="metric-value">Stitching (Bias Dec.)</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальна Роль та Філософія</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>predict_v2.py</code> є виконавчим ядром штучного інтелекту в системі <b>ATLAS</b>. Його основне завдання — генерація високоточних погодинних прогнозів енергоспоживання на заданий горизонт (до 72 годин вперед). Він спроектований за принципом <b>армійської відмовостійкості (Defense Design)</b>: якщо нейромережа виходить з ладу, пошкоджена або видає математично некоректні значення (наприклад, негативне споживання), система безшовно перемикається на резервний статистичний алгоритм, зберігаючи працездатність інтерфейсу.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL APPARATUS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичний Апарат та Алгоритми</h2></div>
    <div class="glass-card flow-step">
        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-bottom: 10px;">1. Алгоритм Усунення Розривів (Seamless Stitching)</h3>
        <p>На стику фактичних історичних даних та першого прогнозного кроку ШІ часто виникає розрив (ступінчаста похибка). Для її ліквідації модуль реалізує формулу експоненціального затухання початкового відхилення (Bias Decay Correction):</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fff; margin: 15px 0; border: 1px solid var(--border);">
            Y_stitch(t + k) = Y_raw(t + k) + Δ * e^(-α * k)
        </div>
        <p>Де:</p>
        <ul>
            <li><code>Δ = Y_fact(t) - Y_raw(t)</code> — похибка моделі на останній відомій точці факту.</li>
            <li><code>α</code> — коефіцієнт швидкості затухання корекції (за замовчуванням <code>0.15</code>, що забезпечує плавний перехід протягом 12 годин).</li>
            <li><code>k</code> — крок прогнозу вперед.</li>
        </ul>

        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-top: 20px; margin-bottom: 10px;">2. Сезонне змішування (Seasons Blending)</h3>
        <p>На дальніх горизонтах точність LSTM нейромережі падає. Для стабілізації прогнозів реалізовано лінійне змішування прогнозу ШІ з історичним сезонним профілем (Baseline):</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fff; margin: 15px 0; border: 1px solid var(--border);">
            Y_final(t + k) = w(k) * Y_stitch(t + k) + (1 - w(k)) * Y_baseline(t + k)
        </div>
        <p>Де вага нейромережі <code>w(k)</code> лінійно спадає від 1.0 (на першому кроці) до 0.4 (на 72-му кроці), передаючи пріоритет стійкій історичній сезонності.</p>
    </div>
</div>

<!-- SECTION 03: KEY METHODS & API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Сигнатури та Логіка Функцій API</h2></div>
    <div class="glass-card flow-step">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def get_ai_forecast(substation_id, hours_ahead) -> tuple[np.ndarray, str]</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);"><b>Основна точка входу.</b> Приймає ID підстанції та глибину прогнозу. Запускає конвеєр: завантаження моделі -> векторизація -> інференс -> коригування помилки. Повертає масив прогнозів та рядок з описом використаної стратегії.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def _run_onnx_inference(sess, input_feed, hours_ahead) -> np.ndarray</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);"><b>ONNX Інференс.</b> Виконує швидке циклічне рекурентне прогнозування. На кожному кроці передбачене значення навантаження зсувається у вікно історії для генерації наступної точки.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def _compute_scale_factor(history_val, sub_id) -> float</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);"><b>Доменна адаптація.</b> Розраховує індивідуальний коефіцієнт масштабування. Оскільки базова LSTM модель навчена на агрегованих даних, цей метод адаптує амплітуду прогнозу під конкретне енергоспоживання обраної підстанції.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def _run_baseline_fallback(hours_ahead, values, last_ts) -> np.ndarray</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);"><b>Захисний Алгоритм.</b> Seasonal Naive fallback. Використовується, якщо ШІ-модель пошкоджена або недоступна. Копіює аналогічний тижневий профіль навантаження з минулого.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 04: EXECUTION DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Діаграма Процесу Інференсу</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("get_ai_forecast()") --> TRY_AI{"Спроба завантажити ONNX"}
    TRY_AI -- Успішно --> RUN_AI("Запуск _run_onnx_inference()")
    TRY_AI -- Помилка / Відсутній ШІ --> FALLBACK("Запуск _run_baseline_fallback()")
    
    RUN_AI --> STITCH("Згладжування розриву (Stitching)")
    STITCH --> BLEND("Сезонне змішування (Blending)")
    BLEND --> SANITY{"Перевірка адекватності (Sanity)"}
    
    SANITY -- OK --> OUT("Вихід прогнозу LSTM")
    SANITY -- Аномалія (Negative/Inf) --> FALLBACK
    
    FALLBACK --> OUT_FALL("Вихід Baseline прогнозу")
    OUT --> FINAL("Повернення даних в UI")
    OUT_FALL --> FINAL
    </div></div>
</div>

<!-- SECTION 05: INTEGRITY & SECURITY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Механізм Захисту (Sanity Check)</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль містить вбудований математичний вартівник результату ШІ. Після виконання розрахунку нейромережі, перед передачею в інтерфейс, масив перевіряється на наявність:</p>
        <ol>
            <li><b>Негативних значень:</b> Споживання підстанції не може бути менше нуля.</li>
            <li><b>Infinite Spikes (NaN/Inf):</b> Виключення ділення на нуль або математичного вибуху ваг моделі.</li>
            <li><b>Градієнтного вибуху:</b> Різка зміна споживання більш ніж на 300% за 1 годину вважається фізично неможливою аномалією.</li>
        </ol>
        <p>Якщо виявлено хоча б одну аномалію, ШІ-прогноз миттєво відхиляється, і додаток автоматично переходить на безпечний <b>Baseline Fallback</b>.</p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../system/atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
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
