from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=None
)

def analyze_emotion(text: str) -> dict:
    results = emotion_classifier(text)[0]
    emotions = {item["label"]: round(item["score"], 3) for item in results}
    return emotions

def get_top_emotions(text: str, top_n: int = 3) -> list:
    emotions = analyze_emotion(text)
    sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
    return [emotion for emotion, score in sorted_emotions[:top_n]]

if __name__ == "__main__":
    test_text = "I am leaving my country to start a new life abroad"
    print("Tüm duygular:", analyze_emotion(test_text))
    print("En güçlü 3 duygu:", get_top_emotions(test_text))