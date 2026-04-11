import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ml.backtest import get_backtest_metrics
from src.core.logger import setup_logger

logger = setup_logger(__name__)

substation = "ПС Бровари"

for v in ["v1", "v2", "v3"]:
    print(f"\n--- 📊 Оцінка для версії {v.upper()} ---")
    mape, err = get_backtest_metrics(version=v, substation_name=substation)
    if err:
        print(f"Error {v}: {err}")
