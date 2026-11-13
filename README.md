# Financial Market Risk & Portfolio Analysis

## 1. Project Overview

This project investigates the relationship between investment returns and financial risk using historical stock market data.

It examines the performance and risk characteristics of selected equities, evaluates portfolio diversification, and compares different portfolio construction strategies against the S&P 500 ETF (SPY).

The project also applies out-of-sample testing, transaction cost analysis, estimation-window sensitivity analysis, and market condition analysis to evaluate portfolio performance under different assumptions.

## 2. Research Objectives

The main objectives are to:

- Analyse historical stock price movements and daily returns.
- Calculate cumulative investment returns.
- Measure and compare asset volatility.
- Examine correlations between financial assets.
- Evaluate the benefits of portfolio diversification.
- Construct and compare equal-weight and minimum-variance portfolios.
- Assess portfolio performance using risk-adjusted performance metrics.
- Conduct out-of-sample portfolio testing.
- Examine the effects of transaction costs and estimation-window choices.
- Compare portfolio behaviour during positive and negative market days.

## 3. Dataset

Historical adjusted price data were obtained using Yahoo Finance through the `yfinance` Python library.

### Assets analysed

| Ticker | Company / Instrument |
|---|---|
| AAPL | Apple Inc. |
| AMZN | Amazon.com Inc. |
| JPM | JPMorgan Chase & Co. |
| MSFT | Microsoft Corporation |
| XOM | Exxon Mobil Corporation |
| SPY | SPDR S&P 500 ETF Trust (benchmark) |

### Dataset coverage

- Historical period: 8 November 2021 – 6 November 2026
- Number of daily price observations: 1,255
- Number of daily return observations: 1,254
- Training period: 2021–2024
- Out-of-sample testing period: 2 January 2025 – 6 November 2026
- Out-of-sample observations: 464
- Annualisation convention: 252 trading days

The five selected equities were used to construct the portfolios, while SPY served as the market benchmark.

## 4. Tools and Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- yfinance
- JupyterLab
- Git and GitHub

## 5. Methodology

The analysis was conducted in several stages.

### 5.1 Exploratory Financial Analysis

- Historical price analysis
- Daily return calculations