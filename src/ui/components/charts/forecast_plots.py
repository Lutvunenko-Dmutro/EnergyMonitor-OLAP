import pandas as pd
import plotly.graph_objects as go

def _generate_forecast_figure(df_hist, df_fc, title, version_lbl):
    fig = go.Figure()
    if not df_hist.empty and "actual_load_mw" in df_hist.columns:
        fig.add_trace(go.Scatter(
            x=df_hist["timestamp"], y=df_hist["actual_load_mw"], name="Історія", line=dict(color="#3498db", width=2.5)
        ))
    
    if not df_fc.empty and "upper_bond" in df_fc.columns:
        h_max = df_hist["actual_load_mw"].max() if not df_hist.empty else 0
        p_max = df_fc["predicted_load_mw"].max()
        safe_upper = df_fc["upper_bond"].clip(upper=max(h_max, p_max) * 1.5)
        fig.add_trace(go.Scatter(
            x=pd.concat([df_fc["timestamp"], df_fc["timestamp"][::-1]]), 
            y=pd.concat([safe_upper, df_fc["lower_bond"][::-1]]), 
            fill="toself", fillcolor="rgba(231,76,60,0.08)", line=dict(color="rgba(0,0,0,0)"), showlegend=False
        ))

    if not df_fc.empty:
        fig.add_trace(go.Scatter(
            x=df_fc["timestamp"], y=df_fc["predicted_load_mw"], name=f"Прогноз ({version_lbl})", 
            line=dict(color="#e74c3c", width=2.5, dash="dash")
        ))
    
    fig.update_layout(template="plotly_dark", height=500, hovermode="x unified", title=title)
    return fig

def _generate_multi_forecast_figure(df_hist, results: dict, title):
    fig = go.Figure()
    if not df_hist.empty:
        fig.add_trace(go.Scatter(x=df_hist["timestamp"], y=df_hist["actual_load_mw"], name="Історія", line=dict(color="#3498db", width=3)))
    
    styles = {"v1": dict(color="#00cec9", width=2, dash="dot"), "v2": dict(color="#0984e3", width=2, dash="dash"), "v3": dict(color="#d63031", width=3.5)}
    for version, df_fc in results.items():
        if df_fc is not None and not df_fc.empty:
            fig.add_trace(go.Scatter(x=df_fc["timestamp"], y=df_fc["predicted_load_mw"], name=f"Прогноз {version.upper()}", line=styles.get(version, {})))

    fig.update_layout(
        template="plotly_dark", 
        height=550, 
        title=dict(text=title, x=0.5, xanchor="center"),
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
        margin=dict(l=10, r=10, t=60, b=80)
    )
    return fig

def generate_comparison_plot(results: dict, substation_name: str) -> go.Figure:
    """Creates a unified Plotly chart showing Actuals + V1/V2/V3 Predictions for Audit."""
    fig = go.Figure()
    if not results: return fig
    
    first_df = next(iter(results.values()))
    fig.add_trace(go.Scatter(
        x=first_df["timestamp"], y=first_df["actual_load_mw"],
        name="Фактичне навантаження (Ground Truth)",
        line=dict(color="#ff9f43", width=3)
    ))
    
    styles = {
        "v1": dict(color="#00d2d3", width=2, dash="dot"),
        "v2": dict(color="#54a0ff", width=2, dash="dash"),
        "v3": dict(color="#ee5253", width=3, dash="solid")
    }
    labels = {
        "v1": "LSTM Baseline (V1)", "v2": "LSTM Diagnostic (V2)", "v3": "LSTM Hybrid (V3) ⭐"
    }
    
    for version, df in results.items():
        if df is None or df.empty: continue
        fig.add_trace(go.Scatter(
            x=df["timestamp"], y=df["predicted_load_mw"],
            name=labels.get(version, f"Model {version.upper()}"),
            line=styles.get(version, dict(color="#fff", width=1))
        ))
        
    fig.update_layout(
        template="plotly_dark", 
        title=dict(text=f"📊 Порівняльна відповідність нейромереж ({substation_name})", x=0.5, xanchor="center"),
        xaxis_title="Час (Last 7 Days)", 
        yaxis_title="МВт", 
        hovermode="x unified",
        margin=dict(l=10, r=10, t=80, b=100),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center")
    )
    return fig

def _generate_mega_hybrid_figure(df_bt, df_fc, title, version_lbl):
    fig = go.Figure()
    if df_bt is not None and not df_bt.empty:
        fig.add_trace(go.Scatter(x=df_bt["timestamp"], y=df_bt["actual_load_mw"], name="Actual", line=dict(color="#ffa502")))
        fig.add_trace(go.Scatter(x=df_bt["timestamp"], y=df_bt["predicted_load_mw"], name="Backtest", line=dict(color="#ee5253")))
    if df_fc is not None and not df_fc.empty:
        fig.add_trace(go.Scatter(x=df_fc["timestamp"], y=df_fc["predicted_load_mw"], name="Live Forecast", line=dict(color="#ee5253", dash="dash")))
    fig.update_layout(template="plotly_dark", height=500, title=title)
    return fig
