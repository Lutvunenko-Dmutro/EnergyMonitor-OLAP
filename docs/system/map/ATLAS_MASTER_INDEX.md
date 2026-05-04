# 🗺️ ATLAS SYSTEM MAP: ГОЛОВНИЙ РЕЄСТР ПАСПОРТІВ

<style>
:root {
    --bg: #0d1117;
    --card-bg: rgba(22, 27, 34, 0.8);
    --accent: #58a6ff;
    --accent-dim: rgba(88, 166, 255, 0.1);
    --border: #30363d;
    --text: #c9d1d9;
    --text-dim: #8b949e;
}

.mega-registry {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: var(--text);
    line-height: 1.6;
    max-width: 1200px;
    margin: 0 auto;
}

.hero-section {
    background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 60px 40px;
    margin-bottom: 40px;
    text-align: center;
    position: relative;
}

.mega-title {
    font-size: 3.5rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(to right, #fff, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hub-summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
    margin-bottom: 40px;
}

.hub-mini-card {
    background: var(--accent-dim);
    border: 1px solid var(--accent);
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    text-decoration: none !important;
}

.hub-mini-card:hover { background: rgba(88, 166, 255, 0.2); }

.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
}

.passport-links-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 12px;
    margin-top: 20px;
}

.passport-link-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px;
    text-decoration: none !important;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 10px;
}

.passport-link-card:hover {
    border-color: var(--accent);
    background: var(--accent-dim);
    transform: translateX(5px);
}

.p-icon { font-size: 1.2rem; }
.p-name { font-size: 0.9rem; font-weight: 600; color: var(--text); }
.p-desc { font-size: 0.7rem; color: var(--text-dim); display: block; }

.section-title {
    font-size: 1.5rem;
    color: var(--accent);
    border-bottom: 1px solid var(--border);
    padding-bottom: 10px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>

<div class="mega-registry">

<div class="hero-section">
    <h1 class="mega-title">Project ATLAS: Master Registry</h1>
    <p style="color: var(--text-dim); font-size: 1.1rem; margin-top: 15px;">
        Централізований інтерфейс документації. Всі модулі консолідовані в архітектурні Хаби для забезпечення 100% цілісності.
    </p>
</div>

<!-- MINI HUB NAVIGATION -->
<div class="hub-summary-grid">
    <a href="../core_kernel_hub/" class="hub-mini-card">🏗️ Kernel</a>
    <a href="../ml_core_engine/" class="hub-mini-card">🧠 ML Engine</a>
    <a href="../analysis_services_hub/" class="hub-mini-card">📊 Analytics</a>
    <a href="../data_services_hub/" class="hub-mini-card">🗄️ Data Hub</a>
    <a href="../diagnostics_engine_hub/" class="hub-mini-card">🛡️ Diagnostics</a>
    <a href="../simulation_engine_hub/" class="hub-mini-card">🎭 Simulation</a>
</div>

<!-- SECTION: CORE -->
<div class="glass-card">
    <div class="section-title"><span>🏗️</span> CORE & INFRASTRUCTURE</div>
    <div class="passport-links-grid">
        <a href="../core_kernel_hub/#main" class="passport-link-card"><span class="p-icon">⚙️</span><div><span class="p-name">main.py</span><span class="p-desc">Watchdog-оркестратор</span></div></a>
        <a href="../core_kernel_hub/#config" class="passport-link-card"><span class="p-icon">🔧</span><div><span class="p-name">config.py</span><span class="p-desc">Системні константи</span></div></a>
        <a href="../core_kernel_hub/#logger" class="passport-link-card"><span class="p-icon">📝</span><div><span class="p-name">logger.py</span><span class="p-desc">Ядро логування</span></div></a>
        <a href="../core_kernel_hub/#physics" class="passport-link-card"><span class="p-icon">⚛️</span><div><span class="p-name">physics.py</span><span class="p-desc">Фізичні моделі</span></div></a>
        <a href="../core_kernel_hub/#queries" class="passport-link-card"><span class="p-icon">🔍</span><div><span class="p-name">queries.py</span><span class="p-desc">SQL-репозиторій</span></div></a>
    </div>
</div>

<!-- SECTION: ML -->
<div class="glass-card">
    <div class="section-title"><span>🧠</span> MACHINE LEARNING HUB</div>
    <div class="passport-links-grid">
        <a href="../ml_core_engine/#predict-v2" class="passport-link-card"><span class="p-icon">🧬</span><div><span class="p-name">predict_v2.py</span><span class="p-desc">LSTM Рекурсія</span></div></a>
        <a href="../ml_core_engine/#backtest" class="passport-link-card"><span class="p-icon">🛡️</span><div><span class="p-name">backtest.py</span><span class="p-desc">Валідація на історії</span></div></a>
        <a href="../ml_core_engine/#vectorizer" class="passport-link-card"><span class="p-icon">🎡</span><div><span class="p-name">vectorizer.py</span><span class="p-desc">Feature Engineering</span></div></a>
        <a href="../ml_core_engine/#model-loader" class="passport-link-card"><span class="p-icon">📥</span><div><span class="p-name">model_loader.py</span><span class="p-desc">Завантажувач ONNX</span></div></a>
        <a href="../ml_core_engine/#metrics" class="passport-link-card"><span class="p-icon">📏</span><div><span class="p-name">metrics.py</span><span class="p-desc">Метрики точності</span></div></a>
    </div>
</div>

<!-- SECTION: DATA -->
<div class="glass-card">
    <div class="section-title"><span>🗄️</span> DATA SERVICES</div>
    <div class="passport-links-grid">
        <a href="../data_services_hub/#database" class="passport-link-card"><span class="p-icon">🔌</span><div><span class="p-name">database.py</span><span class="p-desc">PostgreSQL Driver</span></div></a>
        <a href="../data_services_hub/#db-seeder" class="passport-link-card"><span class="p-icon">🌱</span><div><span class="p-name">db_seeder.py</span><span class="p-desc">ETL-конвеєр</span></div></a>
        <a href="../data_services_hub/#archive" class="passport-link-card"><span class="p-icon">💾</span><div><span class="p-name">archive.py</span><span class="p-desc">Архівація даних</span></div></a>
        <a href="../data_services_hub/#loader" class="passport-link-card"><span class="p-icon">📥</span><div><span class="p-name">loader.py</span><span class="p-desc">Batch Loader</span></div></a>
    </div>
</div>

<!-- SECTION: INTEGRITY -->
<div class="glass-card">
    <div class="section-title" style="color: #a29bfe;"><span>🛡️</span> SYSTEM INTEGRITY & DIAGNOSTICS</div>
    <div class="passport-links-grid">
        <a href="../diagnostics_engine_hub/#scanner" class="passport-link-card"><span class="p-icon">📡</span><div><span class="p-name">scanner.py</span><span class="p-desc">DeepScan Engine</span></div></a>
        <a href="../diagnostics_engine_hub/#reporter" class="passport-link-card"><span class="p-icon">📊</span><div><span class="p-name">reporter.py</span><span class="p-desc">Audit Reporter</span></div></a>
        <a href="../diagnostics_engine_hub/#models" class="passport-link-card"><span class="p-icon">🧱</span><div><span class="p-name">models.py</span><span class="p-desc">Diag Schemas</span></div></a>
        <a href="../diagnostics_engine_hub/#patterns" class="passport-link-card"><span class="p-icon">🧩</span><div><span class="p-name">patterns.py</span><span class="p-desc">Vulnerability Signs</span></div></a>
    </div>
</div>

<!-- SECTION: SIMULATION -->
<div class="glass-card">
    <div class="section-title" style="color: #ffeaa7;"><span>🎭</span> SIMULATION ENGINE</div>
    <div class="passport-links-grid">
        <a href="../simulation_engine_hub/#generator" class="passport-link-card"><span class="p-icon">⚙️</span><div><span class="p-name">data_generator.py</span><span class="p-desc">Synthetic Loads</span></div></a>
        <a href="../simulation_engine_hub/#sensors" class="passport-link-card"><span class="p-icon">📡</span><div><span class="p-name">sensors.py</span><span class="p-desc">Virtual Sensors</span></div></a>
    </div>
</div>

<!-- SECTION: UI -->
<div class="glass-card">
    <div class="section-title" style="color: #55efc4;"><span>🎨</span> UI DASHBOARDS</div>
    <div class="passport-links-grid">
        <a href="../dashboard/" class="passport-link-card"><span class="p-icon">🏠</span><div><span class="p-name">dashboard.md</span><span class="p-desc">UI Оркестратор</span></div></a>
        <a href="../forecast_view/" class="passport-link-card"><span class="p-icon">🔮</span><div><span class="p-name">forecast.md</span><span class="p-desc">AI Forecast HUD</span></div></a>
        <a href="../map_view/" class="passport-link-card"><span class="p-icon">🗺️</span><div><span class="p-name">map_view.md</span><span class="p-desc">Гео-мапа активів</span></div></a>
        <a href="../consumption_view/" class="passport-link-card"><span class="p-icon">📈</span><div><span class="p-name">consumption.md</span><span class="p-desc">Аналіз споживання</span></div></a>
        <a href="../historical_audit_view/" class="passport-link-card"><span class="p-icon">📜</span><div><span class="p-name">audit.md</span><span class="p-desc">Цифровий архів</span></div></a>
    </div>
</div>

</div>
