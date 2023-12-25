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


def calculate_emotion_scores_from_summaries(text, emotion_lexicon):
    words = str(text).split()
    emotion_scores = {emotion: 0 for emotion in emotion_lexicon[list(emotion_lexicon.keys())[0]].keys()}

    for word in words:
        if word in emotion_lexicon:
            for emotion, score in emotion_lexicon[word].items():
                emotion_scores[emotion] += score

    return emotion_scores


book_data = pd.read_csv("booksummaries.txt", sep='\t', header=None)

nrc_lexicon_path = 'NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'
nrc_lexicon = load_emotion_lexicon(nrc_lexicon_path)


def calculate_emotion_scores_from_summaries_df(row, emotion_lexicon):
    summary_text = row['summary_text'] if pd.notna(row['summary_text']) else ''
    return calculate_emotion_scores_from_summaries(summary_text, emotion_lexicon)


book_data['emotion_scores'] = book_data.apply(lambda row: calculate_emotion_scores_from_summaries_df(row, nrc_lexicon), axis=1)


def get_top_books_by_emotion_from_summaries(book_data, emotion, top_n=5):
    book_emotion_scores = []

    for index, row in book_data.iterrows():
        book_rating = row['book_rating']
        emotion_scores = row['emotion_scores']

        if pd.notna(book_rating):
            book_emotion_scores.append({
                'book_title': row['book_title'],
                'emotion_score': emotion_scores[emotion],
                'book_rating': book_rating
            })

    sorted_books = sorted(book_emotion_scores, key=lambda x: (x['emotion_score'], x['book_rating']), reverse=True)

    print(f"Top {top_n} Books with Highest {emotion.capitalize()} Scores from Summaries:")
    for i, book_info in enumerate(sorted_books[:top_n]):
        print(f"{i + 1}. {book_info['book_title']} - {emotion.capitalize()} Score: {book_info['emotion_score']}, Rating: {book_info['book_rating']}")


target_emotion = 'sadness'
get_top_books_by_emotion_from_summaries(book_data, target_emotion)
