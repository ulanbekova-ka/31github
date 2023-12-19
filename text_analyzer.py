import pandas as pd


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
    words = str(text).split()
    emotion_scores = {emotion: 0 for emotion in emotion_lexicon[list(emotion_lexicon.keys())[0]].keys()}

    for word in words:
        if word in emotion_lexicon:
            for emotion, score in emotion_lexicon[word].items():
                emotion_scores[emotion] += score

    return emotion_scores


book_data = pd.read_csv("book_data.csv")

nrc_lexicon_path = 'NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'
nrc_lexicon = load_emotion_lexicon(nrc_lexicon_path)


for index, row in book_data.iterrows():
    book_description = row['book_desc']
    emotion_scores = calculate_emotion_score(book_description, nrc_lexicon)

    sorted_emotion_scores = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
    top_3_emotions = sorted_emotion_scores[:3]

    print(f"Book Title: {row['book_title']}")
    print("Top 3 Emotions:")
    for emotion, score in top_3_emotions:
        print(f"{emotion}: {score}")
    print("\n")