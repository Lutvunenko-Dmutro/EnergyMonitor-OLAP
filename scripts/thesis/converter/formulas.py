"""
ДВИГУН МАТЕМАТИЧНОЇ ТРАНСФОРМАЦІЇ (LaTeX-to-Word Math Engine)
===========================================================
Спеціалізований модуль для конвертації наукової нотації в нативні об'єкти Word.
Забезпечує:
1. LaTeX Parsing: вилучення та очищення математичних виразів з Markdown-контенту.
2. MathML Generation: перетворення формул у XML-представлення (MathML).
3. COM Automation Integration: вставлення формул у Word через буфер обміну (MS Word API).
4. Final Document Polishing: оновлення Змісту та полів документа після вставки об'єктів.
Гарантує професійний вигляд математичних доказів у дипломній роботі.
"""
import re
import os
import time
import win32com.client as win32
import win32clipboard
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from latex2mathml.converter import convert as latex_to_mathml
from .styles import set_run_font

def add_formula(doc, latex_text):
    latex = re.sub(r'^\$\$?|\$\$?$', '', latex_text.strip()).strip()
    if not latex: return
    p = doc.add_paragraph()
    run = p.add_run(f"⇲{latex}⇱")
    set_run_font(run, 14)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(6), Pt(6)
    p.paragraph_format.first_line_indent = Cm(0)

def paste_mathml(text):
    for _ in range(10):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return
        except Exception: time.sleep(0.1)
    raise Exception("Clipboard Locked!")

def convert_formulas_to_word_objects(docx_path):
    print("Запуск COM-автоматизації для перетворення 2D формул...")
    word = win32.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc_word = word.Documents.Open(os.path.abspath(docx_path))
        word.Selection.HomeKey(Unit=6)
        find = word.Selection.Find
        find.ClearFormatting()
        find.MatchWildcards = False
        math_count = 0
        while True:
            find.Text = "⇲"
            if not find.Execute(): break
            start_pos = word.Selection.Start
            word.Selection.Collapse(Direction=0)
            find.Text = "⇱"
            if not find.Execute(): break
            end_pos = word.Selection.End
            rng = doc_word.Range(start_pos, end_pos)
            formula = rng.Text.replace("⇲", "").replace("⇱", "").strip().replace(r'\quad', r'\ ')
            try:
                mathml = latex_to_mathml(formula)
                paste_mathml(mathml)
                time.sleep(0.05)
                rng.Paste()
                math_count += 1
            except Exception as e:
                print(f"Помилка [{formula}]: {e}")
                rng.Text = f"[{formula}]"
            word.Selection.Collapse(Direction=0)
        # Оновлення Змісту та всіх полів (TOC update)
        print("Оновлення Змісту та номерів сторінок...")
        for toc in doc_word.TablesOfContents:
            toc.Update()
        doc_word.Fields.Update()
        
        doc_word.Save()
        print(f"✅ Успішно відформатовано {math_count} формул та оновлено Зміст!")
    finally:
        try:
            doc_word.Close()
            word.Quit()
        except: pass
