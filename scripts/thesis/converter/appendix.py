"""
ГЕНЕРАТОР ТЕХНІЧНИХ ДОДАТКІВ (Source Code Appendix Generator)
===========================================================
Модуль для автоматичного формування додатків до пояснювальної записки диплома.
Забезпечує:
1. Recursive Harvesting: автоматичний збір вихідного коду згідно з білим списком (WHITELIST_FILES).
2. Document Formatting: структуроване додавання коду в об'єкт документа (docx) через кастомні хендлери.
3. Path Normalization: формування релятивних шляхів для коректної ідентифікації модулів у звіті.
Гарантує автоматичне оновлення лістингів коду в документації при зміні розробки.
"""
import os
from .handlers import add_h1, add_h2, add_code
from .config import WHITELIST_FILES

def add_source_code_appendix(doc, src_dir):
    """Збирає ключовий код із src для Додатків."""
    if not os.path.exists(src_dir): return
    
    add_h1(doc, "ДОДАТОК Л. ПОВНИЙ ЛІСТИНГ КЛЮЧОВИХ МОДУЛІВ ПРОЄКТУ")
    
    for root, dirs, files in os.walk(src_dir):
        if "__pycache__" in dirs: dirs.remove("__pycache__")
        for file in files:
            if file in WHITELIST_FILES:
                rel_path = os.path.relpath(os.path.join(root, file), os.getcwd())
                add_h2(doc, f"Файл: {rel_path}")
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f_code:
                        add_code(doc, f_code.read().splitlines())
                except Exception as e:
                    print(f" [WARN] Read ERR {file}: {e}")
