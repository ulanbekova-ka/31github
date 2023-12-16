from transformers import pipeline


def detect_basic_emotion(text):
    classifier = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
    emotions = classifier(text)
    top_emotion = emotions[0]['label']
    return top_emotion


example_text = "I feel really happy about the good news!"
basic_emotion = detect_basic_emotion(example_text)
print(f"Basic emotion: {basic_emotion}")
