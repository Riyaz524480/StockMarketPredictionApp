
# Stock Market Prediction App

An interactive Machine Learning web application built using Python, Streamlit, Yahoo Finance, and Facebook Prophet to analyze historical stock prices and generate price forecasts.

## Overview

The Stock Market Prediction App allows users to select a stock or cryptocurrency, visualize historical prices, and explore forecasts generated from historical closing-price data.

The application provides an interactive dashboard designed to demonstrate the use of time-series forecasting and data visualization in a practical Machine Learning project.

## Features

- Select from multiple stocks and cryptocurrencies.
- Download historical market data using Yahoo Finance.
- View historical opening and closing prices.
- Train a Prophet forecasting model on historical closing prices.
- Generate forecasts for 1 to 5 years.
- Display forecast tables with predicted prices and estimated lower and upper bounds.
- Visualize forecast results using interactive Plotly charts.
- Display the latest available closing price and the model's first future forecast.
- Show an illustrative BUY, SELL, or HOLD signal based on predicted percentage change.

## Technologies Used

- Python
- Streamlit
- Facebook Prophet
- yfinance
- Pandas
- Plotly

## Supported Symbols

The application currently includes:

- AAPL — Apple
- GOOG — Alphabet
- MSFT — Microsoft
- GME — GameStop
- NVDA — NVIDIA
- INTC — Intel
- TSLA — Tesla
- DELL — Dell Technologies
- AMZN — Amazon
- BTC-USD — Bitcoin
- DOGE-USD — Dogecoin
- ESTC — Elastic

Availability of historical data depends on the selected symbol and the Yahoo Finance data service.

## How It Works

1. The user selects a market symbol.
2. Historical price data is downloaded from Yahoo Finance.
3. The application prepares the closing-price time series.
4. A Prophet forecasting model is trained on the available historical observations.
5. The model generates future estimates and uncertainty bounds.
6. Interactive charts and forecast tables are displayed.
7. An illustrative signal is calculated from the difference between the latest close and the first future model forecast.

## Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run stockmarket.py
```

The application will open in your browser, usually at:

http://localhost:8501

## Deployment

This application can be deployed using Streamlit Community Cloud.

1. Push the project files to GitHub.
2. Open https://share.streamlit.io/
3. Connect your GitHub account.
4. Select the repository and the `main` branch.
5. Set the main file path to `stockmarket.py`.
6. Deploy the application.

## Limitations

- Forecasts are based on historical closing prices and may not reflect future market behavior.
- Market prices are subject to volatility and unexpected events.
- Forecast uncertainty intervals are estimates, not guaranteed price ranges.
- Yahoo Finance data availability and service behavior may change.
- The application does not account for all financial, economic, or company-specific factors.
- The BUY/SELL/HOLD label is a simple rule-based illustration, not a validated investment strategy.

## Disclaimer

This project is developed for educational and demonstration purposes only. It is not financial advice and should not be used as the sole basis for investment decisions.

## Author

**Riyaz Ahmad**

BCA | Aspiring Web Developer

