from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path

@dataclass
class DiagIssue:
    severity: str   # "ERROR" | "WARNING" | "INFO"
    code: str
    message: str
    line: Optional[int] = None
    category: str = "quality"

@dataclass
class FunctionDiag:
    name: str
    lineno: int
    lines: int = 0
    issues: List[DiagIssue] = field(default_factory=list)

    @property
    def status(self):
        if any(i.severity == "ERROR" for i in self.issues): return "ERROR"
        if any(i.severity == "WARNING" for i in self.issues): return "WARNING"
        return "OK"

@dataclass
class FileDiag:
    path: Path
    rel_path: str
    syntax_ok: bool
    syntax_error: Optional[str] = None
    imports: List[str] = field(default_factory=list)
    missing_imports: List[str] = field(default_factory=list)
    functions: List[FunctionDiag] = field(default_factory=list)
    file_issues: List[DiagIssue] = field(default_factory=list)
    security_issues: List[DiagIssue] = field(default_factory=list)

    @property
    def status(self):
        if not self.syntax_ok or self.missing_imports: return "ERROR"
        if any(i.severity == "ERROR" for i in self.file_issues + self.security_issues): return "ERROR"
        all_fn_issues = [i for fn in self.functions for i in fn.issues]
        if any(i.severity in ("ERROR", "WARNING") for i in all_fn_issues + self.file_issues + self.security_issues): return "WARNING"
        return "OK"

    @property
    def total_issues(self):
        count = len(self.missing_imports) + len(self.file_issues) + len(self.security_issues)
        for fn in self.functions: count += len(fn.issues)
        return count

    @property
    def security_status(self):
        if any(i.severity == "ERROR" for i in self.security_issues): return "CRITICAL"
        if any(i.severity == "WARNING" for i in self.security_issues): return "RISK"
        return "SAFE"
