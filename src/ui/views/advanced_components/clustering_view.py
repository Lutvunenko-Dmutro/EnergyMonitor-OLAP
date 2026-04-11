import streamlit as st
import plotly.express as px
from src.core.analytics.clustering import cluster_substations
from src.utils.ui_helpers import safe_plotly_render

def render_clustering_segment(df, use_log, selected_substation):
    """
    Renders the clustering analysis segment.
    """
    st.subheader("📊 Кластеризація (Ризик)")
    st.caption("AI аналізує навантаження, щоб виявити проблемні об'єкти.")

    try:
        df_grouped = cluster_substations(df, n_clusters=3)
        if not df_grouped.empty:
            current_names = ["🔴 Високе навантаження", "🟡 Штатний режим", "🟢 Низьке навантаження"]
            col_chart, col_stats = st.columns([3, 1])

            with col_chart:
                color_map = {
                    "🟢 Низьке навантаження": "#00CC96",
                    "🟡 Штатний режим": "#FFA15A",
                    "🔴 Високе навантаження": "#EF553B",
                }
                fig = px.scatter(
                    df_grouped, x="avg_load", y="max_load", color="Status",
                    size=df_grouped["avg_temp"].clip(lower=1),
                    hover_name="substation_name", color_discrete_map=color_map,
                    log_x=use_log, log_y=use_log, template="plotly_dark", height=500,
                    labels={"avg_load": "Середнє навантаження (МВт)", "max_load": "Пікове навантаження (МВт)"},
                )
                safe_plotly_render(fig)

            with col_stats:
                st.write("### 📋 Статистика")
                counts = df_grouped["Status"].value_counts()
                for status in current_names[::-1]:
                    if status in counts:
                        count = counts[status]
                        if "🔴" in status: st.error(f"**{count}** об'єктів у зоні ризику")
                        elif "🟡" in status: st.warning(f"**{count}** об'єктів у штатному режимі")
                        else: st.success(f"**{count}** об'єктів з низьким навантаженням")

                st.divider()
                st.markdown("**Топ навантажених:**")
                top_loaded = df_grouped.sort_values("avg_load", ascending=False).head(5)
                st.dataframe(top_loaded[["substation_name", "avg_load"]], hide_index=True, use_container_width=True)
        else:
            st.info("Недостатньо даних для кластеризації.")
    except Exception as e:
        st.error(f"Помилка при кластеризації: {e}")
