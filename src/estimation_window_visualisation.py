
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Load estimation-window results
results = pd.read_csv(
    "data/processed/estimation_window_comparison.csv"
)

windows = results["Estimation Window"]

# Create three-panel figure
fig, axes = plt.subplots(
    3, 1,
    figsize=(11, 12)
)

# Panel 1: Return and CAGR
axes[0].plot(
    windows,
    results["Annualized Return"] * 100,
    marker="o",
    label="Annualised Return"
)

axes[0].plot(
    windows,
    results["CAGR"] * 100,
    marker="s",
    label="CAGR"
)

axes[0].set_title("Return Performance")
axes[0].set_ylabel("Return (%)")
axes[0].legend()
axes[0].grid(alpha=0.3)

# Panel 2: Volatility and Sharpe ratio
axes[1].plot(
    windows,
    results["Annualized Volatility"] * 100,
    marker="o",
    label="Annualised Volatility"
)

axes[1].plot(
    windows,
    results["Sharpe Ratio"],
    marker="s",
    label="Sharpe Ratio"
)

axes[1].set_title("Risk and Risk-Adjusted Performance")
axes[1].set_ylabel("Value")
axes[1].legend()
axes[1].grid(alpha=0.3)

# Panel 3: Maximum drawdown
axes[2].bar(
    windows,
    results["Maximum Drawdown"] * 100
)

axes[2].set_title("Maximum Drawdown")
axes[2].set_ylabel("Drawdown (%)")
axes[2].grid(axis="y", alpha=0.3)

fig.suptitle(
    "Sensitivity to Portfolio Estimation Window",
    fontsize=15,
    y=0.99
)

plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.savefig(
    "reports/figures/estimation_window_sensitivity.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Estimation-window sensitivity chart saved successfully.")
