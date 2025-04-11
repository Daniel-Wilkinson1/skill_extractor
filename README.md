# Skill Extractor - HR Workflow

## 📁 Folder Structure

```
skill_extractor/
├── data/
│   ├── cv_uploads/               ← Drop CVs here (PDF/DOCX)
│   ├── job_descriptions/         ← Drop job descriptions here (PDF/DOCX/TXT)
│   ├── skill_synonyms.xlsx       ← Define skills + synonyms here
│   ├── hr_skills_auto.xlsx       ← Output: CV skill matches
│   ├── job_skills.xlsx           ← Output: JD skill matches
│   └── match_scores.xlsx         ← Output: CV vs JD match report
│
├── scripts/
│   ├── hr_first_filtered_workflow.py  ← Run this to analyze
│   ├── manage_skill_synonyms.py       ← Launch this to manage synonyms
│   └── run_all.py                     ← (Optional) runs all scripts in order
```

## 🧑‍💼 HR Usage Guide

1. **Drop job ads into:** `data/job_descriptions/`
2. **Add skills + synonyms:** `streamlit run scripts/manage_skill_synonyms.py`
3. **Drop CVs into:** `data/cv_uploads/`
4. **Run the tool:** `python scripts/hr_first_filtered_workflow.py`
5. **View the results in Excel.**

All matched data is saved in the `data/` folder.

## Requirements
```
pip install pandas python-docx pymupdf openpyxl
```

## License
MIT — free to use, adapt, and expand.
