# Технічна специфікація модуля: advanced_mining.py (GIGA-PASSPORT EDITION)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">ADVANCED ML ANALYTICS</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🧠</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">Machine Learning Analytics: advanced_mining</h1>
            <p class="mega-subtitle">Сервіс поглибленого інтелектуального аналізу даних. Реалізує алгоритми машинного навчання (Clustering & Classification) для виявлення патернів навантаження та прогнозування ризиків (Explainable AI).</p>
            <div class="status-tags"><span class="tag tag-online">SCIKIT-LEARN ENGINE</span><span class="tag tag-version">v1.5.0</span><span class="tag tag-role">ML SERVICE</span></div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card"><div class="metric-icon">🔍</div><div class="metric-info"><span class="metric-label">Clustering</span><span class="metric-value">K-Means (3 Clusters)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🌳</div><div class="metric-info"><span class="metric-label">Predictive</span><span class="metric-value">Decision Tree (Depth=3)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">📊</div><div class="metric-info"><span class="metric-label">Output</span><span class="metric-value">Visual Plots (PNG)</span></div></div>
    <div class="glass-card metric-card"><div class="metric-icon">🗄️</div><div class="metric-info"><span class="metric-label">Data</span><span class="metric-value">PostgreSQL Direct</span></div></div>
</div>

<!-- SECTION 01: CONCEPTUAL ROLE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">01</span><h2 class="section-title">Концептуальне призначення</h2></div>
    <div class="glass-card flow-step">
        <p>Модуль <b>advanced_mining.py</b> призначений для "офлайн" аналітики та видобутку знань (Data Mining). На відміну від Streamlit-інтерфейсу, цей скрипт працює безпосередньо з базою даних через SQL і генерує статичні артефакти (зображення та консольні звіти).</p>
        <p style="margin-top: 12px;">Він використовує методи <b>Scikit-Learn</b> для двох ключових завдань: 1) Кластеризація (K-Means), щоб розбити підстанції на групи за середнім навантаженням, волатильністю та аварійністю. 2) Класифікація (Decision Tree), щоб побудувати <i>пояснювану</i> модель прогнозування критичних станів (навантаження > 95% від ліміту) на основі години дня та температури.</p>
    </div>
</div>

<!-- SECTION 02: API REFERENCE -->
<div class="section-container">
    <div class="section-header"><span class="section-number">02</span><h2 class="section-title">Публічний інтерфейс (API)</h2></div>
    <div class="glass-card flow-step">
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def run_clustering_analysis() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Витягує агреговані дані (avg_load, load_volatility, alert_count) з БД. Нормалізує фічі через <code>StandardScaler</code>. Застосовує алгоритм <b>K-Means</b> для пошуку 3 кластерів підстанцій. Зберігає результати розсіювання (Scatter Plot) у файл <code>clustering_result.png</code>.</p>
            </div>
            
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def run_classification_prediction() → None</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Будує <b>DecisionTreeClassifier</b> для прогнозування поля <code>is_critical</code> (навантаження > 95%) на основі температури та години дня. Генерує звіт точності (classification_report) та зберігає візуалізацію правил прийняття рішень (Explainable AI) у файл <code>decision_tree.png</code>.</p>
            </div>

            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 14px; border-radius: 8px;'>
                <code style='color: var(--accent); font-size: 14px; font-weight: 600;'>def get_data(query: str) → pd.DataFrame</code>
                <p style='margin: 8px 0 0 0; font-size: 13px; color: var(--text-dim);'>Утиліта для виконання SQL-запитів до PostgreSQL та повернення результатів у вигляді Pandas DataFrame. Використовує контекстний менеджер <code>get_db_connection()</code>.</p>
            </div>

        </div>
    </div>
</div>

<!-- SECTION 03: DATABASE SCHEMA (SQL TYPES) -->
<div class="section-container">
    <div class="section-header"><span class="section-number">03</span><h2 class="section-title">Схема даних (SQL)</h2></div>
    <div class="glass-card flow-step">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border); color: var(--accent);">
                    <th style="padding: 8px; text-align: left;">Ознака (Feature)</th>
                    <th style="padding: 8px; text-align: left;">Таблиця / Джерело</th>
                    <th style="padding: 8px; text-align: left;">ML Роль</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px; font-weight: 600;">avg_load, stddev_load</td>
                    <td style="padding: 8px;"><code>LoadMeasurements</code> (AGGs)</td>
                    <td style="padding: 8px;">Clustering Feature (K-Means)</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px; font-weight: 600;">alert_count</td>
                    <td style="padding: 8px;"><code>Alerts</code> (COUNT)</td>
                    <td style="padding: 8px;">Clustering Feature (K-Means)</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px; font-weight: 600;">hour_of_day</td>
                    <td style="padding: 8px;"><code>LoadMeasurements</code> (EXTRACT)</td>
                    <td style="padding: 8px;">Predictive Feature (Tree)</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px; font-weight: 600;">temperature</td>
                    <td style="padding: 8px;"><code>WeatherReports</code></td>
                    <td style="padding: 8px;">Predictive Feature (Tree)</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px; font-weight: 600;">is_critical</td>
                    <td style="padding: 8px;"><code>CASE (load/cap > 0.95)</code></td>
                    <td style="padding: 8px;">Target Variable (Y)</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 04: EXECUTION FLOW DIAGRAM -->
<div class="section-container">
    <div class="section-header"><span class="section-number">04</span><h2 class="section-title">Схема ML Пайплайну</h2></div>
    <div class="diagram-outer-wrapper"><div class="mermaid">
graph TD
    DB[(PostgreSQL)] --> |SQL Query| DF1("get_data()\nLoad Aggregates")
    DB --> |SQL Query| DF2("get_data()\nCritical States")
    
    subgraph "run_clustering_analysis()"
        DF1 --> SCALE("StandardScaler")
        SCALE --> KM("KMeans(n_clusters=3)")
        KM --> PLOT1("Save: clustering_result.png")
    end
    
    subgraph "run_classification_prediction()"
        DF2 --> SPLIT("train_test_split()")
        SPLIT --> FIT("DecisionTreeClassifier()\nmax_depth=3")
        FIT --> PLOT2("Save: decision_tree.png")
    end
    </div></div>
</div>

<!-- SECTION 05: DEPENDENCIES -->
<div class="section-container">
    <div class="section-header"><span class="section-number">05</span><h2 class="section-title">Карта залежностей (Imports)</h2></div>
    <div class="glass-card flow-step">
        <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sklearn.cluster</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sklearn.tree</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>sklearn.metrics</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>pandas</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>psycopg2</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>matplotlib.pyplot</span>
            <span style='display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); padding: 4px 10px; border-radius: 6px; font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--accent); margin: 4px;'>seaborn</span>
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
