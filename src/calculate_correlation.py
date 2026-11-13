
import pandas as pd
from pathlib import Path

# Load daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# Calculate correlation matrix
correlation_matrix = returns.corr()

# Save correlation matrix
output_path = Path("data/processed/correlation_matrix.csv")
correlation_matrix.to_csv(output_path)

print("Correlation analysis completed!")

print("\nCorrelation Matrix:")
print(correlation_matrix.round(3))

print(f"\nSaved to: {output_path}")
