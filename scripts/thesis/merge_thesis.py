"""
ІНСТРУМЕНТ СТРУКТУРНОГО ЗЛИТТЯ ДИПЛОМА (Thesis Structural Merger)
==============================================================
Спеціалізована утиліта для об'єднання окремих розділів дисертації в єдиний документ.
Ключові можливості:
1. Sequential Consolidation: автоматичне злиття 13+ файлів у визначеній послідовності.
2. Structure Preservation: забезпечення логічних розривів та форматування між розділами.
3. UTF-8 Standardization: приведення кодування до єдиного стандарту для усунення помилок.
4. Robust Handling: безпечне зчитування з заміною некоректних символів (Safe Read).
Виступає фінальним етапом підготовки "майстер-файлу" диплома перед виданням.
"""
import os

FILES_TO_MERGE = [
    "OFFICIAL_TITLE_PAGE.md",
    "OFFICIAL_TASK_STATEMENT.md",
    "OFFICIAL_REVIEW_PROJECT.md",
    "OFFICIAL_RECENSION_PROJECT.md",
    "THESIS_0_ABSTRACT.md",
    "ABBREVIATIONS.md", # Перемістили сюди згідно п. 6.1
    "THESIS_0_INTRODUCTION.md",
    "THESIS_1_THEORY.md",
    "THESIS_2_REQUIREMENTS.md",
    "THESIS_3_DESIGN_AND_IMPLEMENTATION_EXPANDED.md",
    "THESIS_FINAL_CONCLUSIONS.md",
    "BIBLIOGRAPHY.md",
    "APPENDICES.md"
]

OUTPUT_FILE = "THESIS_FULL_FINAL_UTF8.md"
# Визначаємо корінь проєкту
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE_DIR = os.path.join(ROOT_DIR, "docs", "thesis")

def read_file_safe(filepath):
    # Використовуємо errors="replace", щоб не падати при зустрічі пошкодженого символу
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.read().strip()

def merge_files():
    print(f">>> Запуск злиття файлів у {OUTPUT_FILE} <<<")
    output_path = os.path.join(BASE_DIR, OUTPUT_FILE)
    
    with open(output_path, "w", encoding="utf-8") as outfile:
        for filename in FILES_TO_MERGE:
            filepath = os.path.join(BASE_DIR, filename)
            if os.path.exists(filepath):
                print(f" [+] Додаємо: {filename}")
                content = read_file_safe(filepath)
                # Додаємо дві пусті строки як роздільник між розділами
                outfile.write(content + "\n\n")
            else:
                print(f" [!] УВАГА: Файл {filename} не знайдено!")
                
    print(f"\n✅ Успішно злито всі частини у {output_path} (кодування приведено до єдиного UTF-8)")

if __name__ == "__main__":
    merge_files()
