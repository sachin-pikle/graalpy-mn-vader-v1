import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_ANALYZER = SentimentIntensityAnalyzer()


def analyze_review_json(file_name: str, review_text: str) -> str:
    scores = _ANALYZER.polarity_scores(review_text)
    label = "Neutral"
    if scores["compound"] >= 0.05:
        label = "Positive"
    elif scores["compound"] <= -0.05:
        label = "Negative"

    return json.dumps(
        {
            "fileName": file_name,
            "reviewText": review_text,
            "pythonMessage": "Analyzed in GraalPy using VADER.",
            "sentiment": {
                "positive": round(scores["pos"], 3),
                "neutral": round(scores["neu"], 3),
                "negative": round(scores["neg"], 3),
                "compound": round(scores["compound"], 3),
                "label": label,
            },
        }
    )
