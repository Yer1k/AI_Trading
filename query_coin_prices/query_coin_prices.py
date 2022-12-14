"""
Script to query historic prices for a given coin using CoinGecko API
"""

from datetime import datetime as dt
import json
import requests
import time

from helper_function import *
from config import *

base_url = "https://api.coingecko.com/api/v3"

"""
Function to list all coin in the api

Returns:
JSON: Containing all coin ids, symbols and names of all coins supported by CoinGecko
int: Indicates the response code of the API request
"""


def list_all_coins():
    list_url = base_url + "/coins/list"
    response = requests.get(list_url)
    coins_list = json.loads(response.content)
    return coins_list, response.status_code


"""
Get prices for previous n days for the given coin

Parameters:
arg1 (str): The ID of the coin who's prices are to be fetched
arg2 (str): The currency in which the prices are to be returned
arg3 (int): The number of days (prior to current day) for which prices are to be returned
  
Returns:
2-d list: 2-d list containing prices and unix timestamp
int: Indicates the response code of the API request
"""


def get_prev_price(coin_id, vs_currency, num_days):
    range_url = (
        base_url
        + f"/coins/{coin_id}/market_chart?vs_currency={vs_currency}&days={num_days}"
    )
    response = requests.get(range_url)
    price_chart = json.loads(response.content)
    return price_chart["prices"], response.status_code


"""
Get prices in the given range of dates

Parameters:
arg1 (str): The ID of the coin who's prices are to be fetched
arg2 (str): Start date from which prices are to be fetched yyyy-mm-dd format
arg3 (str): End date from which prices are to be fetched yyyy-mm-dd format
arg4 (str): The currency in which the prices are to be returned
  
Returns:
2-d list: 2-d list containing prices and unix timestamp
int: Indicates the response code of the API request
"""


def get_historic_price(coin_id, start_date, end_date, vs_currency):
    start_date = time.mktime(dt.strptime(start_date, "%Y-%m-%d").timetuple())
    end_date = time.mktime(dt.strptime(end_date, "%Y-%m-%d").timetuple())
    historic_url = (
        base_url
        + f"/coins/{coin_id}/market_chart/range?vs_currency={vs_currency}&from={start_date}&to={end_date}"
    )
    response = requests.get(historic_url)
    historic_chart = json.loads(response.content)
    return historic_chart["prices"], response.status_code


"""
Wrapper function combining the various functions in the script.
Returns the data in a ready to use format. 
Default values are imported from the config file. 

Parameters:
arg1 (str): The name the coin who's prices are to be fetched
arg2 (str): Start date from which prices are to be fetched yyyy-m-d format
arg3 (str): End date from which prices are to be fetched yyyy-m-d format
arg4 (str): The currency in which the prices are to be returned
  
Returns:
dataframe: Returns a 2-column dataframe containing prices and dates (in yyyy-mm-dd) format
"""


def get_prices(
    coin_name=default_coin,
    start_date=default_start_date,
    end_date=default_end_date,
    vs_currency=default_curr,
):
    try:
        coins_list, list_coins_status_code = list_all_coins()
        if list_coins_status_code == 429:
            return {"data": [], "error": "Try after some time, too many requests"}

        coin_id_dict = [x for x in coins_list if x["name"].lower() == coin_name][0]

        historic_data, historic_prices_status_code = get_historic_price(
            coin_id_dict["id"], start_date, end_date, vs_currency
        )
        if historic_prices_status_code == 429:
            return {"data": [], "error": "Try after some time, too many requests"}
        historic_data_formatted = convert_output_format(historic_data)
        historic_data_formatted["coin_name"] = coin_name
        historic_data_formatted["currency_code"] = vs_currency
        return {"data": historic_data_formatted.to_dict(orient="records"), "error": ""}

    except Exception as ee:
        return {"data": [], "error": str(ee)}


if __name__ == "__main__":
    prices_df = get_prices()
    print(prices_df.head())
