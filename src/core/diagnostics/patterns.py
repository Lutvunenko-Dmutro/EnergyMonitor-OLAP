import re
import sys
from pathlib import Path

# --- CONFIG ---
SCAN_DIRS = ["ui", "src", "core", "app", "utils", "ml"]
EXCLUDE_DIRS = {"__pycache__", ".git", "site", "node_modules", ".pytest_cache"}
STDLIB_MODULES = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else set()

KNOWN_THIRD_PARTY = {
    "streamlit", "pandas", "numpy", "plotly", "sqlalchemy", "psycopg2",
    "sklearn", "joblib", "scipy", "dotenv", "tornado", "requests",
    "altair", "pydeck", "folium", "statsmodels", "psutil", "matplotlib", "seaborn"
}

ALLOWED_TOP_LEVEL_CALLS = {
    "load_dotenv", "setup_logger", "getLogger", "basicConfig",
    "mkdir", "makedirs", "warn", "filterwarnings", "templates",
    "exists", "touch", "unlink",
}

LONG_FUNCTION_THRESHOLD_UI = 200
LONG_FUNCTION_THRESHOLD_DEFAULT = 100

# --- SECURITY PATTERNS ---
SECURITY_PATTERNS = [
    (r'(?:execute|run_query|cursor\.execute)\s*\([^)]*f["\'].*?\{', "ERROR", "SQL_INJECTION_FSTRING", "⛔ SQL Injection: f-string in SQL query."),
    (r'(?:execute|run_query)\s*\([^)]*%\s*[(\w]', "WARNING", "SQL_INJECTION_FORMAT", "⚠️ SQL Injection: % formatting in SQL."),
    (r'(?:password|passwd|secret|token|api_key|apikey)\s*=\s*["\'][^"\']{4,}["\']', "ERROR", "HARDCODED_SECRET", "🔑 Hardcoded secret in source!"),
    (r'\beval\s*\(|exec\s*\(', "ERROR", "DANGEROUS_EVAL", "☠️ Dangerous eval() or exec() usage."),
    (r'pickle\.load|yaml\.load\s*\([^)]*Loader', "WARNING", "UNSAFE_DESERIALIZATION", "⚠️ Unsafe deserialization detected."),
    (r'requests\.(get|post|put|delete|patch)\s*\([^)]*\)(?!.*timeout)', "WARNING", "MISSING_TIMEOUT", "⏱️ HTTP request without timeout."),
    (r'except\s+Exception[^:]*:\s*\n\s*pass', "WARNING", "SILENT_EXCEPTION", "🔇 Silent exception handler (pass)."),
    (r'postgresql://[^{}\s"\']{8,}', "ERROR", "EXPOSED_CONN_STRING", "🔑 Exposed DB connection string!"),
    (r'#\s*(TODO|FIXME|HACK|BUG|XXX)', "INFO", "TODO_MARKER", "📝 Found developer marker in comments."),
]
