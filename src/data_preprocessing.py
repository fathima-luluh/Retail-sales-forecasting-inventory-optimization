import pandas as pd

def load_data():
    df = pd.read_csv("data/retail_data.csv", parse_dates=["date"])
    df = df.dropna()
    return df