import tweepy
import pandas as pd
import keys




auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.Token, keys.Token_Secret)
api = tweepy.API(auth)

getClient = tweepy.Client(bearer_token=keys.Bearer_Token,
                          consumer_key=keys.consumer_key,
                          consumer_secret=keys.consumer_secret,
                          access_token=keys.Token,
                          access_token_secret=keys.Token_Secret)
client = getClient


# write a function that gets the tweet with the tweet id
def getTweet(id_twitter):
    tweet = client.get_tweets(
        id_twitter, expansions=['author_id'], user_fields=['username'])
    return tweet


# write a function that searches twitter with key words and returns the tweets with user id of the user who tweeted it
def searchTweets(query, max_results):
    tweets = client.search_recent_tweets(query=query,
                                         tweet_fields=[
                                             'text', 'context_annotations', 'created_at', 'lang'],
                                         expansions=['referenced_tweets.id', 'attachments.media_keys',
                                                     'author_id', 'entities.mentions.username', 'geo.place_id'],
                                         user_fields=[
                                             'id', 'username', 'description', 'entities', 'protected', 'public_metrics', 'verified'],
                                         place_fields=['place_type', 'geo'],
                                         media_fields=['duration_ms', 'height', 'media_key', 'preview_image_url', 'type', 'width','url', 'public_metrics'],
                                         max_results=max_results)

    user = {u['id']: u for u in tweets.includes['users']}
    # media = {m['media_key']: m for m in tweets.includes['media']}
    # print(tweets)
    
    #print media url
    # print(tweets.includes['media'][0]['url'])
    
    results = []
    if not tweets.data is None and len(tweets.data) > 0:
        for tweet in tweets.data:
            twt = getTweet(tweet['id'])
            obj = {}
            obj['created_at'] = tweet.created_at
            obj['author_id'] = tweet.id
            obj['text'] = tweet.text
            obj['lang'] = tweet.lang
            obj['entities'] = tweet.entities
            obj['username'] = twt.includes['users'][0].username
            if user[tweet.author_id]:
                user1 = user[tweet.author_id]
                obj['public_metrics'] = user1.public_metrics
                obj['verified'] = user1.verified
                # media1 = media[tweet.media_keys[0]]
            # obj['media_url'] = tweet.url
                
            obj['url'] = 'https://twitter.com/{}/status/{}'.format(
                twt.includes['users'][0].username, tweet['id'])
            obj['followers_count'] = user1.public_metrics['followers_count']
            obj['following_count'] = user1.public_metrics['following_count']
            obj['tweet_count'] = user1.public_metrics['tweet_count']

            results.append(obj)
    else:
        return "No tweets found"

    search_df = pd.DataFrame(results)

    # save the dataframe to s3

    # search_df.to_csv("s3://projecttwitterbot/Searching/search_df.csv",
    #                  storage_options={'key': keys.access_key, 'secret': keys.secret_access_key})
    search_df.to_csv("search_df.csv")
    return search_df


if __name__ == '__main__':
    searchTweets('crypto', 100)
