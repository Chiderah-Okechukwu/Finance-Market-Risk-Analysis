
import pandas as pd
import numpy as np
from pathlib import Path

# Load daily stock returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# Calculate average daily returns
mean_daily_return = returns.mean()

# Calculate daily volatility (sample standard deviation)
daily_volatility = returns.std()

# Annualise volatility using 252 trading days
annualized_volatility = daily_volatility * np.sqrt(252)

# Organise the results
volatility_summary = pd.DataFrame({
    "Mean Daily Return": mean_daily_return,
    "Daily Volatility": daily_volatility,
    "Annualized Volatility": annualized_volatility
})

# Sort from highest to lowest annualised volatility
volatility_summary = volatility_summary.sort_values(
    by="Annualized Volatility",
    ascending=False
)

# Save results
output_path = Path("data/processed/volatility_summary.csv")
volatility_summary.to_csv(output_path)

print("Volatility analysis completed!")

print("\nVolatility Summary:")
print(volatility_summary)

print(f"\nSaved to: {output_path}")
