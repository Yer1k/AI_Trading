This script is used to query prices for a specific coin for a given time range using the Coingecko API. 

The best way to use it is to import the wrapper function into your code. It taken the coin name, start date, end date and currency as input and returns a dataframe containing prices and dates. 

### To do:
1. Use levenshtein distance to match the given input name to a coin. Currently it relies on an exact match which may not work if the data is not clean or doesn't match the format that coin gecko expects. 
2. Add backoff to the API calls to ensure that additional calls dont get blocked by the website. 
3. Add resampling to ensure that the data is always at a daily frequency. 