
import pandas as pd
import numpy as np
from pathlib import Path

# Load daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# Select the five individual stocks
portfolio_assets = ["AAPL", "AMZN", "JPM", "MSFT", "XOM"]

# Assign equal weights
weights = np.array([0.20, 0.20, 0.20, 0.20, 0.20])

# Calculate daily portfolio returns
portfolio_returns = (
    returns[portfolio_assets] * weights
).sum(axis=1)

# Calculate annualised portfolio metrics
portfolio_mean_daily = portfolio_returns.mean()
portfolio_daily_volatility = portfolio_returns.std()

portfolio_annual_return = portfolio_mean_daily * 252
portfolio_annual_volatility = (
    portfolio_daily_volatility * np.sqrt(252)
)

# Calculate individual asset metrics
individual_returns = returns[portfolio_assets + ["SPY"]]

comparison = pd.DataFrame({
    "Annualized Return": individual_returns.mean() * 252,
    "Annualized Volatility": individual_returns.std() * np.sqrt(252)
})

# Add our equally weighted portfolio
comparison.loc["Equal-Weight Portfolio"] = [
    portfolio_annual_return,
    portfolio_annual_volatility
]

# Save portfolio daily returns
portfolio_returns.to_csv(
    "data/processed/portfolio_returns.csv",
    header=["Portfolio Return"]
)

# Save comparison results
output_path = Path("data/processed/portfolio_comparison.csv")
comparison.to_csv(output_path)

print("Portfolio analysis completed!")

print("\nPortfolio Allocation:")
for asset, weight in zip(portfolio_assets, weights):
    print(f"{asset}: {weight:.0%}")

print("\nPortfolio Daily Return:")
print(portfolio_mean_daily)

print("\nPortfolio Annualised Return:")
print(portfolio_annual_return)

print("\nPortfolio Annualised Volatility:")
print(portfolio_annual_volatility)

print("\nIndividual Assets vs Portfolio:")
print(comparison.round(4))

print(f"\nSaved comparison to: {output_path}")
