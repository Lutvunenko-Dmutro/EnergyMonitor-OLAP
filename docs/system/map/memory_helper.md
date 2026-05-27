# Технічна специфікація модуля: memory_helper.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">RESOURCE WATCHDOG</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧠</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Memory Manager: memory_helper</h1>
            <p class="mega-subtitle">Забезпечує стабільність додатка. Проактивно вимірює споживання RAM, знаходить витоки в сесіях та автоматично скидає кеші при досягненні порогів.</p>
            <div class="status-tags"><span class="tag tag-online">PSUTIL RSS</span><span class="tag tag-version">v2.0.0</span><span class="tag tag-role">GARBAGE COLLECTOR</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">📈</div><div class="metric-info"><span class="metric-label">Tracker</span><span class="metric-value">psutil.Process() RSS</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🧹</div><div class="metric-info"><span class="metric-label">Auto-GC</span><span class="metric-value">Trigger at 380 MB</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🕵️</div><div class="metric-info"><span class="metric-label">Audit</span><span class="metric-value">Session State Top Objects</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Analyzer</span><span class="metric-value">df.memory_usage(deep=True)</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>memory_helper.py</b> — це "імунна система" проєкту. Streamlit має сумнозвісну проблему: він зберігає старі версії кешованих даних та сесій у пам'яті. При роботі з великими Pandas DataFrames (як у нас) це швидко призводить до вичерпання 512 МБ безкоштовного хмарного ліміту (OOM Error) і падіння додатку.</p>
        <p style="margin-top: 12px;">Цей модуль використовує бібліотеку <code>psutil</code> для того, щоб фізично запитати в ОС "Скільки мегабайт оперативної пам'яті їсть зараз цей Python-процес?". Якщо цифра перевищує <code>AUTO_GC_THRESHOLD_MB</code> (зараз 380 МБ), функція <code>auto_gc()</code> радикально видаляє всі <code>st.cache_data</code> та викликає <code>gc.collect()</code>, рятуючи сервер від падіння. Також модуль містить утиліти для інспекції конкретних змінних сесії (знаходження "жирних" об'єктів).</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_memory_usage() → float</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Отримує PID поточного процесу (<code>os.getpid()</code>), підключається через <code>psutil.Process</code> та повертає фізичне споживання RAM (RSS) у мегабайтах.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def auto_gc(threshold_mb: float = 380) → bool</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Функція-запобіжник (Watchdog). Викликає <code>get_memory_usage()</code>. Якщо поточне використання перевищує ліміт — примусово виконує <code>st.cache_data.clear()</code> та <code>gc.collect()</code>, записує дію у логер. Повертає True, якщо очищення відбулось.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_top_objects() → list</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Аналізує <code>st.session_state</code>. Якщо об'єкт є Pandas DataFrame, він обчислює його реальну вагу в пам'яті через <code>memory_usage(deep=True).sum()</code>. Сортує і повертає топ-5 найважчих об'єктів для діагностики витоків (Memory Leaks).</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Життєвий Цикл Auto-GC</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    IN("auto_gc(380 MB)") --> GET("psutil.Process(PID).memory_info().rss")
    
    GET --> CONV("Convert bytes to MB")
    
    CONV --> CHK{"Usage > 380 MB?"}
    
    CHK -->|No| FALSE("Return False (Safe)")
    
    CHK -->|Yes| LOG("logger.warning('Auto-GC Triggered')")
    
    LOG --> CLEAR("st.cache_data.clear()\n(Drops all memoized datasets)")
    
    CLEAR --> GC("gc.collect()\n(Python Garbage Collector)")
    
    GC --> LOG2("logger.info('Memory after GC: ...')")
    
    LOG2 --> TRUE("Return True (Cleaned)")
    </div></div>
</div>

<!-- SECTION 04: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>gc</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>os (os.getpid)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>psutil (Process)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>streamlit (session_state, cache_data)</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>logging</span>
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
