import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from preprocessing.text_cleaning import clean_text

# -----------------------------
# Load dataset safely
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "dataset", "resumes.csv")

data = pd.read_csv(CSV_PATH)

# -----------------------------
# Preprocess text
# -----------------------------
data["Resume_Text"] = data["Resume_Text"].apply(clean_text)

X = data["Resume_Text"]
y = data["ATS_Status"]

print("\nClass Distribution:")
print(y.value_counts())

# -----------------------------
# Vectorization
# -----------------------------
tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=3000,
    ngram_range=(1, 2)
)

X_tfidf = tfidf.fit_transform(X)

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.5, random_state=42
)


# -----------------------------
# Random Forest Model
# -----------------------------
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    class_weight="balanced"
)

rf.fit(X_train, y_train)

# -----------------------------
# Evaluation
# -----------------------------
y_pred = rf.predict(X_test)

print("\nModel Evaluation")
print("----------------")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -----------------------------
# Save model
# -----------------------------
MODEL_PATH = os.path.join(BASE_DIR, "model", "ats_rf_model.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "model", "tfidf.pkl")

pickle.dump(rf, open(MODEL_PATH, "wb"))
pickle.dump(tfidf, open(TFIDF_PATH, "wb"))

print("\nModel trained and saved successfully.")
