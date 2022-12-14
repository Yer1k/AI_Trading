import time
import random
import pandas as pd
import json


def backoff():
    time.sleep(random.randomint(10, 30))


def convert_output_format(time_series):
    df = pd.DataFrame(time_series, columns=["date", "price"])
    df["date"] = pd.to_datetime(df["date"], unit="ms")
    return df
