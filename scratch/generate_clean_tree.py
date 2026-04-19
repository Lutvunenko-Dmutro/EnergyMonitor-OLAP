import os

def generate_tree(startpath, exclude_dirs=['__pycache__', '.git', '.venv', '.gemini', 'tests/__pycache__', 'logs', 'site', 'junit', '.pytest_cache', '.github', 'fallback'], 
                  exclude_files=['.pyc', '.log', '.tmp', '.bak', '.parquet', '.graphml', '.csv', '.html', '.coverage']):
    tree = []
    for root, dirs, files in os.walk(startpath):
        # Фільтруємо папки
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        tree.append(f'{indent}{os.path.basename(root)}/')
        
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            if not any(f.endswith(ext) for ext in exclude_files):
                tree.append(f'{sub_indent}{f}')
    return "\n".join(tree)

if __name__ == "__main__":
    project_root = r"d:\yhoba\1\Test\Py"
    clean_tree = generate_tree(project_root)
    with open(os.path.join(project_root, "docs", "CLEAN_PROJECT_TREE.txt"), "w", encoding="utf-8") as f:
        f.write(clean_tree)
    print("Clean tree generated successfully.")
