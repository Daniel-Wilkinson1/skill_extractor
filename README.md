
# 🧠 Skill Extractor & CV Matching Tool

This project helps HR match employee CVs to open job roles by extracting and comparing relevant skills — using both text analysis and structured synonym handling.

---

## 🗂️ Folder Structure

```
skill_extractor/
├── data/
│   ├── cv_uploads/               # Drop employee CVs here (.pdf, .docx, .txt)
│   ├── job_descriptions/         # Drop job descriptions here (.pdf, .docx, .txt)
│   ├── skill_synonyms.xlsx       # Define skills and their synonyms (HR-managed)
│   ├── hr_skills_auto.xlsx       # OUTPUT: Extracted skills per employee
│   ├── job_skills.xlsx           # OUTPUT: Skills found in each job description
│   └── match_scores.xlsx         # OUTPUT: Match percentage between each person & job
│
├── scripts/
│   ├── hr_first_filtered_workflow.py  # Main script to run the full process
│   ├── manage_skill_synonyms.py       # Streamlit app to add/edit skill synonyms
│   └── run_all.py                     # Optional script to automate all steps
```

---

## 👩‍💼 HR Workflow

### Step 1: Add Job Descriptions
Save job postings as `.pdf`, `.docx`, or `.txt` and place them in `data/job_descriptions/`.

---

### Step 2: Define Relevant Skills
Launch the Streamlit app to define canonical skills and their synonyms:
```bash
streamlit run scripts/manage_skill_synonyms.py
```

This edits the file `data/skill_synonyms.xlsx`.

---

### Step 3: Upload CVs
Drop employee CVs into `data/cv_uploads/` (supports `.pdf`, `.docx`, or `.txt`).

---

### Step 4: Run the Skill Matching Script
Run the main workflow:
```bash
python scripts/hr_first_filtered_workflow.py
```

This will:
- Extract job-specific skills from the job descriptions
- Extract only matching skills from each CV
- Score and rank how well each person fits each job

---

### Step 5: Review the Results
Check the generated Excel files:
- ✅ `hr_skills_auto.xlsx` – what each person knows
- ✅ `job_skills.xlsx` – what each job needs
- ✅ `match_scores.xlsx` – how well each person matches each role

---

## ✅ Output Summary

| File | Description |
|------|-------------|
| `hr_skills_auto.xlsx` | Skills found in each CV |
| `job_skills.xlsx` | Skills required per job |
| `match_scores.xlsx` | Match % and matched skills for each person–job pair |

---

## 💡 Tip: Automate Everything
To run everything in one go:
```bash
python scripts/run_all.py
```

---

## 📬 Questions?
This tool is built for internal HR use and is fully customizable. Let us know if you'd like to:
- Add new skill domains (like soft skills)
- Create a dashboard for real-time insights
- Enable employee self-assessments
