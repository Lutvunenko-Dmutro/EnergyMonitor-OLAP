import os

# ПЕРЕЛІК ФАЙЛІВ ДЛЯ ЗБІРКИ (В порядку п. 6.1 методики)
FILES_TO_MERGE = [
    "OFFICIAL_TITLE_PAGE.md",
    "OFFICIAL_TASK_STATEMENT.md",
    "THESIS_0_ABSTRACT.md",
    "ABBREVIATIONS.md",
    "THESIS_0_INTRODUCTION.md",
    "THESIS_1_THEORY.md",
    "THESIS_2_REQUIREMENTS.md",
    "THESIS_3_DESIGN_AND_IMPLEMENTATION.md",
    "THESIS_FINAL_CONCLUSIONS.md",
    "BIBLIOGRAPHY.md",
    "THESIS_APPENDICES.md"
]

def merge_thesis():
    output_file = "docs/thesis/THESIS_FULL_FINAL_UTF8.md"
    base_dir = "docs/thesis"
    
    print(f"\n>>> Запуск злиття файлів у {os.path.basename(output_file)} <<<")
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        for i, filename in enumerate(FILES_TO_MERGE):
            file_path = os.path.join(base_dir, filename)
            
            if not os.path.exists(file_path):
                print(f" [!] Файл не знайдено: {filename}")
                continue
                
            print(f" [+] Додаємо: {filename}")
            
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                
                # Додаємо розрив сторінки перед кожним новим файлом (крім першого)
                if i > 0:
                    outfile.write("\n<pagebreak>\n")
                
                outfile.write(content)
                outfile.write("\n\n")

    print(f"\n✅ Успішно злито всі частини у {output_file}")

def main():
    merge_thesis()

if __name__ == "__main__":
    main()
