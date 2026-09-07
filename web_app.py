import streamlit as st
import plotly.graph_objects as go

from data import get_stock_data
from indicators import add_indicators
from strategy import generate_signal
from predict import predict_stock

st.set_page_config(page_title="TradeSense AI", layout="wide")

st.title("📈 TradeSense AI")
st.write("Algorithmic Trading Recommendation Dashboard")

symbol = st.text_input(
    "Enter Stock Symbol (Example: RELIANCE.NS, TCS.NS, INFY.NS)",
    "RELIANCE.NS"
)

if st.button("Analyze Stock"):

    try:
        df = get_stock_data(symbol)
        df = add_indicators(df)

        prediction, ml_confidence = predict_stock(df)

        if prediction == 1:
         ml_signal = "BUY"
        else:
         ml_signal = "SELL"

        recommendation, confidence, reasons = generate_signal(df)

        latest = df.iloc[-1]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Current Price", f"₹{latest['Close']:.2f}")
        col2.metric("RSI", f"{latest['RSI']:.2f}")
        col3.metric("Rule Signal", recommendation)
        col4.metric("AI Signal", ml_signal)

        st.success(f"Confidence: {confidence}%")
        st.info(f"AI Confidence: {ml_confidence:.1f}%")

        st.subheader("Why?")
        for reason in reasons:
            st.write("•", reason)

        st.subheader("AI Market Prediction")

        st.metric(
            "Next-Day Prediction",
            ml_signal,
            f"{ml_confidence:.1f}% confidence"
        )

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Candlestick"
        ))

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["SMA20"],
            name="SMA20"
        ))

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["SMA50"],
            name="SMA50"
        ))

        fig.update_layout(
            title=f"{symbol} Price Chart",
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Latest Data")

        st.dataframe(
            df[["Close", "RSI", "MACD", "MACD_SIGNAL", "SMA20", "SMA50"]].tail()
        )

    except Exception as e:
        st.error(str(e))
