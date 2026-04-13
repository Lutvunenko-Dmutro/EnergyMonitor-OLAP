import os
import joblib
import logging
import onnxruntime as ort
from typing import Tuple, Optional, Any, Union, List
from pathlib import Path

DEFAULT_WINDOW_SIZE = 48  # Unified 48h look-back for final V3 stability
V1_DIPLOMA_FREEZE_LOCKED = True

# Динамічне визначення базового шляху до моделей (всередині src/ml/models)
BASE_MODELS_PATH = Path(__file__).parent / "models"

# Standardized Model Architecture Registry (Абсолютні шляхи)
MODEL_REGISTRY = {
    "v1": str(BASE_MODELS_PATH / "substation_model_v1.onnx"),
    "v2": str(BASE_MODELS_PATH / "substation_model_v2.onnx"),
    "v3": str(BASE_MODELS_PATH / "substation_model_v3_final.onnx"),
    "v3_checkpoint": str(BASE_MODELS_PATH / "checkpoints/best_v3.onnx")
}

SCALER_REGISTRY = {
    "v1": str(BASE_MODELS_PATH / "scaler_v1.pkl"),
    "v2": str(BASE_MODELS_PATH / "scaler_v2.pkl"),
    "v3": str(BASE_MODELS_PATH / "scaler_v3_final.pkl")
}

# Substation Identity Mapping
SUBSTATION_MAPPING = {
    "ПС Бровари": 0, "ПС Вінниця": 1, "ПС Дніпровська-750": 2,
    "ПС Запорізька": 3, "ПС Західна (Львів)": 4, "ПС Київська-Центральна": 5,
    "ПС Північна (Київ)": 6, "ПС Полтава-Центр": 7, "ПС Портова (Одеса)": 8,
    "ПС Слобожанська (Харків)": 9, "ПС Трипільська": 10, "ПС Черкаси": 11
}

logger = logging.getLogger(__name__)

# Environment-Aware Streamlit Caching
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

def st_cache_resource_fallback(show_spinner=True):
    """Conditional decorator for Streamlit caching with CLI fallback."""
    def decorator(func):
        if HAS_STREAMLIT:
            return st.cache_resource(show_spinner=show_spinner)(func)
        return func
    return decorator

from src.utils.error_handlers import robust_ml_handler

@st_cache_resource_fallback(show_spinner=False)
def _get_substation_peak_automated(name: Union[str, List[str]]) -> float:
    from src.core.database import run_query
    try:
        q_filter = "s.substation_name = ANY(:n)"
        q = f"""
            SELECT MAX(lm.actual_load_mw) as pk 
            FROM LoadMeasurements lm 
            JOIN Substations s ON lm.substation_id = s.substation_id 
            WHERE {q_filter}
        """
        df = run_query(q, {"n": name if isinstance(name, list) else [name]})
        pk = float(df["pk"].iloc[0]) if not df.empty and df["pk"].iloc[0] is not None else 1.0
            
        q2 = f"SELECT SUM(capacity_mw) as cap FROM Substations WHERE substation_name = ANY(:n)"
        df2 = run_query(q2, {"n": name if isinstance(name, list) else [name]})
        cap = float(df2["cap"].iloc[0]) if not df2.empty and df2["cap"].iloc[0] is not None else pk * 1.2
        
        return max(pk, cap * 0.4)
            
    except Exception as e:
        logger.warning(f"Automation peak fetch failed for {name}: {e}")
        
    return 5269.0 

@st_cache_resource_fallback(show_spinner="⏳ Loading AI Models...")
@robust_ml_handler
def load_resources(version: str = "v3") -> Tuple[Optional[ort.InferenceSession], Optional[Any]]:
    """Loads ONNX model and Joblib scaler with integrity checks."""
    m_path = MODEL_REGISTRY.get(version)
    s_path = SCALER_REGISTRY.get(version)

    if not m_path or not os.path.exists(m_path):
        if version == "v3": 
            m_path = MODEL_REGISTRY["v3_checkpoint"]
        else:
            logger.error(f"❌ Critical Model Path Missing for {version}")
            return None, None

    if not os.path.exists(m_path) or not os.path.exists(s_path):
        logger.error(f"❌ Model or Scaler file not found: {m_path}")
        return None, None

    try:
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        sess_options.intra_op_num_threads = 1
        sess_options.inter_op_num_threads = 1
        
        model = ort.InferenceSession(m_path, sess_options)
        scaler = joblib.load(s_path)
        
        # Verify scaler integrity (Check for expected attributes)
        if not hasattr(scaler, "mean_") and not hasattr(scaler, "data_max_"):
             logger.error("❌ Scaler object is corrupted or invalid.")
             return None, None

        logger.info(f"✅ AI Resources validated for {version}")
        return model, scaler
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI session: {e}")
        return None, None
