"""
tabs/historical_audit.py
Цифровий архів: глибокий аудит фізики за довільний період.
"""

import datetime

import pandas as pd
import streamlit as st

from core.database.archive import (
    get_archive_bounds as _get_archive_bounds,
)
from core.database.archive import (
    load_archive_data as _load_archive_data,
)
from core.database.archive import (
    load_rhythm_data as _load_rhythm_data,
)
from ui.components.charts import render_dual_axis_chart


def render(
    selected_region: str, date_range=None, selected_substation=["Усі підстанції"]
):
    """
    Рендер панелі цифрого архіву з глибоким аналізом кореляції параметрів.
    """
    st.subheader("📜 Цифровий архів")

    # Отримання часових меж з бази даних
    df_bounds = _get_archive_bounds()
    if df_bounds.empty or df_bounds["ts_min"].iloc[0] is None:
        st.warning("⚠️ Таблиця LoadMeasurements порожня — чекаємо на генератор.")
        return

    arch_min = pd.to_datetime(df_bounds["ts_min"].iloc[0]).date()
    arch_max = pd.to_datetime(df_bounds["ts_max"].iloc[0]).date()

    # Розрахунок діапазону відповідно до глобальних фільтрів
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range[0], date_range[1]
    else:
        start_date = arch_max - datetime.timedelta(days=30)
        end_date = arch_max

    # Обмежуємо межами наявних даних
    start_date = max(arch_min, start_date)
    end_date = max(arch_min, min(end_date, arch_max))

    if start_date > end_date:
        st.warning("Некоректний діапазон дат у глобальному фільтрі.")
        return

    # Визначення цільового об'єкта аналізу (Регіон/Підстанція)
    use_aggregate = (
        "Усі підстанції" in selected_substation or not selected_substation
        if isinstance(selected_substation, list)
        else selected_substation == "Усі підстанції"
    )

    active_target = selected_substation if not use_aggregate else selected_region

    # Формування динамічного заголовка звіту
    if isinstance(active_target, list):
        obj_name = ", ".join(active_target)
    else:
        obj_name = (
            active_target
            if active_target
            and active_target not in ("Всі регіони", "Усі підстанції", "")
            else "всіх регіонів"
        )

    st.markdown(
        f"### Аналіз даних для **{obj_name}** "
        f"за період з **{start_date.strftime('%d.%m.%Y')}** "
        f"по **{end_date.strftime('%d.%m.%Y')}**"
    )

    # Завантаження та агрегація даних
    with st.spinner("Виконання агрегаційного запиту..."):
        df = _load_archive_data(start_date, end_date, active_target)

    if df.empty:
        st.warning(
            "Немає даних для обраних параметрів. Перевірте фільтр або чекайте генератора."
        )
        return

    df["ts"] = pd.to_datetime(df["ts"])
    for col in ["load_mw", "oil_temp", "h2_ppm", "health", "air_temp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Агрегуємо в одну середню лінію, якщо станцій декілька (прибирає пилку)
    if "substation" in df.columns and len(df["substation"].unique()) > 1:
        df = df.groupby("ts").mean(numeric_only=True).reset_index()

    # Візуалізація агрегованих метрик
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚡ Макс. навантаження", f"{df['load_mw'].max():.1f} МВт")
    c2.metric(
        "🌡️ Мін. темп. повітря",
        f"{df['air_temp'].min():.1f} °C" if df["air_temp"].notna().any() else "N/A",
    )
    c3.metric(
        "🔥 Макс. темп. масла",
        f"{df['oil_temp'].max():.1f} °C" if df["oil_temp"].notna().any() else "N/A",
    )
    c4.metric(
        "💚 Сер. Health Score",
        f"{df['health'].mean():.1f} %" if df["health"].notna().any() else "N/A",
    )

    st.divider()

    # Візуалізація динаміки навантаження (Доріжки): Будні vs Вихідні
    st.markdown("#### ⏳ Енергетичний Пульс: Будні vs Вихідні")
    st.caption(
        "Наочна демонстрація `day_multiplier`: у будній день заводи працюють, у вихідні — навантаження падає."
    )
    df_rhythm = _load_rhythm_data(start_date, end_date, active_target)
    if not df_rhythm.empty:
        from ui.components.charts import render_rhythm_chart

        st.plotly_chart(render_rhythm_chart(df_rhythm), use_container_width=True)
    else:
        st.info("Недостатньо даних для побудови ритмічного графіку за обраний період.")

    st.divider()

    # Кореляція навантаження та температури повітря
    st.markdown("#### 🌤️ Термодинамічний Баланс: Вплив Погоди")
    st.plotly_chart(
        render_dual_axis_chart(
            df,
            "load_mw",
            "Навантаження (МВт)",
            "#f97316",
            "air_temp",
            "Повітря (°C)",
            "#38bdf8",
        ),
        use_container_width=True,
    )
    st.divider()

    # Кореляція навантаження та температури масла
    st.markdown("#### 🛢️ Теплова Діагностика: Трансформаторне Масло")
    st.plotly_chart(
        render_dual_axis_chart(
            df,
            "load_mw",
            "Навантаження (МВт)",
            "#f97316",
            "oil_temp",
            "Масло (°C)",
            "#f43f5e",
        ),
        use_container_width=True,
    )
    st.divider()

    # Кореляція показників роботи та концентрації газів H2
    st.markdown("#### 🛡️ Моніторинг Здоров'я: Ресурс Обладнання")
    st.plotly_chart(
        render_dual_axis_chart(
            df, "health", "Health Score (%)", "#22c55e", "h2_ppm", "H₂ (ppm)", "#a855f7"
        ),
        use_container_width=True,
    )

    # ── Таблиця: Raw Data ────────────────────────────────────────────────────────
    st.divider()
    st.subheader("📋 Детальні дані (Raw Data)")

    # Форматуємо DataFrame: перейменовуємо, заповнюємо NaN
    # 📋 Детальні дані (Raw Data) Bulletproof Стовпці
    valid_cols = []
    headers = []

    mapping = {
        "ts": "Дата / Час",
        "substation": "Підстанція",
        "load_mw": "Навантаження (МВт)",
        "air_temp": "Повітря (°C)",
        "oil_temp": "Масло (°C)",
        "h2_ppm": "H₂ (ppm)",
        "health": "Health (%)",
    }

    for orig, pretty in mapping.items():
        if orig in df.columns:
            valid_cols.append(orig)
            headers.append(pretty)

    df_display = df[valid_cols].copy()
    df_display.columns = headers

    # Замінюємо NaN на 0 для числових стовпців
    num_cols = [
        c
        for c in [
            "Навантаження (МВт)",
            "Повітря (°C)",
            "Масло (°C)",
            "H₂ (ppm)",
            "Health (%)",
        ]
        if c in df_display.columns
    ]
    df_display[num_cols] = df_display[num_cols].fillna(0)

    st.dataframe(
        df_display.style.format({col: "{:.2f}" for col in num_cols}),
        width="stretch",
        height=350,
    )

    csv_bytes = df_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Скачати CSV",
        data=csv_bytes,
        file_name=f"archive_{start_date}_{end_date}.csv",
        mime="text/csv",
    )
