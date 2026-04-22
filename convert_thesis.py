"""
ГОЛОВНИЙ ЗАПУСКНИЙ ФАЙЛ КОНВЕРТЕРА ДИПЛОМУ v2.2
Пакетна збірка тепер включає ВСІ розділи та офіційні бланки.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.converter.engine import run_conversion
from scripts.converter.config import INPUT, OUTPUT
from scripts.collect_stats import get_stats

# Повний перелік модулів для збірки
THESIS_MODULES = [
    "OFFICIAL_TITLE_PAGE.md",
    "OFFICIAL_TASK_STATEMENT.md",
    "OFFICIAL_REVIEW_PROJECT.md",
    "OFFICIAL_RECENSION_PROJECT.md",
    "THESIS_0_ABSTRACT.md",
    "THESIS_0_INTRODUCTION.md",
    "THESIS_1_THEORY.md",
    "THESIS_2_REQUIREMENTS.md",
    "THESIS_3_DESIGN_AND_IMPLEMENTATION_EXPANDED.md",
    "THESIS_FINAL_CONCLUSIONS.md",
    "BIBLIOGRAPHY.md",
    "ABBREVIATIONS.md",
    "APPENDICES.md"
]

def run_batch_conversion():
    print("\n>>> ЗАПУСК ПОВНОЇ ЗБІРКИ ДИПЛОМА v2.2 <<<")
    for f in THESIS_MODULES:
        in_p = os.path.join("docs", "thesis", f)
        out_name = f.replace(".md", ".docx").replace("_EXPANDED", "")
        out_p = os.path.join("docs", "thesis", "check_pages", out_name)
        
        print(f"Обробка: {f:45} -> {out_name}")
        try:
            run_conversion(in_p, out_p, include_appendix=False)
        except Exception as e:
            print(f" [ERR] Помилка при обробці {f}: {e}")
    
    print("\n>>> ПАКЕТНУ ЗБІРКУ ЗАВЕРШЕНО <<<")
    get_stats()

if __name__ == "__main__":
    if "--all" in sys.argv:
        run_batch_conversion()
    else:
        input_file = sys.argv[1] if len(sys.argv) > 1 else INPUT
        output_file = sys.argv[2] if len(sys.argv) > 2 else OUTPUT
        include_appendix = "--no-appendix" not in sys.argv
        run_conversion(input_file, output_file, include_appendix=include_appendix)
