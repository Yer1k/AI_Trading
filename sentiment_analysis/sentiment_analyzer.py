import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import warnings
import nltk
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax


def clean_data(tweets_df, remove_stopwords=False):
    """Clean the data by removing URLs, converting to lowercase and removing @s and #s from the tweet"""

    warnings.filterwarnings("ignore")

    # remove all URLs from the text
    tweets_df["text"] = tweets_df["text"].str.replace(r"http\S+", "")

    # remove all mentions from the text and replace with generic flag
    tweets_df["text"] = tweets_df["text"].str.replace(r"@\S+", "@user")

    # remove all hashtags from the text
    tweets_df["text"] = tweets_df["text"].str.replace(r"#", "")

    # lowercase all text
    tweets_df["text"] = tweets_df["text"].str.lower()

    if remove_stopwords:
        # remove stopwords
        nltk.download("stopwords")
        stop_words = set(stopwords.words("english"))
        tweets_df["text"] = tweets_df["text"].apply(
            lambda x: " ".join([word for word in x.split() if word not in stop_words])
        )
    return tweets_df


def load_model(task="sentiment-latest"):
    """Load the model and tokenizer for the task."""
    # Tasks:
    # emoji, emotion, hate, irony, offensive, sentiment-latest

    warnings.filterwarnings("ignore")

    MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

    # load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    # load the model
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    return config, tokenizer, model


def analyze_sentiment_score(text, config, tokenizer, model):
    # PT
    encoded_input = tokenizer(text, return_tensors="pt")
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ans = []
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    label = config.id2label[ranking[0]]
    if label == "Positive":
        return scores[ranking[0]]
    elif label == "Negative":
        return scores[ranking[0]] * -1
    else:
        return 0


def return_sentiment(text, config, tokenizer, model):
    """Return sentiment with highest polarity scores"""
    encoded_input = tokenizer(text, return_tensors="pt")
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ans = []
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    return config.id2label[ranking[0]]


def apply_sentiment_to_df(df, config, tokenizer, model, calculate_scores):
    """Apply the sentiment analysis model to the dataframe."""
    df["sentiment"] = df["text"].apply(
        lambda x: return_sentiment(x, config, tokenizer, model)
    )
    if calculate_scores == True:
        df["sentiment_score"] = df["text"].apply(
            lambda x: analyze_sentiment_score(x, config, tokenizer, model)
        )
    return df


def find_sentiment(df, keyword):
    """Find the sentiment of a given keyword. Assumes the dataframe has been cleaned and sentiment analysis has been applied."""
    keyword_tweets = df[df["text"].str.contains(keyword)]
    return keyword_tweets["sentiment"].value_counts(normalize=True)


def sentiment_generator(
    df, calculate_scores=False, task="sentiment-latest", remove_stopwords=False
):
    """Generate sentiment for each tweet in the dataframe.
    If calculate_scores is set to True, then the sentiment scores will be calculated."""

    # clean and preprocess data
    df = clean_data(df, remove_stopwords)

    # load model
    config, tokenizer, model = load_model(task)

    # apply sentiment analysis to dataframe
    df = apply_sentiment_to_df(df, config, tokenizer, model, calculate_scores)

    return df


if __name__ == "__main__":
    # load data
    df = pd.read_csv("../data_outputs/search_df_1.csv")

    # generate sentiment
    df = sentiment_generator(df, calculate_scores=True)

    # save to csv
    df.to_csv("tweets_sentiment_1.csv")
