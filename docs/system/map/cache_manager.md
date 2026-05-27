# Технічна специфікація модуля: cache_manager.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">CACHE LIFECYCLE MANAGER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧹</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">System Hygiene: cache_manager</h1>
            <p class="mega-subtitle">Автоматичне управління життєвим циклом тимчасових даних. Запобігає переповненню дискового простору шляхом TTL-очищення локального кешу.</p>
            <div class="status-tags"><span class="tag tag-online">FILE SYSTEM SCRIPT</span><span class="tag tag-version">v1.1.0</span><span class="tag tag-role">HYGIENE DAEMON</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🕰️</div><div class="metric-info"><span class="metric-label">TTL Cleanup</span><span class="metric-value">24 Hours Default</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🔒</div><div class="metric-info"><span class="metric-label">Protected</span><span class="metric-value">.graphml extensions</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🤫</div><div class="metric-info"><span class="metric-label">Execution</span><span class="metric-value">Silent (No Exceptions)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🩺</div><div class="metric-info"><span class="metric-label">Monitoring</span><span class="metric-value">Disk Volume Stats</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>cache_manager.py</b> відповідає за підтримку здоров'я файлової системи застосунку (папка <code>/cache</code>). Оскільки додаток активно завантажує дані з Kaggle та створює тимчасові JSON-архіви для офлайн режиму, без контролю папка розросталася б безмежно.</p>
        <p style="margin-top: 12px;">Цей модуль працює як фоновий гігієнічний процес (Hygiene Daemon). Він запускається при старті додатку, сканує папку <code>/cache</code>, перевіряє вік файлів (TTL - Time To Live) за мітками <code>st_mtime</code>, і тихо видаляє старі JSON файли. При цьому він <i>ніколи</i> не видаляє критичні ассети, як-от системні карти у форматі <code>.graphml</code>.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def clean_cache(ttl_hours: int = 24) → dict[str, int]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Ітератор по директорії <code>CACHE_DIR</code>. Пропускає директорії та файли з розширенням <code>.graphml</code>. Перевіряє <code>file_path.stat().st_mtime</code> проти поточного <code>time.time()</code>. Якщо різниця більше за TTL, викликає <code>file_path.unlink()</code>. Повертає словник зі статистикою: 'deleted', 'skipped', 'errors'.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_cache_stats() → dict[str, int | float]</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Аналітична функція. Підраховує загальну кількість файлів, розмір у мегабайтах (<code>st_size / 1024 / 1024</code>), кількість JSON та GraphML файлів. Корисно для адмін-панелей.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def startup_cache_cleanup(ttl_hours: int = 24) → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Оркестратор, що викликається при старті <code>main.py</code>. Вимірює розмір до (<code>get_cache_stats</code>), викликає очистку (<code>clean_cache</code>), та обчислює зекономлене місце. Загорнуто в глобальний <code>try...except Exception</code>, щоб будь-яка помилка I/O <b>ніколи</b> не крашила запуск додатку.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема очистки TTL</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    START("App Startup\n(main.py)") --> CALL("startup_cache_cleanup(24h)")
    
    CALL --> STAT1("get_cache_stats()\nMeasure Before Size")
    STAT1 --> CLN("clean_cache()")
    
    CLN --> LOOP{"Iterate files in\n/cache/"}
    
    LOOP -->|Protected (.graphml)| SKIP("result['skipped'] += 1")
    LOOP -->|Expired (Age > 24h)| UNLINK("file_path.unlink()")
    LOOP -->|Recent (Age <= 24h)| SKIP
    
    UNLINK --> DEL("result['deleted'] += 1")
    
    SKIP --> DONE("Return Stats")
    DEL --> DONE
    
    DONE --> LOG("Logger:\nFreed 15.2 MB")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>time</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pathlib.Path</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>typing</span>
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
