
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

# Define the testing period
testing_data = asset_returns.loc[
    "2025-01-01":"2026-11-06"
]

# Store monthly portfolio returns and weights
monthly_returns = []
weight_history = []

# Process one testing month at a time
for month, month_data in testing_data.groupby(
    testing_data.index.to_period("M")
):

    # Use only data available before this month's first trading day
    training_data = asset_returns.loc[
        asset_returns.index < month_data.index[0]
    ].tail(252)

    if len(training_data) < 252:
        raise ValueError("Insufficient training observations.")

    # Estimate annualised covariance matrix
    covariance_matrix = training_data.cov() * 252

    # Portfolio variance objective
    def portfolio_variance(weights):
        return weights.T @ covariance_matrix @ weights

    # Portfolio constraints
    constraints = [
        {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
    ]

    bounds = [(0, 1)] * len(assets)

    initial_weights = np.array([0.20] * len(assets))

    # Optimise portfolio weights
    result = minimize(
        portfolio_variance,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        raise RuntimeError(
            f"Optimisation failed for {month}: {result.message}"
        )

    optimal_weights = result.x

    # Calculate daily portfolio returns for this month
    minimum_variance_returns = (
        month_data * optimal_weights
    ).sum(axis=1)

    monthly_returns.append(minimum_variance_returns)

    # Record the weights used
    weight_record = {
        "Month": str(month),
        "Training Start": training_data.index[0],
        "Training End": training_data.index[-1]
    }

    for asset, weight in zip(assets, optimal_weights):
        weight_record[asset] = weight

    weight_history.append(weight_record)

# Combine monthly returns
minimum_variance_returns = pd.concat(monthly_returns)

# Equal-weight portfolio benchmark
equal_weight_returns = (
    testing_data * 0.20
).sum(axis=1)

# SPY benchmark
spy_returns = returns.loc[testing_data.index, "SPY"]

# Combine all strategies
rolling_comparison = pd.DataFrame({
    "Equal-Weight": equal_weight_returns,
    "Rolling Minimum-Variance": minimum_variance_returns,
    "SPY": spy_returns
})

# Save returns and monthly weights
rolling_comparison.to_csv(
    "data/processed/rolling_window_returns.csv"
)

weights_df = pd.DataFrame(weight_history)

weights_df.to_csv(
    "data/processed/rolling_window_weights.csv",
    index=False
)

print("ROLLING-WINDOW OPTIMISATION COMPLETED")

print("\nMonthly Portfolio Weights:")
print(weights_df.round(4).to_string(index=False))

print("\nTesting Period:")
print(rolling_comparison.index.min(), "to",
      rolling_comparison.index.max())

print("\nTesting Observations:")
print(len(rolling_comparison))

print("\nReturns saved successfully.")
print("Monthly weights saved successfully.")
