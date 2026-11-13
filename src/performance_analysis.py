
import pandas as pd
import numpy as np

# Load daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# Select portfolio assets
assets = ["AAPL", "AMZN", "JPM", "MSFT", "XOM"]

# Equal-weight portfolio
weights = np.array([0.20] * 5)

portfolio_returns = (
    returns[assets] * weights
).sum(axis=1)

# Combine individual assets, benchmark and portfolio
performance_returns = returns.copy()
performance_returns["PORTFOLIO"] = portfolio_returns

# Annual risk-free rate assumption
# Zero is used initially as a simplified assumption.
risk_free_rate = 0.0

results = []

for asset in performance_returns.columns:

    asset_returns = performance_returns[asset].dropna()

    # Annualised return
    annual_return = asset_returns.mean() * 252

    # Annualised volatility
    annual_volatility = asset_returns.std() * np.sqrt(252)

    # Annualised Sharpe ratio
    daily_risk_free_rate = risk_free_rate / 252

    sharpe_ratio = (
        (asset_returns.mean() - daily_risk_free_rate)
        / asset_returns.std()
    ) * np.sqrt(252)

    # Cumulative growth of one unit invested
    wealth_index = (1 + asset_returns).cumprod()

    # Running maximum
    running_peak = wealth_index.cummax()

    # Drawdown
    drawdown = (wealth_index / running_peak) - 1

    # Maximum drawdown
    max_drawdown = drawdown.min()

    # Compounded annual growth rate
    years = len(asset_returns) / 252

    cagr = wealth_index.iloc[-1] ** (1 / years) - 1

    results.append({
        "Asset": asset,
        "Annualized Return": annual_return,
        "Annualized Volatility": annual_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Maximum Drawdown": max_drawdown,
        "CAGR": cagr
    })

# Create results table
performance_summary = pd.DataFrame(results)
performance_summary = performance_summary.set_index("Asset")

# Save results
performance_summary.to_csv(
    "data/processed/performance_summary.csv"
)

print("Performance analysis completed!")

print("\nPerformance Summary:")
print(performance_summary.round(4))

print("\nSaved to data/processed/performance_summary.csv")
