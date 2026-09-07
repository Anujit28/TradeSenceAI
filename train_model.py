
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from data import get_stock_data
from indicators import add_indicators
from model import prepare_data

# NIFTY 50 stocks (Yahoo Finance symbols)
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

all_features = []
all_targets = []

for stock in NIFTY50:
    try:
        print(f"Downloading {stock}...")

        df = get_stock_data(stock, period="5y")
        df = add_indicators(df)

        X, y = prepare_data(df)

        all_features.append(X)
        all_targets.append(y)

    except Exception as e:
        print(f"Skipping {stock}: {e}")

# Combine all stocks
X = pd.concat(all_features)
y = pd.concat(all_targets)

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    shuffle=False
)

# Train model
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))

# Save model
joblib.dump(model, "stock_model.pkl")

print("Model saved successfully.")