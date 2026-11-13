import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load performance summary
performance = pd.read_csv(
    "data/processed/performance_summary.csv",
    index_col=0
)

# Select annualized return and volatility
risk_return = performance[
    ["Annualized Return", "Annualized Volatility"]
].copy()

# Create scatter plot
plt.figure(figsize=(11, 7))

plt.scatter(
    risk_return["Annualized Volatility"] * 100,
    risk_return["Annualized Return"] * 100,
    s=100
)

# Label each point
for asset, row in risk_return.iterrows():
    plt.annotate(
        asset,
        (
            row["Annualized Volatility"] * 100,
            row["Annualized Return"] * 100
        ),
        xytext=(6, 6),
        textcoords="offset points"
    )

plt.title("Risk–Return Relationship")
plt.xlabel("Annualized Volatility (%)")
plt.ylabel("Annualized Return (%)")
plt.grid(alpha=0.3)
plt.tight_layout()

# Save chart
figure_path = Path(
    "reports/figures/risk_return_scatter.png"
)

plt.savefig(figure_path, dpi=300)
plt.show()

print("Risk–return analysis completed!")
print(f"\nChart saved to: {figure_path}")

print("\nRisk–Return Data:")
print((risk_return * 100).round(2))