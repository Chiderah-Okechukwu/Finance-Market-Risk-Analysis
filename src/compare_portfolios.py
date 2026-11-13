import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Load daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

assets = ["AAPL", "AMZN", "JPM", "MSFT", "XOM"]
asset_returns = returns[assets]

# Calculate annualized covariance matrix
covariance_matrix = asset_returns.cov() * 252

# Portfolio variance function
def portfolio_variance(weights):
    return weights.T @ covariance_matrix @ weights

# Portfolio constraints
constraints = {
    "type": "eq",
    "fun": lambda weights: np.sum(weights) - 1
}

bounds = tuple((0, 1) for _ in assets)

initial_weights = np.array([0.20] * 5)

# Optimise portfolio
result = minimize(
    portfolio_variance,
    initial_weights,
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)

if not result.success:
    raise RuntimeError(result.message)

optimal_weights = result.x

# Calculate portfolio daily returns
equal_weight_returns = (
    asset_returns * 0.20
).sum(axis=1)

minimum_variance_returns = (
    asset_returns * optimal_weights
).sum(axis=1)

# Compare portfolios with benchmark
portfolio_data = pd.DataFrame({
    "Equal-Weight": equal_weight_returns,
    "Minimum-Variance": minimum_variance_returns,
    "SPY": returns["SPY"]
})

# Calculate performance metrics
results = []

risk_free_rate = 0.0

for name in portfolio_data.columns:

    daily_returns = portfolio_data[name].dropna()

    annual_return = daily_returns.mean() * 252

    annual_volatility = (
        daily_returns.std() * np.sqrt(252)
    )

    sharpe_ratio = (
        (daily_returns.mean() - risk_free_rate / 252)
        / daily_returns.std()
    ) * np.sqrt(252)

    wealth = (1 + daily_returns).cumprod()

    running_peak = wealth.cummax()

    drawdown = (wealth / running_peak) - 1

    maximum_drawdown = drawdown.min()

    years = len(daily_returns) / 252

    cagr = wealth.iloc[-1] ** (1 / years) - 1

    results.append({
        "Portfolio": name,
        "Annualized Return": annual_return,
        "Annualized Volatility": annual_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Maximum Drawdown": maximum_drawdown,
        "CAGR": cagr
    })

comparison = pd.DataFrame(results).set_index("Portfolio")

# Save results
comparison.to_csv(
    "data/processed/portfolio_comparison_optimised.csv"
)

portfolio_data.to_csv(
    "data/processed/portfolio_returns_comparison.csv"
)

print("Portfolio comparison completed!")

print("\nOptimised Weights:")
for asset, weight in zip(assets, optimal_weights):
    print(f"{asset}: {weight:.2%}")

print("\nPortfolio Performance Comparison:")
print(comparison.round(4))

print("\nResults saved successfully.")