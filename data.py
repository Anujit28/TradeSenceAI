import yfinance as yf

def get_stock_data(symbol, period="1y"):
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    if df.empty:
        raise ValueError("Invalid stock symbol or no data found.")

    return df