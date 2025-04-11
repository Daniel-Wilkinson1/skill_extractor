import os
import re
import pandas as pd
import docx
import fitz  # PyMuPDF
from difflib import get_close_matches

# Define skill synonyms
SKILL_SYNONYMS = {
    "python": ["python programming", "python 3"],
    "cad": ["autocad", "computer-aided design", "2d cad", "3d cad"],
    "fea": ["finite element analysis", "structural simulation"],
    "lca": ["life cycle analysis", "life cycle assessment"],
    "excel": ["microsoft excel", "spreadsheets"],
    "solidworks": ["solid works"],
    "data analysis": ["data analytics", "data mining"],
    "project management": ["pm", "managing projects"],
    "sustainability": ["sustainable design", "sustainable engineering", "environmental impact"]
}

# Canonical skill mapping
PHRASE_TO_SKILL = {}
for canonical, synonyms in SKILL_SYNONYMS.items():
    PHRASE_TO_SKILL[canonical] = canonical
    for s in synonyms:
        PHRASE_TO_SKILL[s] = canonical

# Define categories
skill_categories = {
    "Programming": ["python", "matlab"],
    "Design & CAD": ["cad", "autocad", "solidworks", "3d cad", "2d cad", "computer-aided design"],
    "Analysis": ["fea", "lca", "data analysis", "finite element analysis", "life cycle analysis", "simulation"],
    "Project Management": ["project management", "pm", "managing projects"],
    "Tools": ["excel", "spreadsheets", "microsoft excel"],
    "Sustainability": ["sustainability", "sustainable design", "environmental impact"],
    "PLC systems": ["plc", "plc programming", "Pheonix Contact"]
}

PHRASE_TO_CATEGORY = {}
for category, phrases in skill_categories.items():
    for phrase in phrases:
        PHRASE_TO_CATEGORY[phrase] = category

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

def guess_name(text):
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip()
        if line and len(line.split()) >= 2 and line.replace(' ', '').isalpha():
            return line.title()
    return None

def extract_skills_with_synonyms(text, phrase_map):
    text_lower = text.lower()
    matches = []
    fuzzy_hits = set()
    for phrase, canonical in phrase_map.items():
        if re.search(rf"\b{re.escape(phrase)}\b", text_lower):
            matches.append((canonical, phrase, "exact"))
        else:
            close = get_close_matches(phrase, text_lower.split(), n=1, cutoff=0.9)
            if close:
                fuzzy_hits.add((canonical, phrase, "fuzzy"))
    return matches + list(fuzzy_hits)

def process_cv_folder(cv_folder):
    records = []
    seen = set()  # to avoid duplicate (name, skill) entries
    for file_name in os.listdir(cv_folder):
        if file_name.lower().endswith(('.pdf', '.docx')):
            file_path = os.path.join(cv_folder, file_name)
            text = extract_text_from_pdf(file_path) if file_name.endswith('.pdf') else extract_text_from_docx(file_path)
            matches = extract_skills_with_synonyms(text, PHRASE_TO_SKILL)
            name = guess_name(text) or os.path.splitext(file_name)[0] + " (Guessed)"

            for canonical, phrase, match_type in matches:
                if (name, canonical) in seen:
                    continue
                seen.add((name, canonical))
                category = PHRASE_TO_CATEGORY.get(phrase, "")
                records.append({
                    "name": name,
                    "skill": canonical,
                    "matched_phrase": phrase,
                    "match_type": match_type,
                    "category": category
                })

    return pd.DataFrame(records)

if __name__ == "__main__":
    folder = "cv_uploads"
    os.makedirs(folder, exist_ok=True)
    df = process_cv_folder(folder)
    df.to_excel("hr_skills_auto.xlsx", index=False)
    print("✅ Skill extraction complete.")
    print("📄 Output saved as: hr_skills_auto.xlsx")
