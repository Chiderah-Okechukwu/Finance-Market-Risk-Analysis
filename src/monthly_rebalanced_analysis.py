
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Load daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

assets = ["AAPL", "AMZN", "JPM", "MSFT", "XOM"]

asset_returns = returns[assets].dropna()

# Define training and testing periods
training_data = asset_returns.loc[
    "2021-11-09":"2024-12-31"
]

testing_data = asset_returns.loc[
    "2025-01-01":"2026-11-06"
]

# Portfolio optimisation function
def optimise_portfolio(data):

    covariance_matrix = data.cov() * 252

    def portfolio_variance(weights):
        return weights.T @ covariance_matrix.values @ weights

    constraints = [
        {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
    ]

    bounds = [(0, 1)] * len(assets)

    initial_weights = np.array([0.20] * len(assets))

    result = minimize(
        portfolio_variance,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        raise RuntimeError(result.message)

    return result.x


# Estimate fixed weights using training data only
fixed_weights = optimise_portfolio(training_data)

print("Fixed Minimum-Variance Weights:")

for asset, weight in zip(assets, fixed_weights):
    print(f"{asset}: {weight:.2%}")


# Calculate returns with monthly rebalancing
def monthly_rebalanced_returns(month_data, target_weights):

    current_weights = np.array(target_weights, dtype=float)

    daily_results = []

    for date, daily_returns in month_data.iterrows():

        daily_values = daily_returns.to_numpy()

        portfolio_return = np.dot(
            current_weights,
            daily_values
        )

        daily_results.append(portfolio_return)

        # Allow weights to drift after daily market movements
        current_weights = (
            current_weights * (1 + daily_values)
            / (1 + portfolio_return)
        )

    return pd.Series(
        daily_results,
        index=month_data.index
    )


# Store results
equal_weight_results = []
fixed_results = []
rolling_results = []
weight_history = []

# Process each testing month
for month, month_data in testing_data.groupby(
    testing_data.index.to_period("M")
):

    # Equal-weight portfolio: rebalance monthly
    equal_weight_results.append(
        monthly_rebalanced_returns(
            month_data,
            np.array([0.20] * len(assets))
        )
    )

    # Fixed Minimum-Variance: rebalance monthly
    fixed_results.append(
        monthly_rebalanced_returns(
            month_data,
            fixed_weights
        )
    )

    # Rolling optimisation: use previous 252 trading days
    rolling_training = asset_returns.loc[
        asset_returns.index < month_data.index[0]
    ].tail(252)

    if len(rolling_training) < 252:
        raise ValueError("Insufficient rolling training data.")

    rolling_weights = optimise_portfolio(rolling_training)

    rolling_results.append(
        monthly_rebalanced_returns(
            month_data,
            rolling_weights
        )
    )

    record = {"Month": str(month)}

    for asset, weight in zip(assets, rolling_weights):
        record[asset] = weight

    weight_history.append(record)


# Combine portfolio returns
comparison_returns = pd.DataFrame({
    "Equal-Weight": pd.concat(equal_weight_results),
    "Fixed Minimum-Variance": pd.concat(fixed_results),
    "Rolling Minimum-Variance": pd.concat(rolling_results),
    "SPY": returns.loc[testing_data.index, "SPY"]
})

# Save returns and weights
comparison_returns.to_csv(
    "data/processed/monthly_rebalanced_returns.csv"
)

pd.DataFrame(weight_history).to_csv(
    "data/processed/monthly_rebalanced_weights.csv",
    index=False
)


# Calculate performance
results = []

for name in comparison_returns.columns:

    daily_returns = comparison_returns[name].dropna()

    annual_return = daily_returns.mean() * 252

    annual_volatility = daily_returns.std() * np.sqrt(252)

    sharpe_ratio = (
        daily_returns.mean() / daily_returns.std()
    ) * np.sqrt(252)

    wealth = (1 + daily_returns).cumprod()

    drawdown = wealth / wealth.cummax() - 1

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


summary = pd.DataFrame(results).set_index("Portfolio")

summary.to_csv(
    "data/processed/monthly_rebalanced_comparison.csv"
)

print("\nMONTHLY REBALANCED PERFORMANCE COMPARISON")
print(summary.round(4))


# Plot cumulative wealth
wealth = (1 + comparison_returns).cumprod()

plt.figure(figsize=(12, 6))

for column in wealth.columns:
    plt.plot(
        wealth.index,
        wealth[column],
        label=column
    )

plt.title("Out-of-Sample Performance: Monthly Rebalancing")
plt.xlabel("Date")
plt.ylabel("Growth of $1 Investment")

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "reports/figures/monthly_rebalanced_comparison.png",
    dpi=300
)

plt.show()

print("\nMonthly rebalanced analysis completed successfully.")
