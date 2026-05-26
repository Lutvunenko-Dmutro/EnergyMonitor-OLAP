# Технічний Паспорт Компонента: scripts/ml/benchmark.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🧠 HUMAN COGNITIVE STATE BENCHMARKER</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">👁️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">benchmark.py</h1>
            <p class="mega-subtitle">Експериментальний бенчмарк когнітивного стану та розпізнавання емоцій диспетчерів енергосистеми</p>
            <div class="status-tags">
                <span class="tag tag-online">COGNITIVE SENTRY</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">HUMAN FACTOR LAB</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-info">
            <span class="metric-label">Model Engine</span>
            <span class="metric-value">DeepFace / VGG-Face</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🎭</div>
        <div class="metric-info">
            <span class="metric-label">Target Emotions</span>
            <span class="metric-value">4 classes</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-info">
            <span class="metric-label">Metric</span>
            <span class="metric-value">Accuracy / FPS</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📂</div>
        <div class="metric-info">
            <span class="metric-label">Dataset Dir</span>
            <span class="metric-value">dataset/ (Auto-gen)</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальна роль розпізнавання емоцій</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/ml/benchmark.py</code> є експериментальним ядром для дослідження **людського фактору** (Human Factors in Grid Management) в межах платформи <b>Energy Monitor Ultimate</b>. Його мета — оцінити якість роботи ШІ-моделей комп'ютерного зору (Computer Vision) при розпізнаванні емоційного та психологічного стану чергових диспетчерів енергосистеми.
        </p>
        <p style="margin-top: 10px;">
            Ключові сфери застосування бенчмарку:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Orchestration тестових папок:</strong> Автоматичне створення структурованого репозиторію тестових зображень за чотирма основними емоціями: <i>happy</i>, <i>sad</i>, <i>angry</i>, <i>neutral</i>.</li>
            <li><strong>Facial Inference (Аналіз DeepFace):</strong> Тестування згорткових нейронних мереж на реальних портретних зображеннях для точного визначення міміки обличчя оператора.</li>
            <li><strong>Метрика швидкодії (FPS Profiling):</strong> Оцінка частоти обробки кадрів відеопотоку у реальному часі (Frames Per Second) для забезпечення сумісності з HUD-екранами.</li>
            <li><strong>Калькуляція точності (Scientific Accuracy):</strong> Розрахунок відсотка правильних класифікацій емоцій порівняно з еталонною розміткою папок.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: GRAPHICAL PIPELINE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Конвеєр когнітивного аудиту (Cognitive Sentry Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема відображає послідовність етапів ініціалізації та проходження бенчмарку розпізнавання емоцій:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            graph TD
                START("Запуск: benchmark.py") --> INIT_DIR("1. Автоматичне створення папок dataset/ happy, sad, angry, neutral")
                INIT_DIR --> SCAN_IMAGES("2. Підрахунок зображень (total_images_found)")
                
                SCAN_IMAGES --> CHECK_COUNT{"3. Фото присутні?"}
                CHECK_COUNT -- "Порожньо (0)" --> PRINT_GUIDE("Показати інструкцію та Exit")
                CHECK_COUNT -- "Присутні (>0)" --> START_LOOP("4. Старт циклу обходу фотографій")
                
                START_LOOP --> DEEPFACE_CALL("5. DeepFace.analyze(img, actions=['emotion'])")
                DEEPFACE_CALL --> EXTRACT_EMOTION("6. Отримання dominant_emotion")
                EXTRACT_EMOTION --> COMPARE_EMOTION{"7. Прогноз == Справжня?"}
                
                COMPARE_EMOTION -- "Так" --> CORRECT("Status: ВГАДАНО (correct+1)")
                COMPARE_EMOTION -- "Ні" --> ERROR("Status: ПОМИЛКА")
                
                CORRECT & ERROR --> CHECK_LAST{"8. Останнє фото?"}
                CHECK_LAST -- "Ні" --> START_LOOP
                CHECK_LAST -- "Так" --> CALC_METRICS("9. Калькуляція: Accuracy, FPS, Time")
                
                CALC_METRICS --> PRINT_REPORT("10. Вивід фінальних результатів у консоль")
                PRINT_REPORT --> END("Кінець бенчмарку")
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS & MATHEMATICS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Математичне оцінювання точності та швидкодії</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Точність розпізнавання (Accuracy)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Визначається як відношення правильно вгаданих емоцій $C_{\text{correct}}$ до загальної кількості оброблених фотографій $N$:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{Accuracy} = \frac{C_{\text{correct}}}{N} \times 100\% $$
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Швидкість обробки в кадрах за секунду (FPS - Frames Per Second)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Характеризує пропускну здатність алгоритму нейромережі на конкретному процесорі/відеокарті:
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{FPS} = \frac{N}{T_{\text{processing}}} $$
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Для стабільного моніторингу диспетчера у відеопотоці реального часу FPS має бути не менше **5-10 кадрів/сек**.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. dominant_emotion (Евристика виділення емоцій)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Зі згорткового шару DeepFace повертається вектор ймовірностей для 7 класів емоцій. Ми виділяємо клас із максимальною ймовірністю (також відомий як `dominant_emotion`):
                </p>
                <div class="math-block" style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-family: monospace; color: var(--accent);">
                    $$ \text{Dominant Emotion} = \arg\max_{e \in E} P(e) $$
                </div>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод алгоритму розпізнавання емоцій</h2>
    </div>
    <div class="glass-card">
        <p>
            Логіка обробки зображень та збору статистики точності DeepFace:
        </p>
        <pre><code class="language-python">
# Псевдокод бенчмаркінгу комп'ютерного зору
def run_emotion_benchmark():
    emotions = ["happy", "sad", "angry", "neutral"]
    correct_count = 0
    total_processed = 0
    start_time = get_timestamp()
    
    for true_emotion in emotions:
        images_in_folder = get_files_from_dir("dataset/" + true_emotion)
        
        for img in images_in_folder:
            total_processed += 1
            try:
                # DeepFace аналіз без примусового детектування обличчя (запобігає падінню)
                result = DeepFace.analyze(img_path=img, actions=['emotion'], enforce_detection=False)
                predicted_emotion = result[0]['dominant_emotion']
                
                if predicted_emotion == true_emotion:
                    correct_count += 1
            except Exception as e:
                log.warning(f"Помилка аналізу {img}: {e}")
                
    processing_time = get_timestamp() - start_time
    accuracy = (correct_count / total_processed) * 100.0
    fps = total_processed / processing_time
    
    return accuracy, fps
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому використовується параметр enforce_detection=False?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: За замовчуванням, бібліотека DeepFace намагається знайти чітке обличчя у кадрі за допомогою детектора (наприклад, MTCNN або RetinaFace). Якщо на фото людина повернута боком або освітлення слабке, детектор не знайде обличчя і викине помилку <code>ValueError</code>, що зупинить роботу бенчмарку. Вимкнення цього параметру дозволяє моделі спробувати розпізнати емоцію на всій площі картинки, гарантуючи стійкість тесту.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Які вимоги до фотографій у тестовому датасеті?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Фотографії мають бути у звичайних растрових форматах (PNG, JPG, JPEG). Для отримання репрезентативних метрик рекомендується використовувати реальні знімки облич диспетчерів з чітким виразом міміки в анфас при нормальному освітленні.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як запустити цей бенчмарк?</h4>
        <p style="color: var(--text-dim);">
            A: Закиньте по кілька зображень у відповідні підпапки каталогу <code>dataset/</code> і виконайте команду: <code>python scripts/ml/benchmark.py</code>
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
