
import pandas as pd
from pathlib import Path

# Load historical stock prices
prices = pd.read_csv(
    "data/raw/stock_prices.csv",
    index_col=0,
    parse_dates=True
)

# Calculate daily percentage returns
daily_returns = prices.pct_change(fill_method=None)

# Remove the first row because it has no previous trading day
daily_returns = daily_returns.dropna(how="all")

# Save daily returns
output_path = Path("data/processed/daily_returns.csv")
daily_returns.to_csv(output_path)

print("Daily returns calculated successfully!")

print("\nFirst five observations:")
print(daily_returns.head())

print("\nSummary statistics:")
print(daily_returns.describe())

print(f"\nSaved to: {output_path}")
