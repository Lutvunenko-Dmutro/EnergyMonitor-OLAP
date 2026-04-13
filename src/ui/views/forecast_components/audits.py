import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.ml.forecast_controller import cached_fast_backtest as _cached_fast_backtest
from src.ml.forecast_controller import get_cached_history as _get_history
from src.utils.ui_helpers import safe_plotly_render
from src.ui.views.forecast_components.constants import MODEL_LABELS

def _render_comparative_audit(substation_name, source_type):
    """
    Виконує порівняльний аналіз трьох поколінь LSTM (V1, V2, V3) 
    та відображає порівняльну таблицю і графік.
    """
    from src.ml.backtest import get_fast_backtest
    from src.ui.components.charts import generate_comparison_plot
    from src.ui.views.forecast_components.engine import get_stations_to_process # Імпортуємо напряму з двигуна
    
    # Перевіряємо, чи ввімкнено режим порівняння моделей в UI
    is_multi_requested = st.session_state.get("tab_multi_model_toggle", False)
    
    # Визначаємо версії
    if source_type == "CSV" and not is_multi_requested:
        versions = ["v1"]
    else:
        versions = ["v1", "v2", "v3"]

    def _execute_audit_flow(target_name, title_prefix=""):
        res_dict = {}
        mlist = []
        for v in versions:
            res = _cached_fast_backtest(target_name, v, source_type)
            if res:
                rmse, mae, mape, r2, error, df_bt = res
                res_dict[v] = df_bt
                mlist.append({
                    "Модель": MODEL_LABELS.get(v, v.upper()).split("  ")[0],
                    "Версія": v.upper(),
                    "R² (Точність)": r2 if r2 is not None else 0.0,
                    "RMSE (МВт)": rmse if rmse is not None else 0.0,
                    "MAE (МВт)": mae if mae is not None else 0.0,
                    "MAPE (%)": mape if mape is not None else 0.0,
                    "df": df_bt
                })
        
        if not mlist: 
            st.warning(f"⚠️ Не вдалося отримати дані для {target_name}")
            return
        
        st.markdown(f"#### {title_prefix}")
        
        # Створюємо вкладки для чистоти інтерфейсу
        tb_comp, tb_academic, tb_metrics = st.tabs(["📈 Порівняння", "📊 Діагностика (Best)", "📋 Метрики"])
        
        with tb_comp:
            f_comp = generate_comparison_plot(res_dict, target_name)
            safe_plotly_render(f_comp, key=f"comp_audit_p_{target_name}")
            
        with tb_academic:
            from src.ui.components.charts.academic import generate_academic_plots
            _, f_dist, f_scat = generate_academic_plots(res_dict, target_name)
            
            if f_dist and f_scat:
                # Виводимо тільки Figure 7 та 8, щоб уникнути повторів з першою вкладкою
                safe_plotly_render(f_dist, key=f"acad_dist_multi_{target_name}")
                st.divider()
                safe_plotly_render(f_scat, key=f"acad_scat_multi_{target_name}")
            else:
                st.warning("⚠️ Недостатньо даних для побудови порівняльної діагностики.")
            
        with tb_metrics:
            df_m = pd.DataFrame(mlist).drop(columns=["df"]).sort_values("R² (Точність)", ascending=False)
            st.table(df_m.style.format({
                "R² (Точність)": "{:.4f}", "RMSE (МВт)": "{:.2f}",
                "MAE (МВт)": "{:.2f}", "MAPE (%)": "{:.2f}%"
            }).highlight_max(subset=["R² (Точність)"], color="#10ac84"))

    # --- 1. АУДИТ ВИБРАНОГО ОБ'ЄКТА ---
    # Якщо вибрано конкретну станцію - показуємо аудит відразу.
    # Якщо вибрано "Усі підстанції" - не показуємо загальний блок, щоб уникнути дублювання.
    if substation_name != "Усі підстанції":
        st.markdown(f"### 🧪 Комплексний аудит: {substation_name}")
        with st.status(f"🚀 Розрахунок аудиту для {substation_name}...", expanded=True) as status:
            _execute_audit_flow(substation_name, "Результати аналізу об'єкта")
            status.update(label="✅ Аудит завершено!", state="complete")

    # --- 2. ДЕТАЛІЗАЦІЯ ПO СТАНЦІЯХ (якщо обрано 'Усі') ---
    if substation_name == "Усі підстанції":
        st.markdown("### 📍 Деталізація по об'єктах мережі")
        st.caption("Оберіть підстанцію нижче для перегляду індивідуальної точності нейромоделей.")
        
        stations = get_stations_to_process(substation_name, source_type)
        
        for s in stations:
            with st.expander(f"📊 ПС: {s}", expanded=False):
                _execute_audit_flow(s, f"Аналітика точності: {s}")

    st.info("💡 **Пояснення для диплома:** Порівняння архітектур дозволяє оцінити стабільність прогнозів. V3 інтегрує погодні фактори, що критично для сонячних днів та пікових навантажень.")

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
