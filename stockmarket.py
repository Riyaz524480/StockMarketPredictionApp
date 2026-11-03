import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(page_title="Stock Market Prediction App", layout="wide")

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("📈 Stock Market Prediction App")
st.caption("Educational ML Project Using Historical Stock Data")
st.warning("⚠️ This application is for educational purposes only. Not financial advice.")

# ============================
# SIDEBAR CONTROLS
# ============================
st.sidebar.header("📊 Prediction Controls")

stocks = (
    "AAPL", "GOOG", "MSFT", "GME", "NVDA",
    "INTC", "TSLA", "DELL", "AMZN",
    "BTC-USD", "DOGE-USD", "ESTC"
)

selected_stock = st.sidebar.selectbox("Select Stock", stocks)
n_years = st.sidebar.slider("Years of Prediction", 1, 5, 1)
period = n_years * 365
run = st.sidebar.button("Predict")

# ----------------------------
# Load Data Function
# ----------------------------
@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    if data.empty:
        return pd.DataFrame()
    data.reset_index(inplace=True)
    return data

# ============================
# MAIN CONTENT
# ============================
if run:

    # ----------------------------
    # Load Data
    # ----------------------------
    data = load_data(selected_stock)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    if data.empty:
        st.error("No data found for this ticker.")
        st.stop()

    # ----------------------------
    # Raw Data
    # ----------------------------
    st.subheader("Raw Data")
    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    st.write(data.tail())

    # ----------------------------
    # Raw Price Plot
    # ----------------------------
    st.subheader("📊 Stock Price Visualization")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Open'],
        name="Open Price", line=dict(color="#1f77b4")
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Close'],
        name="Close Price", line=dict(color="#ff7f0e")
    ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # Prepare Data for Prophet
    # ----------------------------
    df_train = data[['Date', 'Close']].rename(
        columns={"Date": "ds", "Close": "y"}
    )
    df_train['ds'] = pd.to_datetime(df_train['ds'])
    df_train['y'] = pd.to_numeric(df_train['y'])
    df_train.dropna(inplace=True)

    # ----------------------------
    # Train Model
    # ----------------------------
    model = Prophet()
    model.fit(df_train)

    # ----------------------------
    # Forecast
    # ----------------------------
    future = model.make_future_dataframe(periods=period)
    forecast = model.predict(future)

    forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
        columns={
            'ds': 'Date',
            'yhat': 'Predicted Price',
            'yhat_lower': 'Min Expected Price',
            'yhat_upper': 'Max Expected Price'
        }
    )

    # ----------------------------
    # Forecast Table
    # ----------------------------
    st.subheader("Forecasted Data")
    st.write(forecast_display.tail())

    # ----------------------------
    # Forecast Plot (Clean)
    # ----------------------------
    st.subheader("📊 Forecast Plot")

    fig1 = plot_plotly(model, forecast)

    # Remove all "All" range selector buttons
    fig1.for_each_xaxis(
        lambda x: x.update(rangeselector=dict(visible=False))
    )

    fig1.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig1, use_container_width=True)
    # ----------------------------
    # 📈 Next Trading Day Prediction & Signal (FIXED)
    # ----------------------------
    st.subheader("📅 Next Trading Day Prediction & Signal")

    # Last actual date & close
    last_actual_date = df_train['ds'].max().normalize()
    last_close = data.iloc[-1]['Close']

    # 👉 Ensure strictly AFTER last actual date
    future_forecast = forecast[
        forecast['ds'].dt.normalize() > last_actual_date
    ]

    # Pick first truly future day
    next_day_row = future_forecast.iloc[0]

    next_date = next_day_row['ds'].date()
    predicted_price = next_day_row['yhat']
    lower_price = next_day_row['yhat_lower']
    upper_price = next_day_row['yhat_upper']

    # ----------------------------
    # Signal logic
    # ----------------------------
    change_pct = ((predicted_price - last_close) / last_close) * 100

    if change_pct > 1:
        signal = "🟢 BUY"
    elif change_pct < -1:
        signal = "🔴 SELL"
    else:
        signal = "🟡 HOLD"

    # ----------------------------
    # Display
    # ----------------------------
    st.success(f"""
    **Next Trading Day**

    **Last Close Price:** {last_close:.2f}  
    **Predicted Price:** {predicted_price:.2f}  
    **Lower Estimate:** {lower_price:.2f}  
    **Upper Estimate:** {upper_price:.2f}  

    **Expected Change:** {change_pct:.2f}%

    **Signal:** **{signal}**
    """)
