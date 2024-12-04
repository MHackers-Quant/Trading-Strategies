import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates


class MACDStrategy:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.download_data()
        self.calculate_macd()
        self.generate_signals()

    def download_data(self):
        """Download historical data."""
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date, progress=False)
        data.reset_index(inplace=True)  # Ensure dates are in a column, not the index
        return data

    def calculate_macd(self):
        """Calculate the MACD and signal line."""
        # Calculate MACD line
        self.data['MACD'] = self.data['Close'].ewm(span=12, adjust=False).mean() - self.data['Close'].ewm(span=26, adjust=False).mean()
        # Calculate signal line
        self.data['MACD_SIGNAL'] = self.data['MACD'].ewm(span=9, adjust=False).mean()

    def generate_signals(self):
        """Generate buy and sell signals."""
        # Create Buy and Sell columns
        self.data['Buy'] = np.nan
        self.data['Sell'] = np.nan
        
        # Identify buy/sell conditions
        buy_conditions = (self.data['MACD'] > self.data['MACD_SIGNAL']) & (self.data['MACD'].shift(1) <= self.data['MACD_SIGNAL'].shift(1))
        sell_conditions = (self.data['MACD'] < self.data['MACD_SIGNAL']) & (self.data['MACD'].shift(1) >= self.data['MACD_SIGNAL'].shift(1))
        
        # Assign buy/sell signals
        self.data.loc[buy_conditions, 'Buy'] = self.data['Close']
        self.data.loc[sell_conditions, 'Sell'] = self.data['Close']

    def print_signals(self):
        """Print out buy and sell signals"""
        # Filter and print buy signals
        buy_signals = self.data[self.data['Buy'].notna()]
        print("\n--- BUY SIGNALS ---")
        for _, row in buy_signals.iterrows():
            print(f"Date: {row['Date']}, Price: ${row['Close']:.2f}")

        # Filter and print sell signals
        sell_signals = self.data[self.data['Sell'].notna()]
        print("\n--- SELL SIGNALS ---")
        for _, row in sell_signals.iterrows():
            print(f"Date: {row['Date']}, Price: ${row['Close']:.2f}")

    def plot_results(self):
        """Plot the MACD strategy results."""
        plt.figure(figsize=(14, 8))
        date_format = mpl_dates.DateFormatter('%d %b %Y')

        # Plot Close Price
        plt.plot(self.data['Date'], self.data['Close'], label='Close Price', color='blue', lw=2)
        
        # Plot MACD and Signal Line
        plt.plot(self.data['Date'], self.data['MACD'], label='MACD', color='purple', lw=1.5)
        plt.plot(self.data['Date'], self.data['MACD_SIGNAL'], label='Signal Line', color='orange', lw=1.5, linestyle='--')

        # Buy/Sell Signals
        plt.scatter(self.data['Date'], self.data['Buy'], color='green', marker='^', s=100, label='Buy Signal')
        plt.scatter(self.data['Date'], self.data['Sell'], color='red', marker='v', s=100, label='Sell Signal')

        # Configure Plot
        plt.title(f'{self.ticker} MACD Strategy', fontsize=16)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Price ($)', fontsize=14)
        plt.legend(fontsize=12)
        plt.grid(alpha=0.7, linestyle='--')
        
        ax = plt.gca()
        ax.xaxis.set_major_formatter(date_format)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()


# Example Usage for Apple Stock
macd_strategy = MACDStrategy(ticker="AAPL", start_date="2022-03-01", end_date=pd.Timestamp.today().strftime('%Y-%m-%d'))
macd_strategy.plot_results()
macd_strategy.print_signals()
