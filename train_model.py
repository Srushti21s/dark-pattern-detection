
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


# Load dataset
data = pd.read_csv("dataset.csv")

X = data["text"]
y = data["label"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000))
])


# Train model
print("Training ML model...")

model.fit(X_train, y_train)


# Evaluate model
predictions = model.predict(X_test)

print("\nMODEL EVALUATION")
print(classification_report(
    y_test,
    predictions,
    zero_division=0
))


# Save model
joblib.dump(model, "dark_pattern_model.pkl")

print("\nModel saved successfully!")
