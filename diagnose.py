# ATLAS_PASSPORT: docs/system/map/diagnose.md
"""
СИСТЕМА ТЕХНІЧНОЇ ДІАГНОСТИКИ ПРОЄКТУ (Project Health Diagnostics)
=================================================================
Головний скрипт для автоматизованого аудиту кодової бази Energy Monitor.
Ключові можливості:
1. Automated Code Audit: сканування структури проєкту на відповідність стандартам.
2. Technical Debt Scanning: виявлення проблем та неоптимальних конструкцій.
3. HTML Report Generation: формування інтерактивного звіту diagnostics_report.html.
4. Health Score Calculation: підрахунок статистики помилок для оцінки стабільності.
Служить інструментом контролю якості (Quality Gate) перед деплоєм або захистом.
"""
from pathlib import Path
from src.core.diagnostics.scanner import ProjectScanner
from src.core.diagnostics.reporter import HtmlReporter

def main():
    ROOT = Path(__file__).parent
    REPORT_DIR = ROOT / "results" / "reports"
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH = REPORT_DIR / "diagnostics_report.html"

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
