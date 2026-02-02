import pickle
from preprocessing.text_cleaning import clean_text

# Load model and vectorizer
rf_model = pickle.load(open("model/ats_rf_model.pkl", "rb"))
tfidf = pickle.load(open("model/tfidf.pkl", "rb"))

def check_ats(resume_text):
    cleaned = clean_text(resume_text)
    vector = tfidf.transform([cleaned])
    prediction = rf_model.predict(vector)[0]
    return prediction

# Example usage
if __name__ == "__main__":
    resume = input("Enter resume text:\n")
    result = check_ats(resume)

    if result == "ATS-Friendly":
        print("\n✅ Resume is ATS Friendly")
    else:
        print("\n❌ Resume is NOT ATS Friendly")
