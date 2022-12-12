import tweepy
import pandas as pd
import keys
import time




auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.Token, keys.Token_Secret)
api = tweepy.API(auth)

getClient = tweepy.Client(bearer_token=keys.Bearer_Token,
                          consumer_key=keys.consumer_key,
                          consumer_secret=keys.consumer_secret,
                          access_token=keys.Token,
                          access_token_secret=keys.Token_Secret)
client = getClient

# read search_df from AWS S3.
search_df = pd.read_csv('s3://projecttwitterbot/Searching/ai_search_df.csv',
                storage_options={'key': keys.access_key, 'secret': keys.secret_access_key})
search_df = search_df.drop(columns=['Unnamed: 0'])                                            # Drop the "Unamed: 0" column
search_df['created_at'] = pd.to_datetime(search_df['created_at'], format='%Y-%m-%d %H:%M:%S') # change the created_at column into datatime format


# a function that searches twitter with key words and returns the tweets with Tweet id and other tweets information
def searchTweets(query, max_results):
    # change the search_recent_tweets to search_all_tweets and add the following time range for specific searching. 
    # Replace with time period of your choice
    # start_time = '2020-01-01T00:00:00Z'
    # Replace with time period of your choice
    # end_time = '2022-10-01T00:00:00Z'   
    tweets = client.search_recent_tweets(query=query,
                                    #   start_time=start_time,
                                    #   end_time=end_time,
                                         tweet_fields=[
                                             'id','text', 'context_annotations', 'created_at', 'lang'],
                                         expansions=['referenced_tweets.id', 'attachments.media_keys',
                                                     'author_id', 'entities.mentions.username', 'geo.place_id'],
                                         user_fields=[
                                             'id', 'username', 'description', 'entities', 'protected', 'public_metrics', 'verified'],
                                         place_fields=['place_type', 'geo'],
                                         media_fields=['duration_ms', 'height', 'media_key', 'preview_image_url', 'type', 'width','url', 'public_metrics'],
                                         max_results=max_results)

    user = {u['id']: u for u in tweets.includes['users']}
    results = []
    if not tweets.data is None and len(tweets.data) > 0:
        for tweet in tweets.data:
            twt = client.get_tweets(tweet['id'], expansions=['author_id'], user_fields=['username'])
            obj = {}
            obj['id'] = tweet['id']
            obj['created_at'] = tweet['created_at']
            obj['author_id'] = tweet.id
            obj['text'] = tweet.text
            obj['lang'] = tweet.lang
            # obj['entities'] = tweet.entities
            obj['username'] = twt.includes['users'][0].username
            if user[tweet.author_id]:
                user1 = user[tweet.author_id]
                # obj['public_metrics'] = user1.public_metrics
                obj['verified'] = user1.verified
                
            obj['url'] = 'https://twitter.com/{}/status/{}'.format(
                twt.includes['users'][0].username, tweet['id'])
            obj['followers_count'] = user1.public_metrics['followers_count']
            obj['following_count'] = user1.public_metrics['following_count']
            obj['tweet_count'] = user1.public_metrics['tweet_count']
            obj['coin'] = query

            results.append(obj)
    else:
        return "No tweets found"

    search_df_new = pd.DataFrame(results)

    # merge the search_df_new with the search_df base on the id
    new_df = pd.merge(search_df, search_df_new, on = ['id','created_at','author_id','text','lang','username', 'verified','url','followers_count','following_count','tweet_count'], how='outer')

    # save the dataframe bakc to s3
    search_df.to_csv("s3://projecttwitterbot/Searching/ai_search_df.csv",
                     storage_options={'key': keys.access_key, 'secret': keys.secret_access_key})

    return search_df


if __name__ == '__main__':
    coins = ['BTC','ETH','DOGE','ADA','BNB','XRP','SOL','MATIC','DOT','STETH','SHIB','TRX','DAI','UNI','WBTC','LTC','LEO','OKB','ATOM','LINK','FTT','XLM','CRO','XMR','ALGO','NEAR','TON']
    for coin in coins:
      searchTweets(coin, 100)
      time.sleep(60*15)
      
