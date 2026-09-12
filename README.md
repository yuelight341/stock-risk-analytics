# Stock Risk Analytics
An automated financial analytics pipeline engineered to evaluate risk metrics and generate optimal portfolio allocations using Markowitz Mean-Variance Optimization.

## Features
- Fetches adjusted close prices for any set of tickers plus a benchmark
- Stores raw prices in SQLite; runs analytics via DuckDB
- Computes returns, volatility, Beta, VaR/CVaR, Sharpe/Sortino/Treynor, correlation matrix
- Solves a long-only Markowitz optimization (max Sharpe ratio) using `scipy.optimize`
- Produces CSVs and PNG visualizations in output/

## Stack
- **Languages:** Python, SQL
- **Libraries:** yfinance, Pandas, NumPy, SciPy, SQLite, DuckDB, Matplotlib, Seaborn

## Architecture
```text
    yfinance API
        │
        ▼
    get_data.py  ──►  SQLite (stock_data.db)
        │
        ▼
    optimal_portfolio.py  ──►  SQLite (stock_data.db)
        │
        ▼
    run_queries.py  ──►  DuckDB (attach SQLite, run sql/*.sql)
        │
        ▼
    output/results/*.csv
        │
        ▼
    graphs.py  ──►  output/graphs/*.png
```

All four scripts orchestrated with `analyze.py`

## Structure
```text
stock-risk-analytics/
├── analyze.py                 # Central wrapper script
├── get_data.py                # Gets price data via yfinance → SQLite
├── optimal_portfolio.py       # Long-only Markowitz Mean-Variance Optimization
├── run_queries.py             # Attaches SQLite to DuckDB, runs sql/*.sql
├── graphs.py                  # Generates PNG visualizations
├── sql/
│   ├── 01_annualized_return.sql
│   ├── 02_cumulative_return.sql
│   ├── ...
│   └── 13_correlation_matrix.sql
├── stock_data.db              # SQLite database
└── output/
    ├── results/               # Cleaned, normalized .csv files
    └── graphs/                # .png visualizations
```

## Computed Metrics
Calculates the following performance and risk metrics using SQL:

### Return
- 01: Annualized Returns
- 02: Cumulative Returns
- 03: Jensen's Alpha

### Risk
- 04: Annual Volatility
- 05: Beta
- 06: Best/Worst Day

### Tail Risk
- 07: Max Drawdown
- 08: VaR 95%
- 09: CVaR 95%

### Risk-Adjusted Performance
- 10: Sharpe Ratio
- 11: Sortino Ratio
- 12: Treynor Ratio

### Correlation
- 13: Correlation Matrix

## Installation
**Requires:** Python 3.10+

```bash
git clone https://github.com/<your-username>/stock-risk-analytics.git
cd stock-risk-analytics
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
This process is run via analyze.py

### CLI Arguments
| Argument      | Short | Description                    | Default       |
|---------------|-------|--------------------------------|---------------|
| `tickers`     |   -   | Space-separated ticker symbols | `AAPL MSFT`   |
| `--benchmark` | `-b`  | Benchmark index ticker         | `^GSPC`       |
| `--start`     | `-s`  | Start date (`YYYY-MM-DD`)      | 15 years ago  |
| `--end`       | `-e`  | End date (`YYYY-MM-DD`)        | Today         |

### Examples
#### Basic Run - Defaults to US Tech (AAPL, MSFT) vs. S&P 500
```python3 analyze.py```

#### Custom Tickers & Benchmark - Big 5 Canadian Banks vs. S&P/TSX Composite
```python3 analyze.py RY.TO TD.TO CM.TO BMO.TO BNS.TO -b ^GSPTSE```

#### Custom Date Range
```python3 analyze.py AAPL MSFT -b ^GSPC -s 2020-01-01 -e 2023-01-01```

### Output
After running, two output folders will be generated.
output/results/: Contains cleaned, normalized .csv files for each computed metric.

output/graphs/: Contains .png visualizations of the Wealth Index, Underwater Plot (Drawdowns), Tail Risk Distribution, and Risk/Reward Scatterplot.

#### Example Output Graph
![Risk/Reward Scatterplot](stock-risk-analytics/04_risk_reward.png)
# stock-risk-analytics
