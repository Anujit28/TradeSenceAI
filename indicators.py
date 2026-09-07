from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
from ta.volatility import BollingerBands

def add_indicators(df):
    # Moving Averages
    df["SMA20"] = SMAIndicator(close=df["Close"], window=20).sma_indicator()
    df["SMA50"] = SMAIndicator(close=df["Close"], window=50).sma_indicator()

    # RSI
    df["RSI"] = RSIIndicator(close=df["Close"], window=14).rsi()

    # MACD
    macd = MACD(close=df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    # Bollinger Bands
    bb = BollingerBands(close=df["Close"], window=20)
    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_LOWER"] = bb.bollinger_lband()

    return df