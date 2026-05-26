"""
АВТОМАТИЗОВАНИЙ АРХІТЕКТОР ДОКУМЕНТАЦІЇ (Project Atlas Metadata Generator)
========================================================================
Модуль реалізує логіку інтелектуального сканування структури проєкту для побудови Атласу.
Ключові можливості:
1. Project Tree Crawler: рекурсивний обхід директорій з ігноруванням службових папок.
2. Semantic Extraction: використання AST-дерев для вилучення та очищення топових докстрінгів.
3. Graph Topology: автоматичне виявлення логічних зв'язків (імпортів) між модулями.
4. Knowledge Serialization: формування бази знань у форматі JSON для інтерактивного візуалізатора.
Є ключовим інструментом для підтримки технічної документації в актуальному стані.
"""
import os
import json
import ast
import re

def extract_docstring(file_path):
    """Extracts the top-level docstring from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
            doc = ast.get_docstring(tree)
            if doc:
                # Take first 1-2 sentences and clean up newlines and markdown underlines
                sentences = doc.strip().split("\n")
                description = "\n".join([s.strip() for s in sentences if s.strip()])
                # Прибираємо декоративні лінії === та ---
                description = re.sub(r'[\=\-]{3,}', '', description)
                # Замінюємо пробіл перед дужкою на нерозривний пробіл (\u00A0)
                # Та додаємо Word Joiner (\u2060) після дужки, щоб вона "приклеїлася" до слова
                description = description.replace(" (", "\u00A0(\u2060")
                return description.replace("\r", "").strip()
    except Exception:
        pass
    return "Технічний модуль системи."

def generate_metadata():
    base_dir = r"d:\yhoba\1\Test\Py"
    # Повний список сміття, яке ми ігноруємо
    exclude_dirs = {
        "site", "__pycache__", ".gemini", "docs", ".git", "venv", ".venv", 
        "env", ".github", ".pytest_cache", ".streamlit", "cache", "logs", 
        "results", "scratch", "sql", "junit", "target", "build"
    }
    
    nodes = []
    edges = []
    created_folders = set()
    
    # Спершу додаємо кореневу папку проєкту
    nodes.append({
        "id": "folder_root",
        "type": "folder",
        "name": "Project (Py)",
        "path": ".",
        "parent_id": None,
        "short_description": "Головна директорія проєкту Energy Monitor Ultimate.",
        "detail_link": "/"
    })
    created_folders.add(".")

    for root, dirs, files in os.walk(base_dir):
        # Фільтруємо папки, які не хочемо бачити
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        rel_root = os.path.relpath(root, base_dir).replace("\\", "/")
        if rel_root == ".":
            folder_id = "folder_root"
        else:
            folder_id = f"folder_{rel_root.replace('/', '_')}"

        # Реєструємо нові папки
        if rel_root != "." and rel_root not in created_folders:
            parent_path = os.path.dirname(rel_root).replace("\\", "/")
            if parent_path == "" or parent_path == ".":
                parent_id = "folder_root"
            else:
                parent_id = f"folder_{parent_path.replace('/', '_')}"
            
            nodes.append({
                "id": folder_id,
                "type": "folder",
                "name": os.path.basename(rel_root),
                "path": rel_root,
                "parent_id": parent_id,
                "short_description": f"Контейнер для модулів у директорії {rel_root}.",
                "detail_link": "/system/map/data_fallback/" if rel_root == "data/fallback" else f"/{rel_root}/"
            })
            created_folders.add(rel_root)

        # Реєструємо файли
        for file in files:
            # Skip scanning individual cache files in data/fallback
            if "data/fallback" in rel_root or "data\\fallback" in rel_root or file.endswith(".parquet"):
                continue
            if file.endswith(".py") or file.endswith(".csv") or file.endswith(".db") or file.endswith(".parquet"):
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, base_dir).replace("\\", "/")
                file_id = f"file_{rel_file_path.replace('/', '_').replace('.', '_')}"
                
                if file.endswith(".py"):
                    description = extract_docstring(file_path)
                elif file.endswith(".csv"):
                    description = f"Файл набору даних (Dataset CSV): {file}. Локальні історичні показники енергоспоживання."
                elif file.endswith(".db"):
                    description = f"Локальна база даних SQLite: {file}. Зберігає кешовані обчислення."
                elif file.endswith(".parquet"):
                    description = f"Кешований запит Parquet: {file}. Містить оптимізовані колонки результатів."
                
                # Перевірка наявності паспорта
                detail_link = None
                if not file.endswith(".py"):
                    # Generate unique clean name for individual passport
                    clean_name = rel_file_path.replace("/", "_").replace(".", "_")
                    detail_link = f"/system/map/{clean_name}/"
                passport_path = None
                
                # Пріоритет 1: Пошук тега # ATLAS_PASSPORT у файлі
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        passport_match = re.search(r'#\s*ATLAS_PASSPORT:\s*([\w/\.\-]+)', file_content)
                        if passport_match:
                            raw_passport_path = passport_match.group(1).strip()
                            # Очищаємо шлях (прибираємо docs/ та .md для лінку)
                            clean_path = raw_passport_path.replace('docs/', '').replace('.md', '')
                            # Видаляємо початковий слеш якщо є
                            clean_path = clean_path.lstrip('/')
                            detail_link = f"/{clean_path}/"
                            print(f"🔗 Знайдено зв'язок: {file} -> {detail_link}")
                except:
                    pass

                # Пріоритет 2: Автоматичний пошук за іменем (якщо лінк ще не знайдено)
                if not detail_link:
                    passport_name = os.path.basename(file).replace('.py', '')
                    passport_path_check = os.path.join(base_dir, "docs", "system", "map", f"{passport_name}.md")
                    if os.path.exists(passport_path_check):
                        detail_link = f"/system/map/{passport_name}/"
                
                nodes.append({
                    "id": file_id,
                    "type": "file",
                    "name": file,
                    "path": rel_file_path,
                    "parent_id": folder_id,
                    "short_description": description,
                    "detail_link": detail_link
                })
                
                # Пошук імпортів
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Пошук локальних імпортів (src, scripts, tests)
                        found_imports = re.findall(r'(?:from|import)\s+(src|scripts|tests)\.([\w\.]+)', content)
                        
                        for base, imp in set(found_imports):
                            target_id = f"file_{base}_{imp.replace('.', '_')}_py"
                            edges.append({
                                "source": file_id,
                                "target": target_id,
                                "type": "import"
                            })
                except:
                    pass

    # Save to JSON
    output_data = {"nodes": nodes, "edges": edges}
    
    output_path = os.path.join(base_dir, "docs", "javascripts", "atlas_data.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=True, indent=2)
    
    print(f"Generated metadata for {len(nodes)} nodes and {len(edges)} edges.")

    # Update the external JS data file
    atlas_js_path = os.path.join(base_dir, "docs/system/atlas_data.js")
    try:
        new_data_str = f"const ATLAS_DATA = {json.dumps(output_data, ensure_ascii=True, indent=2)};"
        os.makedirs(os.path.dirname(atlas_js_path), exist_ok=True)
        with open(atlas_js_path, "w", encoding="utf-8") as f:
            f.write(new_data_str)
        print(f"Successfully updated external data in {atlas_js_path}")
    except Exception as e:
        print(f"Error updating external data: {e}")

if __name__ == "__main__":
    generate_metadata()
