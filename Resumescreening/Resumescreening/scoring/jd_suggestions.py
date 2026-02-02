from scoring.ats_score import KEYWORD_WEIGHTS

def extract_jd_skills(jd_text):
    jd_text = jd_text.lower()
    return [skill for skill in KEYWORD_WEIGHTS if skill in jd_text]

def jd_based_suggestions(resume_text, jd_text):
    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    jd_skills = extract_jd_skills(jd_text)
    missing = [skill for skill in jd_skills if skill not in resume_text]

    suggestions = []

    if missing:
        suggestions.append(
            "Add these job-specific skills: " + ", ".join(missing)
        )

    if "experience" not in resume_text and "experience" in jd_text:
        suggestions.append(
            "Include a detailed experience section aligned with the job role."
        )

    if "project" not in resume_text and "project" in jd_text:
        suggestions.append(
            "Add relevant projects mentioned in the job description."
        )

    if not suggestions:
        suggestions.append(
            "Resume aligns well with the job description."
        )

    return suggestions
