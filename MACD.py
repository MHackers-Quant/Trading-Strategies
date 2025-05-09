import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates

class MACDStrategy:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker.strip().upper()
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.download_data()
        if self.data is not None:
            self.calculate_macd()
            self.generate_signals()

    def download_data(self):
        """Download historical data with error handling."""
        try:
            data = yf.download(self.ticker, start=self.start_date, end=self.end_date, progress=False)
            if data.empty:
                print(f"Error: No data found for ticker {self.ticker}.")
                return None
            data.reset_index(inplace=True)
            return data
        except Exception as e:
            print(f"Error downloading data for ticker {self.ticker}: {e}")
            return None

    def calculate_macd(self):
        """Calculate the MACD, signal line, and histogram."""
        close = self.data['Close']
        exp1 = close.ewm(span=12, adjust=False).mean()
        exp2 = close.ewm(span=26, adjust=False).mean()
        self.data['MACD'] = exp1 - exp2
        self.data['MACD_SIGNAL'] = self.data['MACD'].ewm(span=9, adjust=False).mean()
        self.data['MACD_HIST'] = self.data['MACD'] - self.data['MACD_SIGNAL']

    def generate_signals(self):
        """Generate buy and sell signals."""
        self.data['Buy_Signal'] = False
        self.data['Sell_Signal'] = False

        for i in range(1, len(self.data)):
            if (self.data['MACD'].iloc[i] > self.data['MACD_SIGNAL'].iloc[i] and 
                self.data['MACD'].iloc[i-1] <= self.data['MACD_SIGNAL'].iloc[i-1] and 
                self.data['MACD'].iloc[i] < 0):
                self.data.loc[self.data.index[i], 'Buy_Signal'] = True

            if (self.data['MACD'].iloc[i] < self.data['MACD_SIGNAL'].iloc[i] and 
                self.data['MACD'].iloc[i-1] >= self.data['MACD_SIGNAL'].iloc[i-1] and 
                self.data['MACD'].iloc[i] > 0):
                self.data.loc[self.data.index[i], 'Sell_Signal'] = True

    def print_signals(self):
        """Print the generated buy and sell signals."""
        if self.data is None:
            return
        buy_signals = self.data[self.data['Buy_Signal']]
        print("\n--- BUY SIGNALS ---")
        for _, row in buy_signals.iterrows():
            date = row['Date'].strftime('%Y-%m-%d') if isinstance(row['Date'], pd.Timestamp) else row['Date']
            print(f"Date: {date}, Price: ${row['Close']:.2f}")
        
        sell_signals = self.data[self.data['Sell_Signal']]
        print("\n--- SELL SIGNALS ---")
        for _, row in sell_signals.iterrows():
            date = row['Date'].strftime('%Y-%m-%d') if isinstance(row['Date'], pd.Timestamp) else row['Date']
            print(f"Date: {date}, Price: ${row['Close']:.2f}")

    def plot_results(self):
        """Plot the stock price with signals and the MACD indicator with histogram."""
        if self.data is None:
            return
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

        # Plot closing prices and buy/sell signals
        ax1.plot(self.data['Date'], self.data['Close'], label='Close Price', color='blue', lw=2)
        buy_signals = self.data[self.data['Buy_Signal']]
        ax1.scatter(buy_signals['Date'], buy_signals['Close'], color='green', marker='^', s=200, label='Buy Signal', zorder=5)
        sell_signals = self.data[self.data['Sell_Signal']]
        ax1.scatter(sell_signals['Date'], sell_signals['Close'], color='red', marker='v', s=200, label='Sell Signal', zorder=5)
        ax1.set_title(f'{self.ticker} MACD Strategy', fontsize=16)
        ax1.set_ylabel('Price ($)', fontsize=12)
        ax1.legend(loc='best')
        ax1.grid(alpha=0.7, linestyle='--')

        # Plot MACD, Signal Line, and Histogram
        ax2.plot(self.data['Date'], self.data['MACD'], label='MACD', color='purple', lw=1.5)
        ax2.plot(self.data['Date'], self.data['MACD_SIGNAL'], label='Signal Line', color='orange', lw=1.5, linestyle='--')
        ax2.bar(self.data['Date'], self.data['MACD_HIST'], label='MACD Histogram', color='gray', alpha=0.5, width=1)
        ax2.axhline(y=0, color='black', linestyle='--', alpha=0.6)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('MACD', fontsize=12)
        ax2.legend(loc='best')
        ax2.grid(alpha=0.7, linestyle='--')

        plt.tight_layout()
        plt.show()

# === Run the strategy ===
if __name__ == "__main__":
    ticker = input("Enter the stock ticker: ").strip()
    start = input("Enter the start date (YYYY-MM-DD): ").strip()
    end = input("Enter the end date (YYYY-MM-DD): ").strip()

    if ticker:
        macd_strategy = MACDStrategy(ticker, start_date=start, end_date=end)
        macd_strategy.plot_results()
        macd_strategy.print_signals()
    else:
        print("Error: Please provide a valid stock ticker.")
