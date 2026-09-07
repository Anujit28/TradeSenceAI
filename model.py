import pandas as pd

def prepare_data(df):

    # Tomorrow's closing price
    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    features = ["RSI","MACD","MACD_SIGNAL","SMA20","SMA50"]

    df = df.dropna()

    X = df[features]
    y = df["Target"]

    return X, y