import plotly.graph_objects as go
import numpy as np
import pandas as pd

def generate_academic_plots(data, substation_name="Selected Object"):
    """
    Універсальна функція для академічних графіків (Figure 5, 7, 8).
    Підтримує як одну модель (DataFrame), так і декілька (dict).
    """
    if data is None: return None, None, None
    
    # Конвертуємо одиночний DataFrame у словник для уніфікації логіки
    if isinstance(data, pd.DataFrame):
        results_dict = {"v1": data}
        is_multi = False
    else:
        results_dict = data
        is_multi = True

    if not results_dict: return None, None, None
    
    colors = {"v1": "#a29bfe", "v2": "#74b9ff", "v3": "#ff7675"}
    
    # 1. Figure 5: Temporal Load Dynamics (Trend Comparison)
    fig_trend = go.Figure()
    # Знаходимо перший доступний DF для отримання фактичних даних та позначок часу
    ref_v = next(iter(results_dict))
    ref_df = results_dict[ref_v]
    
    if ref_df is not None and not ref_df.empty:
        # Фактичні дані (Ground Truth)
        fig_trend.add_trace(go.Scatter(
            x=ref_df["timestamp"], y=ref_df["actual_load_mw"], 
            name="Actual (Факт)", line=dict(color="#ff9f43", width=3)
        ))
        
        # Прогнози всіх моделей
        for v, df in results_dict.items():
            if df is None or df.empty: continue
            fig_trend.add_trace(go.Scatter(
                x=df["timestamp"], y=df["predicted_load_mw"], 
                name=f"LSTM {v.upper()}", line=dict(color=colors.get(v, "#fff"), dash="dash" if is_multi else "solid")
            ))
            
    fig_trend.update_layout(
        template="plotly_dark", 
        title=dict(text=f"📉 Figure 5: Temporal Load Dynamics & Multi-Model Tracking", x=0.5, xanchor="center"),
        xaxis_title="Час (Last 7 Days)", yaxis_title="МВт",
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
        margin=dict(l=10, r=10, t=50, b=100), height=500
    )

    # 2. Figure 7: Distribution (Histogram)
    fig_dist = go.Figure()
    for v, df in results_dict.items():
        if df is None or df.empty: continue
        err = df["actual_load_mw"] - df["predicted_load_mw"]
        
        # Гістограма (робимо фоновою, ледь помітною)
        fig_dist.add_trace(go.Histogram(
            x=err, nbinsx=40, histnorm='probability density', 
            name=f"LSTM {v.upper()}", marker_color=colors.get(v, "#fff"),
            opacity=0.2, legendgroup=v, showlegend=False
        ))
        
        # Лінія розподілу (головний акцент)
        import scipy.stats as stats
        mu, std = err.mean(), err.std()
        xr = np.linspace(err.min(), err.max(), 100)
        fig_dist.add_trace(go.Scatter(
            x=xr, y=stats.norm.pdf(xr, mu, std), 
            name=f"Модель {v.upper()}", 
            line=dict(color=colors.get(v, "#fff"), width=4),
            legendgroup=v
        ))
    
    fig_dist.update_layout(
        template="plotly_dark", 
        title=dict(text=f"📊 Figure 7: Comparative Statistical Error Analysis", x=0.5, xanchor="center"),
        barmode='overlay', xaxis_title="Відхилення (МВт)", yaxis_title="Щільність розподілу",
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
        margin=dict(l=10, r=10, t=50, b=100), height=500
    )

    # 3. Figure 8: Scatter (Regression)
    fig_scatter = go.Figure()
    if ref_df is not None and not ref_df.empty:
        mn, mx = ref_df["actual_load_mw"].min(), ref_df["actual_load_mw"].max()
        fig_scatter.add_trace(go.Scatter(
            x=[mn, mx], y=[mn, mx], mode="lines", name="Ideal (y=x)",
            line=dict(color="rgba(255,255,255,0.2)", dash="dash")
        ))
    
    for v, df in results_dict.items():
        if df is None or df.empty: continue
        title_v = f"Pred {v.upper()}" if is_multi else "AI Regression"
        fig_scatter.add_trace(go.Scatter(
            x=df["actual_load_mw"], y=df["predicted_load_mw"], 
            mode="markers", name=title_v,
            marker=dict(opacity=0.5, size=6, color=colors.get(v, "#fff"))
        ))
        
    fig_scatter.update_layout(
        template="plotly_dark", 
        title=dict(text=f"🔵 Figure 8: Neural Regression Correlation ({substation_name})", x=0.5, xanchor="center"),
        xaxis_title="Actual Data (Ground Truth)",
        yaxis_title="Neural Predictions",
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
        margin=dict(l=10, r=10, t=50, b=100), height=550
    )
    
    return fig_trend, fig_dist, fig_scatter
