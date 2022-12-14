import tweepy
import pandas as pd
import keys
import time


auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.Token, keys.Token_Secret)
api = tweepy.API(auth)

getClient = tweepy.Client(
    bearer_token=keys.Bearer_Token,
    consumer_key=keys.consumer_key,
    consumer_secret=keys.consumer_secret,
    access_token=keys.Token,
    access_token_secret=keys.Token_Secret,
)
client = getClient

# read search_df from AWS S3.
search_df = pd.read_csv(
    "s3://projecttwitterbot/Searching/ai_search_df.csv",
    storage_options={"key": keys.access_key, "secret": keys.secret_access_key},
)
search_df = search_df.drop(columns=["Unnamed: 0"])  # Drop the "Unamed: 0" column
search_df["created_at"] = pd.to_datetime(
    search_df["created_at"], format="%Y-%m-%d %H:%M:%S"
)  # change the created_at column into datatime format


# a function that searches twitter with key words and returns the tweets with Tweet id and other tweets information
def searchTweets():
    # change the search_recent_tweets to search_all_tweets and add the following time range for specific searching.
    # Replace with time period of your choice
    # start_time = '2020-01-01T00:00:00Z'
    # Replace with time period of your choice
    # end_time = '2022-10-01T00:00:00Z'

    auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.Token, keys.Token_Secret)
    api = tweepy.API(auth)

    getClient = tweepy.Client(
        bearer_token=keys.Bearer_Token,
        consumer_key=keys.consumer_key,
        consumer_secret=keys.consumer_secret,
        access_token=keys.Token,
        access_token_secret=keys.Token_Secret,
    )
    client = getClient

    # read search_df from AWS S3.
    search_df = pd.read_csv(
        "s3://projecttwitterbot/Searching/ai_search_df.csv",
        storage_options={"key": keys.access_key, "secret": keys.secret_access_key},
    )
    search_df = search_df.drop(columns=["Unnamed: 0"])  # Drop the "Unamed: 0" column
    search_df["created_at"] = pd.to_datetime(
        search_df["created_at"], format="%Y-%m-%d %H:%M:%S"
    )  # change the created_at column into datatime format

    return search_df


if __name__ == "__main__":
    coins = [
        "BTC",
        "ETH",
        "DOGE",
        "ADA",
        "BNB",
        "XRP",
        "SOL",
        "MATIC",
        "DOT",
        "STETH",
        "SHIB",
        "TRX",
        "DAI",
        "UNI",
        "WBTC",
        "LTC",
        "LEO",
        "OKB",
        "ATOM",
        "LINK",
        "FTT",
        "XLM",
        "CRO",
        "XMR",
        "ALGO",
        "NEAR",
        "TON",
    ]
    for coin in coins:
        searchTweets(coin, 100)
        time.sleep(60 * 15)
