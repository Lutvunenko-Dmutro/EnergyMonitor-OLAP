import pandas as pd
import streamlit as st

from ui.components.cards import make_health_bar, render_gauge


def render(df_latest, region_filter: str | None = None):
    """
    Рендеринг інтелектуальної KPI панелі з захистом від порожніх даних (NaN/None).
    region_filter: назва регіону для фільтрації підстанцій (None = всі регіони).
    """
    st.subheader("🚨 Оперативний моніторинг та діагностика")

    if df_latest.empty:
        st.info("Чекаємо на дані від віртуальних датчиків...")
        return

    # Перевірка на "Kaggle mode" (відсутність колонок здоров'я)
    if "health_score" not in df_latest.columns:
        st.info("ℹ️ **Режим реальних даних (Kaggle AEP)**")
        st.info(
            "Ці детальні метрики стану (напруга, здоров'я, склад газів) доступні лише в режимі Live-симуляції з використанням двигуна Digital Twin."
        )

        # Відображаємо тільки загальне споживання
        total_load = df_latest["actual_load_mw"].sum()
        st.metric(
            "⚡ Поточне навантаження регіону",
            f"{total_load:,.1f} МВт".replace(",", " "),
        )
        return

    # Обробка та валідація числових показників (Захист від TypeError)
    df_clean = df_latest.copy()
    numeric_cols = [
        "health_score",
        "frequency_hz",
        "actual_load_mw",
        "voltage_kv",
        "temperature_c",
        "h2_ppm",
    ]
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce").fillna(0.0)

    # Розрахунок середнього здоров'я
    avg_health = (
        df_clean["health_score"].mean() if "health_score" in df_clean.columns else None
    )

    # Частота
    if "frequency_hz" in df_clean.columns:
        first_freq = df_clean["frequency_hz"].iloc[0]
        system_freq = first_freq if first_freq > 0 else 50.0
    else:
        system_freq = None

    total_load = df_clean["actual_load_mw"].sum()

    # Візуалізація верхнього ярусу показників (KPI)
    m1, m2, m3, m4 = st.columns(4)

    if avg_health is not None:
        h_color = "normal" if avg_health > 85 else "inverse"
        m1.metric("🏥 Здоров'я мережі", f"{avg_health:.1f}%", delta_color=h_color)
    else:
        m1.metric("🏥 Здоров'я мережі", "N/A")

    if system_freq is not None:
        f_delta = round(system_freq - 50.0, 3)
        m2.metric(
            "💓 Частота",
            f"{system_freq:.2f} Гц",
            delta=f_delta if f_delta != 0 else None,
        )
    else:
        m2.metric("💓 Частота", "N/A")

    m3.metric("⚡ Повна потужність", f"{total_load:,.1f} МВт".replace(",", " "))

    with m4:
        max_system_capacity = 40000.0  # Базова константа або сума capacity
        avg_load_pct = (total_load / max_system_capacity * 100).clip(0, 100)
        render_gauge(avg_load_pct)

    st.divider()

    # Фільтруємо за регіоном, якщо вибрано
    df_cards = df_clean.copy()
    if "substation_name" in df_cards.columns:
        df_cards = df_cards[df_cards["substation_name"] != "AEP Region"]

    if (
        region_filter
        and region_filter != "Всі регіони"
        and "region_name" in df_cards.columns
    ):
        df_filtered_region = df_cards[df_cards["region_name"] == region_filter]
        if not df_filtered_region.empty:
            df_cards = df_filtered_region

    # Рендеринг деталізованої таблиці підстанцій (Digital Twins)
    st.markdown("### 📊 Деталізація по підстанціях")

    # Готуємо чистий DataFrame для відображення
    df_table = df_cards[
        [
            "substation_name",
            "actual_load_mw",
            "voltage_kv",
            "temperature_c",
            "h2_ppm",
            "health_score",
        ]
    ].copy()

    # Використовуємо імпортований make_health_bar від ui.components.cards

    df_table["Стан (Здоров'я)"] = df_table["health_score"].apply(make_health_bar)

    # Вибираємо порядок стовпців для рендерингу
    df_render = df_table[
        [
            "substation_name",
            "actual_load_mw",
            "voltage_kv",
            "temperature_c",
            "h2_ppm",
            "Стан (Здоров'я)",
        ]
    ]

    # Виводимо сучасну таблицю з візуалізацією всередині
    st.dataframe(
        df_render,
        column_config={
            "substation_name": st.column_config.TextColumn("Підстанція", width="large"),
            "actual_load_mw": st.column_config.NumberColumn(
                "Навантаження", format="%.1f МВт"
            ),
            "voltage_kv": st.column_config.NumberColumn("Напруга", format="%.1f кВ"),
            "temperature_c": st.column_config.NumberColumn(
                "Темп. Масла", format="%.1f °C"
            ),
            "h2_ppm": st.column_config.NumberColumn("H2", format="%.1f ppm"),
            "Стан (Здоров'я)": st.column_config.TextColumn(
                "AI Здоров'я & Статус", width="medium"
            ),
        },
        hide_index=True,
        use_container_width=True,
    )

    # [FIX]: Spacer для скролінгу в самому низу
    st.markdown('<div style="height: 300px;"></div>', unsafe_allow_html=True)


# render_gauge винесено в ui.components.cards
