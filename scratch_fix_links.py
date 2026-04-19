import os
import re
from pathlib import Path

MAPPING = {
    "DIPLOMA_PLAN.md": "thesis/DIPLOMA_PLAN.md",
    "kanban_thesis.md": "thesis/KANBAN_THESIS.md",
    "USER_MANUAL.md": "guides/USER_MANUAL.md",
    "MAINTENANCE.md": "guides/MAINTENANCE.md",
    "testing.md": "guides/TESTING_GUIDE.md",
    "SECURITY.md": "guides/SECURITY.md",
    "architecture.md": "system/architecture.md",
    "database.md": "system/database.md",
    "digital_twin.md": "system/digital_twin.md",
}
# Lowercase mapping for robust lookups
LOWER_MAPPING = {k.lower(): v for k, v in MAPPING.items()}

def resolve_new_link(current_file_path, link_target):
    if link_target.startswith("http"):
        return link_target

    target_clean = link_target.split('#')[0]
    anchor = link_target[len(target_clean):]
    filename_lower = os.path.basename(target_clean).lower()
    
    if filename_lower not in LOWER_MAPPING:
        return link_target
        
    docs_dir = Path("docs").resolve()
    new_abs_target = docs_dir / LOWER_MAPPING[filename_lower]
    current_dir = Path(current_file_path).resolve().parent
    
    try:
        new_relative = os.path.relpath(new_abs_target, current_dir).replace('\\', '/')
        return new_relative + anchor
    except ValueError:
        return link_target

def fix_links_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    def replacer(match):
        text = match.group(1)
        link = match.group(2)
        new_link = resolve_new_link(filepath, link)
        return f"[{text}]({new_link})"

    new_content = re.sub(pattern, replacer, content)

    # Simple text replacements
    for key, val in MAPPING.items():
        base = f"docs/{key}"
        new_content = re.sub(re.escape(base), f"docs/{val}", new_content, flags=re.IGNORECASE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    for dname, dirs, files in os.walk("."):
        if '.git' in dname or '.pytest_cache' in dname:
            continue
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(dname, f)
                try:
                    fix_links_in_file(filepath)
                except Exception as e:
                    pass

if __name__ == '__main__':
    main()
