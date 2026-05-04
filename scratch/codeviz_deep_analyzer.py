import os
import ast
import json
from pathlib import Path

class CallVisitor(ast.NodeVisitor):
    def __init__(self, mod_name, function_map, current_file_imports, file_path):
        self.mod_name = mod_name
        self.function_map = function_map
        self.current_file_imports = current_file_imports
        self.file_path = file_path
        self.current_function = None
        self.edges = []

    def visit_FunctionDef(self, node):
        old_func = self.current_function
        self.current_function = f"{self.mod_name}.{node.name}"
        self.generic_visit(node)
        self.current_function = old_func

    def visit_Call(self, node):
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        
        if func_name in self.function_map:
            potential_mods = self.function_map[func_name]
            for target_mod in potential_mods:
                if any(target_mod.startswith(imp) for imp in self.current_file_imports.values()) or target_mod == self.mod_name:
                    target_id = f"{target_mod}.{func_name}"
                    source_id = self.current_function or self.file_path
                    self.edges.append({
                        "source": source_id,
                        "target": target_id,
                        "type": "call"
                    })
        self.generic_visit(node)

class CallGraphAnalyzer:
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.function_map = {}
        self.nodes = []
        self.edges = []
        self.module_to_file = {}

    def get_module_name(self, file_path):
        rel = file_path.relative_to(self.root)
        return str(rel).replace(os.sep, '.').replace('.__init__.py', '').replace('.py', '')

    def catalog_functions(self):
        print("Cataloging functions...")
        for f in self.root.glob("**/*.py"):
            if any(x in str(f) for x in ["venv", ".gemini", "__pycache__"]): continue
            try:
                with open(f, 'r', encoding='utf-8') as src:
                    src_text = src.read()
                    tree = ast.parse(src_text)
                    mod_name = self.get_module_name(f)
                    self.module_to_file[mod_name] = str(f.relative_to(self.root).as_posix())
                    lines = src_text.splitlines()
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            full_name = f"{mod_name}.{node.name}"
                            if node.name not in self.function_map:
                                self.function_map[node.name] = []
                            self.function_map[node.name].append(mod_name)
                            
                            try:
                                func_lines = lines[node.lineno-1 : node.end_lineno]
                                func_code = "\n".join(func_lines)
                            except: func_code = "Source not available"

                            self.nodes.append({
                                "id": full_name,
                                "label": node.name,
                                "parent": self.module_to_file[mod_name],
                                "type": "function",
                                "code": func_code,
                                "docstring": ast.get_docstring(node) or ""
                            })
            except Exception as e: print(f"Error parsing {f}: {e}")

    def analyze_calls(self):
        print("Analyzing calls...")
        for f in self.root.glob("**/*.py"):
            if any(x in str(f) for x in ["venv", ".gemini", "__pycache__"]): continue
            try:
                with open(f, 'r', encoding='utf-8') as src:
                    tree = ast.parse(src.read())
                    mod_name = self.get_module_name(f)
                    
                    imports = {}
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for n in node.names: imports[n.asname or n.name] = n.name
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                for n in node.names: imports[n.asname or n.name] = node.module

                    visitor = CallVisitor(mod_name, self.function_map, imports, self.module_to_file[mod_name])
                    visitor.visit(tree)
                    self.edges.extend(visitor.edges)
            except: continue

    def _get_domain(self, file_path):
        if "src/ml" in file_path: return "ml"
        if "src/ui" in file_path: return "ui"
        if "src/core" in file_path: return "core"
        if "tests" in file_path: return "tests"
        if "scripts" in file_path: return "scripts"
        return "other"

    def run(self):
        self.catalog_functions()
        
        # Додаємо домени як головні папки (контейнери)
        domains = set()
        for mod, file_path in self.module_to_file.items():
            domains.add(self._get_domain(file_path))
            
        for d in domains:
            self.nodes.append({
                "id": f"folder_{d}",
                "label": d.toUpperCase() if hasattr(d, 'toUpperCase') else d.upper(),
                "type": "folder",
                "is_parent": True
            })
        
        # Додаємо файли як контейнери (картки)
        added_files = set()
        for mod, file_path in self.module_to_file.items():
            if file_path not in added_files:
                parts = file_path.split('/')
                display_label = "/".join(parts[-2:]) if len(parts) > 1 else parts[-1]
                
                domain = self._get_domain(file_path)
                self.nodes.append({
                    "id": file_path,
                    "label": display_label,
                    "type": "file",
                    "domain": domain,
                    "parent": f"folder_{domain}",
                    "is_parent": True
                })
                added_files.add(file_path)
            
        self.analyze_calls()
        
        # Додаємо домени функціям
        for node in self.nodes:
            if node["type"] == "function":
                node["domain"] = self._get_domain(node["parent"])
        
        return {"nodes": self.nodes, "edges": self.edges}

if __name__ == "__main__":
    analyzer = CallGraphAnalyzer(r"d:\yhoba\1\Test\Py")
    result = analyzer.run()
    output_js = r"d:\yhoba\1\Test\Py\docs\atlas\data.js"
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write("// DEEP CODEVIZ DATA\n")
        f.write(f"const CODE_GRAPH = {json.dumps(result, indent=4)};\n")
        f.write("const PROJECT_HIERARCHY = {};\nconst TOUR_STEPS = [];\nconst BRANCH_STYLING = {};\nconst NODE_DESCRIPTIONS = {};\n")
    print(f"Deep analysis done. Found {len(result['nodes'])} entities and {len(result['edges'])} calls.")
