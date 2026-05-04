import os
import re

def get_city_data():
    base_dir = "d:/yhoba/1/Test/Py"
    city_data = {
        "name": "EnergyMonitor-OLAP CyberCity",
        "districts": {},
        "links": [] # Here we will store interactions
    }

    colors = {
        "core": "#fb923c",
        "ml": "#c084fc",
        "ui": "#4ade80",
        "services": "#38bdf8",
        "scripts": "#f472b6",
        "tests": "#94a3b8",
        "other": "#64748b"
    }

    file_to_id = {}

    # 1. First pass: map all files
    for root, dirs, files in os.walk(base_dir):
        if any(x in root for x in ["site", ".git", "__pycache__", "site-packages"]): continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, base_dir).replace("\\", "/")
                file_id = file.replace(".py", "")
                file_to_id[file_id] = rel_path
                
                parts = rel_path.split("/")
                district_name = "other"
                if len(parts) > 1:
                    district_name = parts[1] if parts[0] == "src" and len(parts) > 2 else parts[0]
                
                if district_name not in city_data["districts"]:
                    city_data["districts"][district_name] = {"color": colors.get(district_name, "#64748b"), "buildings": []}
                
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        loc = len(content.splitlines())
                except:
                    content = ""
                    loc = 10
                
                city_data["districts"][district_name]["buildings"].append({
                    "id": rel_path,
                    "name": file,
                    "height": loc,
                    "complexity": os.path.getsize(path) / 1024
                })

                # 2. Extract imports for links
                # Look for 'from ... import ...' or 'import ...'
                imports = re.findall(r"(?:from|import)\s+([\w\.]+)", content)
                for imp in imports:
                    imp_base = imp.split(".")[-1]
                    if imp_base in file_to_id and file_id != imp_base:
                        # We found a dependency!
                        city_data["links"].append({
                            "source": rel_path,
                            "target": imp_base # We will resolve this in JS or here
                        })

    # Resolve links target to full paths
    final_links = []
    for link in city_data["links"]:
        for fid, fpath in file_to_id.items():
            if fid == link["target"]:
                final_links.append({"source": link["source"], "target": fpath})
                break
    city_data["links"] = final_links

    import json
    with open("d:/yhoba/1/Test/Py/docs/javascripts/city_data.js", "w", encoding="utf-8") as f:
        f.write("const CITY_DATA = " + json.dumps(city_data, indent=2) + ";")

get_city_data()
print("CyberCity Data with Links Generated!")
