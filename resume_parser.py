import re
import pdfplumber

def parse_resume(pdf_path):
    parsed = {
        "work_experiences": [],
        "internships": [],
        "certifications": [],
        "activities": [],
        "skills": [],
        "hobbies": []
    }

    # ... your parsing logic here ...
    # even if nothing is found, lists stay empty


    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    # WORK EXPERIENCE
    work_section = re.search(r"WORK EXPERIENCE([\s\S]*?)(INTERNSHIP|EDUCATION|CERTIFICATION|$)", text, re.I)
    if work_section:
        for line in work_section.group(1).split("\n"):
            org_match = re.match(r"([A-Za-z& ]+)\s+(20\d{2}(?:–|-)20\d{2}|20\d{2})", line)
            if org_match:
                parsed["work_experiences"].append({
                    "organization": org_match.group(1).strip(),
                    "year": org_match.group(2)
                })

    # INTERNSHIPS
    intern_section = re.search(r"INTERNSHIP([\s\S]*?)(PROJECT|CERTIFICATION|EXPERTISE|$)", text, re.I)
    if intern_section:
        for line in intern_section.group(1).split("\n"):
            org_match = re.match(r"([A-Za-z& ]+)\s+(20\d{2}(?:–|-)20\d{2}|20\d{2})", line)
            if org_match:
                parsed["internships"].append({
                    "organization": org_match.group(1).strip(),
                    "year": org_match.group(2)
                })

    # SKILLS / EXPERTISE
    skills_section = re.search(r"(EXPERTISE|SKILLS)([\s\S]*?)(PROJECT|CERTIFICATION|$)", text, re.I)
    if skills_section:
        skills_raw = skills_section.group(2).replace("\n", ",")
        skills = [s.strip() for s in re.split(r"[,•]", skills_raw) if s.strip()]
        parsed["skills"] = skills
    
    hobbies_section = re.search(r"(HOBBIES)([\s\S]*?)(PROJECT|CERTIFICATION|$)", text, re.I)
    if hobbies_section:
        hobbies_raw = hobbies_section.group(2).replace("\n", ",")
        hobbies = [s.strip() for s in re.split(r"[,•]", skills_raw) if s.strip()]
        parsed["hobbies"] = hobbies
    
    return parsed
