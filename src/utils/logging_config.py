# ═══════════════════════════════════════════════════════════════
# Logging Configuration for Energy Monitor Ultimate
# ═══════════════════════════════════════════════════════════════
"""
Централізована конфігурація для логування з file rotation.
Використовувати замість manuel logging setup у main.py.
"""

import logging
import logging.handlers
import os
from pathlib import Path
import sys


def setup_logging(
    log_level: str = "INFO",
    log_dir: str = "logs",
    log_file: str = "energy-monitor.log",
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    """Централізоване налаштування логування."""
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    logger = logging.getLogger("ENERGY_MONITOR")
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    logger.propagate = False
    logger.handlers.clear()
    
    # Реєстрація хендлерів через допоміжні функції
    logger.addHandler(_create_console_handler(level))
    logger.addHandler(_create_file_handler(log_path / log_file, max_bytes, backup_count))
    logger.addHandler(_create_error_handler(log_path / "energy-monitor.error.log", max_bytes, backup_count))
    logger.addHandler(_create_daily_handler(log_path / "energy-monitor-daily.log"))
    
    _log_startup_banner(logger, log_level, log_path, log_file)
    return logger


def _create_console_handler(level):
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] ⚡ %(levelname)-5s | %(name)s | %(message)s", datefmt="%H:%M:%S"
    ))
    return handler


def _create_file_handler(path, max_bytes, backup_count):
    handler = logging.handlers.RotatingFileHandler(
        filename=path, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    return handler


def _create_error_handler(path, max_bytes, backup_count):
    handler = logging.handlers.RotatingFileHandler(
        filename=path, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
    )
    handler.setLevel(logging.ERROR)
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d\n%(message)s\nTraceback: %(exc_info)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    return handler


def _create_daily_handler(path):
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=path, when="midnight", interval=1, backupCount=7, encoding='utf-8'
    )
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))
    return handler


def _log_startup_banner(logger, log_level, log_path, log_file):
    logger.info("=" * 60)
    logger.info("🚀 ENERGY MONITOR ULTIMATE: LOGGING INITIALIZED")
    logger.info(f"📝 Log Level: {log_level}")
    logger.info(f"📁 Log Directory: {log_path.absolute()}")
    logger.info(f"📄 Main Log File: {log_path / log_file}")
    logger.info("=" * 60)


# ───────────────────────────────────────────────────────────────
# INITIALIZATION
# ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Приклад використання:
    log = setup_logging(log_level="DEBUG")
    
    log.debug("Це DEBUG повідомлення")
    log.info("Це INFO повідомлення")
    log.warning("Це WARNING повідомлення")
    log.error("Це ERROR повідомлення")
    
    print("\n✅ Логування налаштовано. Перевір папку 'logs/'")
