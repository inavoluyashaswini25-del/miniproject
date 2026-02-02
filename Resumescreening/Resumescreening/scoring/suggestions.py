def generate_suggestions(ats_score, missing_skills, jd_score=None):
    suggestions = []

    if missing_skills:
        suggestions.append(
            "Consider adding these skills: " + ", ".join(missing_skills[:5])
        )

    if jd_score is not None and jd_score < 60:
        suggestions.append(
            "Resume may need better alignment with the job description."
        )

    if not suggestions:
        suggestions.append(
            "Resume is well optimized. Minor improvements only."
        )

    return suggestions
