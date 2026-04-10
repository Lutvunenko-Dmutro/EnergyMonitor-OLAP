import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.ui_helpers import safe_plotly_render

# Координація кольорової схеми для всіх візуалізацій
MASTER_COLORS = {
    "nuclear": "#fbbf24",  # Жовтий
    "thermal": "#a855f7",  # Фіолетовий
    "hydro": "#3b82f6",  # Синій
    "solar": "#f97316",  # Помаранчевий
    "wind": "#2dd4bf",  # Бірюзовий
}


def render(df_gen):
    """
    Рендеринг вкладки генерації.
    Візуалізація: Sankey (потоки), Pie (частка), Area (динаміка).
    """
    st.subheader("⚡ Структура генерації")

    if df_gen.empty:
        st.warning("⚠️ Дані про генерацію відсутні.")
        st.info(
            "💡 Дані про структуру генерації (АЕС, ТЕС, ВДЕ) доступні лише в режимі Live-симуляції."
        )
        return

    # Словник для підписів графіків
    labels_ua = {
        "actual_generation_mw": "Генерація (МВт)",
        "timestamp": "Час",
        "generator_type": "Тип джерела",
        "region_name": "Регіон",
    }

    # Візуалізація потоків енергії (Sankey Diagram)
    st.markdown("##### 🌊 Потік енергії (Джерело -> Регіон)")

    # Групуємо дані для діаграми
    df_s = (
        df_gen.groupby(["generator_type", "region_name"])["actual_generation_mw"]
        .sum()
        .reset_index()
    )

    # 🌟 АЛГОРИТМ SANKEY 🌟
    src_labels = sorted(list(df_s["generator_type"].unique()))
    tgt_labels = sorted(list(df_s["region_name"].unique()))
    all_nodes = src_labels + tgt_labels

    # Mapping назв у індекси
    node_indices = {name: i for i, name in enumerate(all_nodes)}

    # Формуємо зв'язки (source, target, values)
    source_idx = [node_indices[s] for s in df_s["generator_type"]]
    target_idx = [node_indices[t] for t in df_s["region_name"]]
    values = df_s["actual_generation_mw"].tolist()

    # 2. Генеруємо списки кольорів для малюнка (СИНХРОНІЗОВАНИЙ З MASTER_COLORS)
    node_colors = [MASTER_COLORS.get(node.lower(), "#64748b") for node in all_nodes]
    link_colors = [
        MASTER_COLORS.get(src.lower(), "rgba(100, 116, 139, 0.5)").replace("#", "rgba(")
        for src in df_s["generator_type"]
    ]

    # Створюємо зручний rgba формат для Sankey з Hex
    def hex_to_rgba(h, alpha=0.5):
        h = h.lstrip("#")
        rgb = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
        return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"

    node_colors = [MASTER_COLORS.get(n.lower(), "#64748b") for n in all_nodes]
    link_colors = [
        hex_to_rgba(MASTER_COLORS.get(t.lower(), "#888888"), 0.5)
        for t in df_s["generator_type"]
    ]

    # 3. Будуємо оновлений Sankey
    fig_sankey = go.Figure(
        data=[
            go.Sankey(
                valueformat=".1f",  # Форматування цифр у тултипі
                valuesuffix=" МВт*год",  # Одиниці виміру
                node=dict(
                    pad=20,
                    thickness=15,
                    line=dict(color="rgba(255,255,255,0.1)", width=1),
                    label=all_nodes,
                    color=node_colors,  # 🎨 Застосовуємо кольори вузлів
                ),
                link=dict(
                    source=source_idx,
                    target=target_idx,
                    value=values,
                    color=link_colors,  # 🎨 Застосовуємо кольори потоків
                ),
            )
        ]
    )

    fig_sankey.update_layout(
        font_size=12,
        height=350,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )
    safe_plotly_render(fig_sankey)

    st.markdown("---")

    # Деталізація структури за джерелами (Pie & Area) stacked area
    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown("##### 🍰 Частка джерел (Energy Mix)")
        # Створюємо мапу для синхронізації
        mix_map = {
            gen: MASTER_COLORS.get(gen.lower(), "#888888")
            for gen in df_gen["generator_type"].unique()
        }

        fig_pie = px.pie(
            df_gen,
            values="actual_generation_mw",
            names="generator_type",
            hole=0.5,
            color="generator_type",
            color_discrete_map=mix_map,
            labels=labels_ua,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
        safe_plotly_render(fig_pie)

    with c2:
        st.markdown("##### 🌊 Динаміка генерації")
        # Агрегація для Area Chart (сума по годинах)
        df_area = (
            df_gen.groupby(["timestamp", "generator_type"])["actual_generation_mw"]
            .sum()
            .reset_index()
        )

        # Будуємо Area Chart через go.Figure() для 100% контролю стилів
        fig_area = go.Figure()

        # Створення rgba для заливки з Hex
        def hex_to_rgba(h, alpha=0.3):
            h = h.lstrip("#")
            rgb = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
            return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"

        for gen_type in df_area["generator_type"].unique():
            df_sub = df_area[df_area["generator_type"] == gen_type]
            line_color = MASTER_COLORS.get(gen_type.lower(), "#888888")
            rgba_color = hex_to_rgba(line_color, 0.3)

            fig_area.add_trace(
                go.Scatter(
                    x=df_sub["timestamp"],
                    y=df_sub["actual_generation_mw"],
                    mode="lines",
                    name=gen_type,
                    stackgroup="one",  # Stacked Area
                    line=dict(width=2, color=line_color),
                    fillcolor=rgba_color,
                )
            )

        fig_area.update_layout(
            hovermode="x unified",
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            margin=dict(l=20, r=20, t=30, b=20),
        )
        safe_plotly_render(fig_area)

    # [FIX]: Spacer для скролінгу в самому низу
    st.markdown('<div style="height: 300px;"></div>', unsafe_allow_html=True)
