import re

# -----------------------------
# Required resume sections
# -----------------------------
REQUIRED_SECTIONS = ["skills", "experience", "education", "projects"]

# -----------------------------
# Weighted technical keywords
# -----------------------------
KEYWORD_WEIGHTS = {
    "python": 5,
    "java": 5,
    "sql": 4,
    "react": 4,
    "node": 3,
    "spring": 4,
    "spring boot": 5,
    "aws": 4,
    "machine learning": 6,
    "data analysis": 4,
    "api": 3,
    "git": 2
}

# -----------------------------
# ATS Rule-Based Score
# -----------------------------
def calculate_ats_score(resume_text):
    score = 0
    text = resume_text.lower()

    # 1️⃣ Section presence (max 40)
    for section in REQUIRED_SECTIONS:
        if section in text:
            score += 10

    # 2️⃣ Keyword weighted score (max 40)
    keyword_score = 0
    for keyword, weight in KEYWORD_WEIGHTS.items():
        if keyword in text:
            keyword_score += weight

    score += min(keyword_score, 40)

    # 3️⃣ Length & formatting (max 20)
    word_count = len(text.split())
    if word_count > 300:
        score += 20
    elif word_count > 200:
        score += 15
    elif word_count > 120:
        score += 10
    elif word_count > 60:
        score += 5

    return min(score, 100)

# -----------------------------
# Keyword Match Density (0–100)
# -----------------------------
def keyword_match_density(resume_text):
    text = resume_text.lower()
    matched = sum(1 for kw in KEYWORD_WEIGHTS if kw in text)
    density = (matched / len(KEYWORD_WEIGHTS)) * 100
    return round(min(density, 100), 2)
