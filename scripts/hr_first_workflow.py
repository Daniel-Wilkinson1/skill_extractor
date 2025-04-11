
import os
import re
import pandas as pd
import docx
import fitz  # PyMuPDF
from difflib import get_close_matches

# Paths
cv_folder = "../data/cv_uploads"
jd_folder = "../data/job_descriptions"
output_folder = "../data"
os.makedirs(output_folder, exist_ok=True)

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
            matches.add((canonical, phrase, "exact"))
        else:
            close = get_close_matches(phrase, text_lower.split(), n=1, cutoff=0.9)
            if close:
                matches.add((canonical, phrase, "fuzzy"))
    return matches

def guess_name(text):
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip()
        if line and len(line.split()) >= 2 and line.replace(' ', '').isalpha():
            return line.title()
    return None

# Step 1: Extract skills from all JDs
jd_skills_set = set()
for file in os.listdir(jd_folder):
    if file.lower().endswith((".pdf", ".docx", ".txt")):
        path = os.path.join(jd_folder, file)
        if file.endswith(".pdf"):
            text = extract_text_from_pdf(path)
        elif file.endswith(".docx"):
            text = extract_text_from_docx(path)
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        words = re.findall(r"\b[a-zA-Z][a-zA-Z\s\-]{1,30}\b", text.lower())
        jd_skills_set.update([w.strip() for w in words if 2 <= len(w.strip()) <= 30])

# Create phrase-to-skill mapping based on JD content
PHRASE_TO_SKILL = {phrase: phrase for phrase in jd_skills_set}

# Step 2: Extract relevant skills from CVs using JD-derived phrases
records = []
seen = set()
for file in os.listdir(cv_folder):
    if file.lower().endswith((".pdf", ".docx")):
        path = os.path.join(cv_folder, file)
        if file.endswith(".pdf"):
            text = extract_text_from_pdf(path)
        else:
            text = extract_text_from_docx(path)
        name = guess_name(text) or os.path.splitext(file)[0] + " (Guessed)"
        matches = extract_skills(text, PHRASE_TO_SKILL)
        for canonical, phrase, match_type in matches:
            if (name, canonical) in seen:
                continue
            seen.add((name, canonical))
            records.append({
                "name": name,
                "skill": canonical,
                "matched_phrase": phrase,
                "match_type": match_type
            })

cv_df = pd.DataFrame(records)
cv_df.to_excel(os.path.join(output_folder, "hr_skills_auto.xlsx"), index=False)

# Step 3: Match CVs to JDs
jd_skill_df = pd.DataFrame(jd_skills_set, columns=["skill"])
jd_skill_df["job_title"] = "Generic Job"
jd_skill_df.to_excel(os.path.join(output_folder, "job_skills.xlsx"), index=False)

# Create match score
person_skills = cv_df.groupby("name")["skill"].apply(set).to_dict()
job_skills = jd_skill_df.groupby("job_title")["skill"].apply(set).to_dict()

match_rows = []
for person, p_skills in person_skills.items():
    for job, j_skills in job_skills.items():
        matched = p_skills.intersection(j_skills)
        match_score = round(100 * len(matched) / len(j_skills), 1) if j_skills else 0
        match_rows.append({
            "name": person,
            "job_title": job,
            "match_score (%)": match_score,
            "matched_skills": ", ".join(sorted(matched))
        })

match_df = pd.DataFrame(match_rows)
match_df.to_excel(os.path.join(output_folder, "match_scores.xlsx"), index=False)

print("✅ Workflow complete.")
