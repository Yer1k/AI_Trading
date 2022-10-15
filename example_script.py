import pandas as pd
from flatten_tweets import flatten_tweets
from sentiment_analyzer import sentiment_generator
from sentiment_analyzer import find_sentiment


def main():
    """Run an example case of the sentiment analyzer"""

    # Load example tweets from our beloved realDonaldTrump
    tweets = pd.read_json(
        "https://raw.githubusercontent.com/zeegeeko/DS100-Proj1-Twitter/master/realDonaldTrump.json",
        lines=True,
    )

    # Flatten the tweets into pandas dataframe
    tweets = flatten_tweets(tweets)

    # run the sentiment analyzer on a smaller chunk of data- see sentiment_analyzer.py for more details
    test = tweets.iloc[0:10]
    test = sentiment_generator(test)
    test.to_csv("test_output.csv")


if __name__ == "__main__":
    main()
