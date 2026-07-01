from sentence_transformers import SentenceTransformer
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "Training" / "model" / "log_classifier.joblib"

# Load the sentence transformer model to compute log_message embeddings
transformer_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the saved classification model
classifier_model = joblib.load(MODEL_PATH)

def classify_with_bert(log_message):
    embeddings = transformer_model.encode([log_message])
    probabilities = classifier_model.predict_proba(embeddings)[0]
    if max(probabilities) < 0.5:
        return "Unclassified"
    predicted_label = classifier_model.predict(embeddings)[0]
    return predicted_label

if __name__ == "__main__":
    logs = [
        "alpha.osapi_compute.wsgi.server- 12.10.11.1 - API returned 404 Not Found error ",
        "GET /V2/3454/servers/detail HTTP/1.1 RCODE 404 len:1583 time: 0.1878400",
        "System crashed due to drivers errors when restarting the server",
        "Hey bro, chill out",
        "Multiple login failures occurred on user 6454 account",
        "Server a790 was restarted unexpectedly during the process of data transfer"
    ]

    for log in logs:
        label = classify_with_bert(log)
        print(log, "->", label)
