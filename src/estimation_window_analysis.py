
import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Load historical daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

assets = ["AAPL", "AMZN", "JPM", "MSFT", "XOM"]

asset_returns = returns[assets].dropna()

testing_data = asset_returns.loc[
    "2025-01-01":"2026-11-06"
]

# Estimation windows to investigate
windows = {
    "6 Months": 126,
    "1 Year": 252,
    "2 Years": 504,
    "3 Years": 756
}


# Function to calculate optimal portfolio weights
def optimise_portfolio(training_data):

    covariance_matrix = training_data.cov() * 252

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


# Function to simulate monthly rebalancing
def calculate_monthly_returns(month_data, target_weights):

    current_weights = target_weights.copy()
    daily_results = []

    for date, daily_returns in month_data.iterrows():

        asset_returns_today = daily_returns.to_numpy()

        portfolio_return = np.dot(
            current_weights,
            asset_returns_today
        )

        daily_results.append(portfolio_return)

        # Allow portfolio weights to change with market movements
        current_weights = (
            current_weights * (1 + asset_returns_today)
            / (1 + portfolio_return)
        )

    return pd.Series(
        daily_results,
        index=month_data.index
    )


# Calculate performance statistics
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


# Divide testing data into months
monthly_groups = list(
    testing_data.groupby(
        testing_data.index.to_period("M")
    )
)

results = []

# Test each historical estimation window
for window_name, window_size in windows.items():

    print(f"\nTesting estimation window: {window_name}")

    monthly_results = []

    for month, month_data in monthly_groups:

        # Use only historical data available before this month
        training_data = asset_returns.loc[
            asset_returns.index < month_data.index[0]
        ].tail(window_size)

        if len(training_data) < window_size:
            raise ValueError(
                f"Insufficient training data for {window_name}"
            )

        # Calculate portfolio weights
        weights = optimise_portfolio(training_data)

        # Calculate that month's portfolio returns
        monthly_returns = calculate_monthly_returns(
            month_data,
            weights
        )

        monthly_results.append(monthly_returns)

    # Combine all testing-month returns
    strategy_returns = pd.concat(monthly_results)

    performance = calculate_performance(strategy_returns)

    results.append({
        "Estimation Window": window_name,
        **performance
    })


# Create comparison table
comparison = pd.DataFrame(results).set_index(
    "Estimation Window"
)

# Save results
comparison.to_csv(
    "data/processed/estimation_window_comparison.csv"
)

print("\nESTIMATION WINDOW SENSITIVITY RESULTS")
print(comparison.round(4))

print("\nResults saved successfully.")
