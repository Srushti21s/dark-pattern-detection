
import joblib

# Load trained model
model = joblib.load("dark_pattern_model.pkl")

def predict_pattern(text):
    prediction = model.predict([text])[0]

    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities) * 100

    return {
        "prediction": prediction,
        "confidence": round(confidence, 2)
    }


if __name__ == "__main__":
    sample = "Sign up to continue shopping. Additional charges apply."

    result = predict_pattern(sample)

    print("Predicted Pattern:", result["prediction"])
    print("Model Score:", result["confidence"], "%")

