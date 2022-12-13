# Cryptocurrency Data Platform & AI Trading Algorithm

This repository contains the source code, config files, and a short demo of the Cryptocurrency Data Platform & AI Trading Algorithm. 

## Key Objectives
The goal of the service is to provide a data platform that returns the most up-to-date information about the cryptocurrency market, and provide an AI Trading model that predicts the future sentiment of a currency to determine an optimal trading strategy. 

The data regarding coin trends and prices was scraped using Telegram, Twitter and Coingecko APIs and the AI Trading model is using the coin price and sentiment information to determine whether to invest in a coin. 

## Architecture and Program Description

![architecture_diagram drawio (3)](https://user-images.githubusercontent.com/25168588/207426200-9d74b4d0-12f0-4687-b49b-c770a591e2c8.png)

### Telegram Bot
The Telegram Bot will by default scrape all messages from the Airdrop Alert Channel, which contains information about most recent coin releases and trends in the cryptocurrency market. The Telegram Bot will identify the key words (coins) from the channel messages and send them over to the Twitter Bot.

Please see the below for more details about how to set up API connection:
    * Add the following to your GitHub Codespace or Local file
    * API_ID, API_HASH, PHONE, USERNAME
    * api_id = os.getenv('API_ID')
    * api_hash = os.getenv('API_HASH')
    * phone = os.getenv('PHONE')
    * username = os.getenv('USERNAME')

### Twitter Bot
The Twitter Bot accepts the key words generated from Telegram, and search for tweets related to the key words. The bot will return a dataframe containing all the tweets scraped for a specified timeframe. The bot uses the `tweepy` package in Python to connect to the Twitter API. See below for more details:

```
import tweepy
```
For more Twitter API registration details, read from website here: https://scottlai.com/2022/09/24/twitter-bot-101/

* The API setting:  tweepy.Client.
* searching for recent tweets: client.search_recent_tweets.
* Save the Tweets into CSV format.

Input:
```
searchTweets('key_words', max_tweets_amount(less than 100 for each time))
```

output: dataframe 

### Coin Price Query Bot
The Coin price query bot will return a payload that contains the most up-to-date cryptocurrency prices for a specified timeframe. The bot uses the Coingecko API to scrape the data. See below for more details:

@Aditya to add more information.

### Sentiment Analyzer
The sentiment analysis component will predict the sentiment of a given tweet and generate a sentiment score between -1 and 1 for a tweet. 

The sentiment analyzer is a roBERTa-base model that was trained on ~124M Tweets. More information about the model used can be found [here](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest).

Please see below for an example use case / pipeline for the sentiment analysis:

```
from sentiment_analyzer import sentiment_generator

df = sentiment_generator(df, calculate_scores=False, task="sentiment-latest", remove_stopwords=False)
```

The `sentiment_generator` function will accept a pandas dataframe `df` and output another pandas dataframe `df` with one or more columns reporting information about the sentiment of the tweet (see below for more details). All tweets are stored under the field `text`. The function will also take additional three parameters: 1) `calculate_scores` will generate a sentiment score in addition to a sentiment label ('Positive', 'Negative', 'Neutral') if set to `True`. 2) 'remove_stopwords' will remove stopwords from the tweets if set to 'True'. 3) `task`: the Roberta-Base sentiment model can perform other tasks as well including emotion, degree of offensiveness of text. These are the possible parameters a user can input for `task`: emoji, emotion, hate, irony, offensive, sentiment-latest . NOTE: besides for 'sentiment-latest', all other tasks have not been tested with the model.

Data Cleaning steps:
* lowercase all tweets
* remove any URLs.
* an option to remove all stopwords. If user sets `remove_stopwords=True` in the `sentiment_generator` function then stopwords will be removed. By default, stopwords are preserved.
* Handles English tweets only.
* replace mentions with a flag `@User`
* removes hashtag signs

# Algorithm and Automation
The AI Algorithm will take in the scraped twitter data and apply sentiment analysis for each tweet. Along with the coin price information, it will then generate a trading strategy for the user. We are using a time-series model trained on the twitter and sentiment analysis. Please see below for more details about the architecture of the model: 
![framework](https://user-images.githubusercontent.com/55003943/197669184-325a8619-6a53-42bc-bf10-f14f4e8c9001.png)


