
import pandas as pd
import matplotlib.pyplot as plt

# Load out-of-sample returns
returns = pd.read_csv(
    "data/processed/out_of_sample_returns.csv",
    index_col=0,
    parse_dates=True
)

# Calculate cumulative wealth
wealth = (1 + returns).cumprod()

# Plot cumulative wealth
plt.figure(figsize=(12, 6))

for column in wealth.columns:
    plt.plot(
        wealth.index,
        wealth[column],
        label=column
    )

plt.title("Out-of-Sample Portfolio Wealth Growth")
plt.xlabel("Date")
plt.ylabel("Growth of $1 Investment")

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

# Save chart
plt.savefig(
    "reports/figures/out_of_sample_wealth.png",
    dpi=300
)

plt.show()

print("Out-of-sample wealth chart saved successfully.")
