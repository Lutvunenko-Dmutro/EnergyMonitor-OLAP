# ATLAS_PASSPORT: docs/system/map/scanner.md
"""
🔍 SYSTEM AUDIT SCANNER (Deep Code Inspector).
py | Версія: 2.5.0 "DeepScan"
Призначення: Рекурсивний аудит кодової бази на базі Abstract Syntax Tree (AST) та евристичних алгоритмів оцінки якості.

Ключові можливості:
- 🏗️ AST Structural Analysis: Глибока перевірка синтаксису та архітектурних зв'язків.
- 🚚 Import Sentinel: Верифікація ланцюжків залежностей та виявлення відсутніх модулів.
- 📏 Heuristic Quality Control: Розумна оцінка довжини функцій з урахуванням контексту (UI vs Core).
- 🛡️ Security Audit: Багаторівневий пошук вразливостей через інтегровані паттерни.
"""
import os
import ast
import re
import importlib.util
from pathlib import Path
from .models import FileDiag, FunctionDiag, DiagIssue
from .patterns import (
    SCAN_DIRS, EXCLUDE_DIRS, STDLIB_MODULES, KNOWN_THIRD_PARTY,
    ALLOWED_TOP_LEVEL_CALLS, SECURITY_PATTERNS,
    LONG_FUNCTION_THRESHOLD_UI, LONG_FUNCTION_THRESHOLD_DEFAULT
)

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
                    parts = list(f.relative_to(self.root).with_suffix("").parts)
                    for i in range(len(parts)): local.add(".".join(parts[i:]))
        for f in self.root.glob("*.py"): local.add(f.stem)
        return local

    def scan_all(self):
        py_files = []
        for scan_dir in SCAN_DIRS:
            d = self.root / scan_dir
            if d.exists():
                for f in d.rglob("*.py"):
                    if not any(ex in f.parts for ex in EXCLUDE_DIRS): py_files.append(f)
        for f in self.root.glob("*.py"):
            if f.name not in {"diagnose.py", "refactor_run.py"}: py_files.append(f)

        print(f"\n🔍 Scanning {len(py_files)} files...")
        for fpath in sorted(py_files):
            self.results.append(self._analyze_file(fpath))

    def _analyze_file(self, fpath: Path) -> FileDiag:
        rel = str(fpath.relative_to(self.root))
        diag = FileDiag(path=fpath, rel_path=rel, syntax_ok=False)
        try:
            source = fpath.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source, filename=str(fpath))
            diag.syntax_ok = True
            diag.imports, diag.missing_imports = self._check_imports(tree, fpath)
            diag.functions = self._check_functions(tree, fpath)
            diag.file_issues += self._check_file_patterns(tree, source)
            diag.security_issues = self._check_security(source, fpath)
        except SyntaxError as e: diag.syntax_error = f"L{e.lineno}: {e.msg}"
        except Exception as e: diag.file_issues.append(DiagIssue("ERROR", "SCAN_ERR", str(e)))
        return diag

    def _check_imports(self, tree, fpath):
        imports, missing = [], []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    base = alias.name.split(".")[0]
                    if not self._is_known(base, fpath): missing.append(f"import {alias.name} (L{node.lineno})")
            elif isinstance(node, ast.ImportFrom) and node.module:
                base = node.module.split(".")[0]
                if not self._is_known(base, fpath): missing.append(f"from {node.module} (L{node.lineno})")
        return imports, missing

    def _is_known(self, name, fpath):
        return name in STDLIB_MODULES or name in KNOWN_THIRD_PARTY or name in self._available_modules or importlib.util.find_spec(name)

    def _check_functions(self, tree, fpath):
        funcs = []
        is_ui = "ui" in str(fpath).lower()
        threshold = LONG_FUNCTION_THRESHOLD_UI if is_ui else LONG_FUNCTION_THRESHOLD_DEFAULT
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                lines = node.end_lineno - node.lineno + 1
                f_diag = FunctionDiag(node.name, node.lineno, lines)
                if lines > threshold:
                    f_diag.issues.append(DiagIssue("WARNING", "LONG_FN", f"Function too long ({lines} lines)", node.lineno))
                funcs.append(f_diag)
        return funcs

    def _check_file_patterns(self, tree, source):
        issues = []
        lines = source.splitlines()
        has_main = any("__name__" in l and "__main__" in l for l in lines)
        for i, line in enumerate(lines, 1):
            if "print(" in line and not line.strip().startswith("#"):
                issues.append(DiagIssue("INFO", "PRINT", "Found print() statement", i))
        return issues

    def _check_security(self, source, fpath):
        issues = []
        lines = source.splitlines()
        for pattern, severity, code, message in SECURITY_PATTERNS:
            for i, line in enumerate(lines, 1):
                if not line.strip().startswith("#") and re.search(pattern, line, re.I):
                    issues.append(DiagIssue(severity, code, message, i, "security"))
        return issues
