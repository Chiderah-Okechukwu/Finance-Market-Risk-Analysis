
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

asset_returns = returns[assets].dropna()

training_data = asset_returns.loc[
    "2021-11-09":"2024-12-31"
]

testing_data = asset_returns.loc[
    "2025-01-01":"2026-11-06"
]

monthly_groups = list(
    testing_data.groupby(testing_data.index.to_period("M"))
)

# Optimisation function
def optimise_portfolio(data):

    covariance_matrix = data.cov() * 252

    def objective(weights):
        return weights.T @ covariance_matrix.values @ weights

    constraints = [
        {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
    ]

    bounds = [(0, 1)] * len(assets)

    result = minimize(
        objective,
        np.array([0.20] * len(assets)),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        raise RuntimeError(result.message)

    return result.x


# Fixed portfolio weights
fixed_weights = optimise_portfolio(training_data)

# Generate monthly target weights
monthly_targets = {
    "Equal-Weight": [],
    "Fixed Minimum-Variance": [],
    "Rolling Minimum-Variance": []
}

for month, month_data in monthly_groups:

    monthly_targets["Equal-Weight"].append(
        np.array([0.20] * len(assets))
    )

    monthly_targets["Fixed Minimum-Variance"].append(
        fixed_weights
    )

    rolling_training = asset_returns.loc[
        asset_returns.index < month_data.index[0]
    ].tail(252)

    rolling_weights = optimise_portfolio(rolling_training)

    monthly_targets["Rolling Minimum-Variance"].append(
        rolling_weights
    )


# Simulate monthly rebalancing and transaction costs
def simulate_strategy(strategy, cost_bps):

    previous_weights = None
    daily_results = []
    turnover_records = []

    for month_index, (month, month_data) in enumerate(monthly_groups):

        target_weights = monthly_targets[strategy][month_index]

        # Calculate one-way turnover
        if previous_weights is None:
            turnover = 0.0
        else:
            turnover = (
                0.5 * np.abs(target_weights - previous_weights).sum()
            )

        # Transaction cost based on one-way turnover
        transaction_cost = turnover * cost_bps / 10000

        current_weights = target_weights.copy()

        for day_index, (date, daily_returns) in enumerate(
            month_data.iterrows()
        ):

            asset_daily_returns = daily_returns.to_numpy()

            gross_return = np.dot(
                current_weights,
                asset_daily_returns
            )

            net_return = gross_return

            # Apply monthly transaction cost on the first trading day
            if day_index == 0:
                net_return = (
                    (1 + gross_return) *
                    (1 - transaction_cost)
                ) - 1

            daily_results.append({
                "Date": date,
                "Return": net_return
            })

            # Allow weights to drift naturally
            current_weights = (
                current_weights * (1 + asset_daily_returns)
                / (1 + gross_return)
            )

        previous_weights = current_weights

        turnover_records.append({
            "Month": str(month),
            "One-Way Turnover": turnover,
            "Transaction Cost": transaction_cost
        })

    strategy_returns = pd.DataFrame(
        daily_results
    ).set_index("Date")["Return"]

    turnover_df = pd.DataFrame(turnover_records)

    return strategy_returns, turnover_df


# Calculate performance
def calculate_performance(daily_returns):

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

    return {
        "Annualized Return": annual_return,
        "Annualized Volatility": annual_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Maximum Drawdown": maximum_drawdown,
        "CAGR": cagr
    }


# Test different transaction-cost assumptions
cost_scenarios = [0, 5, 10, 25]

all_results = []
turnover_summary = []

for cost_bps in cost_scenarios:

    print(f"\nTesting transaction cost: {cost_bps} bps")

    for strategy in monthly_targets:

        strategy_returns, turnover_df = simulate_strategy(
            strategy,
            cost_bps
        )

        performance = calculate_performance(strategy_returns)

        all_results.append({
            "Transaction Cost (bps)": cost_bps,
            "Portfolio": strategy,
            **performance
        })

        if cost_bps == 10:

            turnover_summary.append({
                "Portfolio": strategy,
                "Average Monthly Turnover":
                    turnover_df["One-Way Turnover"].mean(),
                "Total One-Way Turnover":
                    turnover_df["One-Way Turnover"].sum()
            })

    # SPY is held without monthly rebalancing
    spy_returns = returns.loc[testing_data.index, "SPY"]

    spy_performance = calculate_performance(spy_returns)

    all_results.append({
        "Transaction Cost (bps)": cost_bps,
        "Portfolio": "SPY",
        **spy_performance
    })


# Save performance results
results_df = pd.DataFrame(all_results)

results_df.to_csv(
    "data/processed/transaction_cost_comparison.csv",
    index=False
)

# Save turnover results
turnover_df = pd.DataFrame(turnover_summary)

turnover_df.to_csv(
    "data/processed/portfolio_turnover_summary.csv",
    index=False
)

print("\nTRANSACTION COST PERFORMANCE COMPARISON")
print(results_df.round(4).to_string(index=False))

print("\nPORTFOLIO TURNOVER SUMMARY")
print(turnover_df.round(4).to_string(index=False))

print("\nTransaction cost analysis completed successfully.")
