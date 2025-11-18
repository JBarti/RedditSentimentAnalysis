from transformers import pipeline
from tabulate import tabulate
from app.emoji_cleaner import cleanup
import logging

logger = logging.getLogger(__name__)


classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
)


def classify_sentiment(text: str, return_only_top_score: bool = True) -> dict | list[dict]:
    """Classify the given text and return the results."""
    cleaned_text = cleanup(text)
    cleaned_text = cleaned_text[:512]  # Truncate to max length
    logging.info(f"Classifying text: {cleaned_text}")

    if return_only_top_score:
        result = classifier(cleaned_text, top_k=1)
        return result[0]

    return classifier(text, top_k=None)


if __name__ == "__main__":
    # results = classify("I love coding! 😍")
    while (sentence := input("Enter a sentence: ")) != "q":
        results = classify_sentiment(sentence, return_only_top_score=False)

        # Convert to tabular data
        tabular_data = [
            (emotion["label"], f"{round(emotion['score'] * 100, 2)}%")
            for emotion in results
        ]
        # Sort by value descending
        tabular_data.sort(key=lambda val: float(val[1][:-1]), reverse=True)
        print(tabulate(headers=["Emotion", "Value"], tabular_data=tabular_data))
