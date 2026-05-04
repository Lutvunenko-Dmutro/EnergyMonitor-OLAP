"""
GENERATE ATLAS METADATA (Documentation Orchestrator)
===================================================
Цей скрипт автоматично сканує директорію паспортів та генерує JSON-метадані
для забезпечення цілісності навігації в системі ProperDocs.
"""
import os
import json
import datetime

DOCS_PATH = "docs/system/map"
OUTPUT_FILE = "docs/system/map/atlas_metadata.json"

def generate_metadata():
    print(f"🔍 Сканування паспортів у {DOCS_PATH}...")
    passports = []
    
    if not os.path.exists(DOCS_PATH):
        print(f"❌ Помилка: Директорія {DOCS_PATH} не знайдена.")
        return

    for file in os.listdir(DOCS_PATH):
        if file.endswith(".md") and file != "ATLAS_MASTER_INDEX.md":
            passports.append({
                "name": file,
                "path": f"system/map/{file}",
                "updated_at": datetime.datetime.now().isoformat()
            })
    
    metadata = {
        "project": "Project ATLAS",
        "total_passports": len(passports) + 1,
        "last_sync": datetime.datetime.now().isoformat(),
        "passports": passports
    }
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Метадані успішно збережені у {OUTPUT_FILE}")
    print(f"📊 Всього зафіксовано паспортів: {len(passports) + 1}")

if __name__ == "__main__":
    generate_metadata()
