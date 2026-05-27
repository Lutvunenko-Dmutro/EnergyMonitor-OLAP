# ATLAS_PASSPORT: docs/system/map/reporter.md
"""
📊 DIAGNOSTICS REPORTING ENGINE (Health Auditor).
py | Версія: 1.5.0
Призначення: Трансформація результатів технічного аудиту в інтерактивні HTML-звіти з використанням сучасних стандартів візуалізації.

Ключові можливості:
- 📊 State Aggregation: Підрахунок глобальних метрик здоров'я проєкту (OK/Warning/Error).
- 🎨 Visual Highlighting: Кольорова індикація проблем за рівнем критичності (GitHub-style).
- 🛡️ Security Focused reporting: Окреме виділення вразливостей безпеки.
- 📄 Automated Documentation: Формування автономного файлу diagnostics_report.html.
"""
from datetime import datetime
from pathlib import Path
from .models import FileDiag

class HtmlReporter:
    def generate(self, results: list[FileDiag], output: Path):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = len(results)
        ok = sum(1 for r in results if r.status == "OK")
        warn = sum(1 for r in results if r.status == "WARNING")
        err = sum(1 for r in results if r.status == "ERROR")
        sec_total = sum(len(r.security_issues) for r in results)

        rows = "".join([self._file_row(r) for r in sorted(results, key=lambda x: (x.status != "ERROR", x.rel_path))])
        
        html = f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<title>Energy Monitor Diagnostics</title>
<style>
  body {{ font-family: sans-serif; background: #0d1117; color: #c9d1d9; padding: 2rem; }}
  .stat-card {{ display: inline-block; background: #161b22; border: 1px solid #30363d; padding: 1rem; margin-right: 1rem; border-radius: 8px; min-width: 120px; text-align: center; }}
  .num {{ font-size: 1.5rem; font-weight: bold; display: block; }}
  .file-card {{ background: #161b22; border: 1px solid #30363d; margin: 10px 0; padding: 10px; border-radius: 6px; }}
  .status-ERROR {{ border-left: 4px solid #f85149; }}
  .status-WARNING {{ border-left: 4px solid #d29922; }}
  .status-OK {{ border-left: 4px solid #3fb950; }}
  .issue-item {{ font-size: 0.85rem; margin: 5px 0; color: #8b949e; }}
  .sev-ERROR {{ color: #f85149; font-weight: bold; }}
</style>
</head>
<body>
<h1>⚡ Energy Monitor — Diagnostics Report</h1>
<div class="stats">
  <div class="stat-card"> <span class="num">{total}</span> Files </div>
  <div class="stat-card"> <span class="num" style="color:#3fb950">{ok}</span> Clean </div>
  <div class="stat-card"> <span class="num" style="color:#f85149">{err}</span> Errors </div>
  <div class="stat-card"> <span class="num" style="color:#bd93f9">{sec_total}</span> Security </div>
</div>
<div class="results">{rows}</div>
</body></html>"""
        output.write_text(html, encoding="utf-8")

    def _file_row(self, r: FileDiag):
        issues_html = "".join([f'<div class="issue-item"><b class="sev-{i.severity}">{i.severity}</b>: {i.message} (L{i.line})</div>' for i in r.file_issues + r.security_issues])
        return f'<div class="file-card status-{r.status}"><b>{r.rel_path}</b> {issues_html}</div>'
