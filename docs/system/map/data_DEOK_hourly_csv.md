# Технічний Паспорт Активу: data/DEOK_hourly.csv (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">📊 HISTORICAL TIME-SERIES DATASET</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📊</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">DEOK_hourly.csv</h1>
            <p class="mega-subtitle">Локальний набір історичних даних погодинного навантаження енергосистеми Duke Energy Ohio & Kentucky (Цинциннаті та Північний Кентуккі, США)</p>
            <div class="status-tags">
                <span class="tag tag-online">DATASET ACTIVE</span>
                <span class="tag tag-version">v3.3.0</span>
                <span class="tag tag-role">TIME-SERIES NODE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📁</div>
        <div class="metric-info">
            <span class="metric-label">Format</span>
            <span class="metric-value">CSV (Plain Text)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-info">
            <span class="metric-label">File Size</span>
            <span class="metric-value">1.34 MB</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧬</div>
        <div class="metric-info">
            <span class="metric-label">Target Grid</span>
            <span class="metric-value">DEOK System (Ohio-Kentucky)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Primary Key</span>
            <span class="metric-value">Datetime Index</span>
        </div>
    </div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення та архітектурна роль</h2></div>
    <div class="glass-card flow-step">
        <p>
            Набір даних <code>data/DEOK_hourly.csv</code> містить довгостроковий погодинний архів споживання електроенергії в зоні покриття оператора <b>Duke Energy Ohio & Kentucky (DEOK)</b>. Ця зона охоплює метрополію Цинциннаті та північну частину Кентуккі, забезпечуючи життєдіяльність промислово розвиненого та густонаселеного регіону річки Огайо.
        </p>
        <p style="margin-top: 10px;">
            В архітектурі платформи ATLAS цей набір даних виконує роль критичного компонента для:
        </p>
        <ul>
            <li><strong>Model Training (Навчання ШІ):</strong> Виступає еталонною вибіркою для навчання глибоких рекурентних нейромереж (LSTM) та статистичних моделей (SARIMA).</li>
            <li><strong>Feature Engineering:</strong> Використовується векторним процесором <code>vectorizer.py</code> для побудови ретроспективних ознак (лагові значення, ковзні середні, сезонні профілі).</li>
            <li><strong>Model Validation & Benchmarking:</strong> Застосовується в модулі <code>benchmark_models.py</code> для розрахунку похибок прогнозування та порівняння точності алгоритмів на реальних даних.</li>
            <li><strong>Visual Analytics:</strong> Завантажується інтерфейсом користувача для відображення історичних трендів, сезонної декомпозиції та добових графіків навантаження.</li>
        </ul>
    </div>
</div>

<!-- SECTION 02: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичний опис структури часового ряду</h2></div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Математична формалізація часового ряду</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Історичний чамовий ряд $X$ представляється як впорядкована послідовність двовимірних векторів, де кожному моменту часу $T_t$ відповідає виміряна активна потужність споживання $L_t$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ X = \{ \mathbf{x}_t \}_{t=1}^{N}, \quad \mathbf{x}_t = \langle T_t, \, L_t \rangle \quad \text{де } L_t \in \mathbb{R}^+, \, T_t \in \text{Datetime} $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Метрики аналізу варіативності навантаження</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для оцінки стабільності та передбачуваності навантаження розраховується математичне очікування $\bar{L}$ та стандартне відхилення $\sigma$ ряду за період спостереження:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \bar{L} = \frac{1}{N} \sum_{t=1}^{N} L_t, \quad \sigma = \sqrt{\frac{1}{N-1} \sum_{t=1}^{N} (L_t - \bar{L})^2} $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: INTERACTION PIPELINE (DIAGRAM) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Життєвий цикл обробки датасету</h2></div>
    <div class="glass-card">
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                CSV_ON_DISK[("data/DEOK_hourly.csv")] --> PD_READ["pd.read_csv(usecols, parse_dates)"]
                PD_READ --> CLEAN_VAL["Очищення: Виявлення NaN та дублікатів часу"]
                
                CLEAN_VAL --> MEM_OPT["Memory Diet: Кастинг типів у float32"]
                MEM_OPT --> VECT["vectorizer.py: Генерація лагових ознак L(t-1), L(t-24)"]
                
                VECT --> ML_TRAIN["train_lstm.py: Навчання нейромережі LSTM"]
                VECT --> ARIMA_TRAIN["baseline_arima.py: Статистичний аналіз"]
                
                ML_TRAIN --> FORECAST_OUT["predict_v2.py: Формування прогнозів"]
                FORECAST_OUT --> UI_DASH["ui.views: Рендеринг чартів навантаження"]
            </div>
        </div>
    </div>
</div>

<!-- SECTION 04: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Псевдокод обробки та інтерполяції часових рядів</h2></div>
    <div class="glass-card">
        <p>
            Алгоритм демонструє процес очищення часового ряду, відновлення пропущених точок за допомогою кубічної інтерполяції та приведення типів для ML-навчання:
        </p>
        <pre><code class="language-python">
# Псевдокод обробки часового ряду DEOK
import pandas as pd
import numpy as np

def preprocess_deok_dataset(file_path: str) -> pd.DataFrame:
    # 1. Завантаження з диска з явним парсингом дат
    df = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')
    
    # 2. Виявлення та видалення дублікатів часу (збереження першого входження)
    df = df[~df.index.duplicated(keep='first')]
    
    # 3. Ресемплювання ряду до строгої годинної сітки (заповнення пропущених годин як NaN)
    df = df.resample('h').asfreq()
    
    # 4. Інтерполяція пропущених значень (кубічний сплайн для збереження фізичної гладкості)
    if df['DEOK_MW'].isnull().any():
        df['DEOK_MW'] = df['DEOK_MW'].interpolate(method='cubic')
        
    # 5. Оптимізація типів даних для мінімізації споживання RAM
    df['DEOK_MW'] = df['DEOK_MW'].astype(np.float32)
    
    return df
        </code></pre>
    </div>
</div>

<!-- SECTION 05: TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Технічний FAQ датасету DEOK</h2></div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Яка фізична специфіка споживання в регіоні DEOK (Duke Energy Ohio & Kentucky)?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Зона DEOK розташована на перетині кліматичних поясів, що зумовлює високу чутливість навантаження як до літніх температур, так і до зимових хвиль холоду. У цьому регіоні велика кількість важкої промисловості зосереджена вздовж долини річки Огайо (металургія, хімічні заводи), що забезпечує високий і стабільний базовий рівень навантаження (Base Load) протягом усього року.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Яким чином враховується вологість повітря та температурний індекс для прогнозування DEOK?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Оскільки Цинциннаті характеризується високою вологістю повітря влітку, проста температура повітря не повністю відображає навантаження кондиціонерів. Наша аналітична система може комбінувати дані навантаження з метеорологічним індексом THI (Temperature-Humidity Index): $THI = 0.8 \cdot T_d + (RH / 100) \cdot (T_d - 14.3) + 46.4$, де $T_d$ — температура сухого термометра (°C), а $RH$ — відносна вологість (%). Це дозволяє моделям точніше передбачати різкі стрибки споживання влітку.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як забезпечується стабільність моделей при роботі з порівняно невеликим файлом DEOK (1.34 MB)?</h4>
        <p style="color: var(--text-dim);">
            A: Невеликий розмір файлу обумовлений коротшим історичним періодом спостережень у порівнянні з іншими регіонами. Для запобігання перенавчанню (Overfitting) моделей LSTM на цій вибірці застосовуються додаткові шари регуляризації: Dropout зі значенням $0.2$, L2-вагова регуляризація (Weight Decay $= 10^{-4}$) та рання зупинка навчання (Early Stopping) при стабілізації втрат на валідаційній вибірці протягом 10 епох.
        </p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">Повернутися до Атласу</span></a>
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
