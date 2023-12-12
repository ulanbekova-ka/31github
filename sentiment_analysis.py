from textblob import TextBlob
import pandas as pd

data = pd.read_csv("book_data.csv")
data = data[["book_title", "book_desc"]].dropna()


def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


data["emotion_score"] = data["book_desc"].apply(get_sentiment)

data["emotion_category"] = pd.cut(data["emotion_score"], bins=[-1, -0.5, 0.5, 1], labels=['negative', 'neutral', 'positive'])

data.to_csv("emotion_labeled_data.csv", index=False)
