import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


data = pd.read_csv("book_data.csv")
data = data[["book_title", "book_desc", "book_rating_count"]]
data = data.sort_values(by="book_rating_count", ascending=False)

# recommend by similar description
feature = data["book_desc"].fillna("").tolist()
tfidf = TfidfVectorizer(input='content', stop_words="english")
tfidf_matrix = tfidf.fit_transform(feature)
similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(data.index, index=data['book_title']).drop_duplicates()


def book_recommendation(title, similarity = similarity):
    index = indices[title]
    similarity_scores = list(enumerate(similarity[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[0:5]
    bookindices = [i[0] for i in similarity_scores]
    return data['book_title'].iloc[bookindices]


print(book_recommendation("The Hunger Games"))
