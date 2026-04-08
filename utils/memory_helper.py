import os
import psutil
import sys
import pandas as pd
import streamlit as st

def get_memory_usage():
    """Повертає споживання RAM поточним процесом у MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def get_top_objects():
    """Аналізує st.session_state та повертає топ-3 великих об'єкти."""
    sizes = []
    if "boot_data" in st.session_state:
        data = st.session_state["boot_data"]
        for k, v in data.items():
            if isinstance(v, pd.DataFrame):
                mem = v.memory_usage(deep=True).sum() / (1024 * 1024)
                sizes.append((f"DF:{k}", mem))
    
    return sorted(sizes, key=lambda x: x[1], reverse=True)[:3]

def get_resource_status(limit_mb=512):
    """Повертає статус споживання ресурсів та топ-об'єкти."""
    usage = get_memory_usage()
    percent = (usage / limit_mb) * 100
    top = get_top_objects()
    
    status = "🟢 Safe" if percent < 70 else "🟡 Warning" if percent < 90 else "🔴 Critical"
    color = "green" if percent < 70 else "orange" if percent < 90 else "red"
    
    return status, usage, color, top
