# Технічний Паспорт Компонента: scripts/thesis/quality_check.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🛡️ ACADEMIC QUALITY AUDITOR</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🩺</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">quality_check.py</h1>
            <p class="mega-subtitle">Система інтелектуального аудиту верстки, виявлення обходу плагіату та лінгвістичної валідації за законом Ціпфа</p>
            <div class="status-tags">
                <span class="tag tag-online">QUALITY GUARD</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">DSTU STANDARDIZER</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">Layout Rules</span>
            <span class="metric-value">Times 14pt / Spacing 1.5</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔍</div>
        <div class="metric-info">
            <span class="metric-label">Plagiarism Check</span>
            <span class="metric-value">Mixed Alphabet Detector</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-info">
            <span class="metric-label">Complexity</span>
            <span class="metric-value">ARI Readability Index</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧬</div>
        <div class="metric-info">
            <span class="metric-label">AI Signature</span>
            <span class="metric-value">Zipf / Sentence Var</span>
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
            Модуль <code>scripts/thesis/quality_check.py</code> — це **інтелектуальний щит академічної якості (Academic Quality Guard)** дипломного проєкту платформи <i>Energy Monitor Ultimate</i>. Він проводить комплексний низькорівневий аналіз згенерованих файлів DOCX для перевірки їх відповідності державним стандартам ДСТУ та виявлення прихованих аномалій, що можуть вказувати на неякісний автопереклад, використання ШІ або спроби недоброчесного обходу систем антиплагіату.
        </p>
        <p style="margin-top: 10px;">
            Ключові напрями перевірки системи:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Санітація верстки (Layout & Margins check):</strong> Перевірка фізичних меж сторінки (ліве 3.0см, праве 1.0см, верхнє/нижнє по 2.0см), перевірка основного шрифту Times New Roman 14pt та міжрядкового інтервалу 1.5.</li>
            <li><strong>Детектор змішаних алфавітів (Alphabet Hijack Detection):</strong> Сканування слів на предмет комбінування символів кирилиці та латиниці (наприклад, заміна української "о" чи "а" на англійську для обману антиплагіату).</li>
            <li><strong>Семантичний аналіз варіативності (Sentence Variance Audit):</strong> Оцінка варіативності довжини речень — ШІ-генератори пишуть монотонно з однаковою кількістю слів, тоді як жива мова людини має високу дисперсію.</li>
            <li><strong>Лексичне багатство та Закон Ціпфа:</strong> Розрахунок словникового різноманіття (TTR) та перевірка математичного розподілу частоти слів.</li>
            <li><strong>Індекс читабельності (Readability ARI):</strong> Обчислення індексу автоматичної зрозумілості тексту для підтвердження його високого наукового статусу.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: ARCHITECTURAL FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр лінгвістичного та фізичного аудиту (Audit Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Наступна діаграма деталізує процес покрокового виконання 8 основних тестів якості тексту:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск quality_check.py <target>") --> OPEN_DOC("1. Відкриття файлу DOCX (Document)")
                
                OPEN_DOC --> TEST_1("2. check_margins(): Перевірка полів сторінки (см)")
                TEST_1 --> TEST_2("3. check_mixed_alphabets(): Детектор Cyrillic/Latin слів")
                
                TEST_2 --> TEST_3("4. check_formatting_rules(): Перевірка Times NR & 14pt")
                TEST_3 --> TEST_4("5. check_ai_style(): Дисперсія довжини речень")
                
                TEST_4 --> TEST_5("6. advanced_linguistic_analysis(): Лексичний індекс TTR")
                TEST_5 --> TEST_6("7. calculate_readability(): Обчислення індексу ARI")
                
                TEST_6 --> TEST_7("8. check_zipf_law(): Перевірка частотного розподілу слів")
                TEST_7 --> TEST_8("9. Structural Audit: Пошук розділів 'Зміст' та 'Джерела'")
                
                TEST_8 --> COMBINE_REP("10. Консолідація оцінок та формування звіту")
                COMBINE_REP --> PRINT_OUT("11. Виведення результатів в консоль (CLI)")
                
                PRINT_OUT --> END("Завершення аудиту")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичний апарат лінгвістичної експертизи</h2>
    </div>
    <div class="glass-card">
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Коефіцієнт словникового багатства TTR (Type-Token Ratio)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Індекс TTR відображає відношення кількості унікальних слів (лем/типів, $V$) до загальної кількості слів у тексті (токенів, $N$). Для якісних академічних текстів українською мовою значення має перевищувати $0.35$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    \text{TTR} = \frac{|V|}{N} \quad \implies \quad \text{Audit} = \begin{cases} 
                      \text{Pass}, & \text{TTR} \ge 0.35 \\
                      \text{Warning (AI signature)}, & \text{TTR} < 0.35 
                   \end{cases}
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Дисперсія довжини речень (Sentence Variance)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    AI-асистенти прагнуть писати речення однакової синтаксичної складності, що дає аномально низьку дисперсію $\sigma^2$ довжини речень $x_i$ відносно середнього значення $\mu$. Жива мова характеризується чергуванням довгих описів та коротких тверджень:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    \sigma^2 = \frac{1}{M} \sum_{i=1}^M (x_i - \mu)^2 \quad \implies \quad \text{Status} = \begin{cases} 
                      \text{Monotonous (AI)}, & \sigma^2 < 30 \\
                      \text{Natural (Human)}, & \sigma^2 \ge 30 
                   \end{cases}
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. Automated Readability Index (ARI)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Індекс ARI розраховує складність сприйняття тексту на основі середньої кількості символів у слові ($C/W$) та середньої кількості слів у реченні ($W/S$):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{ARI} = 4.71 \times \left( \frac{\text{Chars}}{\text{Words}} \right) + 0.5 \times \left( \frac{\text{Words}}{\text{Sentences}} \right) - 21.43 $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Значення $\text{ARI} > 16$ підтверджує складний науковий рівень викладу матеріалу.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">4. Математичний закон Ціпфа (Zipf's Law)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Закон Ціпфа стверджує, що в природних мовах частота зустрічальності $n$-го слова є обернено пропорційною до його рангу $n$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ f(n) \propto \frac{1}{n} \quad \implies \quad \frac{f(1)}{f(2)} \approx 2.0, \quad \frac{f(1)}{f(3)} \approx 3.0 $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Якщо відношення перших трьох частот ідеально вкладаються в межі $1.8 < R_2 < 2.2$ та $2.7 < R_3 < 3.3$, це свідчить про штучну генерацію тексту, оскільки математичні алгоритми ШІ намагаються штучно нормалізувати вихідний словник.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму лінгвістичного аудиту</h2>
    </div>
    <div class="glass-card">
        <p>
            Логіка перевірки змішаних алфавітів та валідації стилю:
        </p>
        <pre><code class="language-python">
# Псевдокод аудитора якості тексту
import re

def check_mixed_alphabets_detector(paragraphs):
    mixed_words_list = []
    cyrillic_chars = set("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя")
    latin_chars = set("abcdefghijklmnopqrstuvwxyz")
    
    for p in paragraphs:
        for word in p.split():
            # Очищаємо слово від розділових знаків
            clean_word = re.sub(r'[^\w]', '', word).lower()
            if not clean_word:
                continue
                
            has_cyr = any(c in cyrillic_chars for c in clean_word)
            has_lat = any(c in latin_chars for c in clean_word)
            
            # Якщо слово містить обидва алфавіти та не є абревіатурою / кодом
            if has_cyr and has_lat:
                if not re.search(r'\d', word) and '-' not in word:
                    mixed_words_list.append(word)
                    
    if len(mixed_words_list) > 0:
        return f"CRITICAL: Found {len(mixed_words_list)} mixed-alphabet words! High risk of Plagiarism Bypass."
    return "SUCCESS: Alphabets are clean."
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Навіщо потрібна перевірка на змішані алфавіти?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Це популярний недоброчесний прийом для обходу автоматичних систем перевірки унікальності (плагіату). Студенти замінюють українські літери `а`, `е`, `о`, `х`, `і` на ідентичні за виглядом латинські літери `a`, `e`, `o`, `x`, `i`. Людина не бачить різниці під час читання, але системи перевірки сприймають таке слово як помилкове або унікальне. Скрипт миттєво виявляє цей саботаж і захищає академічну репутацію проєкту.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Чому ідеальний розподіл слів за Законом Ціпфа є підозрілим?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Людська мова є природно хаотичною та емоційною. Людина може часто використовувати певні терміни в одному розділі та повністю забути про них у наступному. Натомість великі мовні моделі (LLM) працюють на базі статистичних розподілів імовірностей наступного слова. Це призводить до того, що на великих обсягах тексту ШІ генерує ідеально згладжені, статистично "правильні" криві частот Ціпфа, що є очевидним цифровим відбитком машини.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Які наслідки виявлення помилок у полях сторінки?</h4>
        <p style="color: var(--text-dim);">
            A: Стандарт ДСТУ висуває жорсткі вимоги: ліве поле має бути рівно 3.0 см (для можливості плетіння/брошурування диплома), праве — 1.0 см, верхнє та нижнє — по 2.0 см. Порушення цих вимог навіть на 2-3 міліметри призведе до того, що під час друку текст або сховається в палітурку, або вийде за межі друкованої області. Скрипт страхує автора від нормоконтролю на етапі верстки.
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
