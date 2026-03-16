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
