def calculate_final_score(ats_score, ml_confidence, keyword_density):
    """
    Final ATS Score Formula:
    0.5 * ATS Rule Score
    + 0.3 * ML Confidence
    + 0.2 * Keyword Match Density
    """
    final_score = (
        0.5 * ats_score +
        0.3 * ml_confidence +
        0.2 * keyword_density
    )
    return round(final_score, 2)
