
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / "reports" / "figures"
OUTPUT = ROOT / "reports" / "Financial_Market_Risk_and_Portfolio_Analysis.pdf"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# DOCUMENT SETUP
# --------------------------------------------------

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=48,
    leftMargin=48,
    topMargin=55,
    bottomMargin=50
)

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="CoverTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=23,
    leading=30,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#17365D"),
    spaceAfter=18
))

styles.add(ParagraphStyle(
    name="Subtitle",
    parent=styles["Normal"],
    fontSize=12,
    leading=18,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#555555"),
    spaceAfter=12
))

styles.add(ParagraphStyle(
    name="Section",
    parent=styles["Heading1"],
    fontSize=16,
    leading=21,
    textColor=colors.HexColor("#17365D"),
    spaceBefore=16,
    spaceAfter=9
))

styles.add(ParagraphStyle(
    name="Subsection",
    parent=styles["Heading2"],
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#365F91"),
    spaceBefore=10,
    spaceAfter=6
))

styles.add(ParagraphStyle(
    name="BodyCustom",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=15,
    alignment=TA_LEFT,
    spaceAfter=8
))

styles.add(ParagraphStyle(
    name="SmallNote",
    parent=styles["BodyText"],
    fontSize=8,
    leading=11,
    textColor=colors.HexColor("#555555"),
    spaceAfter=6
))

story = []

def add_paragraph(text, style="BodyCustom"):
    story.append(Paragraph(text, styles[style]))

def add_heading(text):
    story.append(Paragraph(text, styles["Section"]))

def add_subheading(text):
    story.append(Paragraph(text, styles["Subsection"]))

def add_table(headers, rows, widths=None):
    data = [[Paragraph(str(x), styles["SmallNote"]) for x in headers]]

    for row in rows:
        data.append([
            Paragraph(str(x), styles["SmallNote"]) for x in row
        ])

    table = Table(data, colWidths=widths, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CCCCCC")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F5F7FA")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(table)
    story.append(Spacer(1, 10))

def add_figure(filename, caption, width=6.2*inch):
    path = FIGURES / filename

    if not path.exists():
        add_paragraph(
            f"<i>Figure not inserted: {filename} was not found.</i>",
            "SmallNote"
        )
        return

    img = Image(str(path))
    ratio = img.imageHeight / img.imageWidth
    img.drawWidth = width
    img.drawHeight = width * ratio

    story.append(img)
    story.append(Spacer(1, 4))
    add_paragraph(caption, "SmallNote")
    story.append(Spacer(1, 12))

def footer(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(48, 28, "Financial Market Risk & Portfolio Analysis")
    canvas.drawRightString(
        A4[0] - 48, 28, f"Page {document.page}"
    )
    canvas.restoreState()

# --------------------------------------------------
# COVER PAGE
# --------------------------------------------------

story.append(Spacer(1, 1.1*inch))

add_paragraph(
    "FINANCIAL MARKET RISK<br/>"
    "&amp; PORTFOLIO ANALYSIS",
    "CoverTitle"
)

add_paragraph(
    "Portfolio Construction, Risk Measurement and "
    "Out-of-Sample Performance Evaluation",
    "Subtitle"
)

story.append(Spacer(1, 0.5*inch))

add_paragraph(
    "<b>Research Project</b><br/><br/>"
    "Analysis period: November 2021 – November 2026<br/>"
    "Out-of-sample evaluation: January 2025 – November 2026<br/>"
    "Assets: AAPL, AMZN, JPM, MSFT, XOM<br/>"
    "Benchmark: SPY",
    "Subtitle"
)

story.append(Spacer(1, 1.0*inch))

add_paragraph(
    "This project examines how different portfolio construction "
    "approaches affect investment returns and risk. It compares "
    "equal-weight, fixed minimum-variance and rolling "
    "minimum-variance portfolios against a market benchmark.",
    "BodyCustom"
)

story.append(PageBreak())

# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------

add_heading("1. Executive Summary")

add_paragraph(
    "This project investigates portfolio construction and risk "
    "measurement using historical daily price data for five "
    "individual stocks: Apple (AAPL), Amazon (AMZN), JPMorgan "
    "Chase (JPM), Microsoft (MSFT) and Exxon Mobil (XOM). "
    "The SPDR S&amp;P 500 ETF (SPY) serves as the benchmark."
)

add_paragraph(
    "Three portfolio strategies were evaluated: an equal-weight "
    "portfolio, a fixed minimum-variance portfolio and a rolling "
    "minimum-variance portfolio. Their performance was compared "
    "with SPY using a monthly-rebalanced out-of-sample test."
)

add_paragraph(
    "The fixed minimum-variance strategy recorded the highest "
    "compound annual growth rate (CAGR), at 25.26%, and the "
    "highest Sharpe ratio, at 1.44. The rolling minimum-variance "
    "strategy recorded the smallest maximum drawdown, at "
    "−15.22%. These findings describe the historical test period "
    "and should not be interpreted as predictions of future returns."
)

add_table(
    ["Strategy", "CAGR", "Volatility", "Sharpe", "Max. Drawdown"],
    [
        ["Equal-Weight", "21.82%", "18.18%", "1.18", "−20.04%"],
        ["Fixed Min-Variance", "25.26%", "16.65%", "1.44", "−16.95%"],
        ["Rolling Min-Variance", "21.96%", "16.82%", "1.26", "−15.22%"],
        ["SPY", "14.31%", "17.10%", "0.87", "−18.76%"],
    ]
)

# --------------------------------------------------
# OBJECTIVES
# --------------------------------------------------

add_heading("2. Research Objectives")

add_paragraph(
    "The main objectives of the project were to:"
)

for item in [
    "Measure the historical returns and volatility of selected stocks.",
    "Examine relationships between assets using correlation analysis.",
    "Construct an equal-weight portfolio and a minimum-variance portfolio.",
    "Evaluate portfolio performance using return and risk measures.",
    "Test portfolio strategies on data not used for initial optimisation.",
    "Investigate the effects of monthly rebalancing and transaction costs.",
    "Examine sensitivity to different estimation-window lengths.",
    "Compare portfolio performance on positive and negative market days."
]:
    add_paragraph("• " + item)

# --------------------------------------------------
# DATASET
# --------------------------------------------------

add_heading("3. Dataset and Assets")

add_paragraph(
    "Historical adjusted price data were collected using the "
    "Yahoo Finance data source through the Python yfinance library. "
    "The dataset covers 8 November 2021 to 6 November 2026 and "
    "contains 1,255 daily price observations for the six tickers."
)

add_table(
    ["Ticker", "Company / Instrument", "Role"],
    [
        ["AAPL", "Apple Inc.", "Portfolio asset"],
        ["AMZN", "Amazon.com Inc.", "Portfolio asset"],
        ["JPM", "JPMorgan Chase & Co.", "Portfolio asset"],
        ["MSFT", "Microsoft Corporation", "Portfolio asset"],
        ["XOM", "Exxon Mobil Corporation", "Portfolio asset"],
        ["SPY", "SPDR S&P 500 ETF", "Benchmark"],
    ]
)

add_paragraph(
    "Daily returns were calculated from consecutive adjusted "
    "closing prices. The five individual stocks were used to "
    "construct the portfolios, while SPY was used as the "
    "benchmark for comparison."
)

# --------------------------------------------------
# METHODOLOGY
# --------------------------------------------------

add_heading("4. Methodology")

add_subheading("4.1 Daily Returns")

add_paragraph(
    "A daily return measures the percentage change in an asset's "
    "price from one trading day to the next. It was calculated as:"
)

add_paragraph(
    "<b>Daily Return = (Today's Price / Previous Price) − 1</b>"
)

add_subheading("4.2 Annualised Volatility")

add_paragraph(
    "Volatility measures how much returns fluctuate. Daily "
    "standard deviation was multiplied by the square root of "
    "252, representing the approximate number of trading days "
    "in a year."
)

add_subheading("4.3 Sharpe Ratio")

add_paragraph(
    "The Sharpe ratio measures return relative to volatility. "
    "A higher value indicates more historical return per unit "
    "of risk. A zero risk-free rate was assumed in this project."
)

add_subheading("4.4 Maximum Drawdown")

add_paragraph(
    "Maximum drawdown measures the largest percentage decline "
    "from a previous portfolio peak to a subsequent trough. "
    "It provides a measure of historical downside risk."
)

add_subheading("4.5 Compound Annual Growth Rate")

add_paragraph(
    "CAGR represents the constant annual growth rate that would "
    "produce the same overall investment growth over the period."
)

add_subheading("4.6 Minimum-Variance Optimisation")

add_paragraph(
    "The minimum-variance portfolio seeks the combination of "
    "asset weights that produces the lowest estimated portfolio "
    "variance, subject to long-only weights and a total allocation "
    "of 100%. In simple terms, the optimisation attempts to find "
    "a combination of assets with the lowest historical fluctuation."
)

# --------------------------------------------------
# HISTORICAL ANALYSIS
# --------------------------------------------------

add_heading("5. Historical Risk and Return Analysis")

add_paragraph(
    "The historical analysis showed that the selected stocks "
    "had different levels of volatility. Amazon recorded the "
    "highest annualised volatility, while JPMorgan recorded "
    "the lowest among the five individual stocks."
)

add_table(
    ["Asset", "Annualised Volatility"],
    [
        ["AAPL", "28.14%"],
        ["AMZN", "36.73%"],
        ["JPM", "24.43%"],
        ["MSFT", "28.40%"],
        ["XOM", "26.69%"],
        ["SPY", "17.30%"],
    ]
)

add_paragraph(
    "The correlation analysis showed that Exxon Mobil had "
    "relatively low correlations with several technology stocks. "
    "This illustrates how assets from different sectors can "
    "behave differently and potentially contribute to diversification."
)

add_figure(
    "cumulative_wealth.png",
    "Figure 1. Historical growth of an initial investment of $1."
)

add_figure(
    "drawdown_chart.png",
    "Figure 2. Historical drawdowns across the selected assets and portfolio."
)

add_figure(
    "risk_return_scatter.png",
    "Figure 3. Relationship between historical annualised risk and return."
)

# --------------------------------------------------
# PORTFOLIO CONSTRUCTION
# --------------------------------------------------

add_heading("6. Portfolio Construction")

add_subheading("6.1 Equal-Weight Portfolio")

add_paragraph(
    "The equal-weight portfolio allocated 20% of its capital to "
    "each of the five stocks. It provides a straightforward "
    "benchmark for evaluating whether optimisation adds value."
)

add_subheading("6.2 Fixed Minimum-Variance Portfolio")

add_paragraph(
    "The fixed minimum-variance portfolio used the training-period "
    "data from November 2021 through December 2024 to estimate "
    "the portfolio weights. Those target weights were then used "
    "during the out-of-sample test."
)

add_table(
    ["Asset", "Training Weight"],
    [
        ["AAPL", "14.54%"],
        ["AMZN", "0.00%"],
        ["JPM", "30.04%"],
        ["MSFT", "23.39%"],
        ["XOM", "32.02%"],
    ]
)

add_paragraph(
    "The zero allocation to Amazon means that the optimisation "
    "did not select it under the chosen minimum-variance objective "
    "and constraints. It does not mean that Amazon is inherently "
    "a poor investment."
)

add_subheading("6.3 Rolling Minimum-Variance Portfolio")

add_paragraph(
    "The rolling strategy recalculated portfolio weights monthly "
    "using the previous 252 trading days of available data. "
    "This allowed the portfolio allocation to respond to changing "
    "historical risk and correlation estimates."
)

add_figure(
    "rolling_portfolio_allocation.png",
    "Figure 4. Changes in the rolling minimum-variance portfolio allocation."
)

# --------------------------------------------------
# OUT OF SAMPLE
# --------------------------------------------------

add_heading("7. Out-of-Sample Evaluation")

add_paragraph(
    "The dataset was divided into a training period and a test "
    "period. The training period ended on 31 December 2024. "
    "The out-of-sample test began on 2 January 2025 and ended "
    "on 6 November 2026."
)

add_paragraph(
    "Out-of-sample testing is important because it evaluates "
    "a strategy on observations that were not used to estimate "
    "its original fixed portfolio weights. This provides a more "
    "realistic historical assessment than evaluating a strategy "
    "only on the data used to construct it."
)

add_subheading("7.1 Monthly Rebalancing")

add_paragraph(
    "The strategies reset their target allocations at the "
    "beginning of each month. Weights were allowed to drift "
    "between rebalancing dates as asset prices changed. "
    "The SPY benchmark was held without portfolio rebalancing."
)

add_figure(
    "monthly_rebalanced_comparison.png",
    "Figure 5. Out-of-sample growth of $1 under monthly rebalancing."
)

add_heading("8. Out-of-Sample Performance Results")

add_table(
    ["Portfolio", "Annual Return", "Volatility", "Sharpe", "Max DD", "CAGR"],
    [
        ["Equal-Weight", "21.38%", "18.18%", "1.18", "−20.04%", "21.82%"],
        ["Fixed Min-Variance", "23.91%", "16.65%", "1.44", "−16.95%", "25.26%"],
        ["Rolling Min-Variance", "21.27%", "16.82%", "1.26", "−15.22%", "21.96%"],
        ["SPY", "14.83%", "17.10%", "0.87", "−18.76%", "14.31%"],
    ]
)

add_paragraph(
    "The fixed minimum-variance strategy produced the highest "
    "CAGR and Sharpe ratio in this test. It also had the lowest "
    "annualised volatility. The rolling strategy recorded the "
    "smallest maximum drawdown, indicating the shallowest "
    "peak-to-trough decline among the strategies."
)

add_paragraph(
    "The equal-weight portfolio also performed competitively. "
    "Its results demonstrate that a simple allocation rule can "
    "remain a useful comparison against an optimisation-based "
    "approach."
)

# --------------------------------------------------
# TRANSACTION COSTS
# --------------------------------------------------

add_heading("9. Transaction Cost Analysis")

add_paragraph(
    "Transaction costs were modelled at 0, 5, 10 and 25 basis "
    "points. One basis point is equal to 0.01%. The costs were "
    "applied to monthly portfolio turnover."
)

add_table(
    ["Cost", "Equal-Weight CAGR", "Fixed Min-Var CAGR", "Rolling Min-Var CAGR"],
    [
        ["0 bps", "21.82%", "25.26%", "21.96%"],
        ["5 bps", "21.80%", "25.24%", "21.92%"],
        ["10 bps", "21.78%", "25.22%", "21.88%"],
        ["25 bps", "21.73%", "25.17%", "21.77%"],
    ]
)

add_paragraph(
    "The rolling strategy had higher average monthly one-way "
    "turnover than the other two portfolios. Its average monthly "
    "turnover was approximately 5.01%, compared with 2.31% "
    "for equal-weight and 2.33% for fixed minimum-variance."
)

add_paragraph(
    "The tested transaction costs did not materially change "
    "the ranking of the strategies. However, the cost model "
    "is simplified and does not include all real-world trading "
    "expenses."
)

# --------------------------------------------------
# ESTIMATION WINDOW
# --------------------------------------------------

add_heading("10. Estimation-Window Sensitivity")

add_paragraph(
    "The rolling minimum-variance strategy was also evaluated "
    "using different historical estimation windows: 126, 252, "
    "504 and 756 trading days. This examined whether the length "
    "of historical data used to estimate portfolio weights "
    "affected performance."
)

add_table(
    ["Window", "Annual Return", "Volatility", "Sharpe", "Max DD", "CAGR"],
    [
        ["6 Months", "17.60%", "16.62%", "1.06", "−16.23%", "17.61%"],
        ["1 Year", "21.27%", "16.82%", "1.26", "−15.22%", "21.96%"],
        ["2 Years", "22.34%", "17.41%", "1.28", "−16.80%", "23.15%"],
        ["3 Years", "23.22%", "17.00%", "1.37", "−16.84%", "24.33%"],
    ]
)

add_figure(
    "estimation_window_sensitivity.png",
    "Figure 6. Performance sensitivity to the length of the estimation window."
)

add_paragraph(
    "The three-year estimation window recorded the highest "
    "CAGR and Sharpe ratio in this comparison. The one-year "
    "window produced the smallest maximum drawdown. These "
    "results are specific to the selected assets and test period."
)

# --------------------------------------------------
# MARKET CONDITIONS
# --------------------------------------------------

add_heading("11. Market-Condition Analysis")

add_paragraph(
    "Out-of-sample trading days were classified according to "
    "the daily return of SPY. Days with a non-negative SPY "
    "return were classified as positive-market days, while "
    "days with a negative SPY return were classified as "
    "negative-market days."
)

add_paragraph(
    "This is a simple daily classification. It is not a formal "
    "definition of a bull market or bear market."
)

add_table(
    ["Market Condition", "Equal-Weight", "Fixed Min-Var", "Rolling Min-Var", "SPY"],
    [
        ["Positive Market", "0.5833%", "0.4468%", "0.3774%", "0.6963%"],
        ["Negative Market", "−0.5128%", "−0.3270%", "−0.2669%", "−0.7055%"],
    ]
)

add_paragraph(
    "The minimum-variance portfolios experienced smaller average "
    "daily losses on negative SPY days than the benchmark. "
    "The rolling strategy had the smallest average loss on "
    "negative days. On positive days, however, the portfolios "
    "also recorded lower average daily returns than SPY."
)

# --------------------------------------------------
# LIMITATIONS
# --------------------------------------------------

add_heading("12. Limitations")

for item in [
    "The portfolio universe contains only five selected stocks.",
    "The test period represents one historical market environment.",
    "The Sharpe ratio assumes a zero risk-free rate.",
    "The transaction cost model excludes brokerage, bid-ask spreads, taxes and market impact.",
    "The analysis does not establish that the strategies will outperform in future periods.",
    "Historical covariance estimates may change substantially over time.",
    "The asset selection may introduce historical selection bias."
]:
    add_paragraph("• " + item)

# --------------------------------------------------
# CONCLUSION
# --------------------------------------------------

add_heading("13. Conclusion")

add_paragraph(
    "This project demonstrated how portfolio construction, "
    "risk measurement and out-of-sample evaluation can be "
    "combined in a structured financial analysis."
)

add_paragraph(
    "The fixed minimum-variance strategy delivered the strongest "
    "compound growth and risk-adjusted return in the selected "
    "out-of-sample period. The rolling minimum-variance strategy "
    "recorded the smallest maximum drawdown, while the equal-weight "
    "portfolio remained a competitive and relatively simple alternative."
)

add_paragraph(
    "The analysis also showed that portfolio performance depends "
    "on the estimation window, rebalancing frequency and trading "
    "cost assumptions. No single historical result should be "
    "treated as a guarantee of future performance."
)

add_paragraph(
    "Overall, the project provides a practical demonstration "
    "of financial data analysis using Python, including data "
    "preparation, return calculation, portfolio optimisation, "
    "risk measurement, backtesting and visualisation."
)

# --------------------------------------------------
# REFERENCES
# --------------------------------------------------

add_heading("14. References and Tools")

for item in [
    "Yahoo Finance – historical market price data: https://finance.yahoo.com/",
    "yfinance Python library – market data retrieval.",
    "pandas – data manipulation and analysis.",
    "NumPy – numerical computation.",
    "SciPy – numerical optimisation.",
    "Matplotlib – data visualisation."
]:
    add_paragraph("• " + item)

add_paragraph(
    "Note: This report is an educational research project and "
    "does not constitute investment advice.",
    "SmallNote"
)

# --------------------------------------------------
# BUILD PDF
# --------------------------------------------------

doc.build(story, onFirstPage=footer, onLaterPages=footer)

print("Research report created successfully:")
print(OUTPUT)
