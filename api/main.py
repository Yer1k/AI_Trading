from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
import uvicorn
from Twitter_search import searchTweets
from sentiment_analyzer import sentiment_generator
import sys


sys.path.append('../query_coin_prices')
import query_coin_prices
app = FastAPI()


@app.get("/")
async def root():
    """Home Page with GET HTTP Method"""

    return {"message": "Hello! This is the home page for querying the cryptocurrency data."}

@app.get("/query_coin_price/{coin_name}")
async def get_coin_price(coin_name: str, start_date: str='2022-01-01', end_date: str="2022-06-01", curr_code: str="usd"):
    """Get the most up-to-date price of a cryptocurrency. Takes in a coin name as a parameter.
    Parameters
    ----------
    returns : dict
    """
    return_data = query_coin_prices.get_prices(coin_name=coin_name, start_date=start_date, end_date=end_date, vs_currency=curr_code)
    return return_data

@app.get("/query_telegram_messages")
async def get_telegram_messages():
    """Get Telegram messages from the Crypto Airdrop Alert channel."""

    data = None

    return data

@app.get("/scrape_twitter")
async def scrape_twitter():
    """Scrape Twitter for tweets containing cryptocurrency keywords. Perform sentiment analysis and download the results."""
    
    #extract the data
    data = searchTweets()

    #apply sentiment analysis to the data
    data = sentiment_generator(data, calculate_scores=False, task="sentiment-latest", remove_stopwords=False)
    
    stream = io.StringIO()
    data.to_csv(stream, index = False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=tweets.csv"
    return response

@app.get("/model_predict")
async def model_predict():
    """Apply algorithm to the twitter data to predict the price of a cryptocurrency."""

    #check whether data exists or not

    data = None

    return data


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")