"""
НЕЙРОННИЙ ДЕТЕКТОР АВТОРСТВА (Deep AI Authorship Checker)
========================================================
Модуль для глибокої перевірки тексту на наявність ознак генерації ШІ.
Забезпечує:
1. Transformer-based Classification: використання RoBERTa для розпізнавання тексту ChatGPT.
2. Paragraph Sentiment Profiling: поблочний аналіз сегментів для виявлення "аномалій".
3. Probability Scoring: розрахунок коефіцієнта впевненості моделі в авторстві.
4. Academic Integrity Guard: інструмент підтвердження самостійності написання роботи.
Служить фінальним фільтром якості перед подачею документації на перевірку.
"""
import sys
import os
from docx import Document

# Спробуємо імпортувати бібліотеки для ШІ-аналізу
try:
    from transformers import pipeline
    import torch
except ImportError:
    print(" [!] Для глибокого аналізу потрібно встановити бібліотеки:")
    print(" pip install transformers torch")
    sys.exit(1)

def deep_check(file_path):
    print(f"\n>>> ЗАПУСК НЕЙРОННОГО АНАЛІЗУ: {os.path.basename(file_path)} <<<")
    print(" [⏳] Завантаження моделі RoBERTa (може зайняти час при першому запуску)...")
    
    try:
        # Використовуємо одну з найкращих моделей для детекції ШІ
        pipe = pipeline("text-classification", model="Hello-SimpleAI/chatgpt-detector-roberta")
    except Exception as e:
        print(f" [❌] Помилка завантаження моделі: {e}")
        return

    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if len(p.text) > 150] # Беремо тільки довгі абзаци
    
    print(f" [🔍] Аналізуємо {len(paragraphs)} великих абзаців...\n")
    
    ai_scores = []
    for i, text in enumerate(paragraphs[:15]): # Обмежимо 15-ма для швидкості тесту
        # Модель повертає 'ChatGPT' або 'Human'
        result = pipe(text[:512])[0] # Обмежуємо довжину тексту для моделі
        label = result['label']
        score = result['score']
        
        status = "⚠️ ШІ" if label == "ChatGPT" else "✅ ЛЮДИНА"
        print(f" Абзац {i+1:02}: {status} (впевненість: {round(score*100, 1)}%)")
        
        if label == "ChatGPT":
            ai_scores.append(score)
            
    print("\n" + "="*40)
    if not ai_scores:
        print(" [🎉] ВЕРДИКТ: Модель вважає цей текст ПОВНІСТЮ ЛЮДСЬКИМ.")
    else:
        avg_ai = sum(ai_scores) / len(paragraphs[:15])
        if avg_ai > 0.7:
            print(f" [🚨] ВЕРДИКТ: ВИСОКА ЙМОВІРНІСТЬ ШІ ({round(avg_ai*100, 1)}%)")
        else:
            print(f" [🤔] ВЕРДИКТ: Текст має ознаки редагування або змішаного стилю.")
    print("="*40 + "\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "docs/thesis/THESIS_FINAL_NO_MERMAID_AT_ALL.docx"
    deep_check(target)
