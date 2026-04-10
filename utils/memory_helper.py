"""
memory_helper.py — Інструменти моніторингу та автоматичного керування пам'яттю.
"""
import gc
import os
import logging
import pandas as pd
import psutil
import streamlit as st

logger = logging.getLogger(__name__)

# Поріг автоматичного очищення кешу (MB)
AUTO_GC_THRESHOLD_MB = 380


def get_memory_usage() -> float:
    """Повертає споживання RAM поточним процесом у MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)


def get_top_objects() -> list:
    """Аналізує st.session_state та повертає топ-3 великих об'єкти."""
    sizes = []
    if "boot_data" in st.session_state:
        data = st.session_state["boot_data"]
        for k, v in data.items():
            if isinstance(v, pd.DataFrame):
                mem = v.memory_usage(deep=True).sum() / (1024 * 1024)
                sizes.append((f"DF:{k}", round(mem, 2)))

    # Також перевіряємо інші DF в session_state
    for k, v in st.session_state.items():
        if isinstance(v, pd.DataFrame):
            mem = v.memory_usage(deep=True).sum() / (1024 * 1024)
            sizes.append((f"SS:{k}", round(mem, 2)))

    return sorted(sizes, key=lambda x: x[1], reverse=True)[:5]


def get_resource_status(limit_mb: float = 512) -> tuple:
    """Повертає статус споживання ресурсів та топ-об'єкти."""
    usage = get_memory_usage()
    percent = (usage / limit_mb) * 100
    top = get_top_objects()

    if percent < 60:
        status, color = "🟢 Safe", "green"
    elif percent < 80:
        status, color = "🟡 Warning", "orange"
    else:
        status, color = "🔴 Critical", "red"

    return status, usage, color, top


def auto_gc(threshold_mb: float = AUTO_GC_THRESHOLD_MB) -> bool:
    """
    Автоматичне очищення пам'яті при перевищенні порогу.

    Повертає True якщо очищення було виконано.
    Викликається на початку кожного ререндеру в main.py.
    """
    usage = get_memory_usage()
    if usage > threshold_mb:
        logger.warning(
            f"🧹 AUTO-GC: Споживання {usage:.0f} MB > {threshold_mb} MB. "
            f"Очищення кешу та збір сміття..."
        )
        st.cache_data.clear()
        gc.collect()
        logger.info(f"✅ AUTO-GC: Після очищення: {get_memory_usage():.0f} MB")
        return True
    return False


def df_memory_report(df: pd.DataFrame, name: str = "DataFrame") -> str:
    """Повертає рядок зі статистикою пам'яті DataFrame."""
    total_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    per_col = df.memory_usage(deep=True) / (1024 * 1024)
    top_col = per_col.nlargest(3)
    detail = ", ".join(f"{c}={v:.2f}MB" for c, v in top_col.items() if c != "Index")
    return f"{name}: {total_mb:.2f} MB total ({len(df)} rows) | Top: {detail}"
