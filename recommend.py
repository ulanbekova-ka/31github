import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load the labeled emotion dataset
data = pd.read_csv("emotion_labeled_data.csv")

# Preprocess the data
data["book_desc"] = data["book_desc"].fillna("")  # Handle NaN values
data["book_desc"] = data["book_desc"].str.lower()  # Convert to lowercase

# Filter data based on the user's selected emotion
selected_emotion = "positive"
selected_data = data[data["emotion_category"] == selected_emotion]

# Create a TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf_vectorizer.fit_transform(selected_data["book_desc"])

# Calculate similarity using linear kernel
similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get book recommendations based on user emotion
def book_recommendation(emotion_data, similarity_matrix, top_n=5):
    # Print the unique values in the "book_title" column to understand the structure
    print(emotion_data["book_title"].unique())

    # Drop rows with missing book ratings
    emotion_data = emotion_data.dropna(subset=["book_rating"])

    # Calculate average ratings for each book
    try:
        average_ratings = emotion_data.groupby("book_title")["book_rating"].mean()
    except KeyError:
        print("Error: 'book_rating' column not found in grouped data.")
        return []

    # Get book indices sorted by similarity
    book_indices = similarity_matrix.argsort()[:, ::-1]

    # Exclude books the user has already interacted with (if available in the dataset)
    # Add any necessary logic to filter out books the user has already seen

    # Select top N recommended books
    recommended_books = []
    for index in book_indices:
        for i in index:
            book_title = emotion_data.iloc[i]["book_title"]
            if book_title not in recommended_books:
                recommended_books.append(book_title)
                break
        if len(recommended_books) >= top_n:
            break

    # Get ratings for recommended books
    recommended_books_ratings = average_ratings[recommended_books]

    # Sort books by ratings in descending order
    recommended_books_sorted = recommended_books_ratings.sort_values(ascending=False).index[:top_n]

    return recommended_books_sorted


# Get recommendations for the selected emotion
recommendations = book_recommendation(selected_data, similarity)

print(f"Recommended books for {selected_emotion} emotion:")
print(recommendations)
