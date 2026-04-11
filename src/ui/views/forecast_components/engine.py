import streamlit as st
from src.ui.views.forecast_components.constants import MODEL_LABELS
from src.ml.forecast_controller import cached_ai_forecast as _cached_ai_forecast
from src.ml.forecast_controller import get_cached_history as _get_history

def run_reactive_forecast_engine(sub_name, sub_id_for_hero, version, src_type, scenario, is_multi_model):
    """
    Core logic for calculating forecasts (single or multi-model) reactively.
    Returns results for hero chart and grid processing indicators.
    """
    multi_hero = {}
    res_fc = None
    multi_results = None
    
    # 1. Multi-Model Path
    if is_multi_model:
        v_list = ["v1", "v2", "v3"]
        for v in v_list:
            res_g = _cached_ai_forecast(
                hours_ahead=24, substation_name=sub_id_for_hero, 
                source_type=src_type, version=v, scenario=scenario
            )
            if res_g: multi_hero[v] = res_g[0]
        
        # If it's a single substation comparison
        if not (sub_name == "Усі підстанції" or isinstance(sub_name, list) and len(sub_name) > 1):
             multi_results = multi_hero
    
    # 2. Single Model Path
    else:
        res_fc = _cached_ai_forecast(
            hours_ahead=24, substation_name=sub_id_for_hero, 
            source_type=src_type, version=version, scenario=scenario
        )
        
    return multi_hero, res_fc, multi_results

def get_stations_to_process(sub_name, src_type):
    """Helper to detect list of substations for grid rendering."""
    from src.core import database as db
    
    if sub_name == "Усі підстанції":
        if src_type == "CSV":
            from src.core.kaggle_loader import load_kaggle_data
            k_df = load_kaggle_data()
            return k_df["substation_name"].unique().tolist() if not k_df.empty else []
        else:
            sub_df = db.run_query("SELECT substation_name FROM Substations ORDER BY substation_name")
            return sub_df["substation_name"].tolist() if not sub_df.empty else []
    
    if isinstance(sub_name, list) and len(sub_name) > 1:
        return sub_name
        
    return []
