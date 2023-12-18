def load_emotion_lexicon(file_path):
    lexicon = {}
    with open(file_path, 'r') as file:
        for line in file:
            word, emotion, score = line.strip().split('\t')
            if word not in lexicon:
                lexicon[word] = {}
            lexicon[word][emotion] = int(score)
    return lexicon


def calculate_emotion_score(text, emotion_lexicon):
    words = text.split()
    emotion_scores = {emotion: 0 for emotion in emotion_lexicon[list(emotion_lexicon.keys())[0]].keys()}

    for word in words:
        if word in emotion_lexicon:
            for emotion, score in emotion_lexicon[word].items():
                emotion_scores[emotion] += score

    return emotion_scores


nrc_lexicon_path = 'NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'
nrc_lexicon = load_emotion_lexicon(nrc_lexicon_path)

text = "I am so happy now!"
emotion_scores = calculate_emotion_score(text, nrc_lexicon)

print("NRC Emotion Lexicon Scores:")
for emotion, score in emotion_scores.items():
    print(f"{emotion}: {score}")