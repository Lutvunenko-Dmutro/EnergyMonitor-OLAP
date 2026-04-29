#!/usr/bin/env python3
"""
ENERGY MONITOR: POWER DIAGNOSTICS v2.0 (MODULAR)
Головний скрипт для запуску повного аудиту проекту.
"""
from pathlib import Path
from src.core.diagnostics.scanner import ProjectScanner
from src.core.diagnostics.reporter import HtmlReporter

def main():
    ROOT = Path(__file__).parent
    REPORT_PATH = ROOT / "diagnostics_report.html"

    print("\n" + "═" * 50)
    print("   ⚡ ENERGY MONITOR — DIAGNOSTICS SYSTEM")
    print("═" * 50)

    # 1. Запуск сканування
    scanner = ProjectScanner(ROOT)
    scanner.scan_all()

    # 2. Генерація звіту
    reporter = HtmlReporter()
    reporter.generate(scanner.results, REPORT_PATH)

    # 3. Висновок
    total = len(scanner.results)
    err = sum(1 for r in scanner.results if r.status == "ERROR")
    
    print("\n" + "─" * 50)
    print(f"   📊 Файлів оброблено: {total}")
    print(f"   ❌ Помилок знайдено: {err}")
    print(f"   📄 Звіт збережено:  {REPORT_PATH}")
    print("─" * 50 + "\n")

if __name__ == "__main__":
    main()
