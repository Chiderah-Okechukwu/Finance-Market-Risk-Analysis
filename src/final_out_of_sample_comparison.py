
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load fixed-weight out-of-sample returns
fixed_returns = pd.read_csv(
    "data/processed/out_of_sample_returns.csv",
    index_col=0,
    parse_dates=True
)

# Load rolling-window returns
rolling_returns = pd.read_csv(
    "data/processed/rolling_window_returns.csv",
    index_col=0,
    parse_dates=True
)

# Combine the four strategies
comparison_returns = pd.DataFrame({
    "Equal-Weight": fixed_returns["Equal-Weight"],
    "Fixed Minimum-Variance": fixed_returns["Minimum-Variance"],
    "Rolling Minimum-Variance": rolling_returns[
        "Rolling Minimum-Variance"
    ],
    "SPY": fixed_returns["SPY"]
})

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

# Performance summary
summary = pd.DataFrame(results).set_index("Portfolio")

summary.to_csv(
    "data/processed/final_out_of_sample_comparison.csv"
)

print("\nFINAL OUT-OF-SAMPLE PERFORMANCE")
print(summary.round(4))

# Calculate cumulative wealth
wealth = (1 + comparison_returns).cumprod()

wealth.to_csv(
    "data/processed/final_out_of_sample_wealth.csv"
)

# Plot wealth growth
plt.figure(figsize=(12, 6))

for column in wealth.columns:
    plt.plot(
        wealth.index,
        wealth[column],
        label=column
    )

plt.title("Out-of-Sample Comparison: Four Investment Strategies")
plt.xlabel("Date")
plt.ylabel("Growth of $1 Investment")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "reports/figures/final_out_of_sample_comparison.png",
    dpi=300
)

plt.show()

print("\nFinal comparison table and chart saved successfully.")
