# 📍 Інженерний Атлас Системи (SCADA-стиль)

Це інтерактивна схема "Цифрового Двійника" вашого проєкту. Вона відображає функціональні вузли системи та їхній зв'язок з програмним кодом.

> [!TIP]
> **Клікніть на будь-який блок схеми**, щоб відкрити детальну документацію відповідного модуля.

<div class="atlas-v4-container">
    <svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg" class="atlas-svg">
        <!-- Дефініції для ефектів -->
        <defs>
            <filter id="glow">
                <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
            <linearGradient id="grad-core" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#fb923c;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#ea580c;stop-opacity:1" />
            </linearGradient>
        </defs>

        <!-- Зв'язки (Лінії) -->
        <g class="connections" stroke="#475569" stroke-width="2" fill="none">
            <path d="M150 250 L300 250" class="flow-line" /> <!-- Sensors to Core -->
            <path d="M500 250 L650 250" class="flow-line" /> <!-- Core to UI -->
            <path d="M400 200 L400 100" class="flow-line" /> <!-- Core to ML -->
            <path d="M400 300 L400 400" class="flow-line" /> <!-- Core to DB -->
        </g>

        <!-- Вузли (Об'єкти) -->
        
        <!-- 📡 Sensors Layer -->
        <g class="node-group" onclick="window.location.hash='#srcservicesdatageneratorpy'">
            <rect x="50" y="210" width="100" height="80" rx="10" class="node-rect sensors" />
            <text x="100" y="245" text-anchor="middle" class="node-label">📡 ДЖЕРЕЛА</text>
            <text x="100" y="265" text-anchor="middle" class="node-sub">Sensors & API</text>
        </g>

        <!-- ⚡ Physics Engine (Core) -->
        <g class="node-group" onclick="window.location.hash='#srccorephysicspy'">
            <rect x="300" y="200" width="200" height="100" rx="15" class="node-rect core" />
            <text x="400" y="245" text-anchor="middle" class="node-label-main">⚡ GRID ENGINE</text>
            <text x="400" y="270" text-anchor="middle" class="node-sub">physics.py & math</text>
        </g>

        <!-- 🧠 ML Brain -->
        <g class="node-group" onclick="window.location.hash='#srcmlpredict_v2py'">
            <circle cx="400" cy="80" r="60" class="node-circle ml" />
            <text x="400" y="75" text-anchor="middle" class="node-label">🧠 ШІ-ЯДРО</text>
            <text x="400" y="95" text-anchor="middle" class="node-sub">LSTM Predictor</text>
        </g>

        <!-- 💾 Database Storage -->
        <g class="node-group" onclick="window.location.hash='#srccoredatabasepy'">
            <path d="M350 400 L450 400 L450 460 L350 460 Z" class="node-rect db" />
            <text x="400" y="430" text-anchor="middle" class="node-label">💾 OLAP DB</text>
            <text x="400" y="450" text-anchor="middle" class="node-sub">PostgreSQL</text>
        </g>

        <!-- 📊 Dashboard UI -->
        <g class="node-group" onclick="window.location.hash='#srcuidashboardpy'">
            <rect x="650" y="210" width="100" height="80" rx="10" class="node-rect ui" />
            <text x="700" y="245" text-anchor="middle" class="node-label">📊 ПАНЕЛЬ</text>
            <text x="700" y="265" text-anchor="middle" class="node-sub">Streamlit UI</text>
        </g>
    </svg>
</div>

<style>
.atlas-v4-container {
    background: #0f172a;
    padding: 40px;
    border-radius: 20px;
    border: 1px solid #1e293b;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    margin: 20px 0;
}

.node-group {
    cursor: pointer;
    transition: all 0.3s ease;
}

.node-rect {
    fill: #1e293b;
    stroke: #475569;
    stroke-width: 2;
    transition: 0.3s;
}

.node-rect.core { stroke: #fb923c; fill: rgba(251, 146, 60, 0.1); }
.node-rect.sensors { stroke: #38bdf8; }
.node-rect.ui { stroke: #4ade80; }
.node-rect.db { stroke: #94a3b8; }
.node-circle.ml { fill: rgba(192, 132, 252, 0.1); stroke: #c084fc; stroke-width: 2; }

.node-group:hover .node-rect, .node-group:hover .node-circle {
    filter: url(#glow);
    stroke-width: 4;
}

.node-label { fill: #f1f5f9; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: bold; pointer-events: none; }
.node-label-main { fill: #fff; font-family: 'Inter', sans-serif; font-size: 18px; font-weight: 900; pointer-events: none; }
.node-sub { fill: #94a3b8; font-family: 'JetBrains Mono', monospace; font-size: 10px; pointer-events: none; }

.flow-line {
    stroke-dasharray: 5;
    animation: flow 20s linear infinite;
}

@keyframes flow {
    from { stroke-dashoffset: 100; }
    to { stroke-dashoffset: 0; }
}
</style>

---

## 🗺️ Як користуватися Атласом
1.  **Об'єкти**: Кожен блок представляє фізичний або логічний компонент системи.
2.  **Потоки**: Пунктирні лінії показують рух даних (наприклад, від Датчиків до Ядра).
3.  **Перехід**: Натисніть на назву вузла, щоб автоматично прокрутити сторінку до технічного опису цього файлу нижче.

---

## 📄 Детальний опис модулів

<a id="srcservicesdatageneratorpy"></a>
### 📡 Джерела даних (services/data_generator.py)
Модуль відповідає за генерацію реалістичних даних навантаження та зчитування зовнішніх API погоди.
- **Функція**: Симуляція Smart City оточення.
- [Перейти до коду модуля](https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/src/services/data_generator.py)

<a id="srccorephysicspy"></a>
### ⚡ Фізичне ядро (core/physics.py)
Розрахунок технічних параметрів мережі: втрати потужності, падіння напруги, температурна деградація.
- **Функція**: Математичне моделювання мережі.
- [Читати більше про фізику](digital_twin.md)

<a id="srcmlpredict_v2py"></a>
### 🧠 ШІ-Прогнозування (ml/predict_v2.py)
Використання навченої моделі LSTM для генерації прогнозів на 24 години вперед.
- **Модель**: v3.1 (Stable).
- [Деталі архітектури ML](../ml/index.md)

<a id="srccoredatabasepy"></a>
### 💾 База даних (core/database.py)
Забезпечення цілісності даних та виконання OLAP-запитів.
- **Сховище**: PostgreSQL / Neon.
- [Схема бази даних](database.md)

<a id="srcuidashboardpy"></a>
### 📊 Інтерфейс користувача (ui/dashboard.py)
Головна панель управління для диспетчера.
- **Фреймворк**: Streamlit.
- [Гайд по інтерфейсу](../guides/USER_MANUAL.md)
