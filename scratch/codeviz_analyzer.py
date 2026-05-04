import os
import ast
import json
from pathlib import Path

def get_imports(file_path, project_root):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
        except:
            return []
            
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    
    # Фільтруємо лише внутрішні імпорти проекту
    # Наприклад, якщо проект у папці 'src', шукаємо імпорти 'src.core' тощо
    # Але також враховуємо відносні шляхи
    return list(set(imports))

def analyze_project(root_path):
    root = Path(root_path)
    nodes = []
    edges = []
    
    all_py_files = list(root.glob("**/*.py"))
    
    # Створюємо словник для швидкого пошуку
    module_to_file = {}
    for f in all_py_files:
        rel_path = f.relative_to(root).as_posix()
        module_name = rel_path.replace('/', '.').replace('.__init__.py', '').replace('.py', '')
        module_to_file[module_name] = rel_path
        
        nodes.append({
            "id": rel_path,
            "label": f.name,
            "module": module_name,
            "type": "module"
        })

    for f in all_py_files:
        rel_path = f.relative_to(root).as_posix()
        imports = get_imports(f, root)
        
        for imp in imports:
            # Перевіряємо, чи цей імпорт є частиною нашого проекту
            for mod_name, mod_file in module_to_file.items():
                if imp == mod_name or imp.startswith(mod_name + '.'):
                    edges.append({
                        "source": str(rel_path),
                        "target": mod_file,
                        "type": "import"
                    })
                    break
                    
    return {"nodes": nodes, "edges": edges}

if __name__ == "__main__":
    project_root = r"d:\yhoba\1\Test\Py"
    print(f"Analyzing dependencies in {project_root}...")
    data = analyze_project(project_root)
    
    # Оновлюємо data.js з новими даними у стилі CodeViz
    output_js = os.path.join(project_root, "docs", "atlas", "data.js")
    os.makedirs(os.path.dirname(output_js), exist_ok=True)
    
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write("// CODEVIZ DATA\n")
        f.write(f"const CODE_GRAPH = {json.dumps(data, indent=4)};\n")
        
        # Додамо також ієрархію для дерева, якщо захочемо залишити провідник
        # (яку ми зробили раніше)
        f.write("\nconst PROJECT_HIERARCHY = {}; // Буде заповнено за потреби\n")
        f.write("const TOUR_STEPS = [];\n")
        f.write("const BRANCH_STYLING = {};\n")
        f.write("const NODE_DESCRIPTIONS = {};\n")
        
    print(f"Analysis complete. Found {len(data['nodes'])} modules and {len(data['edges'])} connections.")
