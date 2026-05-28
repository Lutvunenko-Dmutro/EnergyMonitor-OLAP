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
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 15px;
    margin-top: 20px;
}

.passport-link-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 15px;
    text-decoration: none !important;
    transition: all 0.2s ease;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.passport-link-card:hover {
    border-color: var(--accent);
    background: var(--accent-dim);
    transform: translateX(5px);
}

.p-icon { font-size: 1.5rem; margin-top: 2px; }
.p-text { display: flex; flex-direction: column; overflow: hidden; }
.p-name { font-size: 0.95rem; font-weight: 600; color: var(--accent); margin-bottom: 4px; word-break: break-all; }
.p-desc { font-size: 0.75rem; color: var(--text-dim); line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
    margin-bottom: 25px;
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>

<div class="mega-registry">

<div class="hero-section">
    <h1 class="mega-title">Project ATLAS: Master Registry</h1>
    <p style="color: var(--text-dim); font-size: 1.1rem; margin-top: 15px;">
        Централізований інтерфейс документації. Всі модулі організовано за парадигмою '1-to-1 Passport Mapping'.
    </p>
</div>

<!-- SECTION: NAMESPACES -->
<div class="glass-card">
    <div class="section-title" style="color: #0984e3;">📦 SYSTEM NAMESPACES & CONFIG</div>
    <div class="passport-links-grid">
        <a href="../__init__/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/core/analytics/__init__.py</span><span class="p-desc">Універсальний диспетчер ініціалізації...</span></div></a>
        <a href="../app_config/" class="passport-link-card"><span class="p-icon">⚙️</span><div class="p-text"><span class="p-name">src/app/config.py</span><span class="p-desc">Централізоване сховище констант та кл...</span></div></a>
        <a href="../app_init/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/app/__init__.py</span><span class="p-desc">Кореневий вузол рівня додатка, що виз...</span></div></a>
        <a href="../config/" class="passport-link-card"><span class="p-icon">⚙️</span><div class="p-text"><span class="p-name">config</span><span class="p-desc">Центральний реєстр параметрів конверт...</span></div></a>
        <a href="../constants/" class="passport-link-card"><span class="p-icon">⚙️</span><div class="p-text"><span class="p-name">src/ui/views/forecast_components/constants.py</span><span class="p-desc">Централізоване сховище текстових міто...</span></div></a>
        <a href="../core_config/" class="passport-link-card"><span class="p-icon">⚙️</span><div class="p-text"><span class="p-name">src/core/config.py</span><span class="p-desc">Центральний модуль для управління пар...</span></div></a>
        <a href="../core_init/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/core/__init__.py</span><span class="p-desc">Пакет системного ядра. Містить фундам...</span></div></a>
        <a href="../database_init/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/core/database/__init__.py</span><span class="p-desc">Рівень доступу до даних. Надає відмов...</span></div></a>
        <a href="../generator_constants/" class="passport-link-card"><span class="p-icon">⚙️</span><div class="p-text"><span class="p-name">src/services/simulation/generator_constants.py</span><span class="p-desc">Технічний паспорт об'єктів енергосист...</span></div></a>
        <a href="../logging_config/" class="passport-link-card"><span class="p-icon">⚙️</span><div class="p-text"><span class="p-name">src/utils/logging_config.py</span><span class="p-desc">Централізований модуль системи спосте...</span></div></a>
        <a href="../root_init/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/__init__.py</span><span class="p-desc">Головний пакет системи ATLAS. Виконує...</span></div></a>
        <a href="../services_init/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/services/__init__.py</span><span class="p-desc">Сервісний рівень системи. Об'єднує фу...</span></div></a>
        <a href="../ui_charts_library_index/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/ui/components/charts/__init__.py</span><span class="p-desc">Центральний хаб візуалізації проєкту ...</span></div></a>
        <a href="../ui_components_init/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/ui/components/__init__.py</span><span class="p-desc">Бібліотека спільних UI-компонентів. З...</span></div></a>
        <a href="../ui_init/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/ui/__init__.py</span><span class="p-desc">Пакет представлення та візуалізації. ...</span></div></a>
        <a href="../ui_views_registry/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/ui/views/__init__.py</span><span class="p-desc">Центральний пакетний хаб аналітичних ...</span></div></a>
        <a href="../utils_init/" class="passport-link-card"><span class="p-icon">📦</span><div class="p-text"><span class="p-name">src/utils/__init__.py</span><span class="p-desc">Пакет допоміжних утиліт. Набір інстру...</span></div></a>
    </div>
</div>

<!-- SECTION: CORE -->
<div class="glass-card">
    <div class="section-title" style="color: #fdcb6e;">⚙️ CORE LOGIC & PHYSICS</div>
    <div class="passport-links-grid">
        <a href="../aggregator/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/core/analytics/aggregator.py</span><span class="p-desc">Високопродуктивна обробка, ресемплінг...</span></div></a>
        <a href="../filter/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/core/analytics/filter.py</span><span class="p-desc">Забезпечення безпечної, валідованої т...</span></div></a>
        <a href="../formulas/" class="passport-link-card"><span class="p-icon">⚛️</span><div class="p-text"><span class="p-name">formulas</span><span class="p-desc">Двигун математичної трансформації, OL...</span></div></a>
        <a href="../main/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">main</span><span class="p-desc">Високорівнева оркестрація життєвого ц...</span></div></a>
        <a href="../physics/" class="passport-link-card"><span class="p-icon">⚛️</span><div class="p-text"><span class="p-name">src/core/physics.py</span><span class="p-desc">Ядро фізико-математичного моделювання...</span></div></a>
        <a href="../queries/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/core/queries.py</span><span class="p-desc">Централізована бібліотека SQL-рядків ...</span></div></a>
    </div>
</div>

<!-- SECTION: DB_DATA -->
<div class="glass-card">
    <div class="section-title" style="color: #e17055;">🗄️ DATABASE & RAW DATA</div>
    <div class="passport-links-grid">
        <a href="../archive/" class="passport-link-card"><span class="p-icon">🗄️</span><div class="p-text"><span class="p-name">src/core/database/archive.py</span><span class="p-desc">Механізм ретроспективних запитів. Зді...</span></div></a>
        <a href="../check_db_stats/" class="passport-link-card"><span class="p-icon">🗄️</span><div class="p-text"><span class="p-name">check_db_stats</span><span class="p-desc">Утиліта глибокого аудиту фізичного об...</span></div></a>
        <a href="../data_AEP_hourly_csv/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_AEP_hourly_csv</span><span class="p-desc">Локальний набір історичних даних пого...</span></div></a>
        <a href="../data_COMED_hourly_csv/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_COMED_hourly_csv</span><span class="p-desc">Локальний набір історичних даних пого...</span></div></a>
        <a href="../data_DAYTON_hourly_csv/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_DAYTON_hourly_csv</span><span class="p-desc">Локальний набір історичних даних пого...</span></div></a>
        <a href="../data_DEOK_hourly_csv/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_DEOK_hourly_csv</span><span class="p-desc">Локальний набір історичних даних пого...</span></div></a>
        <a href="../data_DOM_hourly_csv/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_DOM_hourly_csv</span><span class="p-desc">Локальний набір історичних даних пого...</span></div></a>
        <a href="../data_DUQ_hourly_csv/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_DUQ_hourly_csv</span><span class="p-desc">Локальний набір історичних даних пого...</span></div></a>
        <a href="../data_EKPC_hourly_csv/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_EKPC_hourly_csv</span><span class="p-desc">Локальний набір історичних даних пого...</span></div></a>
        <a href="../data_FE_hourly_csv/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_FE_hourly_csv</span><span class="p-desc">Локальний набір історичних даних пого...</span></div></a>
        <a href="../data_NI_hourly_csv/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_NI_hourly_csv</span><span class="p-desc">Локальний набір історичних даних пого...</span></div></a>
        <a href="../data_PJME_hourly_csv/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_PJME_hourly_csv</span><span class="p-desc">Локальний набір історичних даних пого...</span></div></a>
        <a href="../data_energy_db/" class="passport-link-card"><span class="p-icon">🗄️</span><div class="p-text"><span class="p-name">data_energy_db</span><span class="p-desc">Локальне реляційне сховище телеметрії...</span></div></a>
        <a href="../db_seeder/" class="passport-link-card"><span class="p-icon">🗄️</span><div class="p-text"><span class="p-name">src/services/data/db_seeder.py</span><span class="p-desc">Повноцикловий конвеєр розгортання та ...</span></div></a>
        <a href="../db_services/" class="passport-link-card"><span class="p-icon">🗄️</span><div class="p-text"><span class="p-name">src/services/data/db_services.py</span><span class="p-desc">Високорівневий рівень бізнес-логіки д...</span></div></a>
        <a href="../loader/" class="passport-link-card"><span class="p-icon">🗄️</span><div class="p-text"><span class="p-name">src/core/database/loader.py</span><span class="p-desc">Центральний вузол управління життєвим...</span></div></a>
        <a href="../lstm_sandbox/" class="passport-link-card"><span class="p-icon">🗄️</span><div class="p-text"><span class="p-name">lstm_sandbox</span><span class="p-desc">Лабораторія ШІ-експериментів, швидког...</span></div></a>
        <a href="../migrate_db/" class="passport-link-card"><span class="p-icon">🗄️</span><div class="p-text"><span class="p-name">src/services/data/migrate_db.py</span><span class="p-desc">Двигун безпечної еволюції схеми Postg...</span></div></a>
        <a href="../sensors_db/" class="passport-link-card"><span class="p-icon">🗄️</span><div class="p-text"><span class="p-name">src/services/simulation/sensors_db.py</span><span class="p-desc">Фоновий процес (Subprocess) для симул...</span></div></a>
        <a href="../test_database/" class="passport-link-card"><span class="p-icon">🗄️</span><div class="p-text"><span class="p-name">test_database</span><span class="p-desc">Система верифікації цілісності схеми ...</span></div></a>
    </div>
</div>

<!-- SECTION: UI_VIEWS -->
<div class="glass-card">
    <div class="section-title" style="color: #00b894;">🖥️ UI DASHBOARDS & VIEWS</div>
    <div class="passport-links-grid">
        <a href="../SUMMARY_DASHBOARD/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">SUMMARY_DASHBOARD</span><span class="p-desc">Оркестратор фінальної звітності проєк...</span></div></a>
        <a href="../advanced/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/advanced.py</span><span class="p-desc">Диспетчер поглибленої аналітики. Розп...</span></div></a>
        <a href="../advanced_ai_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">advanced_ai_view</span><span class="p-desc">Система інтелектуальної сегментації м...</span></div></a>
        <a href="../advanced_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">advanced_view</span><span class="p-desc">Інтелектуальна підсистема декомпозиці...</span></div></a>
        <a href="../alerts_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/alerts.py</span><span class="p-desc">Централізований високопродуктивний ін...</span></div></a>
        <a href="../audit_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">audit_view</span><span class="p-desc">Система поглибленого ретроспективного...</span></div></a>
        <a href="../audits/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/forecast_components/audits.py</span><span class="p-desc">Підсистема глибинного аналізу точност...</span></div></a>
        <a href="../clustering_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/advanced_components/clustering_view.py</span><span class="p-desc">Графічне представлення результатів AI...</span></div></a>
        <a href="../consumption_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/consumption.py</span><span class="p-desc">Універсальний аналітичний двигун візу...</span></div></a>
        <a href="../dashboard/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">dashboard</span><span class="p-desc">Багатопотоковий графічний пульт управ...</span></div></a>
        <a href="../data_table/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/historical_audit_components/data_table.py</span><span class="p-desc">Інтерфейс для детального перегляду та...</span></div></a>
        <a href="../engine/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/forecast_components/engine.py</span><span class="p-desc">Ядро трансляції та верстки, інтелекту...</span></div></a>
        <a href="../finance_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/finance.py</span><span class="p-desc">Економічний монітор та двигун фізико-...</span></div></a>
        <a href="../forecast/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/forecast.py</span><span class="p-desc">Головний інтерфейсний модуль для взає...</span></div></a>
        <a href="../forecast_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">forecast_view</span><span class="p-desc">Головний вебаналітичний інтерфейс ATL...</span></div></a>
        <a href="../generation_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/generation.py</span><span class="p-desc">Багатовимірний монітор джерел енергії...</span></div></a>
        <a href="../grid/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/forecast_components/grid.py</span><span class="p-desc">Забезпечує пакетний рендеринг прогноз...</span></div></a>
        <a href="../header/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/forecast_components/header.py</span><span class="p-desc">Інтерактивна панель налаштування прог...</span></div></a>
        <a href="../historical_audit_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/historical_audit.py</span><span class="p-desc">Центр глибокої ретроспективної аналіт...</span></div></a>
        <a href="../kpi_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/kpi.py</span><span class="p-desc">Високотехнологічний центр контролю кл...</span></div></a>
        <a href="../layouts/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/forecast_components/layouts.py</span><span class="p-desc">Оркестратор представлення. Керує скла...</span></div></a>
        <a href="../map_view/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/views/map.py</span><span class="p-desc">Високопродуктивна інтерактивна систем...</span></div></a>
        <a href="../sidebar/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">sidebar</span><span class="p-desc">Головний інтерфейсний вузол для керув...</span></div></a>
        <a href="../splash/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">splash</span><span class="p-desc">Інтерактивна заставка завантаження у ...</span></div></a>
        <a href="../trend_view/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">src/ui/views/advanced_components/trend_view.py</span><span class="p-desc">Розбиває сигнал навантаження на компо...</span></div></a>
        <a href="../ui_dashboard_layout/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/segments/dashboard.py</span><span class="p-desc">Центральний хаб візуалізації проєкту ...</span></div></a>
        <a href="../ui_sidebar_controls/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/ui/segments/sidebar.py</span><span class="p-desc">Головний інтерфейсний вузол керування...</span></div></a>
        <a href="../ui_splash_screen/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/ui/segments/splash.py</span><span class="p-desc">Система візуального завантаження проє...</span></div></a>
    </div>
</div>

<!-- SECTION: UI_COMP -->
<div class="glass-card">
    <div class="section-title" style="color: #55efc4;">🎨 UI COMPONENTS & CHARTS</div>
    <div class="passport-links-grid">
        <a href="../academic_charts/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">academic_charts</span><span class="p-desc">Система наукового обґрунтування резул...</span></div></a>
        <a href="../base_charts/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">base_charts</span><span class="p-desc">Фундамент візуальної аналітики: уніфі...</span></div></a>
        <a href="../cards/" class="passport-link-card"><span class="p-icon">🃏</span><div class="p-text"><span class="p-name">cards</span><span class="p-desc">Бібліотека інтерактивних карток та ін...</span></div></a>
        <a href="../deployment_ops_guide/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">deployment_ops_guide</span><span class="p-desc">Керівництво з операційної готовності:...</span></div></a>
        <a href="../forecast_plots/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">forecast_plots</span><span class="p-desc">Рушій візуалізації прогнозів машинног...</span></div></a>
        <a href="../forecast_ui_plots/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">forecast_ui_plots</span><span class="p-desc">Система візуалізації майбутнього: рен...</span></div></a>
        <a href="../plots/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">src/ml/utils/plots.py</span><span class="p-desc">Проста утиліта на базі Matplotlib для...</span></div></a>
        <a href="../styles/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">styles</span><span class="p-desc">Двигун академічного стилю та верстки,...</span></div></a>
        <a href="../test_plots/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">test_plots</span><span class="p-desc">Утиліта автономного калібрування граф...</span></div></a>
        <a href="../ui_cards/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">ui_cards</span><span class="p-desc">Система мікро-візуалізації стану мере...</span></div></a>
        <a href="../ui_cards_library/" class="passport-link-card"><span class="p-icon">🃏</span><div class="p-text"><span class="p-name">src/ui/components/cards.py</span><span class="p-desc">Набір компактних візуальних елементів...</span></div></a>
        <a href="../ui_charts/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">ui_charts</span><span class="p-desc">Уніфікована система візуалізації часо...</span></div></a>
        <a href="../ui_charts_academic/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">src/ui/components/charts/academic.py</span><span class="p-desc">Спеціалізований модуль візуалізації н...</span></div></a>
        <a href="../ui_charts_base/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">src/ui/components/charts/base.py</span><span class="p-desc">Фундаментальний двигун графічної анал...</span></div></a>
        <a href="../ui_charts_forecast/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">src/ui/components/charts/forecast_plots.py</span><span class="p-desc">Ядро графічного відображення ШІ-модел...</span></div></a>
        <a href="../ui_design_system/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/ui/components/styles.py</span><span class="p-desc">Ядро візуальної ідентичності проєкту ...</span></div></a>
        <a href="../ui_helpers/" class="passport-link-card"><span class="p-icon">🖥️</span><div class="p-text"><span class="p-name">src/utils/ui_helpers.py</span><span class="p-desc">Єдина точка рендерингу Plotly-графікі...</span></div></a>
        <a href="../ui_live_kpi_segment/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/ui/segments/live_kpi.py</span><span class="p-desc">Високопродуктивний оркестратор реальн...</span></div></a>
    </div>
</div>

<!-- SECTION: ML -->
<div class="glass-card">
    <div class="section-title" style="color: #a29bfe;">🧠 MACHINE LEARNING & AI</div>
    <div class="passport-links-grid">
        <a href="../backtest/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">src/ml/backtest.py</span><span class="p-desc">Механізм верифікації моделей машинног...</span></div></a>
        <a href="../baseline_arima/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/ml/baseline_arima.py</span><span class="p-desc">Наукова база для обґрунтування перева...</span></div></a>
        <a href="../benchmark_models/" class="passport-link-card"><span class="p-icon">🧠</span><div class="p-text"><span class="p-name">benchmark_models</span><span class="p-desc">Двигун академічного бенчмаркінгу моде...</span></div></a>
        <a href="../clustering/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/core/analytics/clustering.py</span><span class="p-desc">Інтелектуальна сегментація енергооб'є...</span></div></a>
        <a href="../forecast_controller/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/ml/forecast_controller.py</span><span class="p-desc">Диспетчер між UI-шаром та ML-моделями...</span></div></a>
        <a href="../metrics_engine/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/ml/metrics_engine.py</span><span class="p-desc">Реалізує комплексний апарат математич...</span></div></a>
        <a href="../ml_assets_architecture/" class="passport-link-card"><span class="p-icon">🧠</span><div class="p-text"><span class="p-name">ml_assets_architecture</span><span class="p-desc">Реєстр інтелектуальних ресурсів ATLAS...</span></div></a>
        <a href="../model_loader/" class="passport-link-card"><span class="p-icon">🧠</span><div class="p-text"><span class="p-name">src/ml/model_loader.py</span><span class="p-desc">Центральний вузол керування життєвим ...</span></div></a>
        <a href="../models/" class="passport-link-card"><span class="p-icon">🧠</span><div class="p-text"><span class="p-name">src/core/diagnostics/models.py</span><span class="p-desc">Визначає базові структури даних (Data...</span></div></a>
        <a href="../predict_v2/" class="passport-link-card"><span class="p-icon">🧠</span><div class="p-text"><span class="p-name">src/ml/predict_v2.py</span><span class="p-desc">Високонадійний конвеєр предиктивної а...</span></div></a>
        <a href="../test_ml_model/" class="passport-link-card"><span class="p-icon">🧠</span><div class="p-text"><span class="p-name">test_ml_model</span><span class="p-desc">Система верифікації LSTM нейромереж, ...</span></div></a>
        <a href="../train_lstm/" class="passport-link-card"><span class="p-icon">🧠</span><div class="p-text"><span class="p-name">src/ml/train_lstm.py</span><span class="p-desc">Автоматизований конвеєр навчання глиб...</span></div></a>
        <a href="../train_v1/" class="passport-link-card"><span class="p-icon">🧠</span><div class="p-text"><span class="p-name">src/ml/train_v1.py</span><span class="p-desc">Тренувальний скрипт для базової модел...</span></div></a>
        <a href="../vectorizer/" class="passport-link-card"><span class="p-icon">🧠</span><div class="p-text"><span class="p-name">src/ml/vectorizer.py</span><span class="p-desc">Трансформація часових рядів у тензори...</span></div></a>
    </div>
</div>

<!-- SECTION: SERVICES -->
<div class="glass-card">
    <div class="section-title" style="color: #ff7675;">🛠️ SYSTEM SERVICES & GENERATORS</div>
    <div class="passport-links-grid">
        <a href="../advanced_mining/" class="passport-link-card"><span class="p-icon">🛠️</span><div class="p-text"><span class="p-name">src/services/analysis/advanced_mining.py</span><span class="p-desc">Сервіс поглибленого інтелектуального ...</span></div></a>
        <a href="../analytics_advanced/" class="passport-link-card"><span class="p-icon">🛠️</span><div class="p-text"><span class="p-name">src/services/analysis/analytics_advanced.py</span><span class="p-desc">Автономний аналітичний сервіс (Data M...</span></div></a>
        <a href="../automated_intersection_tester/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">src/services/analysis/automated_intersection_tester.py</span><span class="p-desc">Модуль автоматизованого верифікаційно...</span></div></a>
        <a href="../core_kaggle_loader/" class="passport-link-card"><span class="p-icon">🛠️</span><div class="p-text"><span class="p-name">src/core/kaggle_loader.py</span><span class="p-desc">Автоматизований ETL-конвеєр проекту A...</span></div></a>
        <a href="../data_generator/" class="passport-link-card"><span class="p-icon">🛠️</span><div class="p-text"><span class="p-name">src/services/simulation/data_generator.py</span><span class="p-desc">Ядро системи для імітації роботи енер...</span></div></a>
        <a href="../diag_columns/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">src/services/analysis/diag_columns.py</span><span class="p-desc">Утиліта прямого доступу для діагности...</span></div></a>
        <a href="../import_real_data/" class="passport-link-card"><span class="p-icon">🛠️</span><div class="p-text"><span class="p-name">src/services/data/import_real_data.py</span><span class="p-desc">Сервіс інтеграції зовнішніх історични...</span></div></a>
        <a href="../kaggle_loader/" class="passport-link-card"><span class="p-icon">🛠️</span><div class="p-text"><span class="p-name">kaggle_loader</span><span class="p-desc">Автоматизований імпорт, стандартизаці...</span></div></a>
        <a href="../sensors/" class="passport-link-card"><span class="p-icon">🛠️</span><div class="p-text"><span class="p-name">src/services/simulation/sensors.py</span><span class="p-desc">Програмна імітація фізичних датчиків高...</span></div></a>
        <a href="../sensors_service/" class="passport-link-card"><span class="p-icon">🛠️</span><div class="p-text"><span class="p-name">sensors_service</span><span class="p-desc">Імітація фізичних датчиків високоволь...</span></div></a>
        <a href="../trends_and_patterns/" class="passport-link-card"><span class="p-icon">📈</span><div class="p-text"><span class="p-name">src/services/analysis/trends_and_patterns.py</span><span class="p-desc">Дослідження циклічних закономірностей...</span></div></a>
    </div>
</div>

<!-- SECTION: DIAGNOSTICS -->
<div class="glass-card">
    <div class="section-title" style="color: #d63031;">🛡️ DIAGNOSTICS & AUDIT</div>
    <div class="passport-links-grid">
        <a href="../AUDIT_REPORT/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">AUDIT_REPORT</span><span class="p-desc">Документ</span></div></a>
        <a href="../audit_data/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">audit_data</span><span class="p-desc">Спеціалізований аудитор цілісності на...</span></div></a>
        <a href="../conftest/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">conftest</span><span class="p-desc">Оркестратор тестового середовища, ізо...</span></div></a>
        <a href="../deep_ai_check/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">deep_ai_check</span><span class="p-desc">Нейронний детектор авторства, трансфо...</span></div></a>
        <a href="../diagnose/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">diagnose</span><span class="p-desc">Оркестратор автоматизованого аудиту к...</span></div></a>
        <a href="../historical_audit/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">historical_audit</span><span class="p-desc">Панель цифрового архіву з підтримкою ...</span></div></a>
        <a href="../patterns/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">src/core/diagnostics/patterns.py</span><span class="p-desc">Централізоване сховище евристичних пр...</span></div></a>
        <a href="../quality_check/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">quality_check</span><span class="p-desc">Система інтелектуального аудиту верст...</span></div></a>
        <a href="../reporter/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">src/core/diagnostics/reporter.py</span><span class="p-desc">Трансформує результати технічного ауд...</span></div></a>
        <a href="../run_backtest_diag/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">run_backtest_diag</span><span class="p-desc">Утиліта експрес-діагностики бектестів...</span></div></a>
        <a href="../scanner/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">src/core/diagnostics/scanner.py</span><span class="p-desc">Рекурсивний аудит кодової бази за доп...</span></div></a>
        <a href="../stylometry_check/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">stylometry_check</span><span class="p-desc">Система стилометричного контролю, ана...</span></div></a>
        <a href="../test_core_analytics/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">test_core_analytics</span><span class="p-desc">Система верифікації математичної точн...</span></div></a>
        <a href="../test_physics/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">test_physics</span><span class="p-desc">Система верифікації фізичних обмежень...</span></div></a>
        <a href="../test_pipeline/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">test_pipeline</span><span class="p-desc">Система наскрізної інтеграційної пере...</span></div></a>
        <a href="../test_security/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">test_security</span><span class="p-desc">Система аудиту безпеки: захист від SQ...</span></div></a>
        <a href="../test_utils/" class="passport-link-card"><span class="p-icon">🛡️</span><div class="p-text"><span class="p-name">test_utils</span><span class="p-desc">Система верифікації допоміжних утиліт...</span></div></a>
    </div>
</div>

<!-- SECTION: UTILS -->
<div class="glass-card">
    <div class="section-title" style="color: #00cec9;">🔧 UTILITIES & HELPERS</div>
    <div class="passport-links-grid">
        <a href="../cache_management_engine/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">cache_management_engine</span><span class="p-desc">Система низькорівневого управління ст...</span></div></a>
        <a href="../cache_manager/" class="passport-link-card"><span class="p-icon">🔧</span><div class="p-text"><span class="p-name">src/utils/cache_manager.py</span><span class="p-desc">Автоматичне управління життєвим цикло...</span></div></a>
        <a href="../error_handlers/" class="passport-link-card"><span class="p-icon">🔧</span><div class="p-text"><span class="p-name">src/utils/error_handlers.py</span><span class="p-desc">Шар відмовостійкості. Забезпечує захи...</span></div></a>
        <a href="../handlers/" class="passport-link-card"><span class="p-icon">🔧</span><div class="p-text"><span class="p-name">handlers</span><span class="p-desc">Бібліотека обробників структурних еле...</span></div></a>
        <a href="../helpers/" class="passport-link-card"><span class="p-icon">🔧</span><div class="p-text"><span class="p-name">src/utils/helpers.py</span><span class="p-desc">Глобальна збірка універсальних інстру...</span></div></a>
        <a href="../logger/" class="passport-link-card"><span class="p-icon">📝</span><div class="p-text"><span class="p-name">src/core/logger.py</span><span class="p-desc">Централізована реєстрація подій, моні...</span></div></a>
        <a href="../memory_helper/" class="passport-link-card"><span class="p-icon">🔧</span><div class="p-text"><span class="p-name">src/utils/memory_helper.py</span><span class="p-desc">Забезпечує стабільність додатка. Проа...</span></div></a>
        <a href="../universal_system_helpers/" class="passport-link-card"><span class="p-icon">🔧</span><div class="p-text"><span class="p-name">universal_system_helpers</span><span class="p-desc">Швейцарський ніж проекту ATLAS: інстр...</span></div></a>
        <a href="../utils_extended_toolkit/" class="passport-link-card"><span class="p-icon">🔧</span><div class="p-text"><span class="p-name">utils_extended_toolkit</span><span class="p-desc">Централізована бібліотека допоміжних ...</span></div></a>
        <a href="../utils_validators/" class="passport-link-card"><span class="p-icon">🔧</span><div class="p-text"><span class="p-name">src/utils/validators.py</span><span class="p-desc">Шар кіберзахисту та цілісності даних ...</span></div></a>
        <a href="../validators/" class="passport-link-card"><span class="p-icon">🔧</span><div class="p-text"><span class="p-name">validators</span><span class="p-desc">Багатошаровий захист від SQL-ін'єкцій...</span></div></a>
    </div>
</div>

<!-- SECTION: DOCS -->
<div class="glass-card">
    <div class="section-title" style="color: #b2bec3;">📚 SYSTEM DOCS & GUIDES</div>
    <div class="passport-links-grid">
        <a href="../academic/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">academic</span><span class="p-desc">Візуалізатор академічної звітності. Р...</span></div></a>
        <a href="../alerts/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">alerts</span><span class="p-desc">Централізований інтерфейс для монітор...</span></div></a>
        <a href="../appendix/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">appendix</span><span class="p-desc">Генератор технічних додатків, автомат...</span></div></a>
        <a href="../atlas_server/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">atlas_server</span><span class="p-desc">Інтерактивний виконавчий сервер REPL,...</span></div></a>
        <a href="../base/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">base</span><span class="p-desc">Фундаментальний графічний рушій систе...</span></div></a>
        <a href="../benchmark/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">benchmark</span><span class="p-desc">Експериментальний бенчмарк когнітивно...</span></div></a>
        <a href="../collect_stats/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">collect_stats</span><span class="p-desc">Аналізатор фізичного обсягу дипломної...</span></div></a>
        <a href="../consumption/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">consumption</span><span class="p-desc">Детальна візуалізація та статистичний...</span></div></a>
        <a href="../convert_thesis/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">convert_thesis</span><span class="p-desc">Головний оркестратор автоматизованої ...</span></div></a>
        <a href="../convert_to_onnx/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">convert_to_onnx</span><span class="p-desc">Оркестратор автоматичної серіалізації...</span></div></a>
        <a href="../data_assets/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_assets</span><span class="p-desc">Документ</span></div></a>
        <a href="../data_fallback/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">data_fallback</span><span class="p-desc">Документ</span></div></a>
        <a href="../error_resilience_system/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">error_resilience_system</span><span class="p-desc">Бронежилет програмного коду: багаторі...</span></div></a>
        <a href="../finance/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">finance</span><span class="p-desc">Інтегрований модуль для моніторингу е...</span></div></a>
        <a href="../generation/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">generation</span><span class="p-desc">Візуалізаційний UI-компонент (Streaml...</span></div></a>
        <a href="../kpi/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">kpi</span><span class="p-desc">Візуалізатор оперативного моніторингу...</span></div></a>
        <a href="../live_kpi/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">live_kpi</span><span class="p-desc">Забезпечує миттєву візуалізацію стану...</span></div></a>
        <a href="../map/" class="passport-link-card"><span class="p-icon">🗺️</span><div class="p-text"><span class="p-name">map</span><span class="p-desc">Забезпечує інтерактивне відображення ...</span></div></a>
        <a href="../merge_thesis/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">merge_thesis</span><span class="p-desc">Утиліта адитивної конкатенації, злитт...</span></div></a>
        <a href="../ram_hygiene_monitor/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">ram_hygiene_monitor</span><span class="p-desc">Система захисту ресурсів: відстеження...</span></div></a>
        <a href="../real_data_evaluation/" class="passport-link-card"><span class="p-icon">📊</span><div class="p-text"><span class="p-name">real_data_evaluation</span><span class="p-desc">Емпіричний валідатор ШІ-моделей на ре...</span></div></a>
        <a href="../refactor_run/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">refactor_run</span><span class="p-desc">Автоматизований оркестратор масового ...</span></div></a>
        <a href="../system_orchestrator/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">system_orchestrator</span><span class="p-desc">Глобальний системний оркестратор, дис...</span></div></a>
        <a href="../types/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">src/app/types.py</span><span class="p-desc">Реєстр типізованих аліасів для статич...</span></div></a>
        <a href="../unified_logging_registry/" class="passport-link-card"><span class="p-icon">📄</span><div class="p-text"><span class="p-name">unified_logging_registry</span><span class="p-desc">Система тотальної простежуваності: ко...</span></div></a>
    </div>
</div>

</div>

<!-- ACADEMIC AUDIT HISTORY -->
<div class='audit-history' style='margin-top: 50px; padding: 20px; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.8rem;'>
    <p><b>Audit ID:</b> ATH-2026-V5-1TO1-MAP</p>
    <p><b>Status:</b> VERIFIED | ORPHAN CLEANUP COMPLETED</p>
    <p><b>Note:</b> Система повністю переведена на індивідуальні паспорти.</p>
</div>