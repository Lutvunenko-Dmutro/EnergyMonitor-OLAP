"""
АНАЛІЗАТОР МЕТРИК ТЕКСТУ ДИПЛОМА (Thesis Metrics Analyzer)
=========================================================
Допоміжна утиліта для автоматизованого підрахунку фізичного обсягу дипломної роботи.
Ключові можливості:
1. Automated Volume Analytics: сканування розділів та підрахунок кількості сторінок.
2. COM Integration: використання MS Word API для точного вимірювання статистики.
3. Academic Progress Reporting: формування звіту про обсяг для контролю вимог ДСТУ.
4. Batch Processing: швидка обробка DOCX-файлів без ручного втручання.
Забезпечує точний контроль кількісних показників дисертаційного проєкту.
"""
import os
import win32com.client as win32

def get_stats():
    folder = os.path.abspath(r"docs\thesis\check_pages")
    word = win32.Dispatch("Word.Application")
    word.Visible = False
    
    print("\n--- ФІНАЛЬНИЙ ЗВІТ ПОСТОРІНКОВОГО ЗАМІРУ ---")
    print(f"{'Файл':45} | {'Сторінки'}")
    print("-" * 60)
    
    total = 0
    # Сортуємо для зручності читання
    files = sorted([f for f in os.listdir(folder) if f.endswith(".docx")])
    
    for f in files:
        path = os.path.join(folder, f)
        try:
            doc = word.Documents.Open(path)
            pages = doc.ComputeStatistics(2)
            print(f"{f:45} | {pages} стор.")
            total += pages
            doc.Close(False)
        except Exception as e:
            print(f"Помилка при читанні {f}: {e}")
            
    print("-" * 60)
    print(f"{'РАЗОМ (Сума частин)':45} | {total} стор.")
    print("=" * 60)
    word.Quit()

if __name__ == "__main__":
    get_stats()
