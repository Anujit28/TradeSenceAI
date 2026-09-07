def generate_signal(df):
    latest = df.iloc[-1]

    score = 0
    reasons = []

    # RSI
    if latest["RSI"] < 30:
        score += 2
        reasons.append("RSI indicates oversold.")
    elif latest["RSI"] > 70:
        score -= 2
        reasons.append("RSI indicates overbought.")

    # MACD
    if latest["MACD"] > latest["MACD_SIGNAL"]:
        score += 1
        reasons.append("MACD bullish crossover.")
    else:
        score -= 1
        reasons.append("MACD bearish crossover.")

    # Moving Average
    if latest["SMA20"] > latest["SMA50"]:
        score += 1
        reasons.append("20-day SMA is above 50-day SMA.")
    else:
        score -= 1
        reasons.append("20-day SMA is below 50-day SMA.")

    # Recommendation
    if score >= 3:
        recommendation = "BUY"
    elif score <= -2:
        recommendation = "SELL"
    else:
        recommendation = "HOLD"

    confidence = min(abs(score) * 25, 100)

    return recommendation, confidence, reasons