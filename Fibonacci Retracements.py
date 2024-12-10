import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class FibonacciStockIndicator:
    def __init__(self, ticker):
        """
        Initialize Fibonacci Stock Indicator with comprehensive data handling
        """
        # Retrieve stock data
        self.ticker = ticker
        self.fetch_stock_data()

    def fetch_stock_data(self):
        """
        Fetch stock data with comprehensive error handling and logging
        """
        try:
            # Download data for past 2 months
            end_date = pd.Timestamp.now()
            start_date = end_date - pd.DateOffset(months=2)

            # Download data with verbose output
            self.data = yf.download(self.ticker, start=start_date, end=end_date, progress=False)

            # Print initial data diagnostics
            print("\n--- DATA OVERVIEW ---")
            print(f"Total data points: {len(self.data)}")
            print(f"Date range: {self.data.index[0]} to {self.data.index[-1]}")
            print("\nFirst few rows:")
            print(self.data.head())

            # Remove rows with NaN values
            self.data.dropna(inplace=True)

            # Ensure we have enough data points
            if len(self.data) < 10:
                raise ValueError("Insufficient data points")

        except Exception as e:
            print(f"Data fetch error: {e}")
            raise

    def calculate_fibonacci_levels(self):
        """
        Calculate Fibonacci retracement levels with comprehensive analysis
        """
        # Use robust method to find high and low
        high = float(self.data['High'].max())
        low = float(self.data['Low'].min())

        # Print Fibonacci level diagnostics
        print("\n--- FIBONACCI LEVELS ---")
        print(f"Highest price: {high}")
        print(f"Lowest price: {low}")

        # Fibonacci retracement levels
        levels = {
            '0%': high,
            '23.6%': high - 0.236 * (high - low),
            '38.2%': high - 0.382 * (high - low),
            '50%': high - 0.5 * (high - low),
            '61.8%': high - 0.618 * (high - low),
            '100%': low
        }

        # Print detailed Fibonacci levels
        for level, price in levels.items():
            print(f"{level} Level: {price:.2f}")

        return levels

    def generate_trading_signals(self):
        """
        Generate comprehensive trading signals
        """
        # Calculate multiple moving averages for robust analysis
        self.data['SMA_10'] = self.data['Close'].rolling(window=10).mean()
        self.data['SMA_30'] = self.data['Close'].rolling(window=30).mean()

        # Initialize signals DataFrame
        signals = pd.DataFrame(index=self.data.index)
        signals['Close'] = self.data['Close']
        signals['Signal'] = 0

        # Advanced crossover signal generation
        # Buy signal: 10-day MA crosses above 30-day MA
        buy_signal = (
                (self.data['SMA_10'] > self.data['SMA_30']) &
                (self.data['SMA_10'].shift(1) <= self.data['SMA_30'].shift(1))
        )

        # Sell signal: 10-day MA crosses below 30-day MA
        sell_signal = (
                (self.data['SMA_10'] < self.data['SMA_30']) &
                (self.data['SMA_10'].shift(1) >= self.data['SMA_30'].shift(1))
        )

        # Apply signals
        signals.loc[buy_signal, 'Signal'] = 1
        signals.loc[sell_signal, 'Signal'] = -1

        # Print signal diagnostics
        print("\n--- TRADING SIGNALS ---")
        buy_count = len(signals[signals['Signal'] == 1])
        sell_count = len(signals[signals['Signal'] == -1])
        print(f"Total Buy Signals: {buy_count}")
        print(f"Total Sell Signals: {sell_count}")

        return signals

    def plot_fibonacci_chart(self):
        """
        Create comprehensive stock chart with detailed visualization
        """
        # Calculate Fibonacci levels
        fib_levels = self.calculate_fibonacci_levels()

        # Generate signals
        signals = self.generate_trading_signals()

        # Create plot with improved readability
        plt.figure(figsize=(20, 10))
        plt.title(f'{self.ticker} Stock Analysis with Fibonacci Levels', fontsize=16)

        # Plot price with increased line width
        plt.plot(self.data.index, self.data['Close'], label='Close Price', color='black', linewidth=2)

        # Plot Fibonacci levels with improved visibility
        for level, price in fib_levels.items():
            plt.axhline(y=price, color='blue', linestyle='--', alpha=0.7,
                        label=f'Fib {level}: {price:.2f}')

        # Plot buy/sell signals
        buy_signals = signals[signals['Signal'] == 1]
        sell_signals = signals[signals['Signal'] == -1]

        plt.scatter(buy_signals.index, buy_signals['Close'],
                    color='green', marker='^', label='Buy Signal', s=100)
        plt.scatter(sell_signals.index, sell_signals['Close'],
                    color='red', marker='v', label='Sell Signal', s=100)

        # Annotate dates with closing prices
        for idx, row in self.data.iterrows():
            close_price = float(row['Close'])
            plt.annotate(f'${close_price:.2f}',
                         (idx, close_price),
                         xytext=(10, 5),
                         textcoords='offset points',
                         fontsize=8,
                         color='gray')

        plt.legend(loc='best')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()


def main():
    # Get ticker from user input
    ticker = input("Enter stock ticker symbol (e.g., AAPL): ").upper()

    try:
        # Create and plot Fibonacci indicator
        indicator = FibonacciStockIndicator(ticker)
        indicator.plot_fibonacci_chart()
    except Exception as e:
        print(f"Error processing {ticker}: {e}")


if __name__ == "__main__":
    main()