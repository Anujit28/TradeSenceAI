import streamlit as st
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

from data import get_stock_data
from indicators import add_indicators
from model import prepare_data

# NIFTY 50 symbols (same list as train_model.py)
NIFTY50 = [
    "ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","ASIANPAINT.NS","AXISBANK.NS",
    "BAJAJ-AUTO.NS","BAJFINANCE.NS","BAJAJFINSV.NS","BEL.NS","BHARTIARTL.NS",
    "BPCL.NS","BRITANNIA.NS","CIPLA.NS","COALINDIA.NS","DRREDDY.NS",
    "EICHERMOT.NS","ETERNAL.NS","GRASIM.NS","HCLTECH.NS","HDFCBANK.NS",
    "HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","HINDUNILVR.NS","ICICIBANK.NS",
    "INDUSINDBK.NS","INFY.NS","ITC.NS","JIOFIN.NS","JSWSTEEL.NS",
    "KOTAKBANK.NS","LT.NS","M&M.NS","MARUTI.NS","NESTLEIND.NS",
    "NTPC.NS","ONGC.NS","POWERGRID.NS","RELIANCE.NS","SBILIFE.NS",
    "SHRIRAMFIN.NS","SBIN.NS","SUNPHARMA.NS","TATACONSUM.NS","TATAMOTORS.NS",
    "TATASTEEL.NS","TCS.NS","TECHM.NS","TITAN.NS","TRENT.NS"
]

@st.cache_resource
def load_model():
    all_X = []
    all_y = []

    for stock in NIFTY50:
        try:
            df = get_stock_data(stock, period="5y")
            df = add_indicators(df)
            X, y = prepare_data(df)
            all_X.append(X)
            all_y.append(y)
        except:
            pass

    X = pd.concat(all_X)
    y = pd.concat(all_y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model

model = load_model()

def predict_stock(df):
    latest = df.iloc[-1]

    X = [[
        latest["RSI"],
        latest["MACD"],
        latest["MACD_SIGNAL"],
        latest["SMA20"],
        latest["SMA50"]
    ]]

    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]

    return pred, max(prob) * 100
