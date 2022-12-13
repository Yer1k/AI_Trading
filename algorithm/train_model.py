import panads as pd
import sklearn as sk
import model_selection as ms
class Model:
    model = None
 
    #senti_data = pd.DataFrame()
    #price_data = pd.DataFrame()
    def __init__(self,data):
        self.model = None
        

        #self.senti_data = pd.DataFrame()
        #self.price_data = pd.DataFrame()

    def predict(self):
        self.predictions = self.model.predict(self.data)
        return self.predictions

    def get_model(self):
        return self.model

    def get_data(self):
        return self.data

    def get_predictions(self):
        return self.predictions

    #def save_model(self):
    #    pass

    #def save_data(self):
    #    pass

    #def save_predictions(self):
    #    pass

    #def load_model(self):
    #    pass

    #def load_data(self):
    #    pass

    def load_predictions(self):
        pass

    # take sentiment data from NLP

    # train model with extracted data
    def train(self,data):
        # train model
        try:
            model = ms.model_selection(data)
        except:
            data = ms.model_selection.transform_to_long(data, 'value')
            model = ms.model_selection(data)
        self.model = model
        #return model