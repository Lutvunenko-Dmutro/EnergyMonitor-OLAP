"""
ДВИГУН ФОРМАТУВАННЯ ТА КОНВЕРТАЦІЇ ТЕЗИ (Thesis Layout Engine)
=============================================================
Ядро системи трансформації Markdown-тексту в професійно оформлений Word-документ.
Ключові можливості:
1. Intelligent Markdown Parsing: розпізнавання заголовків, списків, зображень та блоків коду.
2. Word Object Transformation: перетворення LaTeX-формул у нативні об'єкти Word.
3. Academic Formatting Enforcement: налаштування відступів та шрифтів за вимогами ДСТУ.
4. Dynamic TOC & Pagination: автоматична генерація змісту та нумерації сторінок.
5. Mermaid Filtering: інтелектуальне очищення схем, що призначені лише для веб-версії.
Забезпечує високу якість фінальної верстки пояснювальної записки до диплома.
"""
import os
import re
from docx import Document
from docx.shared import Cm, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from .config import MERMAID_MAP
from .styles import add_page_numbers, add_formatted_run
from .handlers import (
    add_h1, add_h2, add_h3, add_h4, add_body, 
    add_list_item, add_image, add_code, add_table
)
from .formulas import add_formula, convert_formulas_to_word_objects
from .appendix import add_source_code_appendix

NAV_PATTERN = re.compile(r'\[.*?(Назад до|Далі:|Повернутись|⬅️|➡️).*?\]\(.*?\.md\)')

def run_conversion(input_md, output_docx, include_appendix=True):
    if not os.path.exists(input_md):
        print(f" [ERR] Input not found: {input_md}")
        return

    with open(input_md, encoding="utf-8") as f:
        lines = f.readlines()

    doc = Document()
    section = doc.sections[0]
    section.left_margin, section.right_margin = Cm(3.0), Cm(1.0)
    section.top_margin, section.bottom_margin = Cm(2.0), Cm(2.0)

    in_code, code_buf, code_lang = False, [], ""
    in_table = False; in_math = False; table_buf = []; math_buf = []; last_was_image = False
    in_mermaid = False

    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\r\n')
        i += 1
        
        stripped = line.strip()

        # Ігноруємо блоки Mermaid та їхні підписи (вони тільки для GitHub)
        if stripped.startswith('```mermaid'):
            in_mermaid = True
            continue
        if in_mermaid:
            if stripped.startswith('```'):
                in_mermaid = False
            continue
            
        # Ігноруємо підписи до Mermaid схем
        if re.search(r'Схема\s+\d+\.\d+\..*\(Mermaid-версія', stripped):
            continue

        # Фільтрація навігації
        if NAV_PATTERN.search(line) and len(line.strip()) < 150: continue

        # Блоки коду
        if line.startswith('```'):
            last_was_image = False
            if in_code:
                if code_lang != "mermaid":
                    add_code(doc, code_buf)
                code_buf = []; in_code = False; code_lang = ""
            else:
                in_code = True
                code_lang = line[3:].strip().lower()
            continue
        if in_code: code_buf.append(line); continue

        # Блоки формул $$
        if line.strip().startswith('$$'):
            last_was_image = False
            if in_math:
                full_math = " ".join(math_buf) + " " + line.strip().replace('$$', '')
                add_formula(doc, full_math.strip())
                math_buf = []; in_math = False
            else:
                if line.strip().endswith('$$') and len(line.strip()) > 2:
                    add_formula(doc, line.strip())
                else:
                    in_math = True
                    math_buf = [line.strip().replace('$$', '')]
            continue
        if in_math: math_buf.append(line.strip()); continue

        # Таблиці
        if line.strip().startswith('|'):
            last_was_image = False
            if not in_table: in_table, table_buf = True, []
            table_buf.append(line); continue
        elif in_table:
            add_table(doc, table_buf); table_buf = []; in_table = False

        if not stripped or re.match(r'^---+$', stripped): continue

        # Обробка інлайнових формул у тексті
        def process_inline_math(text):
            return re.sub(r'\$(.+?)\$', r'⇲\1⇱', text)

        # Перевірка на відсутність картинки перед підписом Рис.
        if re.search(r'^\*Рис\..+\*', stripped):
            if not last_was_image:
                p = doc.add_paragraph()
                run = p.add_run("[УВАГА: ВІДСУТНЄ ЗОБРАЖЕННЯ ДЛЯ ЦЬОГО ПІДПИСУ!]")
                run.font.bold = True
                from docx.shared import RGBColor
                run.font.color.rgb = RGBColor(255, 0, 0)
            last_was_image = False # Скидаємо після підпису

        if stripped.startswith('####'): 
            text = re.sub(r'^####\s*', '', stripped)
            add_h4(doc, process_inline_math(text))
            last_was_image = False
        elif stripped.startswith('###'): 
            text = re.sub(r'^###\s*', '', stripped)
            add_h3(doc, process_inline_math(text))
            last_was_image = False
        elif stripped.startswith('##'): 
            text = re.sub(r'^##\s*', '', stripped)
            add_h2(doc, process_inline_math(text))
            last_was_image = False
        elif stripped == "<br>":
            doc.add_paragraph()
            continue
            
        elif stripped.startswith('#'):
            text = re.sub(r'^#\s*', '', stripped)
            # ВСТАВКА ЗМІСТУ ПЕРЕД СКОРОЧЕННЯМИ (Згідно п. 6.1: Реферат -> Зміст -> Скорочення)
            if "СКОРОЧЕНЬ" in text.upper() or "ПОЗНАЧЕНЬ" in text.upper():
                doc.add_page_break()
                p_toc = doc.add_paragraph()
                p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_formatted_run(p_toc, "ЗМІСТ", size=16, bold_base=True)
                
                p_field = doc.add_paragraph()
                run = p_field.add_run()
                # Вставка поля TOC (Table of Contents)
                fldChar1 = OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'), 'begin')
                instrText = OxmlElement('w:instrText'); instrText.text = ' TOC \\o "1-3" \\h \\z \\u '
                fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'), 'separate')
                fldChar3 = OxmlElement('w:fldChar'); fldChar3.set(qn('w:fldCharType'), 'end')
                run._r.append(fldChar1); run._r.append(instrText); run._r.append(fldChar2); run._r.append(fldChar3)
                
                doc.add_page_break()

            add_h1(doc, process_inline_math(text))
            last_was_image = False
        elif re.match(r'^Додаток\s+[А-Яа-яA-Za-z]', stripped): add_h1(doc, stripped); last_was_image = False
        elif re.search(r'!\[(.*?)\]\((.*?)\)', stripped):
            m = re.search(r'!\[(.*?)\]\((.*?)\)', stripped)
            add_image(doc, os.path.basename(m.group(2)), m.group(1))
            last_was_image = True
        elif re.match(r'^(\*\*)?\d+\.\s', stripped): 
            add_list_item(doc, process_inline_math(stripped), numbered=True)
            last_was_image = False
        elif stripped.startswith('* ') or stripped.startswith('- '): 
            add_list_item(doc, process_inline_math(stripped[2:]))
            last_was_image = False
        else: 
            add_body(doc, process_inline_math(line))
            # Не скидаємо last_was_image, якщо це порожній рядок або просто текст? 
            # Хоча зазвичай підпис йде одразу після картинки або через порожній рядок.
            if stripped: last_was_image = False

    if in_table: add_table(doc, table_buf)
    
    if include_appendix:
        add_source_code_appendix(doc, "src")
        
    add_page_numbers(doc)
    doc.save(output_docx)
    print(f"✅ Документ збережено: {output_docx}")
    
    convert_formulas_to_word_objects(output_docx)
