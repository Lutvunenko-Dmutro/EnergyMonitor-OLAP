"""
Cache Manager — TTL-based automatic cache cleanup utility.

Видаляє застарілі файли з папки cache/ при кожному запуску.
Зберігає .graphml файли (карти) як "постійний" кеш.
"""

import logging
import os
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Константи
CACHE_DIR = Path("cache")
DEFAULT_TTL_HOURS: int = 24
PROTECTED_EXTENSIONS: set[str] = {".graphml"}  # Файли карт — не видаляємо


def clean_cache(ttl_hours: int = DEFAULT_TTL_HOURS) -> dict[str, int]:
    """
    Видаляє JSON-файли кешу, що старіші за ttl_hours годин.

    Args:
        ttl_hours: Вік файлу в годинах, після якого він вважається застарілим.

    Returns:
        dict з ключами 'deleted', 'skipped', 'errors' та кількістю файлів.
    """
    result: dict[str, int] = {"deleted": 0, "skipped": 0, "errors": 0}

    if not CACHE_DIR.exists():
        logger.debug("Cache directory not found, skipping cleanup.")
        return result

    now = time.time()
    ttl_seconds = ttl_hours * 3600

    for file_path in CACHE_DIR.iterdir():
        if not file_path.is_file():
            continue

        # Захищаємо карти та інші не-JSON файли
        if file_path.suffix.lower() in PROTECTED_EXTENSIONS:
            result["skipped"] += 1
            continue

        try:
            file_age = now - file_path.stat().st_mtime
            if file_age > ttl_seconds:
                file_path.unlink()
                result["deleted"] += 1
                logger.debug(f"🗑️ Видалено застарілий кеш: {file_path.name}")
            else:
                result["skipped"] += 1
        except OSError as e:
            logger.warning(f"⚠️ Не вдалося видалити {file_path.name}: {e}")
            result["errors"] += 1

    if result["deleted"] > 0:
        logger.info(
            f"🧹 Cache cleanup: видалено {result['deleted']} файлів, "
            f"збережено {result['skipped']}, помилок {result['errors']}."
        )
    else:
        logger.debug(f"✅ Кеш чистий (перевірено {result['skipped']} файлів).")

    return result


def get_cache_stats() -> dict[str, int | float]:
    """
    Повертає статистику поточного стану кешу.

    Returns:
        dict з 'total_files', 'total_size_mb', 'json_files', 'graphml_files'.
    """
    if not CACHE_DIR.exists():
        return {"total_files": 0, "total_size_mb": 0.0, "json_files": 0, "graphml_files": 0}

    total_size = 0
    json_count = 0
    graphml_count = 0
    total_count = 0

    for file_path in CACHE_DIR.iterdir():
        if not file_path.is_file():
            continue
        total_count += 1
        total_size += file_path.stat().st_size
        if file_path.suffix.lower() == ".json":
            json_count += 1
        elif file_path.suffix.lower() == ".graphml":
            graphml_count += 1

    return {
        "total_files": total_count,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "json_files": json_count,
        "graphml_files": graphml_count,
    }


def startup_cache_cleanup(ttl_hours: int = DEFAULT_TTL_HOURS) -> None:
    """
    Виклик при запуску додатка. Виконує очищення і логує результат.
    Не кидає винятків — будь-які помилки логуються тихо.

    Args:
        ttl_hours: Вік файлу в годинах для видалення.
    """
    try:
        stats_before = get_cache_stats()
        result = clean_cache(ttl_hours=ttl_hours)

        if result["deleted"] > 0:
            stats_after = get_cache_stats()
            freed_mb = stats_before["total_size_mb"] - stats_after["total_size_mb"]
            logger.info(
                f"🧹 Cache TTL cleanup завершено. "
                f"Видалено: {result['deleted']} файлів ({freed_mb:.1f} МБ звільнено)."
            )
    except Exception as e:
        # Ніколи не ламаємо запуск через помилку в очищенні кешу
        logger.warning(f"⚠️ Cache cleanup failed silently: {e}")
