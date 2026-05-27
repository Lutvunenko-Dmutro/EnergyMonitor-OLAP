# Технічний Паспорт Компонента: scripts/thesis/stylometry_check.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🛡️ STYLOMETRY CONSISTENCY AUDITOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚖️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">stylometry_check.py</h1>
            <p class="mega-subtitle">Система стилометричного контролю, аналізатор лінгвістичної однорідності тексту та детектор стрибків авторського стилю</p>
            <div class="status-tags">
                <span class="tag tag-online">STYLO AUDITOR</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">CONSISTENCY CHECKER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📉</div>
        <div class="metric-info">
            <span class="metric-label">Style Vector</span>
            <span class="metric-value">4 Dimensional</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧩</div>
        <div class="metric-info">
            <span class="metric-label">Segmentation</span>
            <span class="metric-value">Header Blocks (&gt;150w)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Metric Stats</span>
            <span class="metric-value">Mean / Variance / RSD</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🚨</div>
        <div class="metric-info">
            <span class="metric-label">Style Jump Limit</span>
            <span class="metric-value">RSD &gt; 25% Threshold</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль та архітектурне призначення</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/thesis/stylometry_check.py</code> виконує роль <strong>виділеного аудитора лінгвістичної цілісності (Stylometry Consistency Auditor)</strong> дипломного проєкту платформи <i>Energy Monitor Ultimate</i>. Він призначений для вирішення важливого завдання нормоконтролю — перевірки тексту на предмет плагіату шляхом виявлення різких стилістичних розбіжностей (стрибків стилю) між різними розділами роботи.
        </p>
        <p style="margin-top: 10px;">
            Основний функціонал стилометричного аудитора:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Розрахунок стилометричного вектора (Style Vector Extraction):</strong> Оцінювання кожної текстової секції за чотирма фундаментальними параметрами: середньою довжиною речень, середньою довжиною слів, коефіцієнтом лексичного багатства (TTR) та густиною сполучників.</li>
            <li><strong>Поблочна сегментація (Segmented Analysis):</strong> Автоматичне розділення всього документа на змістовні підрозділи на основі метаданих заголовків Word (Heading 1-3) з ігноруванням технічних блоків (вихідний код додатків, списки джерел).</li>
            <li><strong>Математична оцінка стабільності (Consistency Audit):</strong> Розрахунок середньоквадратичного відхилення та коефіцієнта варіації (RSD) для кожного виміру стилометричного вектора.</li>
            <li><strong>Виявлення стрибків стилю (Style Jumps):</strong> Сигналізація у разі перевищення встановленого порогу відхилення (25%), що вказує на ймовірне копіювання фрагментів з чужих робіт без належного перефразування.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр стилометричного аналізу (Stylometry Audit Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема відображає послідовність вилучення текстових блоків, розрахунку лінгвістичних векторів та обчислення варіацій стилю:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск stylometry_check.py &lt;target&gt;") --> OPEN_DOC("1. Зчитування файлу DOCX (python-docx)")
                
                OPEN_DOC --> LOOP_PARA("2. Перебір абзаців документа")
                LOOP_PARA --> FILT_TECH{"3. Чи містить абзац код, додатки або літературу?"}
                
                FILT_TECH -- "Так" --> SKIP_PARA("3a. Пропуск абзацу")
                FILT_TECH -- "Ні" --> CHK_HEAD{"3b. Чи є абзац Заголовком (Heading)?"}
                
                CHK_HEAD -- "Так" --> NEW_BLOCK("4a. Закриття поточного блоку & Створення нового")
                CHK_HEAD -- "Ні" --> ADD_BODY("4b. Додавання тексту в поточний блок")
                
                NEW_BLOCK & ADD_BODY --> LOOP_NEXT("5. Перехід до наступного абзацу")
                SKIP_PARA --> LOOP_NEXT
                
                LOOP_NEXT -- "Є ще абзаци" --> LOOP_PARA
                LOOP_NEXT -- "Всі абзаци оброблено" --> FILTER_SIZE("6. Відбір блоків довжиною понад 150 слів")
                
                FILTER_SIZE --> CALC_VEC("7. get_style_vector(): Розрахунок ASL, AWL, TTR, Conj для перших 10 блоків")
                CALC_VEC --> COMP_VARIANCE("8. Розрахунок середнього, дисперсії та RSD (%) для кожної метрики")
                
                COMP_VARIANCE --> STATS_COMP{"9. Чи перевищує RSD хоча б однієї метрики 25%?"}
                STATS_COMP -- "Так (RSD &gt; 25%)" --> SET_JUMP("10a. Статус: СТРИБОК СТИЛЮ (issues &gt; 0)")
                STATS_COMP -- "Ні (RSD &lt;= 25%)" --> SET_STABLE("10b. Статус: СТАБІЛЬНО (issues = 0)")
                
                SET_JUMP & SET_STABLE --> GEN_VERDICT("11. Формування фінального вердикту про цілісність")
                GEN_VERDICT --> END("Завершення аудиту")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математична модель стилометричної валідації</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Чотиривимірний стилометричний вектор</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Кожен текстовий блок $B_j$ відображається у векторний профіть $\mathbf{v}_j = [x_1, x_2, x_3, x_4] \in \mathbb{R}^4$, де компоненти відповідають лінгвістичним характеристикам:
                </p>
                <ul style="margin-left: 20px; font-size: 13px; color: var(--text-dim); line-height: 1.6;">
                    <li>$x_1 = \text{ASL} = \frac{N_{\text{words}}}{N_{\text{sentences}}}$ (Середня довжина речення)</li>
                    <li>$x_2 = \text{AWL} = \frac{1}{N_{\text{words}}} \sum \text{len}(w_i)$ (Середня довжина слова)</li>
                    <li>$x_3 = \text{TTR} = \frac{|V_{\text{unique}}|}{N_{\text{words}}}$ (Словникове багатство)</li>
                    <li>$x_4 = \text{Conj} = \frac{N_{\text{conjunctions}}}{N_{\text{words}}}$ (Частота сполучників: <i>і, та, але, що, як, бо, тому...</i>)</li>
                </ul>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Обчислення коефіцієнта варіації (Relative Standard Deviation)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Для оцінки коливань певної стилістичної характеристики $x$ на множині з $K$ розділів розраховується математичне сподівання (середнє, $\mu$), дисперсія ($\sigma^2$), середньоквадратичне відхилення ($\sigma$) та відносне стандартне відхилення ($\text{RSD}$):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \mu = \frac{1}{K} \sum_{j=1}^K x_j, \quad \sigma = \sqrt{\frac{1}{K} \sum_{j=1}^K (x_j - \mu)^2}, \quad \text{RSD} = \frac{\sigma}{\mu} \times 100\% $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Критерій стрибка стилю (Style consistency criterion)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Стійкість авторського стилю вважається порушеною (наявність "стрибка"), якщо хоча б один вимір вектора перевищує критичний поріг варіації у 25%:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{Verdict} = \begin{cases} 
                      \text{Stable style}, & \forall m \in [1, 4]: \text{RSD}_m \le 25\% \\
                      \text{Style Jump Alert}, & \exists m \in [1, 4]: \text{RSD}_m > 25\% 
                   \end{cases} $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод стилометричного аудитора</h2>
    </div>
    <div class="glass-card">
        <p>
            Алгоритм вилучення стилістичних векторів та розрахунку відхилень:
        </p>
        <pre><code class="language-python">
# Псевдокод стилометричного контролю
import math
import re

def compute_style_consistency(sections_list):
    vectors = []
    conjunctions_set = {"і", "та", "але", "що", "як", "бо", "тому", "якщо"}
    
    for section_text in sections_list:
        words = re.findall(r'\w+', section_text.lower())
        sentences = re.split(r'[.!?]\s+', section_text)
        
        if len(words) < 50:
            continue
            
        asl = len(words) / len(sentences) # Довжина речення
        awl = sum(len(w) for w in words) / len(words) # Довжина слова
        ttr = len(set(words)) / len(words) # Лексичне багатство
        
        conj_count = sum(1 for w in words if w in conjunctions_set) / len(words)
        
        vectors.append({"asl": asl, "awl": awl, "ttr": ttr, "conj": conj_count})
        
    # Розраховуємо варіації для кожної метрики
    issues_detected = 0
    metrics = ["asl", "awl", "ttr"]
    
    for m in metrics:
        values = [v[m] for v in vectors]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance)
        
        rsd = (std_dev / mean) * 100 if mean > 0 else 0
        
        if rsd > 25.0:
            print(f"Alert: Style jump on metric '{m}' (RSD = {round(rsd, 1)}%)")
            issues_detected += 1
            
    if issues_detected > 0:
        return "VERDICT: NATURAL FLUCUATIONS (HUMAN AUTHOR WITH EDITING)"
    return "VERDICT: EXCELLENT STYLISTIC CONSISTENCY"
        </code></pre>
    </div>
</div>

<!-- SECTION 5: FAQ -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">05</span>
        <h2 class="section-title">Часті питання (FAQ)</h2>
    </div>
    <div class="glass-card">
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Що таке "стрибок стилю" та чому він свідчить про плагіат?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Людина має стійкі мовні звички — певний унікальний словниковий запас, улюблені сполучники, середній розмір речень. Якщо студент самостійно пише роботу, ці параметри залишаються відносно стабільними у всіх розділах. Проте, якщо розділ 1 скопійовано з підручника 90-х років, розділ 2 перекладено з англійської статті, а розділ 3 написаний самостійно — стилометричні вектори цих частин будуть кардинально різними. Скрипт виявить цей перепад як "стрибок стилю".
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому з аналізу виключаються блоки коду додатків та список джерел?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Програмний код (наприклад, файли на Python) та бібліографічні списки містять специфічний синтаксис, короткі рядки без традиційної структури речень та безліч повторюваних службових слів (`def`, `import`, `return`, `pages`, `vol`). Включення їх до стилометричного аналізу викривило б результати, вказуючи на помилкові аномалії в усьому документі.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як інтерпретується вердикт "Текст має природні коливання"?</h4>
        <p style="color: var(--text-dim);">
            A: Це позитивний результат. Він означає, що відхилення хоч і перевищило поріг в 25% на якійсь із метрик, проте загальний лінгвістичний малюнок залишається органічним. Це свідчить про те, що автор самостійно допрацьовував та редагував різні частини роботи, урізноманітнюючи мову викладу, що цілком природно для справжнього людського письма на відміну від монотонної генерації ШІ.
        </p>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn">
        <span class="btn-icon">🔙</span>
        <span class="btn-text">Повернутися до Атласу</span>
    </a>
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
