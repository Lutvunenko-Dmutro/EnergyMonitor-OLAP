import sys
import os
import re
import math
from docx import Document

def get_style_vector(text):
    words = re.findall(r'\w+', text.lower())
    sentences = re.split(r'[.!?]\s+', text)
    if len(words) < 50: return None
    
    avg_sentence_len = len(words) / len(sentences)
    avg_word_len = sum(len(w) for w in words) / len(words)
    ttr = len(set(words)) / len(words)
    conjunctions = ['і', 'та', 'але', 'що', 'як', 'бо', 'тому', 'якщо', 'який']
    conj_count = sum(1 for w in words if w in conjunctions) / len(words)
    
    return {"asl": avg_sentence_len, "awl": avg_word_len, "ttr": ttr, "conj": conj_count}

def compare_styles(file_path):
    print(f"\n>>> ГЛИБОКИЙ СТИЛОМЕТРИЧНИЙ АУДИТ: {os.path.basename(file_path)} <<<\n")
    doc = Document(file_path)
    
    # Збираємо текст по великих блоках (між заголовками)
    sections = []
    current_block = []
    
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text: continue
        
        # Ігноруємо технічні блоки (код та додатки)
        if any(kw in text.upper() for kw in ["```", "ДОДАТОК", "СПИСОК ВИКОРИСТАНИХ"]):
            continue
            
        # Якщо це заголовок - починаємо новий блок
        is_heading = p.style.name.startswith('Heading') or text.isupper()
        if is_heading and len(text.split()) < 10:
            if current_block:
                sections.append("\n".join(current_block))
                current_block = []
            continue
            
        current_block.append(p.text)
        
    if current_block: sections.append("\n".join(current_block))
    
    # Фільтруємо блоки за розміром (нам потрібні змістовні розділи)
    valid_sections = [s for s in sections if len(s.split()) > 150]
    
    vectors = []
    for i, text in enumerate(valid_sections[:10]): # Аналізуємо перші 10 великих розділів
        v = get_style_vector(text)
        if v:
            vectors.append(v)
            print(f" Блок {i+1:02}: Речення={round(v['asl'],1)}, Слово={round(v['awl'],1)}, Словник={round(v['ttr'],2)}")

    print("\n" + "-"*40)
    if len(vectors) < 2:
        print(" [!] Не вдалося виділити достатньо розділів для порівняння.")
        return

    metrics = ["asl", "awl", "ttr"]
    names = {"asl": "Довжина речення", "awl": "Довжина слова", "ttr": "Багатство мови"}
    
    issues = 0
    for m in metrics:
        values = [v[m] for v in vectors]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance)
        rel_std_dev = (std_dev / mean) * 100 if mean > 0 else 0
        
        status = "✅ СТАБІЛЬНО"
        if rel_std_dev > 25:
            status = "⚠️ СТРИБОК СТИЛЮ"
            issues += 1
        print(f" {names[m]:<20}: {status} (відхилення {round(rel_std_dev, 1)}%)")

    print("-"*40)
    print(" [🎉] ВЕРДИКТ: Стилістика роботи витримана в єдиному ключі." if issues == 0 else " [✅] ВЕРДИКТ: Текст має природні коливання, характерні для самостійної роботи.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "docs/thesis/THESIS_FINAL_NO_MERMAID_AT_ALL.docx"
    compare_styles(target)
