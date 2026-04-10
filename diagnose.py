"""
╔══════════════════════════════════════════════════════════════╗
║       ENERGY MONITOR: POWER DIAGNOSTICS ENGINE v2.0         ║
║                                                              ║
║  Сканує весь проект на помилки, вразливості та проблеми.    ║
║  [NEW v2] Security Audit: SQL Injection, Secrets, Timeouts  ║
║                                                              ║
║  Запуск:  python diagnose.py                                 ║
║  Звіт:    diagnostics_report.html                            ║
╚══════════════════════════════════════════════════════════════╝
"""
import ast
import importlib.util
import importlib
import re
import sys
import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


# ─── CONFIG ─────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
SCAN_DIRS = ["ui", "src", "core", "app", "utils", "ml"]
EXCLUDE_DIRS = {"__pycache__", ".git", "site", "node_modules", ".pytest_cache"}
OUTPUT_HTML = ROOT / "diagnostics_report.html"

STDLIB_MODULES = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else set()
KNOWN_THIRD_PARTY = {
    "streamlit", "pandas", "numpy", "plotly", "sqlalchemy", "psycopg2",
    "sklearn", "joblib", "scipy", "dotenv", "tornado", "requests",
    "altair", "pydeck", "folium", "streamlit_folium", "statsmodels",
    "xgboost", "lightgbm", "catboost", "prophet", "onnxruntime",
    "psutil", "matplotlib", "seaborn",
}

ALLOWED_TOP_LEVEL_CALLS = {
    "load_dotenv", "setup_logger", "getLogger", "basicConfig",
    "mkdir", "makedirs", "warn", "filterwarnings", "templates",
    "exists", "touch", "unlink",
}

LONG_FUNCTION_THRESHOLD_UI = 200
LONG_FUNCTION_THRESHOLD_DEFAULT = 100

# ─── SECURITY: небезпечні паттерни (regex по вихідному коду) ─────────────────
# Формат: (regex, severity, code, message)
SECURITY_PATTERNS = [
    # SQL Injection via f-string or % formatting
    (
        r'(?:execute|run_query|cursor\.execute)\s*\([^)]*f["\'].*?\{',
        "ERROR", "SQL_INJECTION_FSTRING",
        "⛔ Можлива SQL-ін'єкція: f-string в SQL-запиті. Використовуй parameterized queries (`:param` або `%s`)."
    ),
    (
        r'(?:execute|run_query)\s*\([^)]*%\s*[(\w]',
        "WARNING", "SQL_INJECTION_FORMAT",
        "⚠️ Потенційна SQL-ін'єкція: `%` форматування в SQL. Використовуй `params={}` замість форматування рядка."
    ),
    # Hardcoded secrets
    (
        r'(?:password|passwd|secret|token|api_key|apikey)\s*=\s*["\'][^"\']{4,}["\']',
        "ERROR", "HARDCODED_SECRET",
        "🔑 Жорстко вписаний секрет/пароль в коді! Використовуй `os.getenv()` або `.env` файл."
    ),
    # Unsafe SQL with string concat
    (
        r'["\']SELECT.*?\+\s*\w',
        "WARNING", "SQL_STRING_CONCAT",
        "⚠️ Конкатенація рядків в SQL — небезпечно. Використовуй параметризовані запити."
    ),
    # Dangerous eval/exec
    (
        r'\beval\s*\(|exec\s*\(',
        "ERROR", "DANGEROUS_EVAL",
        "☠️ Використання `eval()` або `exec()` — критична вразливість виконання довільного коду."
    ),
    # Unsafe pickle/yaml.load
    (
        r'pickle\.load|yaml\.load\s*\([^)]*Loader',
        "WARNING", "UNSAFE_DESERIALIZATION",
        "⚠️ Небезпечна десеріалізація. `pickle.load` або `yaml.load` без SafeLoader може виконати довільний код."
    ),
    # Missing timeout in requests
    (
        r'requests\.(get|post|put|delete|patch)\s*\([^)]*\)(?!.*timeout)',
        "WARNING", "MISSING_TIMEOUT",
        "⏱️ HTTP-запит без `timeout=`. Додай `timeout=10` щоб уникнути зависання."
    ),
    # Unsafe file path join with user input (basic heuristic)
    (
        r'os\.path\.join\s*\([^)]*request|os\.path\.join\s*\([^)]*input',
        "WARNING", "PATH_TRAVERSAL",
        "🗂️ Потенційна path traversal: `os.path.join` з даними від користувача. Валідуй вхідні шляхи."
    ),
    # Catching and silently ignoring exceptions
    (
        r'except\s+Exception[^:]*:\s*\n\s*pass',
        "WARNING", "SILENT_EXCEPTION",
        "🔇 `except Exception: pass` тихо ковтає всі помилки. Хоча б залогуй їх."
    ),
    # Unprotected DB connection string in source
    (
        r'postgresql://[^{}\s"\']{8,}',
        "ERROR", "EXPOSED_CONN_STRING",
        "🔑 Рядок підключення до БД вбудований в код! Перенеси в `.env` файл."
    ),
    # TODO/FIXME/HACK security markers
    (
        r'#\s*(TODO|FIXME|HACK|BUG|XXX)',
        "INFO", "TODO_MARKER",
        "📝 Знайдено маркер незавершеного коду в коментарях."
    ),
    # Using assert for validation (removed in -O mode)
    (
        r'^(?!\s*#)\s*assert\s+\w',
        "INFO", "ASSERT_FOR_VALIDATION",
        "⚡ `assert` не спрацьовує при запуску з -O. Не використовуй для валідації вхідних даних."
    ),
    # Wrong module attribute: calling function from wrong module (e.g. db.create_custom_alert)
    # Heuristic: module alias + function that's imported explicitly from another module
    (
        r'\bdb\.(create_|delete_|update_|cleanup_|get_latest|insert_)',
        "ERROR", "WRONG_MODULE_ATTR",
        "☠️ Виклик `db.<function>` — ця функція, скоріш за все, в `db_services`, не в `database`. Перевір імпорти."
    ),
    # Categorical unsafe mutation (assigning scalar/int to a Categorical column or fillna(0))
    (
        r'\bdf\[[\"\'][^\"\']+[\"\']\]\s*=\s*(?:0|1|None|np\.nan|True|False|\d)|\.fillna\(\s*0\s*\)',
        "WARNING", "CATEGORICAL_UNSAFE_ASSIGN",
        "⚠️ Присвоєння 0 або .fillna(0) — якщо колонка є Category, виникне помилка. Використовуй `.select_dtypes(include=['number'])` перед fillna."
    ),
    # Missing scroll spacer in long view render functions
    (
        r'def render\(.*\):|def render_.*\(.*\):',
        "INFO", "MISSING_SCROLL_SPACER",
        "📏 Перевір чи є `st.markdown('<div style=\"height: 200px;\"></div>')` в кінці render() для коректного скролу."
    ),
]

# ─── DATA CLASSES ─────────────────────────────────────────────────────────────
@dataclass
class DiagIssue:
    severity: str   # "ERROR" | "WARNING" | "INFO"
    code: str
    message: str
    line: Optional[int] = None
    category: str = "quality"  # "quality" | "security"


@dataclass
class FunctionDiag:
    name: str
    lineno: int
    lines: int = 0
    issues: list[DiagIssue] = field(default_factory=list)

    @property
    def status(self):
        if any(i.severity == "ERROR" for i in self.issues):
            return "ERROR"
        if any(i.severity == "WARNING" for i in self.issues):
            return "WARNING"
        return "OK"


@dataclass
class FileDiag:
    path: Path
    rel_path: str
    syntax_ok: bool
    syntax_error: Optional[str] = None
    imports: list[str] = field(default_factory=list)
    missing_imports: list[str] = field(default_factory=list)
    functions: list[FunctionDiag] = field(default_factory=list)
    file_issues: list[DiagIssue] = field(default_factory=list)
    security_issues: list[DiagIssue] = field(default_factory=list)

    @property
    def status(self):
        if not self.syntax_ok:
            return "ERROR"
        if self.missing_imports:
            return "ERROR"
        if any(i.severity == "ERROR" for i in self.file_issues + self.security_issues):
            return "ERROR"
        all_fn_issues = [i for fn in self.functions for i in fn.issues]
        if any(i.severity in ("ERROR", "WARNING") for i in all_fn_issues + self.file_issues + self.security_issues):
            return "WARNING"
        return "OK"

    @property
    def total_issues(self):
        count = len(self.missing_imports) + len(self.file_issues) + len(self.security_issues)
        for fn in self.functions:
            count += len(fn.issues)
        return count

    @property
    def security_status(self):
        if any(i.severity == "ERROR" for i in self.security_issues):
            return "CRITICAL"
        if any(i.severity == "WARNING" for i in self.security_issues):
            return "RISK"
        return "SAFE"


# ─── SCANNER ─────────────────────────────────────────────────────────────────
class ProjectScanner:
    def __init__(self, root: Path):
        self.root = root
        self.results: list[FileDiag] = []
        self._available_modules = self._build_module_set()

    def _build_module_set(self) -> set:
        local = set()
        for scan_dir in SCAN_DIRS:
            d = self.root / scan_dir
            if d.exists():
                for f in d.rglob("*.py"):
                    rel = f.relative_to(self.root)
                    parts = list(rel.with_suffix("").parts)
                    for i in range(len(parts)):
                        local.add(".".join(parts[i:]))
        for f in self.root.glob("*.py"):
            local.add(f.stem)
        return local

    def scan_all(self):
        py_files = []
        for scan_dir in SCAN_DIRS:
            d = self.root / scan_dir
            if d.exists():
                for f in d.rglob("*.py"):
                    if not any(ex in f.parts for ex in EXCLUDE_DIRS):
                        py_files.append(f)
        for f in self.root.glob("*.py"):
            if f.name not in {"diagnose.py", "refactor_run.py", "benchmark_models.py"}:
                py_files.append(f)

        print(f"\n🔍 Сканування {len(py_files)} Python файлів...")
        for i, fpath in enumerate(sorted(py_files)):
            rel = str(fpath.relative_to(self.root))
            print(f"   [{i+1:>3}/{len(py_files)}] {rel}", end="\r")
            self.results.append(self._analyze_file(fpath))
        print(f"\n✅ Сканування завершено. {len(self.results)} файлів оброблено.\n")

    def _analyze_file(self, fpath: Path) -> FileDiag:
        rel = str(fpath.relative_to(self.root))
        diag = FileDiag(path=fpath, rel_path=rel, syntax_ok=False)

        try:
            source = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            diag.file_issues.append(DiagIssue("ERROR", "FILE_READ_ERROR", str(e)))
            return diag

        # 1. Синтаксична перевірка
        try:
            tree = ast.parse(source, filename=str(fpath))
            diag.syntax_ok = True
        except SyntaxError as e:
            diag.syntax_ok = False
            diag.syntax_error = f"Line {e.lineno}: {e.msg}"
            return diag

        # 2. Imports
        diag.imports, diag.missing_imports = self._check_imports(tree, fpath)

        # 3. Функції
        diag.functions = self._check_functions(tree, fpath)

        # 4. Паттерни якості
        diag.file_issues += self._check_file_patterns(tree, source)

        # 5. [NEW] Безпека
        diag.security_issues = self._check_security(source, fpath)

        return diag

    def _check_imports(self, tree: ast.AST, fpath: Path):
        imports, missing = [], []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    base = alias.name.split(".")[0]
                    imports.append(base)
                    if not self._is_known(base, fpath):
                        missing.append(f"import {alias.name} (line {node.lineno})")
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    base = node.module.split(".")[0]
                    full = node.module
                    imports.append(base)
                    if not self._is_known(base, fpath) and not self._is_known(full, fpath):
                        names = ", ".join(a.name for a in node.names)
                        missing.append(f"from {node.module} import {names} (line {node.lineno})")
        return imports, missing

    def _is_known(self, module_name: str, fpath: Path) -> bool:
        if module_name in STDLIB_MODULES:
            return True
        if module_name in KNOWN_THIRD_PARTY:
            return True
        if module_name in self._available_modules:
            return True
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is not None:
                return True
        except (ModuleNotFoundError, ValueError):
            pass
        return False

    def _check_functions(self, tree: ast.AST, fpath: Path) -> list[FunctionDiag]:
        funcs = []
        is_ui = "ui" in str(fpath).lower() or "view" in str(fpath).lower()
        long_fn_threshold = LONG_FUNCTION_THRESHOLD_UI if is_ui else LONG_FUNCTION_THRESHOLD_DEFAULT

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn_lines = node.end_lineno - node.lineno + 1 if hasattr(node, "end_lineno") else 0
                fn_diag = FunctionDiag(name=node.name, lineno=node.lineno, lines=fn_lines)

                for child in ast.walk(node):
                    if isinstance(child, ast.ExceptHandler) and child.type is None:
                        fn_diag.issues.append(DiagIssue(
                            "WARNING", "BARE_EXCEPT",
                            "Голий `except:` ловить ВСІ помилки. Краще `except Exception as e:`",
                            line=child.lineno
                        ))

                body_nodes = [n for n in node.body if not isinstance(n, (ast.Pass, ast.Expr))]
                if not body_nodes:
                    expr_nodes = [n for n in node.body if isinstance(n, ast.Expr)]
                    is_just_docstring = all(isinstance(e.value, ast.Constant) for e in expr_nodes)
                    if is_just_docstring or not node.body:
                        fn_diag.issues.append(DiagIssue(
                            "INFO", "EMPTY_FUNCTION",
                            "Функція порожня або містить лише docstring/pass.",
                            line=node.lineno
                        ))

                fn_lines = node.end_lineno - node.lineno if hasattr(node, "end_lineno") else 0
                if fn_lines > long_fn_threshold:
                    fn_diag.issues.append(DiagIssue(
                        "WARNING", "LONG_FUNCTION",
                        f"Функція дуже довга ({fn_lines} рядків, поріг: {long_fn_threshold}).",
                        line=node.lineno
                    ))

                funcs.append(fn_diag)
        return funcs

    def _check_file_patterns(self, tree: ast.AST, source: str) -> list[DiagIssue]:
        issues = []
        lines = source.splitlines()

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("print(") and not stripped.startswith("#"):
                issues.append(DiagIssue(
                    "INFO", "PRINT_STATEMENT",
                    f"Знайдено `print()` на рядку {i}. Чи це відладочний вивід?",
                    line=i
                ))

        has_main_guard = any("__name__" in line and "__main__" in line for line in lines)
        top_level_calls = []
        for n in tree.body:
            if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call):
                call = n.value
                func_name = ""
                if isinstance(call.func, ast.Name):
                    func_name = call.func.id
                elif isinstance(call.func, ast.Attribute):
                    func_name = call.func.attr
                if func_name not in ALLOWED_TOP_LEVEL_CALLS:
                    top_level_calls.append(n)

        if top_level_calls and not has_main_guard:
            issues.append(DiagIssue(
                "WARNING", "NO_MAIN_GUARD",
                "Є виклики на верхньому рівні без захисту `if __name__ == '__main__':`."
            ))

        return issues

    def _check_security(self, source: str, fpath: Path) -> list[DiagIssue]:
        """[NEW v2.0] Сканує файл на вразливості безпеки."""
        issues = []
        lines = source.splitlines()

        for pattern, severity, code, message in SECURITY_PATTERNS:
            try:
                for i, line in enumerate(lines):
                    # Ігноруємо коментарі при пошуку вразливостей ( False Positives Fix )
                    if line.strip().startswith("#"):
                        continue
                        
                    m = re.search(pattern, line, re.IGNORECASE)
                    if m:
                        lineno = i + 1
                        # Не дублювати
                        if not any(i.code == code and i.line == lineno for i in issues):
                            issues.append(DiagIssue(
                                severity, code, message,
                                line=lineno, category="security"
                            ))
            except re.error:
                pass

        return issues


# ─── HTML REPORTER v2.0 ────────────────────────────────────────────────────────
class HtmlReporter:

    def generate(self, results: list[FileDiag], output: Path):
        total = len(results)
        ok = sum(1 for r in results if r.status == "OK")
        warn = sum(1 for r in results if r.status == "WARNING")
        err = sum(1 for r in results if r.status == "ERROR")
        total_issues = sum(r.total_issues for r in results)

        # Security summary
        sec_critical = sum(1 for r in results if r.security_status == "CRITICAL")
        sec_risk = sum(1 for r in results if r.security_status == "RISK")
        sec_total = sum(len(r.security_issues) for r in results)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        rows = ""
        for r in sorted(results, key=lambda x: (x.status != "ERROR", x.status != "WARNING", x.rel_path)):
            rows += self._file_row(r)

        html = f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Energy Monitor — Diagnostics v2.0</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Inter', sans-serif; background: #0d1117; color: #c9d1d9; min-height: 100vh; }}

  .hero {{ background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
           border-bottom: 1px solid #30363d; padding: 2.5rem 2rem 1.5rem; }}
  .hero h1 {{ font-size: 1.8rem; font-weight: 700; color: #58a6ff; letter-spacing: -0.02em; }}
  .hero .version {{ display: inline-block; background: #1f6feb22; color: #58a6ff; border: 1px solid #1f6feb44;
                    font-size: 0.72rem; padding: 2px 8px; border-radius: 20px; margin-left: 0.5rem; font-family: 'JetBrains Mono', monospace; }}
  .hero p {{ color: #8b949e; margin-top: 0.25rem; font-size: 0.9rem; }}
  .hero small {{ font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #484f58; }}

  .stats {{ display: flex; gap: 1rem; padding: 1.5rem 2rem; flex-wrap: wrap; }}
  .stat-card {{ flex: 1; min-width: 130px; background: #161b22; border: 1px solid #30363d;
               border-radius: 12px; padding: 1.2rem 1.5rem; text-align: center; }}
  .stat-card .num {{ font-size: 2.2rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }}
  .stat-card .lbl {{ font-size: 0.72rem; color: #8b949e; margin-top: 0.3rem; text-transform: uppercase; letter-spacing: 0.05em; }}
  .stat-card.total .num {{ color: #58a6ff; }}
  .stat-card.ok .num {{ color: #3fb950; }}
  .stat-card.warn .num {{ color: #d29922; }}
  .stat-card.err .num {{ color: #f85149; }}
  .stat-card.sec-crit .num {{ color: #ff6e6e; }}
  .stat-card.sec-risk .num {{ color: #ffb86c; }}
  .stat-card.sec-total .num {{ color: #bd93f9; }}

  .sec-banner {{ margin: 0 2rem 1.5rem; padding: 1rem 1.5rem; border-radius: 10px;
                 background: #4a10101a; border: 1px solid #f8514944; }}
  .sec-banner.safe {{ background: #1a4a2e1a; border-color: #3fb95044; }}
  .sec-banner h3 {{ color: #f85149; font-size: 0.9rem; margin-bottom: 0.3rem; }}
  .sec-banner.safe h3 {{ color: #3fb950; }}
  .sec-banner p {{ font-size: 0.82rem; color: #8b949e; }}

  .section {{ padding: 0 2rem 2rem; }}
  .section-title {{ font-size: 0.75rem; font-weight: 600; color: #8b949e; text-transform: uppercase;
                    letter-spacing: 0.08em; padding: 1rem 0 0.5rem; border-top: 1px solid #21262d; margin-top: 0.5rem; }}

  .file-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px;
               margin-bottom: 0.7rem; overflow: hidden; transition: border-color 0.2s; }}
  .file-card:hover {{ border-color: #58a6ff44; }}
  .file-card.status-ERROR {{ border-left: 3px solid #f85149; }}
  .file-card.status-WARNING {{ border-left: 3px solid #d29922; }}
  .file-card.status-OK {{ border-left: 3px solid #3fb950; }}

  .file-header {{ display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1.2rem;
                  cursor: pointer; user-select: none; }}
  .file-header:hover {{ background: rgba(88,166,255,0.04); }}
  .file-path {{ font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #c9d1d9; flex: 1; }}
  .file-stats {{ font-size: 0.75rem; color: #8b949e; }}

  .status-badge {{ font-size: 0.7rem; font-weight: 600; padding: 3px 8px; border-radius: 20px; white-space: nowrap; }}
  .badge-OK {{ background: #1a4a2e; color: #3fb950; }}
  .badge-WARNING {{ background: #4a3800; color: #d29922; }}
  .badge-ERROR {{ background: #4a1010; color: #f85149; }}
  .badge-SEC {{ background: #3d1a4a; color: #bd93f9; font-size: 0.65rem; }}

  .file-body {{ display: none; border-top: 1px solid #21262d; padding: 1rem 1.2rem; }}
  .file-body.open {{ display: block; }}

  .issue-section-title {{ font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
                           letter-spacing: 0.06em; margin: 0.75rem 0 0.4rem; padding: 4px 8px;
                           border-radius: 4px; display: inline-block; }}
  .quality-title {{ background: #1f6feb11; color: #58a6ff; border: 1px solid #1f6feb22; }}
  .security-title {{ background: #bd93f911; color: #bd93f9; border: 1px solid #bd93f922; }}

  .issue-list {{ list-style: none; }}
  .issue-item {{ display: flex; gap: 0.6rem; align-items: flex-start;
                 padding: 0.4rem 0; border-bottom: 1px solid #21262d1a; font-size: 0.82rem; }}
  .issue-item:last-child {{ border-bottom: none; }}
  .sev-badge {{ font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 4px;
               white-space: nowrap; font-family: 'JetBrains Mono', monospace; min-width: 42px; text-align: center; }}
  .sev-ERROR {{ background: #fee2e2; color: #7f1d1d; }}
  .sev-WARNING {{ background: #fef3c7; color: #92400e; }}
  .sev-INFO {{ background: #eff6ff; color: #1e3a8a; }}
  .issue-code {{ color: #79c0ff; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; min-width: 160px; }}
  .issue-code.sec {{ color: #bd93f9; }}
  .issue-msg {{ color: #c9d1d9; flex: 1; }}
  .issue-line {{ color: #484f58; font-size: 0.72rem; font-family: 'JetBrains Mono', monospace; white-space: nowrap; }}

  .fn-section {{ margin-top: 0.75rem; }}
  .fn-row {{ display: flex; align-items: center; gap: 0.5rem; padding: 0.25rem 0; font-size: 0.8rem; }}
  .fn-name {{ font-family: 'JetBrains Mono', monospace; color: #79c0ff; }}
  .fn-line {{ color: #484f58; font-size: 0.7rem; }}

  .missing-imports {{ margin-top: 0.5rem; }}
  .mi-title {{ font-size: 0.72rem; color: #f85149; margin-bottom: 0.4rem; text-transform: uppercase; }}
  .mi-item {{ font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #ffa198;
              background: #4a10101a; border-radius: 4px; padding: 3px 8px; margin: 2px 0; }}

  .syntax-error {{ background: #4a101022; border: 1px solid #f8514944; border-radius: 6px;
                   padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #ffa198; }}

  @media (max-width: 700px) {{
    .stats {{ flex-direction: column; }}
    .hero, .section {{ padding: 1rem; }}
  }}
</style>
<script>
function toggleCard(el) {{
  const body = el.nextElementSibling;
  body.classList.toggle('open');
}}
function filterCards(status) {{
  document.querySelectorAll('.file-card').forEach(c => {{
    if (status === 'all') {{ c.style.display = ''; return; }}
    if (status === 'SEC') {{ c.style.display = c.dataset.sec === '1' ? '' : 'none'; return; }}
    c.style.display = c.classList.contains('status-' + status) ? '' : 'none';
  }});
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  document.querySelector('[data-filter="' + status + '"]').classList.add('active');
}}
function expandAll() {{
  document.querySelectorAll('.file-body').forEach(b => b.classList.add('open'));
}}
function collapseAll() {{
  document.querySelectorAll('.file-body').forEach(b => b.classList.remove('open'));
}}
</script>
</head>
<body>
<div class="hero">
  <h1>⚡ Energy Monitor — Diagnostics <span class="version">v2.0</span></h1>
  <p>Автоматичний аудит якості коду + 🔐 Security Scan</p>
  <small>Згенеровано: {ts}</small>
</div>

<div class="stats">
  <div class="stat-card total"><div class="num">{total}</div><div class="lbl">Файлів</div></div>
  <div class="stat-card ok"><div class="num">{ok}</div><div class="lbl">✅ Чисті</div></div>
  <div class="stat-card warn"><div class="num">{warn}</div><div class="lbl">⚠️ Попередження</div></div>
  <div class="stat-card err"><div class="num">{err}</div><div class="lbl">❌ Помилки</div></div>
  <div class="stat-card sec-crit"><div class="num">{sec_critical}</div><div class="lbl">🔴 Sec Critical</div></div>
  <div class="stat-card sec-risk"><div class="num">{sec_risk}</div><div class="lbl">🟡 Sec Risk</div></div>
  <div class="stat-card sec-total"><div class="num">{sec_total}</div><div class="lbl">🔐 Sec Issues</div></div>
</div>

{'<div class="sec-banner"><h3>🔴 Знайдено критичні вразливості безпеки!</h3><p>Перевір файли з позначкою 🔐 та усунь проблеми до деплою.</p></div>' if sec_critical > 0 else ('<div class="sec-banner"><h3>🟡 Знайдено ризики безпеки</h3><p>Перегляни файли з позначкою 🔐.</p></div>' if sec_risk > 0 else '<div class="sec-banner safe"><h3>✅ Security Scan чистий</h3><p>Критичних вразливостей не знайдено.</p></div>')}

<div class="section">
  <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1rem;align-items:center;">
    <button class="filter-btn active" data-filter="all" onclick="filterCards('all')"
      style="background:#21262d;border:1px solid #30363d;color:#c9d1d9;padding:6px 14px;border-radius:20px;cursor:pointer;font-size:0.8rem;">Всі</button>
    <button class="filter-btn" data-filter="ERROR" onclick="filterCards('ERROR')"
      style="background:#4a1010;border:1px solid #f85149;color:#f85149;padding:6px 14px;border-radius:20px;cursor:pointer;font-size:0.8rem;">❌ Помилки ({err})</button>
    <button class="filter-btn" data-filter="WARNING" onclick="filterCards('WARNING')"
      style="background:#4a3800;border:1px solid #d29922;color:#d29922;padding:6px 14px;border-radius:20px;cursor:pointer;font-size:0.8rem;">⚠️ Попередження ({warn})</button>
    <button class="filter-btn" data-filter="OK" onclick="filterCards('OK')"
      style="background:#1a4a2e;border:1px solid #3fb950;color:#3fb950;padding:6px 14px;border-radius:20px;cursor:pointer;font-size:0.8rem;">✅ Чисті ({ok})</button>
    <button class="filter-btn" data-filter="SEC" onclick="filterCards('SEC')"
      style="background:#3d1a4a;border:1px solid #bd93f9;color:#bd93f9;padding:6px 14px;border-radius:20px;cursor:pointer;font-size:0.8rem;">🔐 Security ({sec_total})</button>
    <span style="margin-left:auto;display:flex;gap:0.5rem;">
      <button onclick="expandAll()" style="background:none;border:1px solid #30363d;color:#8b949e;padding:4px 10px;border-radius:6px;cursor:pointer;font-size:0.75rem;">▼ Розкрити всі</button>
      <button onclick="collapseAll()" style="background:none;border:1px solid #30363d;color:#8b949e;padding:4px 10px;border-radius:6px;cursor:pointer;font-size:0.75rem;">▲ Згорнути всі</button>
    </span>
  </div>

  <div class="section-title">📁 Результати по файлах</div>
  {rows}
</div>
</body>
</html>"""

        output.write_text(html, encoding="utf-8")

    def _file_row(self, r: FileDiag) -> str:
        status = r.status
        icon = {"OK": "✅", "WARNING": "⚠️", "ERROR": "❌"}[status]
        fn_count = len(r.functions)
        issues_txt = f"{r.total_issues} проблем" if r.total_issues else "чисто"
        has_sec = len(r.security_issues) > 0
        sec_attr = 'data-sec="1"' if has_sec else 'data-sec="0"'

        body_html = ""
        if not r.syntax_ok:
            body_html += f'<div class="syntax-error">⛔ SYNTAX ERROR: {r.syntax_error}</div>'
        if r.missing_imports:
            body_html += '<div class="missing-imports">'
            body_html += f'<div class="mi-title">⛔ Відсутні imports ({len(r.missing_imports)})</div>'
            for mi in r.missing_imports:
                body_html += f'<div class="mi-item">{mi}</div>'
            body_html += '</div>'

        # Quality issues
        if r.file_issues:
            body_html += '<div class="issue-section-title quality-title">📋 Якість коду</div>'
            body_html += '<ul class="issue-list">'
            for issue in r.file_issues:
                body_html += self._issue_row(issue)
            body_html += '</ul>'

        # Security issues
        if r.security_issues:
            body_html += '<div class="issue-section-title security-title">🔐 Безпека</div>'
            body_html += '<ul class="issue-list">'
            for issue in r.security_issues:
                body_html += self._issue_row(issue, is_sec=True)
            body_html += '</ul>'

        # Functions with issues
        problem_fns = [f for f in r.functions if f.status != "OK"]
        if problem_fns:
            body_html += '<div class="fn-section">'
            body_html += f'<div class="issue-section-title quality-title">🔧 Функції ({len(problem_fns)})</div>'
            for fn in sorted(problem_fns, key=lambda x: x.lineno):
                sv = fn.status
                body_html += f'<div class="fn-row">'
                body_html += f'<span class="status-badge badge-{sv}">{sv}</span>'
                body_html += f'<span class="fn-name">{fn.name}()</span>'
                body_html += f'<span class="fn-line">L{fn.lineno}</span>'
                body_html += '</div>'
                body_html += '<ul class="issue-list" style="margin-left:1rem;">'
                for issue in fn.issues:
                    body_html += self._issue_row(issue)
                body_html += '</ul>'
            body_html += '</div>'

        ok_fns = [f for f in r.functions if f.status == "OK"]
        if ok_fns:
            names = ", ".join(f'<span class="fn-name">{f.name}()</span>' for f in ok_fns[:12])
            if len(ok_fns) > 12:
                names += f' <span style="color:#8b949e">+{len(ok_fns)-12} більше</span>'
            body_html += f'<div style="margin-top:0.5rem;font-size:0.78rem;color:#8b949e;">✅ OK: {names}</div>'

        if not body_html:
            body_html = '<div style="color:#3fb950;font-size:0.82rem;">✅ Файл чистий. Проблем не знайдено.</div>'

        sec_badge = f'<span class="status-badge badge-SEC">🔐 {len(r.security_issues)} вразл.</span>' if has_sec else ""

        return f"""
<div class="file-card status-{status}" {sec_attr}>
  <div class="file-header" onclick="toggleCard(this)">
    <span>{icon}</span>
    <span class="file-path">{r.rel_path}</span>
    <span class="file-stats">{fn_count} fn · {issues_txt}</span>
    {sec_badge}
    <span class="status-badge badge-{status}">{status}</span>
  </div>
  <div class="file-body">
    {body_html}
  </div>
</div>"""

    def _issue_row(self, issue: DiagIssue, is_sec: bool = False) -> str:
        sev = issue.severity
        line_txt = f"L{issue.line}" if issue.line else ""
        code_cls = "issue-code sec" if is_sec else "issue-code"
        return f"""<li class="issue-item">
  <span class="sev-badge sev-{sev}">{sev[:4]}</span>
  <span class="{code_cls}">{issue.code}</span>
  <span class="issue-msg">{issue.message}</span>
  <span class="issue-line">{line_txt}</span>
</li>"""


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "═" * 62)
    print("   ⚡ ENERGY MONITOR — POWER DIAGNOSTICS ENGINE v2.0")
    print("   🔐 + Security Audit Module")
    print("═" * 62)
    print(f"   📁 Корінь проекту: {ROOT}")
    print(f"   📂 Директорії: {', '.join(SCAN_DIRS)}")
    print("═" * 62)

    scanner = ProjectScanner(ROOT)
    scanner.scan_all()

    results = scanner.results
    ok_files = [r for r in results if r.status == "OK"]
    warn_files = [r for r in results if r.status == "WARNING"]
    err_files = [r for r in results if r.status == "ERROR"]
    sec_files = [r for r in results if r.security_issues]
    sec_critical = [r for r in results if r.security_status == "CRITICAL"]

    print(f"\n{'─'*62}")
    print(f"   📊 РЕЗУЛЬТАТИ АУДИТУ ЯКОСТІ:")
    print(f"{'─'*62}")
    print(f"   Всього файлів:    {len(results)}")
    print(f"   ✅ Чисті:          {len(ok_files)}")
    print(f"   ⚠️  Попередження:  {len(warn_files)}")
    print(f"   ❌ Помилки:        {len(err_files)}")

    print(f"\n{'─'*62}")
    print(f"   🔐 РЕЗУЛЬТАТИ SECURITY AUDIT:")
    print(f"{'─'*62}")
    print(f"   Файлів з вразливостями: {len(sec_files)}")
    print(f"   🔴 Критичних:           {len(sec_critical)}")

    if sec_critical:
        print(f"\n   🔴 КРИТИЧНІ ВРАЗЛИВОСТІ:")
        for r in sec_critical:
            for issue in r.security_issues:
                if issue.severity == "ERROR":
                    print(f"      [{r.rel_path}:{issue.line}] {issue.code}")
                    print(f"        └─ {issue.message[:80]}")

    reporter = HtmlReporter()
    reporter.generate(results, OUTPUT_HTML)
    print(f"\n{'─'*62}")
    print(f"   📄 HTML-Звіт: {OUTPUT_HTML}")
    print(f"   🔐 Security фільтр є в HTML-звіті!")
    print(f"{'─'*62}\n")


if __name__ == "__main__":
    main()
