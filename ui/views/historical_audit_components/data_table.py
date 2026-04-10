import streamlit as st

def render_raw_data_table(df, start_date, end_date):
    """
    Renders the interactive data table and download button for the Digital Archive.
    """
    st.divider()
    st.subheader("📋 Детальні дані (Raw Data)")

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

    num_cols = [c for c in ["Навантаження (МВт)", "Повітря (°C)", "Масло (°C)", "H₂ (ppm)", "Health (%)"] if c in df_display.columns]
    df_display[num_cols] = df_display[num_cols].fillna(0.0)

    st.dataframe(
        df_display.style.format({col: "{:.2f}" for col in num_cols}),
        use_container_width=True,
        height=400,
    )

    st.divider()
    c_down1, _ = st.columns([1, 2])
    with c_down1:
        csv_bytes = df_display.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Скачати CSV",
            data=csv_bytes,
            file_name=f"archive_{start_date}_{end_date}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Гарантований відступ внизу для скролінгу
    st.markdown('<div style="height: 300px;"></div>', unsafe_allow_html=True)
