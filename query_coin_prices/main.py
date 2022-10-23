from datetime import datetime as dt
import json
import requests
import time

from helper_function import *

base_url = 'https://api.coingecko.com/api/v3'

def list_all_coins():
    list_url = base_url + '/coins/list'
    response = requests.get(list_url)
    coins_list = json.loads(response.content)
    return coins_list, response.status_code
    
def get_prev_price(coin_id='bitcoin', vs_currency='usd', num_days=30):
    range_url = base_url + f'/coins/{coin_id}/market_chart?vs_currency={vs_currency}&days={num_days}'
    response = requests.get(range_url)
    price_chart = json.loads(response.content)
    return price_chart['prices'], response.status_code

def get_historic_price(coin_id, start_date, end_date, vs_currency):
    start_date = time.mktime(dt.strptime(start_date, "%Y-%m-%d").timetuple())
    end_date = time.mktime(dt.strptime(end_date, "%Y-%m-%d").timetuple())
    historic_url = base_url + f'/coins/{coin_id}/market_chart/range?vs_currency={vs_currency}&from={start_date}&to={end_date}'
    response = requests.get(historic_url)
    historic_chart = json.loads(response.content)
    return historic_chart['prices'], response.status_code

def wrapper_function(coin_name='bitcoin', start_date='2022-01-01', end_date='2022-06-01', vs_currency='usd'):
    coins_list, list_coins_status_code = list_all_coins()
    coin_id_dict = [x for x in coins_list if x['name'].lower() == coin_name][0]

    historic_data, historic_prices_status_code = get_historic_price(coin_id_dict['id'], start_date, end_date, vs_currency)  
    historic_data_formatted = convert_output_format(historic_data)
    return historic_data_formatted

if __name__ == "__main__":
    prices_df = wrapper_function()
    print(prices_df.head())