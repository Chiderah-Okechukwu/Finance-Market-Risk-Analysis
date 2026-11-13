
import pandas as pd

# Load daily stock returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# Select the five individual stocks
assets = ["AAPL", "AMZN", "JPM", "MSFT", "XOM"]
asset_returns = returns[assets]

# Separate training and testing periods
training_data = asset_returns.loc[
    "2021-11-09":"2024-12-31"
]

testing_data = asset_returns.loc[
    "2025-01-01":"2026-11-06"
]

# Display the periods and observations
print("Training Period:")
print(training_data.index.min(), "to", training_data.index.max())
print("Observations:", len(training_data))

print("\nTesting Period:")
print(testing_data.index.min(), "to", testing_data.index.max())
print("Observations:", len(testing_data))


import numpy as np
from scipy.optimize import minimize

# Calculate covariance matrix using training data only
covariance_matrix = training_data.cov() * 252

# Define portfolio variance
def portfolio_variance(weights):
    return weights.T @ covariance_matrix @ weights

# Require weights to sum to 1
constraints = {
    "type": "eq",
    "fun": lambda weights: np.sum(weights) - 1
}

# No short selling
bounds = tuple((0, 1) for _ in assets)

# Initial allocation
initial_weights = np.array([0.20] * len(assets))

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

# Display optimal weights
print("\nOut-of-Sample Portfolio Weights:")

for asset, weight in zip(assets, optimal_weights):
    print(f"{asset}: {weight:.2%}")

print("\nTotal Weight:", f"{optimal_weights.sum():.4f}")


# Calculate equal-weight portfolio returns
equal_weight_returns = (
    testing_data * 0.20
).sum(axis=1)

# Calculate minimum-variance portfolio returns
minimum_variance_returns = (
    testing_data * optimal_weights
).sum(axis=1)

# Load SPY benchmark returns for testing period
spy_returns = returns.loc[
    testing_data.index, "SPY"
]

# Combine all three return series
out_of_sample_returns = pd.DataFrame({
    "Equal-Weight": equal_weight_returns,
    "Minimum-Variance": minimum_variance_returns,
    "SPY": spy_returns
})

# Save testing-period returns
out_of_sample_returns.to_csv(
    "data/processed/out_of_sample_returns.csv"
)

print("\nOut-of-Sample Returns:")
print(out_of_sample_returns.head())

print("\nTesting observations:")
print(len(out_of_sample_returns))

print("\nReturns saved successfully.")


# Calculate out-of-sample performance metrics

results = []

risk_free_rate = 0.0

for name in out_of_sample_returns.columns:

    daily_returns = out_of_sample_returns[name].dropna()

    # Annualised arithmetic return
    annual_return = daily_returns.mean() * 252

    # Annualised volatility
    annual_volatility = (
        daily_returns.std() * np.sqrt(252)
    )

    # Sharpe ratio (assuming zero risk-free rate)
    sharpe_ratio = (
        (daily_returns.mean() - risk_free_rate / 252)
        / daily_returns.std()
    ) * np.sqrt(252)

    # Calculate cumulative wealth
    wealth = (1 + daily_returns).cumprod()

    # Maximum drawdown
    running_peak = wealth.cummax()

    drawdown = (wealth / running_peak) - 1

    maximum_drawdown = drawdown.min()

    # Compound annual growth rate
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

# Create comparison table
out_of_sample_comparison = (
    pd.DataFrame(results).set_index("Portfolio")
)

# Save comparison
out_of_sample_comparison.to_csv(
    "data/processed/out_of_sample_comparison.csv"
)

print("\nOUT-OF-SAMPLE PERFORMANCE COMPARISON")

print(out_of_sample_comparison.round(4))

print("\nComparison saved successfully.")
