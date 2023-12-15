import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

emotions_data = pd.read_csv("emotion_labeled_data.csv")
book_data = pd.read_csv("book_data.csv")
merged_data = pd.merge(emotions_data, book_data, on="book_title", how="inner")
merged_data = merged_data.drop(columns="book_desc_y")
merged_data = merged_data.rename(columns={"book_desc_x": "book_desc"})

merged_data["book_desc"] = merged_data["book_desc"].fillna("")
merged_data["book_desc"] = merged_data["book_desc"].str.lower()

selected_emotion = "positive"
selected_data = merged_data[merged_data["emotion_category"] == selected_emotion]

tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf_vectorizer.fit_transform(selected_data["book_desc"])
similarity = linear_kernel(tfidf_matrix, tfidf_matrix)


def book_recommendation(emotion_data, similarity_matrix, top_n=5):
    emotion_data = emotion_data.dropna(subset=["book_rating"])
    average_ratings = emotion_data.groupby("book_title")["book_rating"].mean()
    book_indices = similarity_matrix.argsort()[:, ::-1]

    recommended_books = []
    for index in book_indices:
        for i in index:
            book_title = emotion_data.iloc[i]["book_title"]
            if book_title not in recommended_books:
                recommended_books.append(book_title)
                break
        if len(recommended_books) >= top_n:
            break

    recommended_books_ratings = average_ratings[recommended_books]
    recommended_books_sorted = recommended_books_ratings.sort_values(ascending=False).index[:top_n]
    return recommended_books_sorted


recommendations = book_recommendation(selected_data, similarity)

print(f"Recommended books for {selected_emotion} emotion:")
print(recommendations.values)
