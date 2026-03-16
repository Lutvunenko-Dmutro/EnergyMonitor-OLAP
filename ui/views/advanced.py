import pandas as pd
import plotly.express as px
import streamlit as st
from statsmodels.tsa.seasonal import seasonal_decompose

from core.analytics.clustering import cluster_substations


def render_advanced_analysis(df, selected_substation):
    """
    Приймає DataFrame 'load' з main.py.
    Очікувані колонки: 'substation_name', 'actual_load_mw', 'temperature', 'timestamp'
    """
    st.title("🧩 Поглиблена аналітика (AI & Trends)")

    # Перевірка наявності необхідних колонок
    required_cols = ["substation_name", "actual_load_mw", "timestamp"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"У даних відсутні необхідні колонки: {required_cols}")
        return

    if df.empty:
        st.warning("Недостатньо даних для аналізу.")
        return

    # Фільтрація та підготовка даних
    # Дані вже відфільтровані в main.py за вибором користувача.

    tab1, tab2 = st.tabs(["📊 Кластеризація (Сегментація)", "📈 Аналіз трендів"])

    @st.fragment
    def render_clustering(df_cluster_in):
        col_title, col_tools = st.columns([4, 1])
        with col_title:
            st.subheader("📊 Кластеризація (Ризик)")
            st.caption("AI аналізує навантаження, щоб виявити проблемні об'єкти.")

        with col_tools.popover("⚙️ Налаштування", use_container_width=True):
            use_log_advanced = st.toggle(
                "🪵 Логарифмічна шкала", value=False, key="adv_use_log"
            )

        try:
            # Використовуємо аналітичний модуль для кластеризації
            df_grouped = cluster_substations(df_cluster_in, n_clusters=3)

            if not df_grouped.empty:
                current_names = [
                    "🔴 Високе навантаження",
                    "🟡 Штатний режим",
                    "🟢 Низьке навантаження",
                ]

                col_chart, col_stats = st.columns([3, 1])

                with col_chart:
                    color_map = {
                        "🟢 Низьке навантаження": "#00CC96",
                        "🟡 Штатний режим": "#FFA15A",
                        "🔴 Високе навантаження": "#EF553B",
                    }
                    fig = px.scatter(
                        df_grouped,
                        x="avg_load",
                        y="max_load",
                        color="Status",
                        size=df_grouped["avg_temp"].clip(lower=1),
                        hover_name="substation_name",
                        hover_data={
                            "avg_load": ":.2f",
                            "max_load": ":.2f",
                            "avg_temp": ":.1f",
                        },
                        color_discrete_map=color_map,
                        log_x=use_log_advanced,
                        log_y=use_log_advanced,
                        template="plotly_dark",
                        height=500,
                        labels={
                            "avg_load": "Середнє навантаження (МВт)",
                            "max_load": "Пікове навантаження (МВт)",
                        },
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col_stats:
                    st.write("### 📋 Статистика")

                    def get_object_word(count):
                        if count % 10 == 1 and count % 100 != 11:
                            return "об'єкт"
                        elif 2 <= count % 10 <= 4 and (
                            count % 100 < 10 or count % 100 >= 20
                        ):
                            return "об'єкти"
                        else:
                            return "об'єктів"

                    counts = df_grouped["Status"].value_counts()
                    for status in current_names[::-1]:
                        if status in counts:
                            count = counts[status]
                            word = get_object_word(count)
                            if "🔴" in status:
                                st.error(f"**{count}** {word} у зоні ризику")
                            elif "🟡" in status:
                                st.warning(f"**{count}** {word} у штатному режимі")
                            else:
                                st.success(
                                    f"**{count}** {word} з низьким навантаженням"
                                )

                    st.divider()
                    st.markdown("**Топ навантажених:**")
                    top_loaded = df_grouped.sort_values(
                        "avg_load", ascending=False
                    ).head(5)
                    st.dataframe(
                        top_loaded[["substation_name", "avg_load"]],
                        hide_index=True,
                        column_config={
                            "substation_name": "Назва",
                            "avg_load": st.column_config.NumberColumn(
                                "МВт", format="%.1f"
                            ),
                        },
                        width="stretch",
                    )
            else:
                st.info("Недостатньо даних для кластеризації.")
        except Exception as e:
            st.error(f"Помилка при кластеризації: {e}")

    @st.fragment
    def render_trends(df_trends_in):
        col_title, col_tools = st.columns([4, 1])
        col_title.subheader("📈 Декомпозиція часового ряду")

        with col_tools.popover("⚙️ Налаштування", use_container_width=True):
            use_rel_advanced = st.toggle(
                "📈 Відносне навантаження (%)", value=False, key="adv_use_rel"
            )

        # Адаптуємо під вибір sidebar
        use_aggregate = (
            "Усі підстанції" in selected_substation or not selected_substation
            if isinstance(selected_substation, list)
            else selected_substation == "Усі підстанції"
        )

        if not use_aggregate:
            sub_to_analyze = (
                selected_substation[0]
                if isinstance(selected_substation, list)
                else selected_substation
            )
            st.success(f"🎯 Аналіз тренду для об'єкта: **{sub_to_analyze}**")
            df_sub = df_trends_in[
                df_trends_in["substation_name"] == sub_to_analyze
            ].copy()
            title_text = f"Декомпозиція: {sub_to_analyze}"
        else:
            st.info("💡 Агрегований тренд для всієї мережі (Сумарне навантаження)")
            # Агрегуємо по часу для всієї мережі
            df_sub = df_trends_in.copy()
            df_sub["timestamp"] = pd.to_datetime(df_sub["timestamp"])
            df_sub = (
                df_sub.groupby("timestamp").agg({"actual_load_mw": "sum"}).reset_index()
            )
            title_text = "Декомпозиція: Вся мережа (Загальна сума)"

        if not df_sub.empty:
            df_sub["timestamp"] = pd.to_datetime(df_sub["timestamp"])
            df_sub = (
                df_sub.sort_values("timestamp")
                .set_index("timestamp")
                .pipe(lambda x: x[~x.index.duplicated(keep="first")])
            )

            resampled = df_sub["actual_load_mw"].resample("h").mean().ffill()

            if use_rel_advanced and resampled.max() > 0:
                resampled = resampled / resampled.max() * 100

            if len(resampled) > 48:
                try:
                    result = seasonal_decompose(resampled, model="additive", period=24)

                    df_decomp = pd.DataFrame(
                        {
                            "timestamp": resampled.index,
                            "Тренд": result.trend.values,
                            "Сезонність": result.seasonal.values,
                            "Залишок (аномалії)": result.resid.values,
                        }
                    ).melt(
                        id_vars="timestamp", var_name="Компонент", value_name="Значення"
                    )

                    fig_decomp = px.line(
                        df_decomp,
                        x="timestamp",
                        y="Значення",
                        facet_row="Компонент",
                        color="Компонент",
                        template="plotly_dark",
                        height=650,
                        title=title_text,
                    )
                    fig_decomp.update_xaxes(title_text="Дата / Час")
                    fig_decomp.update_yaxes(title_text="", matches=None)
                    fig_decomp.for_each_annotation(
                        lambda a: a.update(text=a.text.split("=")[-1])
                    )
                    st.plotly_chart(fig_decomp, use_container_width=True)

                except Exception as e:
                    st.warning(f"Помилка розрахунку тренду: {e}")
            else:
                st.info("Недостатньо даних (потрібно > 48 годин).")

    with tab1:
        render_clustering(df)
    with tab2:
        render_trends(df)
