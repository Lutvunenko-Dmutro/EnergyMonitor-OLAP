import os
import re
from pathlib import Path

def check_broken_passports(src_dir, docs_dir):
    tag_pattern = re.compile(r'#\s*ATLAS_PASSPORT:\s*([\w/\.\-]+)')
    src_path = Path(src_dir)
    docs_path = Path(docs_dir)
    
    broken_links = []
    
    for py_file in src_path.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                match = tag_pattern.search(content)
                if match:
                    # e.g., docs/system/map/app_config.md
                    md_path_str = match.group(1).strip()
                    
                    # Resolve to absolute path based on project root (assuming standard structure)
                    # For this, let's just grab the filename and check in docs/system/map/
                    md_filename = os.path.basename(md_path_str)
                    target_md_file = docs_path / md_filename
                    
                    if not target_md_file.exists():
                        rel_py = py_file.relative_to(src_path.parent)
                        broken_links.append((str(rel_py), md_filename))
        except Exception as e:
            pass

    print("=== БИТІ ПОСИЛАННЯ (Файл .py вказує на неіснуючий .md паспорт) ===\n")
    if not broken_links:
        print("✅ Усі паспорти існують!")
    else:
        print(f"{'PYTHON ФАЙЛ':<50} | {'ВІДСУТНІЙ ПАСПОРТ (.md)'}")
        print("-" * 90)
        for py_file, md_file in sorted(broken_links):
            print(f"{py_file:<50} | {md_file}")
        print("-" * 90)
        print(f"Знайдено битих посилань: {len(broken_links)}")

if __name__ == "__main__":
    check_broken_passports(
        src_dir=r"d:\yhoba\1\Test\Py\src", 
        docs_dir=r"d:\yhoba\1\Test\Py\docs\system\map"
    )
