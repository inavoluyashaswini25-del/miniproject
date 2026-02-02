from scoring.ats_score import KEYWORD_WEIGHTS

def get_missing_skills(resume_text):
    text = resume_text.lower()
    missing = [skill for skill in KEYWORD_WEIGHTS if skill not in text]
    return missing
