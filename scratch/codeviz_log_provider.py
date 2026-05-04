import os
import json
import time

def get_last_lines(filepath, n=50):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return lines[-n:]
    except:
        return []

if __name__ == "__main__":
    print("Starting Log Provider for Atlas...")
    log_file = r"d:\yhoba\1\Test\Py\logs\energy-monitor.log"
    error_file = r"d:\yhoba\1\Test\Py\logs\energy-monitor.error.log"
    output_js = r"d:\yhoba\1\Test\Py\docs\atlas\logs_data.js"
    
    while True:
        logs = get_last_lines(log_file)
        errors = get_last_lines(error_file)
        
        data = {
            "main": [line.strip() for line in logs],
            "errors": [line.strip() for line in errors],
            "timestamp": time.time()
        }
        
        with open(output_js, 'w', encoding='utf-8') as f:
            f.write(f"const ATLAS_LOGS = {json.dumps(data, indent=4)};")
            
        time.sleep(2)
