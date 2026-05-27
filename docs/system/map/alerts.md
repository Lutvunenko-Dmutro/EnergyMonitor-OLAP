# Технічна специфікація модуля: alerts.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">INCIDENT MANAGEMENT CENTER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🚨</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">UI View: Alerts Dashboard</h1>
            <p class="mega-subtitle">Централізований інтерфейс для моніторингу та обробки аварійних подій. Забезпечує інтерактивне управління життєвим циклом інцидентів (Incident Lifecycle) у реальному часі.</p>
            <div class="status-tags"><span class="tag tag-online">STREAMLIT UI</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">INCIDENT LOG</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📝</div><div class="metric-info"><span class="metric-label">Editor</span><span class="metric-value">st.data_editor</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔄</div><div class="metric-info"><span class="metric-label">Lifecycle</span><span class="metric-value">NEW -> RESOLVED</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">➕</div><div class="metric-info"><span class="metric-label">Registration</span><span class="metric-value">Manual Form Input</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Hygiene</span><span class="metric-value">TOP-10 Cleanup</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>alerts.py</b> виконує роль "Диспетчерського пульта". Він відображає список усіх зафіксованих системою (або створених вручну) аварій. Його ключова фіча — <i>інтерактивність</i>.</p>
        <p style="margin-top: 12px;">Замість статичної таблиці, модуль використовує <code>st.data_editor</code>, дозволяючи диспетчеру прямо в таблиці змінити статус інциденту з "NEW" на "IN PROGRESS" або "RESOLVED". Модуль обробляє ці зміни, автоматично знімаючи emoji-кодування (Visual Coding), і зберігає "чистий" статус назад у базу даних.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def render(df_alerts: pd.DataFrame) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Рендерить весь інтерфейс керування аваріями. Включає ізольовану форму додавання нових інцидентів (<code>create_custom_alert</code>), кнопку швидкого очищення історії до 10 останніх записів (<code>cleanup_old_alerts</code>), та інтерактивний журнал (<code>st.data_editor</code>). Застосовує мапінг емодзі для покращення UX.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def save_changes(changes: dict, df: pd.DataFrame) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Callback-функція (обробник подій), яка спрацьовує при зміні даних у таблиці. Вона бере словник змін <code>edited_rows</code> від Streamlit, знаходить відповідний <code>alert_id</code>, очищує емодзі від статусу (напр. "🟢 RESOLVED" -> "RESOLVED") та викликає метод БД <code>update_alert_status</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема взаємодії (Event Flow)</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    USER(("Диспетчер")) --> |Клікає 'Додати'| FORM("Form Submission")
    USER --> |Клікає 'Очистка'| CLEAN("cleanup_old_alerts(10)")
    USER --> |Змінює статус у таблиці| EDITOR("st.data_editor\n(on_change)")
    
    FORM --> DB_INSERT("create_custom_alert()")
    CLEAN --> DB_DEL("DELETE FROM Alerts")
    
    EDITOR --> SAVE_CB("save_changes()")
    SAVE_CB --> CLEAN_MAP("Mapping: '🟢 RESOLVED' -> 'RESOLVED'")
    CLEAN_MAP --> DB_UPDATE("update_alert_status(id, status)")
    
    DB_INSERT --> RERUN("Clear Cache\nst.rerun()")
    DB_DEL --> RERUN
    DB_UPDATE --> RERUN
    
    RERUN --> UI("Оновлений Інтерфейс\nst.toast(Success)")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.services.data.db_services</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>src.core.database</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>time</span>
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
