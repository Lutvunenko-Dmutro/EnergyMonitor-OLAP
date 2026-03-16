import os

import streamlit as st

from src.core.database import run_query

# Визначення шляхів до збережених моделей та скейлерів
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_MODEL_PATH = os.path.join(_BASE_DIR, "models", "substation_model_v2.h5")
_SCALER_PATH = os.path.join(_BASE_DIR, "models", "scaler_v2.pkl")

from ui.segments.forecast_segments import render_comparison, render_forecast_results


def render(
    selected_substation: str = "Усі підстанції",
    data_source: str = "Синтетична модель (Smart City)",
):
    """
    Точка входу для рендерингу інтерфейсу прогнозування ШІ.

    :param selected_substation: Обрана підстанція або перелік.
    :param data_source: Джерело даних ('Live' / 'CSV').
    """
    try:
        _render_inner(selected_substation, data_source)
    except Exception as exc:
        st.error(f"❌ Критична помилка вкладки Прогноз ШІ: {exc}")
        with st.expander("🔍 Stack trace"):
            import traceback

            st.code(traceback.format_exc())


def _render_inner(selected_substation: str, data_source: str):
    """
    Внутрішній метод рендерингу логіки прогнозування.

    :param selected_substation: Назва обраної підстанції.
    :param data_source: Тип джерела даних.
    """
    st.subheader("🔮 ШІ-прогноз споживання (Batch Analysis)")
    st.markdown(
        "Ця вкладка використовує нейронну мережу **LSTM**, щоб передбачити "
        "навантаження на мережу на основі історичних даних за останні 24 години. "
        "Ви можете обрати кілька підстанцій для масового аналізу."
    )

    # Перевірка наявності файлів моделей в директорії
    model_v3 = os.path.join(_BASE_DIR, "models", "substation_model_v3.h5")
    model_v2 = os.path.join(_BASE_DIR, "models", "substation_model_v2.h5")
    model_v1 = os.path.join(_BASE_DIR, "models", "substation_model_v1.h5")
    scaler_v3 = os.path.join(_BASE_DIR, "models", "scaler_v3.pkl")
    scaler_v2 = os.path.join(_BASE_DIR, "models", "scaler_v2.pkl")
    scaler_v1 = os.path.join(_BASE_DIR, "models", "scaler_v1.pkl")

    with st.sidebar.expander("🛠️ AI Diagnostics", expanded=False):
        st.write("**Weights Checklist:**")
        st.write(
            f"- **V1** Model: {'🟢 Знайдено' if os.path.exists(model_v1) else '🔴 Відсутній'}"
        )
        st.write(
            f"- **V1** Scaler: {'🟢 Знайдено' if os.path.exists(scaler_v1) else '🔴 Відсутній'}"
        )
        st.markdown("---")
        st.write(
            f"- **V2** Model: {'🟢 Знайдено' if os.path.exists(model_v2) else '🔴 Відсутній'}"
        )
        st.write(
            f"- **V2** Scaler: {'🟢 Знайдено' if os.path.exists(scaler_v2) else '🔴 Відсутній'}"
        )
        st.markdown("---")
        st.write(
            f"- **V3** Model: {'🟢 Знайдено' if os.path.exists(model_v3) else '🔴 Відсутній'}"
        )
        st.write(
            f"- **V3 Scaler**: {'🟢 Знайдено' if os.path.exists(scaler_v3) else '🔴 Відсутній'}"
        )

    # Перевірка для відсікання
    if (
        not os.path.exists(model_v3)
        and not os.path.exists(_MODEL_PATH)
        and not os.path.exists(model_v1)
    ):
        st.warning("⚠️ Жодна модель LSTM ще не навчена. Прогноз недоступний.")
        st.info(
            "Натренуйте V1: `python ml/train_v1.py` або V3 `python -m ml.train_lstm --version v3`"
        )
        return

    # Налаштування параметрів прогнозування
    st.markdown("### ⚙️ Налаштування параметрів")

    is_kaggle = data_source == "Еталонні дані (Kaggle)"
    model_options = (
        ["V1 (Базова - тільки МВт)"]
        if is_kaggle
        else ["V1 (Базова - тільки МВт)", "V2 (Мультимодальна)", "V3 (Advanced + Час)"]
    )

    # Вибір версії моделі для аналізу
    model_version_name = st.sidebar.selectbox(
        "🧠 Інтелект моделі",
        options=model_options,
        index=0 if is_kaggle else 2,
        disabled=is_kaggle,
        help="Для Kaggle даних доступна лише базова модель V1 (тільки навантаження)."
        if is_kaggle
        else None,
    )
    version_map = {
        "V1 (Базова - тільки МВт)": "v1",
        "V2 (Мультимодальна)": "v2",
        "V3 (Advanced + Час)": "v3",
    }
    selected_version = version_map[model_version_name]

    # Починаємо з порожнього списку
    if "default_idx" not in locals():
        default_idx = 0

    source_type = "CSV" if is_kaggle else "Live"

    # Визначаємо список підстанцій заздалегідь для Live-режиму
    sub_list = ["AEP Region"]
    if source_type == "CSV":
        from src.core.kaggle_loader import load_kaggle_data

        df_all = load_kaggle_data()
        sub_all_list = ["Усі підстанції"] + df_all["substation_name"].unique().tolist()
    else:
        try:
            sub_res = run_query(
                "SELECT substation_name FROM Substations ORDER BY substation_name"
            )
            sub_names = [
                s for s in sub_res["substation_name"].tolist() if s != "AEP Region"
            ]
            sub_all_list = (
                ["Усі підстанції"] + sub_names
                if not sub_res.empty
                else ["Усі підстанції"]
            )
        except Exception:
            sub_all_list = ["Усі підстанції"]

    # Визначення переліку об'єктів для аналізу
    use_aggregate = (
        "Усі підстанції" in selected_substation or not selected_substation
        if isinstance(selected_substation, list)
        else selected_substation == "Усі підстанції"
    )

    if use_aggregate:
        st.info(
            f"🌍 Обрано для аналізу: **Вся мережа** ({len(sub_all_list) - 1} локальних підстанцій)."
        )
        if source_type == "CSV":
            selected_subs = [s for s in sub_all_list if s != "Усі підстанції"]
        else:
            clean_subs = [
                s for s in sub_all_list if s not in ["Усі підстанції", "AEP Region"]
            ]
            selected_subs = ["Усі підстанції"] + clean_subs
    else:
        st.success(f"🎯 Обрано для аналізу: **{', '.join(selected_substation)}**")
        selected_subs = selected_substation

    st.markdown("<br>", unsafe_allow_html=True)

    # Викликаємо фрагменти
    render_comparison(selected_subs, source_type, sub_all_list)
    render_forecast_results(selected_subs, source_type, selected_version)
