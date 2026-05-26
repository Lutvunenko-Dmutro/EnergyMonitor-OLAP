# Технічний Паспорт Компонента: scripts/thesis/deep_ai_check.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🧠 NEURAL AUTHORSHIP DETECTOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">👁️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">deep_ai_check.py</h1>
            <p class="mega-subtitle">Нейронний детектор авторства, трансформер-класифікатор на базі RoBERTa та інтелектуальний фільтр академічної доброчесності</p>
            <div class="status-tags">
                <span class="tag tag-online">TRANSFORMER AI</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">INTEGRITY GUARD</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🤖</div>
        <div class="metric-info">
            <span class="metric-label">Model Architecture</span>
            <span class="metric-value">RoBERTa Classifier</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🎯</div>
        <div class="metric-info">
            <span class="metric-label">Target Classes</span>
            <span class="metric-value">ChatGPT vs Human</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧱</div>
        <div class="metric-info">
            <span class="metric-label">Input Context</span>
            <span class="metric-value">Max 512 tokens / paragraph</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">Evaluation Metric</span>
            <span class="metric-value">AI Probability Score</span>
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
            Модуль <code>scripts/thesis/deep_ai_check.py</code> виконує роль <strong>експертного нейронного аудитора авторства (Deep AI Authorship Checker)</strong> у системі підготовки дипломного проєкту платформи <i>Energy Monitor Ultimate</i>. Він призначений для проведення глибокого лінгвістичного аналізу згенерованих розділів дисертації за допомогою передових моделей глибокого навчання (Transformers) для виявлення ознак присутності тексту, написаного штучним інтелектом (зокрема, ChatGPT).
        </p>
        <p style="margin-top: 10px;">
            Ключові можливості трансформерного аналізатора:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Трансформерна класифікація (Transformer Classification):</strong> Використання спеціалізованої моделі <code>Hello-SimpleAI/chatgpt-detector-roberta</code> для розпізнавання штучно згенерованого тексту на рівні абзаців.</li>
            <li><strong>Адаптивна фільтрація контексту (Context Filtering):</strong> Сканування файлу DOCX, вилучення лише довгих, змістовних абзаців (довжиною понад 150 символів) для виключення технічних назв та заголовків з аналізу.</li>
            <li><strong>Поблочний аналіз (Paragraph Profiling):</strong> Поабзацне оцінювання з виведенням показника впевненості (Probability) моделі для кожного окремого сегмента тексту.</li>
            <li><strong>Розрахунок інтегрального вердикту (Verdict Generation):</strong> Формування фінального висновку про походження тексту на основі середньої зваженої ймовірності виявленого ШІ-контенту.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Процес трансформерної валідації (AI Detection Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Діаграма демонструє етапи від завантаження трансформерного конвеєра до поабзацного прогону та винесення фінального рішення:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск deep_ai_check.py") --> IMP_LIB("1. Імпорт transformers & torch")
                IMP_LIB -- "Бібліотеки відсутні" --> ERR_LIB("2a. Вивід інструкції зі встановлення & Вихід")
                IMP_LIB -- "Успішно" --> LOAD_PIPE("2b. Ініціалізація pipeline('text-classification')")
                
                LOAD_PIPE --> DOWNLOAD_MODEL("3. Завантаження моделі Hello-SimpleAI/chatgpt-detector-roberta")
                DOWNLOAD_MODEL --> READ_DOC("4. Зчитування файлу DOCX (python-docx)")
                
                READ_DOC --> FILTER_PARA("5. Фільтрація абзаців: len(text) > 150")
                FILTER_PARA --> LOOP_START("6. Цикл по перших 15 великих абзацах")
                
                LOOP_START --> TRUNC("7. Зріз тексту до 512 символів (захист контексту моделі)")
                TRUNC --> INFERENCE("8. Нейромережевий висновок RoBERTa (Inference)")
                
                INFERENCE --> CALC_PROB("9. Розрахунок ймовірності: Label (ChatGPT / Human) & Score")
                CALC_PROB --> LOOP_NEXT("10. Збереження результату & Перехід до наступного")
                
                LOOP_NEXT -- "Є ще абзаци" --> LOOP_START
                LOOP_NEXT -- "Аналіз завершено" --> AVG_SCORE("11. Обчислення середньої ймовірності ШІ (avg_ai)")
                
                AVG_SCORE --> DECISION{"12. Яке значення avg_ai?"}
                DECISION -- "Немає ШІ" --> VERDICT_HUMAN("13a. ВЕРДИКТ: ПОВНІСТЮ ЛЮДСЬКИЙ ТЕКСТ")
                DECISION -- "avg_ai > 0.7" --> VERDICT_AI("13b. ВЕРДИКТ: ВИСОКА ЙМОВІРНІСТЬ ШІ")
                DECISION -- "0.0 < avg_ai <= 0.7" --> VERDICT_MIXED("13c. ВЕРДИКТ: ЗМІШАНИЙ СТИЛЬ / РЕДАГУВАННЯ")
                
                VERDICT_HUMAN & VERDICT_AI & VERDICT_MIXED --> END("Завершення роботи")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичне обґрунтування трансформерного аналізу</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Математика класифікації Softmax в RoBERTa</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Модель RoBERTa виводить логіти (вихідні сирі оцінки) для двох класів: $z_{\text{human}}$ та $z_{\text{chatgpt}}$. Для отримання ймовірності приналежності сегмента до класу ШІ ($p_{\text{ai}}$) застосовується функція Softmax:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ p_{\text{ai}} = \text{Softmax}(z_{\text{chatgpt}}) = \frac{e^{z_{\text{chatgpt}}}}{e^{z_{\text{human}}} + e^{z_{\text{chatgpt}}}} $$
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Інтегральний показник ШІ-присутності (Integrated AI Index)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Фінальний показник ймовірності ШІ розраховується як середнє арифметичне оцінок впевненості лише для тих абзаців, які класифіковані моделлю як штучні ($A_{\text{gpt}} \subset P$). Він ділиться на загальну кількість проаналізованих абзаців $N$ (де $N = \min(15, |P_{\text{valid}}|)$):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{AI\_Score}_{\text{avg}} = \frac{1}{N} \sum_{a \in A_{\text{gpt}}} \text{Score}(a) $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод трансформерного аналізатора</h2>
    </div>
    <div class="glass-card">
        <p>
            Алгоритм завантаження моделі та поабзацної перевірки DOCX-документа:
        </p>
        <pre><code class="language-python">
# Псевдокод нейронного аналізу тексту
def run_neural_authorship_check(docx_path):
    # 1. Ініціалізуємо pipeline RoBERTa
    from transformers import pipeline
    classifier = pipeline("text-classification", model="Hello-SimpleAI/chatgpt-detector-roberta")
    
    # 2. Читаємо абзаци
    paragraphs = extract_paragraphs_from_docx(docx_path)
    # Беремо змістовні абзаци
    valid_paras = [p for p in paragraphs if len(p) > 150]
    
    ai_scores = []
    # Обмежуємо перевірку першими 15 для швидкості
    for i, text in enumerate(valid_paras[:15]):
        # RoBERTa очікує до 512 символів
        truncated_text = text[:512]
        
        result = classifier(truncated_text)[0]
        label = result['label']   # "ChatGPT" або "Human"
        score = result['score']   # Ймовірність від 0.0 до 1.0
        
        if label == "ChatGPT":
            ai_scores.append(score)
            print(f"Paragraph {i+1}: WARNING - AI generated ({round(score*100)}%)")
        else:
            print(f"Paragraph {i+1}: OK - Human author ({round(score*100)}%)")
            
    # 3. Виносимо інтегральний вердикт
    if len(ai_scores) == 0:
        return "VERDICT: 100% HUMAN TEXT"
        
    avg_ai_score = sum(ai_scores) / len(valid_paras[:15])
    if avg_ai_score > 0.7:
        return f"VERDICT: CRITICAL AI PROBABILITY ({round(avg_ai_score*100)}%)"
    else:
        return f"VERDICT: MIXED WRITING STYLE ({round(avg_ai_score*100)}%)"
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Як працює модель RoBERTa для детекції штучного тексту?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Модель RoBERTa (Robustly Optimized BERT Approach) навчалася на гігантському корпусі текстів, згенерованих людьми та ШІ-моделями (ChatGPT). Вона виявляє мікроскопічні закономірності у розподілі слів, частоті використання певних сполучників, рівні ентропії (непередбачуваності вибору наступного слова) та структурі речень. ШІ-моделі зазвичай використовують більш передбачувані та статистично середні мовні паттерни, які RoBERTa миттєво ідентифікує.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому аналіз обмежується 15-ма абзацами та 512 символами на абзац?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Це зроблено з міркувань обчислювальної оптимізації. Прогін великих трансформерних моделей на CPU є ресурсомісткою операцією. Обмеження у 15 абзаців забезпечує високу швидкість тестування (до 10-15 секунд) при збереженні статистичної репрезентативності (якщо людина згенерувала диплом за допомогою ШІ, ознаки будуть присутні в кожному розділі). Обмеження в 512 символів відповідає максимальному розміру контекстного вікна моделі (token limit).
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Що робити, якщо модель видає вердикт "ЗМІШАНИЙ СТИЛЬ" на повністю самостійно написаний текст?</h4>
        <p style="color: var(--text-dim);">
            A: Таке можливе, якщо автор використовував занадто сухі, шаблонні академічні конструкції або скористався інструментами автоматичної перевірки граматики (наприклад, Grammarly / LanguageTool). Рекомендується переписати сумнівні абзаци більш природною, живою мовою, урізноманітнити довжину речень та додати більше авторських оригінальних прикладів чи термінології.
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
