import os
import re
import json
from pathlib import Path
from datetime import datetime

# --- CONFIGURATION: HUB MAPPING ---
HUB_CONSOLIDATION_MAP = {
    "predict_v2.md": "ml_core_engine.md",
    "train_lstm.md": "ml_core_engine.md",
    "train_v1.md": "ml_core_engine.md",
    "vectorizer.md": "ml_core_engine.md",
    "ml_backtest_framework.md": "ml_core_engine.md",
    "ml_visual_utils.md": "ml_core_engine.md",
    "model_loader.md": "ml_core_engine.md",
    "core_config.md": "core_kernel_hub.md",
    "core_kaggle_loader.md": "core_kernel_hub.md",
    "queries.md": "core_kernel_hub.md",
    "kaggle_loader.md": "core_kernel_hub.md",
    "cache_management_engine.md": "core_kernel_hub.md",
    "unified_logging_registry.md": "core_kernel_hub.md",
    "error_resilience_system.md": "core_kernel_hub.md",
    "system_root_package.md": "core_kernel_hub.md",
    "patterns.md": "diagnostics_engine_hub.md",
    "services_data_seeder.md": "data_services_hub.md",
    "sql_schema_passport.md": "data_services_hub.md",
    "db_services.md": "data_services_hub.md",
    "import_real_data.md": "data_services_hub.md",
    "migrate_db.md": "data_services_hub.md",
    "services_package.md": "data_services_hub.md",
    "utils_package.md": "utils_extended_toolkit.md",
    "ui_package_root.md": "ui_components_hub.md",
}

TAG_PATTERN = re.compile(r"# ATLAS_PASSPORT: docs/system/map/(.+?\.md)")

class AtlasSteward:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir)
        self.src_dir = self.root / "src"
        self.docs_dir = self.root / "docs" / "system" / "map"

    def run_cleanup(self):
        print("🛡️ Starting ATLAS Documentation Steward...")
        stats = {"fixed": 0, "duplicates_removed": 0, "total_files": 0}
        
        for py_file in self.src_dir.rglob("*.py"):
            stats["total_files"] += 1
            self._process_file(py_file, stats)
            
        print(f"\n✅ Audit Complete!")
        print(f"📊 Fixed: {stats['fixed']} | Duplicates: {stats['duplicates_removed']} | Scanned: {stats['total_files']}")
        
        self.regenerate_metadata()

    def regenerate_metadata(self):
        metadata_path = self.docs_dir / "atlas_metadata.json"
        md_files = sorted([f.name for f in self.docs_dir.glob("*.md")])
        
        metadata = {
            "project": "Project ATLAS",
            "total_passports": len(md_files),
            "last_sync": datetime.now().isoformat(),
            "passports": [
                {
                    "name": name,
                    "path": f"system/map/{name}",
                    "updated_at": datetime.now().isoformat()
                } for name in md_files
            ]
        }
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        print(f"✨ Updated {metadata_path} with {len(md_files)} entries.")

    def _process_file(self, file_path: Path, stats: dict):
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        new_lines = []
        found_tags = []
        modified = False

        for line in lines:
            match = TAG_PATTERN.search(line)
            if match:
                passport_name = match.group(1)
                if passport_name in HUB_CONSOLIDATION_MAP:
                    new_passport = HUB_CONSOLIDATION_MAP[passport_name]
                    line = line.replace(passport_name, new_passport)
                    passport_name = new_passport
                    modified = True
                    stats["fixed"] += 1

                if passport_name in found_tags:
                    modified = True
                    stats["duplicates_removed"] += 1
                    continue
                found_tags.append(passport_name)
            new_lines.append(line)

        if modified:
            file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    steward = AtlasSteward()
    steward.run_cleanup()
