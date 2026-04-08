import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _hex_to_rgb(hex_color: str) -> str:
    """Конвертує Hex у RGB стрічку для CSS."""
    h = hex_color.lstrip("#")
    return ",".join(str(int(h[i : i + 2], 16)) for i in (0, 2, 4))


def render_dual_axis_chart(
    df: pd.DataFrame,
    left_col: str,
    left_label: str,
    left_color: str,
    right_col: str,
    right_label: str,
    right_color: str,
    fill_left: bool = True,
) -> go.Figure:
    """
    Генерує двовісний графік з підтримкою автоматичного групування за підстанціями.
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    unique_subs = df["substation"].unique() if "substation" in df.columns else [None]
    is_multi = len(unique_subs) > 1

    for sub in unique_subs:
        sub_df = df[df["substation"] == sub] if sub is not None else df
        trace_name = str(sub) if sub is not None else left_label

        fig.add_trace(
            go.Scatter(
                x=sub_df["ts"],
                y=sub_df[left_col],
                name=f"{trace_name} ({left_label})" if is_multi else left_label,
                line=dict(color=left_color if not is_multi else None, width=2),
                fill="tozeroy" if fill_left and not is_multi else "none",
                fillcolor=f"rgba({_hex_to_rgb(left_color)},0.08)"
                if fill_left and not is_multi
                else None,
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=sub_df["ts"],
                y=sub_df[right_col],
                name=f"{trace_name} ({right_label})" if is_multi else right_label,
                line=dict(
                    color=right_color if not is_multi else None,
                    width=1.5,
                    dash="dot" if not is_multi else "solid",
                ),
            ),
            secondary_y=True,
        )

    fig.update_yaxes(title_text=left_label, secondary_y=False)
    fig.update_yaxes(title_text=right_label, secondary_y=True, showgrid=False)
    fig.update_layout(
        hovermode="x unified",
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", y=-0.18),
    )
    return fig


def render_forecast_chart(df_merged: pd.DataFrame, sub_label: str) -> go.Figure:
    """
    Побудова лінійного графіка історії та прогнозу МВт.
    """
    fig = px.line(
        df_merged,
        x="timestamp",
        y="actual_load_mw",
        color="type",
        color_discrete_map={"Історія": "#3b82f6", "Прогноз": "#ef4444"},
        title=f"📈 {sub_label}",
    )
    fig.update_layout(
        template="plotly_dark",
        height=320,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", y=-0.2, title_text=""),
        xaxis_title="",
        yaxis_title="МВт",
    )
    return fig


def render_rhythm_chart(df_rhythm: pd.DataFrame) -> go.Figure:
    """
    Будує ритмічний графік навантаження (Будні vs Вихідні).
    """
    fig_r = go.Figure()
    if df_rhythm.empty:
        return fig_r

    # Гарантуємо числовий тип
    df_r = df_rhythm.copy()
    df_r["dow"] = pd.to_numeric(df_r["dow"], errors="coerce")
    df_r["hour_of_day"] = pd.to_numeric(df_r["hour_of_day"], errors="coerce")
    df_r["avg_load"] = pd.to_numeric(df_r["avg_load"], errors="coerce")

    df_mon = df_r[df_r["dow"] == 1].sort_values("hour_of_day")
    df_sat = df_r[df_r["dow"] == 6].sort_values("hour_of_day")

    if not df_mon.empty:
        fig_r.add_trace(
            go.Scatter(
                x=df_mon["hour_of_day"],
                y=df_mon["avg_load"],
                name="Понеділок (робочий)",
                mode="lines+markers",
                line=dict(color="#f97316", width=3),
            )
        )
    if not df_sat.empty:
        fig_r.add_trace(
            go.Scatter(
                x=df_sat["hour_of_day"],
                y=df_sat["avg_load"],
                name="Субота (вихідний)",
                mode="lines+markers",
                line=dict(color="#38bdf8", width=2, dash="dash"),
            )
        )

    fig_r.update_layout(
        xaxis_title="Година доби (0–23)",
        yaxis_title="Середнє навантаження (МВт)",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", y=-0.2),
        template="plotly_dark",
    )
    return fig_r


import scipy.stats as stats
import numpy as np
from typing import Tuple, Optional, Dict
from sklearn.metrics import r2_score
from ml.backtest import perform_statistical_audit

def generate_academic_plots(df: pd.DataFrame) -> Tuple[Optional[go.Figure], Optional[go.Figure], Optional[go.Figure]]:
    """Generates high-fidelity Plotly figures for diploma defense.

    Args:
        df: DataFrame with columns [timestamp, actual_load_mw, predicted_load_mw].

    Returns:
        Tuple of (Time Series Plot, Error Distribution, Scatter Plot).
    """
    if df.empty:
        return None, None, None
    
    actual = df["actual_load_mw"]
    pred_lstm = df["predicted_load_mw"]
    pred_arima = df.get("arima_load_mw", np.zeros_like(pred_lstm))
    
    err_lstm = actual - pred_lstm
    err_arima = actual - pred_arima if "arima_load_mw" in df.columns else None
    
    # 1. Figure 5: Multi-Model Time Series
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df["timestamp"], y=actual, name="Actual (Факт)", 
        line=dict(color="#ff9f43", width=2.5)
    ))
    fig_trend.add_trace(go.Scatter(
        x=df["timestamp"], y=pred_lstm, name="LSTM Forecast (V3)", 
        line=dict(color="#ee5253", width=2.5)
    ))
    if err_arima is not None:
        fig_trend.add_trace(go.Scatter(
            x=df["timestamp"], y=pred_arima, name="ARIMA Baseline", 
            line=dict(color="#00cec9", width=2, dash="dash")
        ))
    
    fig_trend.update_layout(
        template="plotly_dark", title="📉 Figure 5: Temporal Load Dynamics (Comparative Analysis)",
        xaxis_title="Time", yaxis_title="Load, MW",
        hovermode="x unified", legend=dict(orientation="h", y=1.1, x=1, xanchor="right")
    )

    # 2. Figure 7: Distributional Audit
    fig_dist = go.Figure()
    audit_data = perform_statistical_audit(err_lstm.dropna().values)
    mu_l, std_l = audit_data.get("mu", 0), audit_data.get("sigma", 1)
    
    fig_dist.add_trace(go.Histogram(
        x=err_lstm, name="LSTM Residuals",
        marker_color="#a29bfe", opacity=0.5, histnorm='probability density'
    ))
    
    x_range = np.linspace(np.nanmin(err_lstm), np.nanmax(err_lstm), 200)
    fig_dist.add_trace(go.Scatter(
        x=x_range, y=stats.norm.pdf(x_range, mu_l, std_l),
        name="LSTM Normal Fit", line=dict(color="#6c5ce7", width=3)
    ))

    stats_text = (
        f"<b>LSTM Audit:</b> μ={mu_l:.1f}, σ={std_l:.1f}<br>"
        f"Normality (p): {audit_data.get('p_value',0):.4f}"
    )
    fig_dist.add_annotation(
        text=stats_text, xref="paper", yref="paper", x=0.98, y=0.98, showarrow=False,
        font=dict(size=13, color="white"), align="right",
        bgcolor="rgba(0,0,0,0.6)", bordercolor="#fff", borderwidth=1
    )
    
    fig_dist.update_layout(
        template="plotly_dark", title="📊 Figure 7: Statistical Audit of Residual Distribution",
        xaxis_title="Error (MW)", yaxis_title="Density"
    )

    # 3. Figure 8: Regression Scatter
    r2 = r2_score(actual, pred_lstm)
    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(
        x=actual, y=pred_lstm, mode="markers", name="Fitted Values",
        marker=dict(color="#4facfe", opacity=0.6, size=7)
    ))
    
    xy_lim = [min(actual.min(), pred_lstm.min()), max(actual.max(), pred_lstm.max())]
    fig_scatter.add_trace(go.Scatter(
        x=xy_lim, y=xy_lim, name="Ideal Identity (y=x)",
        line=dict(color="#ee5253", width=2, dash="dash")
    ))
    
    fig_scatter.add_annotation(
        text=f"<b>R² = {r2:.4f}</b>", xref="paper", yref="paper", x=0.05, y=0.95, showarrow=False,
        font=dict(size=22, color="#55efc4"), bgcolor="rgba(0,0,0,0.5)"
    )
    
    fig_scatter.update_layout(
        template="plotly_dark", title="🔵 Regression Fidelity Analysis",
        xaxis_title="Measured (MW)", yaxis_title="Predicted (MW)"
    )

    return fig_trend, fig_dist, fig_scatter


def generate_comparison_plot(results: Dict[str, pd.DataFrame], substation_name: str) -> go.Figure:
    """Creates a unified Plotly chart showing Actuals + V1/V2/V3 Predictions.
    
    Args:
        results: Dictionary where keys are model versions and values are backtest DataFrames.
        substation_name: Name of the substation for the title.
    """
    fig = go.Figure()
    
    # Extract actuals from the first available DataFrame
    first_df = next(iter(results.values()))
    fig.add_trace(go.Scatter(
        x=first_df["timestamp"], y=first_df["actual_load_mw"],
        name="Фактичне навантаження (Ground Truth)",
        line=dict(color="#ff9f43", width=3)
    ))
    
    # Visual cues for each version
    styles = {
        "v1": dict(color="#00d2d3", width=2, dash="dot"),
        "v2": dict(color="#54a0ff", width=2, dash="dash"),
        "v3": dict(color="#ee5253", width=3, dash="solid")
    }
    labels = {
        "v1": "LSTM Baseline (V1)", 
        "v2": "LSTM Diagnostic (V2)", 
        "v3": "LSTM Hybrid (V3) ⭐"
    }
    
    for version, df in results.items():
        if df is None or df.empty:
            continue
            
        fig.add_trace(go.Scatter(
            x=df["timestamp"], y=df["predicted_load_mw"],
            name=labels.get(version, f"Model {version.upper()}"),
            line=styles.get(version, dict(color="#fff", width=1))
        ))
        
    fig.update_layout(
        template="plotly_dark", 
        title=f"📊 Figure 10: Comparative Neural Fidelity Audit ({substation_name})",
        xaxis_title="Time (Last 7 Days)", 
        yaxis_title="Load Intensity, MW",
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig


# ==========================================
# 2. HIGH-PERFORMANCE BACKTEST ENGINE

def _generate_mega_hybrid_figure(df_bt, df_fc, title, version_lbl):
    """
    Створює єдиний потоковий графік (8 днів: 7 днів бектесту + 1 день майбутнього прогнозу).
    """
    if df_bt is None or df_bt.empty:
        return go.Figure().update_layout(title="⚠️ Дані для мега-графіка недоступні")

    fig = go.Figure()

    # 1. Справжній факт (Минуле)
    fig.add_trace(go.Scatter(
        x=df_bt["timestamp"], y=df_bt["actual_load_mw"],
        name="Actual (Факт)", line=dict(color="#ffa502", width=2)
    ))

    # 2. Ретроспективний прогноз (Минуле - Бектест)
    fig.add_trace(go.Scatter(
        x=df_bt["timestamp"], y=df_bt["predicted_load_mw"],
        name=f"Прогноз (Бектест {version_lbl})", 
        line=dict(color="#ee5253", width=2, dash="solid")
    ))

    # 3. Майбутній прогноз (Майбутнє - Live)
    # Прогнозний фрейм (df_fc) ВЖЕ містить останню фактичну точку для зшивання на рівні ml/predict_v2.py
    if not df_fc.empty:
        fig.add_trace(go.Scatter(
            x=df_fc["timestamp"], y=df_fc["predicted_load_mw"],
            name=f"Детальний прогноз ({version_lbl})",
            line=dict(color="#ee5253", width=3, dash="dash")
        ))
        
        # Довірчі інтервали
        if "upper_bond" in df_fc.columns:
            fig.add_trace(go.Scatter(
                x=df_fc["timestamp"], y=df_fc["upper_bond"],
                line=dict(width=0), showlegend=False, hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=df_fc["timestamp"], y=df_fc["lower_bond"],
                fill='tonexty', fillcolor='rgba(238, 82, 83, 0.1)',
                line=dict(width=0), name="Довірчий інтервал (95%)"
            ))

    fig.update_layout(
        template="plotly_dark",
        title=title,
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", y=1.1, x=1, xanchor="right"),
        hovermode="x unified"
    )
    return fig


def _generate_forecast_figure(df_hist, df_fc, title, version_lbl):
    """
    Генерує 'склеєний' графік Plotly (Blue History + Red Forecast).
    """
    fig = go.Figure()
    
    # 1. Історія (Фактичні дані) — Синя лінія
    if not df_hist.empty and "actual_load_mw" in df_hist.columns:
        fig.add_trace(go.Scatter(
            x=df_hist["timestamp"] if "timestamp" in df_hist.columns else df_hist.index,
            y=df_hist["actual_load_mw"], 
            name="Історія (Факт)", 
            mode="lines", 
            line=dict(color="#3498db", width=2.5)
        ))
    
    # 2. Довірчі інтервали (Confidence Bands) — захист від розтягування осі Y
    if not df_fc.empty and "upper_bond" in df_fc.columns and "lower_bond" in df_fc.columns:
        # Розраховуємо розумний ліміт (наприклад, 2x від макс. фактичного/прогнозного)
        # Це запобігає 'відльоту' осі Y в космос через аномальні довірчі інтервали.
        h_max = df_hist["actual_load_mw"].max() if (not df_hist.empty and "actual_load_mw" in df_hist.columns) else 0
        p_max = df_fc["predicted_load_mw"].max() if not df_fc.empty else 0
        max_val = max(h_max, p_max)
        safe_upper = df_fc["upper_bond"].clip(upper=max_val * 1.5)
        
        fig.add_trace(go.Scatter(
            x=pd.concat([df_fc["timestamp"], df_fc["timestamp"][::-1]]), 
            y=pd.concat([safe_upper, df_fc["lower_bond"][::-1]]), 
            fill="toself", 
            fillcolor="rgba(231,76,60,0.08)", 
            line=dict(color="rgba(0,0,0,0)"), 
            hoverinfo="skip", 
            showlegend=False
        ))

    # 3. Прогноз — Червона пунктирна лінія
    if not df_fc.empty:
        fig.add_trace(go.Scatter(
            x=df_fc["timestamp"], 
            y=df_fc["predicted_load_mw"], 
            name=f"Прогноз ШІ ({version_lbl})", 
            mode="lines", 
            line=dict(color="#e74c3c", width=2.5, dash="dash")
        ))
    
    fig.update_layout(
        template="plotly_dark", 
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(12,14,20,1)", 
        height=500, 
        margin=dict(l=10, r=10, t=55, b=10), 
        hovermode="x unified",
        title=dict(text=title, font=dict(size=18, color="#fff"), x=0.01),
        xaxis_title="Час",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # ПРИМУСОВЕ АВТОМАСШТАБУВАННЯ ОСІ Y
    fig.update_yaxes(
        autorange=True, 
        fixedrange=False, 
        title_text="Потужність, МВт",
        gridcolor="rgba(255,255,255,0.05)"
    )
    return fig

