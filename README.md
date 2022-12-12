# Cryptocurrency Data Platform & AI Trading Algorithm

### Telegram Bot


- able to scrap all message from specific channel
- please input your own account credential to test it

    * Add the following to your GitHub Codespace or Local file
    * API_ID, API_HASH, PHONE, USERNAME
    * api_id = os.getenv('API_ID')
    * api_hash = os.getenv('API_HASH')
    * phone = os.getenv('PHONE')
    * username = os.getenv('USERNAME')

- example message scrapped file is on slack group chat

### Twitter Bot
- the Twitter Bot get the key words generat from Telegram, and searching for Twits related with the key words hastags. 
- Put the Tweets into dataframe for the sentiment Analyzer

For this project we are using Tweepy package to connect the Twitter API.

```
import tweepy
```
For more Twitter API registration detials, read from website here: https://scottlai.com/2022/09/24/twitter-bot-101/

* The API setting:  tweepy.Client.
* searching for recent tweets: client.search_recent_tweets.
* Save the Tweets into CSV format.

Input:
```
searchTweets('key_words', max_tweets_amount(less than 100 for each time))
```

output: dataframe 


### Sentiment Analyzer
Please see below for an example use case / pipeline for the sentiment analysis:

```
from sentiment_analyzer import sentiment_generator

df = sentiment_generator(df, calculate_scores=False, task="sentiment-latest", remove_stopwords=False)
```

As simple as that. The `sentiment_generator` function will accept a pandas dataframe `df` and output another pandas dataframe `df` with one or more columns reporting information about the sentiment of the tweet (see below for more details). All tweets are stored under the field `text`.

1) The function will first clean and preprocess the data
* lowercase all tweets
* remove any URLs.
* an option to remove all stopwords. If user sets `remove_stopwords=True` in the `sentiment_generator` function then stopwords will be removed. By default, stopwords are preserved.
* Handles English tweets only.
* replace mentions with a flag `@User`
* removes hashtag signs

2) The sentiment model used can be found [here](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest).

#### Note About Parameters
`calculate_scores`: if user wants to calculate the polarity scores for Positive, Neutral and Negative sentiments then set this parameter to `True`. By default only sentiment is included in the final output.

`task`: the Roberta-Base sentiment model can perform other tasks as well including emotion, degree of offensiveness of text. These are the possible parameters a user can input for `task`: emoji, emotion, hate, irony, offensive, sentiment-latest . NOTE: besides for 'sentiment-latest', all other tasks have not been tested with the model.

`remove_stopwords`: a boolean to determine whether stopwords should be removed from the text prior to sentiment analysis.

# Algorithm and Automation

![framework](https://user-images.githubusercontent.com/55003943/197669184-325a8619-6a53-42bc-bf10-f14f4e8c9001.png)


