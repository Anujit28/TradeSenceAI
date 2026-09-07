
import joblib

model = joblib.load("stock_model.pkl")

def predict_stock(df):

    latest = df.iloc[-1]

    X = [[
        latest["RSI"],
        latest["MACD"],
        latest["MACD_SIGNAL"],
        latest["SMA20"],
        latest["SMA50"]
    ]]

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]

    confidence = max(probability)*100

    return prediction,confidence