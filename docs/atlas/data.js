// БАЗА ДАНИХ АТЛАСУ (v15.0 Museum Edition)
const REPO_ROOT_URL = "https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/";

// 🏛️ МАРШРУТ ЕКСКУРСІЇ (Для рецензента)
const TOUR_STEPS = [
    { 
        id: "ROOT", 
        title: "Точка входу: Project Master", 
        txt: "Вітаємо в проекті EnergyMonitor. Це верхівка нашої архітектурної піраміди, де координуються всі системні виклики." 
    },
    { 
        id: "ROOT/main.py", 
        title: "Ядро Системи (Main Engine)", 
        txt: "Головний файл запуску. Саме тут ініціалізується OLAP-куб та запускається моніторинг енергетичних потоків у реальному часі." 
    },
    { 
        id: "ROOT/data/energy.db", 
        title: "Фундамент Даних (SQLite)", 
        txt: "База даних енергетичного моніторингу. Тут зберігається вся історія споживання та метадані об'єктів моніторингу." 
    },
    { 
        id: "ROOT/diagnose.py", 
        title: "Діагностичний Центр", 
        txt: "Критичний модуль для аудиту стану системи та виявлення аномальних енергетичних стрибків." 
    },
    { 
        id: "ROOT/docs/architecture.md", 
        title: "Цифровий Двійник (Architecture)", 
        txt: "Документація, що описує взаємозв'язки. Ця мапа, яку ви бачите — є живою реалізацією цього документу." 
    },
    { 
        id: "ROOT/docs/thesis/THESIS_FINAL.docx", 
        title: "Фінальний Звіт (Диплом)", 
        txt: "Пояснювальна записка. Документ, що містить повну теоретичну та розрахункову базу проекту." 
    }
];

// ІЄРАРХІЯ ПРОЕКТУ
const PROJECT_HIERARCHY = {
    "ROOT": [".env", "ARCHITECTURE.md", "main.py", "diagnose.py", "data/", "docs/", "requirements.txt"],
    "ROOT/data/": ["energy.db"],
    "ROOT/docs/": ["architecture.md", "CLEAN_PROJECT_TREE.txt", "thesis/"],
    "ROOT/docs/thesis/": ["THESIS_FINAL.docx", "DIPLOMA_PLAN.md"]
};

// СТИЛІЗАЦІЯ ГІЛОК
const BRANCH_STYLING = {
    "data/": { color: "#f59e0b", label: "DATABASE_LAYER" },
    "docs/": { color: "#8b5cf6", label: "DOCUMENTATION" },
    ".py": { color: "#3b82f6", label: "CORE_LOGIC" },
    "default": { color: "#64748b", label: "SYSTEM_UNIT" }
};

// БАЗА ТЕХНІЧНИХ ОПИСІВ (Прискорена)
const NODE_DESCRIPTIONS = {
    "main.py": { txt: "Точка входу додатку. Керує життєвим циклом OLAP-процесів та Streamlit інтерфейсом." },
    "energy.db": { txt: "Реляційна база даних (SQLite). Містить оптимізовані таблиці для швидкої аналітики енерговитрат." },
    "diagnose.py": { txt: "Скрипт перевірки цілісності даних та діагностики підключення до Neon DB." },
    "architecture.md": { txt: "Головна технічна специфікація архітектури рішення. Описує потоки даних." },
    "THESIS_FINAL.docx": { txt: "Повний текст дипломної роботи, підготовлений згідно ДСТУ." }
};
