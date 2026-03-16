import numpy as np
import pandas as pd


def calculate_line_losses(df_lines: pd.DataFrame) -> pd.DataFrame:
    """
    Розраховує втрати потужності в мережі для AC та HVDC ліній.

    :param df_lines: DataFrame з колонками actual_load_mw, load_pct, max_load_mw.
    :return: DataFrame з додатковою колонкою 'losses_mw' i 'line_type'.
    """
    if df_lines.empty:
        return df_lines

    df = df_lines.copy()

    # Визначення типу ліній, якщо ще не визначено
    if "line_type" not in df.columns and "max_load_mw" in df.columns:
        df["line_type"] = df["max_load_mw"].apply(
            lambda x: "HVDC" if x >= 3000 else "AC"
        )

    if "line_type" not in df.columns:
        # Fallback
        df["line_type"] = "AC"

    is_hvdc = df["line_type"] == "HVDC"
    loss_dc = (df["actual_load_mw"] * 0.015) * (df["load_pct"] / 100)
    loss_ac = (df["actual_load_mw"] * 0.035) * (df["load_pct"] / 100) ** 2
    df["losses_mw"] = np.where(is_hvdc, loss_dc, loss_ac)

    return df
