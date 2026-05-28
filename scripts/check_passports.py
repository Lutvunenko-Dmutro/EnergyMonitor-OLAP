import os
import re
from collections import defaultdict
from pathlib import Path

def check_passports(src_dir):
    passport_map = defaultdict(list)
    tag_pattern = re.compile(r'#\s*ATLAS_PASSPORT:\s*([\w/\.\-]+)')
    
    src_path = Path(src_dir)
    for py_file in src_path.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                match = tag_pattern.search(content)
                if match:
                    md_file = match.group(1).strip()
                    md_filename = os.path.basename(md_file)
                    # Get relative path for clean output
                    rel_py = py_file.relative_to(src_path.parent)
                    passport_map[md_filename].append(str(rel_py))
        except Exception as e:
            pass

    print("=== ДУБЛІКАТИ ПАСПОРТІВ (Один .md файл на декілька .py файлів) ===\n")
    print(f"{'MD ПАСПОРТ':<30} | {'PYTHON ФАЙЛИ'}")
    print("-" * 100)
    
    total_duplicates = 0
    for md_file, py_files in sorted(passport_map.items()):
        if len(py_files) > 1:
            total_duplicates += 1
            files_str = ", ".join(py_files)
            print(f"{md_file:<30} | {files_str}")
            
    print("-" * 100)
    print(f"Знайдено проблемних паспортів (де >1 посилання): {total_duplicates}")

if __name__ == "__main__":
    check_passports(r"d:\yhoba\1\Test\Py\src")
