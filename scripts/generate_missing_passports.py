import os
import ast
import re
from pathlib import Path

def extract_docstring(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
            doc = ast.get_docstring(tree)
            if doc:
                lines = doc.strip().split('\n')
                # Try to get the first sentence or two
                first_lines = [line.strip() for line in lines[:2] if line.strip()]
                desc = " ".join(first_lines)
                desc = re.sub(r'[\=\-]{3,}', '', desc).strip()
                if desc:
                    return desc
    except Exception:
        pass
    return "Технічний модуль або ініціалізаційний пакет системи."

TEMPLATE = """# Технічна специфікація: {title} (GIGA-PASSPORT v3)

<div class="mega-passport">

<!-- HERO SECTION -->
<div class="hero-section">
    <div class="hero-badge">📦 COMPONENT REGISTRY</div>
    <div class="hero-main">
        <div class="hero-icon-wrapper"><span class="hero-icon">⚙️</span><div class="pulse-ring"></div></div>
        <div class="hero-title-group">
            <h1 class="mega-title">{py_filename}</h1>
            <p class="mega-subtitle">{docstring}</p>
            <div class="status-tags">
                <span class="tag tag-online">ACTIVE</span>
                <span class="tag tag-version">v3.0.0</span>
            </div>
        </div>
    </div>
</div>

<!-- FOOTER NAV -->
<div class="passport-footer">
    <a href="../../atlas_final/" class="mega-btn"><span class="btn-icon">🔙</span><span class="btn-text">ПОВЕРНУТИСЬ ДО АТЛАСУ</span></a>
</div>

</div>
"""

def generate_missing():
    broken = [
        (r"src\__init__.py", "root_init.md"),
        (r"src\app\__init__.py", "app_init.md"),
        (r"src\app\config.py", "app_config.md"),
        (r"src\core\__init__.py", "core_init.md"),
        (r"src\core\config.py", "core_config.md"),
        (r"src\core\database\__init__.py", "database_init.md"),
        (r"src\services\__init__.py", "services_init.md"),
        (r"src\ui\__init__.py", "ui_init.md"),
        (r"src\ui\components\__init__.py", "ui_components_init.md"),
        (r"src\utils\__init__.py", "utils_init.md")
    ]
    
    base_dir = Path(r"d:\yhoba\1\Test\Py")
    docs_dir = base_dir / "docs" / "system" / "map"
    
    generated = 0
    for py_rel, md_name in broken:
        py_path = base_dir / py_rel
        md_path = docs_dir / md_name
        
        if not md_path.exists():
            docstring = extract_docstring(py_path)
            title = Path(py_rel).name
            if title == "__init__.py":
                title = f"{Path(py_rel).parent.name} (Package Init)"
                
            content = TEMPLATE.format(
                title=title,
                py_filename=Path(py_rel).name,
                docstring=docstring
            )
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Згенеровано: {md_name}")
            generated += 1
            
    print(f"\nУспішно створено {generated} паспортів!")

if __name__ == "__main__":
    generate_missing()
