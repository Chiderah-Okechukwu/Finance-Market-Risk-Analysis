import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Load daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# Select portfolio assets
assets = ["AAPL", "AMZN", "JPM", "MSFT", "XOM"]
asset_returns = returns[assets]

# Calculate annualized covariance matrix
covariance_matrix = asset_returns.cov() * 252

# Number of assets
number_of_assets = len(assets)

# Objective function: portfolio variance
def portfolio_variance(weights):
    return np.dot(
        weights.T,
        np.dot(covariance_matrix, weights)
    )

# Constraint: weights must sum to 1
constraints = ({
    "type": "eq",
    "fun": lambda weights: np.sum(weights) - 1
})

# Constraint: no short selling
bounds = tuple(
    (0, 1) for asset in assets
)

# Initial equal weights
initial_weights = np.array(
    [1 / number_of_assets] * number_of_assets
)

# Run optimisation
result = minimize(
    portfolio_variance,
    initial_weights,
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)

# Check optimisation result
if not result.success:
    raise RuntimeError(
        f"Optimisation failed: {result.message}"
    )

# Extract optimal weights
optimal_weights = result.x

# Calculate minimum portfolio volatility
minimum_variance = result.fun
minimum_volatility = np.sqrt(minimum_variance)

# Calculate annualized portfolio return
mean_daily_returns = asset_returns.mean()
annualized_returns = mean_daily_returns * 252

minimum_variance_return = np.dot(
    optimal_weights,
    annualized_returns
)

# Display results
print("Minimum-Variance Portfolio Optimisation")
print("\nOptimal Portfolio Weights:")

for asset, weight in zip(assets, optimal_weights):
    print(f"{asset}: {weight:.2%}")

print("\nPortfolio Results:")
print(f"Annualized Return: {minimum_variance_return:.2%}")
print(f"Annualized Volatility: {minimum_volatility:.2%}")
print(f"Portfolio Variance: {minimum_variance:.6f}")
print(f"Total Weight: {optimal_weights.sum():.4f}")