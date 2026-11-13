
import pandas as pd
import numpy as np

# Load daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# Load monthly rebalanced portfolio returns
portfolio_returns = pd.read_csv(
    "data/processed/monthly_rebalanced_returns.csv",
    index_col=0,
    parse_dates=True
)

# Combine the portfolio returns with SPY
analysis = pd.DataFrame({
    "Equal-Weight": portfolio_returns["Equal-Weight"],
    "Fixed Minimum-Variance":
        portfolio_returns["Fixed Minimum-Variance"],
    "Rolling Minimum-Variance":
        portfolio_returns["Rolling Minimum-Variance"],
    "SPY": returns.loc[
        portfolio_returns.index, "SPY"
    ]
})

# Classify market conditions using SPY
analysis["Market Condition"] = np.where(
    analysis["SPY"] >= 0,
    "Positive Market",
    "Negative Market"
)

# Calculate average daily returns by market condition
average_returns = analysis.groupby(
    "Market Condition"
)[[
    "Equal-Weight",
    "Fixed Minimum-Variance",
    "Rolling Minimum-Variance",
    "SPY"
]].mean()

# Convert daily averages to percentages
average_returns = average_returns * 100

# Calculate observation counts
observation_counts = analysis[
    "Market Condition"
].value_counts()

# Save results
average_returns.to_csv(
    "data/processed/market_condition_returns.csv"
)

observation_counts.to_csv(
    "data/processed/market_condition_counts.csv"
)

print("\nAVERAGE DAILY RETURNS BY MARKET CONDITION")
print(average_returns.round(4))

print("\nNUMBER OF TRADING DAYS")
print(observation_counts)

print("\nMarket condition analysis completed successfully.")
