
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Load monthly portfolio weights
weights = pd.read_csv(
    "data/processed/monthly_rebalanced_weights.csv",
    index_col=0
)

# Convert month labels into dates
weights.index = pd.to_datetime(weights.index)

# Create stacked area chart
plt.figure(figsize=(13, 7))

plt.stackplot(
    weights.index,
    *[weights[column] for column in weights.columns],
    labels=weights.columns,
    alpha=0.85
)

plt.title(
    "Rolling Minimum-Variance Portfolio: Monthly Asset Allocation",
    fontsize=14
)

plt.xlabel("Month")
plt.ylabel("Portfolio Weight")

plt.gca().yaxis.set_major_formatter(
    mtick.PercentFormatter(1.0)
)

plt.ylim(0, 1)
plt.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.12),
    ncol=5
)

plt.grid(axis="y", alpha=0.25)
plt.tight_layout()

plt.savefig(
    "reports/figures/rolling_portfolio_allocation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Portfolio allocation chart saved successfully.")
