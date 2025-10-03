from transformers import pipeline

class SentimentModel:
    def __init__(self):
        self._pipeline = pipeline("sentiment-analysis", 
                                  model="distilbert-base-uncased-finetuned-sst-2-english")

    def predict(self, text: str) -> dict:
        result = self._pipeline(text)[0]
        return {
            "label": result["label"],
            "confidence": round(result["score"], 4)
        }