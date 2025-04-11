
import pandas as pd

# Load extracted skills
cv_file = "../data/hr_skills_auto.xlsx"
jd_file = "../data/job_skills.xlsx"


cv_df = pd.read_excel(cv_file)
jd_df = pd.read_excel(jd_file)

# Normalize columns
cv_df.columns = cv_df.columns.str.lower().str.strip()
jd_df.columns = jd_df.columns.str.lower().str.strip()

# Group into dictionaries
person_skills = cv_df.groupby("name")["skill"].apply(set).to_dict()
job_skills = jd_df.groupby("job_title")["skill"].apply(set).to_dict()

# Match each person to each job
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

# Output to Excel
match_df = pd.DataFrame(match_rows)
match_df = match_df.sort_values(by=["name", "match_score (%)"], ascending=[True, False])
match_df.to_excel("match_scores.xlsx", index=False)

print("✅ Matching complete. Results saved to match_scores.xlsx.")
