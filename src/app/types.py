# ═══════════════════════════════════════════════════════════════
# Type Definitions for Energy Monitor Ultimate
# ═══════════════════════════════════════════════════════════════
"""
Централізовані type hints та custom types для проекту.
Використовуй ці типи в усіх функціях для консистентності.
"""

from typing import Dict, List, Tuple, Optional, Union
from datetime import date, datetime
import pandas as pd

# ───────────────────────────────────────────────────────────────
# DATA STRUCTURES
# ───────────────────────────────────────────────────────────────

# Database/DataFrame types
DataDict = Dict[str, pd.DataFrame]
"""Словник з DataFrames (load, gen, alerts, lines, fin)"""

DateRange = Tuple[date, date]
"""Кортеж дат (start_date, end_date)"""

SubstationSelection = Union[str, List[str]]
"""Одна підстанція або список підстанцій"""

RegionName = str
"""Назва регіону"""

# ───────────────────────────────────────────────────────────────
# MODEL OUTPUTS
# ───────────────────────────────────────────────────────────────

PredictionResult = Dict[str, Union[pd.DataFrame, float, dict]]
"""Результат LSTM prediction {forecast: df, rmse: float, metadata: dict}"""

MetricsDict = Dict[str, float]
"""Словник метрик {accuracy: 0.95, mse: 0.001, mae: 0.01}"""

AlertData = Dict[str, Union[str, float, bool]]
"""Інформація про алерт {substation, level, severity, timestamp}"""

# ───────────────────────────────────────────────────────────────
# FILTER & QUERY PARAMETERS
# ───────────────────────────────────────────────────────────────

FilterParams = Dict[str, Union[str, DateRange, List[str], None]]
"""Параметри фільтрації {region, dates, substation, data_source}"""

QueryResult = Union[pd.DataFrame, dict, None]
"""Результат DB query: DataFrame або помилка"""

# ───────────────────────────────────────────────────────────────
# CONFIG & STATUS
# ───────────────────────────────────────────────────────────────

BootData = Dict[str, Union[pd.DataFrame, str, int]]
"""Дані з boot sequence {data: dict, status: str, progress: int}"""

HealthStatus = Dict[str, Union[float, str, bool]]
"""Статус здоров'я системи {cpu: 0.45, memory: 0.65, db_healthy: True}"""
