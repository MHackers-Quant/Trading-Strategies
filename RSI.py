import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class RSIStrategy:
    def __init__(self, ticker, start_date, end_date, rsi_period=14, overbought=70, oversold=30):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.rsi_period = rsi_period
        self.overbought = overbought
        self.oversold = oversold
        self.data = None

        # Download the historical data
        self.data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        self.calculate_rsi()

    def calculate_rsi(self):
        # Calculate price changes
        delta = self.data['Close'].diff()

        # Calculate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate the rolling averages for gains and losses
        avg_gain = gain.rolling(window=self.rsi_period, min_periods=1).mean()
        avg_loss = loss.rolling(window=self.rsi_period, min_periods=1).mean()

        # Compute Relative Strength (RS) and RSI
        rs = avg_gain / avg_loss
        self.data['RSI'] = 100 - (100 / (1 + rs))

    def plot_results(self):
        """Plot the results without buy/sell signals."""
        plt.figure(figsize=(16, 9))

        # Plot price data
        plt.subplot(2, 1, 1)
        plt.plot(self.data['Close'], label='Close Price', color='blue', lw=2.5, zorder=1)
        plt.title(f'{self.ticker} RSI Strategy', fontsize=16)
        plt.ylabel('Price ($)', fontsize=14)
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.legend(loc='upper left', fontsize=12, frameon=True, shadow=True)

        # Plot RSI
        plt.subplot(2, 1, 2)
        plt.plot(self.data['RSI'], label='RSI', color='purple', lw=1.5)
        plt.axhline(y=self.overbought, color='red', linestyle='--', label=f'Overbought ({self.overbought})')
        plt.axhline(y=self.oversold, color='green', linestyle='--', label=f'Oversold ({self.oversold})')
        plt.title('Relative Strength Index (RSI)', fontsize=14)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('RSI Value', fontsize=14)
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.legend(loc='upper left', fontsize=12, frameon=True, shadow=True)

        plt.tight_layout()
        plt.show()


# Example of running the RSI strategy
ticker = input("Enter the stock ticker: ").strip()
start = input("Enter the start date: ").strip()
end = input("Enter the end date: ").strip()
rsi_strategy = RSIStrategy(ticker=ticker, start_date=start, end_date=end)
rsi_strategy.plot_results()

