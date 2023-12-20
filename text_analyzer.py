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


def get_top_books_by_emotion(book_data, emotion, top_n=5):
    book_emotion_scores = []

    for index, row in book_data.iterrows():
        book_description = row['book_desc']
        emotion_scores = calculate_emotion_score(book_description, nrc_lexicon)
        book_rating = row['book_rating']

        if book_rating >= 4:
            book_emotion_scores.append({
                'book_title': row['book_title'],
                'emotion_score': emotion_scores[emotion],
                'book_rating': book_rating
            })

    sorted_books = sorted(book_emotion_scores, key=lambda x: (x['emotion_score'], x['book_rating']), reverse=True)

    print(f"Top {top_n} Books with Highest {emotion.capitalize()} Scores and Ratings:")
    for i, book_info in enumerate(sorted_books[:top_n]):
        print(f"{i + 1}. {book_info['book_title']} - {emotion.capitalize()} Score: {book_info['emotion_score']}, Rating: {book_info['book_rating']}")


target_emotion = 'fear'
get_top_books_by_emotion(book_data, target_emotion)