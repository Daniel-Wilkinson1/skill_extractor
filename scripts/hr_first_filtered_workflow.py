import os
import re
import pandas as pd
import docx
import fitz  # PyMuPDF

# === Load skill synonyms from Excel ===
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
synonym_file = os.path.join(base_dir, "data", "skill_synonyms.xlsx")

if not os.path.exists(synonym_file):
    raise FileNotFoundError(f"Skill synonym file not found at: {synonym_file}")

syn_df = pd.read_excel(synonym_file)
PHRASE_TO_SKILL = dict(zip(syn_df["synonym"].str.lower(), syn_df["skill"].str.lower()))

# === Utility functions ===
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

def extract_matched_skills(text, phrase_to_skill):
    text_lower = text.lower()
    matched = set()
    for phrase in phrase_to_skill.keys():
        if re.search(rf"\b{re.escape(phrase)}\b", text_lower):
            matched.add(phrase_to_skill[phrase])
    return matched

# === Define paths ===
cv_folder = os.path.join(base_dir, "data", "cv_uploads")
jd_folder = os.path.join(base_dir, "data", "job_descriptions")
output_folder = os.path.join(base_dir, "data")
os.makedirs(output_folder, exist_ok=True)

# === Step 1: Extract skills from JDs ===
job_skills = []
all_matched_skills = set()

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

        job_title = os.path.splitext(file)[0].replace("_", " ").title()
        matched_skills = extract_matched_skills(text, PHRASE_TO_SKILL)
        all_matched_skills.update(matched_skills)

        for skill in matched_skills:
            job_skills.append({
                "job_title": job_title,
                "skill": skill
            })

# Create a filtered skill map based on JD contents
PHRASE_TO_SKILL_FILTERED = {k: v for k, v in PHRASE_TO_SKILL.items() if v in all_matched_skills}

# === Step 2: Extract skills from CVs ===
records = []
seen = set()

for file in os.listdir(cv_folder):
    if file.lower().endswith((".pdf", ".docx", ".txt")):
        path = os.path.join(cv_folder, file)
        if file.endswith(".pdf"):
            text = extract_text_from_pdf(path)
        elif file.endswith(".docx"):
            text = extract_text_from_docx(path)
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

        name = guess_name(text) or os.path.splitext(file)[0] + " (Guessed)"
        for phrase, canonical in PHRASE_TO_SKILL_FILTERED.items():
            if re.search(rf"\b{re.escape(phrase)}\b", text.lower()):
                if (name, canonical) not in seen:
                    seen.add((name, canonical))
                    records.append({
                        "name": name,
                        "skill": canonical,
                        "matched_phrase": phrase
                    })

cv_df = pd.DataFrame(records)
cv_df.to_excel(os.path.join(output_folder, "hr_skills_auto.xlsx"), index=False)

# === Step 3: Save JD skill data ===
jd_df = pd.DataFrame(job_skills)
jd_df.to_excel(os.path.join(output_folder, "job_skills.xlsx"), index=False)

# === Step 4: Match scoring ===
person_skills = cv_df.groupby("name")["skill"].apply(set).to_dict()
job_skills_dict = jd_df.groupby("job_title")["skill"].apply(set).to_dict()

match_rows = []
for person, p_skills in person_skills.items():
    for job, j_skills in job_skills_dict.items():
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

print("✅ JD-driven CV skill matching complete.")
