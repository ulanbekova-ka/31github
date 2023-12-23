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


def calculate_emotion_scores(text, emotion_lexicon):
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


def get_top_books_by_emotion_rating_and_genre(book_data, emotion, genre, top_n=5):
    book_emotion_scores = []

    for index, row in book_data.iterrows():
        book_description = row['book_desc']
        emotion_scores = calculate_emotion_scores(book_description, nrc_lexicon)
        book_rating = row['book_rating']
        book_genres = str(row['genres'])

        if pd.notna(book_rating) and pd.notna(book_genres) and book_rating >= 4:
            if any(g.lower() == genre.lower() for g in book_genres.split('|')):
                book_emotion_scores.append({
                    'book_title': row['book_title'],
                    'emotion_score': emotion_scores[emotion],
                    'book_rating': book_rating,
                    'book_genres': book_genres
                })

    sorted_books = sorted(book_emotion_scores, key=lambda x: (x['emotion_score'], x['book_rating']), reverse=True)

    print(f"Top {top_n} Books with Highest {emotion.capitalize()} Scores, Ratings (Rating >= 4), and Matching Genre ({genre}):")
    for i, book_info in enumerate(sorted_books[:top_n]):
        print(f"{i + 1}. {book_info['book_title']} - {emotion.capitalize()} Score: {book_info['emotion_score']}, Rating: {book_info['book_rating']}, Genres: {book_info['book_genres']}")


target_emotion = 'sadness'
target_genre = 'Dystopia'

get_top_books_by_emotion_rating_and_genre(book_data, target_emotion, target_genre)

# notes:
# Happy: anything – whatever feels right to you!
# Sad: Romance or Upbeat Contemporary Fiction
# Contemplative: Fantasy, Science Fiction, Literary Fiction, or Non-Fiction
# Bored: Mystery/Thriller or Horror
# Relaxed: Classic Literature, Historical Fiction, or Memoir
# Overwhelmed: Children’s Fiction, Young Adult Fiction, or Short Stories

# Traditional recommendation systems often use collaborative filtering or content-based filtering.
# Collaborative filtering leverages user-item interactions,
# while content-based filtering recommends items based on their features.