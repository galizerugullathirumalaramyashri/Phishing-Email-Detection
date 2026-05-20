import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# =====================================================
# LOAD DATASET
# =====================================================

df = pd.read_csv("dataset/phishing_emails.csv")

# Convert labels into numbers
df["label"] = df["label"].map({
    "safe": 0,
    "phishing": 1
})

# Features and labels
X = df["text"]
y = df["label"]

# =====================================================
# TF-IDF VECTORIZATION
# =====================================================

vectorizer = TfidfVectorizer(
    max_features=8000,
    stop_words="english"
)

X_vec = vectorizer.fit_transform(X)

# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_vec,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =====================================================
# RANDOM FOREST MODEL
# =====================================================

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

# Train model
model.fit(X_train, y_train)

# =====================================================
# PREDICTIONS
# =====================================================

pred = model.predict(X_test)

# =====================================================
# MODEL PERFORMANCE
# =====================================================

print("\n📊 MODEL PERFORMANCE:\n")

print(classification_report(y_test, pred))

# Accuracy
accuracy = accuracy_score(y_test, pred)

print("✅ Accuracy:", round(accuracy * 100, 2), "%")

# =====================================================
# CONFUSION MATRIX
# =====================================================

cm = confusion_matrix(y_test, pred)

plt.figure(figsize=(5, 4))

sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues'
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

# Save image
plt.savefig("screenshots/confusion_matrix.png")

# Show graph
plt.show()

# Close graph after viewing
plt.close()

# =====================================================
# SAVE MODEL & VECTORIZER
# =====================================================

joblib.dump(model, "models/phishing_model.pkl")

joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\n✅ Model trained successfully!")

# =====================================================
# 🔴 LIVE PHISHING DETECTOR
# =====================================================

print("\n==============================")
print("🔴 LIVE PHISHING DETECTOR")
print("Type 'exit' to stop")
print("==============================\n")

while True:

    # User input
    text = input("Enter email/text ➜ ")

    # Exit condition
    if text.lower() == "exit":
        print("👋 Exiting...")
        break

    # Convert text into vector
    vec = vectorizer.transform([text])

    # Predict
    prediction = model.predict(vec)[0]

    # Probability
    probability = model.predict_proba(vec)[0]

    # Confidence
    confidence = probability[prediction] * 100

    # Final label
    label = "PHISHING" if prediction == 1 else "SAFE"

    # Risk level
    if confidence > 90:
        risk = "HIGH RISK"

    elif confidence > 70:
        risk = "MEDIUM RISK"

    else:
        risk = "LOW RISK"

    # =================================================
    # OUTPUT
    # =================================================

    print("\n==============================")
    print("Prediction  ➜", label)
    print("Confidence  ➜", round(confidence, 2), "%")
    print("Risk Level  ➜", risk)
    print("==============================\n")