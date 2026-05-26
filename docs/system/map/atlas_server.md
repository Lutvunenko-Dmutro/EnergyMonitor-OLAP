# Технічний Паспорт Компонента: scripts/system/atlas_server.py (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">🌐 INTERACTIVE REPL BACKEND & DYNAMIC EXECUTION HUB</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">🔌</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">atlas_server.py</h1>
            <p class="mega-subtitle">Інтерактивний виконавчий сервер REPL, місток динамічного виконання функцій та хостинг-провайдер Атласу</p>
            <div class="status-tags">
                <span class="tag tag-online">REPL SERVER</span>
                <span class="tag tag-version">v3.0.0</span>
                <span class="tag tag-role">EXECUTION BRIDGE</span>
            </div>
        </div>
    </div>
</div>

<!-- KEY METRICS GRID -->
<div class="metrics-grid">
    <div class="glass-card metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-info">
            <span class="metric-label">Server Port</span>
            <span class="metric-value">TCP 8001</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🔄</div>
        <div class="metric-info">
            <span class="metric-label">Execution Engine</span>
            <span class="metric-value">importlib.reload</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">📡</div>
        <div class="metric-info">
            <span class="metric-label">Dynamic API</span>
            <span class="metric-value">POST /run (CORS *)</span>
        </div>
    </div>
    <div class="glass-card metric-card">
        <div class="metric-icon">🧹</div>
        <div class="metric-info">
            <span class="metric-label">Output Capture</span>
            <span class="metric-value">sys.stdout (StringIO)</span>
        </div>
    </div>
</div>

<!-- SECTION 1: SYSTEM OVERVIEW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">01</span>
        <h2 class="section-title">Концептуальне призначення виконавчого сервера</h2>
    </div>
    <div class="glass-card">
        <p>
            Модуль <code>scripts/system/atlas_server.py</code> є ключовим **виконавчим містком** (Atlas Interactive REPL Server) в архітектурі платформи <b>Energy Monitor Ultimate</b>. Він створює динамічний зв'язок між статичною документацією проєкту (Атласом) та живим середовищем виконання Python, дозволяючи запускати будь-яку функцію системи безпосередньо з веб-інтерфейсу в один клік.
        </p>
        <p style="margin-top: 10px;">
            Основний функціонал сервера:
        </p>
        <ul style="margin-left: 20px; color: var(--text-dim);">
            <li><strong>Хостинг інтерактивного Атласу (Static Server):</strong> Обслуговування веб-документів, стилів та скриптів Атласу з локальної директорії <code>docs/atlas</code>.</li>
            <li><strong>Динамічний запуск функцій (Dynamic API):</strong> Обробка вхідних POST-запитів на роут <code>/run</code>, десериалізація назв модулів, методів та переданих аргументів.</li>
            <li><strong>Гаряче перевантаження коду (Hot Reloading):</strong> Використання <code>importlib.reload</code> для автоматичного застосування будь-яких правок у кодовій базі без потреби перезавантажувати сам виконавчий сервер.</li>
            <li><strong>Безпечне перехоплення виводу (stdout redirection):</strong> Підміна стандартного потоку виведення <code>sys.stdout</code> на об'єкт <code>io.StringIO</code> для трансляції логів та принтованих результатів виконання функції назад у браузерний термінал.</li>
        </ul>
    </div>
</div>

<!-- SECTION 2: DYNAMIC REPL EXECUTION FLOW -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">02</span>
        <h2 class="section-title">Життєвий цикл динамічного виконання (REPL API Pipeline)</h2>
    </div>
    <div class="glass-card">
        <p>
            Схема відображає шлях проходження HTTP POST запиту на роут `/run` від браузера до виконання коду:
        </p>
        <div class="diagram-outer-wrapper">
            <div class="mermaid">
            sequenceDiagram
                autonumber
                participant Client as Браузер (Atlas UI)
                participant Server as atlas_server.py
                participant Lib as importlib Engine
                participant Code as Системна Функція
                participant Buffer as io.StringIO
                
                Client->>Server: HTTP POST /run (JSON payload: module, function, args)
                Server->>Server: Додавання src/ до sys.path
                Server->>Buffer: Підміна sys.stdout = io.StringIO()
                
                alt Модуль не завантажено
                    Server->>Lib: import_module(module_name)
                else Модуль вже у пам'яті
                    Server->>Lib: reload(module) (Hot Reloading!)
                end
                
                Lib->>Server: Повернення об'єкта модуля
                Server->>Code: Виклик func(*args, **kwargs)
                Code->>Buffer: Вивід у консоль (print / log)
                Code->>Server: Повернення результату (result)
                Server->>Buffer: getvalue() (Зчитування логів)
                Server->>Buffer: Відновлення sys.stdout
                Server->>Client: HTTP 200 (JSON response: status, output, result)
            </div>
        </div>
    </div>
</div>

<!-- SECTION 3: TECHNICAL DETAILS -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">03</span>
        <h2 class="section-title">Інженерні рішення та гаряче перевантаження модулів</h2>
    </div>
    <div class="glass-card">
        
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">1. Механізм Hot Reloading (importlib.reload)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Якщо розробник вносить зміни в логіку ШІ-прогнозу або симулятора, стандартний імпорт Python завантажить версію з кешу пам'яті СУБД. Виклик <code>importlib.reload(module)</code> примусово оновлює внутрішній об'єкт модуля актуальним кодом з диска. Це дозволяє розробляти, тестувати та демонструвати правки коду в реальному часі без рестарту сервера.
                </p>
            </div>
            
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">2. Перехоплення потоку stdout (Redirection Buffer)</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    Коли викликана функція робить `print` або записує повідомлення в лог, ці дані потрапляють у консоль сервера і губляться для веб-користувача. Скрипт перехоплює потік за допомогою контекстного буфера:
                </p>
                <div style="font-family: monospace; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; display: block; color: var(--text-main); font-size: 13px; overflow-x: auto; margin-bottom: 8px;">
                    redirected_output = sys.stdout = io.StringIO()<br>
                    # Виконання коду...<br>
                    output = redirected_output.getvalue()
                </div>
                <p style="margin: 0; font-size: 13.5px; color: var(--text-dim);">
                    Це дозволяє відобразити консольне виведення безпосередньо у віртуальному терміналі на сторінці Атласу.
                </p>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 15px; border-radius: 8px;">
                <h4 style="color: var(--accent); margin: 0 0 8px 0; font-family: 'Orbitron', sans-serif;">3. CORS-політика та OPTIONS запити</h4>
                <p style="margin: 0 0 8px 0; font-size: 13.5px; color: var(--text-dim);">
                    При зверненні до сервера з іншого порту або домену браузери надсилають попередній запит <code>OPTIONS</code> (Preflight Request). Сервер підтримує CORS-заголовки `Access-Control-Allow-Origin: *` та метод <code>do_OPTIONS()</code>, знімаючи будь-які обмеження на крос-доменні запити під час розробки.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- SECTION 4: PSEUDOCODE -->
<div class="section-container">
    <div class="section-header">
        <span class="section-number">04</span>
        <h2 class="section-title">Псевдокод циклу REPL-обробника</h2>
    </div>
    <div class="glass-card">
        <p>
            Алгоритм динамічного імпорту, гарячого перезавантаження та виконання коду:
        </p>
        <pre><code class="language-python">
# Псевдокод обробника запитів /run
def handle_post_run_request(json_payload):
    # 1. Парсинг JSON параметрів
    module_name = json_payload.get("module")
    func_name = json_payload.get("function")
    args = json_payload.get("args", [])
    
    # 2. Перехоплення stdout
    old_stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer
    
    try:
        # 3. Гарячий імпорт модуля з диска
        imported_module = importlib.import_module(module_name)
        importlib.reload(imported_module) # Гаряче оновлення!
        
        # 4. Пошук та виконання функції
        executable_func = getattr(imported_module, func_name)
        result = executable_func(*args)
        
        return {
            "status": "success",
            "output": buffer.getvalue(),
            "result": repr(result)
        }
    except Exception as e:
        return {
            "status": "error",
            "output": buffer.getvalue(),
            "error": str(e),
            "traceback": traceback.format_exc()
        }
    finally:
        # 5. Обов'язкове відновлення stdout
        sys.stdout = old_stdout
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
        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q1: Чому при старті сервера змінюється робоча папка за допомогою os.chdir()?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Скрипт сервера знаходиться у піддиректорії <code>scripts/system/</code>. Якщо запустити його з цієї папки, всі відносні шляхи до баз даних (наприклад, <code>data/energy.db</code>) або моделей у коді аналітики зламаються. Зміна робочої папки на корінь проєкту перед запуском гарантує, що всі імпорти та файлові операції у викликаних функціях будуть працювати абсолютно коректно.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q2: Що станеться, якщо викликана функція зависне у нескінченному циклі?</h4>
        <p style="color: var(--text-dim); margin-bottom: 15px;">
            A: Оскільки HTTP-сервер є однопотоковим, нескінченне виконання заблокує сервер. У продуктивному середовищі рекомендується встановлювати тайм-аути на запити, проте для локальної REPL-розробки достатньо зупинити сервер у консолі клавішами <code>Ctrl+C</code>.
        </p>

        <h4 style="color: var(--text-main); margin-bottom: 5px;">Q3: Як запустити виконавчий сервер REPL?</h4>
        <p style="color: var(--text-dim);">
            A: Достатньо виконати команду: <code>python scripts/system/atlas_server.py</code>, після чого сервер почне прослуховувати порт 8001.
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
