import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# Define portfolio
assets = ["AAPL", "AMZN", "JPM", "MSFT", "XOM"]
weights = np.array([0.20] * 5)

portfolio_returns = (
    returns[assets] * weights
).sum(axis=1)

# Include benchmark and portfolio
all_returns = returns[assets + ["SPY"]].copy()
all_returns["PORTFOLIO"] = portfolio_returns

# Calculate cumulative wealth
cumulative_wealth = (1 + all_returns).cumprod()

# Calculate running historical peaks
running_peaks = cumulative_wealth.cummax()

# Calculate drawdowns
drawdowns = (
    cumulative_wealth / running_peaks
) - 1

# Save drawdown data
output_path = Path("data/processed/drawdowns.csv")
drawdowns.to_csv(output_path)

# Plot drawdowns
plt.figure(figsize=(14, 7))

for column in drawdowns.columns:
    plt.plot(
        drawdowns.index,
        drawdowns[column],
        label=column
    )

plt.title("Historical Portfolio and Asset Drawdowns")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

# Save chart
figure_path = Path("reports/figures/drawdown_chart.png")
plt.savefig(figure_path, dpi=300)
plt.show()

# Display maximum drawdowns
print("Drawdown analysis completed!")

print("\nMaximum Drawdown by Asset:")
print(drawdowns.min().sort_values().round(4))

print(f"\nData saved to: {output_path}")
print(f"Chart saved to: {figure_path}")