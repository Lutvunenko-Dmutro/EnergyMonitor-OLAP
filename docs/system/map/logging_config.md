# Технічна специфікація модуля: logging_config.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">OBSERVABILITY CORE</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">📝</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Central Logger: logging_config</h1>
            <p class="mega-subtitle">Централізований модуль системи спостереження. Налаштовує багатоканальне логування (консоль, файли, помилки, ротація) для прозорої діагностики роботи всіх вузлів бекенду та ML.</p>
            <div class="status-tags"><span class="tag tag-online">MULTI-CHANNEL LOGGER</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">CORE UTILITY</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Rotation</span><span class="metric-value">Size (10MB) & Daily</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📁</div><div class="metric-info"><span class="metric-label">Archival</span><span class="metric-value">Max 5 Backups</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Channels</span><span class="metric-value">Console, Main, Error, Daily</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">⚙️</div><div class="metric-info"><span class="metric-label">Encoding</span><span class="metric-value">UTF-8 Strict</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>logging_config.py</b> вирішує проблему розрізнених логів. Замість того, щоб кожен скрипт друкував свої <code>print()</code>-и куди заманеться, цей модуль надає єдину фабрику логгерів (<code>setup_logging()</code>). Він перехоплює всі події системи і маршрутизує їх по потрібних каналах.</p>
        <p style="margin-top: 12px;">Архітектурна перевага полягає в автоматичній ротації: файли логів ніколи не заповнять весь жорсткий диск, оскільки модуль обмежує розмір кожного файлу (10MB) та створює подобові архіви для ретроспективної діагностики помилок.</p>
    </div>
</div>

<!-- SECTION 02: LOGGING CHANNELS -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Канали спостереження (Handlers)</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th style="padding: 8px; text-align: left;">Хендлер</th>
                    <th style="padding: 8px; text-align: left;">Призначення та рівень</th>
                    <th style="padding: 8px; text-align: left;">Механізм ротації</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><b>Console (stdout)</b></td>
                    <td style="padding: 8px;">Рівень: <code>Задається</code><br><span style="color:var(--text-dim);font-size:11px;">Містить іконки (⚡) та час (HH:MM:SS)</span></td>
                    <td style="padding: 8px;">Немає (живий вивід)</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><b>Main File</b></td>
                    <td style="padding: 8px;">Рівень: <code>DEBUG+</code><br><span style="color:var(--text-dim);font-size:11px;">Детальний запис: funcName, lineno, повний час</span></td>
                    <td style="padding: 8px;">Розмір: <code>max_bytes</code> (10MB)<br>Кількість: <code>backup_count</code></td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><b>Error File</b></td>
                    <td style="padding: 8px;">Рівень: <code>ERROR+</code><br><span style="color:var(--text-dim);font-size:11px;">Записує повний Traceback (exc_info=True)</span></td>
                    <td style="padding: 8px;">Розмір: <code>max_bytes</code> (10MB)<br>Кількість: <code>backup_count</code></td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><b>Daily File</b></td>
                    <td style="padding: 8px;">Рівень: <code>INFO+</code><br><span style="color:var(--text-dim);font-size:11px;">Чистий лог подій без зайвого дебагу</span></td>
                    <td style="padding: 8px;">Час: <code>midnight</code><br>Історія: 7 днів</td>
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
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def setup_logging(log_level="INFO", log_dir="logs", log_file="energy-monitor.log", max_bytes=10MB, backup_count=5) → logging.Logger</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Єдина точка входу. Автоматично створює директорію логів (якщо її немає), очищає старі хендлери (щоб запобігти дублюванню повідомлень) і підключає всі 4 канали спостереження до кореневого логгера "ENERGY_MONITOR". Наприкінці друкує Startup Banner з метаданими.</p>
            </div>

            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>_create_console_handler, _create_file_handler, _create_error_handler, _create_daily_handler</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Приватні фабрики. Інкапсулюють логіку форматування повідомлень та налаштування ротації (RotatingFileHandler та TimedRotatingFileHandler).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 04: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема маршрутизації подій</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    EVENT("log.error('DB Timeout')") --> CORE("Logger: ENERGY_MONITOR")
    
    CORE -->|All Levels| H_CONS("ConsoleHandler\n[sys.stdout]")
    CORE -->|DEBUG+| H_FILE("RotatingFileHandler\n[energy-monitor.log]")
    CORE -->|INFO+| H_DAILY("TimedRotatingHandler\n[energy-monitor-daily.log]")
    CORE -->|ERROR+| H_ERR("RotatingFileHandler\n[energy-monitor.error.log]")
    
    H_ERR --> TRACE("Inject Traceback\n(exc_info)")
    
    H_FILE --> ROTATE_S{"Size > 10MB?"}
    ROTATE_S -->|Yes| ARCHIVE1("Archive to .log.1\nKeep max 5")
    
    H_DAILY --> ROTATE_T{"Is Midnight?"}
    ROTATE_T -->|Yes| ARCHIVE2("Archive to .log.YYYY-MM-DD\nKeep max 7 days")
    </div></div>
</div>

<!-- SECTION 05: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging.handlers</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pathlib</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sys</span>
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
