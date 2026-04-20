const nodeData = {
    sensors: {
        title: "Digital Twin (Цифровий двійник)",
        desc: "Генерує телеметрію в реальному часі через <code>src/services/data_generator.py</code>. Використовує фізичні моделі деградації трансформаторів та розрахунку втрат для імітації реального навантаження мережі.",
        stat: { val: "10ms", label: "Sync Latency" }
    },
    db: {
        title: "OLAP Data Lake (PostgreSQL)",
        desc: "Центральне сховище даних. Зберігає мільйони записів телеметрії та результати прогнозів. Оптимізовано для швидких аналітичних запитів через індексацію часових рядів.",
        stat: { val: "Neon", label: "Cloud Engine" }
    },
    ai: {
        title: "Intelligence Engine (LSTM v3)",
        desc: "Прогнозує навантаження на 24 години вперед. Використовує рекурентні нейромережі. Гібридний підхід з <b>SARIMA Fallback</b> забезпечує стабільність при аномаліях у даних.",
        stat: { val: "97.1%", label: "Accuracy" }
    },
    ui: {
        title: "Executive Dashboard (Streamlit)",
        desc: "Візуалізує KPI, ГІС-карту підстанцій та інтерактивні прогнози. Побудований на <b>Zero-Flicker</b> архітектурі для миттєвого оновлення аналітики без перезавантаження сторінки.",
        stat: { val: "Real-time", label: "Update" }
    }
};

const nodes = document.querySelectorAll('.node');
const detailTitle = document.getElementById('detail-title');
const detailDesc = document.getElementById('detail-desc');
const modelVer = document.getElementById('model-ver');
const simulateBtn = document.getElementById('simulate-btn');
const flows = document.querySelectorAll('.data-flow');

nodes.forEach(node => {
    node.addEventListener('click', () => {
        const id = node.getAttribute('data-info');
        const data = nodeData[id];

        // Анімація контенту
        detailTitle.style.opacity = 0;
        detailDesc.style.opacity = 0;

        setTimeout(() => {
            detailTitle.innerHTML = data.title;
            detailDesc.innerHTML = data.desc;
            detailTitle.style.opacity = 1;
            detailDesc.style.opacity = 1;
            
            // Оновлюємо статистику
            modelVer.innerText = data.stat.val;
            modelVer.nextElementSibling.innerText = data.stat.label;
        }, 200);

        // Підсвічування активного вузла
        nodes.forEach(n => n.style.borderColor = 'rgba(255, 255, 255, 0.1)');
        node.style.borderColor = 'var(--primary)';
    });
});

// Симуляція потоку даних
simulateBtn.addEventListener('click', () => {
    simulateBtn.disabled = true;
    simulateBtn.innerHTML = '<i data-lucide="loader"></i> SIMULATING...';
    lucide.createIcons();

    let delay = 0;
    flows.forEach(flow => {
        setTimeout(() => {
            flow.querySelector('.flow-dot').style.animation = 'flow 1s infinite linear';
            setTimeout(() => {
                flow.querySelector('.flow-dot').style.animation = 'flow 3s infinite linear';
            }, 3000);
        }, delay);
        delay += 500;
    });

    setTimeout(() => {
        simulateBtn.disabled = false;
        simulateBtn.innerHTML = '<i data-lucide="play"></i> RUN DATA SIMULATION';
        lucide.createIcons();
    }, 5000);
});
