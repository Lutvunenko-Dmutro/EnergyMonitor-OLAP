import os

print("Починаю рефакторинг: вилучення графічної логіки...")

# 1. Update forecast.py
with open("ui/views/forecast.py", "r", encoding="utf-8") as f:
    fc_lines = f.readlines()

new_fc_lines = []
skip = False
mega_code = ""
forecast_fig_code = ""

for line in fc_lines:
    if line.startswith("def _cached_ai_forecast"): skip = True
    if line.startswith("def _generate_mega_hybrid_figure"): skip = True
    if line.startswith("def _render_comparative_audit"): skip = False
    if line.startswith("def _generate_forecast_figure"): skip = True
    if line.startswith("def render("): skip = False

    if line.startswith("def _generate_mega_hybrid_figure") or (skip and mega_code != "" and forecast_fig_code == ""):
        if line.startswith("def _generate_forecast_figure"):
            pass
        elif not line.startswith("def _render_comparative_audit") and "def _generate_mega_hybrid_figure" in mega_code or line.startswith("def _generate_mega_hybrid_figure"):
            # Mega hybrid figure collects here
            pass
            
# A better way is using known line indices from the analysis
cache_idx = fc_lines.index('def _cached_ai_forecast(hours_ahead, substation_name, source_type, version, scenario):\n') - 1 # include @st.cache_data
mega_idx = fc_lines.index('def _generate_mega_hybrid_figure(df_bt, df_fc, title, version_lbl):\n')
render_comp_idx = fc_lines.index('def _render_comparative_audit(substation_name, source_type):\n')
forecast_fig_idx = fc_lines.index('def _generate_forecast_figure(df_hist, df_fc, title, version_lbl):\n')
render_idx = fc_lines.index('def render(selected_substation="Усі підстанції", data_source="Live"):\n')

mega_code = "".join(fc_lines[mega_idx:render_comp_idx])
forecast_fig_code = "".join(fc_lines[forecast_fig_idx:render_idx])

# Now construct the new forecast.py
new_fc_lines = fc_lines[:cache_idx]
new_fc_lines.append("from ml.forecast_controller import cached_ai_forecast as _cached_ai_forecast\n")
new_fc_lines.append("from ml.forecast_controller import cached_fast_backtest as _cached_fast_backtest\n")
new_fc_lines.append("from ml.forecast_controller import get_cached_history as _get_history\n")
new_fc_lines.append("from ml.forecast_controller import calculate_instant_metrics as _calculate_instant_metrics\n")
new_fc_lines.append("from ui.components.charts import _generate_mega_hybrid_figure, _generate_forecast_figure\n\n")

new_fc_lines.extend(fc_lines[render_comp_idx:forecast_fig_idx])
new_fc_lines.extend(fc_lines[render_idx:])

with open("ui/views/forecast.py", "w", encoding="utf-8") as f:
    f.writelines(new_fc_lines)

# 2. Update ml/backtest.py
with open("ml/backtest.py", "r", encoding="utf-8") as f:
    bt_lines = f.readlines()

academic_idx = bt_lines.index('def generate_academic_plots(df: pd.DataFrame) -> Tuple[Optional[go.Figure], Optional[go.Figure], Optional[go.Figure]]:\n')
run_backtest_idx = bt_lines.index('@robust_ml_handler\n') # Finding evaluate_last_24h basically
end_comp_idx = next(i for i, line in enumerate(bt_lines) if "def evaluate_last_24h" in line) - 3 # To include the # ====== header

plots_code = "".join(bt_lines[academic_idx:end_comp_idx])

# keep the statistical header and perform_statistical_audit
new_bt_lines = bt_lines[:academic_idx]
new_bt_lines.extend(bt_lines[end_comp_idx:])

with open("ml/backtest.py", "w", encoding="utf-8") as f:
    f.writelines(new_bt_lines)

# 3. Append to charts.py
with open("ui/components/charts.py", "a", encoding="utf-8") as f:
    f.write("\n\n")
    f.write("import scipy.stats as stats\n")
    f.write("import numpy as np\n")
    f.write("from typing import Tuple, Optional\n")
    f.write("from sklearn.metrics import r2_score\n")
    f.write("from ml.backtest import perform_statistical_audit\n\n")
    f.write(plots_code)
    f.write("\n")
    f.write(mega_code)
    f.write("\n")
    f.write(forecast_fig_code)

print("Рефакторинг успішно завершено! Логіку рознесено по модулях.")
