import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class EMACrossover:
    def __init__(self, ticker, start_date, end_date, short_window=20, long_window=50):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.short_window = short_window
        self.long_window = long_window
        self.data = None

        # Download the historical data
        self.data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        self.calculate_ema()
        self.generate_signals()

    def calculate_ema(self):
        """Calculate short-term and long-term EMAs."""
        self.data['EMA_Short'] = self.data['Close'].ewm(span=self.short_window, adjust=False).mean()
        self.data['EMA_Long'] = self.data['Close'].ewm(span=self.long_window, adjust=False).mean()

    def generate_signals(self):
        """Generate buy/sell signals based on EMA crossover."""
        self.data['Signal'] = 0.0
        self.data['Signal'] = np.where(self.data['EMA_Short'] > self.data['EMA_Long'], 1.0, 0.0)
        self.data['Crossover'] = self.data['Signal'].diff()

    def plot_results(self):
        """Plot the results with buy/sell signals."""
        plt.figure(figsize=(16, 9))
        plt.plot(self.data['Close'], label='Close Price', color='blue', lw=2.5, zorder=1)
        plt.plot(self.data['EMA_Short'], label=f'{self.short_window}-Day EMA', color='green', lw=1.5, linestyle='--',
                 zorder=2)
        plt.plot(self.data['EMA_Long'], label=f'{self.long_window}-Day EMA', color='red', lw=1.5, linestyle='--',
                 zorder=2)

        # Mark buy signals with a small offset to be clearly visible
        plt.scatter(self.data[self.data['Crossover'] == 1.0].index,
                    self.data['Close'][self.data['Crossover'] == 1.0] * 1.01,  # offset slightly above the line
                    marker='^', color='green', s=100, label='Buy Signal', zorder=3)

        # Mark sell signals with a small offset to be clearly visible
        plt.scatter(self.data[self.data['Crossover'] == -1.0].index,
                    self.data['Close'][self.data['Crossover'] == -1.0] * 0.99,  # offset slightly below the line
                    marker='v', color='red', s=100, label='Sell Signal', zorder=3)

        plt.title(f'{self.ticker} EMA Crossover Strategy', fontsize=16)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Price ($)', fontsize=14)
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.legend(loc='upper left', fontsize=12, frameon=True, shadow=True)
        plt.tight_layout()
        plt.show()


# Example of running the strategy
ema_strategy = EMACrossover(ticker='AAPL', start_date='2018-03-24', end_date='2023-03-24')
ema_strategy.plot_results()