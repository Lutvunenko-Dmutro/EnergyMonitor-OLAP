import os
import glob
from pathlib import Path

def get_used_passports():
    used = set()
    src_dir = Path(r"d:\yhoba\1\Test\Py\src")
    scripts_dir = Path(r"d:\yhoba\1\Test\Py\scripts")
    
    # Check all python files
    for root_dir in [src_dir, scripts_dir]:
        for py_file in root_dir.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if "ATLAS_PASSPORT:" in line:
                            parts = line.split("ATLAS_PASSPORT:")
                            if len(parts) > 1:
                                passport_path = parts[1].strip()
                                # Some paths might be relative like docs/system/map/file.md
                                basename = os.path.basename(passport_path)
                                used.add(basename)
                            break
            except Exception:
                pass
    return used

def main():
    used_passports = get_used_passports()
    docs_dir = Path(r"d:\yhoba\1\Test\Py\docs\system\map")
    
    all_md_files = set()
    for md_file in docs_dir.glob("*.md"):
        all_md_files.add(md_file.name)
        
    orphaned = all_md_files - used_passports
    # Ignore master index
    if "ATLAS_MASTER_INDEX.md" in orphaned:
        orphaned.remove("ATLAS_MASTER_INDEX.md")
    
    print(f"Total MD files: {len(all_md_files)}")
    print(f"Used MD files: {len(used_passports)}")
    print(f"Orphaned MD files ({len(orphaned)}):")
    for o in sorted(orphaned):
        print(f" - {o}")

if __name__ == "__main__":
    main()
