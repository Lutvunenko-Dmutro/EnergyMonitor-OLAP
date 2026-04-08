import glob
import os

import pandas as pd

KAGGLE_MAPPING = {
    "AEP": "Американська електрична компанія (AEP)",
    "COMED": "Енергомережа Commonwealth Edison (Чикаго)",
    "DAYTON": "Енергомережа м. Дейтон (Огайо)",
    "DEOK": "Енергомережа Duke Energy (Огайо/Кентуккі)",
    "DOM": "Енергомережа Dominion (Вірджинія)",
    "DUQ": "Енергомережа Duquesne (Піттсбург)",
    "EKPC": "Енергокооператив Східного Кентуккі (EKPC)",
    "FE": "Компанія FirstEnergy",
    "NI": "Північний Іллінойс (Хаб)",
    "PJME": "Східний регіон PJM (США)",
}


def load_kaggle_data():
    """
    Зчитує та денормалізує дані з еталонної Kaggle директорії за масками файлів *_hourly.csv.

    :return:pd.DataFrame Об'єднаний DataFrame з колонками: timestamp, actual_load_mw, substation_name, region_name.
    """
    data_dir = "data"
    csv_files = glob.glob(os.path.join(data_dir, "*_hourly.csv"))

    all_dfs = []

    for file_path in csv_files:
        try:
            # Читаємо файл
            df = pd.read_csv(file_path)
            if df.empty:
                continue

            # Визначення префіксу файлу для ідентифікації підстанції
            base = os.path.basename(file_path)
            prefix = base.replace("_hourly.csv", "")

            # Стандартизація колонки часу (timestamp)
            dt_cols = [c for c in df.columns if c.lower() in ["datetime", "timestamp"]]
            if dt_cols:
                df = df.rename(columns={dt_cols[0]: "timestamp"})
            else:
                continue  # Скіпаємо якщо немає колонки часу

            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

            # Стандартизація колонки навантаження (actual_load_mw)
            load_cols = [
                c
                for c in df.columns
                if "_mw" in c.lower()
                or "load" in c.lower()
                or c.upper() == f"{prefix.upper()}_MW"
            ]
            if load_cols:
                df = df.rename(columns={load_cols[0]: "actual_load_mw"})
            else:
                continue  # Скіпаємо якщо не знайдено навантаження

            df["actual_load_mw"] = pd.to_numeric(df["actual_load_mw"], errors="coerce")

            # Мапінг локальних ідентифікаторів на розгорнуті назви (Pretty Name)
            pretty_name = KAGGLE_MAPPING.get(prefix.upper(), prefix)
            df["substation_name"] = pretty_name
            df["region_name"] = (
                pretty_name  # Забезпечення підтримки фільтрації регіонів
            )

            df = df[["timestamp", "actual_load_mw", "substation_name", "region_name"]]
            df = df.dropna(subset=["timestamp", "actual_load_mw"])
            
            # РАДИКАЛЬНА ОПТИМІЗАЦІЯ: Обрізаємо дані ОДРАЗУ після завантаження одного файлу,
            # до того як вони потраплять у великий загальний масив
            df = df.sort_values("timestamp").tail(5000)

            all_dfs.append(df)

        except Exception:
            # Ігноруємо биті файли, йдемо далі
            continue

    if not all_dfs:
        return pd.DataFrame(
            columns=["timestamp", "actual_load_mw", "substation_name", "region_name"]
        )

    # Об'єднуємо (тепер масив вже маленький)
    full_df = pd.concat(all_dfs, ignore_index=True)
    
    from src.core.database import memory_diet
    return memory_diet(full_df)
