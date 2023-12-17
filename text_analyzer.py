from transformers import pipeline


def detect_basic_emotion(text):
    classifier = pipeline('ner', model='dbmdz/bert-large-cased-finetuned-conll03-english')
    entities = classifier(text)
    entity_labels = [entity['entity'] for entity in entities]
    basic_emotion = ', '.join(entity_labels)
    return basic_emotion


example_text = "I am feeling happy and excited!"
basic_emotion = detect_basic_emotion(example_text)
print(f"Basic emotions: {basic_emotion}")
