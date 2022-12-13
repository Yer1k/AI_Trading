from webbrowser import get
import train_model as tm
import pandas as pd
import threading

if __name__ == "__main__":
    """
    senti_model = tm.Model()
    price_model = tm.Model()
    

    def get_sentiment_data():
        pass
    
    # take price data from Aditya
    def get_price_data():
        pass
    
    senti_data = get_sentiment_data()
    senti_model.train(senti_data)
    
    price_data = get_price_data()
    price_model.train(price_data)
    
    senti_predictions = senti_model.predict(forecast_length=3)
    # save to database
    price_predictions = price_model.predict(forecast_length=3)
    # save to database
    """
    
    """
    use idependent instance to get predictions and store in database. Then the real main read from database and do the analysis. Hence, the predictions 
    can work parallelly and save time. 
    
    """
    
    # next step analyze predictions and make decision
    """
    interval = 15

    def myPeriodicFunction():
        price_predictions = price_model.predict(forecast_length=3)
        return price_predictions

    def startTimer():
        threading.Timer(interval, startTimer).start()
        myPeriodicFunction()
    """
        
if __name__ == "__main__":
    df = pd.read_csv('/Users/a563186832/Documents/GitHub/AI_Trading/data_outputs/tweets_sentiment_1.csv') # change to data path
    sentiment = df.groupby(["created_at"]).sentiment_score.mean().reset_index()
    model = read_joblib('/Users/a563186832/Documents/GitHub/AI_Trading/models/sentiment_model.joblib') # change to model path
    pred = model.predict(sentiment,20)
    #gradient = 
    original = sentiment.sentiment_score.to_list()
    new = pred.to_list()
    y = original + new
    X = range(0,len(merged))
    coefficients = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
    if coefficients > 0:
        print("Buy")
    if coefficients < 0:
        print("Sell")            
