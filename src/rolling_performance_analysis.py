
import pandas as pd
import numpy as np

# Load rolling-window returns
returns = pd.read_csv(
    "data/processed/rolling_window_returns.csv",
    index_col=0,
    parse_dates=True
)

results = []

risk_free_rate = 0.0

for name in returns.columns:

    daily_returns = returns[name].dropna()

    # Annualised performance
    annual_return = daily_returns.mean() * 252

    annual_volatility = (
        daily_returns.std() * np.sqrt(252)
    )

    sharpe_ratio = (
        (daily_returns.mean() - risk_free_rate / 252)
        / daily_returns.std()
    ) * np.sqrt(252)

    # Cumulative wealth
    wealth = (1 + daily_returns).cumprod()

    # Maximum drawdown
    running_peak = wealth.cummax()
    drawdown = wealth / running_peak - 1

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
comparison = pd.DataFrame(results).set_index("Portfolio")

# Save results
comparison.to_csv(
    "data/processed/rolling_performance_comparison.csv"
)

print("\nROLLING-WINDOW PERFORMANCE COMPARISON")
print(comparison.round(4))

print("\nResults saved successfully.")
