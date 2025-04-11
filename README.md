# Skill Extractor (Lightweight)

A simple Python tool to extract predefined skills from employee CVs (PDF or Word), identify matches using synonyms, and export structured data to Excel.

## Features
- Extract skills from `.pdf` or `.docx` files
- Handle fuzzy and synonym matches
- Output a flat Excel file of detected skills

## How to Use
1. Place CVs in the `cv_uploads/` folder
2. Run the script:
   ```
   python extract_skills_from_cvs.py
   ```
3. Open `hr_skills_auto.xlsx` for results

## Requirements
```
pip install pandas python-docx pymupdf openpyxl
```

## License
MIT — free to use, adapt, and expand.
