import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return ",".join(str(int(h[i : i + 2], 16)) for i in (0, 2, 4))

def render_dual_axis_chart(df, left_col, left_label, left_color, right_col, right_label, right_color, fill_left=True):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    unique_subs = df["substation"].unique() if "substation" in df.columns else [None]
    is_multi = len(unique_subs) > 1

    for sub in unique_subs:
        sub_df = df[df["substation"] == sub] if sub is not None else df
        trace_name = str(sub) if sub is not None else left_label
        fig.add_trace(go.Scatter(
            x=sub_df["ts"], y=sub_df[left_col], name=f"{trace_name} ({left_label})" if is_multi else left_label,
            line=dict(color=left_color if not is_multi else None, width=2),
            fill="tozeroy" if fill_left and not is_multi else "none",
            fillcolor=f"rgba({_hex_to_rgb(left_color)},0.08)" if fill_left and not is_multi else None
        ), secondary_y=False)

        fig.add_trace(go.Scatter(
            x=sub_df["ts"], y=sub_df[right_col], name=f"{trace_name} ({right_label})" if is_multi else right_label,
            line=dict(color=right_color if not is_multi else None, width=1.5, dash="dot" if not is_multi else "solid")
        ), secondary_y=True)

    fig.update_yaxes(title_text=left_label, secondary_y=False)
    fig.update_yaxes(title_text=right_label, secondary_y=True, showgrid=False)
    fig.update_layout(
        height=400,
        hovermode="x unified",
        margin=dict(l=10, r=10, t=30, b=80), 
        legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5),
        template="plotly_dark"
    )
    return fig

def render_rhythm_chart(df_rhythm: pd.DataFrame) -> go.Figure:
    fig_r = go.Figure()
    if df_rhythm.empty: return fig_r
    df_r = df_rhythm.copy()
    for col in ["dow", "hour_of_day", "avg_load"]: df_r[col] = pd.to_numeric(df_r[col], errors="coerce")
    df_mon = df_r[df_r["dow"] == 1].sort_values("hour_of_day")
    df_sat = df_r[df_r["dow"] == 6].sort_values("hour_of_day")

    if not df_mon.empty:
        fig_r.add_trace(go.Scatter(x=df_mon["hour_of_day"], y=df_mon["avg_load"], name="Понеділок", line=dict(color="#f97316", width=3)))
    if not df_sat.empty:
        fig_r.add_trace(go.Scatter(x=df_sat["hour_of_day"], y=df_sat["avg_load"], name="Субота", line=dict(color="#38bdf8", width=2, dash="dash")))

    fig_r.update_layout(
        height=400,
        xaxis_title="Година (0–23)", 
        yaxis_title="МВт", 
        hovermode="x unified", 
        margin=dict(l=10, r=10, t=30, b=80),
        legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5),
        template="plotly_dark"
    )
    return fig_r
