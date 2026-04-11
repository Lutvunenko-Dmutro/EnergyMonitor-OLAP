import os
import re

# Explicit Mapping for maximum precision
MAPPING = {
    # 1. Main Packages
    r'from app': 'from src.app',
    r'import app': 'import src.app',
    r'from ui': 'from src.ui',
    r'import ui': 'import src.ui',
    r'from utils': 'from src.utils',
    r'import utils': 'import src.utils',
    r'from ml': 'from src.ml',
    r'import ml': 'import src.ml',
    
    # 2. Core (Merged & Reorganized)
    r'from core\.analytics\.physics': 'from src.core.physics',
    r'from core\.analytics\.aggregator': 'from src.core.analytics.aggregator',
    r'from core\.analytics\.clustering': 'from src.core.analytics.clustering',
    r'from core\.analytics\.filter': 'from src.core.analytics.filter',
    r'from core\.database\.loader': 'from src.core.database.loader',
    r'from core\.database\.archive': 'from src.core.database.archive',
    r'from core\.database': 'from src.core.database',
    r'from core': 'from src.core', # catch-all
    
    # 3. Services (Modularized)
    r'from src\.services\.sensors_db': 'from src.services.simulation.sensors_db',
    r'from src\.services\.data_generator': 'from src.services.simulation.data_generator',
    r'from src\.services\.sensors': 'from src.services.simulation.sensors',
    r'from src\.services\.generator_constants': 'from src.services.simulation.generator_constants',
    r'from src\.services\.db_seeder': 'from src.services.data.db_seeder',
    r'from src\.services\.db_services': 'from src.services.data.db_services',
    r'from src\.services\.import_real_data': 'from src.services.data.import_real_data',
    r'from src\.services\.migrate_db': 'from src.services.data.migrate_db',
    r'from src\.services\.advanced_mining': 'from src.services.analysis.advanced_mining',
    r'from src\.services\.analytics_advanced': 'from src.services.analysis.analytics_advanced',
    r'from src\.services\.trends_and_patterns': 'from src.services.analysis.trends_and_patterns',
    r'from src\.services\.diag_columns': 'from src.services.analysis.diag_columns',
    r'from src\.services\.automated_intersection_tester': 'from src.services.analysis.automated_intersection_tester',
    
    # Legacy direct services imports (without src.)
    r'from services\.sensors_db': 'from src.services.simulation.sensors_db',
    r'from services\.data_generator': 'from src.services.simulation.data_generator',
    r'from services\.sensors': 'from src.services.simulation.sensors',
    r'from services\.db_seeder': 'from src.services.data.db_seeder',
    r'from services\.db_services': 'from src.services.data.db_services',
}

def refactor():
    print("🚀 Starting Global Import Refactor...")
    count = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.venv' in root or '.pytest_cache' in root or 'site' in root:
            continue
        
        for file in files:
            if not file.endswith(('.py', '.md')): continue
            path = os.path.join(root, file)
            
            # Skip the script itself
            if 'refactor_imports.py' in path: continue
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for pattern, replacement in MAPPING.items():
                    new_content = re.sub(pattern, replacement, new_content)
                
                if new_content != content:
                    print(f"✅ Refactored: {path}")
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
            except Exception as e:
                print(f"❌ Error in {path}: {e}")
                
    print(f"🏁 Refactor complete. Total files updated: {count}")

if __name__ == "__main__":
    refactor()
