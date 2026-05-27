# Технічна специфікація модуля: db_services.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">DATABASE BUSINESS SERVICES</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🛠️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Data Service Layer: db_services</h1>
            <p class="mega-subtitle">Високорівневий рівень бізнес-логіки для взаємодії з даними. Забезпечує управління життєвим циклом інцидентів та формуванням агрегованих зрізів стану мережі.</p>
            <div class="status-tags"><span class="tag tag-online">SQLALCHEMY ORM</span><span class="tag tag-version">v2.1.0</span><span class="tag tag-role">BUSINESS LOGIC</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📡</div><div class="metric-info"><span class="metric-label">Telemetry</span><span class="metric-value">Latest Snapshots</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🚨</div><div class="metric-info"><span class="metric-label">Incidents</span><span class="metric-value">CRUD Operations</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Hygiene</span><span class="metric-value">Limit-Based Cleanup</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔐</div><div class="metric-info"><span class="metric-label">ACID</span><span class="metric-value">Atomic Transactions</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>db_services.py</b> відділяє низькорівневі SQL-запити від UI. Якщо <code>database.py</code> просто відкриває підключення, то цей модуль реалізує <i>бізнес-сценарії</i>.</p>
        <p style="margin-top: 12px;">Сценарій 1: "Отримати поточний стан мережі для HUD". Викликається складний SQL-запит (через <code>DISTINCT ON</code>), який дістає тільки найостанніші записи для кожної підстанції, та на льоту розраховує віртуальні показники напруги та частоти. Сценарій 2: "Управління аваріями". Інтерфейси створення, зміни статусу та видалення алертів із суворим дотриманням транзакцій (ACID) через <code>engine.begin()</code>.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_latest_measurements() → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Виконує SQL-запит <code>SELECT DISTINCT ON (m.substation_id) ... ORDER BY m.substation_id, m.timestamp DESC</code> для отримання останнього зрізу даних (Snapshot) по всіх об'єктах. Далі застосовує <code>df.apply(calculate_synthetic_electrical)</code> для додавання синтетичних колонок напруги (voltage_kv) та частоти (frequency_hz).</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def create_custom_alert(sub_name: str, alert_type: str, desc: str) → tuple[bool, str]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Управління інцидентами. Відкриває транзакцію (<code>engine.begin()</code>). Робить <code>SELECT</code> для пошуку <code>substation_id</code> за іменем. Якщо знайдено — виконує <code>INSERT INTO Alerts</code>. Повертає (Success Flag, Message).</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def cleanup_old_alerts(keep_last: int = 10) → bool</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Гігієна БД. Знаходить ID N-останніх алертів (через <code>ORDER BY id DESC LIMIT N</code>). Потім видаляє всі записи <code>NOT IN</code> цей список. Використовує транзакції для гарантії цілісності.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Транзакційна логіка (Alerts CRUD)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    UI("UI Action\n(Create Alert)") --> CALL("create_custom_alert()")
    
    CALL --> TXN("with engine.begin() as conn:")
    
    TXN --> LOOKUP("SELECT substation_id\nWHERE name = sub_name")
    
    LOOKUP --> CHECK{"Found?"}
    
    CHECK -->|No| ERR("Rollback.\nReturn (False, 'Not Found')")
    
    CHECK -->|Yes| INSERT("INSERT INTO Alerts\n(ts, type, desc, id, 'NEW')")
    
    INSERT --> COMMIT("Auto-Commit TXN")
    COMMIT --> OK("Return (True, 'Success')")
    
    TXN -.-> EXCEPTION("try...except Exception")
    EXCEPTION --> LOG("log.error(e)")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>random</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>datetime</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sqlalchemy.text</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database (run_query, execute_update, get_engine)</span>
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
