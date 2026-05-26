# Технічний Паспорт Компонента: tests/test_pipeline.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🔗 END-TO-END DATA CHAIN VALIDATOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⛓️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">test_pipeline.py</h1>
            <p class="mega-subtitle">Система наскрізної інтеграційної перевірки: від фізичних законів джерела до 3D LSTM-тензорів</p>
            <div class="status-tags">
                <span class="tag tag-online">INTEGRATION SENTINEL</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">PIPELINE SHIELD</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🔄</div>
        <div class="metric-info">
            <span class="metric-label">Pipeline Type</span>
            <span class="metric-value">End-to-End (E2E)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧱</div>
        <div class="metric-info">
            <span class="metric-label">LSTM Reshape</span>
            <span class="metric-value">3D (1, 24, 9)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧬</div>
        <div class="metric-info">
            <span class="metric-label">Model Target</span>
            <span class="metric-value">V3 (9 Features)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📡</div>
        <div class="metric-info">
            <span class="metric-label">Data Mode</span>
            <span class="metric-value">Live Telemetry</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Системна інтеграція та роль E2E-тестування</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>tests/test_pipeline.py</code> є головним координаційним сенсором, який перевіряє **наскрізну цілісність ланцюга передавання даних** (End-to-End Data Pipeline) в межах проєкту <b>Energy Monitor Ultimate</b>. Він об'єднує в єдину логічну схему фізичні моделі генерації, базу даних PostgreSQL, низькорівневий векторизатор часових рядів та інтерфейси штучного інтелекту LSTM.
        </p>
        <p style="margin-top: 10px;">
            Критичні інтеграційні цілі модуля:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Синхронізація "Фізика -> БД -> ML":</strong> Доказ того, що математичні закони генерації сонячної енергії вночі (рівні 0.0) стабільно проходять через СУБД і коректно агрегуються векторизатором.</li>
            <li><strong>Цілісність ковзного вікна (Window Integrity):</strong> Валідація того, що зріз останніх 24 годин даних по будь-якій активній підстанції успішно перетворюється на матрицю ознак `(24, 9)` без втрати хронологічного порядку.</li>
            <li><strong>Топологічна сумісність нейромережі:</strong> Верифікація безпечного приведення матриць до 3D Keras-сумісної форми `(1, 24, 9)` через операцію reshape.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: END-TO-END DATAFLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Наскрізний ланцюг обробки даних (E2E Pipeline Execution Flow)</h2>
    </div>
    <div class="glass-card">
        <p>
            На схемі зображено наскрізний потік даних від фізичного моделювання до підготовки вхідного тензора ШІ:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                PHYSICS("Physics Simulator (Solar Output)") --> DB("PostgreSQL (LoadMeasurements Table)")
                DB --> VECT("Vectorizer: get_latest_window()")
                
                VECT --> FETCH_WINDOW{"Fetch window size = 24?"}
                FETCH_WINDOW -- "Insufficient data (<24 rows)" --> SKIP("pytest.skip: Skip test case")
                FETCH_WINDOW -- "Successful (24 rows)" --> CHECK_FEAT("Verify features list length = 9")
                
                CHECK_FEAT --> STRUCT_2D("2D Matrix: values.shape = (24, 9)")
                STRUCT_2D --> RESHAPE("Reshape: values.reshape(1, 24, 9)")
                RESHAPE --> STRUCT_3D("3D Tensor: shape = (1, 24, 9)")
                STRUCT_3D --> LSTM("LSTM Neural Inference Engine")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Аналіз тестових сценаріїв та специфікація ознак v3</h2>
    </div>
    <div class="glass-card">
        <p style="margin-bottom: 15px;">
            Тестування ланцюга даних складається з трьох ключових фаз:
        </p>
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Фізична нічна тиша (test_solar_physics_nighttime)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Перевіряє роботу сонячного генератора ПС Західна (ID 12), який має максимальну встановлену потужність $P_{\text{nom}} = 200.0$ МВт. О 02:00 ночі (за відсутності інсоляції) симуляція має генерувати строго нульовий вихід:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; font-family: monospace; color: var(--accent); margin-bottom: 8px;">
                    $$ G_{\text{solar}}(\text{02:00:00}) = 0.0 \text{ MW} $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Валідація вікна векторизатора (test_lstm_vectorizer_window_integrity)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Цей тест є ядром E2E. Він робить запит до реальної бази даних за допомогою функції <code>get_latest_window</code> для опорної підстанції <i>"ПС Київська-Центральна"</i> з режимом <code>source_type="Live"</code>. Очікується повернення 2D-матриці розміром `(24, 9)` та її безпечна конвертація у 3D LSTM-тензор:
                </p>
                <div style="font-family: monospace; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; display: inline-block; color: var(--text-main); font-size: 13px;">
                    tensor\_3d.shape == (1, 24, 9)
                </div>
                <p style="margin: 8px 0 0 0; font-size: 13.5px; color: var(--text-dim);">
                    Тест містить захисний механізм <code>pytest.skip</code> на випадок порожньої або нової бази даних, запобігаючи помилковим падінням (false failures).
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Контракт моделі V3 (test_vectorizer_v3_features_count)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Специфікація моделі версії **v3** вимагає наявності рівно **9 інформаційних ознак** у вхідному тензорі. Спрощення чи зміна цього переліку призведе до падіння матричного множення на шарах нейромережі.
                </p>
                <div style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; border: 1px solid var(--border); margin-top: 8px;">
                    <span class="tag tag-version" style="margin: 4px;">load</span>
                    <span class="tag tag-version" style="margin: 4px;">temp</span>
                    <span class="tag tag-version" style="margin: 4px;">h2</span>
                    <span class="tag tag-version" style="margin: 4px;">health</span>
                    <span class="tag tag-version" style="margin: 4px;">air</span>
                    <span class="tag tag-version" style="margin: 4px;">hour_sin</span>
                    <span class="tag tag-version" style="margin: 4px;">hour_cos</span>
                    <span class="tag tag-version" style="margin: 4px;">day_sin</span>
                    <span class="tag tag-version" style="margin: 4px;">day_cos</span>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод інтеграційного перетворення в 3D-тензор</h2>
    </div>
    <div class="glass-card">
        <p>
            Псевдокод демонструє процедуру отримання та форматування тензора, яка верифікується тестом:
        </p>
        <pre><code class="language-python">
# Псевдокод зрізу та конвертації тензора
def get_tensor_for_lstm(substation_name, window_size=24):
    # 1. Зчитування 2D масиву ознак з бази
    values, features = db.fetch_historical_matrix(substation_name, limit=window_size)
    
    if len(values) < window_size:
        raise InsufficientDataError()
        
    # 2. Формування форми (1, 24, 9)
    # 1: Batch Size (один прогнозний пробіг)
    # 24: Кількість часових кроків (Time Steps)
    # 9: Кількість ознак (Features Count)
    tensor_3d = values.reshape(1, window_size, len(features))
    return tensor_3d
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Що таке "ПС Західна (ID 12)" та звідки беруться ці паспортні константи?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Вони визначені в інженерному довіднику <code>src/services/simulation/generator_constants.py</code>. Це еталонні статичні параметри симулятора цифрового двійника. Завдяки цим константам ми можемо математично перевіряти роботу фізичного ядра без використання заглушок (mocking).
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому тест векторизатора пропускається, якщо в базі менше 24 записів?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Рекурентна LSTM-модель розраховує погодинний прогноз на наступні 24 години на основі *історичного контексту* за попередні 24 години. Якщо база даних абсолютно порожня (наприклад, одразу після розгортання порожнього контейнера), векторизатор не зможе сформувати повноцінне вікно розміром `24x9`. Пропуск тесту запобігає збоям збірки в CI/CD середовищах.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як запустити ці інтеграційні E2E тести?</h4>
        <p style="color: var(--text-dim);">
            A: Достатньо виконати команду у терміналі: <code>pytest tests/test_pipeline.py -v</code>
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
