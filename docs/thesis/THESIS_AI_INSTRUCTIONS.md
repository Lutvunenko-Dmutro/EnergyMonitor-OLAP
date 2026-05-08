# INSTRUCTIONS FOR AI ASSISTANTS (CLAUDE, COPILOT, ANTIGRAVITY)

This project is a Bachelor's Thesis. To maintain quality and institutional compliance, follow these rules strictly:

## 1. Build Process
- Main Command: `python scripts/thesis/convert_thesis.py --all`
- The script automatically:
    1. Kills MS Word processes to avoid file locking.
    2. Converts all `.md` sections in `docs/thesis/` to individual `.docx` files in `docs/thesis/check_pages/`.
    3. Merges all sections using `scripts/thesis/merge_thesis.py` into a single file `docs/thesis/THESIS_FULL_FINAL_UTF8.md`.
    4. Generates the final submission document: `docs/thesis/Литвиненко_YYYYMMDD.docx`.

## 2. Content Style (Humanization Rules)
- **NO JARGON**: Avoid "AI-smell" words: *трансформація, парадигма, екосистема, цифровізація (as a buzzword), безшовний, глибока інтеграція, динамічний сценарій*.
- **BE CONCRETE**: Instead of "allows to improve results", use specific technical facts (e.g., "reduces error MAPE to 3.1%", "uses physics.py for transformer simulation").
- **TONE**: Dry, technical, academic Ukrainian. Like a senior engineering student.
- **FORMATTING**: 
    - No bold headings in lists (e.g., avoid `* **Title**: Text`). Use plain text.
    - Figures must have sources: `*Рис. X.Y. Назва рисунка (згенеровано автором за допомогою [Tool])*`.

## 3. Formatting Standards
- Figures: Centered, captions below.
- Tables: Captions above.
- Formulas: Centered, numbered on the right `(3.1)`.

## 4. Final File Naming
- Always name the final file: `Литвиненко_YYYYMMDD.docx` where YYYYMMDD is the current date.

---
*Note: If you are asked to "polish" or "fix" the text, refer to these rules first.*
