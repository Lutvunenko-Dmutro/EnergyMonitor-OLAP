import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats
from sklearn.metrics import r2_score
from src.ml.backtest import perform_statistical_audit

def generate_academic_plots(df):
    """Figure 5, 7, 8 for diploma defense."""
    if df.empty: return None, None, None
    actual, pred_lstm = df["actual_load_mw"], df["predicted_load_mw"]
    
    # 1. Figure 5: Trend
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df["timestamp"], y=actual, name="Actual", line=dict(color="#ff9f43")))
    fig_trend.add_trace(go.Scatter(x=df["timestamp"], y=pred_lstm, name="LSTM Forecast", line=dict(color="#ee5253")))
    fig_trend.update_layout(template="plotly_dark", title="📉 Figure 5: Temporal Load Dynamics")

    # 2. Figure 7: Distribution
    fig_dist = go.Figure()
    audit = perform_statistical_audit(actual - pred_lstm)
    mu, std = audit.get("mu", 0), audit.get("sigma", 1)
    fig_dist.add_trace(go.Histogram(x=actual-pred_lstm, nbinsx=50, histnorm='probability density', marker_color="#a29bfe"))
    xr = np.linspace(min(actual-pred_lstm), max(actual-pred_lstm), 100)
    fig_dist.add_trace(go.Scatter(x=xr, y=stats.norm.pdf(xr, mu, std), line=dict(color="#6c5ce7", width=3)))
    fig_dist.update_layout(template="plotly_dark", title="📊 Figure 7: Statistical Audit")

    # 3. Figure 8: Scatter
    r2 = r2_score(actual, pred_lstm)
    fig_scatter = go.Figure()
    
    # Add 1:1 Reference Line for visual fidelity
    mn, mx = min(actual.min(), pred_lstm.min()), max(actual.max(), pred_lstm.max())
    fig_scatter.add_trace(go.Scatter(
        x=[mn, mx], y=[mn, mx], 
        mode="lines", name="Ideal (y=x)",
        line=dict(color="rgba(255,255,255,0.3)", dash="dash")
    ))
    
    fig_scatter.add_trace(go.Scatter(
        x=actual, y=pred_lstm, 
        mode="markers", name="Predictions",
        marker=dict(opacity=0.6, color="#74b9ff")
    ))
    
    fig_scatter.update_layout(
        template="plotly_dark", 
        title=f"🔵 Regression Fidelity Analysis (R2={r2:.4f})",
        xaxis_title="Actual Data (Ground Truth)",
        yaxis_title="Neural Prediction (LSTM)",
        showlegend=False
    )
    
    return fig_trend, fig_dist, fig_scatter
