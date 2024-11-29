import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import argparse

def bollinger_bands(ticker, start_date, end_date, period= 20, k = 2):
    data = yf.download(ticker, start = start_date, end = end_date, progress =False)
    if data.empty:
        print("No data found for the given ticker or date range")
        return 
    data['SMA'] = data['Close'].rolling(window=period).mean()
    data['STD'] = data['Close'].rolling(window=period).std()
    data['Upper Band'] = data['SMA'] + (k * data['STD'])
    data['Lower Band'] = data['SMA'] - (k * data['STD'])
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Close'], label=f'{ticker} Closing Price', color='blue')
    plt.plot(data.index, data['SMA'], label=f'{period}-Day SMA', color='orange', linestyle='--')
    plt.plot(data.index, data['Upper Band'], label='Upper Band (+2 SD)', color='green', linestyle='--')
    plt.plot(data.index, data['Lower Band'], label='Lower Band (-2 SD)', color='red', linestyle='--')
    plt.fill_between(data.index, data['Lower Band'], data['Upper Band'], color='gray', alpha=0.2)
    plt.title(f"Bollinger Bands for {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc="upper left")
    plt.grid()
    plt.show()
def main():
    parser = argparse.ArgumentParser(description="Calculate and plot Bollinger Bands for a stock.")
    parser.add_argument("ticker", type=str, help="The stock ticker symbol (e.g., AAPL, MSFT).")
    parser.add_argument("start_date", type=str, help="Start date for historical data (YYYY-MM-DD).")
    parser.add_argument("end_date", type=str, help="End date for historical data (YYYY-MM-DD).")
    parser.add_argument("--period", type=int, default=20, help="Lookback period for the SMA (default: 20).")
    parser.add_argument("--k", type=float, default=2, help="Multiplier for standard deviation (default: 2).")
    args = parser.parse_args()
    bollinger_bands(args.ticker, args.start_date, args.end_date, args.period, args.k)
if __name__ == "__main__":
    main()


