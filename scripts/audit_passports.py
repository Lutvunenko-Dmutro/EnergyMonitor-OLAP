"""
ATLAS Passport Quality Auditor
================================
Сканує всі паспортні .md файли в docs/system/map/,
знаходить відповідні Python-файли через тег ATLAS_PASSPORT,
оцінює якість документації і виводить пріоритизований план виправлень.

Запуск: python scripts/audit_passports.py
        python scripts/audit_passports.py --output docs/system/map/AUDIT_REPORT.md
        python scripts/audit_passports.py --fix-threshold 50  (показати тільки файли з оцінкою < 50)
"""

import ast
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────
# КОНФІГУРАЦІЯ
# ─────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent          # d:\yhoba\1\Test\Py
PASSPORT_DIR = ROOT / "docs" / "system" / "map"
SRC_ROOT = ROOT / "src"

# Штампи "шаблонного" тексту — їх наявність знижує оцінку
GENERIC_PATTERNS = {
    "generic_subtitle": (
        "Технічний скрипт автоматизації процесів збирання, аналізу або конвертації",
        -20, "Загальний subtitle-шаблон — не описує реальне призначення"
    ),
    "generic_badge": (
        "AUTOMATION ENGINE &amp; UTILITY NODE",
        -10, "Незмінений hero-badge від шаблону"
    ),
    "generic_badge_raw": (
        "AUTOMATION ENGINE & UTILITY NODE",
        -10, "Незмінений hero-badge від шаблону"
    ),
    "generic_diagram": (
        'RUN("Основний алгоритм")',
        -20, "Діаграма містить шаблонний вузол 'Основний алгоритм'"
    ),
    "generic_api_desc": (
        "Виконує обчислювальну операцію системи",
        -15, "API-опис не описує реальну поведінку функції"
    ),
    "hardcoded_v5": (
        "v5.0.0",
        -10, "Захардкоджена версія v5.0.0 зі шаблону"
    ),
    "defense_edition": (
        "DEFENSE EDITION",
        -5, "Незмінений status tag 'DEFENSE EDITION' від шаблону"
    ),
    "generic_config_node": (
        'CONFIG("Ініціалізація оточення")',
        -10, "Діаграма: загальний вузол CONFIG без деталей"
    ),
    "generic_comp_node": (
        'COMP("Завершення завдання")',
        -10, "Діаграма: загальний вузол COMP без деталей"
    ),
    "high_performance": (
        "High Performance",
        -5, "Метрика 'High Performance' — порожній маркетинг"
    ),
    "automated_task": (
        "Automated Task",
        -5, "Метрика 'Automated Task' — не несе інформації"
    ),
}

# Бонуси за ознаки якості
QUALITY_BONUSES = {
    "has_table": (
        r"<table",
        +15, "Є HTML-таблиця з детальними даними"
    ),
    "has_params_in_api": (
        r"def \w+\([^)]+\)",
        +10, "API містить параметри функцій"
    ),
    "has_return_type": (
        r"→\s*(None|List|Dict|str|int|float|bool|DataFrame|pd\.|Optional)",
        +8, "API містить тип повернення"
    ),
    "has_specific_diagram": (
        r'graph TD.*?(?:SELECT|ALTER|INSERT|UPDATE|DELETE|fetch|load|train|predict)',
        +12, "Діаграма містить конкретні операції (SQL/ML/API)"
    ),
    "has_code_snippet": (
        r"```python",
        +10, "Є приклад коду Python"
    ),
    "has_real_version": (
        r'v\d+\.\d+\.\d+(?!</span>.*v5\.0\.0)',
        +5, "Є реальний номер версії"
    ),
    "has_sql_columns": (
        r"DECIMAL|VARCHAR|BIGINT|TEXT|BOOLEAN|TIMESTAMP|JSONB",
        +10, "Документовані SQL-типи даних (схема БД)"
    ),
}

# ─────────────────────────────────────────────
# ТИПИ ДАНИХ
# ─────────────────────────────────────────────
@dataclass
class Issue:
    key: str
    description: str
    penalty: int


@dataclass
class Bonus:
    key: str
    description: str
    points: int


@dataclass
class PassportAuditResult:
    md_file: Path
    py_file: Optional[Path]
    score: int
    issues: list[Issue] = field(default_factory=list)
    bonuses: list[Bonus] = field(default_factory=list)
    py_functions: list[str] = field(default_factory=list)
    py_imports: list[str] = field(default_factory=list)
    py_classes: list[str] = field(default_factory=list)
    py_lines: int = 0
    md_size_bytes: int = 0
    orphaned: bool = False   # паспорт без вихідного .py файлу


# ─────────────────────────────────────────────
# ПОШУК PYTHON-ФАЙЛУ ДЛЯ ПАСПОРТУ
# ─────────────────────────────────────────────
def find_py_file(md_path: Path) -> Optional[Path]:
    """
    Шукає Python-файл двома способами:
    1. Читає коментар # ATLAS_PASSPORT: <шлях> у .py файлах
    2. Fallback: ім'я .md → ім'я .py по всій src/
    """
    md_name = md_path.stem  # наприклад 'migrate_db'

    # Пошук за тегом ATLAS_PASSPORT в усіх .py файлах
    expected_tag = f"docs/system/map/{md_name}.md"
    for py in SRC_ROOT.rglob("*.py"):
        try:
            first_lines = py.read_text(encoding="utf-8", errors="ignore")[:500]
            if expected_tag in first_lines:
                return py
        except Exception:
            continue

    # Fallback: пошук за назвою файлу
    candidates = list(SRC_ROOT.rglob(f"{md_name}.py"))
    if candidates:
        return candidates[0]

    return None


# ─────────────────────────────────────────────
# ПАРСИНГ PYTHON-ФАЙЛУ (AST)
# ─────────────────────────────────────────────
def parse_py_file(py_path: Path) -> tuple[list[str], list[str], list[str], int]:
    """Повертає (functions, imports, classes, lines_count)."""
    try:
        source = py_path.read_text(encoding="utf-8", errors="ignore")
        lines = source.count("\n") + 1
        tree = ast.parse(source)
    except Exception:
        return [], [], [], 0

    functions, imports, classes = [], [], []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Збираємо сигнатуру з параметрами
            args = [a.arg for a in node.args.args if a.arg != "self"]
            sig = f"def {node.name}({', '.join(args)})"
            functions.append(sig)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split(".")[0])

    return functions, list(set(imports)), classes, lines


# ─────────────────────────────────────────────
# ОЦІНКА ЯКОСТІ ПАСПОРТУ
# ─────────────────────────────────────────────
def audit_passport(md_path: Path) -> PassportAuditResult:
    score = 100
    issues: list[Issue] = []
    bonuses: list[Bonus] = []

    try:
        content = md_path.read_text(encoding="utf-8", errors="ignore")
        md_size = md_path.stat().st_size
    except Exception:
        return PassportAuditResult(md_path, None, 0, orphaned=True)

    # Знайти Python-файл
    py_file = find_py_file(md_path)
    py_funcs, py_imports, py_classes, py_lines = [], [], [], 0
    orphaned = False

    if py_file is None:
        orphaned = True
        score -= 5  # невелика пенальті — документ може бути для пакету
        issues.append(Issue("no_source", "Не знайдено відповідний .py файл", -5))
    else:
        py_funcs, py_imports, py_classes, py_lines = parse_py_file(py_file)

    # ── Перевірка GENERIC-шаблонів ──
    for key, (pattern, penalty, desc) in GENERIC_PATTERNS.items():
        if pattern in content:
            score += penalty
            issues.append(Issue(key, desc, penalty))

    # ── Перевірка БОНУСІВ ──
    for key, (pattern, points, desc) in QUALITY_BONUSES.items():
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            score += points
            bonuses.append(Bonus(key, desc, points))

    # ── Перевірка API: чи є реальні функції з py_file ──
    if py_funcs:
        matched = sum(1 for fn_sig in py_funcs if fn_sig.split("(")[0].replace("def ", "") in content)
        if matched == 0:
            score -= 10
            issues.append(Issue(
                "api_mismatch",
                f"Жодна з {len(py_funcs)} функцій .py не згадана в паспорті",
                -10
            ))
        elif matched < len(py_funcs) * 0.5:
            score -= 5
            issues.append(Issue(
                "api_partial",
                f"Задокументовано лише {matched}/{len(py_funcs)} функцій",
                -5
            ))

    # ── Перевірка: чи є у паспорті параметри функцій з py_file ──
    for fn_sig in py_funcs[:10]:  # перевіряємо перші 10
        fn_name = fn_sig.split("(")[0].replace("def ", "")
        # Якщо функція є в паспорті але без параметрів — пенальті
        if fn_name in content:
            in_passport_call = re.search(rf"def {fn_name}\([^)]*\)", content)
            if not in_passport_call:
                score -= 2
                issues.append(Issue(
                    f"missing_params_{fn_name}",
                    f"Функція {fn_name}() є в паспорті без параметрів",
                    -2
                ))

    score = max(0, min(100, score))

    return PassportAuditResult(
        md_file=md_path,
        py_file=py_file,
        score=score,
        issues=issues,
        bonuses=bonuses,
        py_functions=py_funcs,
        py_imports=py_imports,
        py_classes=py_classes,
        py_lines=py_lines,
        md_size_bytes=md_size,
        orphaned=orphaned,
    )


# ─────────────────────────────────────────────
# ГРУПУВАННЯ ЗА ПРІОРИТЕТОМ
# ─────────────────────────────────────────────
def priority_label(score: int) -> str:
    if score <= 30:
        return "🔴 CRITICAL"
    elif score <= 50:
        return "🟠 HIGH"
    elif score <= 65:
        return "🟡 MEDIUM"
    elif score <= 80:
        return "🔵 LOW"
    else:
        return "✅ OK"


# ─────────────────────────────────────────────
# ГЕНЕРАЦІЯ MARKDOWN-ЗВІТУ
# ─────────────────────────────────────────────
def generate_report(results: list[PassportAuditResult], threshold: int = 100) -> str:
    filtered = [r for r in results if r.score < threshold]
    filtered.sort(key=lambda r: r.score)

    total = len(results)
    ok_count = sum(1 for r in results if r.score > 80)
    low_count = sum(1 for r in results if 65 < r.score <= 80)
    med_count = sum(1 for r in results if 50 < r.score <= 65)
    high_count = sum(1 for r in results if 30 < r.score <= 50)
    crit_count = sum(1 for r in results if r.score <= 30)

    lines = [
        "# ATLAS Passport Quality Audit Report",
        f"> Згенеровано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Загальна статистика",
        "",
        f"| Метрика | Значення |",
        f"|---|---|",
        f"| Всього паспортів | {total} |",
        f"| ✅ OK (>80) | {ok_count} |",
        f"| 🔵 LOW (66–80) | {low_count} |",
        f"| 🟡 MEDIUM (51–65) | {med_count} |",
        f"| 🟠 HIGH (31–50) | {high_count} |",
        f"| 🔴 CRITICAL (≤30) | {crit_count} |",
        f"| Потребують виправлення (поріг {threshold}) | {len(filtered)} |",
        "",
        "---",
        "",
        "## Пріоритизований план виправлень",
        "",
        f"*(Показані {len(filtered)} файлів з оцінкою < {threshold}, відсортовані від найгіршого)*",
        "",
    ]

    for i, r in enumerate(filtered, 1):
        priority = priority_label(r.score)
        md_name = r.md_file.name
        py_name = r.py_file.name if r.py_file else "❌ не знайдено"
        py_path_rel = str(r.py_file.relative_to(ROOT)).replace("\\", "/") if r.py_file else "—"

        lines.append(f"### {i}. `{md_name}` — {priority} (оцінка: {r.score}/100)")
        lines.append("")
        lines.append(f"- **Джерело:** `{py_path_rel}` ({r.py_lines} рядків)")
        lines.append(f"- **Розмір паспорту:** {r.md_size_bytes // 1024} KB")

        if r.py_functions:
            funcs_preview = ", ".join(f"`{f.split('(')[0].replace('def ', '')}()`" for f in r.py_functions[:6])
            if len(r.py_functions) > 6:
                funcs_preview += f" _+{len(r.py_functions) - 6} ін._"
            lines.append(f"- **Функції в .py:** {funcs_preview}")

        if r.py_classes:
            lines.append(f"- **Класи:** {', '.join(f'`{c}`' for c in r.py_classes[:4])}")

        if r.issues:
            lines.append("")
            lines.append("**Проблеми:**")
            for iss in r.issues:
                lines.append(f"  - [{iss.penalty:+d}] {iss.description}")

        if r.bonuses:
            lines.append("")
            lines.append("**Наявні плюси:**")
            for bon in r.bonuses:
                lines.append(f"  - [+{bon.points}] {bon.description}")

        # Конкретні кроки виправлення
        fix_steps = _generate_fix_steps(r)
        if fix_steps:
            lines.append("")
            lines.append("**Що потрібно зробити:**")
            for step in fix_steps:
                lines.append(f"  1. {step}")

        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def _generate_fix_steps(r: PassportAuditResult) -> list[str]:
    steps = []
    issue_keys = {iss.key for iss in r.issues}

    if "generic_subtitle" in issue_keys:
        steps.append("Замінити subtitle на конкретний опис модуля (що він робить, яку бізнес-задачу вирішує)")

    if "generic_badge" in issue_keys or "generic_badge_raw" in issue_keys:
        steps.append("Оновити hero-badge на роль модуля (VIEW, DATA SERVICE, ML ENGINE, DB QUERY, UTILITY, тощо)")

    if "defense_edition" in issue_keys:
        steps.append("Змінити status tag DEFENSE EDITION на відповідний (IDEMPOTENT, ASYNC, CACHED, тощо)")

    if "hardcoded_v5" in issue_keys:
        steps.append("Замінити v5.0.0 на реальну версію або прибрати")

    if "generic_diagram" in issue_keys or "generic_config_node" in issue_keys or "generic_comp_node" in issue_keys:
        steps.append(
            "Переписати Mermaid-діаграму: показати реальний flow (конкретні функції, SQL-запити, "
            "гілки обробки помилок)"
        )

    if "generic_api_desc" in issue_keys:
        steps.append(
            "В секції 03 додати реальні підписи з параметрами, типами та коротким описом що повертає"
        )

    if "api_mismatch" in issue_keys or "api_partial" in issue_keys:
        if r.py_functions:
            missing = [f"`{s}`" for s in r.py_functions[:5]]
            steps.append(f"Додати до секції API: {', '.join(missing)}")

    if any(k.startswith("missing_params_") for k in issue_keys):
        steps.append("Для кожної функції вказати параметри та тип повернення (→ тип)")

    if "no_source" in issue_keys:
        steps.append("Перевірити чи існує відповідний .py файл або додати тег # ATLAS_PASSPORT у вихідник")

    if not steps:
        steps.append("Загальне покращення: деталізувати метрики в METRICS GRID відповідно до реального модуля")

    return steps


# ─────────────────────────────────────────────
# ГЕНЕРАЦІЯ JSON ДЛЯ МАШИННОГО ЧИТАННЯ
# ─────────────────────────────────────────────
def generate_json_report(results: list[PassportAuditResult]) -> dict:
    return {
        "generated_at": datetime.now().isoformat(),
        "total": len(results),
        "summary": {
            "ok": sum(1 for r in results if r.score > 80),
            "low": sum(1 for r in results if 65 < r.score <= 80),
            "medium": sum(1 for r in results if 50 < r.score <= 65),
            "high": sum(1 for r in results if 30 < r.score <= 50),
            "critical": sum(1 for r in results if r.score <= 30),
        },
        "passports": [
            {
                "md": r.md_file.name,
                "py": str(r.py_file.relative_to(ROOT)).replace("\\", "/") if r.py_file else None,
                "score": r.score,
                "priority": priority_label(r.score),
                "issues": [{"key": i.key, "desc": i.description, "penalty": i.penalty} for i in r.issues],
                "bonuses": [{"key": b.key, "desc": b.description, "points": b.points} for b in r.bonuses],
                "py_functions_count": len(r.py_functions),
                "py_lines": r.py_lines,
                "md_size_bytes": r.md_size_bytes,
            }
            for r in sorted(results, key=lambda r: r.score)
        ],
    }


# ─────────────────────────────────────────────
# ГОЛОВНА ФУНКЦІЯ
# ─────────────────────────────────────────────
def main():
    import argparse

    parser = argparse.ArgumentParser(description="ATLAS Passport Quality Auditor")
    parser.add_argument(
        "--output", "-o",
        default=str(PASSPORT_DIR / "AUDIT_REPORT.md"),
        help="Шлях для збереження MD-звіту (default: docs/system/map/AUDIT_REPORT.md)",
    )
    parser.add_argument(
        "--json-output", "-j",
        default=str(PASSPORT_DIR / "AUDIT_REPORT.json"),
        help="Шлях для збереження JSON-звіту",
    )
    parser.add_argument(
        "--fix-threshold", "-t",
        type=int, default=81,
        help="Показати лише файли з оцінкою нижче порогу (default: 81 = всі крім OK)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Виводити прогрес у консоль",
    )
    args = parser.parse_args()

    md_files = sorted(PASSPORT_DIR.glob("*.md"))
    # Пропускаємо службові файли
    skip_names = {"AUDIT_REPORT.md", "ATLAS_MASTER_INDEX.md", "SUMMARY_DASHBOARD.md"}
    md_files = [f for f in md_files if f.name not in skip_names]

    print(f"🔍 Аудит {len(md_files)} паспортних файлів...")
    print(f"   Джерела: {SRC_ROOT}")
    print(f"   Звіт:    {args.output}")
    print()

    results: list[PassportAuditResult] = []
    for i, md_path in enumerate(md_files, 1):
        result = audit_passport(md_path)
        results.append(result)

        if args.verbose:
            py_name = result.py_file.name if result.py_file else "❌"
            print(f"  [{i:3d}/{len(md_files)}] {priority_label(result.score):20s} "
                  f"{result.score:3d}/100  {md_path.name:<40s} → {py_name}")
        else:
            # Простий прогрес-бар
            bar_done = int(40 * i / len(md_files))
            bar = "█" * bar_done + "░" * (40 - bar_done)
            print(f"\r  [{bar}] {i}/{len(md_files)}", end="", flush=True)

    print()
    print()

    # Збереження звітів
    md_report = generate_report(results, threshold=args.fix_threshold)
    Path(args.output).write_text(md_report, encoding="utf-8")

    json_report = generate_json_report(results)
    Path(args.json_output).write_text(json.dumps(json_report, ensure_ascii=False, indent=2), encoding="utf-8")

    # Підсумок у консоль
    ok = sum(1 for r in results if r.score > 80)
    crit = sum(1 for r in results if r.score <= 30)
    high = sum(1 for r in results if 30 < r.score <= 50)
    med = sum(1 for r in results if 50 < r.score <= 65)
    low = sum(1 for r in results if 65 < r.score <= 80)
    need_fix = sum(1 for r in results if r.score < args.fix_threshold)

    avg = sum(r.score for r in results) // len(results) if results else 0

    print("═" * 60)
    print("  ATLAS PASSPORT AUDIT — ПІДСУМОК")
    print("═" * 60)
    print(f"  Всього паспортів :  {len(results)}")
    print(f"  Середня оцінка  :  {avg}/100")
    print(f"  ✅ OK  (>80)    :  {ok}")
    print(f"  🔵 LOW  (66-80) :  {low}")
    print(f"  🟡 MED  (51-65) :  {med}")
    print(f"  🟠 HIGH (31-50) :  {high}")
    print(f"  🔴 CRIT (≤30)   :  {crit}")
    print(f"  Потребують фіксу:  {need_fix}")
    print("═" * 60)
    print(f"  📄 MD-звіт  → {args.output}")
    print(f"  📊 JSON-звіт→ {args.json_output}")
    print("═" * 60)

    # Топ-10 найгірших
    worst = sorted(results, key=lambda r: r.score)[:10]
    print()
    print("  ТОП-10 НАЙГІРШИХ ПАСПОРТІВ:")
    for r in worst:
        print(f"    {priority_label(r.score)} {r.score:3d}/100  {r.md_file.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
