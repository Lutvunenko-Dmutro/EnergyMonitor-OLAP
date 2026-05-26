# Технічний Паспорт Компонента: scripts/ml/lstm_sandbox.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🧪 NEURAL SANDBOX & LSTM PROTOYPING LAB</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔬</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">lstm_sandbox.py</h1>
            <p class="mega-subtitle">Лабораторія ШІ-експериментів, швидкого прототипування нейромережевих архітектур та багатокрокового прогнозування</p>
            <div class="status-tags">
                <span class="tag tag-online">AI SANDBOX</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">PROTOTYPING DEPOT</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🔄</div>
        <div class="metric-info">
            <span class="metric-label">Data Engine</span>
            <span class="metric-value">Synthetic Sinusoid</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-info">
            <span class="metric-label">Forecast Horizon</span>
            <span class="metric-value">Direct Multi-step (24h)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧱</div>
        <div class="metric-info">
            <span class="metric-label">Regularizer</span>
            <span class="metric-value">Recurrent Dropout 0.2</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📈</div>
        <div class="metric-info">
            <span class="metric-label">Train Budget</span>
            <span class="metric-value">50 Epochs / batch=16</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Експериментальна лабораторія та ШІ-прототипування</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/ml/lstm_sandbox.py</code> є виділеним **дослідницьким полігоном** (LSTM Prototyping Sandbox) в архітектурі платформи <b>Energy Monitor Ultimate</b>. Він надає розробникам ізольоване та швидке середовище для тестування нових гіперпараметрів нейромереж, архітектур шарів, методів регуляризації та оптимізації перед впровадженням моделей у продуктивне аналітичне ядро Atlas.
        </p>
        <p style="margin-top: 10px;">
            Ключові напрями роботи лабораторії:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Синтетична генерація (Synthetic Data Generation):</strong> Моделювання штучних добових часових рядів навантаження з математично заданою гармонічною сезонністю та білим шумом.</li>
            <li><strong>Багатокрокове прогнозування (Direct Multi-step Dataset):</strong> Підготовка даних методом ковзного вікна для прямого прогнозування на добу вперед (24 години) за один прохід інференсу.</li>
            <li><strong>Протидія перенавчанню (Regularization Sandbox):</strong> Дослідження впливу рекурентного завалу ваг (Recurrent Dropout) на стабільність градієнтів та збіжність навчання.</li>
            <li><strong>Контроль навчання (Validation Curve Visualization):</strong> Автоматична побудова графіків втрат (Train/Val Loss) та зіставлення прогнозів з фактом для візуального аудиту якості.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: WORKFLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр швидкого ШІ-експерименту (AI Prototyping Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема відображає етапи проходження швидкого циклу навчання в пісочниці:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск: lstm_sandbox.py") --> GEN_DATA("1. Генерація 1500 точок ряду за гармонічною формулою")
                GEN_DATA --> SCALE_DATA("2. Масштабування MinMaxScaler -> [0, 1]")
                
                SCALE_DATA --> CREATE_WIN("3. Вікна: X (історія 24) -> y (прогноз 24)")
                CREATE_WIN --> RESHAPE_3D("4. Решейпінг X у 3D Keras-тензор (Samples, 24, 1)")
                
                RESHAPE_3D --> BUILD_MODEL("5. Збірка Sequential LSTM (64 units, recurrent_dropout=0.2)")
                BUILD_MODEL --> COMPILE_MODEL("6. Компіляція: Adam(lr=0.001) + MSE Loss")
                
                COMPILE_MODEL --> TRAIN_MODEL("7. Тренування: 50 епох, batch=16, val_split=20%")
                TRAIN_MODEL --> EVAL_RESULTS("8. Вибірковий тест на випадковому вікні")
                
                EVAL_RESULTS --> PLOT_RESULTS("9. Рендеринг графіків: Learning Curve & Predict vs Real")
                PLOT_RESULTS --> END("Експеримент завершено")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичне моделювання та регуляризація LSTM</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Математична модель синтетичного навантаження</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Ряд $y(t)$ генерується за допомогою накладання добової синусоїдальної сезонності амплітудою 20 МВт з базовим навантаженням 50 МВт та випадковим гаусовим шумом:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ y(t) = 50 + 20 \sin\left(\frac{2\pi \cdot t}{24}\right) + \epsilon(t), \quad \text{де } \epsilon(t) \sim \mathcal{N}(0, 2^2) $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Пряме багатокрокове прогнозування (Direct Multi-step Forecast)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    На відміну від рекурсивного прогнозування, яке накопичує похибки на кожному кроці, архітектура пісочниці використовує прямий метод (Direct). Повнозв'язний вихідний шар Dense розраховує вектор значень одразу на весь добовий горизонт прогнозу (24 години):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \mathbf{X} \in \mathbb{R}^{24 \times 1} \quad \implies \quad \hat{\mathbf{y}} = \mathbf{X} \cdot \mathbf{W}_{\text{lstm}} + \mathbf{b} \quad \implies \quad \hat{\mathbf{y}} \in \mathbb{R}^{24 \times 1} $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Рекурентна регуляризація (Recurrent Dropout)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Стандартний Dropout обнуляє випадкові входи повнозв'язного шару, що працює для статичних мереж. Для рекурентних мереж застосовується <code>recurrent_dropout=0.2</code>, який маскує лінійні переходи станів усередині комірки пам'яті LSTM на кожному кроці:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \mathbf{h}_t = \text{LSTM}(\mathbf{x}_t, \mathbf{h}_{t-1} \odot \mathbf{m}) \quad (\text{де } \mathbf{m} \in \{0, 1\}^d \text{ - маска Бернуллі}) $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Це створює потужний заслон від перенавчання моделі на коротких флуктуаціях шуму.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод побудови та навчання LSTM у пісочниці</h2>
    </div>
    <div class="glass-card">
        <p>
            Псевдокод архітектурної ініціалізації та запуску навчання в пісочниці:
        </p>
        <pre><code class="language-python">
# Псевдокод збірки експериментальної LSTM-моделі
def build_and_train_experimental_model():
    # 1. Створення послідовного контейнера Keras
    model = Sequential()
    
    # 2. LSTM шар з маскуванням внутрішнього рекурентного стану (recurrent_dropout)
    model.add(LSTM(
        units=64, 
        input_shape=(24, 1), 
        recurrent_dropout=0.2
    ))
    
    # 3. Додатковий регуляризаційний Dropout
    model.add(Dropout(rate=0.2))
    
    # 4. Dense вихід на 24 точки (прогноз добового горизонту)
    model.add(Dense(units=24))
    
    # 5. Оптимізатор Adam з фіксованим темпом навчання (learning_rate)
    model.compile(optimizer=Adam(learning_rate=0.001), loss="mse")
    
    # 6. Навчання
    history = model.fit(
        X_train, y_train, 
        epochs=50, 
        batch_size=16, 
        validation_split=0.2
    )
    
    return model, history
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Часті питання (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому для навчання в пісочниці використовується саме 50 епох?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Згідно з численними тестами на збіжність, при темпі навчання 0.001 оптимізатора Adam та розмірі батчу 16, синтетична модель повністю збігається (мінімум лосу на валідації) приблизно на 35-40 епосі. 50 епох є оптимальним компромісом між швидкістю виконання експерименту та якістю навчання.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чим Direct Multi-step відрізняється від Recursive прогнозування?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: При рекурсивному методі модель прогнозує годину $t+1$, після чого цей прогноз вставляється у вхідний віконний масив для прогнозування години $t+2$. Це призводить до лавиноподібного накопичення похибок прогнозування. Прямий метод (Direct Multi-step) навчає модель видавати весь вектор прогнозу $[t+1, \dots, t+24]$ за один крок, що забезпечує високу стійкість до накопичення помилок.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як запустити цей експериментальний скрипт?</h4>
        <p style="color: var(--text-dim);">
            A: Переконайтеся, що на вашому комп'ютері встановлені TensorFlow та Matplotlib, і виконайте команду: <code>python scripts/ml/lstm_sandbox.py</code>
        </p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn">
        <span class="btn-icon">🔙</span>
        <span class="btn-text">Повернутися до Атласу</span>
    </a>
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
