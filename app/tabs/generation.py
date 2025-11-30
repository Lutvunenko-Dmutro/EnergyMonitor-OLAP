import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render(df_gen):
    """Вкладка генерації з повною аналітикою (Optimized)."""
    st.subheader("⚡ Структура генерації")
    
    if df_gen.empty:
        st.warning("⚠️ Дані про генерацію відсутні.")
        return

    # Словник для перекладу
    labels_ua = {
        "actual_generation_mw": "Генерація (МВт)",
        "timestamp": "Час",
        "generator_type": "Тип джерела",
        "region_name": "Регіон"
    }

    # --- 1. SANKEY DIAGRAM (Потік енергії) ---
    st.markdown("##### 🌊 Потік енергії (Sankey)")
    
    # Групуємо дані: Джерело -> Регіон
    df_s = df_gen.groupby(['generator_type', 'region_name'])['actual_generation_mw'].sum().reset_index()
    
    # Підготовка вузлів та лінків
    src_labels = list(df_s['generator_type'].unique())
    tgt_labels = list(df_s['region_name'].unique())
    all_nodes = src_labels + tgt_labels
    
    source_indices = [all_nodes.index(s) for s in df_s['generator_type']]
    target_indices = [all_nodes.index(t) for t in df_s['region_name']]
    values = df_s['actual_generation_mw'].tolist()
    
    fig_sankey = go.Figure(go.Sankey(
        node=dict(
            pad=15, 
            thickness=20, 
            line=dict(color="black", width=0.5), 
            label=all_nodes, 
            color="#3b82f6" # Синій колір вузлів
        ),
        link=dict(
            source=source_indices, 
            target=target_indices, 
            value=values,
            color="rgba(59, 130, 246, 0.3)" # Напівпрозорі лінії
        )
    ))
    
    fig_sankey.update_layout(title_text="Баланс: Джерело -> Регіон", font_size=12, height=400)
    st.plotly_chart(fig_sankey, use_container_width=True)

    st.markdown("---")

    # --- 2. ДЕТАЛІЗАЦІЯ (Pie & Area) ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("##### 🍰 Частка джерел (Energy Mix)")
        fig_pie = px.pie(
            df_gen, 
            values='actual_generation_mw', 
            names='generator_type', 
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels=labels_ua
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.markdown("##### 🌊 Динаміка генерації (Stacked Area)")
        # Агрегація по часу для прискорення графіка
        df_area = df_gen.groupby(['timestamp', 'generator_type'])['actual_generation_mw'].sum().reset_index()
        
        fig_area = px.area(
            df_area, 
            x='timestamp', 
            y='actual_generation_mw', 
            color='generator_type', 
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels=labels_ua
        )
        fig_area.update_layout(hovermode="x unified", showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_area, use_container_width=True)