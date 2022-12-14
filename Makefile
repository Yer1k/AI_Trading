install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:	
	black ./api/*.py ./query_coin_prices/*.py ./sentiment_analysis/*.py ./telegram_scraping/*.py ./twitter_scraping/*.py

all: install format  