# Технічна специфікація модуля: model_loader.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ML CORE ENGINE & RESOURCE REGISTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧠</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Resource Loader: model_loader</h1>
            <p class="mega-subtitle">Центральний вузол керування життєвим циклом ONNX-моделей (V1/V2/V3), Joblib-скейлерів та динамічного кешування ресурсів для оптимізованого інференсу.</p>
            <div class="status-tags"><span class="tag tag-online">CACHED INFERENCE</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">ML LOADER</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Inference Engine</span><span class="metric-value">ONNX Runtime</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">💾</div><div class="metric-info"><span class="metric-label">State Storage</span><span class="metric-value">Joblib Scalers</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧠</div><div class="metric-info"><span class="metric-label">Memory Control</span><span class="metric-value">st.cache_resource</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Fault Tolerance</span><span class="metric-value">CLI Fallback / DB Fallback</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>model_loader.py</b> відповідає за безпечне, кешоване та оптимізоване завантаження важких бінарних файлів ШІ-моделей (<code>.onnx</code>) та препроцесорів (<code>.pkl</code>). Його головна задача — гарантувати, що моделі завантажуються в оперативну пам'ять (RAM) <b>лише один раз</b> за сесію, запобігаючи витокам пам'яті (OOM errors) при використанні у веб-інтерфейсі (Streamlit).</p>
        <p style="margin-top: 12px;">Модуль забезпечує абстракцію над фізичними шляхами до моделей (V1, V2, V3) та надає стійкість до помилок: якщо Streamlit недоступний (запуск із CLI/cron), модуль безпечно ігнорує декоратори кешування (через <code>st_cache_resource_fallback</code>).</p>
    </div>
</div>

<!-- SECTION 02: RESOURCE REGISTRY -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Реєстр ШІ-ресурсів</h2></div>
    <div class="glass-card flow-step">
        <p style="margin-bottom: 15px; color: var(--text-dim);">Абсолютні шляхи та відображення конфігурацій (визначаються динамічно відносно <code>src/ml/models</code>):</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th style="padding: 8px; text-align: left;">Версія (ID)</th>
                    <th style="padding: 8px; text-align: left;">ONNX Модель</th>
                    <th style="padding: 8px; text-align: left;">Скейлер (Joblib)</th>
                    <th style="padding: 8px; text-align: left;">Опис</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><b>V1</b></td>
                    <td style="padding: 8px;"><code>substation_model_v1.onnx</code></td>
                    <td style="padding: 8px;"><code>scaler_v1.pkl</code></td>
                    <td style="padding: 8px;">Базова ARIMA/LSTM гібридна модель</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><b>V2</b></td>
                    <td style="padding: 8px;"><code>substation_model_v2.onnx</code></td>
                    <td style="padding: 8px;"><code>scaler_v2.pkl</code></td>
                    <td style="padding: 8px;">Мульти-таргетна (з телеметрією Twin)</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><b>V3</b></td>
                    <td style="padding: 8px;"><code>substation_model_v3_final.onnx</code><br><span style="color:var(--text-dim);font-size:11px;">Fallback: checkpoints/best_v3.onnx</span></td>
                    <td style="padding: 8px;"><code>scaler_v3_final.pkl</code></td>
                    <td style="padding: 8px;">Фінальна архітектура з 48h вікном</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def load_resources(version: str = "v3") → Tuple[Optional[ort.InferenceSession], Optional[Any]]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Головна функція завантаження моделі та скейлера. Кешується у RAM через <code>@st.cache_resource</code>. Включає перевірки цілісності (наявність файлів, наявність атрибутів <code>mean_</code> та <code>data_max_</code> у скейлері). Налаштовує ONNXRuntime на максимальну оптимізацію графа (<code>ORT_ENABLE_ALL</code>) з 1 потоком для стабільності у веб-воркерах.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def st_cache_resource_fallback(show_spinner=True) → Callable</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Декоратор-фабрика. Якщо Streamlit імпортовано успішно, повертає <code>st.cache_resource</code>. Якщо ні (запуск у cron, terminal), повертає функцію без змін. Це дозволяє використовувати один і той же код як у веб-додатку, так і в CLI-скриптах.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def _get_substation_peak_automated(name: Union[str, List[str]]) → float</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Автоматично витягує з БД історичний пік навантаження або ємність підстанції(й) для нормалізації прогнозів. У разі недоступності БД повертає hardcoded fallback значення (<code>5269.0</code>).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 04: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема завантаження (load_resources)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    CALL("load_resources(version='v3')") --> CACHE{Streamlit\nCache Hit?}
    CACHE -->|Yes| RETURN_RAM("Return from RAM")
    CACHE -->|No| CHECK("Check MODEL_REGISTRY")
    
    CHECK --> EXISTS{Files\nExist?}
    EXISTS -->|No| FALLBACK("Try 'v3_checkpoint'")
    FALLBACK --> EXISTS2{Exists?}
    EXISTS2 -->|No| ERR1("Return None, None\nLog Error")
    
    EXISTS -->|Yes| INIT_ORT("Init ONNX InferenceSession\n(ORT_ENABLE_ALL)")
    EXISTS2 -->|Yes| INIT_ORT
    
    INIT_ORT --> LOAD_SCL("joblib.load(scaler_path)")
    LOAD_SCL --> VAL_SCL{Has mean_ &\ndata_max_?}
    
    VAL_SCL -->|No| ERR2("Return None, None\nLog Corruption")
    VAL_SCL -->|Yes| SUCCESS("Cache in RAM\nReturn model, scaler")
    </div></div>
</div>

<!-- SECTION 05: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>onnxruntime</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>joblib</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit (Optional)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.utils.error_handlers</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database</span>
        </div>
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
