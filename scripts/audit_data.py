import sys
import os
import pandas as pd
import numpy as np

# Додаємо корінь проєкту до PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.train_lstm import load_data_from_db

def audit_v3_data():
    print("📊 Запуск аудиту даних для моделi v3...")
    df = load_data_from_db(version="v3")
    
    if df.empty:
        print("❌ Дані порожні!")
        return

    print(f"✅ Всього рядків: {len(df)}")
    print("\n--- Описова статистика ---")
    print(df.describe())
    
    print("\n--- Пропуски (NaN) ---")
    print(df.isnull().sum())
    
    print("\n--- Частка нульових значень (%) ---")
    for col in df.columns:
        zero_percent = (df[col] == 0).sum() / len(df) * 100
        print(f"{col}: {zero_percent:.2f}%")
        
    print("\n--- Кореляція з load_mw ---")
    print(df.corr()['load_mw'].sort_values(ascending=False))

if __name__ == "__main__":
    audit_v3_data()
