
import yfinance as yf
import pandas as pd
from pathlib import Path

# Stocks and market benchmark
tickers = [
    "AAPL",
    "MSFT",
    "JPM",
    "XOM",
    "AMZN",
    "SPY"
]

# Download five years of historical daily prices
print("Downloading financial market data...")

data = yf.download(
    tickers,
    period="5y",
    interval="1d",
    auto_adjust=True
)

# Check whether data was downloaded
if data.empty:
    raise ValueError("No data was downloaded.")

# Extract adjusted closing prices
prices = data["Close"]

# Remove rows where all prices are missing
prices = prices.dropna(how="all")

# Save the dataset
output_path = Path("data/raw/stock_prices.csv")
prices.to_csv(output_path)

print("Download completed successfully!")
print(f"Dataset saved to: {output_path}")
print(f"Number of observations: {len(prices)}")
print(prices.head())

prices = prices.dropna(how="all")

# print("\nMissing values per stock:")
# print(prices.isna().sum())

# print("\nJPM sample data:")
# print(prices["JPM"].head(10))

print("\nDataset information:")
print(prices.info())

print("\nStatistical summary:")
print(prices.describe())

print("\nDate range:")
print(prices.index.min(), "to", prices.index.max())