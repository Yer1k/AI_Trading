install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:	
	black ./api ./query_coin_prices ./sentiment_analysis ./telegram_scraping ./twitter_scraping

all: install format  