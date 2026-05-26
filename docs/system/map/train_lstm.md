# 🧠 Технічна специфікація модуля: train_lstm.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DEEP LEARNING MODEL DESIGN LAB & MODEL REGISTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧬</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Лабораторія Навчання ШІ</h1>
            <p class="mega-subtitle">Автоматизований конвеєр навчання глибоких нейронних мереж LSTM: від вибірки з БД та Feature Engineering до валідації та експорту ONNX артефактів</p>
            <div class="status-tags"><span class="tag tag-online">TRAINING PIPELINE</span><span class="tag tag-version">v3.2.0</span><span class="tag tag-role">MODEL BUILDER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🤖</div><div class="metric-info"><span class="metric-label">Framework</span><span class="metric-value">Keras / TensorFlow</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Optimizer</span><span class="metric-value">Adam (lr=0.001)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Loss Function</span><span class="metric-value">MAE / Huber</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛑</div><div class="metric-info"><span class="metric-label">Regularization</span><span class="metric-value">EarlyStopping (p=7)</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Архітектурне призначення та логіка</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <code>train_lstm.py</code> є «фабрикою інтелекту» аналітичної системи <b>ATLAS</b>. Він виконує офлайн-навчання універсальних моделей прогнозування навантаження підстанцій. Процес побудований так, щоб модель навчалася на об'єднаних історичних профілях споживання з повною ізоляцією об'єктів під час нормалізації. Це дозволяє навчити **єдину потужну модель** (Universal LSTM Engine), яка розуміє глобальні цикли споживання, але адаптується під масштаби окремих вузлів через доменні коефіцієнти.</p>
    </div>
</div>

<!-- SECTION 02: MATHEMATICAL APPARATUS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичний Апарат Навчання</h2></div>
    <div class="glass-card flow-step">
        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-bottom: 10px;">1. Нормалізація ознак (MinMax Scaling)</h3>
        <p>Для швидкої збіжності градієнтного спуску всі вхідні числові фічі переводяться в діапазон <code>[0, 1]</code> за формулою:</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fff; margin: 15px 0; border: 1px solid var(--border);">
            X_std = (X - X_min) / (X_max - X_min)
        </div>
        <p>Параметри <code>X_min</code> та <code>X_max</code> зберігаються окремо для кожної підстанції у вигляді серіалізованих файлів <code>scaler_[sub_id].joblib</code> для зворотного перетворення (Inverse Scaling) при інференсі.</p>

        <h3 style="color: var(--accent); font-family: 'Orbitron', sans-serif; font-size: 14px; margin-top: 20px; margin-bottom: 10px;">2. Цільова функція втрат (MAE Loss)</h3>
        <p>Для навчання рекурентних шарів використовується стійка до викидів функція MAE (Mean Absolute Error):</p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fff; margin: 15px 0; border: 1px solid var(--border);">
            MAE = (1 / N) * Σ |Y_i - Ŷ_i|
        </div>
        <p>Мінімізація помилки виконується алгоритмом адаптивного оцінювання моменту <b>Adam</b>.</p>
    </div>
</div>

<!-- SECTION 03: LSTM NEURAL ARCHITECTURE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Архітектура Нейромережі</h2></div>
    <div class="glass-card flow-step">
        <p>Конвеєр будує рекурентну мережу наступної конфігурації:</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin: 15px 0;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th>Шар (Layer)</th>
                    <th>Конфігурація (Shape / Units)</th>
                    <th>Опис та Регуляризація</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Input Layer</td><td><code>(Batch, 48, 5)</code></td><td>Вікно історії 48 годин, 5 вхідних ознак</td></tr>
                <tr><td>LSTM Layer 1</td><td><code>64 hidden units</code></td><td>Рекурентний шар, <code>return_sequences=True</code></td></tr>
                <tr><td>Dropout 1</td><td><code>Rate = 0.20</code></td><td>Запобігає перенавчанню (скидання 20% зв'язків)</td></tr>
                <tr><td>LSTM Layer 2</td><td><code>32 hidden units</code></td><td>Рекурентний шар, <code>return_sequences=False</code></td></tr>
                <tr><td>Dense Output</td><td><code>1 node (Linear)</code></td><td>Прогноз навантаження на наступний крок (t+1)</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 04: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Сигнатури та Методи API</h2></div>
    <div class="glass-card flow-step">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def train_lstm(version_tag, epochs=100) -> bool</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);"><b>Основна процедура навчання.</b> Виконує повний цикл: збір даних з БД -> векторизація ознак -> створення LSTM-тензорів -> компіляція моделі -> запуск оптимізації -> серіалізація артефактів.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def load_data_from_db() -> pd.DataFrame</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);"><b>Завантажувач даних.</b> Зчитує історичні часові ряди з PostgreSQL та виконує вирівнювання часових шкал для запобігання зміщенню даних (Data Leakage).</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
                <code style="color: var(--accent); font-size: 14px; font-weight: bold;">def create_dataset(dataset, look_back=48) -> tuple[np.ndarray, np.ndarray]</code>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: var(--text-main);"><b>Генератор вікон.</b> Перетворює плоский масив даних у тривимірний тензор <code>(N, 48, 5)</code> для подачі на вхід LSTM шарів.</p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 05: TRAINING FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Життєвий Цикл Навчання Моделі</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DB("Історичні дані (DB)") --> LOAD("load_data_from_db()")
    LOAD --> SCALE("Побудова MinMaxScaler")
    SCALE --> ENG("Feature Engineering (Час/Температура)")
    ENG --> TENSOR("Створення вікон: create_dataset()")
    
    TENSOR --> SPLIT("Розподіл: Train (80%) / Val (20%)")
    SPLIT --> FIT("Навчання: model.fit()")
    
    subgraph CAL_BACKS["Активний контроль"]
        EARLY("EarlyStopping (patience=7)")
        CHECK("ModelCheckpoint (Best only)")
    end
    
    FIT --> CAL_BACKS
    CAL_BACKS -- Перевищення похибки / Зупинка --> EVAL("Оцінка MAE / Validation")
    EVAL --> SAVE("Збереження: .h5 модель & .joblib скалер")
    SAVE --> ONNX("Експорт у формат ONNX (Inference Ready)")
    </div></div>
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
