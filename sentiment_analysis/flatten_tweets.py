import pandas as pd


def flatten_tweets(tweets):
    """
    MOST LIKELY WILL NEED TO BE EDITED!! ONLY COMPATIBLE WITH V1.1 TWITTER API.
    I THINK IT'S DIFFERENT FOR V2.0 TWITTER API, BUT I DIDN'T HAVE GOOD DATA TO TEST IT ON.

    Flatten out json data from tweets into a Pandas dataframe. This function is built on v1 of the Twitter API.
    So will need to be modified if using v2 of the API.

    Args:
    tweets (list): list of tweets in json format

    Returns:
    tweets_df (Pandas dataframe): dataframe of tweets
    """

    tweets_list = []

    # Iterate through each tweet
    for i in tweets:
        # get the tweet metadata
        tweet = tweets[i][0]

        # create a new dictionary for each tweet
        tweet_dict = {}

        # add tweet_id
        tweet_dict["tweet_id"] = tweet["id"]

        # add tweet text
        tweet_dict["text"] = tweet["full_text"]

        # add twitter handle

        tweet_dict["username"] = tweet["user"]["screen_name"]

        # add tweet date
        tweet_dict["date"] = tweet["created_at"]

        # add tweet url
        tweet_dict["url"] = tweet["user"]["url"]

        # add tweet retweet count
        tweet["retweet_count"] = tweet["retweet_count"]

        # add tweet favorite count
        tweet["favorite_count"] = tweet["favorite_count"]

        tweets_list.append(tweet_dict)

    # create a dataframe from the list of dictionaries
    tweets_df = pd.DataFrame(tweets_list)

    return tweets_df
