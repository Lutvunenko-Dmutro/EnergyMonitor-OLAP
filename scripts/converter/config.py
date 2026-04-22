import os

INPUT     = "docs/thesis/THESIS_FULL_FINAL_UTF8.md"
OUTPUT    = "docs/thesis/THESIS_FINAL.docx"

# Словник замін Mermaid на фото
MERMAID_MAP = {
    "graph LR\n    subgraph RNN": ("diag_lstm_compare.png", "Рис. 1.1. Схематичне порівняння архітектур Simple RNN та LSTM"),
    "flowchart LR\n    User":    ("diag_use_case.png",    "Рис. 3.1. Діаграма прецедентів системи EnergyMonitor"),
    "stateDiagram-v2":            ("diag_sequence_1.png",  "Рис. 3.3. Діаграма послідовності (Частина 1)"),
    "graph TB\n    subgraph UI": ("diag_architecture.png", "Рис. 3.0. Архітектурна схема системи EnergyMonitor-OLAP"),
    "graph TD\n    subgraph Local": ("diag_infra_cloud.png", "Рис. 3.2. Схема розгортання та потоків даних системи"),
    "sequenceDiagram":            ("diag_sequence_horizontal.png", "Рис. 3.1. Детальна діаграма послідовності взаємодії компонентів"),
    "erDiagram":                  ("diag_er_db.png",       "Рис. 3.4. Схема бази даних (ER-діаграма)"),
    "flowchart LR\n    Push":    ("diag_cicd_pipeline.png", "Рис. 3.5. Схема CI/CD конвеєра автоматизації")
}

# Білий список модулів для додатків (оптимізовно для рівно 80 сторінок)
WHITELIST_FILES = [
    "physics.py", "predict_v2.py", "vectorizer.py", "metrics_engine.py",
    "data_generator.py", "forecast.py", "kpi.py", "alerts.py", "map.py"
]
