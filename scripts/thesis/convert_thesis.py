"""
ОРКЕСТРАТОР КОНВЕРТАЦІЇ ДИПЛОМНОЇ РОБОТИ (Thesis Conversion Orchestrator)
=====================================================================
Головний скрипт для автоматизованої збірки та конвертації тексту дисертації.
Ключові можливості:
1. Batch Document Conversion: пакетна обробка всіх розділів диплома в один прохід.
2. Markdown to Docx Transformation: перетворення MD-файлів у професійні DOCX-документи.
3. Academic Module Management: управління переліком бланків, розділів та додатків.
4. Statistics Integration: автоматичний збір метрик тексту після завершення збірки.
Забезпечує швидку підготовку фінальних матеріалів для захисту дипломного проєкту.
"""
# Додаємо корінь проєкту до шляху, щоб працювали імпорти src та scripts
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.thesis.converter.engine import run_conversion
from scripts.thesis.converter.config import INPUT, OUTPUT
from scripts.thesis.collect_stats import get_stats

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
