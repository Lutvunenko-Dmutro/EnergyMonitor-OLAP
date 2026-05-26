# Технічна специфікація: Ядро Конфігурації та Типізації Додатка (APP CORE LOGIC) (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">📦 APPLICATION CORE | TYPES & CONFIG</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Ядро Додатка (app)</h1>
            <p class="mega-subtitle">Централізоване управління конфігурацією, типами даних та глобальними константами системи ATLAS, що забезпечує цілісність бізнес-логіки та стабільність обміну даними між шарами</p>
            <div class="status-tags">
                <span class="tag tag-online">CORE ACTIVE</span>
                <span class="tag tag-version">v2.6.0</span>
                <span class="tag tag-role">BASE LOGIC</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🆔</div>
        <div class="metric-info">
            <span class="metric-label">DataKeys</span>
            <span class="metric-value">Strict String Enums</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Strict Typing</span>
            <span class="metric-value">Dataclasses & TypedDict</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🤝</div>
        <div class="metric-info">
            <span class="metric-label">Data Contracts</span>
            <span class="metric-value">Zero-Null Handshake</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-info">
            <span class="metric-label">Static Analysis</span>
            <span class="metric-value">Mypy Compliant</span>
        </div>
    </div>
</div>

<!-- SECTION 01: ARCHITECTURAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Архітектурна Роль Ядра Додатка</h2></div>
    <div class="glass-card flow-step">
        <p>
            Пакет <code>src/app/</code> виконує роль архітектурного контракту (або "Конституції") системи ATLAS. Він визначає структури даних, правила взаємодії та глобальні константи, які є спільними для аналітичного ядра, ML-моделей та графічного інтерфейсу користувача. Замість використання небезпечних динамічних структур та "магічних рядків", пакет впроваджує строгу типізацію. Це гарантує цілісність даних на кордоні взаємодії підсистем та повністю усуває помилки неузгодженості інтерфейсів під час виконання.
        </p>
        <p style="margin-top: 10px;">
            Ключові компоненти пакета:
        </p>
        <ul>
            <li><strong>config.py (Global Config Registry):</strong> Визначає центральний клас <code>DataKeys</code>, що містить стандартизовані ключі доступу до словників стану (State Dictionaries), які використовуються для обміну інформацією між аналітикою та UI.</li>
            <li><strong>types.py (Type Definition Registry):</strong> Зберігає описи складних типів даних, аліасів та доменних моделей (наприклад, прогнози моделей <code>PredictionResult</code>, метрики <code>MetricsDict</code> та параметри фільтрації <code>FilterParams</code>).</li>
            <li><strong>__init__.py:</strong> Фасад пакета, що забезпечує чистий імпорт типів та констант для вищих рівнів системи.</li>
        </ul>
    </div>
</div>

<!-- SECTION 02: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Математичне представлення словників стану</h2></div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Контракт словника стану системи</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Глобальний словник стану $S$ визначається як відображення, що зіставляє кожен стандартизований ключ $k$ з відповідним об'єктом Pandas DataFrame $D$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ S = \{ (k, D_k) \mid k \in \mathcal{K}, \, D_k \in \mathbb{D}_{\text{DataFrame}} \} $$
                </div>
                <p style="margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);">
                    Де множина допустимих ключів доступу $\mathcal{K}$ жорстко зафіксована у класі <code>DataKeys</code>:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \mathcal{K} = \{ \text{"load"}, \, \text{"gen"}, \, \text{"alerts"}, \, \text{"lines"}, \, \text{"fin"} \} $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Формалізація AI-прогнозу (Prediction Tuple)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Кожен результат роботи нейромережевої моделі прогнозування представляє собою колінеарний кортеж $P_{\text{result}}$, який містить часовий ряд прогнозу, середньоквадратичну помилку RMSE та словник метаданих:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ P_{\text{result}} = \langle D_{\text{forecast}}, \, E_{\text{rmse}}, \, M_{\text{meta}} \rangle \quad \text{де } E_{\text{rmse}} \in \mathbb{R}^+, \, M_{\text{meta}} \in \text{Dict} $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 03: INTERACTION PIPELINE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема потоку типізованих об'єктів</h2></div>
    <div class="glass-card">
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph LR
                DB_RAW[("Raw DB Data")] --> CORE_READ["core.database: Read SQL"]
                CORE_READ --> SCH_VALID{"Валідація за types.py"}
                
                SCH_VALID -- "Невідповідність" --> ERR_VAL["Raise ValidationError / Logs"]
                SCH_VALID -- "Успішно (DataDict)" --> ML_ENG["ml.backtest: Predict Engine"]
                
                ML_ENG --> PRED_OUT["prediction: PredictionResult"]
                PRED_OUT --> UI_VIEW["ui.views: Render Charts / Tables"]
                
                CONFIG["config.py: DataKeys"] -- "Контроль доступу" --> UI_VIEW
                UI_VIEW --> DISPLAY["Cyber-HUD Streamlit GUI"]
            </div>
        </div>
    </div>
</div>

<!-- SECTION 04: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Приклад реалізації строгої типізації доменних моделей</h2></div>
    <div class="glass-card">
        <p>
            Псевдокод демонструє практичне застосування типів з <code>types.py</code> для забезпечення стійкої до збоїв обробки аналітичних даних та аліасів:
        </p>
        <pre><code class="language-python">
# Псевдокод з реалізації контрактів даних на основі src/app/types.py
from typing import Dict, List, Tuple, Union, Optional
import pandas as pd

# Визначення базових доменних типів
PredictionResult = Dict[str, Union[pd.DataFrame, float, dict]]
FilterParams = Dict[str, Union[str, Tuple[str, str], List[str], None]]

def process_lstm_forecast(
    raw_forecast: pd.DataFrame, 
    rmse_value: float, 
    substation_id: str
) -> PredictionResult:
    """
    Формує суворий контракт результату прогнозування для передачі в UI.
    Гарантує відсутність Null-значень та правильну структуру полів.
    """
    # Валідація наявності ключових колонок у DataFrame прогнозу
    expected_cols = {'Datetime', 'Forecast_MW', 'Lower_Bound', 'Upper_Bound'}
    actual_cols = set(raw_forecast.columns)
    
    if not expected_cols.issubset(actual_cols):
        raise ValueError(f"Missing columns in forecast DataFrame: {expected_cols - actual_cols}")
        
    # Формування об'єкта PredictionResult
    result: PredictionResult = {
        "forecast": raw_forecast,
        "rmse": float(rmse_value),
        "metadata": {
            "substation": str(substation_id),
            "generated_at": pd.Timestamp.now().isoformat(),
            "status": "VALIDATED"
        }
    }
    return result
        </code></pre>
    </div>
</div>

<!-- SECTION 05: TECHNICAL FAQ -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Технічний FAQ Ядра Додатка</h2></div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому замість Pydantic використовуються стандартні аліаси `Dict` та `Tuple` з `typing`?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Оскільки ядро ATLAS оперує великими об'єктами <code>pandas.DataFrame</code>, використання повноцінних Pydantic-моделей призвело б до значних накладних витрат на порядову валідацію мільйонів рядків телеметрії. Стандартні аліаси типу <code>DataDict = Dict[str, pd.DataFrame]</code> забезпечують бездоганну статичну перевірку типу (Mypy/Pyright) під час розробки з нульовим впливом на швидкість виконання (zero runtime overhead).
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Для чого потрібен клас `DataKeys` у `config.py`?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Клас <code>DataKeys</code> запобігає виникненню багів, пов'язаних з друкарськими помилками в рядках. Якщо в коді зчитування даних написати <code>state["loda"]</code> замість <code>state["load"]</code>, Python видасть помилку лише під час виконання. Використання константи <code>state[DataKeys.LOAD]</code> гарантує автодоповнення в IDE та виявлення будь-яких помилок на етапі статичного аналізу.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Яким чином типізація допомагає у тестуванні системи?</h4>
        <p style="color: var(--text-dim);">
            A: Завдяки суворим контрактам типів у <code>types.py</code>, ми можемо миттєво генерувати фікстури (Mock-дані) для юніт-тестів. Тестувальник точно знає структуру та типи очікуваних полів об'єкта <code>PredictionResult</code> або <code>AlertData</code>, що дозволяє автоматизувати верифікацію роботи як ML-моделей, так і UI-компонентів.
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
