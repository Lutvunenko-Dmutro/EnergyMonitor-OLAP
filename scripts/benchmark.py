import os
import sys
import time
from deepface import DeepFace

# Головна папка та список емоцій для тестування
dataset_path = "dataset"
target_emotions = ['happy', 'sad', 'angry', 'neutral']

print("=== Етап 1: Підготовка тестового середовища ===")

# Автоматичне створення головної папки
os.makedirs(dataset_path, exist_ok=True)

# Створення підпапок для кожної емоції
for emotion in target_emotions:
    folder_path = os.path.join(dataset_path, emotion)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"📁 Створено нову папку: {folder_path}")

# Рахуємо, скільки всього файлів є у папках
total_images_found = 0
for emotion in target_emotions:
    folder_path = os.path.join(dataset_path, emotion)
    total_images_found += len(os.listdir(folder_path))

# Якщо фотографій немає, зупиняємо програму і даємо інструкцію
if total_images_found == 0:
    print("\n⚠️ Тестові папки наразі порожні.")
    print(f"👉 Закиньте хоча б по 1-2 фотографії людей у відповідні папки всередині '{dataset_path}' (наприклад, радісних людей у папку 'happy').")
    print("Після цього запустіть цей скрипт ще раз!")
    sys.exit()

# === Етап 2: Тестування ===
print(f"\nЗнайдено {total_images_found} фотографій. Починаємо тестування моделі: DeepFace...\n")

correct_predictions = 0
processed_count = 0
start_time = time.time()

for true_emotion in target_emotions:
    folder_path = os.path.join(dataset_path, true_emotion)
    
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        processed_count += 1

        try:
            # Аналіз фотографії
            result = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)
            pred_emotion = result[0]['dominant_emotion'] if isinstance(result, list) else result['dominant_emotion']

            # Перевірка результату
            if pred_emotion == true_emotion:
                correct_predictions += 1
                status = "✅ ВГАДАНО"
            else:
                status = "❌ ПОМИЛКА"
            
            print(f"[{processed_count}/{total_images_found}] Файл: {image_name} | Справжня: {true_emotion: <8} | Прогноз: {pred_emotion: <8} | {status}")
            
        except Exception:
            print(f"[{processed_count}/{total_images_found}] Файл: {image_name} | ⚠️ Помилка зчитування")

end_time = time.time()

# === Етап 3: Результати ===
accuracy = (correct_predictions / processed_count) * 100 if processed_count > 0 else 0
processing_time = end_time - start_time
fps = processed_count / processing_time if processing_time > 0 else 0

print("\n" + "="*40)
print("🏆 ФІНАЛЬНІ РЕЗУЛЬТАТИ: DeepFace")
print("="*40)
print(f"Всього оброблено фото: {processed_count}")
print(f"Правильних відповідей: {correct_predictions}")
print(f"Точність (Accuracy):   {accuracy:.2f}%")
print(f"Швидкість обробки:     {fps:.2f} фото/сек")
print(f"Загальний час:         {processing_time:.2f} сек")
print("="*40)