# Methodology: Financial Market Risk & Portfolio Analysis

## 1. Introduction

This document describes the methodology used to analyse historical financial data, construct investment portfolios, and evaluate portfolio risk and performance.

The analysis uses five individual equities and the SPDR S&P 500 ETF (SPY) as a benchmark.

The main objective is to compare equal-weight and minimum-variance portfolio strategies using historical data and an out-of-sample testing framework.

## 2. Data Collection and Preparation

### 2.1 Data Source

Historical adjusted stock price data were obtained from Yahoo Finance using the Python `yfinance` library.

The assets analysed were:

- AAPL – Apple Inc.
- AMZN – Amazon.com Inc.
- JPM – JPMorgan Chase & Co.
- MSFT – Microsoft Corporation
- XOM – Exxon Mobil Corporation
- SPY – SPDR S&P 500 ETF Trust

SPY was used as the market benchmark rather than as a constituent of the five-stock portfolios.

### 2.2 Data Period

The historical dataset covers:

8 November 2021 – 6 November 2026.

The dataset was divided into:

- Training period: 2021–2024
- Testing period: 2 January 2025 – 6 November 2026

The training period was used for estimating portfolio parameters. The testing period was used to evaluate portfolio performance on data not used in the initial estimation.

### 2.3 Daily Returns

Daily simple returns were calculated from adjusted closing prices.

The formula is:

\[
R_t = \frac{P_t-P_{t-1}}{P_{t-1}}
\]

Where:

- \(R_t\) = return on day \(t\)
- \(P_t\) = adjusted closing price on day \(t\)
- \(P_{t-1}\) = adjusted closing price on the previous trading day

Daily returns measure the percentage change in an asset's adjusted price between consecutive trading days.

## 3. Historical Risk and Return Analysis

### 3.1 Average Daily Return

The arithmetic average daily return is:

\[
\bar{R}=\frac{1}{n}\sum_{t=1}^{n}R_t
\]

Where \(n\) represents the number of daily observations.

### 3.2 Annualised Return

Annualised arithmetic return was estimated using 252 trading days per year:

\[
R_{\text{annual}}=\bar{R}\times252
\]

This provides an annualised estimate based on the average daily return.

### 3.3 Volatility

Volatility measures the degree to which returns fluctuate around their average.

Daily volatility is calculated using the sample standard deviation of daily returns.

Annualised volatility is:

\[
\sigma_{\text{annual}}=\sigma_{\text{daily}}\sqrt{252}
\]

A higher volatility indicates greater variability in historical returns.

### 3.4 Correlation Analysis

Correlation measures the strength and direction of the linear relationship between two assets.

The correlation coefficient ranges from -1 to +1.

- +1: Perfect positive correlation.
- 0: No linear correlation.
- -1: Perfect negative correlation.

The correlation matrix was used to examine relationships between the selected equities and the benchmark.

Correlation is important in portfolio construction because combining assets with imperfectly correlated returns can reduce portfolio risk.

## 4. Portfolio Construction

Three portfolio strategies were evaluated.

### 4.1 Equal-Weight Portfolio

The equal-weight portfolio allocates the same proportion of capital to each of the five selected equities.

Each asset receives a weight of:

\[
w_i=\frac{1}{5}=0.20
\]

Therefore, each stock receives a 20% allocation.

Portfolio daily return is:

\[
R_{p,t}=\sum_{i=1}^{5}w_iR_{i,t}
\]

Where:

- \(R_{p,t}\) = portfolio return
- \(w_i\) = weight of asset \(i\)
- \(R_{i,t}\) = return of asset \(i\)

### 4.2 Minimum-Variance Portfolio

The minimum-variance portfolio aims to find asset weights that minimise portfolio variance.

Portfolio variance is:

\[
\sigma_p^2=w^T\Sigma w
\]

Where:

- \(w\) = vector of portfolio weights
- \(\Sigma\) = covariance matrix of asset returns
- \(\sigma_p^2\) = portfolio variance

The optimisation problem is:

\[
\min_w w^T\Sigma w
\]

Subject to:

\[
\sum_{i=1}^{5}w_i=1
\]

\[
w_i\geq0
\]

The constraints require the portfolio weights to sum to 100% and prohibit short selling.

The optimisation uses historical return data to estimate the covariance matrix and determine the portfolio weights.

### 4.3 Fixed Minimum-Variance Portfolio

The fixed minimum-variance portfolio uses weights estimated from the training period (2021–2024).

The estimated target weights are:

| Asset | Weight |
|---|---:|
| AAPL | 14.54% |
| AMZN | 0.00% |
| JPM | 30.04% |
| MSFT | 23.39% |
| XOM | 32.02% |

These target weights are maintained through monthly rebalancing during the out-of-sample testing period.

The weights are not re-optimised using testing-period returns.

### 4.4 Rolling Minimum-Variance Portfolio

The rolling minimum-variance strategy re-estimates portfolio weights using a rolling historical estimation window.

For each monthly rebalancing date, the strategy uses the preceding 252 available trading days to estimate the covariance matrix and calculate new minimum-variance weights.

This allows the portfolio allocation to adapt to changes in historical asset relationships and volatility.

Unlike the fixed strategy, the rolling strategy can change its target weights from month to month.

## 5. Monthly Rebalancing

The final out-of-sample comparison uses monthly rebalancing.

At the beginning of each month, portfolio holdings are adjusted to the strategy's target weights.

Between rebalancing dates, the portfolio weights are allowed to drift as asset prices change.

This means that the portfolio is not continuously restored to its target allocation every trading day.

Monthly rebalancing provides a more realistic framework than assuming that target weights are maintained without considering the frequency of portfolio adjustments.

## 6. Portfolio Performance Evaluation

The portfolios were evaluated using five performance measures.

### 6.1 Annualised Return

Annualised arithmetic return estimates average yearly performance:

\[
R_{\text{annual}}=\bar{R}\times252
\]

### 6.2 Annualised Volatility

Annualised volatility measures the variability of daily portfolio returns:

\[
\sigma_{\text{annual}}=\sigma_{\text{daily}}\sqrt{252}
\]

### 6.3 Sharpe Ratio

The Sharpe ratio measures excess return relative to portfolio volatility.

It was calculated using a zero risk-free rate assumption:

\[
S=\frac{R_{\text{annual}}-R_f}{\sigma_{\text{annual}}}
\]

Where:

- \(R_{\text{annual}}\) = annualised arithmetic return
- \(R_f\) = risk-free rate, assumed to be zero
- \(\sigma_{\text{annual}}\) = annualised volatility

A higher Sharpe ratio indicates greater return per unit of measured volatility under the stated assumptions.

### 6.4 Maximum Drawdown

Maximum drawdown measures the largest observed decline from a previous portfolio wealth peak.

First, cumulative wealth is calculated:

\[
W_t=W_{t-1}(1+R_{p,t})
\]

The running maximum wealth is:

\[
H_t=\max(W_1,W_2,\ldots,W_t)
\]

Drawdown is:

\[
D_t=\frac{W_t}{H_t}-1
\]

Maximum drawdown is the minimum value of the drawdown series.

A more negative maximum drawdown represents a larger historical peak-to-trough loss.

### 6.5 Compound Annual Growth Rate (CAGR)

CAGR measures the annualised growth rate of an investment over the testing period.

\[
CAGR=\left(\frac{W_T}{W_0}\right)^{1/Y}-1
\]

Where:

- \(W_T\) = ending portfolio wealth
- \(W_0\) = initial portfolio wealth
- \(Y\) = elapsed time in years

CAGR summarises the compound growth achieved over the investment period.

## 7. Transaction Cost Analysis

Transaction costs were examined to understand how portfolio rebalancing costs could affect performance.

The analysis considered cost assumptions of:

- 0 basis points
- 5 basis points
- 10 basis points
- 25 basis points

Portfolio turnover was also examined to compare the amount of trading required by each strategy.

The analysis uses a simplified transaction cost model. It does not fully account for brokerage charges, taxes, bid-ask spreads, or market impact.

The rolling minimum-variance strategy was also examined for its higher turnover relative to the other strategies.

## 8. Estimation-Window Sensitivity Analysis

The rolling minimum-variance strategy was evaluated using different historical estimation windows:

- 6 months
- 1 year
- 2 years
- 3 years

The purpose was to examine how the choice of historical estimation period affects portfolio weights and subsequent performance.

Shorter estimation windows respond more quickly to recent market conditions but may produce less stable estimates.

Longer estimation windows use more historical observations but may be slower to reflect recent changes.

## 9. Market Condition Analysis

Market conditions were classified using SPY's daily return.

The classification was:

- Positive Market: SPY daily return greater than or equal to zero.
- Negative Market: SPY daily return below zero.

Average daily portfolio returns were then compared across the two groups.

This analysis examines how the strategies behaved on positive and negative benchmark-return days.

These categories represent daily market conditions, not formal bull-market or bear-market regimes.

## 10. Limitations and Assumptions

The analysis has several limitations:

1. Only five individual equities were selected for portfolio construction.
2. The results are based on one out-of-sample testing period.
3. A zero risk-free rate was assumed for the Sharpe ratio.
4. Transaction costs were represented using simplified basis-point assumptions.
5. Taxes, brokerage charges, bid-ask spreads, and market impact were not fully modelled.
6. Historical covariance estimates may not accurately represent future relationships between assets.
7. The selected assets and testing period may introduce selection and period-specific biases.
8. Historical performance does not guarantee future investment results.

## 11. Conclusion

This project demonstrates how historical financial data can be used to analyse asset risk, examine diversification, construct portfolios, and evaluate investment performance.

The comparison of equal-weight, fixed minimum-variance, and rolling minimum-variance strategies provides insight into the relationship between portfolio construction, risk, return, rebalancing, and estimation choices.

The findings are specific to the selected assets, assumptions, and historical testing period. They should not be interpreted as predictions of future market performance.

