import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# Portfolio assets and equal weights
assets = ["AAPL", "AMZN", "JPM", "MSFT", "XOM"]
weights = [0.20] * 5

# Calculate daily portfolio returns
portfolio_returns = (
    returns[assets] * weights
).sum(axis=1)

# Add portfolio to the return dataset
wealth_returns = returns[assets].copy()
wealth_returns["PORTFOLIO"] = portfolio_returns

# Calculate cumulative wealth
cumulative_wealth = (1 + wealth_returns).cumprod()

# Save cumulative wealth data
output_path = Path("data/processed/cumulative_wealth.csv")
cumulative_wealth.to_csv(output_path)

# Create the chart
plt.figure(figsize=(12, 6))

for column in cumulative_wealth.columns:
    plt.plot(
        cumulative_wealth.index,
        cumulative_wealth[column],
        label=column
    )

plt.title("Growth of $1 Invested")
plt.xlabel("Date")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

# Save chart
figure_path = Path("reports/figures/cumulative_wealth.png")
plt.savefig(figure_path, dpi=300)
plt.show()

print("Cumulative wealth analysis completed!")
print(f"\nData saved to: {output_path}")
print(f"Chart saved to: {figure_path}")

print("\nFinal value of $1 investment:")
print(cumulative_wealth.iloc[-1].round(4))