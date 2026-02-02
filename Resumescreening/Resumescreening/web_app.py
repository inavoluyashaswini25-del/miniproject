import streamlit as st
import pickle

from preprocessing.text_cleaning import clean_text
from preprocessing.resume_parser import extract_text
from scoring.ats_score import calculate_ats_score, keyword_match_density
from scoring.final_score import calculate_final_score
from scoring.missing_skills import get_missing_skills
from scoring.jd_match import jd_match_score
from scoring.suggestions import generate_suggestions
from scoring.jd_suggestions import jd_based_suggestions

# -----------------------------
# Load model and vectorizer
# -----------------------------
rf = pickle.load(open("model/ats_rf_model.pkl", "rb"))
tfidf = pickle.load(open("model/tfidf.pkl", "rb"))

st.title("ATS Resume Screening System")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF / DOCX)",
    type=["pdf", "docx"]
)

jd_text = st.text_area(
    "Paste Job Description (Optional)",
    height=200
)

# =============================
# MAIN LOGIC
# =============================
if uploaded_file:
    resume_text = extract_text(uploaded_file)
    cleaned_text = clean_text(resume_text)

    # ML Prediction
    vector = tfidf.transform([cleaned_text])
    prediction = rf.predict(vector)[0]
    ml_confidence = max(rf.predict_proba(vector)[0]) * 100

    # Rule-based scoring
    ats_score = calculate_ats_score(resume_text)
    keyword_density = keyword_match_density(resume_text)

    # Final Score
    final_score = calculate_final_score(
        ats_score,
        ml_confidence,
        keyword_density
    )

    # Missing Skills
    missing_skills = get_missing_skills(resume_text)

    # JD Match
    jd_score = None
    if jd_text.strip():
        jd_cleaned = clean_text(jd_text)
        jd_vector = tfidf.transform([jd_cleaned])
        jd_score = jd_match_score(vector, jd_vector)

    # JD-Based Suggestions
    jd_specific_suggestions = []
    if jd_text.strip():
        jd_specific_suggestions = jd_based_suggestions(
            resume_text,
            jd_text
        )

    # General Suggestions
    suggestions = generate_suggestions(
        ats_score,
        missing_skills,
        jd_score
    )

    # -----------------------------
    # Remove contradictory JD messages
    # -----------------------------
    if jd_specific_suggestions:
        for s in jd_specific_suggestions:
            if "aligns well" in s.lower():
                suggestions = [
                    msg for msg in suggestions
                    if "align" not in msg.lower()
                ]

    # =============================
    # DISPLAY RESULTS
    # =============================
    st.subheader("Results")

    st.write(f"**ATS Status (ML):** {prediction}")
    st.write(f"**ATS Rule Score:** {ats_score}/100")
    st.write(f"**ML Confidence:** {ml_confidence:.2f}%")
    st.write(f"**Keyword Match Density:** {keyword_density:.2f}%")

    if jd_score is not None:
        st.write(f"**Job Description Match:** {jd_score:.2f}%")

    st.subheader(f"🎯 Final ATS Score: {final_score}/100")

    if final_score >= 75:
        st.success("Strong Resume – High ATS Compatibility")
    elif final_score >= 50:
        st.warning("Average Resume – Needs Optimization")
    else:
        st.error("Low ATS Compatibility – Significant Improvements Needed")

    st.subheader("🔍 Missing Skills")
    st.write(", ".join(missing_skills) if missing_skills else "No major skills missing.")

    st.subheader("🛠 Resume Improvement Suggestions")
    for s in suggestions:
        st.write("- ", s)

    if jd_specific_suggestions:
        st.subheader("📌 Job Description Based Suggestions")
        for s in jd_specific_suggestions:
            st.write("- ", s)
