"""
This class implements model selection algorithms. Current Version is 0.1. It is based on AutoTS (More details: https://winedarksea.github.io/AutoTS/build/html/source/tutorial.html).
The main function is model_selection, which takes a dataframe and a target column name as input, and returns a list of models and their corresponding parameters.
The output is used as input for model_training.py
"""


import os
from datetime import date, datetime
import pandas as pd
import json

from autots import AutoTS

"""
This methods return the citation for AutoTS
"""

def citation():
    print("If you use this package, please cite the following paper: https://winedarksea.github.io/AutoTS/build/html/source/tutorial.html")
    return "If you use this package, please cite the following paper: https://winedarksea.github.io/AutoTS/build/html/source/tutorial.html"

"""
    This method transforms the dataframe to long format. It takes a dataframe and a target column name as input, and returns a dataframe in long format.
    The output is used as input for model_selection.
"""

def transform_to_long(df, target_col_name):
    
    df_long = pd.melt(df, id_vars=[target_col_name], var_name='ds', value_name='y')
    return df_long


    """
    This method takes a dataframe and use AutoTS to select the best model. 
    The output is a dataframe of models and their corresponding parameters.
    """

def model_selection(df_long):
    model = AutoTS(
        forecast_length=3,
        frequency='infer',
        ensemble='simple',
        max_generations=5,
        num_validations=2,
    )
    model = model.fit(df_long, date_col='datetime', value_col='value', id_col='series_id')
    return model.best_model