
import os
import re
import pandas as pd
import docx
import fitz  # PyMuPDF
from difflib import get_close_matches

# Skill synonyms and canonical mapping
SKILL_SYNONYMS = {
    "python": ["python programming", "python 3"],
    "cad": ["autocad", "computer-aided design", "2d cad", "3d cad"],
    "fea": ["finite element analysis", "structural simulation"],
    "lca": ["life cycle analysis", "life cycle assessment"],
    "excel": ["microsoft excel", "spreadsheets"],
    "solidworks": ["solid works"],
    "data analysis": ["data analytics", "data mining"],
    "project management": ["pm", "managing projects"],
    "sustainability": ["sustainable design", "sustainable engineering", "environmental impact"],
    "plc systems": ["plc", "plc programming", "Pheonix Contact"]
}

PHRASE_TO_SKILL = {}
for canonical, synonyms in SKILL_SYNONYMS.items():
    PHRASE_TO_SKILL[canonical] = canonical
    for s in synonyms:
        PHRASE_TO_SKILL[s] = canonical

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_skills(text, phrase_map):
    text_lower = text.lower()
    matches = set()
    for phrase, canonical in phrase_map.items():
        if re.search(rf"\b{re.escape(phrase)}\b", text_lower):
            matches.add(canonical)
        else:
            close = get_close_matches(phrase, text_lower.split(), n=1, cutoff=0.9)
            if close:
                matches.add(canonical)
    return matches

def process_jd_folder(jd_folder):
    records = []
    for file_name in os.listdir(jd_folder):
        if file_name.lower().endswith(('.pdf', '.docx', '.txt')):
            file_path = os.path.join(jd_folder, file_name)

            if file_name.lower().endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif file_name.lower().endswith(".docx"):
                text = extract_text_from_docx(file_path)
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

            job_title = os.path.splitext(file_name)[0].replace('_', ' ').title()
            found_skills = extract_skills(text, PHRASE_TO_SKILL)

            for skill in found_skills:
                records.append({
                    "job_title": job_title,
                    "skill": skill
                })

    return pd.DataFrame(records)

if __name__ == "__main__":
    jd_folder = "job_descriptions"
    os.makedirs(jd_folder, exist_ok=True)

    df = process_jd_folder(jd_folder)
    df.to_excel("job_skills.xlsx", index=False)
    print("✅ Job description skill extraction complete.")
    print("📄 Output saved as: job_skills.xlsx")
