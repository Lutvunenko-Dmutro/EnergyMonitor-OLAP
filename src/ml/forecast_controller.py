# ATLAS_PASSPORT: docs/system/map/forecast_controller.md
"""
🚀 AI FORECAST ORCHESTRATOR (Execution & Caching Control).
=============================================================================
Модуль виступає диспетчером між UI-компонентами та ML-ядром системи.
Основні функції:
1. Neural Inference Orchestration: координація запусків нейронних мереж (V1-V3) залежно від контексту.
2. Scenario-based Simulation: адаптація прогнозів під користувацькі сценарії (температурні зсуви, стан обладнання).
3. Intelligent Caching: мінімізація надлишкових обчислень та запитів до БД через st.cache_data.
4. Instant Accuracy Audit: миттєва верифікація моделі на останньому зрізі історії для формування довірчих інтервалів.
Забезпечує високу швидкість відгуку аналітичного дашборду при складних ШІ-обчисленнях.
"""
import streamlit as st
import pandas as pd
from src.ml.predict_v2 import get_ai_forecast
from src.ml.backtest import get_fast_backtest, evaluate_last_24h

@st.cache_data(ttl=3600, show_spinner="🧠 Neural Inference (Vectorized)...")
def cached_ai_forecast(hours_ahead, substation_name, source_type, version, scenario):
    """Cached wrapper for ML inference to prevent redundant re-computation."""
    # Захист від некоректного типу даних сценарію
    if not isinstance(scenario, dict):
        scenario = {"air_temp": 15, "health_score": 100}
        
    temp_s = scenario.get("air_temp", 15) - 15 # Зсув відносно норми (15C)
    consts = {"health": scenario.get("health_score", 100)}
    
    return get_ai_forecast(
        hours_ahead=hours_ahead, 
        substation_name=substation_name, 
        source_type=source_type, 
        version=version, 
        temp_shift=temp_s,
        constants=consts
    )

@st.cache_data(ttl=3600, show_spinner="📊 Batch Auditing System Accuracy...")
def cached_fast_backtest(substation_name, version, source_type):
    """Cached wrapper for full-period backtesting to prevent redundant DB sweeps."""
    return get_fast_backtest(substation_name, version, source_type)

@st.cache_data(ttl=600, show_spinner=False)
def get_cached_history(sub, src):
    if src == "Kaggle" or src == "CSV":
        from src.core.analytics.aggregator import get_history_csv
        return get_history_csv(sub)
    from src.core.analytics.aggregator import get_history_live
    return get_history_live(sub)

def calculate_instant_metrics(df_hist, version, sub_name, src_type):
    """
    Проводить миттєву перевірку моделі на останніх 24 годинах історії.
    Повертає сукупні метрики та оцінку sigma для довірчих інтервалів.
    """
    metrics = evaluate_last_24h(sub_name, version, src_type)
    
    if metrics:
        sigma = metrics.pop("sigma", 0.05)
        return metrics, sigma
    
    return None, 0.05
