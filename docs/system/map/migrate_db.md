# Технічна специфікація модуля: migrate_db.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATABASE EVOLUTION ENGINE & SCHEMA MANAGER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🗄️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Migration Engine: migrate_db</h1>
            <p class="mega-subtitle">Двигун безпечної еволюції схеми PostgreSQL-бази: ідемпотентне розширення таблиці <code>LoadMeasurements</code> фізичними параметрами Digital Twin для забезпечення сумісності з ML-моделями V2/V3</p>
            <div class="status-tags"><span class="tag tag-online">IDEMPOTENT SAFE</span><span class="tag tag-version">v1.0.0</span><span class="tag tag-role">DB MIGRATION SCRIPT</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📋</div><div class="metric-info"><span class="metric-label">Таблиця</span><span class="metric-value">LoadMeasurements</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">➕</div><div class="metric-info"><span class="metric-label">Нових колонок</span><span class="metric-value">6 параметрів</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🛡️</div><div class="metric-info"><span class="metric-label">Безпека</span><span class="metric-value">IF NOT EXISTS</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🖥️</div><div class="metric-info"><span class="metric-label">Інтерфейс</span><span class="metric-value">CLI / Import API</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>migrate_db.py</b> вирішує конкретну задачу — <b>розширення схеми таблиці <code>LoadMeasurements</code></b> шістьма новими колонками, необхідними для побудови повноцінного <b>Digital Twin</b> (цифрового двійника) підстанції. Без цих колонок ML-моделі V2 та V3 не мають доступу до фізичних параметрів обладнання, що унеможливлює точне прогнозування навантаження та оцінку стану здоров'я трансформаторів.</p>
        <p style="margin-top: 12px;">Сценарій запуску: <b>одноразово</b> при першому розгортанні системи або після оновлення, яке додало нові поля телеметрії. Завдяки конструкції <code>IF NOT EXISTS</code> — повторний запуск є <b>повністю безпечним</b> і не зашкодить наявним даним.</p>
        <p style="margin-top: 12px;"><b>Архітектурний інтерфейс:</b> єдина публічна функція <code>migrate()</code>, яка виконує 6 <code>ALTER TABLE</code>-запитів через шар <code>src.core.database.execute_update()</code>.</p>
    </div>
</div>

<!-- SECTION 02: SCHEMA CHANGES — CORE INFO -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Зміни схеми: нові колонки таблиці LoadMeasurements</h2></div>
    <div class="glass-card flow-step">
        <p style="margin-bottom: 15px; color: var(--text-dim);">Всі колонки мають тип <code>DECIMAL(10, 2)</code> або <code>VARCHAR(50)</code> і додаються з гарантією ідемпотентності (<code>IF NOT EXISTS</code>):</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th style="padding: 8px; text-align: left;">Колонка</th>
                    <th style="padding: 8px; text-align: left;">Тип</th>
                    <th style="padding: 8px; text-align: left;">Фізичний сенс</th>
                    <th style="padding: 8px; text-align: left;">Використання в ML</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><code>voltage_kv</code></td>
                    <td style="padding: 8px;"><code>DECIMAL(10,2)</code></td>
                    <td style="padding: 8px;">Напруга на шинах (кВ)</td>
                    <td style="padding: 8px;">Feature V2/V3: відхилення напруги</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><code>frequency_hz</code></td>
                    <td style="padding: 8px;"><code>DECIMAL(10,2)</code></td>
                    <td style="padding: 8px;">Частота мережі (Гц)</td>
                    <td style="padding: 8px;">Feature V2/V3: відхилення частоти від 50 Гц</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><code>temperature_c</code></td>
                    <td style="padding: 8px;"><code>DECIMAL(10,2)</code></td>
                    <td style="padding: 8px;">Температура масла трансформатора (°C)</td>
                    <td style="padding: 8px;">Feature V2/V3: сезонна корекція навантаження</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><code>h2_ppm</code></td>
                    <td style="padding: 8px;"><code>DECIMAL(10,2)</code></td>
                    <td style="padding: 8px;">Концентрація водню в маслі (ppm)</td>
                    <td style="padding: 8px;">Основний індикатор деградації ізоляції</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px;"><code>health_score</code></td>
                    <td style="padding: 8px;"><code>DECIMAL(10,2)</code></td>
                    <td style="padding: 8px;">Агрегований індекс здоров'я (0–100)</td>
                    <td style="padding: 8px;">Target V3: передбачення ризику відмови</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><code>sensor_status</code></td>
                    <td style="padding: 8px;"><code>VARCHAR(50)</code></td>
                    <td style="padding: 8px;">Стан датчика (OK / FAULT / OFFLINE)</td>
                    <td style="padding: 8px;">Маска для фільтрації недостовірних вимірів</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 03: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Публічний інтерфейс</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def migrate() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Виконує 6 SQL <code>ALTER TABLE</code> запитів до таблиці <code>LoadMeasurements</code>. Кожен запит обгорнутий у <code>execute_update()</code> з повторними спробами. Результат кожної операції (SUCCESS / FAILED) виводиться в stdout. Не повертає значення — помилки підключення до БД логуються в шарі <code>src.core.database</code>.</p>
                <p style='margin: 8px 0 0 0; font-size: 12px; color: var(--text-dim);'><b>Виклик:</b> <code>python -m src.services.data.migrate_db</code> або <code>from src.services.data.migrate_db import migrate; migrate()</code></p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 04: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема виконання міграції</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("python migrate_db.py") --> IMPORT("Import execute_update\nfrom src.core.database")
    IMPORT --> CALL("migrate()")
    CALL --> Q1["ALTER TABLE LoadMeasurements\nADD COLUMN IF NOT EXISTS voltage_kv"]
    Q1 --> Q2["ADD COLUMN IF NOT EXISTS frequency_hz"]
    Q2 --> Q3["ADD COLUMN IF NOT EXISTS temperature_c"]
    Q3 --> Q4["ADD COLUMN IF NOT EXISTS h2_ppm"]
    Q4 --> Q5["ADD COLUMN IF NOT EXISTS health_score"]
    Q5 --> Q6["ADD COLUMN IF NOT EXISTS sensor_status"]
    Q6 --> DONE("Migration complete ✅")

    Q1 -->|FAILED| ERR["execute_update → FAILED\nDB logs error, continues"]
    ERR --> Q2
    </div></div>
</div>

<!-- SECTION 05: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <p style="margin-bottom: 12px; color: var(--text-dim);">Модуль навмисно мінімалістичний — лише одна зовнішня залежність:</p>
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database.execute_update</span>
        </div>
        <p style="margin-top: 12px; font-size: 13px; color: var(--text-dim);">Функція <code>execute_update()</code> надає повторні спроби підключення (до 2 разів), обробку помилок та логування. Будь-яка помилка підключення до PostgreSQL не зупиняє цикл міграції — наступний запит все одно буде виконаний.</p>
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
