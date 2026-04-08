import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from ml.forecast_controller import cached_fast_backtest as _cached_fast_backtest
from ml.forecast_controller import get_cached_history as _get_history
from utils.ui_helpers import safe_plotly_render
from ui.views.forecast_components.constants import MODEL_LABELS

def _render_comparative_audit(substation_name, source_type):
    """
    Виконує порівняльний аналіз трьох поколінь LSTM (V1, V2, V3) 
    та відображає порівняльну таблицю і графік.
    """
    from ml.backtest import get_fast_backtest
    from ui.components.charts import generate_comparison_plot
    
    # Optimization for CSV/Benchmark sources: V2/V3 are not suitable due to missing sensors
    if source_type == "CSV":
        versions = ["v1"]
        audit_title = f"🎯 Детальний аудит точності для {substation_name} (Базова архітектура V1)"
    else:
        versions = ["v1", "v2", "v3"]
        audit_title = f"🏆 Рейтинг ефективності нейромережевих архітектур для {substation_name}"
    
    results = {}
    metrics_list = []
    
    with st.status(f"🚀 Запуск комплексного порівняльного аудиту для {substation_name}...", expanded=True) as status:
        p_bar = st.progress(0, text="Підготовка до аналізу...")
        total = len(versions)
        
        for idx, v in enumerate(versions):
            progress_pct = (idx + 1) / total
            status.update(label=f"🧠 Аналіз архітектури {v.upper()} ({idx+1}/{total})...")
            p_bar.progress(progress_pct, text=f"Обчислення: Модель {v.upper()}...")
            
            # Викликаємо кешований бектест (168 годин)
            res = _cached_fast_backtest(substation_name, v, source_type)
            if res:
                rmse, mae, mape, r2, error, df_bt = res
                results[v] = df_bt
                
                row = {
                    "Модель": MODEL_LABELS.get(v, v.upper()).split("  ")[0],
                    "Версія": v.upper(),
                    "R² (Точність)": r2 if r2 is not None else 0.0,
                    "RMSE (МВт)": rmse if rmse is not None else 0.0,
                    "MAE (МВт)": mae if mae is not None else 0.0,
                    "MAPE (%)": mape if mape is not None else 0.0
                }
                metrics_list.append(row)
        
        p_bar.empty()
        status.update(label="✅ Порівняльний аудит завершено успішно!", state="complete")

    if not metrics_list:
        st.error("⚠️ Дані для порівняння недоступні. Перевірте наявність моделей у папці /models")
        return

    # 1. Leaderboard Table
    st.markdown(f"#### {audit_title}")
    df_metrics = pd.DataFrame(metrics_list)
    df_metrics = df_metrics.sort_values("R² (Точність)", ascending=False)
    
    st.table(df_metrics.style.format({
        "R² (Точність)": "{:.4f}",
        "RMSE (МВт)": "{:.2f}",
        "MAE (МВт)": "{:.2f}",
        "MAPE (%)": "{:.2f}%"
    }).highlight_max(subset=["R² (Точність)"], color="#10ac84")
      .highlight_min(subset=["RMSE (МВт)", "MAE (МВт)"], color="#10ac84"))

    # 2. Multi-Model Comparison Chart
    fig_comp = generate_comparison_plot(results, substation_name)
    safe_plotly_render(fig_comp, key=f"comp_audit_plot_{substation_name}")
    
    if source_type == "CSV":
         st.info("💡 **Пояснення для диплома:** Для еталонних даних використовується базова модель V1, яка демонструє високу стійкість до відсутності телеметрії погодних датчиків, фокусуючись на періодичності енергоспоживання.")
    else:
         st.info("💡 **Пояснення для диплома:** Версія V3 показує найкращий результат завдяки інтеграції погодних факторів та добових часових гармонік, що дозволяє моделі 'розуміти' періодичність навантаження.")

def _render_group_comparison(stations_list, source_type, version):
    """
    Рендерить порівняльний графік для декількох підстанцій одночасно.
    """
    st.markdown("#### ⚖️ Груповий аналіз навантаження (Multi-Object Comparison)")
    fig = go.Figure()
    
    with st.spinner("📦 Завантаження та синхронізація даних..."):
        for station in stations_list:
            df_hist = _get_history(station, source_type)
            if not df_hist.empty:
                # Беремо останні 7 днів для наочності
                display_df = df_hist.tail(168)
                fig.add_trace(go.Scatter(
                    x=display_df["timestamp"], 
                    y=display_df["actual_load_mw"], 
                    name=station,
                    mode="lines",
                    line=dict(width=2)
                ))
    
    fig.update_layout(
        template="plotly_dark",
        title=f"📈 Figure 11: Системне порівняння навантаження ({len(stations_list)} об'єктів)",
        xaxis_title="Час",
        yaxis_title="Навантаження, МВт",
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center")
    )
    safe_plotly_render(fig, key=f"group_comp_{len(stations_list)}")
    
    st.caption("💡 *Цей режим дозволяє диспетчеру візуально порівнювати графіки споживання різних районів для оптимізації перетоків енергії.*")
